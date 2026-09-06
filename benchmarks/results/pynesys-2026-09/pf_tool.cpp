// pf_tool: in-process PineForge timer / parameter sweep over one strategy .so.
//   pf_tool time  <strategy.so> <ohlcv.csv> <iters>                 -> JSON {bars, iters, ns:[...]}
//   pf_tool sweep <strategy.so> <ohlcv.csv> <input> <v1,v2,...>    -> JSON {bars, n, totalNs, perNs:[...], trades:[...]}
// Loads the CSV once; each iteration = strategy_create + (set_input) + run_backtest + report_free + strategy_free.
#include <pineforge/pineforge.h>
#include <dlfcn.h>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
using fn_create = pf_strategy_t (*)(const char*);
using fn_run = void (*)(pf_strategy_t, pf_bar_t*, int, pf_report_t*);
using fn_rfree = void (*)(pf_report_t*);
using fn_sfree = void (*)(pf_strategy_t);
using fn_setin = void (*)(pf_strategy_t, const char*, const char*);
static std::vector<pf_bar_t> load(const char* p) {
  std::vector<pf_bar_t> v; std::ifstream f(p); std::string line; std::getline(f, line);
  while (std::getline(f, line)) { pf_bar_t b; char* s = line.data(); b.timestamp = strtoll(s, &s, 10); s++; b.open = strtod(s, &s); s++; b.high = strtod(s, &s); s++; b.low = strtod(s, &s); s++; b.close = strtod(s, &s); s++; b.volume = strtod(s, &s); v.push_back(b); }
  return v;
}
int main(int argc, char** argv) {
  if (argc < 5) { fprintf(stderr, "usage\n"); return 2; }
  void* h = dlopen(argv[2], RTLD_NOW | RTLD_LOCAL); if (!h) { fprintf(stderr, "dlopen: %s\n", dlerror()); return 1; }
  auto create = (fn_create)dlsym(h, "strategy_create"); auto run = (fn_run)dlsym(h, "run_backtest"); auto rfree = (fn_rfree)dlsym(h, "report_free"); auto sfree = (fn_sfree)dlsym(h, "strategy_free"); auto setin = (fn_setin)dlsym(h, "strategy_set_input");
  if (!create || !run || !rfree || !sfree) { fprintf(stderr, "missing ABI symbols\n"); return 1; }
  auto bars = load(argv[3]); std::string mode = argv[1];
  if (mode == "time") {
    int iters = atoi(argv[4]); printf("{\"bars\":%zu,\"iters\":%d,\"ns\":[", bars.size(), iters);
    for (int i = 0; i < iters; i++) { auto t0 = std::chrono::steady_clock::now(); pf_strategy_t s = create(nullptr); pf_report_t r; memset(&r, 0, sizeof r); run(s, bars.data(), (int)bars.size(), &r); long long tr = r.total_trades; rfree(&r); sfree(s); auto ns = std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::steady_clock::now() - t0).count(); printf("%s%lld", i ? "," : "", (long long)ns); if (i == 0) fprintf(stderr, "trades=%lld\n", tr); }
    printf("]}\n");
  } else {
    if (!setin) { fprintf(stderr, "no strategy_set_input\n"); return 1; }
    std::vector<std::string> vals; std::stringstream ss(argv[5]); std::string tok; while (std::getline(ss, tok, ',')) vals.push_back(tok);
    auto T0 = std::chrono::steady_clock::now(); printf("{\"bars\":%zu,\"n\":%zu,\"perNs\":[", bars.size(), vals.size()); std::vector<long long> trades;
    for (size_t i = 0; i < vals.size(); i++) { auto t0 = std::chrono::steady_clock::now(); pf_strategy_t s = create(nullptr); setin(s, argv[4], vals[i].c_str()); pf_report_t r; memset(&r, 0, sizeof r); run(s, bars.data(), (int)bars.size(), &r); trades.push_back(r.total_trades); rfree(&r); sfree(s); printf("%s%lld", i ? "," : "", (long long)std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::steady_clock::now() - t0).count()); }
    printf("],\"totalNs\":%lld,\"trades\":[", (long long)std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::steady_clock::now() - T0).count()); for (size_t i = 0; i < trades.size(); i++) printf("%s%lld", i ? "," : "", trades[i]); printf("]}\n");
  }
  return 0;
}
