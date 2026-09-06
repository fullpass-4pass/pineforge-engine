// test_ta_window_underapplied -- round 9 (family W, jayentriken stochRSI on
// six lanes): TradingView's sliding-window sum re-sums the window whenever the
// carried Kahan compensation is UNDER-applied to the incoming source
// (round 9: |fl(x - c) - x| < |c|; round 10 pinned the quantity TradingView
// tests as x + |c| -- test_ta_window_round10 -- which decides identically on
// every bar below), and ta.stdev is sqrt(Sxx / n - m * m) over the same
// sliding sums (window_sum.hpp, ta.hpp StdDev). Pinned 2026-09-05 on full-precision
// NYSE:F@15 oracles exported by pineforge-workflow (famw-f15-kdhi-*,
// famw-f15-sd-*: every value is TradingView's exact double, tiny residues
// scaled by 2^60 on export).
//
// Every segment below starts cold at a bar from which the fitted arithmetic
// reproduces TradingView bit-for-bit through the pinned re-sum bar (the
// round-7 trigger misses each one: bars 747, 1156, 2324, 2659, 3362, 4351,
// 4879, 5623 of math.sum(stoch, 3) and 262, 305 of math.sum(k, 3)); the
// stdev segment is the lane's own range start (bar 0 = 2025-04-01 13:30Z).

#include <pineforge/ta.hpp>
#include <pineforge/math.hpp>
#include <pineforge/na.hpp>

#include <cmath>
#include <cstdio>

#include "test_ta_window_underapplied_data.hpp"

using namespace pineforge;

static int tests_passed = 0;
static int tests_failed = 0;

#define CHECK_TRUE(cond, tag) do {                                            \
    if (cond) { tests_passed++; }                                             \
    else { tests_failed++; std::printf("FAIL %s\n", (tag)); }                 \
} while (0)

static bool same_bits(double a, double b) {
    if (std::isnan(a) && std::isnan(b)) return true;
    return a == b && std::signbit(a) == std::signbit(b);
}

int main() {
    // 1. math.sum(x, n) / ta.sma(x, n): the re-sum trigger.
    for (const WindowSumSeg& seg : kWindowSumSegs) {
        math::Sum sum(seg.length);
        ta::SMA sma(seg.length);
        int bad = 0;
        for (int i = 0; i < seg.len; ++i) {
            const double s = sum.compute(seg.x[i]);
            const double m = sma.compute(seg.x[i]);
            if (i < seg.length - 1) continue;
            if (!same_bits(s, seg.tv[i])) {
                if (bad++ < 3) std::printf("  %s: bar %d math.sum %.17g != TradingView %.17g\n", seg.name, i, s, seg.tv[i]);
            }
            if (!same_bits(m, seg.tv[i] / seg.length)) {
                if (bad++ < 3) std::printf("  %s: bar %d ta.sma %.17g != TradingView %.17g\n", seg.name, i, m, seg.tv[i] / seg.length);
            }
        }
        char tag[200];
        std::snprintf(tag, sizeof tag, "%s: math.sum / ta.sma bit-exact (%d bad)", seg.name, bad);
        CHECK_TRUE(bad == 0, tag);
    }

    // 2. ta.stdev(close, 7) = sqrt(Sxx/7 - m*m) over the sliding sums; ta.sma basis = Sx/7.
    for (const StdevSeg& seg : kStdevSegs) {
        math::Sum sx(7), sxx(7);
        ta::SMA basis(7);
        ta::StdDev sd(7);
        int bad = 0;
        for (int i = 0; i < seg.len; ++i) {
            const double c = seg.close[i];
            const double vsx = sx.compute(c);
            const double vsxx = sxx.compute(c * c);
            const double vb = basis.compute(c);
            const double vsd = sd.compute(c);
            if (i < 6) continue;
            if (!same_bits(vsx, seg.tv_sx[i]) || !same_bits(vsxx, seg.tv_sxx[i]) ||
                !same_bits(vb, seg.tv_basis[i]) || !same_bits(vsd, seg.tv_stdev[i])) {
                if (bad++ < 3) std::printf("  %s: bar %d sx %.17g/%.17g sxx %.17g/%.17g basis %.17g/%.17g stdev %.17g/%.17g\n",
                                           seg.name, i, vsx, seg.tv_sx[i], vsxx, seg.tv_sxx[i], vb, seg.tv_basis[i], vsd, seg.tv_stdev[i]);
            }
        }
        char tag[200];
        std::snprintf(tag, sizeof tag, "%s: math.sum(close), math.sum(close*close), ta.sma, ta.stdev bit-exact (%d bad)", seg.name, bad);
        CHECK_TRUE(bad == 0, tag);
    }

    // 3. recompute() replays a bar bit-for-bit (intrabar path): feed each
    //    stdev bar twice (a wrong first tick, then the real source).
    {
        const StdevSeg& seg = kStdevSegs[0];
        ta::StdDev sd(7);
        int bad = 0;
        for (int i = 0; i < seg.len; ++i) {
            sd.compute(seg.close[i] + 0.5);
            const double v = sd.recompute(seg.close[i]);
            if (i >= 6 && !same_bits(v, seg.tv_stdev[i])) bad++;
        }
        CHECK_TRUE(bad == 0, "ta.stdev recompute() replays the bar bit-for-bit");
    }

    std::printf("test_ta_window_underapplied: passed=%d failed=%d\n", tests_passed, tests_failed);
    return tests_failed == 0 ? 0 : 1;
}
