// test_ta_window_round10 -- round 10 (family W, stage 2: onuriano
// macd-stoch-rsi on NYSE:F@15, whose d = ta.sma(k, 3) sits on residue-only
// plateaus): TradingView's sliding-window sum re-sums the window whenever the
// MAGNITUDE of the carried Kahan compensation, ADDED to the incoming source,
// is under-applied -- fire iff c != 0 and |fl(x + |c|) - x| < |c|
// (window_sum.hpp). Round 9's x - c form is the special case where x - c and
// x + |c| round alike; it decides wrongly on residue-only sources, on sources
// within |c| of a power of two and on negative sources.
//
// Pinned 2026-09-06 by pineforge-workflow r9-famW-5 on 21,509 labelled
// decisions: the onuriano and jayentriken NYSE:F@15 oracles (math.sum(stoch,
// 3) 7,018/7,018 and math.sum(k, 3) 7,016/7,016 each, bit-exact), the stdev
// sums (7,029/7,029 x2) and 1,003 lab tv literal replays (dense +-40 ulp
// neighbourhoods of x = 8/3 u, sign mirrors, binade straddles, window lengths
// 3 and 5). Every segment below is TradingView's exact double series: the
// oracle segments start cold at a bar from which this arithmetic reproduces
// TradingView through the decisive bar (where the round-9 form decides the
// other way) and six bars beyond; the literal segments carry TradingView's
// echoed inputs (its decimal-literal parser is not correctly rounded) and its
// printed sums.

#include <pineforge/ta.hpp>
#include <pineforge/math.hpp>
#include <pineforge/na.hpp>

#include <cmath>
#include <cstdio>

#include "test_ta_window_round10_data.hpp"

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
    int decisive = 0;
    for (const Round10Seg& seg : kRound10Segs) {
        math::Sum sum(seg.length);
        ta::SMA sma(seg.length);
        int bad = 0;
        for (int i = 0; i < seg.len; ++i) {
            const double s = sum.compute(seg.x[i]);
            const double m = sma.compute(seg.x[i]);
            if (i < seg.length - 1 || std::isnan(seg.tv[i])) continue;
            if (!same_bits(s, seg.tv[i])) {
                if (bad++ < 3) std::printf("  %s: bar %d math.sum %.17g != TradingView %.17g\n", seg.name, i, s, seg.tv[i]);
            }
            if (!same_bits(m, seg.tv[i] / seg.length)) {
                if (bad++ < 3) std::printf("  %s: bar %d ta.sma %.17g != TradingView %.17g\n", seg.name, i, m, seg.tv[i] / seg.length);
            }
        }
        if (!seg.round9_ok) decisive++;
        char tag[200];
        std::snprintf(tag, sizeof tag, "%s: math.sum / ta.sma bit-exact (%d bad)%s", seg.name, bad,
                      seg.round9_ok ? "" : " [round-9 form decides differently here]");
        CHECK_TRUE(bad == 0, tag);
    }
    // The fixture set must keep exercising the bars that separate the two forms.
    CHECK_TRUE(decisive >= 20, "at least 20 segments where the round-9 x - c form and the round-10 x + |c| form disagree");

    std::printf("test_ta_window_round10: %d passed, %d failed\n", tests_passed, tests_failed);
    return tests_failed == 0 ? 0 : 1;
}
