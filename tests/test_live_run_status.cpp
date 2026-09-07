#include <pineforge/bar.hpp>
#include <pineforge/engine.hpp>
#include <pineforge/pineforge.h>
#include <cstdio>
using namespace pineforge;
namespace {
int failures = 0;
#define CHECK(cond) do { if (!(cond)) { std::fprintf(stderr, "FAIL %s:%d  %s\n", __FILE__, __LINE__, #cond); ++failures; } } while (0)
Bar flat_bar(double p, int64_t ts) { return Bar{p, p, p, p, 1.0, ts}; }
class NoopStrategy final : public BacktestEngine {
public:
    void on_bar(const Bar&) override {}
};
}
int main() {
    CHECK(PF_ABI_VERSION == 4);
    NoopStrategy s;
    CHECK(s.last_run_status() == 0);
    const Bar bars[] = {flat_bar(100.0, 0), flat_bar(101.0, 60'000)};
    s.run(bars, 2);
    CHECK(s.last_error().empty());
    CHECK(s.last_run_status() == 0);
    return failures == 0 ? 0 : 1;
}
