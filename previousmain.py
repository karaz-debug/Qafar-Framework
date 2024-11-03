# main.py

from backtest_framework.backtest.backtest_runner import BacktestRunner
from strategies.breakout_strategy import BreakoutMTFStrategy
from strategies.momentum_strategy import MomentumStrategy
from strategies.multi_tf_strategy import MultiTimeframeStrategy
# Import other strategy classes as needed
from data.data_manager import DataManager
from backtest_framework.backtest.results_analysis import ResultsAnalyzer
from optimization.grid_search_optimizer import GridSearchOptimizer
from optimization.random_search_optimizer import RandomSearchOptimizer
from optimization.sequential_optimizer import SequentialOptimizer
from optimization.optimization_analysis import OptimizationAnalyzer
from optimization.monte_carlo_optimizer import MonteCarloOptimizer
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

    # Define available assets, timeframes, and strategies
    available_assets = ['BTCUSD', 'ETHUSD', 'LTCUSD']  # Update with your available assets
    available_timeframes = ['1m', '5m', '15m', '1H', '4H', '1D']  # Update as needed
    available_strategies = {
        'BreakoutMTFStrategy': BreakoutMTFStrategy,
        'MomentumStrategy' : MomentumStrategy,
        'MultiTimeframeStrategy' : MultiTimeframeStrategy
        # Add other strategies here
        # 'AnotherStrategy': AnotherStrategyClass,
    }

    # Prompt user to select asset
    print("Available assets:")
    for i, asset in enumerate(available_assets, 1):
        print(f"{i}. {asset}")
    while True:
        try:
            asset_choice = int(input("Enter the number of the asset you want to backtest: ").strip())
            if 1 <= asset_choice <= len(available_assets):
                selected_asset = available_assets[asset_choice - 1]
                break
            else:
                print("Invalid selection. Please choose a valid asset number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    logger.info(f"User selected asset: {selected_asset}")

    # Prompt user to select timeframes
    print("\nAvailable timeframes:")
    for i, tf in enumerate(available_timeframes, 1):
        print(f"{i}. {tf}")
    timeframes_needed = []
    while True:
        tf_choice = input("Enter the number of the timeframe you want to add (or 'done' to finish): ").strip()
        if tf_choice.lower() == 'done':
            if timeframes_needed:
                break
            else:
                print("You must select at least one timeframe.")
                continue
        try:
            tf_index = int(tf_choice) - 1
            if 0 <= tf_index < len(available_timeframes):
                selected_tf = available_timeframes[tf_index]
                if selected_tf not in timeframes_needed:
                    timeframes_needed.append(selected_tf)
                    print(f"Added timeframe: {selected_tf}")
                else:
                    print("Timeframe already selected.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a number or 'done'.")

    logger.info(f"User selected timeframes: {timeframes_needed}")

    # Prompt user to select strategy
    print("\nAvailable strategies:")
    for i, strategy_name in enumerate(available_strategies.keys(), 1):
        print(f"{i}. {strategy_name}")
    while True:
        try:
            strategy_choice = int(input("Enter the number of the strategy you want to use: ").strip())
            if 1 <= strategy_choice <= len(available_strategies):
                selected_strategy_name = list(available_strategies.keys())[strategy_choice - 1]
                selected_strategy_class = available_strategies[selected_strategy_name]
                break
            else:
                print("Invalid selection. Please choose a valid strategy number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    logger.info(f"User selected strategy: {selected_strategy_name}")

    # Initialize DataManager and load data
    data_manager = DataManager(
        raw_data_path='C:/Users/IQRA/Desktop/Qafary Framework/data/raw',
        processed_data_path='C:/Users/IQRA/Desktop/Qafary Framework/data/processed'
    )
    processed_data = {}
    assets = [selected_asset]

    # Load data for selected asset and timeframes
    processed_data[selected_asset] = {}
    for tf in timeframes_needed:
        df = data_manager.load_processed_data(selected_asset, tf)
        if not df.empty:
            processed_data[selected_asset][tf] = df
            logger.info(f"Loaded data for {selected_asset} at {tf} timeframe with {len(df)} records.")
        else:
            logger.warning(f"No data loaded for {selected_asset} at {tf} timeframe.")

    # Set strategy-specific parameters dynamically
    strategy_params = getattr(selected_strategy_class, 'strategy_params', {})
    for param_name, param_info in strategy_params.items():
        prompt = param_info.get('prompt', f"Enter value for {param_name}: ")
        default = param_info.get('default')
        param_type = param_info.get('type', str)
        while True:
            user_input = input(prompt).strip()
            if user_input == '':
                value = default
                break
            else:
                try:
                    if param_type == bool:
                        if user_input.lower() in ['true', 'yes', '1']:
                            value = True
                        elif user_input.lower() in ['false', 'no', '0']:
                            value = False
                        else:
                            raise ValueError
                    else:
                        value = param_type(user_input)
                    break
                except ValueError:
                    print(f"Invalid input. Please enter a {param_type.__name__}.")
        setattr(selected_strategy_class, param_name, value)
        logger.info(f"Set {param_name} to {value}")

    # Initialize BacktestRunner with the selected strategy
    backtest_runner = BacktestRunner(
        strategies=[selected_strategy_class],
        data_dict=processed_data,
        transaction_costs=0.002,  # 0.1%
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
        # For the selected strategy
        strategy_key = f"{selected_strategy_name}_{asset}"
        analyzer.plot_equity_curve(strategy_key)
        analyzer.generate_full_report(strategy_key, filename=f"{strategy_key}_Report.html")
        analyzer.generate_performance_metrics(strategy_key)

    # Ask user if they want to run optimization
    user_choice = input("\nDo you want to run optimization? (yes/no): ").strip().lower()

    if user_choice in ['yes', 'y']:
        logger.info("User chose to run optimization.")

        # Ask user to select optimization method
        print("\nSelect optimization method:")
        print("1. Grid Search")
        print("2. Random Search")
        print("3. Sequential Optimization")
        print("4. Monte Carlo Simulation")  
        while True:
            opt_choice = input("Enter the number of the optimization method you want to use: ").strip()
            if opt_choice in ['1', '2', '3', '4']:
                break
            else:
                print("Invalid selection. Please enter 1, 2, or 3.")

        # Assume single asset and primary timeframe for simplicity
        asset = selected_asset
        timeframe = getattr(selected_strategy_class, 'primary_tf', None)
        if timeframe is None:
            print("Error: Strategy does not have a primary_tf attribute set.")
            logger.error("Strategy does not have a primary_tf attribute set.")
            sys.exit(1)
        data = processed_data[asset][timeframe]

        # Prepare higher timeframe data if needed
        higher_tf_data = None
        if getattr(selected_strategy_class, 'requires_multiple_timeframes', False):
            higher_tf = getattr(selected_strategy_class, 'higher_tf', None)
            if higher_tf is None:
                print("Error: Strategy requires higher_tf attribute but it's not set.")
                logger.error("Strategy requires higher_tf attribute but it's not set.")
                sys.exit(1)
            higher_tf_data = processed_data[asset].get(higher_tf)
            if higher_tf_data is None:
                logger.error(f"Higher timeframe data '{higher_tf}' not found for asset '{asset}'.")
                sys.exit(1)

        # Prepare strategy_kwargs
        strategy_kwargs = {}
        if higher_tf_data is not None:
            strategy_kwargs['higher_tf_data'] = higher_tf_data

        # Get optimizable parameters from strategy
        optimizable_params = getattr(selected_strategy_class, 'optimizable_params', [])
        if not optimizable_params:
            print("No optimizable parameters defined for this strategy.")
            logger.warning("No optimizable parameters defined for this strategy.")
            sys.exit(1)

        # Prompt user for parameter ranges or distributions
        print("\nEnter parameter ranges for optimization:")
        param_inputs = {}
        for param in optimizable_params:
            param_type = strategy_params.get(param, {}).get('type', float)
            while True:
                range_input = input(f"Enter range for {param} (e.g., start,stop,step): ").strip()
                try:
                    start_str, stop_str, step_str = [s.strip() for s in range_input.split(',')]
                    start = param_type(start_str)
                    stop = param_type(stop_str)
                    step = param_type(step_str)
                    param_inputs[param] = (start, stop, step)
                    break
                except ValueError:
                    print(f"Invalid input. Please enter start, stop, and step values separated by commas for {param}.")
                    continue

        # Optional constraint
        constraint = None
        if len(optimizable_params) >= 2:
            print("\nDo you want to set a constraint on the parameters? (yes/no)")
            constraint_choice = input().strip().lower()
            if constraint_choice in ['yes', 'y']:
                print("Enter constraint as a Python expression involving the parameters (e.g., tp_percent > sl_percent):")
                constraint_expr = input().strip()
                def constraint(params):
                    return eval(constraint_expr, {}, params)

        if opt_choice == '1':
            logger.info("User selected Grid Search Optimization.")
            optimizer = GridSearchOptimizer(
                backtest_runner,
                selected_strategy_class,
                data,
                processed_data[asset],
                logger=logger
            )

            # Define Parameter Ranges
            param_ranges = {}
            for param, (start, stop, step) in param_inputs.items():
                if isinstance(start, int) and isinstance(step, int):
                    param_ranges[param] = range(int(start), int(stop)+1, int(step))
                else:
                    param_ranges[param] = [start + i * step for i in range(int((stop - start) / step) + 1)]

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
                selected_strategy_class,
                data,
                processed_data[asset],
                logger=logger
            )

            # Define Parameter Distributions
            param_distributions = {}
            for param, (start, stop, step) in param_inputs.items():
                if isinstance(start, int) and isinstance(step, int):
                    param_distributions[param] = list(range(int(start), int(stop)+1, int(step)))
                else:
                    param_distributions[param] = [start + i * step for i in range(int((stop - start) / step) + 1)]

            # Prompt for number of iterations
            while True:
                n_iter_input = input("Enter the number of random samples to perform: ").strip()
                try:
                    n_iter = int(n_iter_input)
                    break
                except ValueError:
                    print("Invalid input. Please enter an integer value.")
                    continue

            # Perform Random Search Optimization with joblib
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
            param_grid_phase1 = {}
            for param, (start, stop, step) in param_inputs.items():
                if isinstance(start, int) and isinstance(step, int):
                    param_grid_phase1[param] = range(int(start), int(stop)+1, int(step))
                else:
                    param_grid_phase1[param] = [start + i * step for i in range(int((stop - start) / step) + 1)]

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
            print(best_phase1)

            # Save Best Parameters to Analysis Page (e.g., a CSV file)
            best_params_file = os.path.join('optimization', 'phase1', 'best_parameters_phase1.csv')
            os.makedirs(os.path.dirname(best_params_file), exist_ok=True)
            best_phase1.to_csv(best_params_file, index=False)
            logger.info(f"Best Phase 1 parameters saved to {best_params_file}")

            # Define Secondary Metrics and Their Directions
            # Prompt user for secondary metrics
            secondary_metrics = []
            print("\nEnter secondary metrics to optimize (e.g., 'Sharpe Ratio', 'Max Drawdown [%]'), or 'done' to finish:")
            while True:
                metric_input = input("Enter metric name (or 'done'): ").strip()
                if metric_input.lower() == 'done':
                    if secondary_metrics:
                        break
                    else:
                        print("You must enter at least one secondary metric.")
                        continue
                direction = input("Do you want to maximize or minimize this metric? (maximize/minimize): ").strip().lower()
                if direction in ['maximize', 'minimize']:
                    secondary_metrics.append({'metric': metric_input, 'direction': direction})
                else:
                    print("Invalid input. Please enter 'maximize' or 'minimize'.")

            # Define Parameter Refinement for Phase 2
            param_refinement_phase2 = {
                'top_n': 5,  # Number of top parameter sets to consider
                'refine_on': list(param_grid_phase1.keys()),  # Parameters to refine
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
            best_phase2 = None
            for sec_metric in secondary_metrics:
                metric_name = sec_metric['metric']
                if sec_metric['direction'] == 'minimize':
                    best_phase2 = df_phase2_combined.loc[df_phase2_combined[metric_name].idxmin()]
                else:
                    best_phase2 = df_phase2_combined.loc[df_phase2_combined[metric_name].idxmax()]
                print(f"\nBest Parameters from Phase 2 (Optimize {metric_name}):")
                print(best_phase2)

            # Save Best Parameters to Analysis Page (e.g., a CSV file)
            best_params_phase2_file = os.path.join('optimization', 'phase2', 'best_parameters_phase2.csv')
            os.makedirs(os.path.dirname(best_params_phase2_file), exist_ok=True)
            best_phase2.to_csv(best_params_phase2_file, index=False)
            logger.info(f"Best Phase 2 parameters saved to {best_params_phase2_file}")

            # Save Optimization Results and Generate Heatmaps
            optimizer.save_results(df_phase1, df_phase2_combined, 'optimization/REPORT')

            # Initialize OptimizationAnalyzer
            analyzer = OptimizationAnalyzer(logger=logger)

            # Generate Comprehensive Optimization Report
            analyzer.generate_report(df_phase1, df_phase2_combined, 'optimization/REPORT')
        
        elif opt_choice == '4':
            logger.info("User selected Monte Carlo Optimization.")
            optimizer = MonteCarloOptimizer(
                backtest_runner,
                selected_strategy_class,
                asset,  # Pass the asset name
                data,
                processed_data[asset],
                logger=logger
            )

            # Define Parameter Ranges
            print("\nEnter parameter ranges for Monte Carlo Optimization:")
            param_ranges = {}
            for param in optimizable_params:
                param_type = strategy_params.get(param, {}).get('type', float)
                while True:
                    range_input = input(f"Enter low and high values for {param} (e.g., low,high): ").strip()
                    try:
                        low_str, high_str = [s.strip() for s in range_input.split(',')]
                        low = param_type(low_str)
                        high = param_type(high_str)
                        param_ranges[param] = (low, high)
                        break
                    except ValueError:
                        print(f"Invalid input. Please enter low and high values separated by a comma for {param}.")
                        continue

            # Prompt for number of simulations
            while True:
                n_simulations_input = input("Enter the number of simulations to perform: ").strip()
                try:
                    n_simulations = int(n_simulations_input)
                    break
                except ValueError:
                    print("Invalid input. Please enter an integer value.")
                    continue

            # Prompt whether to perturb data
            perturb_data_input = input("Do you want to perturb data in simulations? (yes/no): ").strip().lower()
            perturb_data = perturb_data_input in ['yes', 'y']

            # Perform Monte Carlo Optimization
            best_result, df_results = optimizer.optimize(
                param_ranges=param_ranges,
                n_simulations=n_simulations,
                perturb_data=perturb_data,
                max_cores=-1
            )

            if best_result is not None:
                # Display Best Parameters
                print("\nBest Parameters from Monte Carlo Optimization:")
                print(best_result)

                # Save Results
                results_file = os.path.join('optimization', 'monte_carlo', 'monte_carlo_results.csv')
                os.makedirs(os.path.dirname(results_file), exist_ok=True)
                df_results.to_csv(results_file, index=False)
                logger.info(f"Monte Carlo results saved to {results_file}")
            else:
                print("Monte Carlo Optimization failed. No successful simulations.")
                logger.warning("Monte Carlo Optimization failed. No successful simulations.")



        else:
            logger.warning("Invalid optimization method selected. Process terminated.")
            print("Invalid selection. Please restart the program and select a valid optimization method.")
            sys.exit(1)

    else:
        logger.info("User chose not to run optimization. Process completed.")

    logger.info("Process completed successfully.")

if __name__ == "__main__":
    main()
    
    
    