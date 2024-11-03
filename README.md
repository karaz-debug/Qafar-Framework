# Algo Trading Framework (Qafary Framework)


**Algo Trading Framework (Qafary Framework)** is a modular, scalable, and efficient algorithmic trading platform designed to  backtest, and optimize trading strategies with different need in terms of timeframes, and comprehensive reporting tools, this framework empowers traders and developers to backtest and optimize  their trading strategies in order to find best paramters to play with in the live market 

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [System Architecture](#system-architecture)
5. [Project File Structure](#project-file-structure)
6. [Detailed Component Breakdown](#detailed-component-breakdown)
   - [A. Data Management (data/)](#a-data-management-data)
   - [B. Strategies (strategies/)](#b-strategies-strategies)
   - [C. Backtesting (backtesting/)](#c-backtesting-backtesting)
   - [D. Optimization (optimization/)](#d-optimization-optimization)
   - [E. Utilities (utils/)](#e-utilities-utils)
   - [F. Testing (tests/)](#f-testing-tests)
7. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
8. [Usage](#usage)
9. [CLI Implementation](#cli-implementation)
10. [Reporting & Visualization](#reporting--visualization)
11. [Contributing](#contributing)
12. [Testing](#testing)
13. [Deployment](#deployment)
14. [Documentation](#documentation)
15. [License](#license)
16. [Contact](#contact)

---

## Project Overview

The **Algo Trading Framework (Qafary Framework)** is engineered to facilitate the development, testing, and optimization of trading strategies across various assets and timeframes.The framework offers a unified platform for executing automated trades, conducting rigorous backtests, and fine-tuning strategies to achieve optimal performance.

---

## Features

- **Data Management:** Automated loading, cleaning, resampling, and caching of high-frequency market data.
- **Strategy Development:** Modular support for single-timeframe and multi-timeframe trading strategies.
- **Backtesting Engine:** Robust system for executing strategies, managing portfolios, and applying risk management rules.
- **Optimization Module:** Comprehensive optimization techniques including Grid Search, Random Search, Sequential Optimization, Monte Carlo Simulation, and Genetic Algorithms.
- **Reporting & Visualization:** Generates detailed backtest reports with performance metrics, equity curves, and trade summaries.
- **Command-Line Interface (CLI):** Interactive CLI for easy selection of assets, timeframes, strategies, and optimization methods.
- **Testing Framework:** Extensive unit and integration tests to ensure reliability and correctness.
- **Scalable Architecture:** Designed to handle multiple assets and timeframes concurrently.
- **Version Control:** Managed with Git and hosted on GitHub for collaboration and version tracking.

---

## Technology Stack

- **Programming Language:** Python
- **Libraries & Frameworks:**
  - **Data Handling:** Pandas, NumPy
  - **Backtesting:** Backtesting.py
  - **Optimization:** Joblib, SciPy
  - **CLI Development:** Click or argparse
  - **Reporting:** Matplotlib, Seaborn
- **Version Control:** Git, GitHub
- **Testing:** PyTest
- **Documentation:** Markdown
- **Others:** OS, Logging, Configuration Management

---

## System Architecture

The **Qafary Framework** follows a modular architecture, separating concerns across different components to enhance maintainability and scalability. The core components include:

1. **Data Management:** Handles all data-related operations, ensuring data integrity and availability for strategies.
2. **Strategies:** Encapsulates trading logic, supporting both single and multi-timeframe strategies.
3. **Backtesting Engine:** Executes strategies against historical data, simulating trades and recording performance.
4. **Optimization Module:** Fine-tunes strategy parameters to maximize performance metrics.
5. **Utilities:** Provides common functionalities like logging, configuration management, and helper functions.
6. **Testing Framework:** Ensures all components function as intended through rigorous testing.

For a detailed overview, refer to the [Architecture Documentation](./docs/architecture.md).

---

## Project File Structure

Organizing your project directory effectively is crucial. Here's the recommended structure tailored to your requirements:

Qafary_Framework/ ├── data/ │ ├── raw/ │ │ └── [Asset]/ # e.g., BTCUSD/ │ │ └── BTCUSDT_1m.csv # 1-minute data │ ├── processed/ │ │ └── [Asset]/ # e.g., BTCUSD/ │ │ ├── BTCUSDT_1m_processed.csv │ │ ├── BTCUSDT_1H_processed.csv │ │ └── BTCUSDT_1D_processed.csv │ └── data_manager.py ├── strategies/ │ ├── init.py │ ├── base_strategy.py │ ├── momentum_strategy.py │ ├── multi_tf_strategy.py │ └── breakout_mtf_strategy.py ├── backtesting/ │ ├── init.py │ ├── backtest_runner.py │ └── results_analysis.py ├── optimization/ │ ├── init.py │ ├── optimizer.py │ ├── alpha_decay.py │ ├── monte_carlo.py │ └── genetic_algorithm.py ├── utils/ │ ├── init.py │ ├── logger.py │ ├── config.py │ └── helpers.py ├── tests/ │ ├── test_data_manager.py │ ├── test_backtest_runner.py │ └── test_optimizer.py ├── reports/ │ ├── [StrategyName]_Report.html │ ├── [StrategyName]_equity_curve.png │ └── backtest_summary.csv ├── main.py ├── requirements.txt └── README.md

markdown
Copy code

---

## Detailed Component Breakdown

### A. Data Management (`data/`)

**Purpose:** Handle all data-related operations, including loading, preprocessing, resampling, and caching to avoid redundant processing.

#### i. Folder Structure

- **`raw/`**: Contains unprocessed high-frequency data for each asset in separate subfolders.
  - *Example:*
    ```
    data/raw/EURUSD/EURUSD_minute.csv
    data/raw/GBPUSD/GBPUSD_minute.csv
    ```
- **`processed/`**: Stores processed data at various timeframes for each asset.
  - *Example:*
    ```
    data/processed/EURUSD/EURUSD_minute_processed.csv
    data/processed/EURUSD/EURUSD_1H_processed.csv
    data/processed/EURUSD/EURUSD_1D_processed.csv
    ```
- **`data_manager.py`**: Core module for data operations.

#### ii. `data_manager.py` Features

- **Loading Raw Data:**
  - Automatically detects and loads raw data files from the `raw/` directory.
  - Supports multiple assets by scanning subdirectories.

- **Preprocessing:**
  - Cleans data (handles missing values, sorts by date).
  - Ensures consistency in data formats across different assets.

- **Resampling:**
  - Converts high-frequency data (e.g., 1-minute) to lower timeframes (e.g., 1-hour, 1-day) using efficient resampling methods.
  - Implements a caching mechanism to check if a processed file already exists before resampling, saving computational resources.

- **Saving and Loading Processed Data:**
  - Saves processed and resampled data into the `processed/` directory.
  - Loads processed data for backtesting and optimization.

- **Batch Processing:**
  - Handles multiple assets and their corresponding timeframes in a single operation.
  - Ensures scalability as more assets are added.

#### iii. Output

- **Processed Data Files:** Ready-to-use CSV files for each asset at various timeframes, stored in the `data/processed/` directory.
- **Logs:** Records of data processing steps, errors, and statuses for debugging and auditing.

#### iv. Resources

- **Pandas Resampling Documentation**
- **Python `os` Module for File Operations**

---

### B. Strategies (`strategies/`)

**Purpose:** Define various trading strategies, both single-timeframe and multi-timeframe, each encapsulated in its own module for modularity and reusability.

#### i. Folder Structure

- **`__init__.py`**: Makes the directory a Python package.
- **`base_strategy.py`**: Abstract base class defining the structure and shared functionalities for all strategies.
- **Strategy Modules**: Each strategy (e.g., Momentum, BreakoutMTF) has its own Python file.

#### ii. `base_strategy.py` Features

- **Abstract Methods:**
  - `init()`: Initialize indicators and variables.
  - `next()`: Define the trading logic, to be implemented by derived classes.

- **Attributes:**
  - `requires_multiple_timeframes`: Boolean indicating if the strategy is multi-timeframe.

#### iii. Individual Strategy Modules

- **Single-Timeframe Strategies (e.g., `momentum_strategy.py`):**
  - Inherit from `BaseStrategy`.
  - Implement `init()` and `next()` methods.
  - Define strategy-specific parameters and parameter bounds for optimization.

- **Multi-Timeframe Strategies (e.g., `breakout_mtf_strategy.py`):**
  - Inherit from `BaseStrategy`.
  - Set `requires_multiple_timeframes = True`.
  - Access multiple dataframes (e.g., hourly and daily) via strategy keyword arguments.
  - Implement `init()` and `next()` using indicators from multiple timeframes.

#### iv. Output

- **Strategy Classes:** Ready-to-use classes that can be instantiated and passed to the backtesting module.

#### v. Resources

- **Object-Oriented Programming in Python**
- **Backtesting.py Documentation**

---

### C. Backtesting (`backtesting/`)

**Purpose:** Execute backtests for different strategies, handling both single-timeframe and multi-timeframe strategies, and analyze results.

#### i. Folder Structure

- **`__init__.py`**: Makes the directory a Python package.
- **`backtest_runner.py`**: Core module to run backtests.
- **`results_analysis.py`**: Module to analyze and visualize backtest results.

#### ii. `backtest_runner.py` Features

- **Initialization:**
  - Accepts a `data_dict` containing processed data for each asset and timeframe.
  - Determines if the strategy requires multiple timeframes.

- **Running Backtests:**
  - **For Single-Timeframe Strategies:**
    - Use only the primary timeframe data.
  - **For Multi-Timeframe Strategies:**
    - Pass the entire `data_dict` to the strategy via `strategy_kwargs`.
    - Ensure that the `Backtest` instance is correctly configured based on the strategy type.

- **Handling Multiple Assets:**
  - Iterates through each asset and executes backtests individually or concurrently, depending on design preferences.

- **Result Storage:**
  - Stores backtest results for further analysis.

#### iii. `results_analysis.py` Features

- **Performance Metrics:**
  - Calculates and displays key metrics like Equity Final, Sharpe Ratio, Drawdown, etc.

- **Visualization:**
  - Plots equity curves, drawdown charts, and other relevant visualizations for performance assessment.

- **Reporting:**
  - Generates summary reports consolidating results from multiple backtests.

#### iv. Output

- **Backtest Results:** Metrics and visualizations showcasing strategy performance.
- **Logs:** Records of backtest execution steps and any errors encountered.

#### v. Resources

- **Backtesting.py Documentation**
- **Matplotlib for Plotting**

---

### D. Optimization (`optimization/`)

**Purpose:** Fine-tune strategy parameters to maximize performance metrics through various optimization techniques.

#### i. Folder Structure

- **`__init__.py`**: Makes the directory a Python package.
- **`optimizer.py`**: Core module handling optimization processes.
- **`alpha_decay.py`**: Module for Alpha Decay Optimization.
- **`monte_carlo.py`**: Module for Monte Carlo Optimization.
- **`genetic_algorithm.py`**: Module for Genetic Algorithm Optimization.

#### ii. `optimizer.py` Features

- **Optimization Methods:**
  - **Grid Search:** Exhaustively searches through a specified subset of hyperparameters.
  - **Random Search:** Randomly samples parameters, often faster and more efficient than grid search.
  - **Sequential Optimization:** Sequentially optimizes primary and secondary objectives to manage conflicting goals.

- **Parameter Range Definition:**
  - Allows users to define parameter ranges and constraints for optimization.

- **Integration with Backtesting:**
  - Seamlessly integrates with the backtesting engine to evaluate different parameter sets.

#### iii. `monte_carlo.py` Features

- **Monte Carlo Simulation:**
  - Runs multiple simulations with random variations in parameters and market data to assess strategy robustness.

#### iv. `alpha_decay.py` Features

- **Alpha Decay Analysis:**
  - Analyzes the decay of alpha (strategy's edge) over time to optimize timing-related parameters.

#### v. `genetic_algorithm.py` Features

- **Genetic Algorithms:**
  - Implements evolutionary algorithms to optimize strategy parameters through selection, crossover, and mutation.

#### vi. Output

- **Optimized Parameters:** Best-performing parameter sets based on defined objectives.
- **Optimization Reports:** Detailed reports outlining optimization results and performance metrics.

#### vii. Resources

- **SciPy Optimization Documentation**
- **Genetic Algorithms in Python**

---

### E. Utilities (`utils/`)

**Purpose:** Provide common functionalities like logging, configuration management, and helper functions to support other modules.

#### i. Folder Structure

- **`__init__.py`**: Makes the directory a Python package.
- **`logger.py`**: Configures and manages logging across the framework.
- **`config.py`**: Handles configuration settings and parameter loading.
- **`helpers.py`**: Contains utility functions used by multiple modules.

#### ii. `logger.py` Features

- **Logging Setup:**
  - Configures logging levels, formats, and handlers.
  - Ensures consistent logging across all modules.

- **Custom Loggers:**
  - Provides named loggers for different components (e.g., DataManager, Strategy, BacktestRunner).

#### iii. `config.py` Features

- **Configuration Management:**
  - Loads configuration files (e.g., YAML, JSON) for setting parameters.
  - Provides interfaces to access configuration settings.

#### iv. `helpers.py` Features

- **Utility Functions:**
  - Data validation and cleaning functions.
  - File and directory operations.
  - Statistical calculations and other common utilities.

#### v. Output

- **Centralized Utilities:** Streamlines common tasks, reducing code redundancy.

#### vi. Resources

- **Python Logging Module Documentation**
- **Python Configuration Management**

---

### F. Testing (`tests/`)

**Purpose:** Ensure all components function correctly through rigorous unit and integration testing.

#### i. Folder Structure

- **`__init__.py`**: Makes the directory a Python package.
- **`test_data_manager.py`**: Tests for the Data Management module.
- **`test_backtest_runner.py`**: Tests for the Backtesting module.
- **`test_optimizer.py`**: Tests for the Optimization module.

#### ii. Testing Framework

- **PyTest:**
  - Utilizes PyTest for writing and executing tests.
  - Supports fixtures, parameterized testing, and comprehensive reporting.

#### iii. Test Coverage

- **Unit Tests:**
  - Verify individual functions and methods behave as expected.
  
- **Integration Tests:**
  - Ensure different modules interact seamlessly.
  
- **Edge Case Handling:**
  - Tests handle unexpected inputs and scenarios gracefully.

#### iv. Output

- **Test Reports:** Detailed results of test executions, highlighting passed and failed tests.
- **Code Quality Assurance:** Ensures reliability and robustness of the framework.

#### v. Resources

- **PyTest Documentation**
- **Test-Driven Development (TDD) Best Practices**

---

## Getting Started

### Prerequisites

- **Python 3.8+**
- **Git**
- **Pandas**
- **NumPy**
- **Backtesting.py**
- **Joblib**
- **SciPy**
- **Matplotlib**
- **Seaborn**
- **PyTest**

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/automated-trading-system.git
   cd automated-trading-system
Set Up Python Environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
Configure Environment Variables:

Create a .env file in the root directory.
Populate it with necessary configurations like data paths, strategy parameters, and logging settings.
Initialize the Database:

(If applicable) Set up any required databases or data storage solutions.
Run Tests to Verify Installation:

bash
Copy code
pytest
Usage
Launch the CLI:

bash
Copy code
python main.py
Select Asset:

Choose from available assets (e.g., BTCUSD, ETHUSD, LTCUSD).
Select Timeframes:

Add desired timeframes (e.g., 1m, 5m, 15m, 1H, 4H, 1D).
Select Strategy:

Choose from available strategies (e.g., BreakoutMTFStrategy, MomentumStrategy, MultiTimeframeStrategy).
Input Strategy Parameters:

Enter parameters like take-profit percentage, stop-loss percentage, moving averages, etc.
Run Backtest:

Execute the backtest and view results in the terminal and generated reports.
Run Optimization (Optional):

Choose optimization methods (Grid Search, Random Search, Sequential Optimization).
Define parameter ranges and constraints.
Execute optimization and review optimized parameters and reports.
CLI Implementation
Purpose: Provide an interactive command-line interface for users to easily configure and execute backtests and optimizations.

Features
Asset Selection: Choose from a list of available trading assets.
Timeframe Configuration: Select multiple timeframes for multi-timeframe strategies.
Strategy Selection: Pick from predefined trading strategies.
Parameter Input: Input or adjust strategy-specific parameters.
Optimization Choice: Select and configure optimization methods.
Report Generation: Automatically generate and save backtest and optimization reports.
Example Usage
bash
Copy code
$ python main.py
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

Enter take-profit percentage (e.g., 14): 12
Enter stop-loss percentage (e.g., 11): 8
Enter higher_tf_short_ma (e.g., 20): 20
Enter higher_tf_long_ma (e.g., 50): 50
Enter primary timeframe (e.g., 5m): 5m
Enter higher timeframe (e.g., 1H): 1H
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

Do you want to run optimization? (yes/no): yes

User chose to run optimization.

Select optimization method:
1. Grid Search
2. Random Search
3. Sequential Optimization
Enter the number of the optimization method you want to use: 1

Enter parameter ranges for optimization:
Enter range for tp_percent (e.g., start,stop,step): 10,14,1
Enter range for sl_percent (e.g., start,stop,step): 5,10,1
Enter range for higher_tf_short_ma (e.g., start,stop,step): 15,25,5
Enter range for higher_tf_long_ma (e.g., start,stop,step): 40,60,10

Do you want to set a constraint on the parameters? (yes/no): yes
Enter constraint as a Python expression involving the parameters (e.g., tp_percent > sl_percent): tp_percent > sl_percent

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
Reporting & Visualization
The framework automatically generates comprehensive reports and visualizations to aid in strategy analysis and optimization.

Generated Reports
Backtest Summary:

Located in the reports/ directory as backtest_summary.csv.
Contains key performance metrics like Return %, Sharpe Ratio, Max Drawdown, etc.
Equity Curve Plot:

Located in the reports/ directory as [StrategyName]_equity_curve.png.
Visual representation of portfolio equity over time.
Full Strategy Report:

Located in the reports/ directory as [StrategyName]_Report.html.
Detailed HTML report including performance metrics, trade logs, and visualizations.
Example Results
plaintext
Copy code
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
Contributing
Contributions are welcome! To contribute to the Algo Trading Framework (Qafary Framework), please follow these guidelines:

Fork the Repository:

Click the "Fork" button on the top-right corner of the repository page.
Clone Your Fork:

bash
Copy code
git clone https://github.com/yourusername/automated-trading-system.git
cd automated-trading-system
Create a Feature Branch:

bash
Copy code
git checkout -b feature/your-feature-name
Commit Your Changes:

bash
Copy code
git add .
git commit -m "Add feature: your-feature-name"
Push to Your Fork:

bash
Copy code
git push origin feature/your-feature-name
Create a Pull Request:

Navigate to your fork on GitHub.
Click "Compare & pull request".
Provide a clear description of your changes.
Submit the pull request for review.
Pull Request Guidelines
Describe Your Changes: Provide a detailed explanation of what your pull request does.
Reference Issues: If your PR addresses an existing issue, reference it using #issue_number.
Follow Coding Standards: Ensure your code adheres to the project's coding conventions.
Include Tests: If applicable, add tests to cover your changes.
Code of Conduct
Please adhere to the Code of Conduct when contributing to this project.

Testing
Ensure the framework's reliability by running the comprehensive test suite.

Running Tests
Activate the Python Environment:

bash
Copy code
source venv/bin/activate  # On Windows: venv\Scripts\activate
Navigate to the Project Directory:

bash
Copy code
cd automated-trading-system
Run Tests Using PyTest:

bash
Copy code
pytest
Test Coverage
Data Management: Validates data loading, preprocessing, and resampling functions.
Backtesting Engine: Ensures strategies execute correctly and performance metrics are accurately calculated.
Optimization Module: Confirms optimization methods correctly identify optimal parameters.
Utilities: Tests helper functions, logging, and configuration management.
Example Test Output
plaintext
Copy code
============================= test session starts ==============================
platform win32 -- Python 3.8.5, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: C:\Users\IQRA\Desktop\Automated Multi-Broker System
collected 15 items

tests\test_data_manager.py .....                                         [ 33%]
tests\test_backtest_runner.py ......                                   [ 73%]
tests\test_optimizer.py ....                                         [100%]

============================== 15 passed in 3.45s ===============================
Deployment
The Algo Trading Framework (Qafary Framework) is designed for deployment in secure and scalable environments.

Deployment Steps
Prepare the Environment:

Ensure all dependencies are installed.
Set up environment variables and configuration files.
Containerization (Optional):

Use Docker to containerize the application for consistent deployment across different environments.
Build Docker Image:
bash
Copy code
docker build -t qafary-framework .
Run Docker Container:
bash
Copy code
docker run -d --name qafary-framework-container qafary-framework
Deploy to Cloud Services:

AWS EC2:
Launch an EC2 instance.
Install necessary dependencies.
Clone the repository and run the application.
Docker Containers:
Deploy Docker containers using orchestration tools like Kubernetes or Docker Compose.
Set Up Continuous Integration/Continuous Deployment (CI/CD):

Utilize GitHub Actions to automate testing and deployment processes.
Example Workflow:
yaml
Copy code
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest
    - name: Deploy to AWS
      if: success()
      run: |
        # Deployment commands go here
Security Measures:

Implement JWT authentication and SSL/TLS encryption.
Regularly update dependencies to patch vulnerabilities.
Monitor logs and system health using monitoring tools.
Documentation
Comprehensive documentation is available in the docs/ directory, covering all aspects of the framework.

Included Documents
Architecture Documentation: Detailed overview of the system architecture and component interactions.
API Documentation: Documentation of backend APIs for integration and extensions.
User Guide: Instructions on using the framework, including CLI operations and strategy implementation.
Developer Guide: Guidelines for contributing to the framework, including coding standards and development workflows.
Security Documentation: Information on security practices and measures implemented within the framework.
License
This project is licensed under the MIT License.

Contact
For questions, support, or feedback, please contact:

Email: abdiqafar@traderabukar.com
GitHub Issues: https://github.com/karaz-debug/automated-trading-system/issues
Community: Join our Discord
