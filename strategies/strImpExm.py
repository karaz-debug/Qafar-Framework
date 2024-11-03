# main.py

from data.data_manager import DataManager
from strategies import BreakoutStrategy

def main():
    # Initialize DataManager
    data_manager = DataManager()
    
    # Load and prepare data for BTCUSD at 1m timeframe
    btc_1m_data = data_manager.load_processed_data('BTCUSD', '1m')
    
    # Ensure 'support' and 'resistance' columns are present
    # Example: Calculating support and resistance if not already done
    # if 'support' not in btc_1m_data.columns or 'resistance' not in btc_1m_data.columns:
        # btc_1m_data = calculate_support_resistance(btc_1m_data, window=20)  # Define this function in utils
    
    # Define strategy parameters
    strategy_kwargs = {
        'data': btc_1m_data
    }
    
    # Instantiate the BreakoutStrategy
    breakout_strategy = BreakoutStrategy(stop_loss=0.02, take_profit=0.04, **strategy_kwargs)
    
    # Initialize indicators
    breakout_strategy.init()
    
    # At this point, you can print indicators to verify
    print(breakout_strategy.indicators)
    
    # Placeholder for backtesting integration
    # Once backtesting is implemented, pass the strategy to the backtest engine
    # backtest = Backtesting(strategy=breakout_strategy, data=btc_1m_data)
    # backtest.run()
    # backtest.report()

if __name__ == "__main__":
    main()
