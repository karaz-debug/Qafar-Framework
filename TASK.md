# Algo Trading Framework

## Table of Contents
1. [Project Overview](#project-overview)
2. [Project File Structure](#project-file-structure)
3. [Detailed Component Breakdown](#detailed-component-breakdown)
   - [A. Data Management (data/)](#a-data-management-data)
   - [B. Strategies (strategies/)](#b-strategies-strategies)
   - [C. Backtesting (backtesting/)](#c-backtesting-backtesting)
   - [D. Optimization (optimization/)](#d-optimization-optimization)
   - [E. Utilities (utils/)](#e-utilities-utils)
   - [F. Testing (tests/)](#f-testing-tests)
4. [Step-by-Step Implementation Plan](#step-by-step-implementation-plan)
   - [Day 1: Set Up Project Structure and Initialize Modules](#day-1-set-up-project-structure-and-initialize-modules)
   - [Day 2: Develop Data Management Module](#day-2-develop-data-management-module)
   - [Day 3: Resampling and Caching](#day-3-resampling-and-caching)
   - [Day 4: Base Strategy and Single-TF Strategy](#day-4-base-strategy-and-single-tf-strategy)
   - [Day 5: Backtesting Runner](#day-5-backtesting-runner)
   - [Day 6: Multi-Timeframe Strategy](#day-6-multi-timeframe-strategy)
   - [Day 7: Backtest Runner Enhancement for MTF](#day-7-backtest-runner-enhancement-for-mtf)
   - [Day 8: Logging and Configuration](#day-8-logging-and-configuration)
   - [Day 9: Optimization Module](#day-9-optimization-module)
   - [Day 10: Helper Functions and Dynamic Strategy Loading](#day-10-helper-functions-and-dynamic-strategy-loading)
   - [Day 11: Testing Framework](#day-11-testing-framework)
   - [Day 12: Main Execution Workflow](#day-12-main-execution-workflow)
   - [Day 13: Final Refinements and Documentation](#day-13-final-refinements-and-documentation)
5. [Additional Considerations](#additional-considerations)
6. [Resources for Further Learning](#resources-for-further-learning)
7. [Implementation Checklist](#implementation-checklist)
8. [Moving Forward](#moving-forward)

## Project Overview
Your algorithmic trading framework is designed to be a modular, scalable, and efficient system capable of handling multiple assets and timeframes. The framework encompasses data management, strategy development, backtesting, optimization, and comprehensive testing, ensuring robust and reliable trading strategies.

## ########### ---------------------------------------------------#####################################################################
## FOR TOMMOROW(16/10) WORKS START HERE INSHALLAH #########----------------------------####################################
## ########### ---------------------------------------------------#####################################################################

## Project File Structure  - -----  16/10 INSHALLAH THIS I WILL BE DOING TOMMOROW FINISHING IN 6 DAYS INSTEAD OF 13 DAYS
Organizing your project directory effectively is crucial. Here's the recommended structure tailored to your requirements:

```
Qafary_Framework/
├── data/
│   ├── raw/
│   │   └── [Asset]/                 # e.g., BTCUSD/
│   │       └── BTCUSDT_1m.csv       # 1-minute data
│   ├── processed/
│   │   └── [Asset]/                 # e.g., BTCUSD/
│   │       ├── BTCUSDT_1m_processed.csv
│   │       ├── BTCUSDT_1H_processed.csv
│   │       └── BTCUSDT_1D_processed.csv
│   └── data_manager.py
├── strategies/
│   ├── __init__.py
│   ├── base_strategy.py
│   ├── momentum_strategy.py
│   ├── multi_tf_strategy.py
│   └── custom_strategy.py
├── backtesting/
│   ├── __init__.py
│   ├── backtest_runner.py
│   └── results_analysis.py
├── optimization/
│   ├── __init__.py
│   ├── optimizer.py
│   ├── alpha_decay.py
│   ├── walk_forward.py
│   └── monte_carlo.py
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   ├── config.py
│   └── helpers.py
├── tests/
│   ├── test_data_manager.py
│   ├── test_backtest_runner.py
│   └── test_optimizer.py
├── main.py
├── requirements.txt
└── README.md

```

## Detailed Component Breakdown

### A. Data Management (data/) - 16/10 INSHALLAH THIS I WILL BE DOING TOMMOROW FINISHING IN 6 DAYS INSTEAD OF 13 DAYS
Purpose: Handle all data-related operations, including loading, preprocessing, resampling, and caching to avoid redundant processing.

#### i. Folder Structure = DONE SUCCESSFULLY
- raw/: Contains unprocessed high-frequency data for each asset in separate subfolders.
  Example:
  ```
  data/raw/EURUSD/EURUSD_minute.csv
  data/raw/GBPUSD/GBPUSD_minute.csv
  ```
- processed/: Stores processed data at various timeframes for each asset.
  Example:
  ```
  data/processed/EURUSD/EURUSD_minute_processed.csv
  data/processed/EURUSD/EURUSD_1H_processed.csv
  data/processed/EURUSD/EURUSD_1D_processed.csv
  ```

#### ii. data_manager.py Features = = DONE SUCCESSFULLY
- Loading Raw Data: DONE
  - Automatically detect and load raw data files from the raw/ directory.
  - Support multiple assets by scanning subdirectories.
- Preprocessing: DONE
  - Clean data (e.g., handle missing values, sort by date).
  - Ensure consistency in data formats across different assets.
- Resampling: DONE
  - Convert high-frequency data (e.g., 1-minute) to lower timeframes (e.g., 1-hour, 1-day) using efficient resampling methods.
  - Implement a caching mechanism to check if a processed file already exists before resampling to save computational resources.
- Saving and Loading Processed Data: DONE
  - Save processed and resampled data into the processed/ directory.
  - Load processed data for backtesting and optimization.
- Batch Processing:
  - Handle multiple assets and their corresponding timeframes in a single operation.
  - Ensure scalability as more assets are added.

#### iii. Output
- Processed Data Files: Ready-to-use CSV files for each asset at various timeframes, stored in the data/processed/ directory.
- Logs: Records of data processing steps, errors, and statuses for debugging and auditing.

#### iv. Resources
- Pandas Resampling Documentation
- Python os Module for File Operations


## ########### ---------------------------------------------------#####################################################################
## FOR TOMMOROW WORKS END HERE INSHALLAH #########----------------------------########################################################
## ########### ---------------------------------------------------#####################################################################


- Congratulations on successfully completing and testing the Data   Management part of your Qafary Framework, Ak Dev! 🎉 Moving forward, establishing the Strategy component is a crucial step toward enabling effective backtesting and optimization. Below, you'll find a comprehensive guide to setting up the Strategies module, including the necessary folder structure, base classes, and example strategy implementations



### B. Strategies (strategies/)
Purpose: Define various trading strategies, both single-timeframe and multi-timeframe, each encapsulated in its own module for modularity and reusability.

#### i. Folder Structure
- __init__.py: Makes the directory a Python package.
- base_strategy.py: Abstract base class defining the structure and shared functionalities for all strategies.
- Strategy Modules: Each strategy (e.g., Momentum, Multi-TF, Custom) has its own Python file.

#### ii. base_strategy.py Features
- Abstract Methods:
  - init(): Initialize indicators and variables.
  - next(): Define the trading logic, to be implemented by derived classes.
- Attributes:
  - requires_multiple_timeframes: Boolean indicating if the strategy is multi-timeframe.

#### iii. Individual Strategy Modules
- Single-Timeframe Strategies (e.g., momentum_strategy.py):
  - Inherit from BaseStrategy.
  - Implement init() and next() methods.
  - Define strategy-specific parameters and param_bounds for optimization.
- Multi-Timeframe Strategies (e.g., multi_tf_strategy.py):
  - Inherit from BaseStrategy.
  - Set requires_multiple_timeframes = True.
  - Access multiple dataframes (e.g., hourly and daily) via strategy_kwargs.
  - Implement init() and next() using indicators from multiple timeframes.

#### iv. Output
- Strategy Classes: Ready-to-use classes that can be instantiated and passed to the backtesting module.

#### v. Resources
- Object-Oriented Programming in Python
- Backtesting.py Documentation

###  DONE ALL ON 16/10
####  ####   FINISH UP THIS TODAY ALLX #############
####  ####   FINISH UP THIS TODAY ALLX #############
####  ####   FINISH UP THIS TODAY ALLX #############
####  ####   FINISH UP THIS TODAY ALLX #############



## TOMMOROW TASK INSHALLAH ADDED SOME FUNCTIONALLITY ALSO HERE DOWN
## ########### ---------------------------------------------------#####################################################################
## FOR 17TH WORKS STARTED HERE #########----------------------------########################################################
## ########### ---------------------------------------------------#####################################################################

## Plan for Tomorrow (Backtesting Implementation):

- Develop Backtesting Engine: Create a class that can consume strategy signals, execute trades, manage the portfolio, and apply risk management techniques.
- Integrate Strategies: Ensure the backtesting engine can interact seamlessly with strategy instances, interpreting their signals and executing trades accordingly.
- Implement Risk Management: Utilize the risk parameters provided by strategies to manage positions effectively (e.g., setting stop-loss and take-profit orders).

### C. Backtesting (backtesting/)
Purpose: Execute backtests for different strategies, handling both single-TF and MTF strategies, and analyze results.

#### i. Folder Structure
- __init__.py: Makes the directory a Python package.
- backtest_runner.py: Core module to run backtests.
- results_analysis.py: Module to analyze and visualize backtest results.

#### ii. backtest_runner.py Features
- Initialization:
  - Accepts a data_dict containing processed data for each asset and timeframe.
  - Determines if the strategy requires multiple timeframes.
- Running Backtests:
  - For Single-TF Strategies:
    - Use only the primary timeframe data.
  - For MTF Strategies:
    - Pass the entire data_dict to the strategy via strategy_kwargs.
    - Ensure that the Backtest instance is correctly configured based on the strategy type.
- Handling Multiple Assets:
  - Iterate through each asset and execute backtests individually or concurrently, depending on design preferences.
- Result Storage:
  - Store backtest results for further analysis.

#### iii. results_analysis.py Features
- Performance Metrics:
  - Calculate and display key metrics like Equity Final, Sharpe Ratio, Drawdown, etc.
- Visualization:
  - Plot equity curves, drawdown charts, and other relevant visualizations for performance assessment.
- Reporting:
  - Generate summary reports consolidating results from multiple backtests.

#### iv. Output
- Backtest Results: Metrics and visualizations showcasing strategy performance.
- Logs: Records of backtest execution steps and any errors encountered.

#### v. Resources
- Backtesting.py Documentation
- Matplotlib for Plotting


###  DONE ALL ON 17/10  IT WAS QUITE DIFFICULT BUT WILL ALL STRAGLES OF LAST 2 DAYS WE MADE IT FINALY AND TEST THE THE BACKTEST OF 
## ON MOMENTUM STRATEGY AND IT WORKS FINE AND WE ARE ON THE RIGHT TRACK ON TRYING TO TEST MTF STRATEGY AND SEE IF IT WORKS 
####  ####   FINISH UP THIS TODAY ALLX #############
####  ####   FINISH UP THIS TODAY ALLX #############
####  ####   FINISH UP THIS TODAY ALLX #############
####  ####   FINISH UP THIS TODAY ALLX #############

## HERE THE RESULT OF MOMENTUM STRATEGY I TEST WITH OUR NEW FRAMWORK
###  @@RESULTS
# Duration: 1506 days 08:15:00
# Start: 2020-08-31 21:00:00
# End: 2024-10-16 05:15:00
# Return (%): -82.8260913099938
# Buy & Hold Return (%): 474.6917414732492
# Return (Ann.) (%): -34.71613443662537
# Volatility (Ann.) (%): 20.34245993750424
# Sharpe Ratio: 0.0
# Sortino Ratio: 0.0
# Calmar Ratio: 0.0
# Max Drawdown (%): -84.6266259455898
# Avg Drawdown (%): -3.761489102217156
# # Trades: 2536
# Win Rate (%): 27.444794952681388
# Profit Factor: 0.8686968373151382
# SQN: -2.1330843087242615


## WE DID WELL ALSO IN PERFORMING MTF STRATEGT WITH 2 DIFFERENT TF SUCH AS 1 HR AND 5 MIN THIS IS GREAT  - 19/10 DONE SUCCESSFULLY ALLXX
## Full report generated and saved to 'REPORT\MultiTimeframeStrategy_BTCUSD_Report.html'
## Performance Metrics for 'MultiTimeframeStrategy_BTCUSD':
# Duration: 1506 days 08:15:00
# Start: 2020-08-31 21:00:00
# End: 2024-10-16 05:15:00
# Return (%): -48.54503313999935
# Buy & Hold Return (%): 474.6917414732492
# Return (Ann.) (%): -14.856174284773182
# Volatility (Ann.) (%): 15.100173192359131
# Sharpe Ratio: 0.0
# Sortino Ratio: 0.0
# Calmar Ratio: 0.0
# Max Drawdown (%): N/A
# Avg Drawdown (%): N/A
# Total Trades: N/A
# Win Rate (%): N/A
# Profit Factor: 0.7750752189019486
# SQN: -2.041989626078631


## TESTED AGAIN WITH BREAKOUT STRATEGY WHICH HAVE SUPPORT AND RESISTANCE CALCULATION AND IT WORKS FINE AND WE ARE ON THE RIGHT TRACK ON TRYING TO TEST MTF STRATEGY AND SEE IF IT WORKS - 20TH 10 DONE

## HERE THE RESULT OF BREAKOUT STRATEGY I TEST WITH OUR NEW FRAMWORK

## Backtest summary saved to 'REPORT\backtest_summary.csv'
- Equity curve plotted and saved to 'REPORT\BreakoutMTFStrategy_BTCUSD_equity_curve.png'
- Full report generated and saved to 'REPORT\BreakoutMTFStrategy_BTCUSD_Report.html'
- Performance Metrics for 'BreakoutMTFStrategy_BTCUSD':
- Duration: 1506 days 08:15:00
- Start: 2020-08-31 21:00:00
- End: 2024-10-16 05:15:00
- Return (%): 115.28262992000222
- Buy & Hold Return (%): 474.6917414732492
- Return (Ann.) (%): 20.393297209260997
- Volatility (Ann.) (%): 57.10415128040648
- Sharpe Ratio: 0.35712460043615646
- Sortino Ratio: 0.6625514259200266
- Calmar Ratio: 0.3457822457254105
- Max Drawdown (%): N/A
- Avg Drawdown (%): N/A
- Total Trades: N/A
- Win Rate (%): N/A
- Profit Factor: 1.2586755203965798
- SQN: 0.664879128581542



## ########### ---------------------------------------------------#####################################################################
## FOR 21/10 WORKS STARTED HERE #########----------------------------########################################################
## ########### ---------------------------------------------------#####################################################################

### D. Optimization (optimization/)
Documentation: Implementing Sequential Optimization in Backtesting.py
This documentation explains how to implement a sequential optimization process in Backtesting.py. The objective of this method is to first optimize a strategy based on profitability metrics (such as maximizing equity) and then refine the best parameter set by minimizing risk metrics (such as drawdown).

Overview of Sequential Optimization
Sequential Optimization is a method where you optimize a strategy in stages. First, you focus on maximizing a primary objective (e.g., equity or Sharpe ratio), and once you find the best-performing parameters for this goal, you proceed to refine them by optimizing for a secondary objective (e.g., minimizing drawdown). This approach allows you to manage conflicting goals (e.g., high returns vs. low risk) effectively and incrementally.

Step-by-Step Guide
1. Set Up Your Strategy in Backtesting.py
Before performing optimization, you need to have a strategy defined in Backtesting.py. Ensure that the strategy is already tested and ready for optimization.

2. Define Parameter Space
To optimize a strategy, you need to define the parameter ranges that you want to explore. These parameters could include things like:

Moving average periods
Stop-loss and take-profit levels
Risk management variables
For example, define the parameter ranges such as:

ma_period_short: [10, 20, 30]
ma_period_long: [50, 100, 200]
stop_loss: [0.02, 0.05, 0.1]
take_profit: [0.02, 0.05, 0.1]
3. Phase 1: Optimize for Maximizing Equity (or Primary Objective)
The first phase focuses on maximizing profitability (e.g., equity). This involves running a backtest on various combinations of parameters using either grid search or random search.

Goal: Find the parameter set that maximizes equity or another key performance metric such as the Sharpe ratio or total return.
Steps:
Set Up Search: Create a parameter grid or random search function that explores different parameter combinations.
Run Backtests: For each parameter set, run the backtest and collect the results (e.g., final equity).
Evaluate Performance: Identify the parameter set that performs best in terms of equity (or other primary metrics).
Output:
The best-performing parameters that maximize equity.
4. Phase 2: Optimize for Minimizing Drawdown (or Secondary Objective)
Once you have found the best parameters based on equity, the next step is to refine these parameters by optimizing for a secondary objective, such as minimizing drawdown or reducing volatility.

Goal: Take the best-performing parameters from Phase 1 and further refine them to minimize drawdown (or other risk-related metrics).
Steps:
Parameter Refinement: Narrow down the parameter ranges to focus on the best-performing parameters from Phase 1.
Run Backtests Again: For each refined parameter set, run new backtests, this time evaluating based on metrics like maximum drawdown or volatility.
Minimize Drawdown: Identify the parameter set that minimizes drawdown while maintaining a satisfactory level of equity.
Output:
The parameter set that both maximizes equity and minimizes drawdown.
5. Optional Phase 3: Further Refinement for Additional Goals
If you have more objectives to consider, such as improving the Sharpe ratio, increasing the win rate, or minimizing volatility, you can add additional stages.

Goal: Further optimize the strategy by balancing additional objectives like risk-adjusted returns or win rate.
Steps:
Refine Parameter Space: Based on the best parameters from Phase 2, define a new, narrower parameter space.
Run Optimization: Run another round of optimization targeting the new objective.
Evaluate Results: Choose the parameters that strike the best balance between all objectives.
Output:
A finely-tuned strategy that balances profitability, risk, and other trading metrics.
Key Considerations for Sequential Optimization
Weighting Different Objectives:

In some cases, you may want to combine multiple objectives into a single custom objective function. However, in sequential optimization, you handle each objective one at a time. If you prefer to weight goals differently, you could do this by assigning weights to different metrics (e.g., 40% for equity, 30% for Sharpe ratio, 20% for win rate, 10% for drawdown).
Efficiency:

Sequential optimization is often more efficient than optimizing all objectives at once because you limit the search space after each phase. In the second phase, you're focusing on a smaller, more refined set of parameters, which reduces computational overhead.
Interpretability:

This staged process helps you understand how each objective influences your strategy's performance. By isolating each goal, you can better interpret the trade-offs between profitability and risk.
Conflict Between Objectives:

Many trading objectives (like maximizing returns vs. minimizing drawdown) are inherently conflicting. Sequential optimization allows you to first maximize your primary goal and then deal with trade-offs by refining parameters for risk or other metrics.
Examples of Common Objectives
Primary Objective: Maximize Equity

Focus on maximizing the final value of your portfolio over the backtesting period. This is typically the most important metric for traders focused on growth.
Secondary Objective: Minimize Drawdown

After optimizing for equity, refine parameters to minimize drawdown, which measures the peak-to-trough decline in portfolio value. This is crucial for managing risk.
Tertiary Objectives: Sharpe Ratio, Volatility, Win Rate

Further optimization could involve improving the Sharpe ratio (risk-adjusted returns), minimizing portfolio volatility, or increasing the win rate (percentage of successful trades).
Conclusion
Sequential optimization is a flexible and effective way to optimize trading strategies in Backtesting.py. By focusing on one goal at a time (first maximizing equity, then minimizing risk), you can manage conflicting objectives more effectively and ensure a well-balanced trading strategy. This method provides clarity, computational efficiency, and better control over trade-offs, making it ideal for refining complex trading systems.


## THIS WAS THE OPTIMIZED RESULTS WE GET ON PHASE 1 OF THE OPTIMIZATION
# Backtest summary saved to 'REPORT\backtest_summary.csv'
- Equity curve plotted and saved to 'REPORT\BreakoutMTFStrategy_BTCUSD_equity_curve.png'
- Full report generated and saved to 'REPORT\BreakoutMTFStrategy_BTCUSD_Report.html'
- Performance Metrics for 'BreakoutMTFStrategy_BTCUSD':
- Duration: 1506 days 08:15:00
- Start: 2020-08-31 21:00:00
- End: 2024-10-16 05:15:00
- Return (%): 256.5775288400029 FROM 115%
- Buy & Hold Return (%): 474.6917414732492
- Return (Ann.) (%): 36.03313114263158
- Volatility (Ann.) (%): 68.22625657363997
- Sharpe Ratio: 0.5281417001640599 FROM 0
- Sortino Ratio: 1.1719892872470579 FROM 0
- Calmar Ratio: 0.5715065988465318  FROM 0
- Max Drawdown (%): 63.05
- Avg Drawdown (%):  29.62
- Total Trades: 116
- Win Rate (%): 41.38
- Profit Factor: 1.37
- SQN: 1.0258738573189277

## PREVIOUS TP PERCENTAGE AND STOPLOSS  -  
  - tp_percent = 7
  - sl_percent =  15

## AFTER OPTIMIZATION WITH SOME TWEEKS WE GOT BEST PARAMETERS AS THIS
 - tp_percent = 14
 - sl_percent =  7 
 - AND WITH THIS TWEEK YIELDED THIS FROM 115% TO 256% RETURN PNL WITH GOOD SHARPE RATIO AND SORTINO RATIO AND CALMAR RATIO



## Grid Search Best Parameter's
Select optimization method:
1. Grid Search
2. Random Search
3. Sequential Optimization
Enter the number of the optimization method you want to use: 1

Best Parameters from Grid Search:
tp_percent                    14
sl_percent                    11
Equity Final [$]    315511.79916
Sharpe Ratio             0.44905
Calmar Ratio            0.465615
Win Rate [%]           51.252847
Max Drawdown [%]            None
Name: 63, dtype: object


# WITH ABOVE OPTIMIZATION HERE THE RESULT LESSER THAN THE PREVIOUS 
Full report generated and saved to 'REPORT\BreakoutMTFStrategy_BTCUSD_Report.html'

Performance Metrics for 'BreakoutMTFStrategy_BTCUSD':
Duration: 1506 days 08:15:00
Start: 2020-08-31 21:00:00
End: 2024-10-16 05:15:00
Return (%): 192.84
Buy & Hold Return (%): 474.69
Return (Ann.) (%): 29.70
Volatility (Ann.) (%): 67.19
Sharpe Ratio: 0.44
Sortino Ratio: 0.93
Calmar Ratio: 0.49
Max Drawdown (%): 60.43
Avg Drawdown (%): 28.88
Total Trades: 81
Win Rate (%): 51.85
Profit Factor: 1.33
SQN: 0.86



## Radom Search Best Parameter's played well than the Grid Search
Do you want to run optimization? (yes/no): YES
Select optimization method:
1. Grid Search
2. Random Search
3. Sequential Optimization
Enter the number of the optimization method you want to use: 2

Best Parameters from Random Search:
tp_percent                    14
sl_percent                     7
Equity Final [$]    314533.14854
Sharpe Ratio            0.471246
Calmar Ratio            0.496913
Win Rate [%]           50.569476
Max Drawdown [%]            None
Name: 11, dtype: object

## Similar to Our Sequential Optimization we did first well - 
## Time:
 - Sequential Optimization: 2hrs to Run 4 years data
 - Grid Search: 25min To  run 4years data
 - Random Search: 13min to run 4years data


## ########### ---------------------------------------------------#####################################################################
## FINISHED WITHIN 21/10 WITH OPTIMIZED RESULT #########----------------------------########################################################
## ########### ---------------------------------------------------#####################################################################



## ######################## NICE CLI IMPLEMENTATION FOR BACKTESTING #########################################################
## HERE HOW IT LOOKS  - 27/10
 C:/Users/IQRA/anaconda3/envs/algotrader_new_env/python.exe "c:/Users/IQRA/Desktop/Qafary Framework/main.py"      
Available assets:
1. BTCUSD
2. ETHUSD
3. LTCUSD
Enter the number of the asset you want to backtest: 1

Available timeframes:
1. 1m
2. 5m
3. 15m
4. 1H
5. 4H
6. 1D
Enter the number of the timeframe you want to add (or 'done' to finish): 2
Added timeframe: 5m
Enter the number of the timeframe you want to add (or 'done' to finish): 4
Added timeframe: 1H
Enter the number of the timeframe you want to add (or 'done' to finish): done

Available strategies:
1. BreakoutMTFStrategy
2. MomentumStrategy
3. MultiTimeframeStrategy
Enter the number of the strategy you want to use: 1
2024-10-27 19:38:36,180 - INFO - Initialized DataManager with raw data path: C:/Users/IQRA/Desktop/Qafary Framework/data/raw and processed data path: C:/Users/IQRA/Desktop/Qafary Framework/data/processed
Enter take-profit percentage (e.g., 14): 14
Enter stop-loss percentage (e.g., 11): 7
Enter higher_tf_short_ma (e.g., 20): 20
Enter higher_tf_long_ma (e.g., 50): 50
Enter primary timeframe (e.g., 5m): 5m
Enter higher timeframe (e.g., 1H): 1H
Enter value for requires_multiple_timeframes: True
Report directory 'REPORT' is ready.

Result for 'BreakoutMTFStrategy_BTCUSD':
Available Trade Columns: ['Size', 'EntryBar', 'ExitBar', 'EntryPrice', 'ExitPrice', 'PnL', 'ReturnPct', 'EntryTime', 'ExitTime', 'Duration']
   Size  EntryBar  ...            ExitTime         Duration
0    -1      2281  ... 2020-09-14 13:50:00  5 days 18:45:00
1    -9      1909  ... 2020-09-14 16:05:00  7 days 04:00:00
2    -1      6601  ... 2020-10-09 12:45:00 15 days 17:40:00
3    -8      4873  ... 2020-10-12 21:25:00 25 days 02:20:00
4     7     12961  ... 2020-10-21 22:30:00  6 days 01:25:00

[5 rows x 10 columns]
Error accessing attribute 'is_unique': unhashable type: 'DataFrame'
Available Result Attributes: ['Duration', 'End', 'SQN', 'Start', 'array', 'at', 'attrs', 'axes', 'dtype', 'dtypes', 'empty', 'flags', 'hasnans', 'iat', 'index', 'is_monotonic_decreasing', 'is_monotonic_increasing', 'name', 'nbytes', 'ndim', 'shape', 'size', 'str', 'values']
Computed Max Drawdown (%): 62.87
Computed Avg Drawdown (%): 29.73

Summary of Backtest Results:
                     Strategy  ...       SQN
0  BreakoutMTFStrategy_BTCUSD  ...  0.982357

[1 rows x 14 columns]
Backtest summary saved to 'REPORT\backtest_summary.csv'
Equity curve plotted and saved to 'REPORT\BreakoutMTFStrategy_BTCUSD_equity_curve.png'
Strategy Name: BreakoutMTFStrategy_BTCUSD
Equity Curve Image: BreakoutMTFStrategy_BTCUSD_equity_curve.png
Summary Keys: ['Duration', 'Start', 'End', 'Return (%)', 'Buy & Hold Return (%)', 'Return (Ann.) (%)', 'Volatility (Ann.) (%)', 'Sharpe Ratio', 'Sortino Ratio', 'Calmar Ratio', 'Max Drawdown (%)', 'Avg Drawdown (%)', 'Total Trades', 'Win Rate (%)', 'Profit Factor', 'SQN']
Summary Values: [Timedelta('1506 days 08:15:00'), Timestamp('2020-08-31 21:00:00'), Timestamp('2024-10-16 05:15:00'), '238.74', '474.69', '34.35', '67.22', '0.51', '1.12', '0.55', '62.87', '29.73', 116, '41.38', '1.34', '0.98']
Trades Table: <table border="1" class="dataframe dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>Size</th>
      <th>EntryBar</th>
      <th>ExitBar</th>
      <th>EntryPrice</th>
      <th>ExitPrice</th>
      <th>PnL</th>
      <th>ReturnPct</th>
      <th>EntryTime</th>
      <th>ExitTime</th>
      <th>Duration</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>-1</td>
      <td>2281</td>
      <td>3946</td>
      <td>9936.61694</td>
      <td>10653.4871</td>
      <td>-716.87016</
Looking for templates in: C:/Users/IQRA/Desktop/Qafary Framework/templates     
Full report generated and saved to 'REPORT\BreakoutMTFStrategy_BTCUSD_Report.html'

Performance Metrics for 'BreakoutMTFStrategy_BTCUSD':
Duration: 1506 days 08:15:00
Start: 2020-08-31 21:00:00
End: 2024-10-16 05:15:00
Return (%): 238.74
Buy & Hold Return (%): 474.69
Return (Ann.) (%): 34.35
Volatility (Ann.) (%): 67.22
Sharpe Ratio: 0.51
Sortino Ratio: 1.12
Calmar Ratio: 0.55
Max Drawdown (%): 62.87
Avg Drawdown (%): 29.73
Total Trades: 116
Win Rate (%): 41.38
Profit Factor: 1.34
SQN: 0.98



Do you want to run optimization? (yes/no): yes

Select optimization method:
1. Grid Search
2. Random Search
3. Sequential Optimization
Enter the number of the optimization method you want to use: 2

Enter parameter ranges for optimization:
Enter range for tp_percent (e.g., start,stop,step): 10,14,1
Enter range for sl_percent (e.g., start,stop,step): 5,10,1
Enter range for higher_tf_short_ma (e.g., start,stop,step): 14,25,5
Enter range for higher_tf_long_ma (e.g., start,stop,step): 40,60,10

Do you want to set a constraint on the parameters? (yes/no)
tp_percent > sl_percent
Enter the number of random samples to perform: 20

Best Parameters from Random Search:
tp_percent                    14.0
sl_percent                    10.0
higher_tf_short_ma              19
higher_tf_short_ma              19
higher_tf_long_ma               50
Equity Final [$]      209341.82602
Sharpe Ratio              0.310637
Calmar Ratio              0.273992
Win Rate [%]             50.340136
Max Drawdown [%]              None
Name: 6, dtype: object
PS C:\Users\IQRA\Desktop\Qafary Framework>



## AND THIS HOW IT LOOKS WHEN YOUR INPUTING FROM THE TERMINAL IS LOOKING AMAIZING AND RUNNING ALL OUR OPTIMIZATION - DONE THIS ON 27/10
- Implement user CLI for backtesting in main.py so that we can run the backtesting on our own terminal easily with choices ahead  = DONE THIS FINISHED SUCCESSFULLY

Starting Qafary Framework Process.
Available assets:
1. BTCUSD
2. ETHUSD
3. LTCUSD
Enter the number of the asset you want to backtest: 1

User selected asset: BTCUSD

Available timeframes:
1. 1m
2. 5m
3. 15m
4. 1H
5. 4H
6. 1D
Enter the number of the timeframe you want to add (or 'done' to finish): 2
Added timeframe: 5m
Enter the number of the timeframe you want to add (or 'done' to finish): 4
Added timeframe: 1H
Enter the number of the timeframe you want to add (or 'done' to finish): done

User selected timeframes: ['5m', '1H']

Available strategies:
1. MomentumStrategy
2. BreakoutMTFStrategy
3. MultiTimeframeStrategy
Enter the number of the strategy you want to use: 2

User selected strategy: BreakoutMTFStrategy

Enter take-profit percentage (e.g., 14): **12**
Enter stop-loss percentage (e.g., 11): **8**
Enter higher_tf_short_ma (e.g., 20): **20**
Enter higher_tf_long_ma (e.g., 50): **50**
Enter primary timeframe (e.g., 5m): **5m**
Enter higher timeframe (e.g., 1H): **1H**
Set requires_multiple_timeframes to True

Running Backtest without Optimization.

[Backtest runs, and results are generated...]

Strategy: BreakoutMTFStrategy_BTCUSD
Start: 2021-01-01 00:00:00
End:   2021-12-31 23:59:00

Total Trades: 150
Total Return: 30.00%
Sharpe Ratio: 1.8
Max Drawdown: -12.00%

Do you want to run optimization? (yes/no): **yes**

User chose to run optimization.

Select optimization method:
1. Grid Search
2. Random Search
3. Sequential Optimization
Enter the number of the optimization method you want to use: **1**

Enter parameter ranges for optimization:
Enter range for tp_percent (e.g., start,stop,step): **10,14,1**
Enter range for sl_percent (e.g., start,stop,step): **5,10,1**
Enter range for higher_tf_short_ma (e.g., start,stop,step): **15,25,5**
Enter range for higher_tf_long_ma (e.g., start,stop,step): **40,60,10**

Do you want to set a constraint on the parameters? (yes/no)
**yes**
Enter constraint as a Python expression involving the parameters (e.g., tp_percent > sl_percent):
**tp_percent > sl_percent**

Starting Grid Search Optimization with joblib
Total parameter combinations after applying constraints: 24

[Optimization runs...]

Best Parameters from Grid Search:
tp_percent              12
sl_percent               6
higher_tf_short_ma      20
higher_tf_long_ma       50
Equity Final [$]    130000
Sharpe Ratio           1.85
Max Drawdown [%]    -10.00

Grid search results saved to optimization/grid_search/grid_search_results.csv

Process completed successfully.



## this is



##  OPTIMIZATION ON GOING INSHALLAH TOMMOROW WE WILL IMPLEMENT THESE FEATURES  - 28/10
## TODO:
- Monte Carlo Optimization = done
- Alpha decay optimization = still
- Genetic Algorithm Optimization - still


- Monte Carlo Optimization: We'll create a MonteCarloOptimizer class that runs multiple simulations with random variations in parameters and market data to assess the robustness  of the strategy.

- Alpha Decay Optimization: We'll create an AlphaDecayOptimizer class that analyzes the decay of alpha (strategy's edge) over time, helping to optimize parameters related to timing.
