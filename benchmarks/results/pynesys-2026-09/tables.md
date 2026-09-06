## Set A: public benchmark suite (100, ETHUSDT 15m, 53,929 bars)

| engine | n | excellent | strong | moderate | weak | minimal | compile_fail | build_fail | run_error | timeout | not_run | tvTrades | engineTrades | matchedPct | countDelta_median | countDelta_p90 | entryP90_median | entryP90_p90 | exitP90_median | exitP90_p90 | pnlP90_median | pnlP90_p90 | netProfitRelErr_median | netProfitRelErr_p90 | maxEquityDev_median | wall_median_s | wall_p95_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PineForge (full feed, tape-window) | 100 | 89 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 167301 | 166022 | 99.93 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0795% | 0.0930% | 0.0975% | 2.0523% | 0.0689% | 0.430 | 2.478 |
| PineForge (full feed, raw) | 100 | 84 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 167301 | 245503 | 99.92 | 0.0000% | 0.0339% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0798% | 0.0968% | 0.5586% | 18.6848% | 0.3071% | 0.425 | 1.025 |
| PyneCore 6.9.1 (full feed) | 100 | 81 | 18 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 167301 | 245417 | 99.64 | 0.0000% | 0.0351% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0798% | 0.1016% | 0.5687% | 18.6848% | 0.3223% | 1.955 | 5.012 |
| PyneCore 6.4.6 (full feed) | 100 | 69 | 18 | 10 | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 167301 | 242657 | 99.11 | 0.0000% | 0.1456% | 0.0000% | 0.0000% | 0.0000% | 0.4962% | 0.0820% | 348.3379% | 1.0946% | 52.6213% | 0.6040% | 2.721 | 7.858 |


## Set B: public corpus (312, ETHUSDT.P 15m, 222,295 bars)

| engine | n | excellent | strong | moderate | weak | minimal | compile_fail | build_fail | run_error | timeout | not_run | tvTrades | engineTrades | matchedPct | countDelta_median | countDelta_p90 | entryP90_median | entryP90_p90 | exitP90_median | exitP90_p90 | pnlP90_median | pnlP90_p90 | netProfitRelErr_median | netProfitRelErr_p90 | maxEquityDev_median | wall_median_s | wall_p95_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PineForge (full feed, tape-window) | 311 | 311 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 431244 | 429642 | 100.00 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0866% | 0.0000% | 0.704 | 1.149 |
| PineForge (range-start feed) | 311 | 282 | 24 | 0 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 431244 | 426248 | 99.38 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 1.1989% | 0.0000% | 0.396 | 0.699 |
| PineForge (full feed, raw) | 311 | 267 | 34 | 2 | 2 | 6 | 0 | 0 | 0 | 0 | 0 | 431244 | 2286415 | 99.22 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0378% | 11.1367% | 0.0316% | 0.531 | 1.209 |
| PyneCore 6.9.1 (full feed) | 311 | 90 | 31 | 0 | 2 | 1 | 0 | 0 | 10 | 10 | 167 | 431244 | 1016298 | 99.31 | 0.0000% | 0.1532% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 7.1621% | 0.4425% | 13.3149% | 0.2284% | 6.112 | 16.368 |
| PyneCore 6.9.1 (range-start feed) | 311 | 117 | 15 | 0 | 2 | 0 | 0 | 0 | 10 | 0 | 167 | 431244 | 199008 | 99.63 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0065% | 3.9352% | 0.0029% | 1.411 | 116.542 |
| PyneCore 6.4.6 (full feed) | 311 | 57 | 24 | 4 | 2 | 2 | 0 | 0 | 55 | 0 | 167 | 431244 | 679305 | 97.92 | 0.0000% | 0.5472% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 18.2579% | 0.7138% | 18.2405% | 0.4353% | 8.349 | 22.039 |
| PyneCore 6.4.6 (range-start feed) | 311 | 92 | 14 | 7 | 6 | 0 | 0 | 0 | 25 | 0 | 167 | 431244 | 165423 | 98.77 | 0.0000% | 0.0848% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.1534% | 12.1736% | 0.1216% | 1.656 | 3.374 |


## Set C: closed campaign sample (200 script-lane probes, 15 lanes)

| engine | n | excellent | strong | moderate | weak | minimal | compile_fail | build_fail | run_error | timeout | not_run | tvTrades | engineTrades | matchedPct | countDelta_median | countDelta_p90 | entryP90_median | entryP90_p90 | exitP90_median | exitP90_p90 | pnlP90_median | pnlP90_p90 | netProfitRelErr_median | netProfitRelErr_p90 | maxEquityDev_median | wall_median_s | wall_p95_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PineForge (full feed, tape-window) | 200 | 140 | 29 | 8 | 3 | 7 | 0 | 0 | 13 | 0 | 0 | 165223 | 151629 | 98.92 | 0.0000% | 0.5164% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.1178% | 0.0000% | 16.4154% | 0.0000% | 0.344 | 1.524 |
| PineForge (range-start feed) | 200 | 157 | 18 | 5 | 3 | 4 | 0 | 0 | 13 | 0 | 0 | 165223 | 151393 | 98.98 | 0.0000% | 0.0994% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 3.3898% | 0.0000% | 0.253 | 0.605 |
| PineForge (full feed, raw) | 200 | 93 | 59 | 20 | 3 | 12 | 0 | 0 | 13 | 0 | 0 | 165223 | 744013 | 97.16 | 0.0000% | 3.2010% | 0.0000% | 0.0000% | 0.0000% | 0.0049% | 0.0000% | 73.6169% | 1.4433% | 94.5207% | 1.3638% | 0.353 | 1.546 |
| PyneCore 6.9.1 (full feed) | 200 | 67 | 60 | 21 | 10 | 10 | 0 | 0 | 29 | 3 | 0 | 165223 | 707535 | 95.69 | 0.0000% | 5.4496% | 0.0000% | 0.0000% | 0.0000% | 0.0555% | 0.0000% | 100.0000% | 16.2577% | 121.2802% | 8.5821% | 3.092 | 112.913 |
| PyneCore 6.9.1 (range-start feed) | 200 | 107 | 38 | 13 | 10 | 3 | 0 | 0 | 29 | 0 | 0 | 165223 | 146186 | 98.26 | 0.0000% | 0.8386% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 75.0000% | 4.3658% | 100.0000% | 2.4196% | 0.974 | 30.658 |
| PyneCore 6.4.6 (full feed) | 200 | 43 | 49 | 27 | 8 | 19 | 0 | 0 | 54 | 0 | 0 | 165223 | 707639 | 90.28 | 0.0000% | 75.0000% | 0.0000% | 0.0003% | 0.0000% | 0.4548% | 0.0783% | 100.0000% | 18.7982% | 130.4566% | 11.6838% | 5.152 | 24.785 |
| PyneCore 6.4.6 (range-start feed) | 200 | 60 | 45 | 25 | 5 | 11 | 0 | 0 | 54 | 0 | 0 | 165223 | 146032 | 90.87 | 0.0000% | 40.1070% | 0.0000% | 0.0003% | 0.0000% | 0.2517% | 0.0139% | 100.0000% | 12.5345% | 114.7061% | 5.0745% | 1.033 | 4.417 |


### Closed set by lane — PineForge (full feed, tape-window)

| lane | sampled | excellent | strong | moderate | weak | minimal | fail | not_run |
|---|---|---|---|---|---|---|---|---|
| eth | 20 | 17 | 2 | 1 | 0 | 0 | 0 | 0 |
| btcusdt | 18 | 13 | 3 | 0 | 0 | 0 | 2 | 0 |
| btcusdt-1d | 13 | 5 | 2 | 4 | 0 | 0 | 2 | 0 |
| es1 | 9 | 7 | 1 | 0 | 0 | 1 | 0 | 0 |
| es1-1d | 8 | 4 | 1 | 0 | 0 | 2 | 1 | 0 |
| nq1 | 9 | 7 | 1 | 0 | 1 | 0 | 0 | 0 |
| nq1-1d | 8 | 4 | 0 | 2 | 0 | 1 | 1 | 0 |
| aapl | 18 | 14 | 2 | 0 | 1 | 1 | 0 | 0 |
| nifty | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 |
| nifty-1d | 8 | 7 | 0 | 0 | 0 | 0 | 1 | 0 |
| f | 17 | 14 | 3 | 0 | 0 | 0 | 0 | 0 |
| f-1d | 13 | 10 | 1 | 0 | 0 | 0 | 2 | 0 |
| eurusd | 19 | 10 | 8 | 0 | 0 | 0 | 1 | 0 |
| xauusd | 19 | 12 | 3 | 0 | 1 | 2 | 1 | 0 |
| xauusd-1d | 12 | 7 | 2 | 1 | 0 | 0 | 2 | 0 |


### Closed set by lane — PineForge (range-start feed)

| lane | sampled | excellent | strong | moderate | weak | minimal | fail | not_run |
|---|---|---|---|---|---|---|---|---|
| eth | 20 | 15 | 4 | 1 | 0 | 0 | 0 | 0 |
| btcusdt | 18 | 15 | 1 | 0 | 0 | 0 | 2 | 0 |
| btcusdt-1d | 13 | 9 | 0 | 2 | 0 | 0 | 2 | 0 |
| es1 | 9 | 8 | 0 | 0 | 0 | 1 | 0 | 0 |
| es1-1d | 8 | 5 | 0 | 0 | 0 | 2 | 1 | 0 |
| nq1 | 9 | 8 | 0 | 0 | 1 | 0 | 0 | 0 |
| nq1-1d | 8 | 6 | 0 | 1 | 0 | 0 | 1 | 0 |
| aapl | 18 | 13 | 3 | 1 | 1 | 0 | 0 | 0 |
| nifty | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 |
| nifty-1d | 8 | 7 | 0 | 0 | 0 | 0 | 1 | 0 |
| f | 17 | 17 | 0 | 0 | 0 | 0 | 0 | 0 |
| f-1d | 13 | 11 | 0 | 0 | 0 | 0 | 2 | 0 |
| eurusd | 19 | 11 | 7 | 0 | 0 | 0 | 1 | 0 |
| xauusd | 19 | 14 | 3 | 0 | 0 | 1 | 1 | 0 |
| xauusd-1d | 12 | 9 | 0 | 0 | 1 | 0 | 2 | 0 |


### Closed set by lane — PyneCore 6.9.1 (full feed)

| lane | sampled | excellent | strong | moderate | weak | minimal | fail | not_run |
|---|---|---|---|---|---|---|---|---|
| eth | 20 | 6 | 8 | 2 | 0 | 0 | 4 | 0 |
| btcusdt | 18 | 6 | 7 | 0 | 0 | 2 | 3 | 0 |
| btcusdt-1d | 13 | 0 | 2 | 8 | 1 | 0 | 2 | 0 |
| es1 | 9 | 6 | 2 | 1 | 0 | 0 | 0 | 0 |
| es1-1d | 8 | 0 | 3 | 1 | 0 | 2 | 2 | 0 |
| nq1 | 9 | 6 | 1 | 0 | 0 | 0 | 2 | 0 |
| nq1-1d | 8 | 2 | 0 | 0 | 0 | 4 | 2 | 0 |
| aapl | 18 | 6 | 7 | 0 | 3 | 0 | 2 | 0 |
| nifty | 9 | 7 | 0 | 2 | 0 | 0 | 0 | 0 |
| nifty-1d | 8 | 1 | 3 | 1 | 0 | 1 | 2 | 0 |
| f | 17 | 8 | 5 | 1 | 2 | 0 | 1 | 0 |
| f-1d | 13 | 3 | 2 | 2 | 2 | 0 | 4 | 0 |
| eurusd | 19 | 6 | 8 | 1 | 0 | 0 | 4 | 0 |
| xauusd | 19 | 4 | 10 | 1 | 1 | 1 | 2 | 0 |
| xauusd-1d | 12 | 6 | 2 | 1 | 1 | 0 | 2 | 0 |


### Closed set by lane — PyneCore 6.9.1 (range-start feed)

| lane | sampled | excellent | strong | moderate | weak | minimal | fail | not_run |
|---|---|---|---|---|---|---|---|---|
| eth | 20 | 10 | 7 | 0 | 1 | 0 | 2 | 0 |
| btcusdt | 18 | 12 | 2 | 0 | 1 | 0 | 3 | 0 |
| btcusdt-1d | 13 | 5 | 2 | 3 | 1 | 0 | 2 | 0 |
| es1 | 9 | 8 | 0 | 0 | 1 | 0 | 0 | 0 |
| es1-1d | 8 | 1 | 3 | 0 | 0 | 2 | 2 | 0 |
| nq1 | 9 | 8 | 0 | 0 | 0 | 0 | 1 | 0 |
| nq1-1d | 8 | 2 | 1 | 3 | 0 | 0 | 2 | 0 |
| aapl | 18 | 9 | 4 | 0 | 3 | 0 | 2 | 0 |
| nifty | 9 | 8 | 0 | 1 | 0 | 0 | 0 | 0 |
| nifty-1d | 8 | 2 | 2 | 2 | 0 | 0 | 2 | 0 |
| f | 17 | 13 | 1 | 0 | 2 | 0 | 1 | 0 |
| f-1d | 13 | 4 | 2 | 3 | 0 | 0 | 4 | 0 |
| eurusd | 19 | 8 | 6 | 1 | 0 | 0 | 4 | 0 |
| xauusd | 19 | 9 | 6 | 0 | 1 | 1 | 2 | 0 |
| xauusd-1d | 12 | 8 | 2 | 0 | 0 | 0 | 2 | 0 |


### Closed set by lane — PyneCore 6.4.6 (full feed)

| lane | sampled | excellent | strong | moderate | weak | minimal | fail | not_run |
|---|---|---|---|---|---|---|---|---|
| eth | 20 | 2 | 7 | 1 | 3 | 1 | 6 | 0 |
| btcusdt | 18 | 2 | 7 | 1 | 1 | 1 | 6 | 0 |
| btcusdt-1d | 13 | 0 | 1 | 9 | 0 | 0 | 3 | 0 |
| es1 | 9 | 6 | 1 | 0 | 0 | 1 | 1 | 0 |
| es1-1d | 8 | 0 | 1 | 2 | 0 | 2 | 3 | 0 |
| nq1 | 9 | 4 | 2 | 0 | 0 | 0 | 3 | 0 |
| nq1-1d | 8 | 3 | 0 | 0 | 0 | 4 | 1 | 0 |
| aapl | 18 | 4 | 4 | 2 | 0 | 0 | 8 | 0 |
| nifty | 9 | 5 | 0 | 2 | 0 | 0 | 2 | 0 |
| nifty-1d | 8 | 1 | 3 | 1 | 0 | 1 | 2 | 0 |
| f | 17 | 6 | 6 | 1 | 0 | 0 | 4 | 0 |
| f-1d | 13 | 3 | 2 | 1 | 2 | 1 | 4 | 0 |
| eurusd | 19 | 3 | 4 | 4 | 0 | 4 | 4 | 0 |
| xauusd | 19 | 0 | 9 | 1 | 1 | 4 | 4 | 0 |
| xauusd-1d | 12 | 4 | 2 | 2 | 1 | 0 | 3 | 0 |


### Feature buckets — set A (a script counts in every feature it uses)

| bucket | engine | n | excellent | strong | moderate | weak | minimal | fail | not_run | excellentPct | excellentStrongPct |
|---|---|---|---|---|---|---|---|---|---|---|---|
| trail | PineForge (full feed, tape-window) | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| trail | PineForge (full feed, raw) | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| trail | PyneCore 6.9.1 (full feed) | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| trail | PyneCore 6.4.6 (full feed) | 6 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0.00 | 0.00 |
| brackets | PineForge (full feed, tape-window) | 22 | 20 | 2 | 0 | 0 | 0 | 0 | 0 | 90.90 | 100.00 |
| brackets | PineForge (full feed, raw) | 22 | 20 | 2 | 0 | 0 | 0 | 0 | 0 | 90.90 | 100.00 |
| brackets | PyneCore 6.9.1 (full feed) | 22 | 20 | 2 | 0 | 0 | 0 | 0 | 0 | 90.90 | 100.00 |
| brackets | PyneCore 6.4.6 (full feed) | 22 | 10 | 2 | 10 | 0 | 0 | 0 | 0 | 45.50 | 54.50 |
| partial | PineForge (full feed, tape-window) | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 66.70 | 100.00 |
| partial | PineForge (full feed, raw) | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 66.70 | 100.00 |
| partial | PyneCore 6.9.1 (full feed) | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 66.70 | 100.00 |
| partial | PyneCore 6.4.6 (full feed) | 3 | 0 | 1 | 2 | 0 | 0 | 0 | 0 | 0.00 | 33.30 |
| pyramiding | PineForge (full feed, tape-window) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| pyramiding | PineForge (full feed, raw) | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 66.70 | 100.00 |
| pyramiding | PyneCore 6.9.1 (full feed) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| pyramiding | PyneCore 6.4.6 (full feed) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| pooc | PineForge (full feed, tape-window) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| pooc | PineForge (full feed, raw) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| pooc | PyneCore 6.9.1 (full feed) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| pooc | PyneCore 6.4.6 (full feed) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| margin_lt100 | PineForge (full feed, tape-window) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.00 | 100.00 |
| margin_lt100 | PineForge (full feed, raw) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.00 | 100.00 |
| margin_lt100 | PyneCore 6.9.1 (full feed) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.00 | 100.00 |
| margin_lt100 | PyneCore 6.4.6 (full feed) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.00 | 100.00 |
| magnifier | PineForge (full feed, tape-window) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| magnifier | PineForge (full feed, raw) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| magnifier | PyneCore 6.9.1 (full feed) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| magnifier | PyneCore 6.4.6 (full feed) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| var_state | PineForge (full feed, tape-window) | 22 | 16 | 6 | 0 | 0 | 0 | 0 | 0 | 72.70 | 100.00 |
| var_state | PineForge (full feed, raw) | 22 | 17 | 5 | 0 | 0 | 0 | 0 | 0 | 77.30 | 100.00 |
| var_state | PyneCore 6.9.1 (full feed) | 22 | 17 | 5 | 0 | 0 | 0 | 0 | 0 | 77.30 | 100.00 |
| var_state | PyneCore 6.4.6 (full feed) | 22 | 16 | 5 | 0 | 0 | 0 | 1 | 0 | 72.70 | 95.50 |
| arrays | PineForge (full feed, tape-window) | 7 | 6 | 1 | 0 | 0 | 0 | 0 | 0 | 85.70 | 100.00 |
| arrays | PineForge (full feed, raw) | 7 | 6 | 1 | 0 | 0 | 0 | 0 | 0 | 85.70 | 100.00 |
| arrays | PyneCore 6.9.1 (full feed) | 7 | 4 | 3 | 0 | 0 | 0 | 0 | 0 | 57.10 | 100.00 |
| arrays | PyneCore 6.4.6 (full feed) | 7 | 4 | 3 | 0 | 0 | 0 | 0 | 0 | 57.10 | 100.00 |


### Feature buckets — set B (a script counts in every feature it uses)

| bucket | engine | n | excellent | strong | moderate | weak | minimal | fail | not_run | excellentPct | excellentStrongPct |
|---|---|---|---|---|---|---|---|---|---|---|---|
| trail | PineForge (full feed, tape-window) | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| trail | PineForge (range-start feed) | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| trail | PineForge (full feed, raw) | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| trail | PyneCore 6.9.1 (full feed) | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| trail | PyneCore 6.9.1 (range-start feed) | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| trail | PyneCore 6.4.6 (full feed) | 7 | 0 | 0 | 3 | 0 | 0 | 4 | 0 | 0.00 | 0.00 |
| trail | PyneCore 6.4.6 (range-start feed) | 7 | 0 | 0 | 5 | 0 | 0 | 2 | 0 | 0.00 | 0.00 |
| brackets | PineForge (full feed, tape-window) | 59 | 59 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| brackets | PineForge (range-start feed) | 59 | 54 | 2 | 0 | 0 | 3 | 0 | 0 | 91.50 | 94.90 |
| brackets | PineForge (full feed, raw) | 59 | 36 | 19 | 0 | 1 | 3 | 0 | 0 | 61.00 | 93.20 |
| brackets | PyneCore 6.9.1 (full feed) | 59 | 25 | 13 | 0 | 0 | 0 | 3 | 18 | 42.40 | 64.40 |
| brackets | PyneCore 6.9.1 (range-start feed) | 59 | 39 | 2 | 0 | 0 | 0 | 0 | 18 | 66.10 | 69.50 |
| brackets | PyneCore 6.4.6 (full feed) | 59 | 9 | 10 | 4 | 1 | 0 | 17 | 18 | 15.30 | 32.20 |
| brackets | PyneCore 6.4.6 (range-start feed) | 59 | 25 | 3 | 7 | 2 | 0 | 4 | 18 | 42.40 | 47.50 |
| partial | PineForge (full feed, tape-window) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| partial | PineForge (range-start feed) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| partial | PineForge (full feed, raw) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| partial | PyneCore 6.9.1 (full feed) | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 1 | 66.70 | 66.70 |
| partial | PyneCore 6.9.1 (range-start feed) | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 1 | 66.70 | 66.70 |
| partial | PyneCore 6.4.6 (full feed) | 3 | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 0.00 | 0.00 |
| partial | PyneCore 6.4.6 (range-start feed) | 3 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 0.00 | 0.00 |
| pyramiding | PineForge (full feed, tape-window) | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| pyramiding | PineForge (range-start feed) | 10 | 9 | 0 | 0 | 0 | 1 | 0 | 0 | 90.00 | 90.00 |
| pyramiding | PineForge (full feed, raw) | 10 | 7 | 2 | 0 | 0 | 1 | 0 | 0 | 70.00 | 90.00 |
| pyramiding | PyneCore 6.9.1 (full feed) | 10 | 2 | 0 | 0 | 0 | 0 | 0 | 8 | 20.00 | 20.00 |
| pyramiding | PyneCore 6.9.1 (range-start feed) | 10 | 2 | 0 | 0 | 0 | 0 | 0 | 8 | 20.00 | 20.00 |
| pyramiding | PyneCore 6.4.6 (full feed) | 10 | 2 | 0 | 0 | 0 | 0 | 0 | 8 | 20.00 | 20.00 |
| pyramiding | PyneCore 6.4.6 (range-start feed) | 10 | 2 | 0 | 0 | 0 | 0 | 0 | 8 | 20.00 | 20.00 |
| calc_on_fills | PineForge (full feed, tape-window) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| calc_on_fills | PineForge (range-start feed) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| calc_on_fills | PineForge (full feed, raw) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| calc_on_fills | PyneCore 6.9.1 (full feed) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.00 | 100.00 |
| calc_on_fills | PyneCore 6.9.1 (range-start feed) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.00 | 100.00 |
| calc_on_fills | PyneCore 6.4.6 (full feed) | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0.00 | 0.00 |
| calc_on_fills | PyneCore 6.4.6 (range-start feed) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.00 | 100.00 |
| pooc | PineForge (full feed, tape-window) | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| pooc | PineForge (range-start feed) | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| pooc | PineForge (full feed, raw) | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| pooc | PyneCore 6.9.1 (full feed) | 4 | 1 | 1 | 0 | 0 | 0 | 0 | 2 | 25.00 | 50.00 |
| pooc | PyneCore 6.9.1 (range-start feed) | 4 | 1 | 1 | 0 | 0 | 0 | 0 | 2 | 25.00 | 50.00 |
| pooc | PyneCore 6.4.6 (full feed) | 4 | 0 | 0 | 0 | 0 | 0 | 2 | 2 | 0.00 | 0.00 |
| pooc | PyneCore 6.4.6 (range-start feed) | 4 | 1 | 1 | 0 | 0 | 0 | 0 | 2 | 25.00 | 50.00 |
| margin_lt100 | PineForge (full feed, tape-window) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| margin_lt100 | PineForge (range-start feed) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| margin_lt100 | PineForge (full feed, raw) | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0.00 | 0.00 |
| security | PineForge (full feed, tape-window) | 22 | 22 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| security | PineForge (range-start feed) | 22 | 21 | 1 | 0 | 0 | 0 | 0 | 0 | 95.50 | 100.00 |
| security | PineForge (full feed, raw) | 22 | 18 | 3 | 1 | 0 | 0 | 0 | 0 | 81.80 | 95.50 |
| security | PyneCore 6.9.1 (full feed) | 22 | 1 | 0 | 0 | 0 | 0 | 20 | 1 | 4.50 | 4.50 |
| security | PyneCore 6.9.1 (range-start feed) | 22 | 9 | 2 | 0 | 0 | 0 | 10 | 1 | 40.90 | 50.00 |
| security | PyneCore 6.4.6 (full feed) | 22 | 0 | 0 | 0 | 0 | 0 | 21 | 1 | 0.00 | 0.00 |
| security | PyneCore 6.4.6 (range-start feed) | 22 | 0 | 0 | 0 | 0 | 0 | 21 | 1 | 0.00 | 0.00 |
| magnifier | PineForge (full feed, tape-window) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| magnifier | PineForge (range-start feed) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| magnifier | PineForge (full feed, raw) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| magnifier | PyneCore 6.9.1 (full feed) | 5 | 4 | 0 | 0 | 0 | 0 | 0 | 1 | 80.00 | 80.00 |
| magnifier | PyneCore 6.9.1 (range-start feed) | 5 | 4 | 0 | 0 | 0 | 0 | 0 | 1 | 80.00 | 80.00 |
| magnifier | PyneCore 6.4.6 (full feed) | 5 | 3 | 0 | 0 | 0 | 0 | 1 | 1 | 60.00 | 60.00 |
| magnifier | PyneCore 6.4.6 (range-start feed) | 5 | 4 | 0 | 0 | 0 | 0 | 0 | 1 | 80.00 | 80.00 |
| var_state | PineForge (full feed, tape-window) | 82 | 82 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| var_state | PineForge (range-start feed) | 82 | 71 | 8 | 0 | 0 | 3 | 0 | 0 | 86.60 | 96.30 |
| var_state | PineForge (full feed, raw) | 82 | 71 | 7 | 0 | 1 | 3 | 0 | 0 | 86.60 | 95.10 |
| var_state | PyneCore 6.9.1 (full feed) | 82 | 33 | 7 | 0 | 0 | 0 | 4 | 38 | 40.20 | 48.80 |
| var_state | PyneCore 6.9.1 (range-start feed) | 82 | 39 | 4 | 0 | 0 | 0 | 1 | 38 | 47.60 | 52.40 |
| var_state | PyneCore 6.4.6 (full feed) | 82 | 22 | 7 | 0 | 0 | 0 | 15 | 38 | 26.80 | 35.40 |
| var_state | PyneCore 6.4.6 (range-start feed) | 82 | 33 | 5 | 0 | 0 | 0 | 6 | 38 | 40.20 | 46.30 |
| arrays | PineForge (full feed, tape-window) | 22 | 22 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| arrays | PineForge (range-start feed) | 22 | 18 | 4 | 0 | 0 | 0 | 0 | 0 | 81.80 | 100.00 |
| arrays | PineForge (full feed, raw) | 22 | 17 | 5 | 0 | 0 | 0 | 0 | 0 | 77.30 | 100.00 |
| arrays | PyneCore 6.9.1 (full feed) | 22 | 7 | 9 | 0 | 0 | 0 | 3 | 3 | 31.80 | 72.70 |
| arrays | PyneCore 6.9.1 (range-start feed) | 22 | 14 | 2 | 0 | 0 | 0 | 3 | 3 | 63.60 | 72.70 |
| arrays | PyneCore 6.4.6 (full feed) | 22 | 6 | 8 | 0 | 0 | 0 | 5 | 3 | 27.30 | 63.60 |
| arrays | PyneCore 6.4.6 (range-start feed) | 22 | 14 | 2 | 0 | 0 | 0 | 3 | 3 | 63.60 | 72.70 |
| udt | PineForge (full feed, tape-window) | 29 | 29 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| udt | PineForge (range-start feed) | 29 | 24 | 2 | 0 | 0 | 3 | 0 | 0 | 82.80 | 89.70 |
| udt | PineForge (full feed, raw) | 29 | 24 | 2 | 0 | 0 | 3 | 0 | 0 | 82.80 | 89.70 |
| udt | PyneCore 6.9.1 (full feed) | 29 | 1 | 0 | 0 | 0 | 0 | 0 | 28 | 3.40 | 3.40 |
| udt | PyneCore 6.9.1 (range-start feed) | 29 | 1 | 0 | 0 | 0 | 0 | 0 | 28 | 3.40 | 3.40 |
| udt | PyneCore 6.4.6 (full feed) | 29 | 0 | 0 | 0 | 0 | 0 | 1 | 28 | 0.00 | 0.00 |
| udt | PyneCore 6.4.6 (range-start feed) | 29 | 1 | 0 | 0 | 0 | 0 | 0 | 28 | 3.40 | 3.40 |


### Feature buckets — set C (a script counts in every feature it uses)

| bucket | engine | n | excellent | strong | moderate | weak | minimal | fail | not_run | excellentPct | excellentStrongPct |
|---|---|---|---|---|---|---|---|---|---|---|---|
| trail | PineForge (full feed, tape-window) | 10 | 9 | 1 | 0 | 0 | 0 | 0 | 0 | 90.00 | 100.00 |
| trail | PineForge (range-start feed) | 10 | 9 | 1 | 0 | 0 | 0 | 0 | 0 | 90.00 | 100.00 |
| trail | PineForge (full feed, raw) | 10 | 6 | 1 | 3 | 0 | 0 | 0 | 0 | 60.00 | 70.00 |
| trail | PyneCore 6.9.1 (full feed) | 10 | 3 | 1 | 1 | 4 | 0 | 1 | 0 | 30.00 | 40.00 |
| trail | PyneCore 6.9.1 (range-start feed) | 10 | 3 | 1 | 1 | 4 | 0 | 1 | 0 | 30.00 | 40.00 |
| trail | PyneCore 6.4.6 (full feed) | 10 | 1 | 0 | 2 | 1 | 1 | 5 | 0 | 10.00 | 10.00 |
| trail | PyneCore 6.4.6 (range-start feed) | 10 | 1 | 0 | 3 | 1 | 0 | 5 | 0 | 10.00 | 10.00 |
| brackets | PineForge (full feed, tape-window) | 74 | 49 | 15 | 3 | 2 | 2 | 3 | 0 | 66.20 | 86.50 |
| brackets | PineForge (range-start feed) | 74 | 57 | 8 | 2 | 2 | 2 | 3 | 0 | 77.00 | 87.80 |
| brackets | PineForge (full feed, raw) | 74 | 39 | 23 | 5 | 2 | 2 | 3 | 0 | 52.70 | 83.80 |
| brackets | PyneCore 6.9.1 (full feed) | 74 | 28 | 26 | 7 | 1 | 2 | 10 | 0 | 37.80 | 73.00 |
| brackets | PyneCore 6.9.1 (range-start feed) | 74 | 42 | 15 | 4 | 3 | 1 | 9 | 0 | 56.80 | 77.00 |
| brackets | PyneCore 6.4.6 (full feed) | 74 | 14 | 16 | 13 | 3 | 9 | 19 | 0 | 18.90 | 40.50 |
| brackets | PyneCore 6.4.6 (range-start feed) | 74 | 21 | 13 | 12 | 3 | 6 | 19 | 0 | 28.40 | 45.90 |
| partial | PineForge (full feed, tape-window) | 15 | 9 | 4 | 1 | 0 | 0 | 1 | 0 | 60.00 | 86.70 |
| partial | PineForge (range-start feed) | 15 | 10 | 2 | 2 | 0 | 0 | 1 | 0 | 66.70 | 80.00 |
| partial | PineForge (full feed, raw) | 15 | 6 | 5 | 2 | 0 | 1 | 1 | 0 | 40.00 | 73.30 |
| partial | PyneCore 6.9.1 (full feed) | 15 | 5 | 1 | 2 | 0 | 1 | 6 | 0 | 33.30 | 40.00 |
| partial | PyneCore 6.9.1 (range-start feed) | 15 | 5 | 2 | 1 | 1 | 0 | 6 | 0 | 33.30 | 46.70 |
| partial | PyneCore 6.4.6 (full feed) | 15 | 4 | 0 | 1 | 1 | 2 | 7 | 0 | 26.70 | 26.70 |
| partial | PyneCore 6.4.6 (range-start feed) | 15 | 4 | 2 | 0 | 1 | 1 | 7 | 0 | 26.70 | 40.00 |
| pyramiding | PineForge (full feed, tape-window) | 10 | 2 | 0 | 0 | 1 | 1 | 6 | 0 | 20.00 | 20.00 |
| pyramiding | PineForge (range-start feed) | 10 | 4 | 0 | 0 | 0 | 0 | 6 | 0 | 40.00 | 40.00 |
| pyramiding | PineForge (full feed, raw) | 10 | 3 | 0 | 0 | 0 | 1 | 6 | 0 | 30.00 | 30.00 |
| pyramiding | PyneCore 6.9.1 (full feed) | 10 | 2 | 1 | 0 | 0 | 1 | 6 | 0 | 20.00 | 30.00 |
| pyramiding | PyneCore 6.9.1 (range-start feed) | 10 | 2 | 1 | 0 | 0 | 1 | 6 | 0 | 20.00 | 30.00 |
| pyramiding | PyneCore 6.4.6 (full feed) | 10 | 1 | 0 | 1 | 0 | 1 | 7 | 0 | 10.00 | 10.00 |
| pyramiding | PyneCore 6.4.6 (range-start feed) | 10 | 1 | 0 | 1 | 0 | 1 | 7 | 0 | 10.00 | 10.00 |
| calc_on_fills | PineForge (full feed, tape-window) | 5 | 2 | 1 | 0 | 0 | 2 | 0 | 0 | 40.00 | 60.00 |
| calc_on_fills | PineForge (range-start feed) | 5 | 2 | 1 | 0 | 0 | 2 | 0 | 0 | 40.00 | 60.00 |
| calc_on_fills | PineForge (full feed, raw) | 5 | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 60.00 | 100.00 |
| calc_on_fills | PyneCore 6.9.1 (full feed) | 5 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 20.00 | 100.00 |
| calc_on_fills | PyneCore 6.9.1 (range-start feed) | 5 | 1 | 3 | 0 | 1 | 0 | 0 | 0 | 20.00 | 80.00 |
| calc_on_fills | PyneCore 6.4.6 (full feed) | 5 | 0 | 1 | 0 | 0 | 4 | 0 | 0 | 0.00 | 20.00 |
| calc_on_fills | PyneCore 6.4.6 (range-start feed) | 5 | 0 | 0 | 1 | 0 | 4 | 0 | 0 | 0.00 | 0.00 |
| pooc | PineForge (full feed, tape-window) | 31 | 18 | 5 | 0 | 0 | 1 | 7 | 0 | 58.10 | 74.20 |
| pooc | PineForge (range-start feed) | 31 | 20 | 3 | 1 | 0 | 0 | 7 | 0 | 64.50 | 74.20 |
| pooc | PineForge (full feed, raw) | 31 | 5 | 15 | 3 | 0 | 1 | 7 | 0 | 16.10 | 64.50 |
| pooc | PyneCore 6.9.1 (full feed) | 31 | 4 | 8 | 0 | 5 | 1 | 13 | 0 | 12.90 | 38.70 |
| pooc | PyneCore 6.9.1 (range-start feed) | 31 | 8 | 5 | 0 | 6 | 0 | 12 | 0 | 25.80 | 41.90 |
| pooc | PyneCore 6.4.6 (full feed) | 31 | 1 | 5 | 0 | 2 | 3 | 20 | 0 | 3.20 | 19.40 |
| pooc | PyneCore 6.4.6 (range-start feed) | 31 | 3 | 4 | 1 | 1 | 2 | 20 | 0 | 9.70 | 22.60 |
| margin_lt100 | PineForge (full feed, tape-window) | 5 | 3 | 0 | 0 | 2 | 0 | 0 | 0 | 60.00 | 60.00 |
| margin_lt100 | PineForge (range-start feed) | 5 | 4 | 0 | 0 | 1 | 0 | 0 | 0 | 80.00 | 80.00 |
| margin_lt100 | PineForge (full feed, raw) | 5 | 3 | 0 | 0 | 1 | 1 | 0 | 0 | 60.00 | 60.00 |
| margin_lt100 | PyneCore 6.9.1 (full feed) | 5 | 3 | 0 | 0 | 0 | 1 | 1 | 0 | 60.00 | 60.00 |
| margin_lt100 | PyneCore 6.9.1 (range-start feed) | 5 | 3 | 0 | 0 | 0 | 1 | 1 | 0 | 60.00 | 60.00 |
| margin_lt100 | PyneCore 6.4.6 (full feed) | 5 | 0 | 1 | 0 | 1 | 1 | 2 | 0 | 0.00 | 20.00 |
| margin_lt100 | PyneCore 6.4.6 (range-start feed) | 5 | 0 | 0 | 1 | 1 | 1 | 2 | 0 | 0.00 | 0.00 |
| security | PineForge (full feed, tape-window) | 48 | 21 | 9 | 2 | 1 | 2 | 13 | 0 | 43.80 | 62.50 |
| security | PineForge (range-start feed) | 48 | 27 | 5 | 2 | 1 | 0 | 13 | 0 | 56.20 | 66.70 |
| security | PineForge (full feed, raw) | 48 | 12 | 15 | 4 | 1 | 3 | 13 | 0 | 25.00 | 56.20 |
| security | PyneCore 6.9.1 (full feed) | 48 | 3 | 8 | 2 | 2 | 1 | 32 | 0 | 6.20 | 22.90 |
| security | PyneCore 6.9.1 (range-start feed) | 48 | 8 | 6 | 1 | 4 | 0 | 29 | 0 | 16.70 | 29.20 |
| security | PyneCore 6.4.6 (full feed) | 48 | 1 | 2 | 1 | 0 | 1 | 43 | 0 | 2.10 | 6.20 |
| security | PyneCore 6.4.6 (range-start feed) | 48 | 3 | 0 | 1 | 0 | 1 | 43 | 0 | 6.20 | 6.20 |
| var_state | PineForge (full feed, tape-window) | 134 | 88 | 21 | 5 | 3 | 6 | 11 | 0 | 65.70 | 81.30 |
| var_state | PineForge (range-start feed) | 134 | 100 | 13 | 4 | 3 | 3 | 11 | 0 | 74.60 | 84.30 |
| var_state | PineForge (full feed, raw) | 134 | 54 | 42 | 15 | 3 | 9 | 11 | 0 | 40.30 | 71.60 |
| var_state | PyneCore 6.9.1 (full feed) | 134 | 31 | 42 | 15 | 10 | 7 | 29 | 0 | 23.10 | 54.50 |
| var_state | PyneCore 6.9.1 (range-start feed) | 134 | 55 | 31 | 10 | 10 | 2 | 26 | 0 | 41.00 | 64.20 |
| var_state | PyneCore 6.4.6 (full feed) | 134 | 20 | 28 | 16 | 7 | 15 | 48 | 0 | 14.90 | 35.80 |
| var_state | PyneCore 6.4.6 (range-start feed) | 134 | 26 | 30 | 17 | 4 | 9 | 48 | 0 | 19.40 | 41.80 |
| arrays | PineForge (full feed, tape-window) | 24 | 8 | 5 | 0 | 1 | 1 | 9 | 0 | 33.30 | 54.20 |
| arrays | PineForge (range-start feed) | 24 | 12 | 2 | 1 | 0 | 0 | 9 | 0 | 50.00 | 58.30 |
| arrays | PineForge (full feed, raw) | 24 | 5 | 6 | 0 | 1 | 3 | 9 | 0 | 20.80 | 45.80 |
| arrays | PyneCore 6.9.1 (full feed) | 24 | 2 | 7 | 1 | 1 | 2 | 11 | 0 | 8.30 | 37.50 |
| arrays | PyneCore 6.9.1 (range-start feed) | 24 | 5 | 4 | 3 | 0 | 1 | 11 | 0 | 20.80 | 37.50 |
| arrays | PyneCore 6.4.6 (full feed) | 24 | 3 | 3 | 1 | 1 | 2 | 14 | 0 | 12.50 | 25.00 |
| arrays | PyneCore 6.4.6 (range-start feed) | 24 | 5 | 1 | 3 | 0 | 1 | 14 | 0 | 20.80 | 25.00 |
| udt | PineForge (full feed, tape-window) | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| udt | PineForge (range-start feed) | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| udt | PineForge (full feed, raw) | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 50.00 | 100.00 |
| udt | PyneCore 6.9.1 (full feed) | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 50.00 | 100.00 |
| udt | PyneCore 6.9.1 (range-start feed) | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 100.00 | 100.00 |
| udt | PyneCore 6.4.6 (full feed) | 2 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 50.00 | 50.00 |
| udt | PyneCore 6.4.6 (range-start feed) | 2 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 50.00 | 50.00 |

