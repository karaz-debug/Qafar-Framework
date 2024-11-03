# utils/portfolio.py

import logging
from typing import Dict, Any, List
import pandas as pd
# utils/portfolio.py


class Portfolio:
    """
    The Portfolio class manages the trading account's state, including balance, positions,
    executing trades, and calculating performance metrics.
    """

    def __init__(self, initial_balance: float = 100000):
        """
        Initialize the Portfolio.

        Parameters:
            initial_balance (float): Starting capital for the portfolio.
        """
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.position = 0  # Number of units held
        self.entry_price = 0.0
        self.stop_loss = 0.0
        self.take_profit = 0.0
        self.trades = []  # List to record executed trades
        self.equity_curve = [initial_balance]
        logging.info(f"Portfolio initialized with balance: ${self.balance}")

    def execute_trade(self, signal: Dict[str, Any], price: float, strategy: Any):
        """
        Execute a trade based on the generated signal.

        Parameters:
            signal (Dict[str, Any]): Contains trade type, price, stop-loss, and take-profit.
            price (float): The price at which to execute the order.
            strategy (BaseStrategy): The strategy instance generating the signal.
        """
        try:
            trade_type = signal.get('type')
            stop_loss = signal.get('stop_loss')
            take_profit = signal.get('take_profit')

            if trade_type == 'buy' and self.position == 0:
                # Enter a long position
                self.position = self.balance / price
                self.entry_price = price
                self.stop_loss = stop_loss
                self.take_profit = take_profit
                logging.info(f"BUY executed at ${price}, Position size: {self.position}")
                self.trades.append({
                    'type': 'buy',
                    'price': price,
                    'position': self.position,
                    'stop_loss': self.stop_loss,
                    'take_profit': self.take_profit
                })

            elif trade_type == 'sell' and self.position > 0:
                # Exit the long position
                proceeds = self.position * price
                self.balance = proceeds
                logging.info(f"SELL executed at ${price}, Proceeds: ${proceeds}")
                self.trades.append({
                    'type': 'sell',
                    'price': price,
                    'position': self.position,
                    'stop_loss': self.stop_loss,
                    'take_profit': self.take_profit
                })
                self.position = 0
                self.entry_price = 0.0
                self.stop_loss = 0.0
                self.take_profit = 0.0

            # Update equity curve
            current_equity = self.balance + (self.position * price)
            self.equity_curve.append(current_equity)

        except Exception as e:
            logging.error(f"Error executing trade: {e}")

    def check_stop_loss_take_profit(self, current_price: float):
        """
        Check and execute stop-loss or take-profit orders based on the current price.

        Parameters:
            current_price (float): The latest market price.
        """
        try:
            if self.position > 0:
                if current_price <= self.stop_loss:
                    # Trigger stop-loss
                    logging.info(f"Stop-Loss triggered at ${current_price}")
                    self.execute_trade({
                        'type': 'sell',
                        'price': current_price,
                        'stop_loss': self.stop_loss,
                        'take_profit': self.take_profit
                    }, current_price, None)

                elif current_price >= self.take_profit:
                    # Trigger take-profit
                    logging.info(f"Take-Profit triggered at ${current_price}")
                    self.execute_trade({
                        'type': 'sell',
                        'price': current_price,
                        'stop_loss': self.stop_loss,
                        'take_profit': self.take_profit
                    }, current_price, None)

        except Exception as e:
            logging.error(f"Error checking stop-loss/take-profit: {e}")

    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Calculate and return performance metrics.

        Returns:
            Dict[str, Any]: Performance metrics including final equity, return, drawdown, etc.
        """
        try:
            final_equity = self.equity_curve[-1]
            total_return = (final_equity - self.initial_balance) / self.initial_balance

            # Calculate drawdown
            equity_series = pd.Series(self.equity_curve)
            rolling_max = equity_series.cummax()
            drawdown = (rolling_max - equity_series) / rolling_max
            max_drawdown = drawdown.max()

            # Calculate number of trades
            num_trades = len(self.trades)

            performance = {
                'Initial Balance': self.initial_balance,
                'Final Equity': final_equity,
                'Total Return (%)': round(total_return * 100, 2),
                'Max Drawdown (%)': round(max_drawdown * 100, 2),
                'Number of Trades': num_trades,
                'equity_curve': self.equity_curve  # Include equity curve for analysis
            }

            logging.info(f"Performance Metrics: {performance}")

            return performance

        except Exception as e:
            logging.error(f"Error calculating performance metrics: {e}")
            return {}
