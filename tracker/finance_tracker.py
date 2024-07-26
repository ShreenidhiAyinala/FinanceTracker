from typing import List, Optional
from datetime import datetime
from .transaction import Transaction
import os
import json
import csv
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from reports.report_generator import generate_report

class FinanceTracker:
    def __init__(self):
        self.transactions = []
        self.recurring_transactions = []
        self.load_data()

    def add_transaction(self, amount=None, category=None, description=None, transaction_type=None, tags=None):
        try:
            if amount is None:
                amount = float(input("Enter amount: "))
            if category is None:
                category = input("Enter category: ")
            if description is None:
                description = input("Enter description: ")
            if transaction_type is None:
                transaction_type = input("Enter type (income/expense): ").lower()
                if transaction_type not in ['income', 'expense']:
                    raise ValueError("Transaction type must be 'income' or 'expense'")
            if tags is None:
                tags = input("Enter tags (comma-separated): ").split(',')
            
            date = datetime.now().strftime("%Y-%m-%d")
            transaction = Transaction(amount, category, description, date, transaction_type, tags)
            self.transactions.append(transaction)
            print("Transaction added successfully.")
        except ValueError as e:
            print(f"Error adding transaction: {e}")

    def add_transaction(self, amount: float, category: str, description: str, 
                        transaction_type: str, tags: List[str] = None, 
                        recurring: bool = False, frequency: str = None) -> None:
        """
        Add a new transaction to the tracker.
        
        :param amount: Transaction amount
        :param category: Transaction category
        :param description: Transaction description
        :param transaction_type: Type of transaction (income/expense)
        :param tags: List of tags for the transaction
        :param recurring: Whether the transaction is recurring
        :param frequency: Frequency of recurring transaction (daily, weekly, monthly)
        """
        try:
            transaction = Transaction(amount, category, description, datetime.now().strftime("%Y-%m-%d"), 
                                      transaction_type, tags or [])
            if recurring:
                if frequency not in ['daily', 'weekly', 'monthly']:
                    raise ValueError("Invalid frequency for recurring transaction")
                self.recurring_transactions.append((transaction, frequency))
            else:
                self.transactions.append(transaction)
            print("Transaction added successfully.")
        except ValueError as e:
            print(f"Error adding transaction: {e}")
        
    def view_transactions(self, start_date=None, end_date=None, category=None):
        filtered_transactions = self.transactions

        if start_date:
            filtered_transactions = [t for t in filtered_transactions if t.date >= start_date]
        if end_date:
            filtered_transactions = [t for t in filtered_transactions if t.date <= end_date]
        if category:
            filtered_transactions = [t for t in filtered_transactions if t.category.lower() == category.lower()]

        for t in filtered_transactions:
            print(t)

    def view_transactions(self, start_date: Optional[str] = None, 
                          end_date: Optional[str] = None, 
                          category: Optional[str] = None) -> None:
        """
        View transactions with optional filters.
        
        :param start_date: Start date for filtering transactions
        :param end_date: End date for filtering transactions
        :param category: Category for filtering transactions
        """
        filtered_transactions = self.transactions

        if start_date:
            filtered_transactions = [t for t in filtered_transactions if t.date >= start_date]
        if end_date:
            filtered_transactions = [t for t in filtered_transactions if t.date <= end_date]
        if category:
            filtered_transactions = [t for t in filtered_transactions if t.category.lower() == category.lower()]

        for t in filtered_transactions:
            print(t)
        
    def process_recurring_transactions(self) -> None:
        """Process all recurring transactions and add them to the main transaction list."""
        today = datetime.now().date()
        for transaction, frequency in self.recurring_transactions:
            if frequency == 'daily':
                self.transactions.append(transaction)
            elif frequency == 'weekly' and today.weekday() == 0:  # Monday
                self.transactions.append(transaction)
            elif frequency == 'monthly' and today.day == 1:
                self.transactions.append(transaction)

    def calculate_balance(self, start_date=None, end_date=None):
        relevant_transactions = self.transactions
        if start_date:
            relevant_transactions = [t for t in relevant_transactions if t.date >= start_date]
        if end_date:
            relevant_transactions = [t for t in relevant_transactions if t.date <= end_date]

        balance = sum(t.amount if t.transaction_type == 'income' else -t.amount for t in relevant_transactions)
        return balance

    def generate_report(self, report_type="summary", start_date=None, end_date=None):
        from reports.report_generator import generate_report
        return generate_report(self.transactions, report_type, start_date, end_date)

    def save_data(self):
        with open('data/transactions.json', 'w') as f:
            json.dump([t.to_dict() for t in self.transactions], f, indent=4)
        print("Data saved successfully.")

    def load_data(self):
        try:
            with open('data/transactions.json', 'r') as f:
                data = json.load(f)
                self.transactions = [Transaction.from_dict(t) for t in data]
            print("Data loaded successfully.")
        except FileNotFoundError:
            print("No existing data found. Starting with an empty transaction list.")
            self.transactions = []

    def edit_transaction(self, index):
        try:
            transaction = self.transactions[index]
            print(f"Editing transaction: {transaction}")
            
            amount = input(f"Enter new amount (current: {transaction.amount}): ")
            if amount:
                transaction.amount = float(amount)
            
            category = input(f"Enter new category (current: {transaction.category}): ")
            if category:
                transaction.category = category
            
            description = input(f"Enter new description (current: {transaction.description}): ")
            if description:
                transaction.description = description
            
            transaction_type = input(f"Enter new type (income/expense) (current: {transaction.transaction_type}): ")
            if transaction_type:
                if transaction_type not in ['income', 'expense']:
                    raise ValueError("Transaction type must be 'income' or 'expense'")
                transaction.transaction_type = transaction_type
            
            tags = input(f"Enter new tags (comma-separated) (current: {','.join(transaction.tags)}): ")
            if tags:
                transaction.tags = tags.split(',')
            
            print("Transaction updated successfully.")
        except IndexError:
            print("Invalid transaction index.")
        except ValueError as e:
            print(f"Error updating transaction: {e}")

    def delete_transaction(self, index):
        try:
            deleted_transaction = self.transactions.pop(index)
            print(f"Deleted transaction: {deleted_transaction}")
        except IndexError:
            print("Invalid transaction index.")

    def export_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Date', 'Type', 'Amount', 'Category', 'Description', 'Tags'])
            for t in self.transactions:
                writer.writerow([t.date, t.transaction_type, t.amount, t.category, t.description, ','.join(t.tags)])
        print(f"Data exported to {filename}")

    def get_statistics(self):
        if not self.transactions:
            return "No transactions to analyze."

        total_income = sum(t.amount for t in self.transactions if t.transaction_type == 'income')
        total_expense = sum(t.amount for t in self.transactions if t.transaction_type == 'expense')
        net_savings = total_income - total_expense

        category_totals = {}
        for t in self.transactions:
            if t.category not in category_totals:
                category_totals[t.category] = 0
            category_totals[t.category] += t.amount if t.transaction_type == 'income' else -t.amount

        most_expensive_category = max(category_totals, key=category_totals.get)
        most_profitable_category = min(category_totals, key=category_totals.get)

        return f"""
        Financial Statistics:
        Total Income: ${total_income:.2f}
        Total Expenses: ${total_expense:.2f}
        Net Savings: ${net_savings:.2f}
        Most Expensive Category: {most_expensive_category} (${abs(category_totals[most_expensive_category]):.2f})
        Most Profitable Category: {most_profitable_category} (${abs(category_totals[most_profitable_category]):.2f})
        """
    def calculate_balance(self, start_date: Optional[str] = None, 
                          end_date: Optional[str] = None) -> float:
        """
        Calculate balance within the given date range.
        
        :param start_date: Start date for balance calculation
        :param end_date: End date for balance calculation
        :return: Calculated balance
        """
        relevant_transactions = self.transactions
        if start_date:
            relevant_transactions = [t for t in relevant_transactions if t.date >= start_date]
        if end_date:
            relevant_transactions = [t for t in relevant_transactions if t.date <= end_date]

        balance = sum(t.amount if t.transaction_type == 'income' else -t.amount for t in relevant_transactions)
        return balance
    def generate_report(self):
        data = [t.__dict__ for t in self.transactions]
        report_path = os.path.join("reports", f"report_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")
        generate_report(data, report_path)
        
        return report_path

    def generate_category_report(self) -> None:
        """Generate and display a pie chart of expenses by category."""
        category_totals = {}
        for t in self.transactions:
            if t.transaction_type == 'expense':
                if t.category not in category_totals:
                    category_totals[t.category] = 0
                category_totals[t.category] += t.amount

        labels = list(category_totals.keys())
        values = list(category_totals.values())

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_layout(title='Expenses by Category')
        fig.show()

    def generate_monthly_report(self) -> None:
        """Generate and display a line chart of monthly expenses and income."""
        monthly_data = {}
        for t in self.transactions:
            month = t.date[:7]  # YYYY-MM
            if month not in monthly_data:
                monthly_data[month] = {'income': 0, 'expense': 0}
            if t.transaction_type == 'income':
                monthly_data[month]['income'] += t.amount
            else:
                monthly_data[month]['expense'] += t.amount

        months = sorted(monthly_data.keys())
        income = [monthly_data[m]['income'] for m in months]
        expenses = [monthly_data[m]['expense'] for m in months]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=months, y=income, name="Income"), secondary_y=False)
        fig.add_trace(go.Scatter(x=months, y=expenses, name="Expenses"), secondary_y=True)
        fig.update_layout(title='Monthly Income and Expenses')
        fig.update_xaxes(title_text="Month")
        fig.update_yaxes(title_text="Amount", secondary_y=False)
        fig.update_yaxes(title_text="Amount", secondary_y=True)
        fig.show()
    
    def clear_transactions(self):
        self.transactions = []
        print("All transactions have been cleared.")
