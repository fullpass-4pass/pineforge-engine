// Symbol-clock D/W/M anchors shared by ta.vwap's default anchor,
// timeframe.change, time()/time_close() and request.security period keys.
//
// TradingView's daily bar is the SESSION day: OANDA:EURUSD
// (America/New_York, 1700-1700) opens at 17:00 ET and its week on Sunday
// 17:00 ET; NASDAQ:AAPL (0930-1600) opens 09:30 ET Monday..Friday; a 24x7
// UTC symbol opens at 00:00 UTC. The tz="UTC" + empty/"24x7" session forms
// must stay bit-identical to the pre-existing UTC integer math.
#include <cmath>
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>

#include <pineforge/na.hpp>
#include <pineforge/session_time.hpp>
#include <pineforge/ta.hpp>
#include <pineforge/timeframe.hpp>

using namespace pineforge;

static int tests_passed = 0;
static int tests_failed = 0;

#define CHECK(expr)                                                            \
    do {                                                                        \
        if (!(expr)) {                                                          \
            std::printf("  FAIL  %s:%d  %s\n", __FILE__, __LINE__, #expr);     \
            ++tests_failed;                                                     \
        } else {                                                                \
            ++tests_passed;                                                     \
        }                                                                       \
    } while (0)

#define CHECK_EQ_MS(actual, expected)                                          \
    do {                                                                        \
        const int64_t _a = (actual), _e = (expected);                          \
        if (_a != _e) {                                                         \
            std::printf("  FAIL  %s:%d  %s == %s  (got %lld, want %lld)\n",     \
                        __FILE__, __LINE__, #actual, #expected,                 \
                        (long long)_a, (long long)_e);                          \
            ++tests_failed;                                                     \
        } else {                                                                \
            ++tests_passed;                                                     \
        }                                                                       \
    } while (0)

// Unix ms of a UTC civil date-time (Howard Hinnant's days_from_civil).
static int64_t utc_ms(int y, int m, int d, int h = 0, int mi = 0) {
    y -= (m <= 2);
    long era = (y >= 0 ? y : y - 399) / 400;
    unsigned yoe = (unsigned)(y - era * 400);
    unsigned doy = (153u * (m + (m > 2 ? -3 : 9)) + 2) / 5 + d - 1;
    unsigned doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
    long days = era * 146097L + (long)doe - 719468L;
    return (static_cast<int64_t>(days) * 86400 + h * 3600 + mi * 60) * 1000;
}

static const std::string NY = "America/New_York";
static const std::string FX = "1700-1700";
static const std::string RTH = "0930-1600";
static const std::string UTC = "UTC";
static const std::string NONE;

// ─── Forex: America/New_York 1700-1700 ────────────────────────────────────────

static void test_forex_daily_open_is_17et() {
    std::printf("test_forex_daily_open_is_17et\n");
    // Tue 2025-06-10 03:00 EDT belongs to the session that opened Mon 17:00 EDT.
    const int64_t bar = utc_ms(2025, 6, 10, 7, 0);
    CHECK_EQ_MS(session_period_open_ms(bar, NY, FX, CalendarPeriod::DAY),
                utc_ms(2025, 6, 9, 21, 0));
    // Mon 16:30 EDT is still SUNDAY's session (opened Sun 17:00 EDT).
    CHECK_EQ_MS(session_period_open_ms(utc_ms(2025, 6, 9, 20, 30), NY, FX, CalendarPeriod::DAY),
                utc_ms(2025, 6, 8, 21, 0));
    // The first bar at 17:00 EDT opens the new session.
    CHECK_EQ_MS(session_period_open_ms(utc_ms(2025, 6, 9, 21, 0), NY, FX, CalendarPeriod::DAY),
                utc_ms(2025, 6, 9, 21, 0));
    // UTC midnight is NOT a boundary on this symbol.
    CHECK(session_day_index(utc_ms(2025, 6, 9, 23, 45), NY, FX)
          == session_day_index(utc_ms(2025, 6, 10, 0, 0), NY, FX));
    CHECK(session_day_index(utc_ms(2025, 6, 9, 20, 45), NY, FX)
          != session_day_index(utc_ms(2025, 6, 9, 21, 0), NY, FX));
    // Winter (EST): 17:00 ET == 22:00Z.
    CHECK_EQ_MS(session_period_open_ms(utc_ms(2025, 1, 15, 12, 0), NY, FX, CalendarPeriod::DAY),
                utc_ms(2025, 1, 14, 22, 0));
    // Daily close == next session open (exclusive); time_close reports the last ms.
    CHECK_EQ_MS(session_period_close_ms(bar, NY, FX, CalendarPeriod::DAY),
                utc_ms(2025, 6, 10, 21, 0));
    CHECK_EQ_MS(pine_time_close(bar, "D", "", "", "15", NY, FX),
                utc_ms(2025, 6, 10, 21, 0) - 1);
}

static void test_forex_dst_step() {
    std::printf("test_forex_dst_step\n");
    // US DST began Sun 2025-03-09 07:00Z. Friday before: 17:00 EST == 22:00Z.
    CHECK_EQ_MS(session_period_open_ms(utc_ms(2025, 3, 7, 12, 0), NY, FX, CalendarPeriod::DAY),
                utc_ms(2025, 3, 6, 22, 0));
    // Monday after: the week/day opened Sun 17:00 EDT == 21:00Z.
    CHECK_EQ_MS(session_period_open_ms(utc_ms(2025, 3, 10, 8, 0), NY, FX, CalendarPeriod::DAY),
                utc_ms(2025, 3, 9, 21, 0));
    CHECK_EQ_MS(session_period_open_ms(utc_ms(2025, 3, 10, 8, 0), NY, FX, CalendarPeriod::WEEK),
                utc_ms(2025, 3, 9, 21, 0));
    // Fall back: DST ended Sun 2025-11-02 06:00Z. Monday 2025-11-03 bar ->
    // Sun 17:00 EST == 22:00Z.
    CHECK_EQ_MS(session_period_open_ms(utc_ms(2025, 11, 3, 10, 0), NY, FX, CalendarPeriod::DAY),
                utc_ms(2025, 11, 2, 22, 0));
    // Friday before fall-back: Thu 17:00 EDT == 21:00Z.
    CHECK_EQ_MS(session_period_open_ms(utc_ms(2025, 10, 31, 10, 0), NY, FX, CalendarPeriod::DAY),
                utc_ms(2025, 10, 30, 21, 0));
}

static void test_forex_week_opens_sunday_17et() {
    std::printf("test_forex_week_opens_sunday_17et\n");
    const int64_t sun_open = utc_ms(2025, 6, 8, 21, 0);
    CHECK_EQ_MS(session_period_open_ms(utc_ms(2025, 6, 10, 7, 0), NY, FX, CalendarPeriod::WEEK), sun_open);
    CHECK_EQ_MS(session_period_open_ms(utc_ms(2025, 6, 8, 22, 0), NY, FX, CalendarPeriod::WEEK), sun_open);
    CHECK_EQ_MS(session_period_open_ms(utc_ms(2025, 6, 13, 20, 45), NY, FX, CalendarPeriod::WEEK), sun_open);
    // Friday 16:45 EDT of the previous week.
    CHECK_EQ_MS(session_period_open_ms(utc_ms(2025, 6, 6, 20, 45), NY, FX, CalendarPeriod::WEEK),
                utc_ms(2025, 6, 1, 21, 0));
    // Weekly close == next Sunday open.
    CHECK_EQ_MS(session_period_close_ms(utc_ms(2025, 6, 10, 7, 0), NY, FX, CalendarPeriod::WEEK),
                utc_ms(2025, 6, 15, 21, 0));
    // tf_change("W") fires on the Sunday open, not at Monday 00:00Z.
    CHECK(tf_change(utc_ms(2025, 6, 6, 20, 45), utc_ms(2025, 6, 8, 21, 0), "W", NY, FX));
    CHECK(!tf_change(utc_ms(2025, 6, 8, 21, 0), utc_ms(2025, 6, 9, 0, 0), "W", NY, FX));
    CHECK(!tf_change(utc_ms(2025, 6, 8, 21, 0), utc_ms(2025, 6, 9, 21, 15), "W", NY, FX));
}

static void test_forex_month_opens_on_trading_date() {
    std::printf("test_forex_month_opens_on_trading_date\n");
    // July 1 2025 is a Tuesday: its daily bar opens Mon Jun 30 17:00 EDT.
    const int64_t jul_open = utc_ms(2025, 6, 30, 21, 0);
    CHECK_EQ_MS(session_period_open_ms(utc_ms(2025, 7, 10, 7, 0), NY, FX, CalendarPeriod::MONTH), jul_open);
    CHECK_EQ_MS(session_period_open_ms(utc_ms(2025, 6, 30, 21, 0), NY, FX, CalendarPeriod::MONTH), jul_open);
    // Mon Jun 30 16:45 EDT is still June.
    CHECK_EQ_MS(session_period_open_ms(utc_ms(2025, 6, 30, 20, 45), NY, FX, CalendarPeriod::MONTH),
                utc_ms(2025, 5, 31, 21, 0));   // June 1 is a Sunday: nominal Sat-open session
    // Aug 1 2025 is a Friday -> Thu Jul 31 17:00 EDT.
    CHECK_EQ_MS(session_period_close_ms(utc_ms(2025, 7, 10, 7, 0), NY, FX, CalendarPeriod::MONTH),
                utc_ms(2025, 7, 31, 21, 0));
    // timeframe.change("M") / security M keys agree with the open.
    CHECK(tf_change(utc_ms(2025, 6, 30, 20, 45), utc_ms(2025, 6, 30, 21, 0), "M", NY, FX));
    CHECK(!tf_change(utc_ms(2025, 6, 30, 21, 0), utc_ms(2025, 7, 1, 0, 0), "M", NY, FX));
    CHECK(!tf_change(utc_ms(2025, 7, 1, 20, 45), utc_ms(2025, 7, 1, 21, 15), "M", NY, FX));
    CHECK(crosses_boundary(utc_ms(2025, 6, 30, 20, 45), utc_ms(2025, 6, 30, 21, 0),
                           CalendarPeriod::MONTH, NY, FX));
    // Year roll: Jan 1 2026 is a Thursday -> Wed Dec 31 17:00 EST == 22:00Z.
    CHECK_EQ_MS(session_period_open_ms(utc_ms(2026, 1, 8, 12, 0), NY, FX, CalendarPeriod::MONTH),
                utc_ms(2025, 12, 31, 22, 0));
}

static void test_forex_tf_change_daily() {
    std::printf("test_forex_tf_change_daily\n");
    CHECK(tf_change(utc_ms(2025, 6, 9, 20, 45), utc_ms(2025, 6, 9, 21, 0), "D", NY, FX));
    CHECK(tf_change(utc_ms(2025, 6, 9, 20, 45), utc_ms(2025, 6, 9, 21, 0), "1D", NY, FX));
    CHECK(!tf_change(utc_ms(2025, 6, 9, 23, 45), utc_ms(2025, 6, 10, 0, 0), "D", NY, FX));
    // The tz-less form is the UTC-midnight rule (corpus regime).
    CHECK(tf_change(utc_ms(2025, 6, 9, 23, 45), utc_ms(2025, 6, 10, 0, 0), "D"));
    CHECK(!tf_change(utc_ms(2025, 6, 9, 20, 45), utc_ms(2025, 6, 9, 21, 0), "D"));
}

static void test_forex_pine_time_symbol_clock() {
    std::printf("test_forex_pine_time_symbol_clock\n");
    const int64_t bar = utc_ms(2025, 6, 10, 7, 0);   // Tue 03:00 EDT
    CHECK_EQ_MS(pine_time(bar, "D", "", "", "15", NY, FX), utc_ms(2025, 6, 9, 21, 0));
    CHECK_EQ_MS(pine_time(bar, "1D", "", "", "15", NY, FX), utc_ms(2025, 6, 9, 21, 0));
    CHECK_EQ_MS(pine_time(bar, "W", "", "", "15", NY, FX), utc_ms(2025, 6, 8, 21, 0));
    // Two-arg time("D", "<tz>") — a timezone in the session slot is not a
    // session: filter dropped, open still the symbol's daily bar.
    CHECK_EQ_MS(pine_time(bar, "D", "Europe/Prague", "", "15", NY, FX), utc_ms(2025, 6, 9, 21, 0));
    // A VALID session argument defines the day in ITS timezone (TV keys
    // `time("D", "0000-2359", "America/New_York")` on New York midnight —
    // measured on lukeborgerding-orb-avwap-retest, 100% vs 18%): the
    // tz-only calendar floor of the 5-arg forms, na outside the window.
    CHECK_EQ_MS(pine_time(utc_ms(2025, 6, 10, 14, 0), "D", RTH, NY, "15", NY, FX),
                pine_time(utc_ms(2025, 6, 10, 14, 0), "D", RTH, NY, "15"));
    CHECK_EQ_MS(pine_time(utc_ms(2025, 6, 10, 14, 0), "D", RTH, NY, "15", NY, FX),
                utc_ms(2025, 6, 10, 4, 0));
    CHECK(is_na(pine_time(bar, "D", RTH, NY, "15", NY, FX)));
    // Same on a UTC/24x7 symbol: the session's tz rolls the day, not UTC.
    CHECK_EQ_MS(pine_time(utc_ms(2025, 6, 10, 1, 0), "D", "0000-2359", NY, "15", UTC, "24x7"),
                utc_ms(2025, 6, 9, 4, 0));
    CHECK_EQ_MS(pine_time_close(utc_ms(2025, 6, 10, 1, 0), "D", "0000-2359", NY, "15", UTC, "24x7"),
                pine_time_close(utc_ms(2025, 6, 10, 1, 0), "D", "0000-2359", NY, "15"));
    // Intraday tfs sit on the symbol's day-stamp-anchored HTF grid, the one
    // request.security aggregates on. (Re-pinned: the rule "intraday tfs
    // keep the epoch grid" arrived with b1449c3 as a design statement with
    // no tape behind it, and this "60" check on 1700-1700 never told the two
    // grids apart -- 17:00 ET is on the hour in EDT and EST. pin-time-hours
    // on NYSE:F / NSE:NIFTY / OANDA:XAUUSD 15, 2025-04-01..07-01, reads the
    // session-anchored grid on every session symbol; see
    // test_pine_time_day_stamp_grid.) On forex "60" still coincides with
    // the epoch hour; "240" is the 17:00-ET-anchored grid: Tue 03:00 EDT
    // sits in the 01:00-05:00 EDT bucket, not the epoch 04:00Z-08:00Z one.
    CHECK_EQ_MS(pine_time(bar, "60", "", "", "15", NY, FX), pine_time(bar, "60", "", "", "15"));
    CHECK_EQ_MS(pine_time(bar, "240", "", "", "15", NY, FX), utc_ms(2025, 6, 10, 5, 0));
    CHECK_EQ_MS(pine_time_close(bar, "240", "", "", "15", NY, FX), utc_ms(2025, 6, 10, 9, 0));
    CHECK_EQ_MS(pine_time(bar, "240", "", "", "15"), utc_ms(2025, 6, 10, 4, 0));
    // Empty tf falls back to the chart tf.
    CHECK_EQ_MS(pine_time(bar, "", "", "", "D", NY, FX), utc_ms(2025, 6, 9, 21, 0));
}

// ─── Equities: America/New_York 0930-1600 ─────────────────────────────────────

static void test_equity_daily_open_is_0930et() {
    std::printf("test_equity_daily_open_is_0930et\n");
    const int64_t bar = utc_ms(2025, 6, 10, 14, 0);   // Tue 10:00 EDT
    CHECK_EQ_MS(session_period_open_ms(bar, NY, RTH, CalendarPeriod::DAY), utc_ms(2025, 6, 10, 13, 30));
    CHECK_EQ_MS(pine_time(bar, "D", "", "", "15", NY, RTH), utc_ms(2025, 6, 10, 13, 30));
    // Close == 16:00 ET, not the next session open.
    CHECK_EQ_MS(session_period_close_ms(bar, NY, RTH, CalendarPeriod::DAY), utc_ms(2025, 6, 10, 20, 0));
    CHECK_EQ_MS(pine_time_close(bar, "D", "", "", "15", NY, RTH), utc_ms(2025, 6, 10, 20, 0) - 1);
    // Winter: 09:30 EST == 14:30Z.
    CHECK_EQ_MS(session_period_open_ms(utc_ms(2025, 1, 15, 15, 0), NY, RTH, CalendarPeriod::DAY),
                utc_ms(2025, 1, 15, 14, 30));
    // Session-day advances between Friday's last bar and Monday's first.
    CHECK(session_day_index(utc_ms(2025, 6, 6, 19, 45), NY, RTH)
          != session_day_index(utc_ms(2025, 6, 9, 13, 30), NY, RTH));
    CHECK(session_day_index(utc_ms(2025, 6, 9, 13, 30), NY, RTH)
          == session_day_index(utc_ms(2025, 6, 9, 19, 45), NY, RTH));
    CHECK(tf_change(utc_ms(2025, 6, 9, 19, 45), utc_ms(2025, 6, 10, 13, 30), "D", NY, RTH));
    CHECK(!tf_change(utc_ms(2025, 6, 10, 13, 30), utc_ms(2025, 6, 10, 13, 45), "D", NY, RTH));
}

static void test_equity_week_and_month_open_monday_first() {
    std::printf("test_equity_week_and_month_open_monday_first\n");
    const int64_t bar = utc_ms(2025, 6, 11, 14, 0);   // Wed
    CHECK_EQ_MS(session_period_open_ms(bar, NY, RTH, CalendarPeriod::WEEK), utc_ms(2025, 6, 9, 13, 30));
    CHECK_EQ_MS(pine_time(bar, "W", "", "", "15", NY, RTH), utc_ms(2025, 6, 9, 13, 30));
    CHECK_EQ_MS(session_period_close_ms(bar, NY, RTH, CalendarPeriod::WEEK), utc_ms(2025, 6, 16, 13, 30));
    // July 1 2025 (Tuesday) 09:30 EDT.
    CHECK_EQ_MS(session_period_open_ms(utc_ms(2025, 7, 10, 14, 0), NY, RTH, CalendarPeriod::MONTH),
                utc_ms(2025, 7, 1, 13, 30));
    CHECK(tf_change(utc_ms(2025, 6, 30, 19, 45), utc_ms(2025, 7, 1, 13, 30), "M", NY, RTH));
    CHECK(!tf_change(utc_ms(2025, 6, 27, 19, 45), utc_ms(2025, 6, 30, 13, 30), "M", NY, RTH));
    CHECK(tf_change(utc_ms(2025, 6, 6, 19, 45), utc_ms(2025, 6, 9, 13, 30), "W", NY, RTH));
    CHECK(!tf_change(utc_ms(2025, 6, 9, 19, 45), utc_ms(2025, 6, 10, 13, 30), "W", NY, RTH));
}

// ─── East-of-UTC exchange (Asia/Tokyo 0900-1530) ──────────────────────────────

static void test_tokyo_open_on_previous_utc_date() {
    std::printf("test_tokyo_open_on_previous_utc_date\n");
    const std::string TK = "Asia/Tokyo", JP = "0900-1530";
    const int64_t bar = utc_ms(2025, 6, 10, 1, 0);   // Tue 10:00 JST
    CHECK_EQ_MS(session_period_open_ms(bar, TK, JP, CalendarPeriod::DAY), utc_ms(2025, 6, 10, 0, 0));
    CHECK_EQ_MS(session_period_open_ms(bar, TK, JP, CalendarPeriod::WEEK), utc_ms(2025, 6, 9, 0, 0));
    // Tue Jul 1 09:00 JST == Mon Jun 30 24:00Z: the month open sits on the
    // previous UTC date and must still resolve to July.
    CHECK_EQ_MS(session_period_open_ms(utc_ms(2025, 7, 10, 1, 0), TK, JP, CalendarPeriod::MONTH),
                utc_ms(2025, 7, 1, 0, 0));
    CHECK_EQ_MS(session_period_close_ms(bar, TK, JP, CalendarPeriod::DAY), utc_ms(2025, 6, 10, 6, 30));
}

// ─── 24x7 / UTC identity ──────────────────────────────────────────────────────

static void test_utc_identity_with_tz_less_forms() {
    std::printf("test_utc_identity_with_tz_less_forms\n");
    const char* tfs[] = {"D", "1D", "W", "1W", "M", "1M", "60", "240", "15"};
    const std::string sessions[] = {NONE, "24x7"};
    int64_t ms = utc_ms(2024, 12, 20, 0, 0);
    const int64_t end = utc_ms(2025, 3, 20, 0, 0);
    int checked = 0;
    for (; ms < end; ms += 7 * 3600000LL + 37 * 60000LL) {
        for (const auto& sess : sessions) {
            CHECK_EQ_MS(session_period_open_ms(ms, UTC, sess, CalendarPeriod::DAY),
                        pine_time(ms, "D", "", "", "15"));
            CHECK_EQ_MS(session_period_open_ms(ms, UTC, sess, CalendarPeriod::WEEK),
                        pine_time(ms, "W", "", "", "15"));
            CHECK_EQ_MS(session_period_open_ms(ms, UTC, sess, CalendarPeriod::MONTH),
                        pine_time(ms, "M", "", "", "15"));
            CHECK_EQ_MS(session_day_index(ms, UTC, sess), ms / kMsPerDay);
            CHECK_EQ_MS(session_day_index(ms, NONE, sess), ms / kMsPerDay);
            for (const char* tf : tfs) {
                CHECK_EQ_MS(pine_time(ms, tf, "", "", "15", UTC, sess),
                            pine_time(ms, tf, "", "", "15"));
                CHECK_EQ_MS(pine_time_close(ms, tf, "", "", "15", UTC, sess),
                            pine_time_close(ms, tf, "", "", "15"));
                CHECK(tf_change(ms, ms + 900000, tf, UTC, sess) == tf_change(ms, ms + 900000, tf));
                CHECK(tf_change(ms, ms + 86400000LL, tf, UTC, sess) == tf_change(ms, ms + 86400000LL, tf));
            }
            ++checked;
        }
    }
    CHECK(checked > 200);
}

static void test_vwap_utc_identity_and_forex_reset() {
    std::printf("test_vwap_utc_identity_and_forex_reset\n");
    // Identity: the tz/session overload with UTC + 24x7 reproduces the tz-less
    // sequence bit-for-bit (including the recompute path).
    ta::VWAP a, b;
    int64_t ms = utc_ms(2025, 6, 8, 12, 0);
    double px = 1.1000, vol = 100.0;
    for (int i = 0; i < 400; ++i, ms += 900000) {
        px += ((i * 7919) % 13 - 6) * 0.0001;
        vol = 50.0 + (i * 31) % 97;
        double va = a.compute(px, vol, ms);
        double vb = b.compute(px, vol, ms, UTC, "24x7");
        CHECK(std::memcmp(&va, &vb, sizeof(double)) == 0);
        if (i % 5 == 0) {
            double ra = a.recompute(px + 0.0002, vol, ms);
            double rb = b.recompute(px + 0.0002, vol, ms, UTC, "24x7");
            CHECK(std::memcmp(&ra, &rb, sizeof(double)) == 0);
        }
    }
    // Forex: the cumulator resets at 17:00 ET (21:00Z in June), not 00:00Z.
    ta::VWAP fx;
    fx.compute(1.10, 100.0, utc_ms(2025, 6, 9, 20, 30), NY, FX);
    fx.compute(1.20, 100.0, utc_ms(2025, 6, 9, 20, 45), NY, FX);
    double v = fx.compute(1.30, 100.0, utc_ms(2025, 6, 9, 21, 0), NY, FX);
    CHECK(v == 1.30);   // fresh session: vwap == src
    v = fx.compute(1.50, 100.0, utc_ms(2025, 6, 9, 23, 45), NY, FX);
    CHECK(v == 1.40);
    v = fx.compute(1.70, 100.0, utc_ms(2025, 6, 10, 0, 0), NY, FX);
    CHECK(v == 1.50);   // no reset at UTC midnight
    // Bands form resets on the same key.
    ta::VWAP fb;
    fb.compute_bands(1.10, 100.0, utc_ms(2025, 6, 9, 20, 45), 1.0, NY, FX);
    ta::VWAPBandsResult r = fb.compute_bands(1.30, 100.0, utc_ms(2025, 6, 9, 21, 0), 1.0, NY, FX);
    CHECK(r.vwap == 1.30);
    CHECK(r.upper - 1.30 < 1e-6 && 1.30 - r.lower < 1e-6);   // single-bar stdev ~ 0 (fp)
    // Equities: reset at 09:30 ET between Friday's last bar and Monday's first.
    ta::VWAP eq;
    eq.compute(200.0, 100.0, utc_ms(2025, 6, 6, 19, 45), NY, RTH);
    v = eq.compute(210.0, 100.0, utc_ms(2025, 6, 9, 13, 30), NY, RTH);
    CHECK(v == 210.0);
    v = eq.compute(230.0, 100.0, utc_ms(2025, 6, 9, 13, 45), NY, RTH);
    CHECK(v == 220.0);
}

// TradingView's OWN ta.vwap values on OANDA:EURUSD 15m, checked against the
// registry feed's bars (round 10 family AF).
//
// The synthetic reset checks above pin WHEN the cumulator rolls; this pins the
// VALUE it produces, against numbers TradingView printed itself. A `lab tv`
// sensor (scratchpad/r10/famAF/pins/famaf-eur-apr05.pine) ran
// `vw = ta.vwap(close)` over the probe's own window (2025-04-01..2026-05-01)
// and encoded ema9/vwap/cross flags per bar into the order comments; the close
// and volume of every bar below are the registry feed's
// (f945f31a140aedc64ca24e2ace42b9885a914ce31a2531f74179b703c025a648) and match
// the sensor's echoed values exactly.
//
// The slice starts on the session open, Sunday 2026-04-05 21:00Z = 17:00 EDT:
// TradingView reports vwap == that bar's own close there, so the cumulator is
// demonstrably empty and this table is self-contained.
//
// Two anchors are excluded by TradingView's own numbers:
//   * UTC day  -- at 2026-04-06 00:00Z TV reports 1.151216085569, NOT the
//     bar's close 1.15156 that a midnight reset would give (asserted below).
//   * chart timezone -- the tape this came from is stamped UTC+8, whose day
//     rolls at 16:00Z; TV does not reset there either (23:45Z -> 00:00Z runs
//     straight through, and 2026-04-05 21:00Z resets instead).
// Recomputing the whole probe under a UTC-day anchor reproduces only 372 of
// TradingView's 1346 entry bars; under this 17:00-New-York session day it
// reproduces all 1346.
struct EurVwapBar {
    int64_t ts_ms;
    double close;
    double volume;
    double tv_vwap;   // TradingView's ta.vwap(close), 12 decimals as printed
};

static void test_vwap_oanda_eurusd_matches_tradingview() {
    std::printf("test_vwap_oanda_eurusd_matches_tradingview\n");
    static const EurVwapBar kBars[] = {
    { 1775422800000LL, 1.15232, 27.0, 1.15232 },  // 2026-04-05 21:00Z
    { 1775423700000LL, 1.15228, 85.0, 1.152289642857 },  // 2026-04-05 21:15Z
    { 1775424600000LL, 1.15206, 272.0, 1.152126979167 },  // 2026-04-05 21:30Z
    { 1775425500000LL, 1.15213, 29.0, 1.152127191283 },  // 2026-04-05 21:45Z
    { 1775426400000LL, 1.15106, 2001.0, 1.151242580779 },  // 2026-04-05 22:00Z
    { 1775427300000LL, 1.15114, 2445.0, 1.151190963161 },  // 2026-04-05 22:15Z
    { 1775428200000LL, 1.15114, 1988.0, 1.151176166204 },  // 2026-04-05 22:30Z
    { 1775429100000LL, 1.1515, 859.0, 1.151212264469 },  // 2026-04-05 22:45Z
    { 1775430000000LL, 1.15124, 1054.0, 1.151215601598 },  // 2026-04-05 23:00Z
    { 1775430900000LL, 1.15094, 748.0, 1.151193919857 },  // 2026-04-05 23:15Z
    { 1775431800000LL, 1.15094, 776.0, 1.151174759821 },  // 2026-04-05 23:30Z
    { 1775432700000LL, 1.15098, 972.0, 1.151157941542 },  // 2026-04-05 23:45Z
    { 1775433600000LL, 1.15156, 1903.0, 1.151216085569 },  // 2026-04-06 00:00Z
    { 1775434500000LL, 1.1515, 1218.0, 1.151240138416 },  // 2026-04-06 00:15Z
    { 1775435400000LL, 1.15164, 1105.0, 1.151268677819 },  // 2026-04-06 00:30Z
    { 1775436300000LL, 1.15118, 1046.0, 1.151263065707 },  // 2026-04-06 00:45Z
    { 1775437200000LL, 1.15084, 1410.0, 1.151229811016 },  // 2026-04-06 01:00Z
    { 1775438100000LL, 1.15105, 1138.0, 1.15121908419 },  // 2026-04-06 01:15Z
    { 1775439000000LL, 1.15089, 908.0, 1.151204131805 },  // 2026-04-06 01:30Z
    { 1775439900000LL, 1.1507, 573.0, 1.151190079778 },  // 2026-04-06 01:45Z
    { 1775440800000LL, 1.15194, 2307.0, 1.151265747463 },  // 2026-04-06 02:00Z
    { 1775441700000LL, 1.15244, 2498.0, 1.151381404069 },  // 2026-04-06 02:15Z
    { 1775442600000LL, 1.1521, 1318.0, 1.151416902924 },  // 2026-04-06 02:30Z
    { 1775443500000LL, 1.15206, 1277.0, 1.151446277855 },  // 2026-04-06 02:45Z
    { 1775444400000LL, 1.15214, 777.0, 1.15146503689 },  // 2026-04-06 03:00Z
    };
    const int n = (int)(sizeof(kBars) / sizeof(kBars[0]));
    // TV prints 12 decimals on a ~1.15 quote, so half an ulp of the printed
    // value is 5e-13; allow that and nothing more.
    const double kTol = 5e-13;

    ta::VWAP vw;
    for (int i = 0; i < n; ++i) {
        const double got = vw.compute(kBars[i].close, kBars[i].volume, kBars[i].ts_ms, NY, FX);
        const double want = kBars[i].tv_vwap;
        if (!(std::fabs(got - want) <= kTol)) {
            std::printf("  FAIL  %s:%d  bar %d (ts %lld): vwap %.12f, TradingView %.12f\n",
                        __FILE__, __LINE__, i, (long long)kBars[i].ts_ms, got, want);
            ++tests_failed;
        } else {
            ++tests_passed;
        }
    }
    // The session's first bar carries its own close: the reset bar is not
    // seeded from the previous session.
    CHECK(kBars[0].tv_vwap == kBars[0].close);

    // Negative control -- a UTC-day anchor is a different series. Replaying the
    // same bars with the tz-less (UTC-keyed) overload must diverge at the first
    // bar of the new UTC day, 2026-04-06 00:00Z, where it resets to that bar's
    // own close while TradingView keeps cumulating.
    ta::VWAP utc_vw;
    double utc_at_midnight = na<double>();
    double session_at_midnight = na<double>();
    ta::VWAP session_vw;
    for (int i = 0; i < n; ++i) {
        const double u = utc_vw.compute(kBars[i].close, kBars[i].volume, kBars[i].ts_ms);
        const double s = session_vw.compute(kBars[i].close, kBars[i].volume, kBars[i].ts_ms, NY, FX);
        if (kBars[i].ts_ms == utc_ms(2026, 4, 6, 0, 0)) {
            utc_at_midnight = u;
            session_at_midnight = s;
        }
    }
    CHECK(!is_na(utc_at_midnight));
    CHECK(utc_at_midnight == 1.15156);                              // reset to the bar's close
    CHECK(std::fabs(session_at_midnight - 1.151216085569) <= kTol); // TradingView's value
    CHECK(std::fabs(utc_at_midnight - session_at_midnight) > 1e-4);

    // The 2026-04-05 22:00Z bar is the one family AF was opened on: the engine
    // sees ema9 above vwap and enters, TradingView computes the same crossover
    // (its sensor row reads d=+0.00060587593021|CO) and then declines the
    // order at percent_of_equity=100. The vwap underneath it is identical, so
    // that residual is an admission question, not a ta.vwap one.
    ta::VWAP probe;
    double v2200 = na<double>();
    for (int i = 0; i < n; ++i) {
        const double v = probe.compute(kBars[i].close, kBars[i].volume, kBars[i].ts_ms, NY, FX);
        if (kBars[i].ts_ms == utc_ms(2026, 4, 5, 22, 0)) v2200 = v;
    }
    CHECK(std::fabs(v2200 - 1.151242580779) <= kTol);
}

static void test_session_length_edge_cases() {
    std::printf("test_session_length_edge_cases\n");
    // "0000-0000" is a full day whose trading date is its open date.
    const std::string ALLDAY = "0000-0000";
    CHECK_EQ_MS(session_period_open_ms(utc_ms(2025, 6, 10, 7, 0), UTC, ALLDAY, CalendarPeriod::DAY),
                utc_ms(2025, 6, 10, 0, 0));
    CHECK_EQ_MS(session_period_close_ms(utc_ms(2025, 6, 10, 7, 0), UTC, ALLDAY, CalendarPeriod::DAY),
                utc_ms(2025, 6, 11, 0, 0));
    CHECK_EQ_MS(session_period_open_ms(utc_ms(2025, 6, 10, 7, 0), UTC, ALLDAY, CalendarPeriod::WEEK),
                utc_ms(2025, 6, 9, 0, 0));
    // A 1800-1700 session wraps midnight like forex: trading date == close
    // date, the day closing 17:00 ET. (Re-pinned: b1449c3 wrote this parser
    // edge case as "CME-style" with the New York zone, which makes it
    // OANDA's 1800-1700 metals session -- whose D bar is stamped at the
    // 17:00 ET roll an hour before it trades, so its D / W open is the
    // stamp: pin-time-hours on OANDA:XAUUSD, see test_pine_time_day_stamp_grid.
    // A real CME session is 1700-1600 America/Chicago, whose open IS its
    // stamp; test_pine_time_day_stamp_grid rule E pins that grid.)
    const std::string CME = "1800-1700";
    CHECK_EQ_MS(session_period_open_ms(utc_ms(2025, 6, 10, 7, 0), NY, CME, CalendarPeriod::DAY),
                utc_ms(2025, 6, 9, 21, 0));
    CHECK_EQ_MS(session_period_close_ms(utc_ms(2025, 6, 10, 7, 0), NY, CME, CalendarPeriod::DAY),
                utc_ms(2025, 6, 10, 21, 0));
    CHECK_EQ_MS(session_period_open_ms(utc_ms(2025, 6, 10, 7, 0), NY, CME, CalendarPeriod::WEEK),
                utc_ms(2025, 6, 8, 21, 0));
    // Day-of-week suffix does not disturb parsing.
    CHECK_EQ_MS(session_period_open_ms(utc_ms(2025, 6, 10, 14, 0), NY, "0930-1600:23456", CalendarPeriod::DAY),
                utc_ms(2025, 6, 10, 13, 30));
}

int main() {
    std::printf("=== Session-day anchor tests ===\n\n");
    test_forex_daily_open_is_17et();
    test_forex_dst_step();
    test_forex_week_opens_sunday_17et();
    test_forex_month_opens_on_trading_date();
    test_forex_tf_change_daily();
    test_forex_pine_time_symbol_clock();
    test_equity_daily_open_is_0930et();
    test_equity_week_and_month_open_monday_first();
    test_tokyo_open_on_previous_utc_date();
    test_utc_identity_with_tz_less_forms();
    test_vwap_utc_identity_and_forex_reset();
    test_vwap_oanda_eurusd_matches_tradingview();
    test_session_length_edge_cases();
    std::printf("\n=== Results: %d passed, %d failed ===\n", tests_passed, tests_failed);
    return tests_failed > 0 ? 1 : 0;
}
