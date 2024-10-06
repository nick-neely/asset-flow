# AssetFlow 📈

Welcome to **AssetFlow**! This Streamlit application helps you visualize your financial journey by tracking your net worth over time. Whether you're planning for retirement, tracking progress towards financial goals, or visualizing the impact of loans and investments, AssetFlow has you covered.

## Table of Contents 📚

- [AssetFlow 📈](#assetflow-)
  - [Table of Contents 📚](#table-of-contents-)
  - [Features ✨](#features-)
  - [Installation 🛠️](#installation-️)
  - [Usage 🚀](#usage-)
  - [Inputs 📥](#inputs-)
    - [Assets 💰](#assets-)
    - [Liabilities 💸](#liabilities-)
    - [Investments 📈](#investments-)
    - [Savings Accounts 🏦](#savings-accounts-)
    - [Financial Goals 🎯](#financial-goals-)
    - [Simulation Settings ⚙️](#simulation-settings-️)
  - [Outputs 📊](#outputs-)
    - [Net Worth Over Time 📅](#net-worth-over-time-)
    - [Overall Data Table 📋](#overall-data-table-)
    - [Detailed Data Table 📑](#detailed-data-table-)
  - [Export Options 📤](#export-options-)
  - [Contributing 🤝](#contributing-)
  - [License 📜](#license-)

## Features ✨

- **Add Retirement Accounts**: Track your retirement savings and contributions.
- **Add Investment Accounts**: Monitor your investments and their growth.
- **Add Loans**: Keep an eye on your liabilities and their impact on your net worth.
- **Add Savings Accounts**: Manage your savings and see how they grow over time.
- **Set Financial Goals**: Define your financial goals and track your progress towards achieving them.
- **Simulate Net Worth**: Visualize your net worth over time based on the data you provide.

## Installation 🛠️

To install and run AssetFlow, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/assetflow.git
   cd assetflow
   ```

2. **Create the Virtual Environment**

   ```bash
   python -m venv .venv
   ```

3. **Activate Virtual Environment**

   - **Windows**:

     ```bash
     .venv\Scripts\activate
     ```

   - **Mac/Linux**:

     ```bash
     source .venv/bin/activate
     ```

4. **Install the required depepndencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Streamlit application**

   ```bash
   streamlit run asset-flow.py
   ```

## Usage 🚀

Once the application is running, you can interact with it through the sidebar to input your financial data and visualize your net worth over time.

## Inputs 📥

### Assets 💰

Add your retirement accounts, investments, and savings accounts. For each account, you can specify:

- **Label**: A name for the account.
- **Initial Value**: The starting balance of the account.
- **Monthly Contribution**: The amount you contribute to the account each month.
- **Annual Growth Rate**: The expected annual growth rate of the account.

### Liabilities 💸

Add your loans and specify:

- **Label**: A name for the loan.
- **Initial Balance**: The starting balance of the loan.
- **Monthly Payment**: The amount you pay towards the loan each month.
- **Annual Interest Rate**: The annual interest rate of the loan.
- **Start Year**: The year the loan starts.
- **Appreciation/Depreciation Rate**: The rate at which the value of the asset associated with the loan appreciates or depreciates.
- **Include Principal as Equity**: Whether to include the principal as equity.

### Investments 📈

Add your investment accounts and specify:

- **Label**: A name for the investment.
- **Initial Value**: The starting balance of the investment.
- **Monthly Contribution**: The amount you contribute to the investment each month.
- **Annual Growth Rate**: The expected annual growth rate of the investment.

### Savings Accounts 🏦

Add your savings accounts and specify:

- **Label**: A name for the savings account.
- **Initial Value**: The starting balance of the savings account.
- **Monthly Contribution**: The amount you contribute to the savings account each month.
- **Annual Growth Rate**: The expected annual growth rate of the savings account.

### Financial Goals 🎯

Set your financial goals and specify:

- **Goal Name**: A name for the goal.
- **Goal Amount**: The amount you aim to save for the goal.
- **Target Year**: The year by which you aim to achieve the goal.

### Simulation Settings ⚙️

Configure the simulation settings:

- **Number of Years to Simulate**: The number of years over which to simulate your net worth.

## Outputs 📊

### Net Worth Over Time 📅

Visualize your net worth over time with a line chart. The chart shows your assets, liabilities, and net worth for each month of the simulation period.

### Overall Data Table 📋

View a table of your overall financial data, including assets, liabilities, and net worth for each month of the simulation period.

### Detailed Data Table 📑

View a detailed table of your financial data, including the values of each retirement account, investment, savings account, and loan for each month of the simulation period.

## Export Options 📤

Export your financial data to CSV or Excel format for further analysis or record-keeping.

## Contributing 🤝

We welcome contributions to AssetFlow! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License 📜

This project is licensed under the MIT License. See the LICENSE file for more details.

---

Thank you for using AssetFlow! We hope it helps you achieve your financial goals. 🚀
