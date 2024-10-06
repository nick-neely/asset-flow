import streamlit as st
import pandas as pd
import numpy as np
import datetime
import altair as alt

CACHE_FILE = "net_worth_cache.json"


def calculate_retirement_value(start_value, monthly_contribution, annual_growth_rate, months):
    monthly_growth_rate = (1 + annual_growth_rate) ** (1/12) - 1
    contributions = np.full(months, monthly_contribution)
    values = np.zeros(months)
    if start_value > 0.001:
        values[0] = start_value * (1 + monthly_growth_rate) + contributions[0]
    for month in range(1, months):
        values[month] = values[month - 1] * \
            (1 + monthly_growth_rate) + contributions[month]
        if not np.isfinite(values[month]):
            values[month] = 0  # Prevent infinite values
    return values.tolist()


def calculate_loan_balance(start_balance, monthly_payment, annual_interest_rate, months, start_month=0, appreciation_rate=0.0):
    balance = start_balance
    monthly_interest_rate = annual_interest_rate / 12
    monthly_appreciation_rate = (1 + appreciation_rate) ** (1/12) - 1
    balances = [0] * start_month
    equity = [0] * start_month

    for month in range(start_month, months):
        interest = balance * monthly_interest_rate
        principal_payment = monthly_payment - interest
        balance = balance + interest - monthly_payment
        balance = max(balance, 0)  # Ensure balance doesn't go negative
        if not np.isfinite(balance):
            balance = 0  # Prevent infinite values
        # Adjust for appreciation/depreciation
        start_balance *= (1 + monthly_appreciation_rate)
        if not np.isfinite(start_balance):
            start_balance = 0  # Prevent infinite values
        # Continue appreciating/depreciating even after loan is paid off
        if balance == 0:
            start_balance *= (1 + monthly_appreciation_rate)
            if not np.isfinite(start_balance):
                start_balance = 0  # Prevent infinite values
        equity_value = start_balance - balance if balance > 0 else start_balance
        balances.append(balance)
        equity.append(equity_value)

    return balances, equity


def calculate_investment_value(start_value, monthly_contribution, annual_growth_rate, months):
    monthly_growth_rate = (1 + annual_growth_rate) ** (1/12) - 1
    contributions = np.full(months, monthly_contribution)
    values = np.zeros(months)
    values[0] = start_value * (1 + monthly_growth_rate) + contributions[0]
    for month in range(1, months):
        values[month] = values[month - 1] * \
            (1 + monthly_growth_rate) + contributions[month]
        if not np.isfinite(values[month]):
            values[month] = 0  # Prevent infinite values
    return values.tolist()


def main():
    st.title("AssetFlow")
    st.subheader("Visualize Your Financial Journey")
    st.write(
        """
        Welcome to AssetFlow! This app helps you visualize your financial journey by tracking your net worth over time. 
        Here's what you can do:
        - Add retirement accounts
        - Add investment accounts
        - Add loans
        - Add savings accounts
        - Set financial goals
        
        The app will simulate your net worth based on the data you provide, helping you:
        - Plan for retirement
        - Track progress towards financial goals
        - Visualize the impact of loans and investments
        """
    )

    st.write("\n")
    st.write("-----------------------------------")

    # Initialize session state
    if "cache" not in st.session_state:
        st.session_state.cache = {}
    cache = st.session_state.cache

    st.sidebar.header("Assets")
    retirement_accounts = []
    num_retirement = st.sidebar.number_input(
        "Number of retirement accounts", min_value=0, value=cache.get("num_retirement", 1), step=1)
    cache["num_retirement"] = num_retirement
    for i in range(num_retirement):
        account_label = st.sidebar.text_input(f"Label for Retirement Account #{i+1}", value=cache.get(
            f"retirement_label_{i}", f"Retirement Account {i+1}"), key=f"retirement_label_{i}")
        st.sidebar.subheader(account_label)
        cache[f"retirement_label_{i}"] = account_label
        start_value = st.sidebar.number_input(f"Initial Value of Account #{i+1}", min_value=0.0, value=cache.get(
            f"retirement_start_value_{i}", 10000.0), step=1000.0, key=f"retirement_start_value_{i}")
        monthly_contribution = st.sidebar.number_input(f"Monthly Contribution for Account #{i+1}", min_value=0.0, value=cache.get(
            f"retirement_monthly_contribution_{i}", 500.0), step=50.0, key=f"retirement_monthly_contribution_{i}")
        annual_growth_rate = st.sidebar.number_input(f"Annual Growth Rate (in %) for Account #{
                                                     i+1}", min_value=0.0, value=5.0, step=0.1, key=f"retirement_annual_growth_rate_{i}") / 100
        retirement_accounts.append(
            (start_value, monthly_contribution, annual_growth_rate))
        cache[f"retirement_start_value_{i}"] = start_value
        cache[f"retirement_monthly_contribution_{i}"] = monthly_contribution
        cache[f"retirement_annual_growth_rate_{i}"] = annual_growth_rate

    st.sidebar.header("Liabilities")

    loans = []
    num_loans = st.sidebar.number_input(
        "Number of loans", min_value=0, value=cache.get("num_loans", 1), step=1)
    cache["num_loans"] = num_loans
    for i in range(num_loans):
        loan_label = st.sidebar.text_input(f"Label for Loan #{
            i+1}", value=cache.get(f"loan_label_{i}", f"Loan {i+1}"), key=f"loan_label_{i}")
        st.sidebar.subheader(loan_label)
        cache[f"loan_label_{i}"] = loan_label
        start_balance = st.sidebar.number_input(f"Initial Balance of Loan #{i+1}", min_value=0.0, value=cache.get(
            f"loan_start_balance_{i}", 15000.0), step=1000.0, key=f"loan_start_balance_{i}")
        monthly_payment = st.sidebar.number_input(f"Monthly Payment for Loan #{
            i+1}", min_value=0.0, value=cache.get(f"loan_monthly_payment_{i}", 300.0), step=50.0, key=f"loan_monthly_payment_{i}")
        annual_interest_rate = st.sidebar.number_input(f"Annual Interest Rate (in %) for Loan #{
            i+1}", min_value=0.0, value=3.0, step=0.1, key=f"loan_annual_interest_rate_{i}") / 100
        start_year = st.sidebar.number_input(f"Start Year for Loan #{
            i+1} (e.g., 4.5 for 4 and a half years)", min_value=0.0, value=0.0, step=0.1, key=f"loan_start_year_{i}")
        start_month = int(start_year * 12)
        appreciation_rate = st.sidebar.number_input(f"Appreciation/Depreciation Rate (in %) for Loan #{
                                                    i+1}", min_value=-100.0, max_value=100.0, value=0.0, step=0.1, key=f"loan_appreciation_rate_{i}") / 100
        equity_checkbox = st.sidebar.checkbox(f"Include Principal as Equity for Loan #{
            i+1}", value=False, key=f"loan_equity_checkbox_{i}")
        loans.append((start_balance, monthly_payment, annual_interest_rate,
                      start_month, appreciation_rate, equity_checkbox))
        cache[f"loan_start_balance_{i}"] = start_balance
        cache[f"loan_monthly_payment_{i}"] = monthly_payment
        cache[f"loan_annual_interest_rate_{i}"] = annual_interest_rate
        cache[f"loan_start_year_{i}"] = start_year
        cache[f"loan_appreciation_rate_{i}"] = appreciation_rate
        cache[f"loan_equity_checkbox_{i}"] = equity_checkbox

    st.sidebar.header("Investments")
    investments = []
    num_investments = st.sidebar.number_input(
        "Number of investments", min_value=0, value=cache.get("num_investments", 1), step=1)
    cache["num_investments"] = num_investments
    for i in range(num_investments):
        investment_label = st.sidebar.text_input(f"Label for Investment #{
            i+1}", value=cache.get(f"investment_label_{i}", f"Investment {i+1}"), key=f"investment_label_{i}")
        st.sidebar.subheader(investment_label)
        cache[f"investment_label_{i}"] = investment_label
        start_value = st.sidebar.number_input(f"Initial Value of Investment #{i+1}", min_value=0.0, value=cache.get(
            f"investment_start_value_{i}", 5000.0), step=1000.0, key=f"investment_start_value_{i}")
        monthly_contribution = st.sidebar.number_input(f"Monthly Contribution for Investment #{i+1}", min_value=0.0, value=cache.get(
            f"investment_monthly_contribution_{i}", 200.0), step=50.0, key=f"investment_monthly_contribution_{i}")
        annual_growth_rate = st.sidebar.number_input(f"Annual Growth Rate (in %) for Investment #{
            i+1}", min_value=0.0, value=7.0, step=0.1, key=f"investment_annual_growth_rate_{i}") / 100
        investments.append(
            (start_value, monthly_contribution, annual_growth_rate))
        cache[f"investment_start_value_{i}"] = start_value
        cache[f"investment_monthly_contribution_{i}"] = monthly_contribution
        cache[f"investment_annual_growth_rate_{i}"] = annual_growth_rate

    st.sidebar.header("Savings Accounts")
    savings_accounts = []
    num_savings = st.sidebar.number_input(
        "Number of savings accounts", min_value=0, value=cache.get("num_savings", 1), step=1)
    cache["num_savings"] = num_savings
    for i in range(num_savings):
        savings_label = st.sidebar.text_input(f"Label for Savings Account #{
            i+1}", value=cache.get(f"savings_label_{i}", f"Savings Account {i+1}"), key=f"savings_label_{i}")
        st.sidebar.subheader(savings_label)
        cache[f"savings_label_{i}"] = savings_label
        start_value = st.sidebar.number_input(f"Initial Value of Savings Account #{i+1}", min_value=0.0, value=cache.get(
            f"savings_start_value_{i}", 2000.0), step=500.0, key=f"savings_start_value_{i}")
        monthly_contribution = st.sidebar.number_input(f"Monthly Contribution for Savings Account #{
            i+1}", min_value=0.0, value=cache.get(f"savings_monthly_contribution_{i}", 100.0), step=50.0, key=f"savings_monthly_contribution_{i}")
        annual_growth_rate = st.sidebar.number_input(f"Annual Growth Rate (in %) for Savings Account #{
            i+1}", min_value=0.0, value=1.5, step=0.1, key=f"savings_annual_growth_rate_{i}") / 100
        savings_accounts.append(
            (start_value, monthly_contribution, annual_growth_rate))
        cache[f"savings_start_value_{i}"] = start_value
        cache[f"savings_monthly_contribution_{i}"] = monthly_contribution
        cache[f"savings_annual_growth_rate_{i}"] = annual_growth_rate

    goals = []

    num_goals = st.sidebar.number_input(
        "Number of financial goals", min_value=0, value=cache.get("num_goals", 1), step=1)
    cache["num_goals"] = num_goals
    for i in range(num_goals):
        st.sidebar.subheader(f"Goal #{i+1}")
        goal_name = st.sidebar.text_input(f"Goal Name #{
            i+1}", value=cache.get(f"goal_name_{i}", f"Goal {i+1}"), key=f"goal_name_{i}")
        goal_amount = st.sidebar.number_input(f"Goal Amount #{i+1}", min_value=0.0, value=cache.get(
            f"goal_amount_{i}", 10000.0), step=100.0, key=f"goal_amount_{i}")
        target_year = st.sidebar.number_input(f"Target Year for Goal #{i+1}", min_value=0.0, value=float(cache.get(
            f"goal_target_year_{i}", cache.get("num_years", 10))), step=1.0, key=f"goal_target_year_{i}")
        target_month = int(target_year * 12)
        goals.append((goal_name, goal_amount, target_month))
        cache[f"goal_name_{i}"] = goal_name
        cache[f"goal_amount_{i}"] = goal_amount
        cache[f"goal_target_year_{i}"] = target_year

    st.sidebar.header("Simulation Settings")
    num_years = st.sidebar.slider("Number of years to simulate", min_value=1,
                                  max_value=50, value=cache.get("num_years", 10), key="num_years")
    cache["num_years"] = num_years
    months = num_years * 12

    # Save session state
    st.session_state.cache = cache

    # Calculate retirement values
    total_assets = np.zeros(months)
    for start_value, monthly_contribution, annual_growth_rate in retirement_accounts:
        values = calculate_retirement_value(
            start_value, monthly_contribution, annual_growth_rate, months)
        total_assets += np.array(values)

    # Calculate investment values
    for start_value, monthly_contribution, annual_growth_rate in investments:
        values = calculate_investment_value(
            start_value, monthly_contribution, annual_growth_rate, months)
        total_assets += np.array(values)

    # Calculate savings values
    for start_value, monthly_contribution, annual_growth_rate in savings_accounts:
        values = calculate_investment_value(
            start_value, monthly_contribution, annual_growth_rate, months)
        total_assets += np.array(values)

    # Calculate loan balances
    total_liabilities = np.zeros(months)
    for i, (start_balance, monthly_payment, annual_interest_rate, start_month, appreciation_rate, equity_checkbox) in enumerate(loans):
        balances, equity = calculate_loan_balance(
            start_balance, monthly_payment, annual_interest_rate, months, start_month, appreciation_rate)
        total_liabilities += np.array(balances)
        if equity_checkbox:
            total_assets += np.array(equity)

    # Calculate net worth
    net_worth = [asset - liability for asset,
                 liability in zip(total_assets, total_liabilities)]

    # Plotting the results
    st.header("Net Worth Over Time")

    # Create a dataframe
    dates = [datetime.date.today() + datetime.timedelta(days=30 * i)
             for i in range(months)]
    df = pd.DataFrame({"Date": dates, "Assets": total_assets,
                      "Liabilities": total_liabilities, "Net Worth": net_worth})

    # Set the date as the index
    df.set_index("Date", inplace=True)

    # Ensure all values are finite
    df = df[np.isfinite(df).all(1)]

    # Add goals to the dataframe for visualization
    goal_dates = []
    goal_values = []
    goal_labels = []
    for goal_name, goal_amount, target_month in goals:
        if target_month < months:
            goal_dates.append(dates[target_month])
            goal_values.append(goal_amount)
            goal_labels.append(goal_name)

    # Create the base chart
    chart = alt.Chart(df.reset_index()).transform_fold(
        fold=['Assets', 'Liabilities', 'Net Worth'],
        as_=['Category', 'Value']
    ).mark_line().encode(
        x='Date:T',
        y='Value:Q',
        color='Category:N'
    ).properties(
        width=800,
        height=400
    )

    # Add goal markers to the chart
    if goal_dates:
        goal_df = pd.DataFrame(
            {"Date": goal_dates, "Goal Value": goal_values, "Goal": goal_labels})
        goal_chart = alt.Chart(goal_df).mark_point(shape="circle", size=100, color="red").encode(
            x='Date:T',
            y='Goal Value:Q',
            tooltip=['Goal', 'Goal Value']
        )
        chart += goal_chart

    st.altair_chart(chart)

    # Show data in a table
    st.header("Overall Data Table")
    st.dataframe(df)

    # Create a more in-depth data table
    st.header("Detailed Data Table")
    detailed_data = []

    # Add detailed data for retirement accounts
    for i, (start_value, monthly_contribution, annual_growth_rate) in enumerate(retirement_accounts):
        values = calculate_retirement_value(
            start_value, monthly_contribution, annual_growth_rate, months)
        detailed_data.append(
            (cache.get(f"retirement_label_{i}", f"Retirement Account {i+1}"), values))

    # Add detailed data for investments
    for i, (start_value, monthly_contribution, annual_growth_rate) in enumerate(investments):
        values = calculate_investment_value(
            start_value, monthly_contribution, annual_growth_rate, months)
        detailed_data.append(
            (cache.get(f"investment_label_{i}", f"Investment {i+1}"), values))

    # Add detailed data for savings accounts
    for i, (start_value, monthly_contribution, annual_growth_rate) in enumerate(savings_accounts):
        values = calculate_investment_value(
            start_value, monthly_contribution, annual_growth_rate, months)
        detailed_data.append(
            (cache.get(f"savings_label_{i}", f"Savings Account {i+1}"), values))

    # Add detailed data for loans
    for i, (start_balance, monthly_payment, annual_interest_rate, start_month, appreciation_rate, equity_checkbox) in enumerate(loans):
        balances, equity = calculate_loan_balance(
            start_balance, monthly_payment, annual_interest_rate, months, start_month, appreciation_rate)
        detailed_data.append(
            (f"{cache.get(f'loan_label_{i}', f'Loan {i+1}')} Balance", balances))
        if equity_checkbox:
            detailed_data.append(
                (f"{cache.get(f'loan_label_{i}', f'Loan {i+1}')} Equity", equity))

    # Create a dictionary for DataFrame construction
    detailed_dict = {label: values for label, values in detailed_data}

    # Create the DataFrame
    detailed_df = pd.DataFrame(detailed_dict, index=dates)

    # Show detailed data in a table
    st.dataframe(detailed_df)

    # Export options
    st.sidebar.header("Export Options")
    if st.sidebar.button("Export to CSV"):
        df.to_csv("net_worth_export.csv")
        st.sidebar.success("Exported data to net_worth_export.csv")
    if st.sidebar.button("Export to Excel"):
        df.to_excel("net_worth_export.xlsx")
        st.sidebar.success("Exported data to net_worth_export.xlsx")


if __name__ == "__main__":
    main()
