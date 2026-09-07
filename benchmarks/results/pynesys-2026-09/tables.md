## HEADLINE (best supported configuration per engine) - Set A: public benchmark suite (100, ETHUSDT 15m, 53,929 bars)

| engine | n | excellent | strong | moderate | weak | minimal | compile_fail | build_fail | run_error | timeout | not_run | tvTrades | engineTrades | matchedPct | countDelta_median | countDelta_p90 | entryP90_median | entryP90_p90 | exitP90_median | exitP90_p90 | pnlP90_median | pnlP90_p90 | netProfitRelErr_median | netProfitRelErr_p90 | maxEquityDev_median | wall_median_s | wall_p95_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PineForge - BEST SUPPORTED CONFIGURATION | 100 | 90 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 167301 | 166611 | 99.9301 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0795% | 0.0930% | 0.0975% | 2.0523% | 0.0689% | 0.192 | 0.283 |
| PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 100 | 82 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 167301 | 246026 | 99.8933 | 0.0000% | 0.0348% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0798% | 0.0968% | 0.5586% | 17.3902% | 0.3071% | 1.955 | 5.012 |
| PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 100 | 69 | 18 | 10 | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 167301 | 242657 | 99.1091 | 0.0000% | 0.1456% | 0.0000% | 0.0000% | 0.0000% | 0.4962% | 0.0820% | 348.3379% | 1.0946% | 52.6213% | 0.6040% | 2.721 | 7.858 |


### Which configuration won, set A

| engine | graded | PineForge (full feed, tape-window) | PineForge (range-start feed) | PineForge (full feed, raw) | PyneCore 6.9.1 (full feed) | PyneCore 6.9.1 (recompiled 6.0.66, full feed) | PyneCore 6.4.6 (full feed) |
|---|---|---|---|---|---|---|---|
| PineForge - BEST SUPPORTED CONFIGURATION | 100 | 97 | 2 | 1 |  |  |  |
| PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 100 |  |  |  | 99 | 1 |  |
| PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 99 |  |  |  |  |  | 99 |


### SECONDARY - one chart CSV, no setup - Set A: public benchmark suite (100, ETHUSDT 15m, 53,929 bars)

| engine | n | excellent | strong | moderate | weak | minimal | compile_fail | build_fail | run_error | timeout | not_run | tvTrades | engineTrades | matchedPct | countDelta_median | countDelta_p90 | entryP90_median | entryP90_p90 | exitP90_median | exitP90_p90 | pnlP90_median | pnlP90_p90 | netProfitRelErr_median | netProfitRelErr_p90 | maxEquityDev_median | wall_median_s | wall_p95_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PineForge (full feed, tape-window) | 100 | 89 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 167301 | 166022 | 99.9253 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0795% | 0.0930% | 0.0975% | 2.0523% | 0.0689% | 0.192 | 0.288 |
| PyneCore 6.9.1 (full feed) | 100 | 81 | 18 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 167301 | 245417 | 99.6354 | 0.0000% | 0.0351% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0798% | 0.1016% | 0.5687% | 18.6848% | 0.3223% | 1.955 | 5.012 |
| PyneCore 6.4.6 (full feed) | 100 | 69 | 18 | 10 | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 167301 | 242657 | 99.1091 | 0.0000% | 0.1456% | 0.0000% | 0.0000% | 0.0000% | 0.4962% | 0.0820% | 348.3379% | 1.0946% | 52.6213% | 0.6040% | 2.721 | 7.858 |


### Every rung measured - Set A: public benchmark suite (100, ETHUSDT 15m, 53,929 bars)

| engine | n | excellent | strong | moderate | weak | minimal | compile_fail | build_fail | run_error | timeout | not_run | tvTrades | engineTrades | matchedPct | countDelta_median | countDelta_p90 | entryP90_median | entryP90_p90 | exitP90_median | exitP90_p90 | pnlP90_median | pnlP90_p90 | netProfitRelErr_median | netProfitRelErr_p90 | maxEquityDev_median | wall_median_s | wall_p95_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 100 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 100 | 0 | 0 | 167301 | 0 | 0.0000 |  |  |  |  |  |  |  |  |  |  |  |  |  |
| PineForge (full feed, tape-window) | 100 | 89 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 167301 | 166022 | 99.9253 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0795% | 0.0930% | 0.0975% | 2.0523% | 0.0689% | 0.192 | 0.288 |
| PineForge (range-start feed) | 100 | 89 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 167301 | 165850 | 99.9252 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0797% | 0.0949% | 0.0975% | 3.9090% | 0.0775% | 0.186 | 0.281 |
| PineForge (full feed, raw) | 100 | 84 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 167301 | 245503 | 99.9247 | 0.0000% | 0.0339% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0798% | 0.0968% | 0.5586% | 18.6848% | 0.3071% | 0.158 | 0.225 |
| PyneCore 6.9.1 (full feed, --security supplied) | 100 | 81 | 18 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 167301 | 245417 | 99.6354 | 0.0000% | 0.0351% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0798% | 0.1016% | 0.5687% | 18.6848% | 0.3223% | 2.142 | 4.304 |
| PyneCore 6.9.1 (full feed) | 100 | 81 | 18 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 167301 | 245417 | 99.6354 | 0.0000% | 0.0351% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0798% | 0.1016% | 0.5687% | 18.6848% | 0.3223% | 1.955 | 5.012 |
| PyneCore 6.9.1 (--security + the probe's --from/--to window) | 100 | 81 | 18 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 167301 | 236847 | 99.6354 | 0.0000% | 0.0351% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0798% | 0.1016% | 0.2973% | 11.7541% | 0.1445% | 1.030 | 2.403 |
| PyneCore 6.4.6 (full feed) | 100 | 69 | 18 | 10 | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 167301 | 242657 | 99.1091 | 0.0000% | 0.1456% | 0.0000% | 0.0000% | 0.0000% | 0.4962% | 0.0820% | 348.3379% | 1.0946% | 52.6213% | 0.6040% | 2.721 | 7.858 |
| PyneCore 6.9.1 (recompiled 6.0.66, full feed) | 100 | 82 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 167301 | 246026 | 99.8933 | 0.0000% | 0.0348% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0798% | 0.0968% | 0.5586% | 17.3902% | 0.3071% | 1.937 | 4.943 |


## HEADLINE (best supported configuration per engine) - Set B: public corpus (312, ETHUSDT.P 15m, 222,295 bars)

| engine | n | excellent | strong | moderate | weak | minimal | compile_fail | build_fail | run_error | timeout | not_run | tvTrades | engineTrades | matchedPct | countDelta_median | countDelta_p90 | entryP90_median | entryP90_p90 | exitP90_median | exitP90_p90 | pnlP90_median | pnlP90_p90 | netProfitRelErr_median | netProfitRelErr_p90 | maxEquityDev_median | wall_median_s | wall_p95_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PineForge - BEST SUPPORTED CONFIGURATION | 311 | 310 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 431244 | 429642 | 99.9977 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0801% | 0.0000% | 4.750 | 28.920 |
| PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 311 | 272 | 24 | 0 | 11 | 1 | 0 | 0 | 3 | 0 | 0 | 431244 | 2236989 | 99.3391 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0041% | 3.8518% | 0.0024% | 5.550 | 14.413 |
| PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 311 | 233 | 25 | 8 | 11 | 1 | 0 | 0 | 33 | 0 | 0 | 431244 | 2069901 | 98.6802 | 0.0000% | 0.0182% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0630% | 12.9898% | 0.0482% | 6.789 | 14.508 |


### Which configuration won, set B

| engine | graded | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | PyneCore 6.9.1 (full feed) | PyneCore 6.9.1 (range-start feed) | PyneCore 6.9.1 (full feed, --security supplied) | PyneCore 6.9.1 (+ campaign 1m feed via --security) | PyneCore 6.4.6 (full feed) | PyneCore 6.4.6 (range-start feed) |
|---|---|---|---|---|---|---|---|---|
| PineForge - BEST SUPPORTED CONFIGURATION | 311 | 311 |  |  |  |  |  |  |
| PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 308 |  | 253 | 48 | 5 | 2 |  |  |
| PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 278 |  |  |  |  |  | 242 | 36 |


### SECONDARY - one chart CSV, no setup - Set B: public corpus (312, ETHUSDT.P 15m, 222,295 bars)

| engine | n | excellent | strong | moderate | weak | minimal | compile_fail | build_fail | run_error | timeout | not_run | tvTrades | engineTrades | matchedPct | countDelta_median | countDelta_p90 | entryP90_median | entryP90_p90 | exitP90_median | exitP90_p90 | pnlP90_median | pnlP90_p90 | netProfitRelErr_median | netProfitRelErr_p90 | maxEquityDev_median | wall_median_s | wall_p95_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PineForge (full feed, tape-window) | 311 | 311 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 431244 | 429642 | 99.9974 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0866% | 0.0000% | 0.314 | 0.420 |
| PyneCore 6.9.1 (full feed) | 311 | 230 | 51 | 0 | 7 | 3 | 0 | 0 | 10 | 10 | 0 | 431244 | 2384331 | 99.2172 | 0.0000% | 0.0256% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0378% | 9.7821% | 0.0326% | 5.932 | 12.100 |
| PyneCore 6.4.6 (full feed) | 311 | 205 | 50 | 8 | 11 | 4 | 0 | 0 | 33 | 0 | 0 | 431244 | 2272737 | 98.1593 | 0.0000% | 0.1570% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 14.0165% | 0.1294% | 19.3962% | 0.0971% | 8.115 | 15.578 |


### Every rung measured - Set B: public corpus (312, ETHUSDT.P 15m, 222,295 bars)

| engine | n | excellent | strong | moderate | weak | minimal | compile_fail | build_fail | run_error | timeout | not_run | tvTrades | engineTrades | matchedPct | countDelta_median | countDelta_p90 | entryP90_median | entryP90_p90 | exitP90_median | exitP90_p90 | pnlP90_median | pnlP90_p90 | netProfitRelErr_median | netProfitRelErr_p90 | maxEquityDev_median | wall_median_s | wall_p95_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 311 | 310 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 431244 | 429642 | 99.9977 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0801% | 0.0000% | 4.750 | 28.920 |
| PineForge (full feed, tape-window) | 311 | 311 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 431244 | 429642 | 99.9974 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0866% | 0.0000% | 0.314 | 0.420 |
| PineForge (range-start feed) | 311 | 282 | 24 | 0 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 431244 | 426248 | 99.3812 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 1.1989% | 0.0000% | 0.235 | 0.346 |
| PineForge (full feed, raw) | 311 | 267 | 34 | 2 | 2 | 6 | 0 | 0 | 0 | 0 | 0 | 431244 | 2286415 | 99.2230 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0378% | 11.1367% | 0.0316% | 0.289 | 0.529 |
| PineForge (+ campaign 1m auxiliary feed) | 311 | 305 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 431244 | 420748 | 99.9974 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0785% | 0.0000% | 2.373 | 3.143 |
| PineForge (+ campaign 1m auxiliary feed, range-start bound) | 311 | 276 | 24 | 0 | 1 | 4 | 0 | 0 | 6 | 0 | 0 | 431244 | 417375 | 99.3681 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.7000% | 0.0000% | 2.303 | 3.078 |
| PyneCore 6.9.1 (full feed, --security supplied) | 311 | 230 | 51 | 0 | 12 | 3 | 0 | 0 | 2 | 13 | 0 | 431244 | 2386258 | 99.0867 | 0.0000% | 0.0351% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 3.1637% | 0.0479% | 11.6519% | 0.0370% | 6.069 | 11.984 |
| PyneCore 6.9.1 (full feed) | 311 | 230 | 51 | 0 | 7 | 3 | 0 | 0 | 10 | 10 | 0 | 431244 | 2384331 | 99.2172 | 0.0000% | 0.0256% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0378% | 9.7821% | 0.0326% | 5.932 | 12.100 |
| PyneCore 6.9.1 (range-start feed) | 311 | 263 | 31 | 0 | 6 | 1 | 0 | 0 | 10 | 0 | 0 | 431244 | 433924 | 99.4528 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0010% | 2.4973% | 0.0006% | 1.391 | 4.014 |
| PyneCore 6.9.1 (+ campaign 1m feed via --security) | 311 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 309 | 431244 | 23835 | 100.0000 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 25.838 | 96.753 |
| PyneCore 6.9.1 (+ campaign 1m feed via --security, range-start feed) | 311 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 309 | 431244 | 3974 | 99.9745 | 0.0000% | 0.0322% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 10.476 | 31.050 |
| PyneCore 6.9.1 (--security + the probe's --from/--to window) | 311 | 231 | 51 | 0 | 12 | 3 | 0 | 0 | 0 | 14 | 0 | 431244 | 2398521 | 99.0950 | 0.0000% | 0.0348% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0395% | 13.3149% | 0.0328% | 3.118 | 8.182 |
| PyneCore 6.4.6 (full feed) | 311 | 205 | 50 | 8 | 11 | 4 | 0 | 0 | 33 | 0 | 0 | 431244 | 2272737 | 98.1593 | 0.0000% | 0.1570% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 14.0165% | 0.1294% | 19.3962% | 0.0971% | 8.115 | 15.578 |
| PyneCore 6.4.6 (range-start feed) | 311 | 226 | 32 | 8 | 11 | 1 | 0 | 0 | 33 | 0 | 0 | 431244 | 390385 | 98.6691 | 0.0000% | 0.0403% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0563% | 9.2622% | 0.0467% | 1.545 | 2.896 |


## HEADLINE (best supported configuration per engine) - Set C: closed campaign sample (200 script-lane probes, 15 lanes)

| engine | n | excellent | strong | moderate | weak | minimal | compile_fail | build_fail | run_error | timeout | not_run | tvTrades | engineTrades | matchedPct | countDelta_median | countDelta_p90 | entryP90_median | entryP90_p90 | exitP90_median | exitP90_p90 | pnlP90_median | pnlP90_p90 | netProfitRelErr_median | netProfitRelErr_p90 | maxEquityDev_median | wall_median_s | wall_p95_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PineForge - BEST SUPPORTED CONFIGURATION | 200 | 198 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 165223 | 153227 | 99.9856 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0626% | 0.0000% | 2.580 | 12.590 |
| PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 200 | 114 | 42 | 15 | 15 | 6 | 0 | 0 | 8 | 0 | 0 | 165223 | 586436 | 98.1482 | 0.0000% | 2.1739% | 0.0000% | 0.0000% | 0.0000% | 0.0327% | 0.0000% | 90.0000% | 4.4598% | 100.0000% | 2.7160% | 2.558 | 117.556 |
| PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 200 | 60 | 46 | 24 | 5 | 11 | 0 | 0 | 54 | 0 | 0 | 165223 | 565321 | 90.9022 | 0.0000% | 38.3607% | 0.0000% | 0.0003% | 0.0000% | 0.2517% | 0.0265% | 100.0000% | 17.1103% | 102.1059% | 6.5536% | 2.400 | 20.601 |


### Which configuration won, set C

| engine | graded | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | PyneCore 6.9.1 (full feed) | PyneCore 6.9.1 (range-start feed) | PyneCore 6.9.1 (--security + the probe's --from/--to window) | PyneCore 6.9.1 (full feed, --security supplied) | PyneCore 6.9.1 (+ campaign 1m feed via --security, range-start feed) | PyneCore 6.9.1 (+ campaign 1m feed via --security) | PyneCore 6.9.1 (+ the campaign's native TradingView daily feed under SYMBOL:D/1D) | PyneCore 6.4.6 (full feed) | PyneCore 6.4.6 (range-start feed) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PineForge - BEST SUPPORTED CONFIGURATION | 200 | 200 |  |  |  |  |  |  |  |  |  |
| PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 192 |  | 108 | 61 | 7 | 7 | 5 | 3 | 1 |  |  |
| PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 146 |  |  |  |  |  |  |  |  | 100 | 46 |


### SECONDARY - one chart CSV, no setup - Set C: closed campaign sample (200 script-lane probes, 15 lanes)

| engine | n | excellent | strong | moderate | weak | minimal | compile_fail | build_fail | run_error | timeout | not_run | tvTrades | engineTrades | matchedPct | countDelta_median | countDelta_p90 | entryP90_median | entryP90_p90 | exitP90_median | exitP90_p90 | pnlP90_median | pnlP90_p90 | netProfitRelErr_median | netProfitRelErr_p90 | maxEquityDev_median | wall_median_s | wall_p95_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PineForge (full feed, tape-window) | 200 | 140 | 29 | 8 | 3 | 7 | 0 | 0 | 13 | 0 | 0 | 165223 | 151629 | 98.9187 | 0.0000% | 0.5164% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.1178% | 0.0000% | 16.4154% | 0.0000% | 0.225 | 0.652 |
| PyneCore 6.9.1 (full feed) | 200 | 67 | 60 | 21 | 10 | 10 | 0 | 0 | 29 | 3 | 0 | 165223 | 707537 | 95.6891 | 0.0000% | 5.4496% | 0.0000% | 0.0000% | 0.0000% | 0.0555% | 0.0000% | 100.0000% | 16.9231% | 118.2531% | 8.3560% | 3.092 | 112.913 |
| PyneCore 6.4.6 (full feed) | 200 | 43 | 49 | 27 | 8 | 19 | 0 | 0 | 54 | 0 | 0 | 165223 | 707641 | 90.2838 | 0.0000% | 75.0000% | 0.0000% | 0.0003% | 0.0000% | 0.4548% | 0.0783% | 100.0000% | 17.8564% | 130.4566% | 10.4792% | 5.152 | 24.785 |


### Every rung measured - Set C: closed campaign sample (200 script-lane probes, 15 lanes)

| engine | n | excellent | strong | moderate | weak | minimal | compile_fail | build_fail | run_error | timeout | not_run | tvTrades | engineTrades | matchedPct | countDelta_median | countDelta_p90 | entryP90_median | entryP90_p90 | exitP90_median | exitP90_p90 | pnlP90_median | pnlP90_p90 | netProfitRelErr_median | netProfitRelErr_p90 | maxEquityDev_median | wall_median_s | wall_p95_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 200 | 198 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 165223 | 153227 | 99.9856 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0626% | 0.0000% | 2.580 | 12.590 |
| PineForge (full feed, tape-window) | 200 | 140 | 29 | 8 | 3 | 7 | 0 | 0 | 13 | 0 | 0 | 165223 | 151629 | 98.9187 | 0.0000% | 0.5164% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.1178% | 0.0000% | 16.4154% | 0.0000% | 0.225 | 0.652 |
| PineForge (range-start feed) | 200 | 156 | 19 | 5 | 3 | 4 | 0 | 0 | 13 | 0 | 0 | 165223 | 151390 | 98.9797 | 0.0000% | 0.1048% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 4.3140% | 0.0000% | 0.158 | 0.323 |
| PineForge (full feed, raw) | 200 | 93 | 59 | 20 | 3 | 12 | 0 | 0 | 13 | 0 | 0 | 165223 | 744008 | 97.1624 | 0.0000% | 3.2010% | 0.0000% | 0.0000% | 0.0000% | 0.0049% | 0.0000% | 73.6169% | 1.4433% | 94.5207% | 1.3638% | 0.204 | 0.746 |
| PineForge (+ campaign 1m auxiliary feed) | 200 | 105 | 24 | 6 | 3 | 3 | 0 | 0 | 59 | 0 | 0 | 165223 | 128423 | 99.2948 | 0.0000% | 0.2660% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.7080% | 0.0000% | 17.0719% | 0.0000% | 1.561 | 3.162 |
| PineForge (+ campaign 1m auxiliary feed, range-start bound) | 200 | 168 | 19 | 5 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 165223 | 151651 | 98.9670 | 0.0000% | 0.1048% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 3.3898% | 0.0000% | 1.178 | 2.406 |
| PyneCore 6.9.1 (full feed, --security supplied) | 200 | 68 | 62 | 22 | 14 | 13 | 0 | 0 | 19 | 2 | 0 | 165223 | 711272 | 95.5649 | 0.0000% | 10.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0747% | 0.0000% | 100.0000% | 16.9231% | 124.3221% | 8.9725% | 2.864 | 110.386 |
| PyneCore 6.9.1 (full feed) | 200 | 67 | 60 | 21 | 10 | 10 | 0 | 0 | 29 | 3 | 0 | 165223 | 707537 | 95.6891 | 0.0000% | 5.4496% | 0.0000% | 0.0000% | 0.0000% | 0.0555% | 0.0000% | 100.0000% | 16.9231% | 118.2531% | 8.3560% | 3.092 | 112.913 |
| PyneCore 6.9.1 (range-start feed) | 200 | 107 | 38 | 13 | 10 | 3 | 0 | 0 | 29 | 0 | 0 | 165223 | 146191 | 98.2573 | 0.0000% | 0.8386% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 75.0000% | 3.2258% | 100.0000% | 2.1563% | 0.974 | 30.658 |
| PyneCore 6.9.1 (+ campaign 1m feed via --security) | 200 | 2 | 0 | 2 | 2 | 2 | 0 | 0 | 0 | 5 | 187 | 165223 | 399 | 89.4118 | 5.5556% | 50.0000% | 0.0000% | 0.0000% | 0.0000% | 0.1335% | 6.7923% | 87.7875% | 6.8138% | 50.8928% | 18.4513% | 118.626 | 215.247 |
| PyneCore 6.9.1 (+ campaign 1m feed via --security, range-start feed) | 200 | 4 | 2 | 0 | 1 | 1 | 0 | 0 | 0 | 5 | 187 | 165223 | 102 | 96.7742 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0487% | 0.0000% | 2.5307% | 6.4478% | 50.3241% | 2.7798% | 116.439 | 215.531 |
| PyneCore 6.9.1 (--security + the probe's --from/--to window) | 200 | 104 | 48 | 16 | 16 | 6 | 0 | 0 | 3 | 7 | 0 | 165223 | 145806 | 98.2584 | 0.0000% | 2.1739% | 0.0000% | 0.0000% | 0.0000% | 0.3110% | 0.0000% | 86.6106% | 4.3658% | 100.0000% | 2.7528% | 0.847 | 127.368 |
| PyneCore 6.9.1 (+ the campaign's native TradingView daily feed under SYMBOL:D/1D) | 200 | 42 | 9 | 2 | 7 | 2 | 0 | 0 | 0 | 0 | 138 | 165223 | 30415 | 97.1057 | 0.0000% | 4.7619% | 0.0000% | 0.0000% | 0.0000% | 0.1378% | 0.0000% | 60.4778% | 8.6037% | 49.1377% | 4.5957% | 0.578 | 142.518 |
| PyneCore 6.4.6 (full feed) | 200 | 43 | 49 | 27 | 8 | 19 | 0 | 0 | 54 | 0 | 0 | 165223 | 707641 | 90.2838 | 0.0000% | 75.0000% | 0.0000% | 0.0003% | 0.0000% | 0.4548% | 0.0783% | 100.0000% | 17.8564% | 130.4566% | 10.4792% | 5.152 | 24.785 |
| PyneCore 6.4.6 (range-start feed) | 200 | 60 | 45 | 25 | 5 | 11 | 0 | 0 | 54 | 0 | 0 | 165223 | 146034 | 90.8744 | 0.0000% | 40.1070% | 0.0000% | 0.0003% | 0.0000% | 0.2517% | 0.0139% | 100.0000% | 11.5611% | 114.7061% | 4.9036% | 1.033 | 4.417 |


### Closed set by symbol@timeframe — PineForge - BEST SUPPORTED CONFIGURATION

| lane | sampled | excellent | strong | moderate | weak | minimal | fail | not_run |
|---|---|---|---|---|---|---|---|---|
| BINANCE:ETHUSDT.P@15 | 20 | 20 | 0 | 0 | 0 | 0 | 0 | 0 |
| BINANCE:BTCUSDT@15 | 18 | 18 | 0 | 0 | 0 | 0 | 0 | 0 |
| BINANCE:BTCUSDT@1D | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 |
| CME_MINI:ES1!@15 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 |
| CME_MINI:ES1!@1D | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 |
| CME_MINI:NQ1!@15 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 |
| CME_MINI:NQ1!@1D | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 |
| NASDAQ:AAPL@15 | 18 | 18 | 0 | 0 | 0 | 0 | 0 | 0 |
| NSE:NIFTY@15 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 |
| NSE:NIFTY@1D | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 |
| NYSE:F@15 | 17 | 17 | 0 | 0 | 0 | 0 | 0 | 0 |
| NYSE:F@1D | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 |
| OANDA:EURUSD@15 | 19 | 17 | 2 | 0 | 0 | 0 | 0 | 0 |
| OANDA:XAUUSD@15 | 19 | 19 | 0 | 0 | 0 | 0 | 0 | 0 |
| OANDA:XAUUSD@1D | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 |


### Closed set by symbol@timeframe — PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION

| lane | sampled | excellent | strong | moderate | weak | minimal | fail | not_run |
|---|---|---|---|---|---|---|---|---|
| BINANCE:ETHUSDT.P@15 | 20 | 11 | 7 | 0 | 2 | 0 | 0 | 0 |
| BINANCE:BTCUSDT@15 | 18 | 12 | 2 | 0 | 2 | 0 | 2 | 0 |
| BINANCE:BTCUSDT@1D | 13 | 7 | 2 | 3 | 1 | 0 | 0 | 0 |
| CME_MINI:ES1!@15 | 9 | 8 | 1 | 0 | 0 | 0 | 0 | 0 |
| CME_MINI:ES1!@1D | 8 | 1 | 3 | 1 | 0 | 3 | 0 | 0 |
| CME_MINI:NQ1!@15 | 9 | 8 | 0 | 0 | 0 | 1 | 0 | 0 |
| CME_MINI:NQ1!@1D | 8 | 3 | 2 | 3 | 0 | 0 | 0 | 0 |
| NASDAQ:AAPL@15 | 18 | 9 | 4 | 1 | 4 | 0 | 0 | 0 |
| NSE:NIFTY@15 | 9 | 8 | 0 | 1 | 0 | 0 | 0 | 0 |
| NSE:NIFTY@1D | 8 | 3 | 2 | 2 | 1 | 0 | 0 | 0 |
| NYSE:F@15 | 17 | 13 | 1 | 0 | 2 | 1 | 0 | 0 |
| NYSE:F@1D | 13 | 5 | 3 | 3 | 2 | 0 | 0 | 0 |
| OANDA:EURUSD@15 | 19 | 8 | 6 | 1 | 0 | 0 | 4 | 0 |
| OANDA:XAUUSD@15 | 19 | 10 | 6 | 0 | 1 | 1 | 1 | 0 |
| OANDA:XAUUSD@1D | 12 | 8 | 3 | 0 | 0 | 0 | 1 | 0 |


### Closed set by symbol@timeframe — PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION

| lane | sampled | excellent | strong | moderate | weak | minimal | fail | not_run |
|---|---|---|---|---|---|---|---|---|
| BINANCE:ETHUSDT.P@15 | 20 | 4 | 6 | 0 | 3 | 1 | 6 | 0 |
| BINANCE:BTCUSDT@15 | 18 | 2 | 7 | 1 | 1 | 1 | 6 | 0 |
| BINANCE:BTCUSDT@1D | 13 | 3 | 1 | 6 | 0 | 0 | 3 | 0 |
| CME_MINI:ES1!@15 | 9 | 7 | 0 | 0 | 0 | 1 | 1 | 0 |
| CME_MINI:ES1!@1D | 8 | 0 | 3 | 0 | 0 | 2 | 3 | 0 |
| CME_MINI:NQ1!@15 | 9 | 5 | 1 | 0 | 0 | 0 | 3 | 0 |
| CME_MINI:NQ1!@1D | 8 | 3 | 1 | 3 | 0 | 0 | 1 | 0 |
| NASDAQ:AAPL@15 | 18 | 6 | 2 | 2 | 0 | 0 | 8 | 0 |
| NSE:NIFTY@15 | 9 | 5 | 1 | 1 | 0 | 0 | 2 | 0 |
| NSE:NIFTY@1D | 8 | 2 | 2 | 2 | 0 | 0 | 2 | 0 |
| NYSE:F@15 | 17 | 9 | 3 | 1 | 0 | 0 | 4 | 0 |
| NYSE:F@1D | 13 | 4 | 2 | 3 | 0 | 0 | 4 | 0 |
| OANDA:EURUSD@15 | 19 | 4 | 3 | 4 | 1 | 3 | 4 | 0 |
| OANDA:XAUUSD@15 | 19 | 0 | 12 | 0 | 0 | 3 | 4 | 0 |
| OANDA:XAUUSD@1D | 12 | 6 | 2 | 1 | 0 | 0 | 3 | 0 |


### Closed set by symbol@timeframe — PineForge (full feed, tape-window)

| lane | sampled | excellent | strong | moderate | weak | minimal | fail | not_run |
|---|---|---|---|---|---|---|---|---|
| BINANCE:ETHUSDT.P@15 | 20 | 17 | 2 | 1 | 0 | 0 | 0 | 0 |
| BINANCE:BTCUSDT@15 | 18 | 13 | 3 | 0 | 0 | 0 | 2 | 0 |
| BINANCE:BTCUSDT@1D | 13 | 5 | 2 | 4 | 0 | 0 | 2 | 0 |
| CME_MINI:ES1!@15 | 9 | 7 | 1 | 0 | 0 | 1 | 0 | 0 |
| CME_MINI:ES1!@1D | 8 | 4 | 1 | 0 | 0 | 2 | 1 | 0 |
| CME_MINI:NQ1!@15 | 9 | 7 | 1 | 0 | 1 | 0 | 0 | 0 |
| CME_MINI:NQ1!@1D | 8 | 4 | 0 | 2 | 0 | 1 | 1 | 0 |
| NASDAQ:AAPL@15 | 18 | 14 | 2 | 0 | 1 | 1 | 0 | 0 |
| NSE:NIFTY@15 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 |
| NSE:NIFTY@1D | 8 | 7 | 0 | 0 | 0 | 0 | 1 | 0 |
| NYSE:F@15 | 17 | 14 | 3 | 0 | 0 | 0 | 0 | 0 |
| NYSE:F@1D | 13 | 10 | 1 | 0 | 0 | 0 | 2 | 0 |
| OANDA:EURUSD@15 | 19 | 10 | 8 | 0 | 0 | 0 | 1 | 0 |
| OANDA:XAUUSD@15 | 19 | 12 | 3 | 0 | 1 | 2 | 1 | 0 |
| OANDA:XAUUSD@1D | 12 | 7 | 2 | 1 | 0 | 0 | 2 | 0 |


### Closed set by symbol@timeframe — PineForge (range-start feed)

| lane | sampled | excellent | strong | moderate | weak | minimal | fail | not_run |
|---|---|---|---|---|---|---|---|---|
| BINANCE:ETHUSDT.P@15 | 20 | 15 | 4 | 1 | 0 | 0 | 0 | 0 |
| BINANCE:BTCUSDT@15 | 18 | 15 | 1 | 0 | 0 | 0 | 2 | 0 |
| BINANCE:BTCUSDT@1D | 13 | 9 | 0 | 2 | 0 | 0 | 2 | 0 |
| CME_MINI:ES1!@15 | 9 | 8 | 0 | 0 | 0 | 1 | 0 | 0 |
| CME_MINI:ES1!@1D | 8 | 5 | 0 | 0 | 0 | 2 | 1 | 0 |
| CME_MINI:NQ1!@15 | 9 | 8 | 0 | 0 | 1 | 0 | 0 | 0 |
| CME_MINI:NQ1!@1D | 8 | 6 | 0 | 1 | 0 | 0 | 1 | 0 |
| NASDAQ:AAPL@15 | 18 | 13 | 3 | 1 | 1 | 0 | 0 | 0 |
| NSE:NIFTY@15 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 |
| NSE:NIFTY@1D | 8 | 7 | 0 | 0 | 0 | 0 | 1 | 0 |
| NYSE:F@15 | 17 | 17 | 0 | 0 | 0 | 0 | 0 | 0 |
| NYSE:F@1D | 13 | 11 | 0 | 0 | 0 | 0 | 2 | 0 |
| OANDA:EURUSD@15 | 19 | 10 | 8 | 0 | 0 | 0 | 1 | 0 |
| OANDA:XAUUSD@15 | 19 | 14 | 3 | 0 | 0 | 1 | 1 | 0 |
| OANDA:XAUUSD@1D | 12 | 9 | 0 | 0 | 1 | 0 | 2 | 0 |


### Closed set by symbol@timeframe — PyneCore 6.9.1 (full feed, --security supplied)

| lane | sampled | excellent | strong | moderate | weak | minimal | fail | not_run |
|---|---|---|---|---|---|---|---|---|
| BINANCE:ETHUSDT.P@15 | 20 | 6 | 9 | 2 | 1 | 0 | 2 | 0 |
| BINANCE:BTCUSDT@15 | 18 | 6 | 7 | 0 | 1 | 2 | 2 | 0 |
| BINANCE:BTCUSDT@1D | 13 | 0 | 2 | 8 | 1 | 0 | 2 | 0 |
| CME_MINI:ES1!@15 | 9 | 6 | 2 | 1 | 0 | 0 | 0 | 0 |
| CME_MINI:ES1!@1D | 8 | 0 | 3 | 2 | 0 | 2 | 1 | 0 |
| CME_MINI:NQ1!@15 | 9 | 7 | 1 | 0 | 0 | 1 | 0 | 0 |
| CME_MINI:NQ1!@1D | 8 | 2 | 0 | 0 | 0 | 4 | 2 | 0 |
| NASDAQ:AAPL@15 | 18 | 6 | 7 | 0 | 4 | 0 | 1 | 0 |
| NSE:NIFTY@15 | 9 | 7 | 0 | 2 | 0 | 0 | 0 | 0 |
| NSE:NIFTY@1D | 8 | 1 | 3 | 1 | 1 | 1 | 1 | 0 |
| NYSE:F@15 | 17 | 8 | 5 | 1 | 2 | 1 | 0 | 0 |
| NYSE:F@1D | 13 | 3 | 3 | 2 | 2 | 1 | 2 | 0 |
| OANDA:EURUSD@15 | 19 | 6 | 8 | 1 | 0 | 0 | 4 | 0 |
| OANDA:XAUUSD@15 | 19 | 4 | 10 | 1 | 1 | 1 | 2 | 0 |
| OANDA:XAUUSD@1D | 12 | 6 | 2 | 1 | 1 | 0 | 2 | 0 |


### Closed set by symbol@timeframe — PyneCore 6.9.1 (full feed)

| lane | sampled | excellent | strong | moderate | weak | minimal | fail | not_run |
|---|---|---|---|---|---|---|---|---|
| BINANCE:ETHUSDT.P@15 | 20 | 6 | 8 | 2 | 0 | 0 | 4 | 0 |
| BINANCE:BTCUSDT@15 | 18 | 6 | 7 | 0 | 0 | 2 | 3 | 0 |
| BINANCE:BTCUSDT@1D | 13 | 0 | 2 | 8 | 1 | 0 | 2 | 0 |
| CME_MINI:ES1!@15 | 9 | 6 | 2 | 1 | 0 | 0 | 0 | 0 |
| CME_MINI:ES1!@1D | 8 | 0 | 3 | 1 | 0 | 2 | 2 | 0 |
| CME_MINI:NQ1!@15 | 9 | 6 | 1 | 0 | 0 | 0 | 2 | 0 |
| CME_MINI:NQ1!@1D | 8 | 2 | 0 | 0 | 0 | 4 | 2 | 0 |
| NASDAQ:AAPL@15 | 18 | 6 | 7 | 0 | 3 | 0 | 2 | 0 |
| NSE:NIFTY@15 | 9 | 7 | 0 | 2 | 0 | 0 | 0 | 0 |
| NSE:NIFTY@1D | 8 | 1 | 3 | 1 | 0 | 1 | 2 | 0 |
| NYSE:F@15 | 17 | 8 | 5 | 1 | 2 | 0 | 1 | 0 |
| NYSE:F@1D | 13 | 3 | 2 | 2 | 2 | 0 | 4 | 0 |
| OANDA:EURUSD@15 | 19 | 6 | 8 | 1 | 0 | 0 | 4 | 0 |
| OANDA:XAUUSD@15 | 19 | 4 | 10 | 1 | 1 | 1 | 2 | 0 |
| OANDA:XAUUSD@1D | 12 | 6 | 2 | 1 | 1 | 0 | 2 | 0 |


### Closed set by symbol@timeframe — PyneCore 6.9.1 (range-start feed)

| lane | sampled | excellent | strong | moderate | weak | minimal | fail | not_run |
|---|---|---|---|---|---|---|---|---|
| BINANCE:ETHUSDT.P@15 | 20 | 10 | 7 | 0 | 1 | 0 | 2 | 0 |
| BINANCE:BTCUSDT@15 | 18 | 12 | 2 | 0 | 1 | 0 | 3 | 0 |
| BINANCE:BTCUSDT@1D | 13 | 5 | 2 | 3 | 1 | 0 | 2 | 0 |
| CME_MINI:ES1!@15 | 9 | 8 | 0 | 0 | 1 | 0 | 0 | 0 |
| CME_MINI:ES1!@1D | 8 | 1 | 3 | 0 | 0 | 2 | 2 | 0 |
| CME_MINI:NQ1!@15 | 9 | 8 | 0 | 0 | 0 | 0 | 1 | 0 |
| CME_MINI:NQ1!@1D | 8 | 2 | 1 | 3 | 0 | 0 | 2 | 0 |
| NASDAQ:AAPL@15 | 18 | 9 | 4 | 0 | 3 | 0 | 2 | 0 |
| NSE:NIFTY@15 | 9 | 8 | 0 | 1 | 0 | 0 | 0 | 0 |
| NSE:NIFTY@1D | 8 | 2 | 2 | 2 | 0 | 0 | 2 | 0 |
| NYSE:F@15 | 17 | 13 | 1 | 0 | 2 | 0 | 1 | 0 |
| NYSE:F@1D | 13 | 4 | 2 | 3 | 0 | 0 | 4 | 0 |
| OANDA:EURUSD@15 | 19 | 8 | 6 | 1 | 0 | 0 | 4 | 0 |
| OANDA:XAUUSD@15 | 19 | 9 | 6 | 0 | 1 | 1 | 2 | 0 |
| OANDA:XAUUSD@1D | 12 | 8 | 2 | 0 | 0 | 0 | 2 | 0 |


### Closed set by symbol@timeframe — PyneCore 6.9.1 (--security + the probe's --from/--to window)

| lane | sampled | excellent | strong | moderate | weak | minimal | fail | not_run |
|---|---|---|---|---|---|---|---|---|
| BINANCE:ETHUSDT.P@15 | 20 | 9 | 8 | 0 | 1 | 0 | 2 | 0 |
| BINANCE:BTCUSDT@15 | 18 | 11 | 3 | 0 | 2 | 0 | 2 | 0 |
| BINANCE:BTCUSDT@1D | 13 | 7 | 0 | 5 | 1 | 0 | 0 | 0 |
| CME_MINI:ES1!@15 | 9 | 7 | 1 | 0 | 1 | 0 | 0 | 0 |
| CME_MINI:ES1!@1D | 8 | 1 | 3 | 1 | 0 | 3 | 0 | 0 |
| CME_MINI:NQ1!@15 | 9 | 8 | 0 | 0 | 0 | 1 | 0 | 0 |
| CME_MINI:NQ1!@1D | 8 | 3 | 2 | 3 | 0 | 0 | 0 | 0 |
| NASDAQ:AAPL@15 | 18 | 9 | 4 | 0 | 5 | 0 | 0 | 0 |
| NSE:NIFTY@15 | 9 | 8 | 0 | 1 | 0 | 0 | 0 | 0 |
| NSE:NIFTY@1D | 8 | 3 | 2 | 2 | 1 | 0 | 0 | 0 |
| NYSE:F@15 | 17 | 10 | 4 | 0 | 2 | 1 | 0 | 0 |
| NYSE:F@1D | 13 | 5 | 3 | 3 | 2 | 0 | 0 | 0 |
| OANDA:EURUSD@15 | 19 | 6 | 8 | 1 | 0 | 0 | 4 | 0 |
| OANDA:XAUUSD@15 | 19 | 10 | 6 | 0 | 1 | 1 | 1 | 0 |
| OANDA:XAUUSD@1D | 12 | 7 | 4 | 0 | 0 | 0 | 1 | 0 |


### Closed set by symbol@timeframe — PyneCore 6.9.1 (+ the campaign's native TradingView daily feed under SYMBOL:D/1D)

| lane | sampled | excellent | strong | moderate | weak | minimal | fail | not_run |
|---|---|---|---|---|---|---|---|---|
| BINANCE:ETHUSDT.P@15 | 20 | 0 | 0 | 0 | 0 | 0 | 0 | 20 |
| BINANCE:BTCUSDT@15 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 18 |
| BINANCE:BTCUSDT@1D | 13 | 0 | 0 | 0 | 0 | 0 | 0 | 13 |
| CME_MINI:ES1!@15 | 9 | 7 | 1 | 0 | 1 | 0 | 0 | 0 |
| CME_MINI:ES1!@1D | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 8 |
| CME_MINI:NQ1!@15 | 9 | 8 | 0 | 0 | 0 | 1 | 0 | 0 |
| CME_MINI:NQ1!@1D | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 8 |
| NASDAQ:AAPL@15 | 18 | 9 | 4 | 1 | 4 | 0 | 0 | 0 |
| NSE:NIFTY@15 | 9 | 8 | 0 | 1 | 0 | 0 | 0 | 0 |
| NSE:NIFTY@1D | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 8 |
| NYSE:F@15 | 17 | 10 | 4 | 0 | 2 | 1 | 0 | 0 |
| NYSE:F@1D | 13 | 0 | 0 | 0 | 0 | 0 | 0 | 13 |
| OANDA:EURUSD@15 | 19 | 0 | 0 | 0 | 0 | 0 | 0 | 19 |
| OANDA:XAUUSD@15 | 19 | 0 | 0 | 0 | 0 | 0 | 0 | 19 |
| OANDA:XAUUSD@1D | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 12 |


### Closed set by symbol@timeframe — PyneCore 6.4.6 (full feed)

| lane | sampled | excellent | strong | moderate | weak | minimal | fail | not_run |
|---|---|---|---|---|---|---|---|---|
| BINANCE:ETHUSDT.P@15 | 20 | 2 | 7 | 1 | 3 | 1 | 6 | 0 |
| BINANCE:BTCUSDT@15 | 18 | 2 | 7 | 1 | 1 | 1 | 6 | 0 |
| BINANCE:BTCUSDT@1D | 13 | 0 | 1 | 9 | 0 | 0 | 3 | 0 |
| CME_MINI:ES1!@15 | 9 | 6 | 1 | 0 | 0 | 1 | 1 | 0 |
| CME_MINI:ES1!@1D | 8 | 0 | 1 | 2 | 0 | 2 | 3 | 0 |
| CME_MINI:NQ1!@15 | 9 | 4 | 2 | 0 | 0 | 0 | 3 | 0 |
| CME_MINI:NQ1!@1D | 8 | 3 | 0 | 0 | 0 | 4 | 1 | 0 |
| NASDAQ:AAPL@15 | 18 | 4 | 4 | 2 | 0 | 0 | 8 | 0 |
| NSE:NIFTY@15 | 9 | 5 | 0 | 2 | 0 | 0 | 2 | 0 |
| NSE:NIFTY@1D | 8 | 1 | 3 | 1 | 0 | 1 | 2 | 0 |
| NYSE:F@15 | 17 | 6 | 6 | 1 | 0 | 0 | 4 | 0 |
| NYSE:F@1D | 13 | 3 | 2 | 1 | 2 | 1 | 4 | 0 |
| OANDA:EURUSD@15 | 19 | 3 | 4 | 4 | 0 | 4 | 4 | 0 |
| OANDA:XAUUSD@15 | 19 | 0 | 9 | 1 | 1 | 4 | 4 | 0 |
| OANDA:XAUUSD@1D | 12 | 4 | 2 | 2 | 1 | 0 | 3 | 0 |


## The finer-timeframe rung, both engines on the campaign's own 1-minute feeds

The 511 probes whose chart-feed-only run needed a `request.security`
timeframe finer than the staged feed. BOTH engines refuse these inputs on the chart
feed alone, and BOTH are given the campaign's own 1-minute bytes here.

| variant | inputs | n | excellent | strong | moderate | weak | minimal | run_error | timeout | no_finer_feed | not_run |
|---|---|---|---|---|---|---|---|---|---|---|---|
| pf | PineForge, chart feed only | 511 | 451 | 29 | 8 | 3 | 7 | 13 | 0 | 0 | 0 |
| pf_finer | PineForge + campaign 1m auxiliary security feed | 511 | 410 | 24 | 6 | 3 | 3 | 65 | 0 | 0 | 0 |
| pf_finer_rs | PineForge + campaign 1m auxiliary feed, range-start bound | 511 | 444 | 43 | 5 | 5 | 8 | 6 | 0 | 0 | 0 |
| pc691 | PyneCore 6.9.1, chart feed only | 511 | 297 | 111 | 21 | 17 | 13 | 39 | 13 | 0 | 0 |
| pc691_sec | PyneCore 6.9.1, --security from the chart feed | 511 | 298 | 113 | 22 | 26 | 16 | 21 | 15 | 0 | 0 |
| pc691_finer | PyneCore 6.9.1 + campaign 1m feed via --security | 511 | 4 | 0 | 2 | 2 | 2 | 0 | 5 | 0 | 496 |
| pc691_finer_rs | PyneCore 6.9.1 + campaign 1m feed via --security, range-start feed | 511 | 5 | 3 | 0 | 1 | 1 | 0 | 5 | 0 | 496 |
| pc691_best | PyneCore 6.9.1, --security + the probe's --from/--to window | 511 | 335 | 99 | 16 | 28 | 9 | 3 | 21 | 0 | 0 |
| pf @ B/eth-corpus | PineForge, chart feed only | 311 | 311 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pf_finer @ B/eth-corpus | PineForge + campaign 1m auxiliary security feed | 311 | 305 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 |
| pf_finer_rs @ B/eth-corpus | PineForge + campaign 1m auxiliary feed, range-start bound | 311 | 276 | 24 | 0 | 1 | 4 | 6 | 0 | 0 | 0 |
| pc691 @ B/eth-corpus | PyneCore 6.9.1, chart feed only | 311 | 230 | 51 | 0 | 7 | 3 | 10 | 10 | 0 | 0 |
| pc691_sec @ B/eth-corpus | PyneCore 6.9.1, --security from the chart feed | 311 | 230 | 51 | 0 | 12 | 3 | 2 | 13 | 0 | 0 |
| pc691_finer @ B/eth-corpus | PyneCore 6.9.1 + campaign 1m feed via --security | 311 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 309 |
| pc691_finer_rs @ B/eth-corpus | PyneCore 6.9.1 + campaign 1m feed via --security, range-start feed | 311 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 309 |
| pc691_best @ B/eth-corpus | PyneCore 6.9.1, --security + the probe's --from/--to window | 311 | 231 | 51 | 0 | 12 | 3 | 0 | 14 | 0 | 0 |
| pf @ C/aapl | PineForge, chart feed only | 18 | 14 | 2 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| pf_finer @ C/aapl | PineForge + campaign 1m auxiliary security feed | 18 | 14 | 2 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| pf_finer_rs @ C/aapl | PineForge + campaign 1m auxiliary feed, range-start bound | 18 | 12 | 3 | 1 | 2 | 0 | 0 | 0 | 0 | 0 |
| pc691 @ C/aapl | PyneCore 6.9.1, chart feed only | 18 | 6 | 7 | 0 | 3 | 0 | 2 | 0 | 0 | 0 |
| pc691_sec @ C/aapl | PyneCore 6.9.1, --security from the chart feed | 18 | 6 | 7 | 0 | 4 | 0 | 1 | 0 | 0 | 0 |
| pc691_finer @ C/aapl | PyneCore 6.9.1 + campaign 1m feed via --security | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 18 |
| pc691_finer_rs @ C/aapl | PyneCore 6.9.1 + campaign 1m feed via --security, range-start feed | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 18 |
| pc691_best @ C/aapl | PyneCore 6.9.1, --security + the probe's --from/--to window | 18 | 9 | 4 | 0 | 5 | 0 | 0 | 0 | 0 | 0 |
| pf @ C/btcusdt | PineForge, chart feed only | 18 | 13 | 3 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| pf_finer @ C/btcusdt | PineForge + campaign 1m auxiliary security feed | 18 | 15 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pf_finer_rs @ C/btcusdt | PineForge + campaign 1m auxiliary feed, range-start bound | 18 | 17 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pc691 @ C/btcusdt | PyneCore 6.9.1, chart feed only | 18 | 6 | 7 | 0 | 0 | 2 | 3 | 0 | 0 | 0 |
| pc691_sec @ C/btcusdt | PyneCore 6.9.1, --security from the chart feed | 18 | 6 | 7 | 0 | 1 | 2 | 2 | 0 | 0 | 0 |
| pc691_finer @ C/btcusdt | PyneCore 6.9.1 + campaign 1m feed via --security | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 16 |
| pc691_finer_rs @ C/btcusdt | PyneCore 6.9.1 + campaign 1m feed via --security, range-start feed | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 16 |
| pc691_best @ C/btcusdt | PyneCore 6.9.1, --security + the probe's --from/--to window | 18 | 11 | 3 | 0 | 2 | 0 | 0 | 2 | 0 | 0 |
| pf @ C/btcusdt-1d | PineForge, chart feed only | 13 | 5 | 2 | 4 | 0 | 0 | 2 | 0 | 0 | 0 |
| pf_finer @ C/btcusdt-1d | PineForge + campaign 1m auxiliary security feed | 13 | 7 | 2 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| pf_finer_rs @ C/btcusdt-1d | PineForge + campaign 1m auxiliary feed, range-start bound | 13 | 11 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| pc691 @ C/btcusdt-1d | PyneCore 6.9.1, chart feed only | 13 | 0 | 2 | 8 | 1 | 0 | 2 | 0 | 0 | 0 |
| pc691_sec @ C/btcusdt-1d | PyneCore 6.9.1, --security from the chart feed | 13 | 0 | 2 | 8 | 1 | 0 | 2 | 0 | 0 | 0 |
| pc691_finer @ C/btcusdt-1d | PyneCore 6.9.1 + campaign 1m feed via --security | 13 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 11 |
| pc691_finer_rs @ C/btcusdt-1d | PyneCore 6.9.1 + campaign 1m feed via --security, range-start feed | 13 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 11 |
| pc691_best @ C/btcusdt-1d | PyneCore 6.9.1, --security + the probe's --from/--to window | 13 | 7 | 0 | 5 | 1 | 0 | 0 | 0 | 0 | 0 |
| pf @ C/es1 | PineForge, chart feed only | 9 | 7 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| pf_finer @ C/es1 | PineForge + campaign 1m auxiliary security feed | 9 | 0 | 0 | 0 | 0 | 0 | 9 | 0 | 0 | 0 |
| pf_finer_rs @ C/es1 | PineForge + campaign 1m auxiliary feed, range-start bound | 9 | 8 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| pc691 @ C/es1 | PyneCore 6.9.1, chart feed only | 9 | 6 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| pc691_sec @ C/es1 | PyneCore 6.9.1, --security from the chart feed | 9 | 6 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| pc691_finer @ C/es1 | PyneCore 6.9.1 + campaign 1m feed via --security | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 |
| pc691_finer_rs @ C/es1 | PyneCore 6.9.1 + campaign 1m feed via --security, range-start feed | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 |
| pc691_best @ C/es1 | PyneCore 6.9.1, --security + the probe's --from/--to window | 9 | 7 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| pf @ C/es1-1d | PineForge, chart feed only | 8 | 4 | 1 | 0 | 0 | 2 | 1 | 0 | 0 | 0 |
| pf_finer @ C/es1-1d | PineForge + campaign 1m auxiliary security feed | 8 | 0 | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 |
| pf_finer_rs @ C/es1-1d | PineForge + campaign 1m auxiliary feed, range-start bound | 8 | 6 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| pc691 @ C/es1-1d | PyneCore 6.9.1, chart feed only | 8 | 0 | 3 | 1 | 0 | 2 | 2 | 0 | 0 | 0 |
| pc691_sec @ C/es1-1d | PyneCore 6.9.1, --security from the chart feed | 8 | 0 | 3 | 2 | 0 | 2 | 1 | 0 | 0 | 0 |
| pc691_finer @ C/es1-1d | PyneCore 6.9.1 + campaign 1m feed via --security | 8 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 7 |
| pc691_finer_rs @ C/es1-1d | PyneCore 6.9.1 + campaign 1m feed via --security, range-start feed | 8 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 7 |
| pc691_best @ C/es1-1d | PyneCore 6.9.1, --security + the probe's --from/--to window | 8 | 1 | 3 | 1 | 0 | 3 | 0 | 0 | 0 | 0 |
| pf @ C/eth | PineForge, chart feed only | 20 | 17 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| pf_finer @ C/eth | PineForge + campaign 1m auxiliary security feed | 20 | 17 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| pf_finer_rs @ C/eth | PineForge + campaign 1m auxiliary feed, range-start bound | 20 | 15 | 4 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| pc691 @ C/eth | PyneCore 6.9.1, chart feed only | 20 | 6 | 8 | 2 | 0 | 0 | 2 | 2 | 0 | 0 |
| pc691_sec @ C/eth | PyneCore 6.9.1, --security from the chart feed | 20 | 6 | 9 | 2 | 1 | 0 | 0 | 2 | 0 | 0 |
| pc691_finer @ C/eth | PyneCore 6.9.1 + campaign 1m feed via --security | 20 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 20 |
| pc691_finer_rs @ C/eth | PyneCore 6.9.1 + campaign 1m feed via --security, range-start feed | 20 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 20 |
| pc691_best @ C/eth | PyneCore 6.9.1, --security + the probe's --from/--to window | 20 | 9 | 8 | 0 | 1 | 0 | 0 | 2 | 0 | 0 |
| pf @ C/eurusd | PineForge, chart feed only | 19 | 10 | 8 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| pf_finer @ C/eurusd | PineForge + campaign 1m auxiliary security feed | 19 | 11 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pf_finer_rs @ C/eurusd | PineForge + campaign 1m auxiliary feed, range-start bound | 19 | 11 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pc691 @ C/eurusd | PyneCore 6.9.1, chart feed only | 19 | 6 | 8 | 1 | 0 | 0 | 4 | 0 | 0 | 0 |
| pc691_sec @ C/eurusd | PyneCore 6.9.1, --security from the chart feed | 19 | 6 | 8 | 1 | 0 | 0 | 4 | 0 | 0 | 0 |
| pc691_finer @ C/eurusd | PyneCore 6.9.1 + campaign 1m feed via --security | 19 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 18 |
| pc691_finer_rs @ C/eurusd | PyneCore 6.9.1 + campaign 1m feed via --security, range-start feed | 19 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 18 |
| pc691_best @ C/eurusd | PyneCore 6.9.1, --security + the probe's --from/--to window | 19 | 6 | 8 | 1 | 0 | 0 | 3 | 1 | 0 | 0 |
| pf @ C/f | PineForge, chart feed only | 17 | 14 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pf_finer @ C/f | PineForge + campaign 1m auxiliary security feed | 17 | 0 | 0 | 0 | 0 | 0 | 17 | 0 | 0 | 0 |
| pf_finer_rs @ C/f | PineForge + campaign 1m auxiliary feed, range-start bound | 17 | 17 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pc691 @ C/f | PyneCore 6.9.1, chart feed only | 17 | 8 | 5 | 1 | 2 | 0 | 1 | 0 | 0 | 0 |
| pc691_sec @ C/f | PyneCore 6.9.1, --security from the chart feed | 17 | 8 | 5 | 1 | 2 | 1 | 0 | 0 | 0 | 0 |
| pc691_finer @ C/f | PyneCore 6.9.1 + campaign 1m feed via --security | 17 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 17 |
| pc691_finer_rs @ C/f | PyneCore 6.9.1 + campaign 1m feed via --security, range-start feed | 17 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 17 |
| pc691_best @ C/f | PyneCore 6.9.1, --security + the probe's --from/--to window | 17 | 10 | 4 | 0 | 2 | 1 | 0 | 0 | 0 | 0 |
| pf @ C/f-1d | PineForge, chart feed only | 13 | 10 | 1 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| pf_finer @ C/f-1d | PineForge + campaign 1m auxiliary security feed | 13 | 12 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pf_finer_rs @ C/f-1d | PineForge + campaign 1m auxiliary feed, range-start bound | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pc691 @ C/f-1d | PyneCore 6.9.1, chart feed only | 13 | 3 | 2 | 2 | 2 | 0 | 4 | 0 | 0 | 0 |
| pc691_sec @ C/f-1d | PyneCore 6.9.1, --security from the chart feed | 13 | 3 | 3 | 2 | 2 | 1 | 2 | 0 | 0 | 0 |
| pc691_finer @ C/f-1d | PyneCore 6.9.1 + campaign 1m feed via --security | 13 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 11 |
| pc691_finer_rs @ C/f-1d | PyneCore 6.9.1 + campaign 1m feed via --security, range-start feed | 13 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 11 |
| pc691_best @ C/f-1d | PyneCore 6.9.1, --security + the probe's --from/--to window | 13 | 5 | 3 | 3 | 2 | 0 | 0 | 0 | 0 | 0 |
| pf @ C/nifty | PineForge, chart feed only | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pf_finer @ C/nifty | PineForge + campaign 1m auxiliary security feed | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pf_finer_rs @ C/nifty | PineForge + campaign 1m auxiliary feed, range-start bound | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pc691 @ C/nifty | PyneCore 6.9.1, chart feed only | 9 | 7 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| pc691_sec @ C/nifty | PyneCore 6.9.1, --security from the chart feed | 9 | 7 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| pc691_finer @ C/nifty | PyneCore 6.9.1 + campaign 1m feed via --security | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 |
| pc691_finer_rs @ C/nifty | PyneCore 6.9.1 + campaign 1m feed via --security, range-start feed | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 |
| pc691_best @ C/nifty | PyneCore 6.9.1, --security + the probe's --from/--to window | 9 | 8 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| pf @ C/nifty-1d | PineForge, chart feed only | 8 | 7 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| pf_finer @ C/nifty-1d | PineForge + campaign 1m auxiliary security feed | 8 | 0 | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 |
| pf_finer_rs @ C/nifty-1d | PineForge + campaign 1m auxiliary feed, range-start bound | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pc691 @ C/nifty-1d | PyneCore 6.9.1, chart feed only | 8 | 1 | 3 | 1 | 0 | 1 | 2 | 0 | 0 | 0 |
| pc691_sec @ C/nifty-1d | PyneCore 6.9.1, --security from the chart feed | 8 | 1 | 3 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| pc691_finer @ C/nifty-1d | PyneCore 6.9.1 + campaign 1m feed via --security | 8 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 7 |
| pc691_finer_rs @ C/nifty-1d | PyneCore 6.9.1 + campaign 1m feed via --security, range-start feed | 8 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7 |
| pc691_best @ C/nifty-1d | PyneCore 6.9.1, --security + the probe's --from/--to window | 8 | 3 | 2 | 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| pf @ C/nq1 | PineForge, chart feed only | 9 | 7 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| pf_finer @ C/nq1 | PineForge + campaign 1m auxiliary security feed | 9 | 0 | 0 | 0 | 0 | 0 | 9 | 0 | 0 | 0 |
| pf_finer_rs @ C/nq1 | PineForge + campaign 1m auxiliary feed, range-start bound | 9 | 8 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| pc691 @ C/nq1 | PyneCore 6.9.1, chart feed only | 9 | 6 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 |
| pc691_sec @ C/nq1 | PyneCore 6.9.1, --security from the chart feed | 9 | 7 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| pc691_finer @ C/nq1 | PyneCore 6.9.1 + campaign 1m feed via --security | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 |
| pc691_finer_rs @ C/nq1 | PyneCore 6.9.1 + campaign 1m feed via --security, range-start feed | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 |
| pc691_best @ C/nq1 | PyneCore 6.9.1, --security + the probe's --from/--to window | 9 | 8 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| pf @ C/nq1-1d | PineForge, chart feed only | 8 | 4 | 0 | 2 | 0 | 1 | 1 | 0 | 0 | 0 |
| pf_finer @ C/nq1-1d | PineForge + campaign 1m auxiliary security feed | 8 | 0 | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 |
| pf_finer_rs @ C/nq1-1d | PineForge + campaign 1m auxiliary feed, range-start bound | 8 | 7 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| pc691 @ C/nq1-1d | PyneCore 6.9.1, chart feed only | 8 | 2 | 0 | 0 | 0 | 4 | 2 | 0 | 0 | 0 |
| pc691_sec @ C/nq1-1d | PyneCore 6.9.1, --security from the chart feed | 8 | 2 | 0 | 0 | 0 | 4 | 2 | 0 | 0 | 0 |
| pc691_finer @ C/nq1-1d | PyneCore 6.9.1 + campaign 1m feed via --security | 8 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 7 |
| pc691_finer_rs @ C/nq1-1d | PyneCore 6.9.1 + campaign 1m feed via --security, range-start feed | 8 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 7 |
| pc691_best @ C/nq1-1d | PyneCore 6.9.1, --security + the probe's --from/--to window | 8 | 3 | 2 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| pf @ C/xauusd | PineForge, chart feed only | 19 | 12 | 3 | 0 | 1 | 2 | 1 | 0 | 0 | 0 |
| pf_finer @ C/xauusd | PineForge + campaign 1m auxiliary security feed | 19 | 13 | 3 | 0 | 1 | 2 | 0 | 0 | 0 | 0 |
| pf_finer_rs @ C/xauusd | PineForge + campaign 1m auxiliary feed, range-start bound | 19 | 15 | 3 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| pc691 @ C/xauusd | PyneCore 6.9.1, chart feed only | 19 | 4 | 10 | 1 | 1 | 1 | 2 | 0 | 0 | 0 |
| pc691_sec @ C/xauusd | PyneCore 6.9.1, --security from the chart feed | 19 | 4 | 10 | 1 | 1 | 1 | 2 | 0 | 0 | 0 |
| pc691_finer @ C/xauusd | PyneCore 6.9.1 + campaign 1m feed via --security | 19 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 18 |
| pc691_finer_rs @ C/xauusd | PyneCore 6.9.1 + campaign 1m feed via --security, range-start feed | 19 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 18 |
| pc691_best @ C/xauusd | PyneCore 6.9.1, --security + the probe's --from/--to window | 19 | 10 | 6 | 0 | 1 | 1 | 0 | 1 | 0 | 0 |
| pf @ C/xauusd-1d | PineForge, chart feed only | 12 | 7 | 2 | 1 | 0 | 0 | 2 | 0 | 0 | 0 |
| pf_finer @ C/xauusd-1d | PineForge + campaign 1m auxiliary security feed | 12 | 7 | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| pf_finer_rs @ C/xauusd-1d | PineForge + campaign 1m auxiliary feed, range-start bound | 12 | 11 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| pc691 @ C/xauusd-1d | PyneCore 6.9.1, chart feed only | 12 | 6 | 2 | 1 | 1 | 0 | 2 | 0 | 0 | 0 |
| pc691_sec @ C/xauusd-1d | PyneCore 6.9.1, --security from the chart feed | 12 | 6 | 2 | 1 | 1 | 0 | 2 | 0 | 0 | 0 |
| pc691_finer @ C/xauusd-1d | PyneCore 6.9.1 + campaign 1m feed via --security | 12 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 10 |
| pc691_finer_rs @ C/xauusd-1d | PyneCore 6.9.1 + campaign 1m feed via --security, range-start feed | 12 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 10 |
| pc691_best @ C/xauusd-1d | PyneCore 6.9.1, --security + the probe's --from/--to window | 12 | 7 | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |


## CAMPAIGN CROSS-CHECK — the campaign's own grade vs this benchmark's, probe by probe

The parity campaign has already measured every probe in sets B and C. This table is the
check that the benchmark reproduces it. `campaign` is the active baseline's snapshot
(engine bfdbe9618c12 / codegen 3fd97fe28abd); `benchmark` is the PineForge headline column
of this run. A row with a non-zero `delta` is itemised below the table, never averaged away.

| set | lane | sampled | campaign_excellent | campaign_strong | campaign_other | benchmark_excellent | benchmark_strong | benchmark_other | delta |
|---|---|---|---|---|---|---|---|---|---|
| B | BINANCE:ETHUSDT.P@15 (public corpus) | 309 | 309 | 0 | 0 | 309 | 0 | 0 | 0 |
| B | ALL | 309 | 309 | 0 | 0 | 309 | 0 | 0 | 0 |
| C | NASDAQ:AAPL@15 | 18 | 18 | 0 | 0 | 18 | 0 | 0 | 0 |
| C | BINANCE:BTCUSDT@15 | 18 | 18 | 0 | 0 | 18 | 0 | 0 | 0 |
| C | BINANCE:BTCUSDT@1D | 13 | 13 | 0 | 0 | 13 | 0 | 0 | 0 |
| C | CME_MINI:ES1!@15 | 9 | 9 | 0 | 0 | 9 | 0 | 0 | 0 |
| C | CME_MINI:ES1!@1D | 8 | 8 | 0 | 0 | 8 | 0 | 0 | 0 |
| C | BINANCE:ETHUSDT.P@15 | 20 | 20 | 0 | 0 | 20 | 0 | 0 | 0 |
| C | OANDA:EURUSD@15 | 19 | 17 | 2 | 0 | 17 | 2 | 0 | 0 |
| C | NYSE:F@15 | 17 | 17 | 0 | 0 | 17 | 0 | 0 | 0 |
| C | NYSE:F@1D | 13 | 13 | 0 | 0 | 13 | 0 | 0 | 0 |
| C | NSE:NIFTY@15 | 9 | 9 | 0 | 0 | 9 | 0 | 0 | 0 |
| C | NSE:NIFTY@1D | 8 | 8 | 0 | 0 | 8 | 0 | 0 | 0 |
| C | CME_MINI:NQ1!@15 | 9 | 9 | 0 | 0 | 9 | 0 | 0 | 0 |
| C | CME_MINI:NQ1!@1D | 8 | 8 | 0 | 0 | 8 | 0 | 0 | 0 |
| C | OANDA:XAUUSD@15 | 19 | 19 | 0 | 0 | 19 | 0 | 0 | 0 |
| C | OANDA:XAUUSD@1D | 12 | 12 | 0 | 0 | 12 | 0 | 0 | 0 |
| C | ALL | 200 | 198 | 2 | 0 | 198 | 2 | 0 | 0 |


**Residual: zero.** Every probe the campaign has measured carries the campaign's own tier,
match percentage and trade-count delta in this benchmark.


## CONDITIONAL — what the other engine does where one engine is exact

A conditional that runs only one way is advocacy, not evidence, so both directions are here.
Neither replaces a headline number: each restricts the sample to one engine's own exact probes
and reports what the others grade on exactly that restricted sample.


### Selector: PineForge - BEST SUPPORTED CONFIGURATION — restricted to the probes PineForge reproduces trade-for-trade (its headline tier is `excellent`); the unrestricted tables above remain the headline

| set | lane | engine | n | excellent | strong | moderate | weak | minimal | errors | timeouts | not_run |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | ALL | PineForge - BEST SUPPORTED CONFIGURATION | 90 | 90 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A | ALL | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 90 | 82 | 8 | 0 | 0 | 0 | 0 | 0 | 0 |
| A | ALL | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 90 | 69 | 8 | 10 | 2 | 0 | 1 | 0 | 0 |
| B | ALL | PineForge - BEST SUPPORTED CONFIGURATION | 310 | 310 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| B | ALL | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 310 | 272 | 23 | 0 | 11 | 1 | 3 | 0 | 0 |
| B | ALL | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 310 | 233 | 24 | 8 | 11 | 1 | 33 | 0 | 0 |
| C | ALL | PineForge - BEST SUPPORTED CONFIGURATION | 198 | 198 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | ALL | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 198 | 114 | 40 | 15 | 15 | 6 | 8 | 0 | 0 |
| C | ALL | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 198 | 60 | 46 | 23 | 5 | 10 | 54 | 0 | 0 |
| C | NASDAQ:AAPL@15 | PineForge - BEST SUPPORTED CONFIGURATION | 18 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | NASDAQ:AAPL@15 | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 18 | 9 | 4 | 1 | 4 | 0 | 0 | 0 | 0 |
| C | NASDAQ:AAPL@15 | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 18 | 6 | 2 | 2 | 0 | 0 | 8 | 0 | 0 |
| C | BINANCE:BTCUSDT@15 | PineForge - BEST SUPPORTED CONFIGURATION | 18 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | BINANCE:BTCUSDT@15 | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 18 | 12 | 2 | 0 | 2 | 0 | 2 | 0 | 0 |
| C | BINANCE:BTCUSDT@15 | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 18 | 2 | 7 | 1 | 1 | 1 | 6 | 0 | 0 |
| C | BINANCE:BTCUSDT@1D | PineForge - BEST SUPPORTED CONFIGURATION | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | BINANCE:BTCUSDT@1D | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 13 | 7 | 2 | 3 | 1 | 0 | 0 | 0 | 0 |
| C | BINANCE:BTCUSDT@1D | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 13 | 3 | 1 | 6 | 0 | 0 | 3 | 0 | 0 |
| C | CME_MINI:ES1!@15 | PineForge - BEST SUPPORTED CONFIGURATION | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | CME_MINI:ES1!@15 | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 9 | 8 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | CME_MINI:ES1!@15 | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 9 | 7 | 0 | 0 | 0 | 1 | 1 | 0 | 0 |
| C | CME_MINI:ES1!@1D | PineForge - BEST SUPPORTED CONFIGURATION | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | CME_MINI:ES1!@1D | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 8 | 1 | 3 | 1 | 0 | 3 | 0 | 0 | 0 |
| C | CME_MINI:ES1!@1D | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 8 | 0 | 3 | 0 | 0 | 2 | 3 | 0 | 0 |
| C | BINANCE:ETHUSDT.P@15 | PineForge - BEST SUPPORTED CONFIGURATION | 20 | 20 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | BINANCE:ETHUSDT.P@15 | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 20 | 11 | 7 | 0 | 2 | 0 | 0 | 0 | 0 |
| C | BINANCE:ETHUSDT.P@15 | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 20 | 4 | 6 | 0 | 3 | 1 | 6 | 0 | 0 |
| C | OANDA:EURUSD@15 | PineForge - BEST SUPPORTED CONFIGURATION | 17 | 17 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | OANDA:EURUSD@15 | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 17 | 8 | 4 | 1 | 0 | 0 | 4 | 0 | 0 |
| C | OANDA:EURUSD@15 | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 17 | 4 | 3 | 3 | 1 | 2 | 4 | 0 | 0 |
| C | NYSE:F@15 | PineForge - BEST SUPPORTED CONFIGURATION | 17 | 17 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | NYSE:F@15 | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 17 | 13 | 1 | 0 | 2 | 1 | 0 | 0 | 0 |
| C | NYSE:F@15 | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 17 | 9 | 3 | 1 | 0 | 0 | 4 | 0 | 0 |
| C | NYSE:F@1D | PineForge - BEST SUPPORTED CONFIGURATION | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | NYSE:F@1D | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 13 | 5 | 3 | 3 | 2 | 0 | 0 | 0 | 0 |
| C | NYSE:F@1D | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 13 | 4 | 2 | 3 | 0 | 0 | 4 | 0 | 0 |
| C | NSE:NIFTY@15 | PineForge - BEST SUPPORTED CONFIGURATION | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | NSE:NIFTY@15 | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 9 | 8 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| C | NSE:NIFTY@15 | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 9 | 5 | 1 | 1 | 0 | 0 | 2 | 0 | 0 |
| C | NSE:NIFTY@1D | PineForge - BEST SUPPORTED CONFIGURATION | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | NSE:NIFTY@1D | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 8 | 3 | 2 | 2 | 1 | 0 | 0 | 0 | 0 |
| C | NSE:NIFTY@1D | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 8 | 2 | 2 | 2 | 0 | 0 | 2 | 0 | 0 |
| C | CME_MINI:NQ1!@15 | PineForge - BEST SUPPORTED CONFIGURATION | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | CME_MINI:NQ1!@15 | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 9 | 8 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| C | CME_MINI:NQ1!@15 | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 9 | 5 | 1 | 0 | 0 | 0 | 3 | 0 | 0 |
| C | CME_MINI:NQ1!@1D | PineForge - BEST SUPPORTED CONFIGURATION | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | CME_MINI:NQ1!@1D | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 8 | 3 | 2 | 3 | 0 | 0 | 0 | 0 | 0 |
| C | CME_MINI:NQ1!@1D | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 8 | 3 | 1 | 3 | 0 | 0 | 1 | 0 | 0 |
| C | OANDA:XAUUSD@15 | PineForge - BEST SUPPORTED CONFIGURATION | 19 | 19 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | OANDA:XAUUSD@15 | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 19 | 10 | 6 | 0 | 1 | 1 | 1 | 0 | 0 |
| C | OANDA:XAUUSD@15 | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 19 | 0 | 12 | 0 | 0 | 3 | 4 | 0 | 0 |
| C | OANDA:XAUUSD@1D | PineForge - BEST SUPPORTED CONFIGURATION | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | OANDA:XAUUSD@1D | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 12 | 8 | 3 | 0 | 0 | 0 | 1 | 0 | 0 |
| C | OANDA:XAUUSD@1D | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 12 | 6 | 2 | 1 | 0 | 0 | 3 | 0 | 0 |

Sets A and B are single-lane (set A: BINANCE:ETHUSDT@15, the public benchmark suite; set B: BINANCE:ETHUSDT.P@15, the public corpus), so they carry no per-lane breakdown.


### Selector: PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION — restricted to the probes PyneCore 6.9.1 reproduces trade-for-trade (its headline tier is `excellent`); the unrestricted tables above remain the headline

| set | lane | engine | n | excellent | strong | moderate | weak | minimal | errors | timeouts | not_run |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | ALL | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 82 | 82 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A | ALL | PineForge - BEST SUPPORTED CONFIGURATION | 82 | 82 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A | ALL | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 82 | 69 | 1 | 10 | 1 | 0 | 1 | 0 | 0 |
| B | ALL | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 272 | 272 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| B | ALL | PineForge - BEST SUPPORTED CONFIGURATION | 272 | 272 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| B | ALL | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 272 | 233 | 5 | 8 | 5 | 0 | 21 | 0 | 0 |
| C | ALL | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 114 | 114 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | ALL | PineForge - BEST SUPPORTED CONFIGURATION | 114 | 114 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | ALL | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 114 | 59 | 24 | 7 | 4 | 2 | 18 | 0 | 0 |
| C | NASDAQ:AAPL@15 | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | NASDAQ:AAPL@15 | PineForge - BEST SUPPORTED CONFIGURATION | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | NASDAQ:AAPL@15 | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 9 | 6 | 0 | 1 | 0 | 0 | 2 | 0 | 0 |
| C | BINANCE:BTCUSDT@15 | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | BINANCE:BTCUSDT@15 | PineForge - BEST SUPPORTED CONFIGURATION | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | BINANCE:BTCUSDT@15 | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 12 | 2 | 6 | 0 | 1 | 1 | 2 | 0 | 0 |
| C | BINANCE:BTCUSDT@1D | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | BINANCE:BTCUSDT@1D | PineForge - BEST SUPPORTED CONFIGURATION | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | BINANCE:BTCUSDT@1D | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 7 | 3 | 0 | 2 | 0 | 0 | 2 | 0 | 0 |
| C | CME_MINI:ES1!@15 | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | CME_MINI:ES1!@15 | PineForge - BEST SUPPORTED CONFIGURATION | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | CME_MINI:ES1!@15 | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 8 | 7 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| C | CME_MINI:ES1!@1D | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | CME_MINI:ES1!@1D | PineForge - BEST SUPPORTED CONFIGURATION | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | CME_MINI:ES1!@1D | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | BINANCE:ETHUSDT.P@15 | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 11 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | BINANCE:ETHUSDT.P@15 | PineForge - BEST SUPPORTED CONFIGURATION | 11 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | BINANCE:ETHUSDT.P@15 | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 11 | 4 | 3 | 0 | 2 | 0 | 2 | 0 | 0 |
| C | OANDA:EURUSD@15 | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | OANDA:EURUSD@15 | PineForge - BEST SUPPORTED CONFIGURATION | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | OANDA:EURUSD@15 | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 8 | 4 | 1 | 2 | 1 | 0 | 0 | 0 | 0 |
| C | NYSE:F@15 | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | NYSE:F@15 | PineForge - BEST SUPPORTED CONFIGURATION | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | NYSE:F@15 | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 13 | 9 | 3 | 1 | 0 | 0 | 0 | 0 | 0 |
| C | NYSE:F@1D | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | NYSE:F@1D | PineForge - BEST SUPPORTED CONFIGURATION | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | NYSE:F@1D | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 5 | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| C | NSE:NIFTY@15 | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | NSE:NIFTY@15 | PineForge - BEST SUPPORTED CONFIGURATION | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | NSE:NIFTY@15 | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 8 | 5 | 1 | 0 | 0 | 0 | 2 | 0 | 0 |
| C | NSE:NIFTY@1D | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | NSE:NIFTY@1D | PineForge - BEST SUPPORTED CONFIGURATION | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | NSE:NIFTY@1D | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 3 | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| C | CME_MINI:NQ1!@15 | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | CME_MINI:NQ1!@15 | PineForge - BEST SUPPORTED CONFIGURATION | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | CME_MINI:NQ1!@15 | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 8 | 5 | 1 | 0 | 0 | 0 | 2 | 0 | 0 |
| C | CME_MINI:NQ1!@1D | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | CME_MINI:NQ1!@1D | PineForge - BEST SUPPORTED CONFIGURATION | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | CME_MINI:NQ1!@1D | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 3 | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| C | OANDA:XAUUSD@15 | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | OANDA:XAUUSD@15 | PineForge - BEST SUPPORTED CONFIGURATION | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | OANDA:XAUUSD@15 | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 10 | 0 | 8 | 0 | 0 | 1 | 1 | 0 | 0 |
| C | OANDA:XAUUSD@1D | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | OANDA:XAUUSD@1D | PineForge - BEST SUPPORTED CONFIGURATION | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | OANDA:XAUUSD@1D | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 8 | 6 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |

Sets A and B are single-lane (set A: BINANCE:ETHUSDT@15, the public benchmark suite; set B: BINANCE:ETHUSDT.P@15, the public corpus), so they carry no per-lane breakdown.


## Lane facts and per-lane results (lanes.csv, mirrored)

| lane | symbolTimeframe | bars | sampled | pf_excellent | pf_strong | pf_other | pc691_excellent | pc691_strong | pc691_other | pc646_excellent | pc646_strong | pc646_other | cond_pfExact_n | cond_pfExact_pc691_excellent | cond_pc691Exact_n | cond_pc691Exact_pf_excellent | campaign_excellent | campaign_strong | campaign_delta |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| aapl | NASDAQ:AAPL@15 | 32536 | 18 | 18 | 0 | 0 | 9 | 4 | 5 | 6 | 2 | 10 | 18 | 9 | 9 | 9 | 18 | 0 | 0 |
| btcusdt-1d | BINANCE:BTCUSDT@1D | 1827 | 13 | 13 | 0 | 0 | 7 | 2 | 4 | 3 | 1 | 9 | 13 | 7 | 7 | 7 | 13 | 0 | 0 |
| btcusdt | BINANCE:BTCUSDT@15 | 175261 | 18 | 18 | 0 | 0 | 12 | 2 | 4 | 2 | 7 | 9 | 18 | 12 | 12 | 12 | 18 | 0 | 0 |
| es1-1d | CME_MINI:ES1!@1D | 1259 | 8 | 8 | 0 | 0 | 1 | 3 | 4 | 0 | 3 | 5 | 8 | 1 | 1 | 1 | 8 | 0 | 0 |
| es1 | CME_MINI:ES1!@15 | 118005 | 9 | 9 | 0 | 0 | 8 | 1 | 0 | 7 | 0 | 2 | 9 | 8 | 8 | 8 | 9 | 0 | 0 |
| eth-corpus | BINANCE:ETHUSDT.P@15 (public corpus) | 222295 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| eth-suite | BINANCE:ETHUSDT@15 (public benchmark suite) | 53929 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| eth | BINANCE:ETHUSDT.P@15 | 222295 | 20 | 20 | 0 | 0 | 11 | 7 | 2 | 4 | 6 | 10 | 20 | 11 | 11 | 11 | 20 | 0 | 0 |
| eurusd | OANDA:EURUSD@15 | 124590 | 19 | 17 | 2 | 0 | 8 | 6 | 5 | 4 | 3 | 12 | 17 | 8 | 8 | 8 | 17 | 2 | 0 |
| f-1d | NYSE:F@1D | 1255 | 13 | 13 | 0 | 0 | 5 | 3 | 5 | 4 | 2 | 7 | 13 | 5 | 5 | 5 | 13 | 0 | 0 |
| f | NYSE:F@15 | 32512 | 17 | 17 | 0 | 0 | 13 | 1 | 3 | 9 | 3 | 5 | 17 | 13 | 13 | 13 | 17 | 0 | 0 |
| nifty-1d | NSE:NIFTY@1D | 1240 | 8 | 8 | 0 | 0 | 3 | 2 | 3 | 2 | 2 | 4 | 8 | 3 | 3 | 3 | 8 | 0 | 0 |
| nifty | NSE:NIFTY@15 | 30868 | 9 | 9 | 0 | 0 | 8 | 0 | 1 | 5 | 1 | 3 | 9 | 8 | 8 | 8 | 9 | 0 | 0 |
| nq1-1d | CME_MINI:NQ1!@1D | 1259 | 8 | 8 | 0 | 0 | 3 | 2 | 3 | 3 | 1 | 4 | 8 | 3 | 3 | 3 | 8 | 0 | 0 |
| nq1 | CME_MINI:NQ1!@15 | 118005 | 9 | 9 | 0 | 0 | 8 | 0 | 1 | 5 | 1 | 3 | 9 | 8 | 8 | 8 | 9 | 0 | 0 |
| xauusd-1d | OANDA:XAUUSD@1D | 1291 | 12 | 12 | 0 | 0 | 8 | 3 | 1 | 6 | 2 | 4 | 12 | 8 | 8 | 8 | 12 | 0 | 0 |
| xauusd | OANDA:XAUUSD@15 | 118249 | 19 | 19 | 0 | 0 | 10 | 6 | 3 | 0 | 12 | 7 | 19 | 10 | 10 | 10 | 19 | 0 | 0 |


## Showcase — hard public-corpus strategies PineForge reproduces exactly

**This is illustration, not measurement.** These rows are a hand-picked reading aid drawn from
set B's public corpus; they are already counted in set B's headline and are NOT a separate
result, a separate sample, or a claim about any other strategy. Each is a PUBLIC corpus
script (pineforge-corpus, `validation/`), reproduced by PineForge at the `excellent` tier
under the campaign verifier, and each exercises a behaviour that is hard to get right.

| strategy | feature | tvTrades | pineforgeTier | matchPct | countAbsDelta |
|---|---|---|---|---|---|
| bracket-atr-trail-series-int-points-01 | a bracket exit with a trailing stop | 792 | excellent | 100.000 | 0 |
| bracket-compass-partial-ladder-01 | a partial close (FIFO lot fragmentation) | 836 | excellent | 100.000 | 0 |
| mtf-htf-60-close-change-baseline-01 | a multi-timeframe request.security | 8779 | excellent | 100.000 | 0 |
| pyramid-deferred-flip-close-all-01 | pyramiding into a position | 2356 | excellent | 100.000 | 0 |
| session-ny-spring-forward-dst-01 | a session window across a DST spring-forward | 396 | excellent | 100.000 | 0 |
| magnifier-tick-dist-endpoints-rsi-cross-08a | the intrabar bar magnifier | 2345 | excellent | 100.000 | 0 |
| bracket-rivet-calc-on-fill-01 | calc_on_order_fills intrabar re-evaluation | 541 | excellent | 100.000 | 0 |
| order-process-on-close-true-01 | process_orders_on_close | 857 | excellent | 100.000 | 0 |


### Feature buckets — set A (a script counts in every feature it uses)

| bucket | engine | n | excellent | strong | moderate | weak | minimal | fail | not_run | excellentPct | excellentStrongPct |
|---|---|---|---|---|---|---|---|---|---|---|---|
| trail | PineForge - BEST SUPPORTED CONFIGURATION | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 6 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0.0 | 0.0 |
| trail | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 6 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0.0 | 0.0 |
| trail | PineForge (full feed, tape-window) | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PineForge (range-start feed) | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PineForge (full feed, raw) | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PyneCore 6.9.1 (full feed, --security supplied) | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PyneCore 6.9.1 (full feed) | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PyneCore 6.4.6 (full feed) | 6 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0.0 | 0.0 |
| trail | PyneCore 6.9.1 (recompiled 6.0.66, full feed) | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| brackets | PineForge - BEST SUPPORTED CONFIGURATION | 22 | 20 | 2 | 0 | 0 | 0 | 0 | 0 | 90.9 | 100.0 |
| brackets | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 22 | 20 | 2 | 0 | 0 | 0 | 0 | 0 | 90.9 | 100.0 |
| brackets | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 22 | 10 | 2 | 10 | 0 | 0 | 0 | 0 | 45.5 | 54.5 |
| brackets | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 22 | 0 | 0 | 0 | 0 | 0 | 22 | 0 | 0.0 | 0.0 |
| brackets | PineForge (full feed, tape-window) | 22 | 20 | 2 | 0 | 0 | 0 | 0 | 0 | 90.9 | 100.0 |
| brackets | PineForge (range-start feed) | 22 | 20 | 2 | 0 | 0 | 0 | 0 | 0 | 90.9 | 100.0 |
| brackets | PineForge (full feed, raw) | 22 | 20 | 2 | 0 | 0 | 0 | 0 | 0 | 90.9 | 100.0 |
| brackets | PyneCore 6.9.1 (full feed, --security supplied) | 22 | 20 | 2 | 0 | 0 | 0 | 0 | 0 | 90.9 | 100.0 |
| brackets | PyneCore 6.9.1 (full feed) | 22 | 20 | 2 | 0 | 0 | 0 | 0 | 0 | 90.9 | 100.0 |
| brackets | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 22 | 20 | 2 | 0 | 0 | 0 | 0 | 0 | 90.9 | 100.0 |
| brackets | PyneCore 6.4.6 (full feed) | 22 | 10 | 2 | 10 | 0 | 0 | 0 | 0 | 45.5 | 54.5 |
| brackets | PyneCore 6.9.1 (recompiled 6.0.66, full feed) | 22 | 20 | 2 | 0 | 0 | 0 | 0 | 0 | 90.9 | 100.0 |
| partial | PineForge - BEST SUPPORTED CONFIGURATION | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 66.7 | 100.0 |
| partial | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 66.7 | 100.0 |
| partial | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 3 | 0 | 1 | 2 | 0 | 0 | 0 | 0 | 0.0 | 33.3 |
| partial | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 3 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0.0 | 0.0 |
| partial | PineForge (full feed, tape-window) | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 66.7 | 100.0 |
| partial | PineForge (range-start feed) | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 66.7 | 100.0 |
| partial | PineForge (full feed, raw) | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 66.7 | 100.0 |
| partial | PyneCore 6.9.1 (full feed, --security supplied) | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 66.7 | 100.0 |
| partial | PyneCore 6.9.1 (full feed) | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 66.7 | 100.0 |
| partial | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 66.7 | 100.0 |
| partial | PyneCore 6.4.6 (full feed) | 3 | 0 | 1 | 2 | 0 | 0 | 0 | 0 | 0.0 | 33.3 |
| partial | PyneCore 6.9.1 (recompiled 6.0.66, full feed) | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 66.7 | 100.0 |
| pyramiding | PineForge - BEST SUPPORTED CONFIGURATION | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pyramiding | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pyramiding | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pyramiding | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 3 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0.0 | 0.0 |
| pyramiding | PineForge (full feed, tape-window) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pyramiding | PineForge (range-start feed) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pyramiding | PineForge (full feed, raw) | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 66.7 | 100.0 |
| pyramiding | PyneCore 6.9.1 (full feed, --security supplied) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pyramiding | PyneCore 6.9.1 (full feed) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pyramiding | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pyramiding | PyneCore 6.4.6 (full feed) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pyramiding | PyneCore 6.9.1 (recompiled 6.0.66, full feed) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PineForge - BEST SUPPORTED CONFIGURATION | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0.0 | 0.0 |
| pooc | PineForge (full feed, tape-window) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PineForge (range-start feed) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PineForge (full feed, raw) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PyneCore 6.9.1 (full feed, --security supplied) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PyneCore 6.9.1 (full feed) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PyneCore 6.4.6 (full feed) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PyneCore 6.9.1 (recompiled 6.0.66, full feed) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| margin_lt100 | PineForge - BEST SUPPORTED CONFIGURATION | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| margin_lt100 | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| margin_lt100 | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| margin_lt100 | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0.0 | 0.0 |
| margin_lt100 | PineForge (full feed, tape-window) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| margin_lt100 | PineForge (range-start feed) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| margin_lt100 | PineForge (full feed, raw) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| margin_lt100 | PyneCore 6.9.1 (full feed, --security supplied) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| margin_lt100 | PyneCore 6.9.1 (full feed) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| margin_lt100 | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| margin_lt100 | PyneCore 6.4.6 (full feed) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| margin_lt100 | PyneCore 6.9.1 (recompiled 6.0.66, full feed) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| magnifier | PineForge - BEST SUPPORTED CONFIGURATION | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 5 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0.0 | 0.0 |
| magnifier | PineForge (full feed, tape-window) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PineForge (range-start feed) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PineForge (full feed, raw) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PyneCore 6.9.1 (full feed, --security supplied) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PyneCore 6.9.1 (full feed) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PyneCore 6.4.6 (full feed) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PyneCore 6.9.1 (recompiled 6.0.66, full feed) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| var_state | PineForge - BEST SUPPORTED CONFIGURATION | 22 | 17 | 5 | 0 | 0 | 0 | 0 | 0 | 77.3 | 100.0 |
| var_state | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 22 | 17 | 5 | 0 | 0 | 0 | 0 | 0 | 77.3 | 100.0 |
| var_state | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 22 | 16 | 5 | 0 | 0 | 0 | 1 | 0 | 72.7 | 95.5 |
| var_state | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 22 | 0 | 0 | 0 | 0 | 0 | 22 | 0 | 0.0 | 0.0 |
| var_state | PineForge (full feed, tape-window) | 22 | 16 | 6 | 0 | 0 | 0 | 0 | 0 | 72.7 | 100.0 |
| var_state | PineForge (range-start feed) | 22 | 16 | 6 | 0 | 0 | 0 | 0 | 0 | 72.7 | 100.0 |
| var_state | PineForge (full feed, raw) | 22 | 17 | 5 | 0 | 0 | 0 | 0 | 0 | 77.3 | 100.0 |
| var_state | PyneCore 6.9.1 (full feed, --security supplied) | 22 | 17 | 5 | 0 | 0 | 0 | 0 | 0 | 77.3 | 100.0 |
| var_state | PyneCore 6.9.1 (full feed) | 22 | 17 | 5 | 0 | 0 | 0 | 0 | 0 | 77.3 | 100.0 |
| var_state | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 22 | 17 | 5 | 0 | 0 | 0 | 0 | 0 | 77.3 | 100.0 |
| var_state | PyneCore 6.4.6 (full feed) | 22 | 16 | 5 | 0 | 0 | 0 | 1 | 0 | 72.7 | 95.5 |
| var_state | PyneCore 6.9.1 (recompiled 6.0.66, full feed) | 22 | 17 | 5 | 0 | 0 | 0 | 0 | 0 | 77.3 | 100.0 |
| arrays | PineForge - BEST SUPPORTED CONFIGURATION | 7 | 6 | 1 | 0 | 0 | 0 | 0 | 0 | 85.7 | 100.0 |
| arrays | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 7 | 4 | 3 | 0 | 0 | 0 | 0 | 0 | 57.1 | 100.0 |
| arrays | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 7 | 4 | 3 | 0 | 0 | 0 | 0 | 0 | 57.1 | 100.0 |
| arrays | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 7 | 0 | 0 | 0 | 0 | 0 | 7 | 0 | 0.0 | 0.0 |
| arrays | PineForge (full feed, tape-window) | 7 | 6 | 1 | 0 | 0 | 0 | 0 | 0 | 85.7 | 100.0 |
| arrays | PineForge (range-start feed) | 7 | 6 | 1 | 0 | 0 | 0 | 0 | 0 | 85.7 | 100.0 |
| arrays | PineForge (full feed, raw) | 7 | 6 | 1 | 0 | 0 | 0 | 0 | 0 | 85.7 | 100.0 |
| arrays | PyneCore 6.9.1 (full feed, --security supplied) | 7 | 4 | 3 | 0 | 0 | 0 | 0 | 0 | 57.1 | 100.0 |
| arrays | PyneCore 6.9.1 (full feed) | 7 | 4 | 3 | 0 | 0 | 0 | 0 | 0 | 57.1 | 100.0 |
| arrays | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 7 | 4 | 3 | 0 | 0 | 0 | 0 | 0 | 57.1 | 100.0 |
| arrays | PyneCore 6.4.6 (full feed) | 7 | 4 | 3 | 0 | 0 | 0 | 0 | 0 | 57.1 | 100.0 |
| arrays | PyneCore 6.9.1 (recompiled 6.0.66, full feed) | 7 | 4 | 3 | 0 | 0 | 0 | 0 | 0 | 57.1 | 100.0 |


### Feature buckets — set B (a script counts in every feature it uses)

| bucket | engine | n | excellent | strong | moderate | weak | minimal | fail | not_run | excellentPct | excellentStrongPct |
|---|---|---|---|---|---|---|---|---|---|---|---|
| trail | PineForge - BEST SUPPORTED CONFIGURATION | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 7 | 0 | 0 | 5 | 0 | 0 | 2 | 0 | 0.0 | 0.0 |
| trail | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PineForge (full feed, tape-window) | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PineForge (range-start feed) | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PineForge (full feed, raw) | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PineForge (+ campaign 1m auxiliary feed) | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PineForge (+ campaign 1m auxiliary feed, range-start bound) | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PyneCore 6.9.1 (full feed, --security supplied) | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PyneCore 6.9.1 (full feed) | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PyneCore 6.9.1 (range-start feed) | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PyneCore 6.4.6 (full feed) | 7 | 0 | 0 | 5 | 0 | 0 | 2 | 0 | 0.0 | 0.0 |
| trail | PyneCore 6.4.6 (range-start feed) | 7 | 0 | 0 | 5 | 0 | 0 | 2 | 0 | 0.0 | 0.0 |
| brackets | PineForge - BEST SUPPORTED CONFIGURATION | 59 | 59 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| brackets | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 59 | 54 | 3 | 0 | 2 | 0 | 0 | 0 | 91.5 | 96.6 |
| brackets | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 59 | 38 | 4 | 7 | 3 | 1 | 6 | 0 | 64.4 | 71.2 |
| brackets | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 59 | 59 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| brackets | PineForge (full feed, tape-window) | 59 | 59 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| brackets | PineForge (range-start feed) | 59 | 54 | 2 | 0 | 0 | 3 | 0 | 0 | 91.5 | 94.9 |
| brackets | PineForge (full feed, raw) | 59 | 36 | 19 | 0 | 1 | 3 | 0 | 0 | 61.0 | 93.2 |
| brackets | PineForge (+ campaign 1m auxiliary feed) | 59 | 56 | 0 | 0 | 0 | 0 | 3 | 0 | 94.9 | 94.9 |
| brackets | PineForge (+ campaign 1m auxiliary feed, range-start bound) | 59 | 51 | 2 | 0 | 0 | 3 | 3 | 0 | 86.4 | 89.8 |
| brackets | PyneCore 6.9.1 (full feed, --security supplied) | 59 | 34 | 19 | 0 | 3 | 0 | 3 | 0 | 57.6 | 89.8 |
| brackets | PyneCore 6.9.1 (full feed) | 59 | 34 | 19 | 0 | 3 | 0 | 3 | 0 | 57.6 | 89.8 |
| brackets | PyneCore 6.9.1 (range-start feed) | 59 | 54 | 3 | 0 | 2 | 0 | 0 | 0 | 91.5 | 96.6 |
| brackets | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 59 | 34 | 19 | 0 | 3 | 0 | 3 | 0 | 57.6 | 89.8 |
| brackets | PyneCore 6.4.6 (full feed) | 59 | 23 | 18 | 7 | 4 | 1 | 6 | 0 | 39.0 | 69.5 |
| brackets | PyneCore 6.4.6 (range-start feed) | 59 | 38 | 4 | 7 | 3 | 1 | 6 | 0 | 64.4 | 71.2 |
| partial | PineForge - BEST SUPPORTED CONFIGURATION | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| partial | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| partial | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 3 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 33.3 | 33.3 |
| partial | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| partial | PineForge (full feed, tape-window) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| partial | PineForge (range-start feed) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| partial | PineForge (full feed, raw) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| partial | PineForge (+ campaign 1m auxiliary feed) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| partial | PineForge (+ campaign 1m auxiliary feed, range-start bound) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| partial | PyneCore 6.9.1 (full feed, --security supplied) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| partial | PyneCore 6.9.1 (full feed) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| partial | PyneCore 6.9.1 (range-start feed) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| partial | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| partial | PyneCore 6.4.6 (full feed) | 3 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 33.3 | 33.3 |
| partial | PyneCore 6.4.6 (range-start feed) | 3 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 33.3 | 33.3 |
| pyramiding | PineForge - BEST SUPPORTED CONFIGURATION | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pyramiding | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 10 | 9 | 0 | 0 | 0 | 1 | 0 | 0 | 90.0 | 90.0 |
| pyramiding | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 10 | 8 | 0 | 1 | 0 | 0 | 1 | 0 | 80.0 | 80.0 |
| pyramiding | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pyramiding | PineForge (full feed, tape-window) | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pyramiding | PineForge (range-start feed) | 10 | 9 | 0 | 0 | 0 | 1 | 0 | 0 | 90.0 | 90.0 |
| pyramiding | PineForge (full feed, raw) | 10 | 7 | 2 | 0 | 0 | 1 | 0 | 0 | 70.0 | 90.0 |
| pyramiding | PineForge (+ campaign 1m auxiliary feed) | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pyramiding | PineForge (+ campaign 1m auxiliary feed, range-start bound) | 10 | 9 | 0 | 0 | 0 | 1 | 0 | 0 | 90.0 | 90.0 |
| pyramiding | PyneCore 6.9.1 (full feed, --security supplied) | 10 | 8 | 1 | 0 | 0 | 1 | 0 | 0 | 80.0 | 90.0 |
| pyramiding | PyneCore 6.9.1 (full feed) | 10 | 8 | 1 | 0 | 0 | 1 | 0 | 0 | 80.0 | 90.0 |
| pyramiding | PyneCore 6.9.1 (range-start feed) | 10 | 8 | 1 | 0 | 0 | 1 | 0 | 0 | 80.0 | 90.0 |
| pyramiding | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 10 | 8 | 1 | 0 | 0 | 1 | 0 | 0 | 80.0 | 90.0 |
| pyramiding | PyneCore 6.4.6 (full feed) | 10 | 7 | 1 | 1 | 0 | 0 | 1 | 0 | 70.0 | 80.0 |
| pyramiding | PyneCore 6.4.6 (range-start feed) | 10 | 7 | 1 | 1 | 0 | 0 | 1 | 0 | 70.0 | 80.0 |
| calc_on_fills | PineForge - BEST SUPPORTED CONFIGURATION | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| calc_on_fills | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| calc_on_fills | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| calc_on_fills | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| calc_on_fills | PineForge (full feed, tape-window) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| calc_on_fills | PineForge (range-start feed) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| calc_on_fills | PineForge (full feed, raw) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| calc_on_fills | PineForge (+ campaign 1m auxiliary feed) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| calc_on_fills | PineForge (+ campaign 1m auxiliary feed, range-start bound) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| calc_on_fills | PyneCore 6.9.1 (full feed, --security supplied) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| calc_on_fills | PyneCore 6.9.1 (full feed) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| calc_on_fills | PyneCore 6.9.1 (range-start feed) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| calc_on_fills | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| calc_on_fills | PyneCore 6.4.6 (full feed) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| calc_on_fills | PyneCore 6.4.6 (range-start feed) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| pooc | PineForge - BEST SUPPORTED CONFIGURATION | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 4 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 75.0 | 100.0 |
| pooc | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 4 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 75.0 | 100.0 |
| pooc | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PineForge (full feed, tape-window) | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PineForge (range-start feed) | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PineForge (full feed, raw) | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PineForge (+ campaign 1m auxiliary feed) | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PineForge (+ campaign 1m auxiliary feed, range-start bound) | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PyneCore 6.9.1 (full feed, --security supplied) | 4 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 75.0 | 100.0 |
| pooc | PyneCore 6.9.1 (full feed) | 4 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 75.0 | 100.0 |
| pooc | PyneCore 6.9.1 (range-start feed) | 4 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 75.0 | 100.0 |
| pooc | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 4 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 75.0 | 100.0 |
| pooc | PyneCore 6.4.6 (full feed) | 4 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 75.0 | 100.0 |
| pooc | PyneCore 6.4.6 (range-start feed) | 4 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 75.0 | 100.0 |
| margin_lt100 | PineForge - BEST SUPPORTED CONFIGURATION | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| margin_lt100 | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| margin_lt100 | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| margin_lt100 | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| margin_lt100 | PineForge (full feed, tape-window) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| margin_lt100 | PineForge (range-start feed) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| margin_lt100 | PineForge (full feed, raw) | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0.0 | 0.0 |
| margin_lt100 | PineForge (+ campaign 1m auxiliary feed) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| margin_lt100 | PineForge (+ campaign 1m auxiliary feed, range-start bound) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| margin_lt100 | PyneCore 6.9.1 (full feed, --security supplied) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| margin_lt100 | PyneCore 6.9.1 (full feed) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| margin_lt100 | PyneCore 6.9.1 (range-start feed) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| margin_lt100 | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| margin_lt100 | PyneCore 6.4.6 (full feed) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| margin_lt100 | PyneCore 6.4.6 (range-start feed) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| security | PineForge - BEST SUPPORTED CONFIGURATION | 22 | 22 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| security | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 22 | 12 | 2 | 0 | 5 | 0 | 3 | 0 | 54.5 | 63.6 |
| security | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 22 | 0 | 0 | 0 | 0 | 0 | 22 | 0 | 0.0 | 0.0 |
| security | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 22 | 22 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| security | PineForge (full feed, tape-window) | 22 | 22 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| security | PineForge (range-start feed) | 22 | 21 | 1 | 0 | 0 | 0 | 0 | 0 | 95.5 | 100.0 |
| security | PineForge (full feed, raw) | 22 | 18 | 3 | 1 | 0 | 0 | 0 | 0 | 81.8 | 95.5 |
| security | PineForge (+ campaign 1m auxiliary feed) | 22 | 20 | 0 | 0 | 0 | 0 | 2 | 0 | 90.9 | 90.9 |
| security | PineForge (+ campaign 1m auxiliary feed, range-start bound) | 22 | 19 | 1 | 0 | 0 | 0 | 2 | 0 | 86.4 | 90.9 |
| security | PyneCore 6.9.1 (full feed, --security supplied) | 22 | 2 | 0 | 0 | 5 | 0 | 15 | 0 | 9.1 | 9.1 |
| security | PyneCore 6.9.1 (full feed) | 22 | 2 | 0 | 0 | 0 | 0 | 20 | 0 | 9.1 | 9.1 |
| security | PyneCore 6.9.1 (range-start feed) | 22 | 10 | 2 | 0 | 0 | 0 | 10 | 0 | 45.5 | 54.5 |
| security | PyneCore 6.9.1 (+ campaign 1m feed via --security) | 22 | 2 | 0 | 0 | 0 | 0 | 0 | 20 | 9.1 | 9.1 |
| security | PyneCore 6.9.1 (+ campaign 1m feed via --security, range-start feed) | 22 | 1 | 1 | 0 | 0 | 0 | 0 | 20 | 4.5 | 9.1 |
| security | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 22 | 3 | 0 | 0 | 5 | 0 | 14 | 0 | 13.6 | 13.6 |
| security | PyneCore 6.4.6 (full feed) | 22 | 0 | 0 | 0 | 0 | 0 | 22 | 0 | 0.0 | 0.0 |
| security | PyneCore 6.4.6 (range-start feed) | 22 | 0 | 0 | 0 | 0 | 0 | 22 | 0 | 0.0 | 0.0 |
| magnifier | PineForge - BEST SUPPORTED CONFIGURATION | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PineForge (full feed, tape-window) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PineForge (range-start feed) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PineForge (full feed, raw) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PineForge (+ campaign 1m auxiliary feed) | 5 | 1 | 0 | 0 | 0 | 0 | 4 | 0 | 20.0 | 20.0 |
| magnifier | PineForge (+ campaign 1m auxiliary feed, range-start bound) | 5 | 1 | 0 | 0 | 0 | 0 | 4 | 0 | 20.0 | 20.0 |
| magnifier | PyneCore 6.9.1 (full feed, --security supplied) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PyneCore 6.9.1 (full feed) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PyneCore 6.9.1 (range-start feed) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PyneCore 6.4.6 (full feed) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PyneCore 6.4.6 (range-start feed) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| var_state | PineForge - BEST SUPPORTED CONFIGURATION | 82 | 82 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| var_state | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 82 | 74 | 6 | 0 | 2 | 0 | 0 | 0 | 90.2 | 97.6 |
| var_state | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 82 | 63 | 6 | 0 | 0 | 1 | 12 | 0 | 76.8 | 84.1 |
| var_state | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 82 | 82 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| var_state | PineForge (full feed, tape-window) | 82 | 82 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| var_state | PineForge (range-start feed) | 82 | 71 | 8 | 0 | 0 | 3 | 0 | 0 | 86.6 | 96.3 |
| var_state | PineForge (full feed, raw) | 82 | 71 | 7 | 0 | 1 | 3 | 0 | 0 | 86.6 | 95.1 |
| var_state | PineForge (+ campaign 1m auxiliary feed) | 82 | 81 | 0 | 0 | 0 | 0 | 1 | 0 | 98.8 | 98.8 |
| var_state | PineForge (+ campaign 1m auxiliary feed, range-start bound) | 82 | 70 | 8 | 0 | 0 | 3 | 1 | 0 | 85.4 | 95.1 |
| var_state | PyneCore 6.9.1 (full feed, --security supplied) | 82 | 64 | 12 | 0 | 3 | 0 | 3 | 0 | 78.0 | 92.7 |
| var_state | PyneCore 6.9.1 (full feed) | 82 | 64 | 12 | 0 | 2 | 0 | 4 | 0 | 78.0 | 92.7 |
| var_state | PyneCore 6.9.1 (range-start feed) | 82 | 74 | 6 | 0 | 1 | 0 | 1 | 0 | 90.2 | 97.6 |
| var_state | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 82 | 64 | 12 | 0 | 3 | 0 | 3 | 0 | 78.0 | 92.7 |
| var_state | PyneCore 6.4.6 (full feed) | 82 | 56 | 12 | 0 | 1 | 1 | 12 | 0 | 68.3 | 82.9 |
| var_state | PyneCore 6.4.6 (range-start feed) | 82 | 63 | 6 | 0 | 0 | 1 | 12 | 0 | 76.8 | 84.1 |
| arrays | PineForge - BEST SUPPORTED CONFIGURATION | 22 | 22 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| arrays | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 22 | 19 | 2 | 0 | 1 | 0 | 0 | 0 | 86.4 | 95.5 |
| arrays | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 22 | 17 | 2 | 0 | 0 | 0 | 3 | 0 | 77.3 | 86.4 |
| arrays | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 22 | 22 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| arrays | PineForge (full feed, tape-window) | 22 | 22 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| arrays | PineForge (range-start feed) | 22 | 18 | 4 | 0 | 0 | 0 | 0 | 0 | 81.8 | 100.0 |
| arrays | PineForge (full feed, raw) | 22 | 17 | 5 | 0 | 0 | 0 | 0 | 0 | 77.3 | 100.0 |
| arrays | PineForge (+ campaign 1m auxiliary feed) | 22 | 20 | 0 | 0 | 0 | 0 | 2 | 0 | 90.9 | 90.9 |
| arrays | PineForge (+ campaign 1m auxiliary feed, range-start bound) | 22 | 16 | 4 | 0 | 0 | 0 | 2 | 0 | 72.7 | 90.9 |
| arrays | PyneCore 6.9.1 (full feed, --security supplied) | 22 | 9 | 10 | 0 | 1 | 0 | 2 | 0 | 40.9 | 86.4 |
| arrays | PyneCore 6.9.1 (full feed) | 22 | 9 | 10 | 0 | 0 | 0 | 3 | 0 | 40.9 | 86.4 |
| arrays | PyneCore 6.9.1 (range-start feed) | 22 | 16 | 3 | 0 | 0 | 0 | 3 | 0 | 72.7 | 86.4 |
| arrays | PyneCore 6.9.1 (+ campaign 1m feed via --security) | 22 | 2 | 0 | 0 | 0 | 0 | 0 | 20 | 9.1 | 9.1 |
| arrays | PyneCore 6.9.1 (+ campaign 1m feed via --security, range-start feed) | 22 | 1 | 1 | 0 | 0 | 0 | 0 | 20 | 4.5 | 9.1 |
| arrays | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 22 | 11 | 10 | 0 | 1 | 0 | 0 | 0 | 50.0 | 95.5 |
| arrays | PyneCore 6.4.6 (full feed) | 22 | 9 | 10 | 0 | 0 | 0 | 3 | 0 | 40.9 | 86.4 |
| arrays | PyneCore 6.4.6 (range-start feed) | 22 | 16 | 3 | 0 | 0 | 0 | 3 | 0 | 72.7 | 86.4 |
| udt | PineForge - BEST SUPPORTED CONFIGURATION | 29 | 29 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| udt | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 29 | 28 | 1 | 0 | 0 | 0 | 0 | 0 | 96.6 | 100.0 |
| udt | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 29 | 23 | 0 | 0 | 0 | 0 | 6 | 0 | 79.3 | 79.3 |
| udt | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 29 | 29 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| udt | PineForge (full feed, tape-window) | 29 | 29 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| udt | PineForge (range-start feed) | 29 | 24 | 2 | 0 | 0 | 3 | 0 | 0 | 82.8 | 89.7 |
| udt | PineForge (full feed, raw) | 29 | 24 | 2 | 0 | 0 | 3 | 0 | 0 | 82.8 | 89.7 |
| udt | PineForge (+ campaign 1m auxiliary feed) | 29 | 29 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| udt | PineForge (+ campaign 1m auxiliary feed, range-start bound) | 29 | 24 | 2 | 0 | 0 | 3 | 0 | 0 | 82.8 | 89.7 |
| udt | PyneCore 6.9.1 (full feed, --security supplied) | 29 | 26 | 3 | 0 | 0 | 0 | 0 | 0 | 89.7 | 100.0 |
| udt | PyneCore 6.9.1 (full feed) | 29 | 26 | 3 | 0 | 0 | 0 | 0 | 0 | 89.7 | 100.0 |
| udt | PyneCore 6.9.1 (range-start feed) | 29 | 28 | 1 | 0 | 0 | 0 | 0 | 0 | 96.6 | 100.0 |
| udt | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 29 | 26 | 3 | 0 | 0 | 0 | 0 | 0 | 89.7 | 100.0 |
| udt | PyneCore 6.4.6 (full feed) | 29 | 21 | 2 | 0 | 0 | 0 | 6 | 0 | 72.4 | 79.3 |
| udt | PyneCore 6.4.6 (range-start feed) | 29 | 23 | 0 | 0 | 0 | 0 | 6 | 0 | 79.3 | 79.3 |


### Feature buckets — set C (a script counts in every feature it uses)

| bucket | engine | n | excellent | strong | moderate | weak | minimal | fail | not_run | excellentPct | excellentStrongPct |
|---|---|---|---|---|---|---|---|---|---|---|---|
| trail | PineForge - BEST SUPPORTED CONFIGURATION | 10 | 9 | 1 | 0 | 0 | 0 | 0 | 0 | 90.0 | 100.0 |
| trail | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 10 | 3 | 1 | 1 | 5 | 0 | 0 | 0 | 30.0 | 40.0 |
| trail | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 10 | 1 | 0 | 3 | 1 | 0 | 5 | 0 | 10.0 | 10.0 |
| trail | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 10 | 9 | 1 | 0 | 0 | 0 | 0 | 0 | 90.0 | 100.0 |
| trail | PineForge (full feed, tape-window) | 10 | 9 | 1 | 0 | 0 | 0 | 0 | 0 | 90.0 | 100.0 |
| trail | PineForge (range-start feed) | 10 | 9 | 1 | 0 | 0 | 0 | 0 | 0 | 90.0 | 100.0 |
| trail | PineForge (full feed, raw) | 10 | 6 | 1 | 3 | 0 | 0 | 0 | 0 | 60.0 | 70.0 |
| trail | PineForge (+ campaign 1m auxiliary feed) | 10 | 7 | 1 | 0 | 0 | 0 | 2 | 0 | 70.0 | 80.0 |
| trail | PineForge (+ campaign 1m auxiliary feed, range-start bound) | 10 | 9 | 1 | 0 | 0 | 0 | 0 | 0 | 90.0 | 100.0 |
| trail | PyneCore 6.9.1 (full feed, --security supplied) | 10 | 3 | 1 | 1 | 5 | 0 | 0 | 0 | 30.0 | 40.0 |
| trail | PyneCore 6.9.1 (full feed) | 10 | 3 | 1 | 1 | 4 | 0 | 1 | 0 | 30.0 | 40.0 |
| trail | PyneCore 6.9.1 (range-start feed) | 10 | 3 | 1 | 1 | 4 | 0 | 1 | 0 | 30.0 | 40.0 |
| trail | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 10 | 2 | 2 | 1 | 5 | 0 | 0 | 0 | 20.0 | 40.0 |
| trail | PyneCore 6.9.1 (+ the campaign's native TradingView daily feed under SYMBOL:D/1D) | 10 | 0 | 1 | 0 | 2 | 0 | 0 | 7 | 0.0 | 10.0 |
| trail | PyneCore 6.4.6 (full feed) | 10 | 1 | 0 | 2 | 1 | 1 | 5 | 0 | 10.0 | 10.0 |
| trail | PyneCore 6.4.6 (range-start feed) | 10 | 1 | 0 | 3 | 1 | 0 | 5 | 0 | 10.0 | 10.0 |
| brackets | PineForge - BEST SUPPORTED CONFIGURATION | 74 | 73 | 1 | 0 | 0 | 0 | 0 | 0 | 98.6 | 100.0 |
| brackets | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 74 | 44 | 17 | 5 | 5 | 2 | 1 | 0 | 59.5 | 82.4 |
| brackets | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 74 | 21 | 14 | 11 | 3 | 6 | 19 | 0 | 28.4 | 47.3 |
| brackets | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 74 | 73 | 1 | 0 | 0 | 0 | 0 | 0 | 98.6 | 100.0 |
| brackets | PineForge (full feed, tape-window) | 74 | 49 | 15 | 3 | 2 | 2 | 3 | 0 | 66.2 | 86.5 |
| brackets | PineForge (range-start feed) | 74 | 56 | 9 | 2 | 2 | 2 | 3 | 0 | 75.7 | 87.8 |
| brackets | PineForge (full feed, raw) | 74 | 39 | 23 | 5 | 2 | 2 | 3 | 0 | 52.7 | 83.8 |
| brackets | PineForge (+ campaign 1m auxiliary feed) | 74 | 36 | 15 | 3 | 1 | 1 | 18 | 0 | 48.6 | 68.9 |
| brackets | PineForge (+ campaign 1m auxiliary feed, range-start bound) | 74 | 59 | 9 | 2 | 2 | 2 | 0 | 0 | 79.7 | 91.9 |
| brackets | PyneCore 6.9.1 (full feed, --security supplied) | 74 | 28 | 26 | 7 | 4 | 3 | 6 | 0 | 37.8 | 73.0 |
| brackets | PyneCore 6.9.1 (full feed) | 74 | 28 | 26 | 7 | 1 | 2 | 10 | 0 | 37.8 | 73.0 |
| brackets | PyneCore 6.9.1 (range-start feed) | 74 | 42 | 15 | 4 | 3 | 1 | 9 | 0 | 56.8 | 77.0 |
| brackets | PyneCore 6.9.1 (+ campaign 1m feed via --security) | 74 | 1 | 0 | 0 | 1 | 1 | 0 | 71 | 1.4 | 1.4 |
| brackets | PyneCore 6.9.1 (+ campaign 1m feed via --security, range-start feed) | 74 | 1 | 2 | 0 | 0 | 0 | 0 | 71 | 1.4 | 4.1 |
| brackets | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 74 | 40 | 19 | 5 | 6 | 2 | 2 | 0 | 54.1 | 79.7 |
| brackets | PyneCore 6.9.1 (+ the campaign's native TradingView daily feed under SYMBOL:D/1D) | 74 | 14 | 4 | 2 | 2 | 1 | 0 | 51 | 18.9 | 24.3 |
| brackets | PyneCore 6.4.6 (full feed) | 74 | 14 | 16 | 13 | 3 | 9 | 19 | 0 | 18.9 | 40.5 |
| brackets | PyneCore 6.4.6 (range-start feed) | 74 | 21 | 13 | 12 | 3 | 6 | 19 | 0 | 28.4 | 45.9 |
| partial | PineForge - BEST SUPPORTED CONFIGURATION | 15 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| partial | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 15 | 5 | 3 | 3 | 4 | 0 | 0 | 0 | 33.3 | 53.3 |
| partial | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 15 | 4 | 2 | 0 | 1 | 1 | 7 | 0 | 26.7 | 40.0 |
| partial | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 15 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| partial | PineForge (full feed, tape-window) | 15 | 9 | 4 | 1 | 0 | 0 | 1 | 0 | 60.0 | 86.7 |
| partial | PineForge (range-start feed) | 15 | 10 | 2 | 2 | 0 | 0 | 1 | 0 | 66.7 | 80.0 |
| partial | PineForge (full feed, raw) | 15 | 6 | 5 | 2 | 0 | 1 | 1 | 0 | 40.0 | 73.3 |
| partial | PineForge (+ campaign 1m auxiliary feed) | 15 | 4 | 5 | 1 | 0 | 0 | 5 | 0 | 26.7 | 60.0 |
| partial | PineForge (+ campaign 1m auxiliary feed, range-start bound) | 15 | 11 | 2 | 2 | 0 | 0 | 0 | 0 | 73.3 | 86.7 |
| partial | PyneCore 6.9.1 (full feed, --security supplied) | 15 | 5 | 1 | 3 | 2 | 2 | 2 | 0 | 33.3 | 40.0 |
| partial | PyneCore 6.9.1 (full feed) | 15 | 5 | 1 | 2 | 0 | 1 | 6 | 0 | 33.3 | 40.0 |
| partial | PyneCore 6.9.1 (range-start feed) | 15 | 5 | 2 | 1 | 1 | 0 | 6 | 0 | 33.3 | 46.7 |
| partial | PyneCore 6.9.1 (+ campaign 1m feed via --security) | 15 | 0 | 0 | 0 | 1 | 0 | 0 | 14 | 0.0 | 0.0 |
| partial | PyneCore 6.9.1 (+ campaign 1m feed via --security, range-start feed) | 15 | 0 | 1 | 0 | 0 | 0 | 0 | 14 | 0.0 | 6.7 |
| partial | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 15 | 5 | 2 | 3 | 5 | 0 | 0 | 0 | 33.3 | 46.7 |
| partial | PyneCore 6.9.1 (+ the campaign's native TradingView daily feed under SYMBOL:D/1D) | 15 | 3 | 0 | 1 | 0 | 0 | 0 | 11 | 20.0 | 20.0 |
| partial | PyneCore 6.4.6 (full feed) | 15 | 4 | 0 | 1 | 1 | 2 | 7 | 0 | 26.7 | 26.7 |
| partial | PyneCore 6.4.6 (range-start feed) | 15 | 4 | 2 | 0 | 1 | 1 | 7 | 0 | 26.7 | 40.0 |
| pyramiding | PineForge - BEST SUPPORTED CONFIGURATION | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pyramiding | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 10 | 3 | 1 | 0 | 1 | 1 | 4 | 0 | 30.0 | 40.0 |
| pyramiding | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 10 | 1 | 0 | 1 | 0 | 1 | 7 | 0 | 10.0 | 10.0 |
| pyramiding | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pyramiding | PineForge (full feed, tape-window) | 10 | 2 | 0 | 0 | 1 | 1 | 6 | 0 | 20.0 | 20.0 |
| pyramiding | PineForge (range-start feed) | 10 | 4 | 0 | 0 | 0 | 0 | 6 | 0 | 40.0 | 40.0 |
| pyramiding | PineForge (full feed, raw) | 10 | 3 | 0 | 0 | 0 | 1 | 6 | 0 | 30.0 | 30.0 |
| pyramiding | PineForge (+ campaign 1m auxiliary feed) | 10 | 8 | 0 | 0 | 1 | 1 | 0 | 0 | 80.0 | 80.0 |
| pyramiding | PineForge (+ campaign 1m auxiliary feed, range-start bound) | 10 | 9 | 0 | 0 | 1 | 0 | 0 | 0 | 90.0 | 90.0 |
| pyramiding | PyneCore 6.9.1 (full feed, --security supplied) | 10 | 2 | 1 | 0 | 0 | 1 | 6 | 0 | 20.0 | 30.0 |
| pyramiding | PyneCore 6.9.1 (full feed) | 10 | 2 | 1 | 0 | 0 | 1 | 6 | 0 | 20.0 | 30.0 |
| pyramiding | PyneCore 6.9.1 (range-start feed) | 10 | 2 | 1 | 0 | 0 | 1 | 6 | 0 | 20.0 | 30.0 |
| pyramiding | PyneCore 6.9.1 (+ campaign 1m feed via --security) | 10 | 1 | 0 | 0 | 1 | 0 | 4 | 4 | 10.0 | 10.0 |
| pyramiding | PyneCore 6.9.1 (+ campaign 1m feed via --security, range-start feed) | 10 | 1 | 0 | 0 | 1 | 0 | 4 | 4 | 10.0 | 10.0 |
| pyramiding | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 10 | 3 | 1 | 0 | 1 | 1 | 4 | 0 | 30.0 | 40.0 |
| pyramiding | PyneCore 6.9.1 (+ the campaign's native TradingView daily feed under SYMBOL:D/1D) | 10 | 1 | 0 | 0 | 0 | 0 | 0 | 9 | 10.0 | 10.0 |
| pyramiding | PyneCore 6.4.6 (full feed) | 10 | 1 | 0 | 1 | 0 | 1 | 7 | 0 | 10.0 | 10.0 |
| pyramiding | PyneCore 6.4.6 (range-start feed) | 10 | 1 | 0 | 1 | 0 | 1 | 7 | 0 | 10.0 | 10.0 |
| calc_on_fills | PineForge - BEST SUPPORTED CONFIGURATION | 5 | 4 | 1 | 0 | 0 | 0 | 0 | 0 | 80.0 | 100.0 |
| calc_on_fills | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 5 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 20.0 | 100.0 |
| calc_on_fills | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 5 | 0 | 1 | 0 | 0 | 4 | 0 | 0 | 0.0 | 20.0 |
| calc_on_fills | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 5 | 4 | 1 | 0 | 0 | 0 | 0 | 0 | 80.0 | 100.0 |
| calc_on_fills | PineForge (full feed, tape-window) | 5 | 2 | 1 | 0 | 0 | 2 | 0 | 0 | 40.0 | 60.0 |
| calc_on_fills | PineForge (range-start feed) | 5 | 2 | 1 | 0 | 0 | 2 | 0 | 0 | 40.0 | 60.0 |
| calc_on_fills | PineForge (full feed, raw) | 5 | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 60.0 | 100.0 |
| calc_on_fills | PineForge (+ campaign 1m auxiliary feed) | 5 | 2 | 1 | 0 | 0 | 1 | 1 | 0 | 40.0 | 60.0 |
| calc_on_fills | PineForge (+ campaign 1m auxiliary feed, range-start bound) | 5 | 2 | 1 | 0 | 0 | 2 | 0 | 0 | 40.0 | 60.0 |
| calc_on_fills | PyneCore 6.9.1 (full feed, --security supplied) | 5 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 20.0 | 100.0 |
| calc_on_fills | PyneCore 6.9.1 (full feed) | 5 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 20.0 | 100.0 |
| calc_on_fills | PyneCore 6.9.1 (range-start feed) | 5 | 1 | 3 | 0 | 1 | 0 | 0 | 0 | 20.0 | 80.0 |
| calc_on_fills | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 5 | 1 | 3 | 0 | 1 | 0 | 0 | 0 | 20.0 | 80.0 |
| calc_on_fills | PyneCore 6.9.1 (+ the campaign's native TradingView daily feed under SYMBOL:D/1D) | 5 | 0 | 0 | 0 | 1 | 0 | 0 | 4 | 0.0 | 0.0 |
| calc_on_fills | PyneCore 6.4.6 (full feed) | 5 | 0 | 1 | 0 | 0 | 4 | 0 | 0 | 0.0 | 20.0 |
| calc_on_fills | PyneCore 6.4.6 (range-start feed) | 5 | 0 | 0 | 1 | 0 | 4 | 0 | 0 | 0.0 | 0.0 |
| pooc | PineForge - BEST SUPPORTED CONFIGURATION | 31 | 30 | 1 | 0 | 0 | 0 | 0 | 0 | 96.8 | 100.0 |
| pooc | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 31 | 9 | 6 | 2 | 9 | 0 | 5 | 0 | 29.0 | 48.4 |
| pooc | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 31 | 3 | 5 | 0 | 1 | 2 | 20 | 0 | 9.7 | 25.8 |
| pooc | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 31 | 30 | 1 | 0 | 0 | 0 | 0 | 0 | 96.8 | 100.0 |
| pooc | PineForge (full feed, tape-window) | 31 | 18 | 5 | 0 | 0 | 1 | 7 | 0 | 58.1 | 74.2 |
| pooc | PineForge (range-start feed) | 31 | 19 | 4 | 1 | 0 | 0 | 7 | 0 | 61.3 | 74.2 |
| pooc | PineForge (full feed, raw) | 31 | 5 | 15 | 3 | 0 | 1 | 7 | 0 | 16.1 | 64.5 |
| pooc | PineForge (+ campaign 1m auxiliary feed) | 31 | 19 | 6 | 0 | 0 | 1 | 5 | 0 | 61.3 | 80.6 |
| pooc | PineForge (+ campaign 1m auxiliary feed, range-start bound) | 31 | 25 | 4 | 1 | 1 | 0 | 0 | 0 | 80.6 | 93.5 |
| pooc | PyneCore 6.9.1 (full feed, --security supplied) | 31 | 4 | 8 | 1 | 6 | 2 | 10 | 0 | 12.9 | 38.7 |
| pooc | PyneCore 6.9.1 (full feed) | 31 | 4 | 8 | 0 | 5 | 1 | 13 | 0 | 12.9 | 38.7 |
| pooc | PyneCore 6.9.1 (range-start feed) | 31 | 8 | 5 | 0 | 6 | 0 | 12 | 0 | 25.8 | 41.9 |
| pooc | PyneCore 6.9.1 (+ campaign 1m feed via --security) | 31 | 1 | 0 | 0 | 2 | 0 | 4 | 24 | 3.2 | 3.2 |
| pooc | PyneCore 6.9.1 (+ campaign 1m feed via --security, range-start feed) | 31 | 1 | 1 | 0 | 1 | 0 | 4 | 24 | 3.2 | 6.5 |
| pooc | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 31 | 9 | 6 | 1 | 9 | 0 | 6 | 0 | 29.0 | 48.4 |
| pooc | PyneCore 6.9.1 (+ the campaign's native TradingView daily feed under SYMBOL:D/1D) | 31 | 4 | 1 | 1 | 2 | 0 | 0 | 23 | 12.9 | 16.1 |
| pooc | PyneCore 6.4.6 (full feed) | 31 | 1 | 5 | 0 | 2 | 3 | 20 | 0 | 3.2 | 19.4 |
| pooc | PyneCore 6.4.6 (range-start feed) | 31 | 3 | 4 | 1 | 1 | 2 | 20 | 0 | 9.7 | 22.6 |
| margin_lt100 | PineForge - BEST SUPPORTED CONFIGURATION | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| margin_lt100 | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 5 | 3 | 0 | 0 | 0 | 2 | 0 | 0 | 60.0 | 60.0 |
| margin_lt100 | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 5 | 0 | 1 | 0 | 1 | 1 | 2 | 0 | 0.0 | 20.0 |
| margin_lt100 | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| margin_lt100 | PineForge (full feed, tape-window) | 5 | 3 | 0 | 0 | 2 | 0 | 0 | 0 | 60.0 | 60.0 |
| margin_lt100 | PineForge (range-start feed) | 5 | 4 | 0 | 0 | 1 | 0 | 0 | 0 | 80.0 | 80.0 |
| margin_lt100 | PineForge (full feed, raw) | 5 | 3 | 0 | 0 | 1 | 1 | 0 | 0 | 60.0 | 60.0 |
| margin_lt100 | PineForge (+ campaign 1m auxiliary feed) | 5 | 2 | 0 | 0 | 1 | 0 | 2 | 0 | 40.0 | 40.0 |
| margin_lt100 | PineForge (+ campaign 1m auxiliary feed, range-start bound) | 5 | 4 | 0 | 0 | 1 | 0 | 0 | 0 | 80.0 | 80.0 |
| margin_lt100 | PyneCore 6.9.1 (full feed, --security supplied) | 5 | 3 | 0 | 0 | 0 | 2 | 0 | 0 | 60.0 | 60.0 |
| margin_lt100 | PyneCore 6.9.1 (full feed) | 5 | 3 | 0 | 0 | 0 | 1 | 1 | 0 | 60.0 | 60.0 |
| margin_lt100 | PyneCore 6.9.1 (range-start feed) | 5 | 3 | 0 | 0 | 0 | 1 | 1 | 0 | 60.0 | 60.0 |
| margin_lt100 | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 5 | 3 | 0 | 0 | 0 | 2 | 0 | 0 | 60.0 | 60.0 |
| margin_lt100 | PyneCore 6.9.1 (+ the campaign's native TradingView daily feed under SYMBOL:D/1D) | 5 | 1 | 0 | 0 | 0 | 1 | 0 | 3 | 20.0 | 20.0 |
| margin_lt100 | PyneCore 6.4.6 (full feed) | 5 | 0 | 1 | 0 | 1 | 1 | 2 | 0 | 0.0 | 20.0 |
| margin_lt100 | PyneCore 6.4.6 (range-start feed) | 5 | 0 | 0 | 1 | 1 | 1 | 2 | 0 | 0.0 | 0.0 |
| security | PineForge - BEST SUPPORTED CONFIGURATION | 48 | 48 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| security | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 48 | 14 | 10 | 3 | 10 | 3 | 8 | 0 | 29.2 | 50.0 |
| security | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 48 | 3 | 0 | 1 | 0 | 1 | 43 | 0 | 6.2 | 6.2 |
| security | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 48 | 48 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| security | PineForge (full feed, tape-window) | 48 | 21 | 9 | 2 | 1 | 2 | 13 | 0 | 43.8 | 62.5 |
| security | PineForge (range-start feed) | 48 | 26 | 6 | 2 | 1 | 0 | 13 | 0 | 54.2 | 66.7 |
| security | PineForge (full feed, raw) | 48 | 12 | 15 | 4 | 1 | 3 | 13 | 0 | 25.0 | 56.2 |
| security | PineForge (+ campaign 1m auxiliary feed) | 48 | 23 | 9 | 1 | 1 | 2 | 12 | 0 | 47.9 | 66.7 |
| security | PineForge (+ campaign 1m auxiliary feed, range-start bound) | 48 | 38 | 6 | 2 | 2 | 0 | 0 | 0 | 79.2 | 91.7 |
| security | PyneCore 6.9.1 (full feed, --security supplied) | 48 | 4 | 10 | 3 | 6 | 4 | 21 | 0 | 8.3 | 29.2 |
| security | PyneCore 6.9.1 (full feed) | 48 | 3 | 8 | 2 | 2 | 1 | 32 | 0 | 6.2 | 22.9 |
| security | PyneCore 6.9.1 (range-start feed) | 48 | 8 | 6 | 1 | 4 | 0 | 29 | 0 | 16.7 | 29.2 |
| security | PyneCore 6.9.1 (+ campaign 1m feed via --security) | 48 | 2 | 0 | 2 | 2 | 2 | 5 | 35 | 4.2 | 4.2 |
| security | PyneCore 6.9.1 (+ campaign 1m feed via --security, range-start feed) | 48 | 4 | 2 | 0 | 1 | 1 | 5 | 35 | 8.3 | 12.5 |
| security | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 48 | 13 | 10 | 2 | 10 | 3 | 10 | 0 | 27.1 | 47.9 |
| security | PyneCore 6.9.1 (+ the campaign's native TradingView daily feed under SYMBOL:D/1D) | 48 | 5 | 3 | 2 | 3 | 2 | 0 | 33 | 10.4 | 16.7 |
| security | PyneCore 6.4.6 (full feed) | 48 | 1 | 2 | 1 | 0 | 1 | 43 | 0 | 2.1 | 6.2 |
| security | PyneCore 6.4.6 (range-start feed) | 48 | 3 | 0 | 1 | 0 | 1 | 43 | 0 | 6.2 | 6.2 |
| var_state | PineForge - BEST SUPPORTED CONFIGURATION | 134 | 134 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| var_state | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 134 | 60 | 34 | 12 | 15 | 5 | 8 | 0 | 44.8 | 70.1 |
| var_state | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 134 | 26 | 31 | 16 | 4 | 9 | 48 | 0 | 19.4 | 42.5 |
| var_state | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 134 | 134 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| var_state | PineForge (full feed, tape-window) | 134 | 88 | 21 | 5 | 3 | 6 | 11 | 0 | 65.7 | 81.3 |
| var_state | PineForge (range-start feed) | 134 | 99 | 14 | 4 | 3 | 3 | 11 | 0 | 73.9 | 84.3 |
| var_state | PineForge (full feed, raw) | 134 | 54 | 42 | 15 | 3 | 9 | 11 | 0 | 40.3 | 71.6 |
| var_state | PineForge (+ campaign 1m auxiliary feed) | 134 | 72 | 19 | 3 | 3 | 3 | 34 | 0 | 53.7 | 67.9 |
| var_state | PineForge (+ campaign 1m auxiliary feed, range-start bound) | 134 | 109 | 14 | 4 | 4 | 3 | 0 | 0 | 81.3 | 91.8 |
| var_state | PyneCore 6.9.1 (full feed, --security supplied) | 134 | 32 | 43 | 16 | 14 | 10 | 19 | 0 | 23.9 | 56.0 |
| var_state | PyneCore 6.9.1 (full feed) | 134 | 31 | 42 | 15 | 10 | 7 | 29 | 0 | 23.1 | 54.5 |
| var_state | PyneCore 6.9.1 (range-start feed) | 134 | 55 | 31 | 10 | 10 | 2 | 26 | 0 | 41.0 | 64.2 |
| var_state | PyneCore 6.9.1 (+ campaign 1m feed via --security) | 134 | 2 | 0 | 0 | 2 | 2 | 5 | 123 | 1.5 | 1.5 |
| var_state | PyneCore 6.9.1 (+ campaign 1m feed via --security, range-start feed) | 134 | 2 | 2 | 0 | 1 | 1 | 5 | 123 | 1.5 | 3.0 |
| var_state | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 134 | 54 | 36 | 13 | 16 | 5 | 10 | 0 | 40.3 | 67.2 |
| var_state | PyneCore 6.9.1 (+ the campaign's native TradingView daily feed under SYMBOL:D/1D) | 134 | 20 | 6 | 2 | 7 | 2 | 0 | 97 | 14.9 | 19.4 |
| var_state | PyneCore 6.4.6 (full feed) | 134 | 20 | 28 | 16 | 7 | 15 | 48 | 0 | 14.9 | 35.8 |
| var_state | PyneCore 6.4.6 (range-start feed) | 134 | 26 | 30 | 17 | 4 | 9 | 48 | 0 | 19.4 | 41.8 |
| arrays | PineForge - BEST SUPPORTED CONFIGURATION | 24 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| arrays | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 24 | 7 | 6 | 4 | 1 | 2 | 4 | 0 | 29.2 | 54.2 |
| arrays | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 24 | 5 | 1 | 3 | 0 | 1 | 14 | 0 | 20.8 | 25.0 |
| arrays | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 24 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| arrays | PineForge (full feed, tape-window) | 24 | 8 | 5 | 0 | 1 | 1 | 9 | 0 | 33.3 | 54.2 |
| arrays | PineForge (range-start feed) | 24 | 12 | 2 | 1 | 0 | 0 | 9 | 0 | 50.0 | 58.3 |
| arrays | PineForge (full feed, raw) | 24 | 5 | 6 | 0 | 1 | 3 | 9 | 0 | 20.8 | 45.8 |
| arrays | PineForge (+ campaign 1m auxiliary feed) | 24 | 12 | 4 | 0 | 1 | 1 | 6 | 0 | 50.0 | 66.7 |
| arrays | PineForge (+ campaign 1m auxiliary feed, range-start bound) | 24 | 21 | 2 | 1 | 0 | 0 | 0 | 0 | 87.5 | 95.8 |
| arrays | PyneCore 6.9.1 (full feed, --security supplied) | 24 | 2 | 7 | 1 | 1 | 2 | 11 | 0 | 8.3 | 37.5 |
| arrays | PyneCore 6.9.1 (full feed) | 24 | 2 | 7 | 1 | 1 | 2 | 11 | 0 | 8.3 | 37.5 |
| arrays | PyneCore 6.9.1 (range-start feed) | 24 | 5 | 4 | 3 | 0 | 1 | 11 | 0 | 20.8 | 37.5 |
| arrays | PyneCore 6.9.1 (+ campaign 1m feed via --security) | 24 | 1 | 0 | 0 | 2 | 2 | 4 | 15 | 4.2 | 4.2 |
| arrays | PyneCore 6.9.1 (+ campaign 1m feed via --security, range-start feed) | 24 | 1 | 2 | 0 | 1 | 1 | 4 | 15 | 4.2 | 12.5 |
| arrays | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 24 | 7 | 6 | 3 | 2 | 2 | 4 | 0 | 29.2 | 54.2 |
| arrays | PyneCore 6.9.1 (+ the campaign's native TradingView daily feed under SYMBOL:D/1D) | 24 | 2 | 3 | 2 | 0 | 0 | 0 | 17 | 8.3 | 20.8 |
| arrays | PyneCore 6.4.6 (full feed) | 24 | 3 | 3 | 1 | 1 | 2 | 14 | 0 | 12.5 | 25.0 |
| arrays | PyneCore 6.4.6 (range-start feed) | 24 | 5 | 1 | 3 | 0 | 1 | 14 | 0 | 20.8 | 25.0 |
| udt | PineForge - BEST SUPPORTED CONFIGURATION | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| udt | PyneCore 6.9.1 - BEST SUPPORTED CONFIGURATION | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| udt | PyneCore 6.4.6 - BEST SUPPORTED CONFIGURATION | 2 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 50.0 | 50.0 |
| udt | PineForge (the campaign's own verifier: verify-engine-local.py ladder) | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| udt | PineForge (full feed, tape-window) | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| udt | PineForge (range-start feed) | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| udt | PineForge (full feed, raw) | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 50.0 | 100.0 |
| udt | PineForge (+ campaign 1m auxiliary feed) | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| udt | PineForge (+ campaign 1m auxiliary feed, range-start bound) | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| udt | PyneCore 6.9.1 (full feed, --security supplied) | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 50.0 | 100.0 |
| udt | PyneCore 6.9.1 (full feed) | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 50.0 | 100.0 |
| udt | PyneCore 6.9.1 (range-start feed) | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| udt | PyneCore 6.9.1 (--security + the probe's --from/--to window) | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| udt | PyneCore 6.9.1 (+ the campaign's native TradingView daily feed under SYMBOL:D/1D) | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 50.0 | 50.0 |
| udt | PyneCore 6.4.6 (full feed) | 2 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 50.0 | 50.0 |
| udt | PyneCore 6.4.6 (range-start feed) | 2 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 50.0 | 50.0 |

