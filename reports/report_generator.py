import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

def generate_report(transactions, report_type="summary", start_date=None, end_date=None):
    if not os.path.exists('reports'):
        os.makedirs('reports')
    
    # Filter transactions by date if specified
    if start_date:
        transactions = [t for t in transactions if t.date >= start_date]
    if end_date:
        transactions = [t for t in transactions if t.date <= end_date]
    
    if report_type == "summary":
        return generate_summary_report(transactions)
    elif report_type == "detailed":
        return generate_detailed_report(transactions)
    else:
        raise ValueError("Invalid report type. Choose 'summary' or 'detailed'.")

def generate_summary_report(transactions):
    income = sum(t.amount for t in transactions if t.transaction_type == 'income')
    expenses = sum(t.amount for t in transactions if t.transaction_type == 'expense')
    
    # Create pie chart
    plt.figure(figsize=(10, 6))
    plt.pie([income, expenses], labels=['Income', 'Expenses'], autopct='%1.1f%%')
    plt.title('Income vs Expenses')
    
    report_path = 'reports/financial_summary.png'
    plt.savefig(report_path)
    plt.close()
    
    text_report = f"""
    Financial Summary Report
    ------------------------
    Total Income: ${income:.2f}
    Total Expenses: ${expenses:.2f}
    Net Balance: ${income - expenses:.2f}
    """
    
    with open('reports/financial_summary.txt', 'w') as f:
        f.write(text_report)
    
    return report_path

def generate_detailed_report(transactions):
    categories = {}
    dates = []
    balances = []
    running_balance = 0
    
    for t in sorted(transactions, key=lambda x: x.date):
        if t.category not in categories:
            categories[t.category] = 0
        categories[t.category] += t.amount if t.transaction_type == 'income' else -t.amount
        
        running_balance += t.amount if t.transaction_type == 'income' else -t.amount
        dates.append(datetime.strptime(t.date, "%Y-%m-%d"))
        balances.append(running_balance)
    
    # Create category breakdown
    plt.figure(figsize=(12, 6))
    plt.bar(categories.keys(), categories.values())
    plt.title('Category Breakdown')
    plt.xlabel('Category')
    plt.ylabel('Amount')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    category_report_path = 'reports/category_breakdown.png'
    plt.savefig(category_report_path)
    plt.close()
    
    # Create balance over time chart
    plt.figure(figsize=(12, 6))
    plt.plot(dates, balances)
    plt.title('Balance Over Time')
    plt.xlabel('Date')
    plt.ylabel('Balance')
    plt.tight_layout()
    
    balance_report_path = 'reports/balance_over_time.png'
    plt.savefig(balance_report_path)
    plt.close()
    
    return [category_report_path, balance_report_path]