## Set A: public benchmark suite (100, ETHUSDT 15m, 53,929 bars)

| engine | n | excellent | strong | moderate | weak | minimal | compile_fail | build_fail | run_error | timeout | not_run | tvTrades | engineTrades | matchedPct | countDelta_median | countDelta_p90 | entryP90_median | entryP90_p90 | exitP90_median | exitP90_p90 | pnlP90_median | pnlP90_p90 | netProfitRelErr_median | netProfitRelErr_p90 | maxEquityDev_median | wall_median_s | wall_p95_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PineForge (full feed, tape-window) | 100 | 89 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 167301 | 166022 | 99.9253 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0795% | 0.0930% | 0.0975% | 2.0523% | 0.0689% | 0.430 | 2.478 |
| PineForge (full feed, raw) | 100 | 84 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 167301 | 245503 | 99.9247 | 0.0000% | 0.0339% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0798% | 0.0968% | 0.5586% | 18.6848% | 0.3071% | 0.425 | 1.025 |
| PyneCore 6.9.1 (full feed, --security supplied) | 100 | 81 | 18 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 167301 | 245417 | 99.6354 | 0.0000% | 0.0351% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0798% | 0.1016% | 0.5687% | 18.6848% | 0.3223% | 2.142 | 4.304 |
| PyneCore 6.9.1 (full feed) | 100 | 81 | 18 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 167301 | 245417 | 99.6354 | 0.0000% | 0.0351% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0798% | 0.1016% | 0.5687% | 18.6848% | 0.3223% | 1.955 | 5.012 |
| PyneCore 6.4.6 (full feed) | 100 | 69 | 18 | 10 | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 167301 | 242657 | 99.1091 | 0.0000% | 0.1456% | 0.0000% | 0.0000% | 0.0000% | 0.4962% | 0.0820% | 348.3379% | 1.0946% | 52.6213% | 0.6040% | 2.721 | 7.858 |


## Set B: public corpus (312, ETHUSDT.P 15m, 222,295 bars)

| engine | n | excellent | strong | moderate | weak | minimal | compile_fail | build_fail | run_error | timeout | not_run | tvTrades | engineTrades | matchedPct | countDelta_median | countDelta_p90 | entryP90_median | entryP90_p90 | exitP90_median | exitP90_p90 | pnlP90_median | pnlP90_p90 | netProfitRelErr_median | netProfitRelErr_p90 | maxEquityDev_median | wall_median_s | wall_p95_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PineForge (full feed, tape-window) | 311 | 311 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 431244 | 429642 | 99.9974 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0866% | 0.0000% | 0.704 | 1.149 |
| PineForge (range-start feed) | 311 | 282 | 24 | 0 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 431244 | 426248 | 99.3812 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 1.1989% | 0.0000% | 0.396 | 0.699 |
| PineForge (full feed, raw) | 311 | 267 | 34 | 2 | 2 | 6 | 0 | 0 | 0 | 0 | 0 | 431244 | 2286415 | 99.2230 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0378% | 11.1367% | 0.0316% | 0.531 | 1.209 |
| PyneCore 6.9.1 (full feed, --security supplied) | 311 | 90 | 31 | 0 | 7 | 1 | 0 | 0 | 2 | 13 | 167 | 431244 | 1018225 | 99.0090 | 0.0000% | 0.3697% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 13.3150% | 0.5673% | 18.2479% | 0.2482% | 5.898 | 13.782 |
| PyneCore 6.9.1 (full feed) | 311 | 90 | 31 | 0 | 2 | 1 | 0 | 0 | 10 | 10 | 167 | 431244 | 1016298 | 99.3120 | 0.0000% | 0.1532% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 7.1621% | 0.4425% | 13.3149% | 0.2284% | 5.894 | 13.840 |
| PyneCore 6.9.1 (range-start feed) | 311 | 117 | 15 | 0 | 2 | 0 | 0 | 0 | 10 | 0 | 167 | 431244 | 199008 | 99.6294 | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0065% | 3.9352% | 0.0029% | 1.416 | 117.806 |
| PyneCore 6.4.6 (full feed) | 311 | 76 | 29 | 7 | 5 | 2 | 0 | 0 | 25 | 0 | 167 | 431244 | 967448 | 97.7850 | 0.0000% | 1.1905% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 27.4307% | 0.7582% | 19.3962% | 0.5410% | 8.427 | 17.908 |
| PyneCore 6.4.6 (range-start feed) | 311 | 92 | 14 | 7 | 6 | 0 | 0 | 0 | 25 | 0 | 167 | 431244 | 165423 | 98.7676 | 0.0000% | 0.0848% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.1534% | 12.1736% | 0.1216% | 1.571 | 3.023 |


## Set C: closed campaign sample (200 script-lane probes, 15 lanes)

| engine | n | excellent | strong | moderate | weak | minimal | compile_fail | build_fail | run_error | timeout | not_run | tvTrades | engineTrades | matchedPct | countDelta_median | countDelta_p90 | entryP90_median | entryP90_p90 | exitP90_median | exitP90_p90 | pnlP90_median | pnlP90_p90 | netProfitRelErr_median | netProfitRelErr_p90 | maxEquityDev_median | wall_median_s | wall_p95_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PineForge (full feed, tape-window) | 200 | 140 | 29 | 8 | 3 | 7 | 0 | 0 | 13 | 0 | 0 | 165223 | 151629 | 98.9187 | 0.0000% | 0.5164% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.1178% | 0.0000% | 16.4154% | 0.0000% | 0.344 | 1.524 |
| PineForge (range-start feed) | 200 | 157 | 18 | 5 | 3 | 4 | 0 | 0 | 13 | 0 | 0 | 165223 | 151393 | 98.9817 | 0.0000% | 0.0994% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 3.3898% | 0.0000% | 0.253 | 0.605 |
| PineForge (full feed, raw) | 200 | 93 | 59 | 20 | 3 | 12 | 0 | 0 | 13 | 0 | 0 | 165223 | 744013 | 97.1624 | 0.0000% | 3.2010% | 0.0000% | 0.0000% | 0.0000% | 0.0049% | 0.0000% | 73.6169% | 1.4433% | 94.5207% | 1.3638% | 0.353 | 1.546 |
| PyneCore 6.9.1 (full feed, --security supplied) | 200 | 68 | 62 | 22 | 14 | 13 | 0 | 0 | 19 | 2 | 0 | 165223 | 711270 | 95.5654 | 0.0000% | 10.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0737% | 0.0000% | 100.0000% | 16.2577% | 124.3221% | 9.6976% | 2.864 | 110.386 |
| PyneCore 6.9.1 (full feed) | 200 | 67 | 60 | 21 | 10 | 10 | 0 | 0 | 29 | 3 | 0 | 165223 | 707535 | 95.6897 | 0.0000% | 5.4496% | 0.0000% | 0.0000% | 0.0000% | 0.0555% | 0.0000% | 100.0000% | 16.2577% | 121.2802% | 8.5821% | 3.092 | 112.913 |
| PyneCore 6.9.1 (range-start feed) | 200 | 107 | 38 | 13 | 10 | 3 | 0 | 0 | 29 | 0 | 0 | 165223 | 146186 | 98.2572 | 0.0000% | 0.8386% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 0.0000% | 75.0000% | 4.3658% | 100.0000% | 2.4196% | 0.974 | 30.658 |
| PyneCore 6.4.6 (full feed) | 200 | 43 | 49 | 27 | 8 | 19 | 0 | 0 | 54 | 0 | 0 | 165223 | 707639 | 90.2836 | 0.0000% | 75.0000% | 0.0000% | 0.0003% | 0.0000% | 0.4548% | 0.0783% | 100.0000% | 18.7982% | 130.4566% | 11.6838% | 5.152 | 24.785 |
| PyneCore 6.4.6 (range-start feed) | 200 | 60 | 45 | 25 | 5 | 11 | 0 | 0 | 54 | 0 | 0 | 165223 | 146032 | 90.8742 | 0.0000% | 40.1070% | 0.0000% | 0.0003% | 0.0000% | 0.2517% | 0.0139% | 100.0000% | 12.5345% | 114.7061% | 5.0745% | 1.033 | 4.417 |


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


### Closed set by lane — PyneCore 6.9.1 (full feed, --security supplied)

| lane | sampled | excellent | strong | moderate | weak | minimal | fail | not_run |
|---|---|---|---|---|---|---|---|---|
| eth | 20 | 6 | 9 | 2 | 1 | 0 | 2 | 0 |
| btcusdt | 18 | 6 | 7 | 0 | 1 | 2 | 2 | 0 |
| btcusdt-1d | 13 | 0 | 2 | 8 | 1 | 0 | 2 | 0 |
| es1 | 9 | 6 | 2 | 1 | 0 | 0 | 0 | 0 |
| es1-1d | 8 | 0 | 3 | 2 | 0 | 2 | 1 | 0 |
| nq1 | 9 | 7 | 1 | 0 | 0 | 1 | 0 | 0 |
| nq1-1d | 8 | 2 | 0 | 0 | 0 | 4 | 2 | 0 |
| aapl | 18 | 6 | 7 | 0 | 4 | 0 | 1 | 0 |
| nifty | 9 | 7 | 0 | 2 | 0 | 0 | 0 | 0 |
| nifty-1d | 8 | 1 | 3 | 1 | 1 | 1 | 1 | 0 |
| f | 17 | 8 | 5 | 1 | 2 | 1 | 0 | 0 |
| f-1d | 13 | 3 | 3 | 2 | 2 | 1 | 2 | 0 |
| eurusd | 19 | 6 | 8 | 1 | 0 | 0 | 4 | 0 |
| xauusd | 19 | 4 | 10 | 1 | 1 | 1 | 2 | 0 |
| xauusd-1d | 12 | 6 | 2 | 1 | 1 | 0 | 2 | 0 |


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
| trail | PineForge (full feed, tape-window) | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PineForge (full feed, raw) | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PyneCore 6.9.1 (full feed, --security supplied) | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PyneCore 6.9.1 (full feed) | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PyneCore 6.4.6 (full feed) | 6 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0.0 | 0.0 |
| brackets | PineForge (full feed, tape-window) | 22 | 20 | 2 | 0 | 0 | 0 | 0 | 0 | 90.9 | 100.0 |
| brackets | PineForge (full feed, raw) | 22 | 20 | 2 | 0 | 0 | 0 | 0 | 0 | 90.9 | 100.0 |
| brackets | PyneCore 6.9.1 (full feed, --security supplied) | 22 | 20 | 2 | 0 | 0 | 0 | 0 | 0 | 90.9 | 100.0 |
| brackets | PyneCore 6.9.1 (full feed) | 22 | 20 | 2 | 0 | 0 | 0 | 0 | 0 | 90.9 | 100.0 |
| brackets | PyneCore 6.4.6 (full feed) | 22 | 10 | 2 | 10 | 0 | 0 | 0 | 0 | 45.5 | 54.5 |
| partial | PineForge (full feed, tape-window) | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 66.7 | 100.0 |
| partial | PineForge (full feed, raw) | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 66.7 | 100.0 |
| partial | PyneCore 6.9.1 (full feed, --security supplied) | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 66.7 | 100.0 |
| partial | PyneCore 6.9.1 (full feed) | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 66.7 | 100.0 |
| partial | PyneCore 6.4.6 (full feed) | 3 | 0 | 1 | 2 | 0 | 0 | 0 | 0 | 0.0 | 33.3 |
| pyramiding | PineForge (full feed, tape-window) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pyramiding | PineForge (full feed, raw) | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 66.7 | 100.0 |
| pyramiding | PyneCore 6.9.1 (full feed, --security supplied) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pyramiding | PyneCore 6.9.1 (full feed) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pyramiding | PyneCore 6.4.6 (full feed) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PineForge (full feed, tape-window) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PineForge (full feed, raw) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PyneCore 6.9.1 (full feed, --security supplied) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PyneCore 6.9.1 (full feed) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PyneCore 6.4.6 (full feed) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| margin_lt100 | PineForge (full feed, tape-window) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| margin_lt100 | PineForge (full feed, raw) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| margin_lt100 | PyneCore 6.9.1 (full feed, --security supplied) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| margin_lt100 | PyneCore 6.9.1 (full feed) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| margin_lt100 | PyneCore 6.4.6 (full feed) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| magnifier | PineForge (full feed, tape-window) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PineForge (full feed, raw) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PyneCore 6.9.1 (full feed, --security supplied) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PyneCore 6.9.1 (full feed) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PyneCore 6.4.6 (full feed) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| var_state | PineForge (full feed, tape-window) | 22 | 16 | 6 | 0 | 0 | 0 | 0 | 0 | 72.7 | 100.0 |
| var_state | PineForge (full feed, raw) | 22 | 17 | 5 | 0 | 0 | 0 | 0 | 0 | 77.3 | 100.0 |
| var_state | PyneCore 6.9.1 (full feed, --security supplied) | 22 | 17 | 5 | 0 | 0 | 0 | 0 | 0 | 77.3 | 100.0 |
| var_state | PyneCore 6.9.1 (full feed) | 22 | 17 | 5 | 0 | 0 | 0 | 0 | 0 | 77.3 | 100.0 |
| var_state | PyneCore 6.4.6 (full feed) | 22 | 16 | 5 | 0 | 0 | 0 | 1 | 0 | 72.7 | 95.5 |
| arrays | PineForge (full feed, tape-window) | 7 | 6 | 1 | 0 | 0 | 0 | 0 | 0 | 85.7 | 100.0 |
| arrays | PineForge (full feed, raw) | 7 | 6 | 1 | 0 | 0 | 0 | 0 | 0 | 85.7 | 100.0 |
| arrays | PyneCore 6.9.1 (full feed, --security supplied) | 7 | 4 | 3 | 0 | 0 | 0 | 0 | 0 | 57.1 | 100.0 |
| arrays | PyneCore 6.9.1 (full feed) | 7 | 4 | 3 | 0 | 0 | 0 | 0 | 0 | 57.1 | 100.0 |
| arrays | PyneCore 6.4.6 (full feed) | 7 | 4 | 3 | 0 | 0 | 0 | 0 | 0 | 57.1 | 100.0 |


### Feature buckets — set B (a script counts in every feature it uses)

| bucket | engine | n | excellent | strong | moderate | weak | minimal | fail | not_run | excellentPct | excellentStrongPct |
|---|---|---|---|---|---|---|---|---|---|---|---|
| trail | PineForge (full feed, tape-window) | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PineForge (range-start feed) | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PineForge (full feed, raw) | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PyneCore 6.9.1 (full feed, --security supplied) | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PyneCore 6.9.1 (full feed) | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PyneCore 6.9.1 (range-start feed) | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| trail | PyneCore 6.4.6 (full feed) | 7 | 0 | 0 | 5 | 0 | 0 | 2 | 0 | 0.0 | 0.0 |
| trail | PyneCore 6.4.6 (range-start feed) | 7 | 0 | 0 | 5 | 0 | 0 | 2 | 0 | 0.0 | 0.0 |
| brackets | PineForge (full feed, tape-window) | 59 | 59 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| brackets | PineForge (range-start feed) | 59 | 54 | 2 | 0 | 0 | 3 | 0 | 0 | 91.5 | 94.9 |
| brackets | PineForge (full feed, raw) | 59 | 36 | 19 | 0 | 1 | 3 | 0 | 0 | 61.0 | 93.2 |
| brackets | PyneCore 6.9.1 (full feed, --security supplied) | 59 | 25 | 13 | 0 | 0 | 0 | 3 | 18 | 42.4 | 64.4 |
| brackets | PyneCore 6.9.1 (full feed) | 59 | 25 | 13 | 0 | 0 | 0 | 3 | 18 | 42.4 | 64.4 |
| brackets | PyneCore 6.9.1 (range-start feed) | 59 | 39 | 2 | 0 | 0 | 0 | 0 | 18 | 66.1 | 69.5 |
| brackets | PyneCore 6.4.6 (full feed) | 59 | 16 | 12 | 7 | 2 | 0 | 4 | 18 | 27.1 | 47.5 |
| brackets | PyneCore 6.4.6 (range-start feed) | 59 | 25 | 3 | 7 | 2 | 0 | 4 | 18 | 42.4 | 47.5 |
| partial | PineForge (full feed, tape-window) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| partial | PineForge (range-start feed) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| partial | PineForge (full feed, raw) | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| partial | PyneCore 6.9.1 (full feed, --security supplied) | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 1 | 66.7 | 66.7 |
| partial | PyneCore 6.9.1 (full feed) | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 1 | 66.7 | 66.7 |
| partial | PyneCore 6.9.1 (range-start feed) | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 1 | 66.7 | 66.7 |
| partial | PyneCore 6.4.6 (full feed) | 3 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 0.0 | 0.0 |
| partial | PyneCore 6.4.6 (range-start feed) | 3 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 0.0 | 0.0 |
| pyramiding | PineForge (full feed, tape-window) | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pyramiding | PineForge (range-start feed) | 10 | 9 | 0 | 0 | 0 | 1 | 0 | 0 | 90.0 | 90.0 |
| pyramiding | PineForge (full feed, raw) | 10 | 7 | 2 | 0 | 0 | 1 | 0 | 0 | 70.0 | 90.0 |
| pyramiding | PyneCore 6.9.1 (full feed, --security supplied) | 10 | 2 | 0 | 0 | 0 | 0 | 0 | 8 | 20.0 | 20.0 |
| pyramiding | PyneCore 6.9.1 (full feed) | 10 | 2 | 0 | 0 | 0 | 0 | 0 | 8 | 20.0 | 20.0 |
| pyramiding | PyneCore 6.9.1 (range-start feed) | 10 | 2 | 0 | 0 | 0 | 0 | 0 | 8 | 20.0 | 20.0 |
| pyramiding | PyneCore 6.4.6 (full feed) | 10 | 2 | 0 | 0 | 0 | 0 | 0 | 8 | 20.0 | 20.0 |
| pyramiding | PyneCore 6.4.6 (range-start feed) | 10 | 2 | 0 | 0 | 0 | 0 | 0 | 8 | 20.0 | 20.0 |
| calc_on_fills | PineForge (full feed, tape-window) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| calc_on_fills | PineForge (range-start feed) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| calc_on_fills | PineForge (full feed, raw) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| calc_on_fills | PyneCore 6.9.1 (full feed, --security supplied) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| calc_on_fills | PyneCore 6.9.1 (full feed) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| calc_on_fills | PyneCore 6.9.1 (range-start feed) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| calc_on_fills | PyneCore 6.4.6 (full feed) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| calc_on_fills | PyneCore 6.4.6 (range-start feed) | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.0 | 100.0 |
| pooc | PineForge (full feed, tape-window) | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PineForge (range-start feed) | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PineForge (full feed, raw) | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| pooc | PyneCore 6.9.1 (full feed, --security supplied) | 4 | 1 | 1 | 0 | 0 | 0 | 0 | 2 | 25.0 | 50.0 |
| pooc | PyneCore 6.9.1 (full feed) | 4 | 1 | 1 | 0 | 0 | 0 | 0 | 2 | 25.0 | 50.0 |
| pooc | PyneCore 6.9.1 (range-start feed) | 4 | 1 | 1 | 0 | 0 | 0 | 0 | 2 | 25.0 | 50.0 |
| pooc | PyneCore 6.4.6 (full feed) | 4 | 1 | 1 | 0 | 0 | 0 | 0 | 2 | 25.0 | 50.0 |
| pooc | PyneCore 6.4.6 (range-start feed) | 4 | 1 | 1 | 0 | 0 | 0 | 0 | 2 | 25.0 | 50.0 |
| margin_lt100 | PineForge (full feed, tape-window) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| margin_lt100 | PineForge (range-start feed) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| margin_lt100 | PineForge (full feed, raw) | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0.0 | 0.0 |
| security | PineForge (full feed, tape-window) | 22 | 22 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| security | PineForge (range-start feed) | 22 | 21 | 1 | 0 | 0 | 0 | 0 | 0 | 95.5 | 100.0 |
| security | PineForge (full feed, raw) | 22 | 18 | 3 | 1 | 0 | 0 | 0 | 0 | 81.8 | 95.5 |
| security | PyneCore 6.9.1 (full feed, --security supplied) | 22 | 1 | 0 | 0 | 5 | 0 | 15 | 1 | 4.5 | 4.5 |
| security | PyneCore 6.9.1 (full feed) | 22 | 1 | 0 | 0 | 0 | 0 | 20 | 1 | 4.5 | 4.5 |
| security | PyneCore 6.9.1 (range-start feed) | 22 | 9 | 2 | 0 | 0 | 0 | 10 | 1 | 40.9 | 50.0 |
| security | PyneCore 6.4.6 (full feed) | 22 | 0 | 0 | 0 | 0 | 0 | 21 | 1 | 0.0 | 0.0 |
| security | PyneCore 6.4.6 (range-start feed) | 22 | 0 | 0 | 0 | 0 | 0 | 21 | 1 | 0.0 | 0.0 |
| magnifier | PineForge (full feed, tape-window) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PineForge (range-start feed) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PineForge (full feed, raw) | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| magnifier | PyneCore 6.9.1 (full feed, --security supplied) | 5 | 4 | 0 | 0 | 0 | 0 | 0 | 1 | 80.0 | 80.0 |
| magnifier | PyneCore 6.9.1 (full feed) | 5 | 4 | 0 | 0 | 0 | 0 | 0 | 1 | 80.0 | 80.0 |
| magnifier | PyneCore 6.9.1 (range-start feed) | 5 | 4 | 0 | 0 | 0 | 0 | 0 | 1 | 80.0 | 80.0 |
| magnifier | PyneCore 6.4.6 (full feed) | 5 | 4 | 0 | 0 | 0 | 0 | 0 | 1 | 80.0 | 80.0 |
| magnifier | PyneCore 6.4.6 (range-start feed) | 5 | 4 | 0 | 0 | 0 | 0 | 0 | 1 | 80.0 | 80.0 |
| var_state | PineForge (full feed, tape-window) | 82 | 82 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| var_state | PineForge (range-start feed) | 82 | 71 | 8 | 0 | 0 | 3 | 0 | 0 | 86.6 | 96.3 |
| var_state | PineForge (full feed, raw) | 82 | 71 | 7 | 0 | 1 | 3 | 0 | 0 | 86.6 | 95.1 |
| var_state | PyneCore 6.9.1 (full feed, --security supplied) | 82 | 33 | 7 | 0 | 1 | 0 | 3 | 38 | 40.2 | 48.8 |
| var_state | PyneCore 6.9.1 (full feed) | 82 | 33 | 7 | 0 | 0 | 0 | 4 | 38 | 40.2 | 48.8 |
| var_state | PyneCore 6.9.1 (range-start feed) | 82 | 39 | 4 | 0 | 0 | 0 | 1 | 38 | 47.6 | 52.4 |
| var_state | PyneCore 6.4.6 (full feed) | 82 | 30 | 8 | 0 | 0 | 0 | 6 | 38 | 36.6 | 46.3 |
| var_state | PyneCore 6.4.6 (range-start feed) | 82 | 33 | 5 | 0 | 0 | 0 | 6 | 38 | 40.2 | 46.3 |
| arrays | PineForge (full feed, tape-window) | 22 | 22 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| arrays | PineForge (range-start feed) | 22 | 18 | 4 | 0 | 0 | 0 | 0 | 0 | 81.8 | 100.0 |
| arrays | PineForge (full feed, raw) | 22 | 17 | 5 | 0 | 0 | 0 | 0 | 0 | 77.3 | 100.0 |
| arrays | PyneCore 6.9.1 (full feed, --security supplied) | 22 | 7 | 9 | 0 | 1 | 0 | 2 | 3 | 31.8 | 72.7 |
| arrays | PyneCore 6.9.1 (full feed) | 22 | 7 | 9 | 0 | 0 | 0 | 3 | 3 | 31.8 | 72.7 |
| arrays | PyneCore 6.9.1 (range-start feed) | 22 | 14 | 2 | 0 | 0 | 0 | 3 | 3 | 63.6 | 72.7 |
| arrays | PyneCore 6.4.6 (full feed) | 22 | 7 | 9 | 0 | 0 | 0 | 3 | 3 | 31.8 | 72.7 |
| arrays | PyneCore 6.4.6 (range-start feed) | 22 | 14 | 2 | 0 | 0 | 0 | 3 | 3 | 63.6 | 72.7 |
| udt | PineForge (full feed, tape-window) | 29 | 29 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| udt | PineForge (range-start feed) | 29 | 24 | 2 | 0 | 0 | 3 | 0 | 0 | 82.8 | 89.7 |
| udt | PineForge (full feed, raw) | 29 | 24 | 2 | 0 | 0 | 3 | 0 | 0 | 82.8 | 89.7 |
| udt | PyneCore 6.9.1 (full feed, --security supplied) | 29 | 1 | 0 | 0 | 0 | 0 | 0 | 28 | 3.4 | 3.4 |
| udt | PyneCore 6.9.1 (full feed) | 29 | 1 | 0 | 0 | 0 | 0 | 0 | 28 | 3.4 | 3.4 |
| udt | PyneCore 6.9.1 (range-start feed) | 29 | 1 | 0 | 0 | 0 | 0 | 0 | 28 | 3.4 | 3.4 |
| udt | PyneCore 6.4.6 (full feed) | 29 | 1 | 0 | 0 | 0 | 0 | 0 | 28 | 3.4 | 3.4 |
| udt | PyneCore 6.4.6 (range-start feed) | 29 | 1 | 0 | 0 | 0 | 0 | 0 | 28 | 3.4 | 3.4 |


### Feature buckets — set C (a script counts in every feature it uses)

| bucket | engine | n | excellent | strong | moderate | weak | minimal | fail | not_run | excellentPct | excellentStrongPct |
|---|---|---|---|---|---|---|---|---|---|---|---|
| trail | PineForge (full feed, tape-window) | 10 | 9 | 1 | 0 | 0 | 0 | 0 | 0 | 90.0 | 100.0 |
| trail | PineForge (range-start feed) | 10 | 9 | 1 | 0 | 0 | 0 | 0 | 0 | 90.0 | 100.0 |
| trail | PineForge (full feed, raw) | 10 | 6 | 1 | 3 | 0 | 0 | 0 | 0 | 60.0 | 70.0 |
| trail | PyneCore 6.9.1 (full feed, --security supplied) | 10 | 3 | 1 | 1 | 5 | 0 | 0 | 0 | 30.0 | 40.0 |
| trail | PyneCore 6.9.1 (full feed) | 10 | 3 | 1 | 1 | 4 | 0 | 1 | 0 | 30.0 | 40.0 |
| trail | PyneCore 6.9.1 (range-start feed) | 10 | 3 | 1 | 1 | 4 | 0 | 1 | 0 | 30.0 | 40.0 |
| trail | PyneCore 6.4.6 (full feed) | 10 | 1 | 0 | 2 | 1 | 1 | 5 | 0 | 10.0 | 10.0 |
| trail | PyneCore 6.4.6 (range-start feed) | 10 | 1 | 0 | 3 | 1 | 0 | 5 | 0 | 10.0 | 10.0 |
| brackets | PineForge (full feed, tape-window) | 74 | 49 | 15 | 3 | 2 | 2 | 3 | 0 | 66.2 | 86.5 |
| brackets | PineForge (range-start feed) | 74 | 57 | 8 | 2 | 2 | 2 | 3 | 0 | 77.0 | 87.8 |
| brackets | PineForge (full feed, raw) | 74 | 39 | 23 | 5 | 2 | 2 | 3 | 0 | 52.7 | 83.8 |
| brackets | PyneCore 6.9.1 (full feed, --security supplied) | 74 | 28 | 26 | 7 | 4 | 3 | 6 | 0 | 37.8 | 73.0 |
| brackets | PyneCore 6.9.1 (full feed) | 74 | 28 | 26 | 7 | 1 | 2 | 10 | 0 | 37.8 | 73.0 |
| brackets | PyneCore 6.9.1 (range-start feed) | 74 | 42 | 15 | 4 | 3 | 1 | 9 | 0 | 56.8 | 77.0 |
| brackets | PyneCore 6.4.6 (full feed) | 74 | 14 | 16 | 13 | 3 | 9 | 19 | 0 | 18.9 | 40.5 |
| brackets | PyneCore 6.4.6 (range-start feed) | 74 | 21 | 13 | 12 | 3 | 6 | 19 | 0 | 28.4 | 45.9 |
| partial | PineForge (full feed, tape-window) | 15 | 9 | 4 | 1 | 0 | 0 | 1 | 0 | 60.0 | 86.7 |
| partial | PineForge (range-start feed) | 15 | 10 | 2 | 2 | 0 | 0 | 1 | 0 | 66.7 | 80.0 |
| partial | PineForge (full feed, raw) | 15 | 6 | 5 | 2 | 0 | 1 | 1 | 0 | 40.0 | 73.3 |
| partial | PyneCore 6.9.1 (full feed, --security supplied) | 15 | 5 | 1 | 3 | 2 | 2 | 2 | 0 | 33.3 | 40.0 |
| partial | PyneCore 6.9.1 (full feed) | 15 | 5 | 1 | 2 | 0 | 1 | 6 | 0 | 33.3 | 40.0 |
| partial | PyneCore 6.9.1 (range-start feed) | 15 | 5 | 2 | 1 | 1 | 0 | 6 | 0 | 33.3 | 46.7 |
| partial | PyneCore 6.4.6 (full feed) | 15 | 4 | 0 | 1 | 1 | 2 | 7 | 0 | 26.7 | 26.7 |
| partial | PyneCore 6.4.6 (range-start feed) | 15 | 4 | 2 | 0 | 1 | 1 | 7 | 0 | 26.7 | 40.0 |
| pyramiding | PineForge (full feed, tape-window) | 10 | 2 | 0 | 0 | 1 | 1 | 6 | 0 | 20.0 | 20.0 |
| pyramiding | PineForge (range-start feed) | 10 | 4 | 0 | 0 | 0 | 0 | 6 | 0 | 40.0 | 40.0 |
| pyramiding | PineForge (full feed, raw) | 10 | 3 | 0 | 0 | 0 | 1 | 6 | 0 | 30.0 | 30.0 |
| pyramiding | PyneCore 6.9.1 (full feed, --security supplied) | 10 | 2 | 1 | 0 | 0 | 1 | 6 | 0 | 20.0 | 30.0 |
| pyramiding | PyneCore 6.9.1 (full feed) | 10 | 2 | 1 | 0 | 0 | 1 | 6 | 0 | 20.0 | 30.0 |
| pyramiding | PyneCore 6.9.1 (range-start feed) | 10 | 2 | 1 | 0 | 0 | 1 | 6 | 0 | 20.0 | 30.0 |
| pyramiding | PyneCore 6.4.6 (full feed) | 10 | 1 | 0 | 1 | 0 | 1 | 7 | 0 | 10.0 | 10.0 |
| pyramiding | PyneCore 6.4.6 (range-start feed) | 10 | 1 | 0 | 1 | 0 | 1 | 7 | 0 | 10.0 | 10.0 |
| calc_on_fills | PineForge (full feed, tape-window) | 5 | 2 | 1 | 0 | 0 | 2 | 0 | 0 | 40.0 | 60.0 |
| calc_on_fills | PineForge (range-start feed) | 5 | 2 | 1 | 0 | 0 | 2 | 0 | 0 | 40.0 | 60.0 |
| calc_on_fills | PineForge (full feed, raw) | 5 | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 60.0 | 100.0 |
| calc_on_fills | PyneCore 6.9.1 (full feed, --security supplied) | 5 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 20.0 | 100.0 |
| calc_on_fills | PyneCore 6.9.1 (full feed) | 5 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 20.0 | 100.0 |
| calc_on_fills | PyneCore 6.9.1 (range-start feed) | 5 | 1 | 3 | 0 | 1 | 0 | 0 | 0 | 20.0 | 80.0 |
| calc_on_fills | PyneCore 6.4.6 (full feed) | 5 | 0 | 1 | 0 | 0 | 4 | 0 | 0 | 0.0 | 20.0 |
| calc_on_fills | PyneCore 6.4.6 (range-start feed) | 5 | 0 | 0 | 1 | 0 | 4 | 0 | 0 | 0.0 | 0.0 |
| pooc | PineForge (full feed, tape-window) | 31 | 18 | 5 | 0 | 0 | 1 | 7 | 0 | 58.1 | 74.2 |
| pooc | PineForge (range-start feed) | 31 | 20 | 3 | 1 | 0 | 0 | 7 | 0 | 64.5 | 74.2 |
| pooc | PineForge (full feed, raw) | 31 | 5 | 15 | 3 | 0 | 1 | 7 | 0 | 16.1 | 64.5 |
| pooc | PyneCore 6.9.1 (full feed, --security supplied) | 31 | 4 | 8 | 1 | 6 | 2 | 10 | 0 | 12.9 | 38.7 |
| pooc | PyneCore 6.9.1 (full feed) | 31 | 4 | 8 | 0 | 5 | 1 | 13 | 0 | 12.9 | 38.7 |
| pooc | PyneCore 6.9.1 (range-start feed) | 31 | 8 | 5 | 0 | 6 | 0 | 12 | 0 | 25.8 | 41.9 |
| pooc | PyneCore 6.4.6 (full feed) | 31 | 1 | 5 | 0 | 2 | 3 | 20 | 0 | 3.2 | 19.4 |
| pooc | PyneCore 6.4.6 (range-start feed) | 31 | 3 | 4 | 1 | 1 | 2 | 20 | 0 | 9.7 | 22.6 |
| margin_lt100 | PineForge (full feed, tape-window) | 5 | 3 | 0 | 0 | 2 | 0 | 0 | 0 | 60.0 | 60.0 |
| margin_lt100 | PineForge (range-start feed) | 5 | 4 | 0 | 0 | 1 | 0 | 0 | 0 | 80.0 | 80.0 |
| margin_lt100 | PineForge (full feed, raw) | 5 | 3 | 0 | 0 | 1 | 1 | 0 | 0 | 60.0 | 60.0 |
| margin_lt100 | PyneCore 6.9.1 (full feed, --security supplied) | 5 | 3 | 0 | 0 | 0 | 2 | 0 | 0 | 60.0 | 60.0 |
| margin_lt100 | PyneCore 6.9.1 (full feed) | 5 | 3 | 0 | 0 | 0 | 1 | 1 | 0 | 60.0 | 60.0 |
| margin_lt100 | PyneCore 6.9.1 (range-start feed) | 5 | 3 | 0 | 0 | 0 | 1 | 1 | 0 | 60.0 | 60.0 |
| margin_lt100 | PyneCore 6.4.6 (full feed) | 5 | 0 | 1 | 0 | 1 | 1 | 2 | 0 | 0.0 | 20.0 |
| margin_lt100 | PyneCore 6.4.6 (range-start feed) | 5 | 0 | 0 | 1 | 1 | 1 | 2 | 0 | 0.0 | 0.0 |
| security | PineForge (full feed, tape-window) | 48 | 21 | 9 | 2 | 1 | 2 | 13 | 0 | 43.8 | 62.5 |
| security | PineForge (range-start feed) | 48 | 27 | 5 | 2 | 1 | 0 | 13 | 0 | 56.2 | 66.7 |
| security | PineForge (full feed, raw) | 48 | 12 | 15 | 4 | 1 | 3 | 13 | 0 | 25.0 | 56.2 |
| security | PyneCore 6.9.1 (full feed, --security supplied) | 48 | 4 | 10 | 3 | 6 | 4 | 21 | 0 | 8.3 | 29.2 |
| security | PyneCore 6.9.1 (full feed) | 48 | 3 | 8 | 2 | 2 | 1 | 32 | 0 | 6.2 | 22.9 |
| security | PyneCore 6.9.1 (range-start feed) | 48 | 8 | 6 | 1 | 4 | 0 | 29 | 0 | 16.7 | 29.2 |
| security | PyneCore 6.4.6 (full feed) | 48 | 1 | 2 | 1 | 0 | 1 | 43 | 0 | 2.1 | 6.2 |
| security | PyneCore 6.4.6 (range-start feed) | 48 | 3 | 0 | 1 | 0 | 1 | 43 | 0 | 6.2 | 6.2 |
| var_state | PineForge (full feed, tape-window) | 134 | 88 | 21 | 5 | 3 | 6 | 11 | 0 | 65.7 | 81.3 |
| var_state | PineForge (range-start feed) | 134 | 100 | 13 | 4 | 3 | 3 | 11 | 0 | 74.6 | 84.3 |
| var_state | PineForge (full feed, raw) | 134 | 54 | 42 | 15 | 3 | 9 | 11 | 0 | 40.3 | 71.6 |
| var_state | PyneCore 6.9.1 (full feed, --security supplied) | 134 | 32 | 43 | 16 | 14 | 10 | 19 | 0 | 23.9 | 56.0 |
| var_state | PyneCore 6.9.1 (full feed) | 134 | 31 | 42 | 15 | 10 | 7 | 29 | 0 | 23.1 | 54.5 |
| var_state | PyneCore 6.9.1 (range-start feed) | 134 | 55 | 31 | 10 | 10 | 2 | 26 | 0 | 41.0 | 64.2 |
| var_state | PyneCore 6.4.6 (full feed) | 134 | 20 | 28 | 16 | 7 | 15 | 48 | 0 | 14.9 | 35.8 |
| var_state | PyneCore 6.4.6 (range-start feed) | 134 | 26 | 30 | 17 | 4 | 9 | 48 | 0 | 19.4 | 41.8 |
| arrays | PineForge (full feed, tape-window) | 24 | 8 | 5 | 0 | 1 | 1 | 9 | 0 | 33.3 | 54.2 |
| arrays | PineForge (range-start feed) | 24 | 12 | 2 | 1 | 0 | 0 | 9 | 0 | 50.0 | 58.3 |
| arrays | PineForge (full feed, raw) | 24 | 5 | 6 | 0 | 1 | 3 | 9 | 0 | 20.8 | 45.8 |
| arrays | PyneCore 6.9.1 (full feed, --security supplied) | 24 | 2 | 7 | 1 | 1 | 2 | 11 | 0 | 8.3 | 37.5 |
| arrays | PyneCore 6.9.1 (full feed) | 24 | 2 | 7 | 1 | 1 | 2 | 11 | 0 | 8.3 | 37.5 |
| arrays | PyneCore 6.9.1 (range-start feed) | 24 | 5 | 4 | 3 | 0 | 1 | 11 | 0 | 20.8 | 37.5 |
| arrays | PyneCore 6.4.6 (full feed) | 24 | 3 | 3 | 1 | 1 | 2 | 14 | 0 | 12.5 | 25.0 |
| arrays | PyneCore 6.4.6 (range-start feed) | 24 | 5 | 1 | 3 | 0 | 1 | 14 | 0 | 20.8 | 25.0 |
| udt | PineForge (full feed, tape-window) | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| udt | PineForge (range-start feed) | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| udt | PineForge (full feed, raw) | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 50.0 | 100.0 |
| udt | PyneCore 6.9.1 (full feed, --security supplied) | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 50.0 | 100.0 |
| udt | PyneCore 6.9.1 (full feed) | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 50.0 | 100.0 |
| udt | PyneCore 6.9.1 (range-start feed) | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 100.0 | 100.0 |
| udt | PyneCore 6.4.6 (full feed) | 2 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 50.0 | 50.0 |
| udt | PyneCore 6.4.6 (range-start feed) | 2 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 50.0 | 50.0 |

