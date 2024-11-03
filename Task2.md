# Algorithmic Trading Framework Implementation Guide

## Overview

This README provides a comprehensive, day-by-day guide for implementing an algorithmic trading framework. The framework includes modules for data management, strategy development, backtesting, optimization, and utilities.

## Table of Contents

1. [Project Structure](#1-project-structure)
2. [Implementation Plan](#2-implementation-plan)
3. [Detailed Component Breakdown](#3-detailed-component-breakdown)
4. [Daily Implementation Steps](#4-daily-implementation-steps)
5. [Additional Considerations](#5-additional-considerations)
6. [Resources](#6-resources)

## 1. Project Structure

```
algo_trading_framework/
├── data/
│   ├── raw/
│   │   └── [Asset]/
│   │       └── [Asset]_minute.csv
│   ├── processed/
│   │   └── [Asset]/
│   │       ├── [Asset]_minute_processed.csv
│   │       ├── [Asset]_1H_processed.csv
│   │       └── [Asset]_1D_processed.csv
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

## 2. Implementation Plan

Follow this 13-day plan to implement the framework:

1. Project Setup
2. Data Management Module
3. Resampling and Caching
4. Base Strategy and Single-TF Strategy
5. Backtesting Runner
6. Multi-Timeframe Strategy
7. Backtest Runner Enhancement for MTF
8. Logging and Configuration
9. Optimization Module
10. Helper Functions and Dynamic Strategy Loading
11. Testing Framework
12. Main Execution Workflow
13. Final Refinements and Documentation

## 3. Detailed Component Breakdown

### A. Data Management (data/)

Purpose: Handle all data-related operations, including loading, preprocessing, resampling, and caching.

Features:
- Loading Raw Data
- Preprocessing
- Resampling
- Saving and Loading Processed Data
- Batch Processing

### B. Strategies (strategies/)

Purpose: Define various trading strategies, both single-timeframe and multi-timeframe.

Features:
- Base Strategy Class
- Single-Timeframe Strategies
- Multi-Timeframe Strategies

### C. Backtesting (backtesting/)

Purpose: Execute backtests for different strategies, handling both single-TF and MTF strategies, and analyze results.

Features:
- Initialization
- Running Backtests
- Handling Multiple Assets
- Result Storage

### D. Optimization (optimization/)

Purpose: Optimize strategy parameters based on various performance metrics.

Features:
- Initialization
- Defining Optimization Objectives
- Optimization Algorithms
- Handling Multiple Assets
- Caching Mechanism

### E. Utilities (utils/)

Purpose: Provide helper functions, logging, and configuration management.

Features:
- Logging Setup
- Configuration Parameters
- Dynamic Strategy Loading
- Validation Functions

## 4. Daily Implementation Steps

### Day 1: Project Setup

Tasks:
- [ ] Create the directory structure as outlined above
- [ ] Initialize Python packages with __init__.py files
- [ ] Set up version control (e.g., Git) to track changes

Verification:
- [ ] Ensure all directories are correctly created
- [ ] Confirm that the project is under version control

### Day 2: Data Management Module

Tasks:
- [ ] Implement data_manager.py with functions to load and preprocess data
- [ ] Develop automated asset detection

Verification:
- [ ] Test loading raw data for multiple assets
- [ ] Verify automated asset detection functionality

### Day 3: Resampling and Caching

Tasks:
- [ ] Implement resampling functions in data_manager.py
- [ ] Add caching to reuse processed data

Verification:
- [ ] Test resampling accuracy
- [ ] Verify caching functionality

### Day 4: Base Strategy and Single-TF Strategy

Tasks:
- [ ] Develop base_strategy.py defining the abstract base class
- [ ] Implement a simple single-timeframe strategy (e.g., Momentum Strategy)

Verification:
- [ ] Instantiate the Momentum Strategy and ensure it initializes correctly
- [ ] Check that it correctly accesses the primary timeframe data

### Day 5: Backtesting Runner

Tasks:
- [ ] Develop backtest_runner.py to handle backtest execution
- [ ] Create results_analysis.py for performance metrics and visualizations

Verification:
- [ ] Run a backtest for the Momentum Strategy and verify output metrics
- [ ] Ensure that visualizations are correctly generated

### Day 6: Multi-Timeframe Strategy

Tasks:
- [ ] Implement a multi-timeframe strategy (e.g., using hourly and daily data)
- [ ] Ensure it correctly accesses multiple dataframes via strategy_kwargs

Verification:
- [ ] Run a backtest for the MTF Strategy and verify that it utilizes both timeframes
- [ ] Check for correct trading signals based on multiple timeframes

### Day 7: Backtest Runner Enhancement for MTF

Tasks:
- [ ] Update backtest_runner.py to differentiate between Single-TF and MTF strategies
- [ ] Ensure that only necessary data is passed based on strategy type

Verification:
- [ ] Backtest both Single-TF and MTF strategies and verify correct data handling
- [ ] Confirm that Single-TF strategies do not receive unnecessary data

### Day 8: Logging and Configuration

Tasks:
- [ ] Develop logger.py to set up centralized logging
- [ ] Create config.py to manage configuration settings

Verification:
- [ ] Test logging across different modules
- [ ] Ensure that configuration settings are accessible and correctly applied

### Day 9: Optimization Module

Tasks:
- [ ] Implement optimizer.py to handle parameter optimization with maximize and minimize metrics
- [ ] Incorporate weight handling for metrics prioritization

Verification:
- [ ] Run optimization on the Momentum Strategy and verify that parameters are optimized based on defined metrics
- [ ] Test different weight configurations to observe their impact

### Day 10: Helper Functions and Dynamic Strategy Loading

Tasks:
- [ ] Develop helpers.py with functions like dynamic strategy loading
- [ ] Ensure that strategies can be loaded based on user input without hardcoding

Verification:
- [ ] Dynamically load and execute different strategies through main.py
- [ ] Confirm that strategies are correctly instantiated with required parameters

### Day 11: Testing Framework

Tasks:
- [ ] Write unit tests for data_manager.py, backtest_runner.py, and optimizer.py
- [ ] Ensure that tests cover key functionalities and edge cases

Verification:
- [ ] Run all tests and ensure they pass
- [ ] Address any failures or bugs identified through testing

### Day 12: Main Execution Workflow

Tasks:
- [ ] Implement main.py with command-line argument parsing
- [ ] Integrate all components to execute backtests and optimizations based on user inputs

Verification:
- [ ] Run sample commands to execute backtests and optimizations
- [ ] Ensure that outputs are as expected and that the framework behaves correctly

### Day 13: Final Refinements and Documentation

Tasks:
- [ ] Refine code for efficiency and readability
- [ ] Optimize data processing and backtest execution times
- [ ] Address any remaining bugs or issues identified during testing
- [ ] Update README.md with detailed instructions, usage examples, and feature descriptions
- [ ] Ensure all modules have comprehensive docstrings

Verification:
- [ ] Profile the framework to identify bottlenecks
- [ ] Ensure that optimizations do not compromise functionality
- [ ] Review documentation for clarity and completeness
- [ ] Validate that the framework is ready for use and further development

## 5. Additional Considerations

- Handling Dynamic Timeframes
- Optimizing Multiple Assets
- Enhancing Optimization Weights
- Efficient Data Processing
- User Experience Enhancements

## 6. Resources

- Pandas Documentation
- Backtesting.py Documentation
- SciPy Optimization Documentation
- Python Logging Documentation
- Python unittest Framework
- Argparse Documentation

Remember to adapt this plan as needed based on your progress and any specific requirements that arise during development. Good luck with your implementation!




## LEARNING ON 16/10/2024
Example of Indicator Reuse:
# utils/indicators.py

import pandas as pd

def calculate_moving_average(data, window):
    """
    Calculate the moving average for a given window size.

    Parameters:
        data (pd.Series): Series of prices.
        window (int): Window size for the moving average.

    Returns:
        pd.Series: Moving average values.
    """
    return data.rolling(window=window).mean()


## AND HOW TO USE IT IN STRATEGY - THIS IS GREAT ALSO BECOUSE WE CAN CREATE FOLDER OF INDICATORS AND THEN USE THEM IN STRATEGY
# strategies/momentum_strategy.py

from .base_strategy import BaseStrategy
from utils.indicators import calculate_moving_average

class MomentumStrategy(BaseStrategy):
    def __init__(self, short_window=50, long_window=200, **strategy_kwargs):
        super().__init__(**strategy_kwargs)
        self.short_window = short_window
        self.long_window = long_window

    def init(self):
        self.indicators['short_ma'] = calculate_moving_average(self.strategy_kwargs['data']['Close'], self.short_window)
        self.indicators['long_ma'] = calculate_moving_average(self.strategy_kwargs['data']['Close'], self.long_window)

    # Rest of the class remains the same

## INDICATOR FOR SUPPORT AND RESISTANCE LEVELS CALCULATIONS
# Example: Calculating Support and Resistance (Simple Example)

import pandas as pd

def calculate_support_resistance(data, window=20):
    """
    Calculate support and resistance levels using rolling min and max.

    Parameters:
        data (pd.DataFrame): DataFrame containing 'Close' prices.
        window (int): Number of periods to consider for calculating support and resistance.

    Returns:
        pd.DataFrame: Original DataFrame with added 'support' and 'resistance' columns.
    """
    data['support'] = data['Close'].rolling(window=window).min()
    data['resistance'] = data['Close'].rolling(window=window).max()
    return data

## INTIALIZING THE STRATEGY
from strategies import BreakoutStrategy

# Load and prepare data
btc_1m_data = data_manager.load_processed_data('BTCUSD', '1m')
btc_1m_data = calculate_support_resistance(btc_1m_data, window=20)

# Define strategy parameters
strategy_kwargs = {
    'data': btc_1m_data
}

# Instantiate the strategy
breakout_strategy = BreakoutStrategy(**strategy_kwargs)

# Initialize indicators
breakout_strategy.init()

## Integrating with Backtesting
from backtesting.backtesting import Backtesting

# Instantiate the backtesting engine with the strategy and data
backtest = Backtesting(strategy=breakout_strategy, data=btc_1m_data)

# Run the backtest
backtest.run()

# Generate report
backtest.report()

### #############Expected Output ######################
BUY signal generated at price 10500 based on breakout strategy
SELL signal generated at price 10200 based on breakout strategy


📌 Key Takeaways
- Separation of Concerns: Keep strategies focused on trading logic and backtesting focused on execution and management.
- Flexibility in Strategies: Design strategies to accept various parameters and emit detailed signals to facilitate future integrations.
- Reusability of Indicators: Encapsulate indicator calculations in utility functions to promote reuse across different strategies and projects.
- Preparation for Backtesting: Structure your strategies in a way that the backtesting engine can easily consume their signals and parameters.

+--------------------+          +---------------------+
|                    |          |                     |
|    Backtesting     |          |      Strategy       |
|                    |          |                     |
| - Uses strategy    |<>--------| - Implements logic  |
| - Executes trades  |          | - Generates signals |
| - Manages portfolio|          |                     |
| - Applies risk mgmt |          |                     |
+--------------------+          +---------------------+
           ^
           |
           |
+--------------------+
|                    |
|    Data Management |
|                    |
| - Loads data       |
| - Preprocesses data |
| - Provides data to |
|   Backtesting      |
+--------------------+


## LEARNINGS ON 17/10
Question:
If you instantiate a strategy without data, how is it using the processed data? Is it through the backtest it will provide then pass the data to the strategy to execute its logic?

- Yes, exactly. The BacktestRunner is responsible for supplying the necessary data to each strategy during the backtest execution. Here's how it works:
- Strategy Instantiation:

- When you instantiate a strategy (e.g., MomentumStrategy, BreakoutStrategy, MultiTimeframeStrategy), you do not directly pass the data to the constructor.
- Instead, you can pass any static parameters required by the strategy (like moving average windows, stop-loss percentages, etc.).

Data Provision During Backtest:

The BacktestRunner handles data provision based on whether the strategy is Single-TF or MTF.
For Single-TF Strategies, it passes only the primary timeframe data.
For MTF Strategies, it passes multiple timeframes as required by the strategy.


BacktestRunner (primary_tf='1m') 
        |
        |---> Strategy: MultiTimeframeStrategy (requires_multiple_timeframes=True)
                | 
                |---> Pass '1m' data as primary data to Backtest
                |---> Pass '1H' data as additional data via strategy_kwargs
                |
                |---> Strategy uses '1m' for trade execution and '1H' for signals
data_dict = {
    'BTCUSD': {
        '1m': DataFrame_for_1m,
        '1H': DataFrame_for_1H,
        '1D': DataFrame_for_1D
    }
}

BacktestRunner:
    strategies = [multi_tf_strategy]
    data_dict = processed_data
    primary_tf = '1m'
    
    Iterates over strategies:
        multi_tf_strategy:
            Iterates over assets:
                BTCUSD:
                    - Retrieves '1m' (primary_tf) and '1H' (additional_tf) data
                    - Initializes Backtest with '1m' data
                    - Passes '1H' data via strategy_kwargs


  How self.data is Set:

Initialization by backtesting.py: When the Backtest instance runs, it instantiates the strategy class and assigns the provided data (timeframes[primary_tf]) to self.data.
For MTF Strategies: Additional data (e.g., higher_tf_data) is passed via strategy_kwargs and accessed within the strategy.

BacktestRunner
    |
    |--- Retrieves primary_tf ('1m') and higher_tf ('1H') for MultiTimeframeStrategy
    |
    |--- Passes '1m' data to Backtest (self.data in strategy)
    |--- Passes '1H' data via strategy_kwargs
    |
MultiTimeframeStrategy
    |
    |--- init()
    |       |--- Uses strategy_kwargs['1H_data'] for higher_tf indicators
    |       |--- Uses self.data (primary_tf) for current_tf indicators
    |
    |--- next()
            |--- Determines trend based on higher_tf indicators
            |--- Generates signals based on current_tf indicators
            |--- Executes trades using self.data (primary_tf) prices





Accessing the Underlying DataFrame:

Before: self.data.Close returned a _Array.
After: df = self.data.df accesses the original pandas DataFrame.
Usage: df['Close'] is now a pandas Series, which supports .rolling() and .mean().



Start with Grid Search:

Reason: It's simple to implement and provides a comprehensive understanding of how different parameter combinations affect strategy performance.
Action: Utilize your existing bt.optimize() method with method='grid' to perform exhaustive parameter sweeps.
Implement Random Search:

Reason: More efficient than Grid Search, especially useful when dealing with multiple parameters or larger ranges.
Action: Modify your optimization calls to use method='random' and specify the number of random samples (n).


## 21 /10 MAIN.PY PAGE
# main.py

from backtest_framework.backtest.backtest_runner import BacktestRunner  # Updated import
from strategies.momentum_strategy import MomentumStrategy
from strategies.breakout_strategy import BreakoutMTFStrategy
from strategies.multi_tf_strategy import MultiTimeframeStrategy  # Corrected import
from data.data_manager import DataManager
from backtest_framework.backtest.results_analysis import ResultsAnalyzer  # Ensure this module is implemented
import sys
import logging

# Disable bytecode generation
sys.dont_write_bytecode = True

# Configure logging globally
logging.basicConfig(
    filename='backtesting.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filemode='w'  # Overwrite the log file each run; change to 'a' to append
)

def main():
    # Initialize DataManager and load data
    data_manager = DataManager(
        raw_data_path='C:/Users/IQRA/Desktop/Qafary Framework/data/raw',
        processed_data_path='C:/Users/IQRA/Desktop/Qafary Framework/data/processed'
    )
    processed_data = {}
    assets = ['BTCUSD']  # Example with multiple assets
    timeframes_needed = ['1m', '5m', '1H']  # Define all timeframes required by strategies

    for asset in assets:
        processed_data[asset] = {}
        for tf in timeframes_needed:
            df = data_manager.load_processed_data(asset, tf)
            if not df.empty:
                processed_data[asset][tf] = df
                print(f"Loaded data for {asset} at {tf} timeframe with {len(df)} records.")
            else:
                print(f"No data loaded for {asset} at {tf} timeframe.")

    # Set strategy-specific parameters by setting class attributes
    # 1. MomentumStrategy (STF) - Executes on '5m'
    # MomentumStrategy.short_window = 20
    # MomentumStrategy.long_window = 100
    # MomentumStrategy.primary_tf = '5m'  # Executes trades on 5-minute timeframe

    # 2. MultiTimeframeStrategy (MTF) - Uses '1m' and '1H'
    # MultiTimeframeStrategy.higher_tf_short_ma = 5
    # MultiTimeframeStrategy.higher_tf_long_ma = 10
    # MultiTimeframeStrategy.current_tf_short_ma = 3
    # MultiTimeframeStrategy.current_tf_long_ma = 7
    # MultiTimeframeStrategy.higher_tf = '1H'
    # MultiTimeframeStrategy.primary_tf = '5m'
    
    # 3. BreakoutMTFStrategy - Uses '1H' and '5m'
    BreakoutMTFStrategy.higher_tf_short_ma = 20
    BreakoutMTFStrategy.higher_tf_long_ma = 50
    BreakoutMTFStrategy.primary_tf = '5m'
    BreakoutMTFStrategy.higher_tf = '1H'
    BreakoutMTFStrategy.tp_percent = 7
    BreakoutMTFStrategy.sl_percent = 15
    # Initialize BacktestRunner with all strategy classes
    backtest_runner = BacktestRunner(
        strategies=[BreakoutMTFStrategy],
        data_dict=processed_data,
        transaction_costs=0.001,  # 0.1%
    )

    # Run backtests sequentially (set concurrent=True to enable multiprocessing)
    backtest_runner.run_backtests(concurrent=False)

    # Retrieve and analyze results
    results = backtest_runner.get_results()
    analyzer = ResultsAnalyzer(results, report_dir='REPORT')
    analyzer.display_summary()
    analyzer.save_summary_to_csv()

    # Plot Equity Curves and Generate Full Reports
    for asset in assets:
        # MomentumStrategy (STF)
        # strategy_key_stf = f"MomentumStrategy_{asset}"
        # analyzer.plot_equity_curve(strategy_key_stf)
        # analyzer.generate_full_report(strategy_key_stf, filename=f"{strategy_key_stf}_Report.html")
        # analyzer.generate_performance_metrics(strategy_key_stf)

        # # MultiTimeframeStrategy (MTF)
        # strategy_key_mtf = f"MultiTimeframeStrategy_{asset}"
        # analyzer.plot_equity_curve(strategy_key_mtf)
        # analyzer.generate_full_report(strategy_key_mtf, filename=f"{strategy_key_mtf}_Report.html")
        # analyzer.generate_performance_metrics(strategy_key_mtf)
        
        # BreakoutMTFStrategy
        strategy_key_breakout_mtf = f"BreakoutMTFStrategy_{asset}"
        analyzer.plot_equity_curve(strategy_key_breakout_mtf)
        analyzer.generate_full_report(strategy_key_breakout_mtf, filename=f"{strategy_key_breakout_mtf}_Report.html")
        analyzer.generate_performance_metrics(strategy_key_breakout_mtf)


if __name__ == "__main__":
    main()




## UPDATION OF MAIN.PY ACCORDING TO CHANGES WE DID ON OPTIMIZATIONS AND BACKTESTING  - 27/10
# main.py

from backtest_framework.backtest.backtest_runner import BacktestRunner
from strategies.breakout_strategy import BreakoutMTFStrategy
from data.data_manager import DataManager
from backtest_framework.backtest.results_analysis import ResultsAnalyzer
from optimization.grid_search_optimizer import GridSearchOptimizer
from optimization.random_search_optimizer import RandomSearchOptimizer
from optimization.sequential_optimizer import SequentialOptimizer
from optimization.optimization_analysis import OptimizationAnalyzer
import sys
import logging
import os
import pandas as pd

# Disable bytecode generation
sys.dont_write_bytecode = True

# Configure logging globally
logging.basicConfig(
    filename='backtesting.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filemode='w'  # Overwrite the log file each run; change to 'a' to append
)

def main():
    logger = logging.getLogger('Main')
    logger.info("Starting Qafary Framework Process.")
    
    # Initialize DataManager and load data
    data_manager = DataManager(
        raw_data_path='C:/Users/IQRA/Desktop/Qafary Framework/data/raw',
        processed_data_path='C:/Users/IQRA/Desktop/Qafary Framework/data/processed'
    )
    processed_data = {}
    assets = ['BTCUSD']  # Example with multiple assets
    timeframes_needed = ['1m', '5m', '1H']  # Define all timeframes required by strategies

    for asset in assets:
        processed_data[asset] = {}
        for tf in timeframes_needed:
            df = data_manager.load_processed_data(asset, tf)
            if not df.empty:
                processed_data[asset][tf] = df
                logger.info(f"Loaded data for {asset} at {tf} timeframe with {len(df)} records.")
            else:
                logger.warning(f"No data loaded for {asset} at {tf} timeframe.")
    
    # Set strategy-specific parameters by setting class attributes
    BreakoutMTFStrategy.higher_tf_short_ma = 20
    BreakoutMTFStrategy.higher_tf_long_ma = 50
    BreakoutMTFStrategy.primary_tf = '5m'
    BreakoutMTFStrategy.higher_tf = '1H'
    BreakoutMTFStrategy.tp_percent = 14  # Default value
    BreakoutMTFStrategy.sl_percent = 7   # Default value

    # Assume the strategy requires multiple timeframes
    BreakoutMTFStrategy.requires_multiple_timeframes = True

    # Initialize BacktestRunner with the strategy
    backtest_runner = BacktestRunner(
        strategies=[BreakoutMTFStrategy],
        data_dict=processed_data,
        transaction_costs=0.001,  # 0.1%
    )
    
    # Run Backtest Without Optimization
    logger.info("Running Backtest without Optimization.")
    backtest_runner.run_backtests(concurrent=False)
    
    # Retrieve and analyze results
    results = backtest_runner.get_results()
    analyzer = ResultsAnalyzer(results, report_dir='REPORT')
    analyzer.display_summary()
    analyzer.save_summary_to_csv()
    
    # Plot Equity Curves and Generate Full Reports
    for asset in assets:
        # BreakoutMTFStrategy
        strategy_key_breakout_mtf = f"BreakoutMTFStrategy_{asset}"
        analyzer.plot_equity_curve(strategy_key_breakout_mtf)
        analyzer.generate_full_report(strategy_key_breakout_mtf, filename=f"{strategy_key_breakout_mtf}_Report.html")
        analyzer.generate_performance_metrics(strategy_key_breakout_mtf)
    
    # Ask user if they want to run optimization
    user_choice = input("Do you want to run optimization? (yes/no): ").strip().lower()
    
    if user_choice in ['yes', 'y']:
        logger.info("User chose to run optimization.")
        
        # Ask user to select optimization method
        print("Select optimization method:")
        print("1. Grid Search")
        print("2. Random Search")
        print("3. Sequential Optimization")
        opt_choice = input("Enter the number of the optimization method you want to use: ").strip()
        
        # Assume single asset and primary timeframe for simplicity
        asset = assets[0]
        timeframe = BreakoutMTFStrategy.primary_tf
        data = processed_data[asset][timeframe]
        
        # Prepare higher timeframe data
        higher_tf = BreakoutMTFStrategy.higher_tf
        higher_tf_data = processed_data[asset].get(higher_tf)
        if higher_tf_data is None:
            logger.error(f"Higher timeframe data '{higher_tf}' not found for asset '{asset}'.")
            sys.exit(1)
        
        # Prepare strategy_kwargs
        strategy_kwargs = {'higher_tf_data': higher_tf_data}
        
        if opt_choice == '1':
            logger.info("User selected Grid Search Optimization.")
            optimizer = GridSearchOptimizer(
                backtest_runner,
                BreakoutMTFStrategy,
                data,
                processed_data[asset],
                logger=logger
            )
            
            # Define Parameter Ranges
            param_ranges = {
                'tp_percent': range(3, 15),
                'sl_percent': range(3, 15)
            }
            
            # Optional constraint
            constraint = lambda params: params['tp_percent'] > params['sl_percent']
            
            # Perform Grid Search Optimization with joblib
            best_result, df_results = optimizer.optimize(
                param_ranges=param_ranges,
                metric='Equity Final [$]',
                maximize=True,
                constraint=constraint,
                max_cores=-1  # Use all available CPU cores
            )
            
            # Display Best Parameters
            print("\nBest Parameters from Grid Search:")
            print(best_result)
            
            # Save Results
            results_file = os.path.join('optimization', 'grid_search', 'grid_search_results.csv')
            os.makedirs(os.path.dirname(results_file), exist_ok=True)
            df_results.to_csv(results_file, index=False)
            logger.info(f"Grid search results saved to {results_file}")
            
        elif opt_choice == '2':
            logger.info("User selected Random Search Optimization.")
            optimizer = RandomSearchOptimizer(
                backtest_runner,
                BreakoutMTFStrategy,
                data,
                processed_data[asset],
                logger=logger
            )
            
            # Define Parameter Distributions
            param_distributions = {
                'tp_percent': list(range(3, 15)),
                'sl_percent': list(range(3, 15))
            }
            
            # Optional constraint
            constraint = lambda params: params['tp_percent'] > params['sl_percent']
            
            # Perform Random Search Optimization with joblib
            n_iter = 20  # Number of random samples
            best_result, df_results = optimizer.optimize(
                param_distributions=param_distributions,
                n_iter=n_iter,
                metric='Equity Final [$]',
                maximize=True,
                constraint=constraint,
                max_cores=-1  # Use all available CPU cores
            )
            
            # Display Best Parameters
            if best_result is not None:
                print("\nBest Parameters from Random Search:")
                print(best_result)
                
                # Save Results
                results_file = os.path.join('optimization', 'random_search', 'random_search_results.csv')
                os.makedirs(os.path.dirname(results_file), exist_ok=True)
                df_results.to_csv(results_file, index=False)
                logger.info(f"Random search results saved to {results_file}")
            else:
                logger.warning("Random search optimization did not yield any results.")
                
        elif opt_choice == '3':
            logger.info("User selected Sequential Optimization.")
            optimizer = SequentialOptimizer(backtest_runner, logger=logger)
            
            # Define Parameter Grid for Phase 1
            param_grid_phase1 = {
                'tp_percent': range(3, 15, 1),  # Take-Profit: 3% to 14%
                'sl_percent': range(3, 15, 1),  # Stop-Loss: 3% to 14%
            }
            
            # Ensure that higher_tf_data is passed during optimization
            optimizer.strategy_kwargs = strategy_kwargs
            
            # Perform Phase 1 Optimization
            df_phase1 = optimizer.optimize_phase1(
                primary_metric='Equity Final [$]',
                param_grid=param_grid_phase1
            )
            
            # Display Best Parameters from Phase 1
            best_phase1 = df_phase1.loc[df_phase1['Primary Metric'].idxmax()]
            print("\nBest Parameters from Phase 1 (Maximize Equity Final [$]):")
            print(best_phase1[['tp_percent', 'sl_percent', 'Primary Metric']])
            
            # Save Best Parameters to Analysis Page (e.g., a CSV file)
            best_params_file = os.path.join('optimization', 'phase1', 'best_parameters_phase1.csv')
            os.makedirs(os.path.dirname(best_params_file), exist_ok=True)
            best_phase1[['tp_percent', 'sl_percent', 'Primary Metric']].to_csv(best_params_file, index=False)
            logger.info(f"Best Phase 1 parameters saved to {best_params_file}")
            
            # Define Secondary Metrics and Their Directions
            # Example: Minimize Drawdown and Maximize Sharpe Ratio
            secondary_metrics = [
                {'metric': 'Max Drawdown [%]', 'direction': 'minimize'},
                {'metric': 'Sharpe Ratio', 'direction': 'maximize'}
            ]
            
            # Define Parameter Refinement for Phase 2
            param_refinement_phase2 = {
                'top_n': 5,  # Number of top parameter sets to consider
                'refine_on': ['tp_percent', 'sl_percent'],  # Parameters to refine
                'refinement_step': 1,  # Step size for refining parameters
                'step': 1  # Step size within the refined range
            }
            
            # Perform Phase 2 Optimization for Each Secondary Metric
            df_phase2_list = []
            for sec_metric in secondary_metrics:
                df_phase2 = optimizer.optimize_phase2(
                    df_phase1=df_phase1,
                    secondary_metrics=[sec_metric],
                    param_refinement=param_refinement_phase2
                )
                df_phase2_list.append(df_phase2)
            
            # Concatenate Phase 2 results if multiple secondary metrics are optimized
            if len(df_phase2_list) > 1:
                df_phase2_combined = pd.concat(df_phase2_list, ignore_index=True)
            else:
                df_phase2_combined = df_phase2_list[0]
            
            # Display Best Parameters from Phase 2
            best_phase2 = df_phase2_combined.loc[df_phase2_combined['Secondary Metric'].idxmin()] if any(sec['direction'] == 'minimize' for sec in secondary_metrics) else df_phase2_combined.loc[df_phase2_combined['Secondary Metric'].idxmax()]
            print("\nBest Parameters from Phase 2 (Optimize Secondary Metrics):")
            print(best_phase2[['tp_percent', 'sl_percent', 'Secondary Metric']])
            
            # Save Best Parameters to Analysis Page (e.g., a CSV file)
            best_params_phase2_file = os.path.join('optimization', 'phase2', 'best_parameters_phase2.csv')
            os.makedirs(os.path.dirname(best_params_phase2_file), exist_ok=True)
            best_phase2[['tp_percent', 'sl_percent', 'Secondary Metric']].to_csv(best_params_phase2_file, index=False)
            logger.info(f"Best Phase 2 parameters saved to {best_params_phase2_file}")
            
            # Save Optimization Results and Generate Heatmaps
            optimizer.save_results(df_phase1, df_phase2_combined, 'optimization/REPORT')
            
            # Initialize OptimizationAnalyzer
            analyzer = OptimizationAnalyzer(logger=logger)
            
            # Generate Comprehensive Optimization Report
            analyzer.generate_report(df_phase1, df_phase2_combined, 'optimization/REPORT')
            
        else:
            logger.warning("Invalid optimization method selected. Process terminated.")
            print("Invalid selection. Please restart the program and select a valid optimization method.")
            sys.exit(1)
        
    else:
        logger.info("User chose not to run optimization. Process completed.")

    logger.info("Process completed successfully.")

if __name__ == "__main__":
    main()


