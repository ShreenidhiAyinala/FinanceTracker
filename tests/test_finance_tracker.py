import unittest
from unittest.mock import patch, mock_open
from tracker.finance_tracker import FinanceTracker
from tracker.transaction import Transaction
from reports.report_generator import generate_report
from datetime import datetime

class TestFinanceTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = FinanceTracker()
        self.tracker.transactions = []  # Clear existing transactions

    @patch('builtins.input', side_effect=['100', 'Salary', 'Monthly pay', 'income', 'work,salary'])
    def test_add_transaction(self, mock_input):
        self.tracker.add_transaction(100, 'Salary', 'Monthly pay', 'income', ['work', 'salary'])
        self.assertEqual(len(self.tracker.transactions), 1)
        t = self.tracker.transactions[0]
        self.assertEqual(t.amount, 100)
        self.assertEqual(t.category, 'Salary')
        self.assertEqual(t.description, 'Monthly pay')
        self.assertEqual(t.transaction_type, 'income')
        self.assertEqual(t.tags, ['work', 'salary'])

    def test_calculate_balance(self):
        t1 = Transaction(amount=100, category="Income", description="Salary", transaction_type="income")
        t2 = Transaction(amount=50, category="Food", description="Dinner", transaction_type="expense")
        self.tracker.transactions = [t1, t2]
        self.assertEqual(self.tracker.calculate_balance(), 50)

    @patch('tracker.finance_tracker.generate_report')
    @patch('tracker.finance_tracker.datetime')
    def test_generate_report(self, mock_datetime, mock_generate_report):
        mock_datetime.now.return_value = datetime(2024, 7, 25, 0, 46, 19)
        mock_generate_report.return_value = 'mocked_report_path'
        report_path = self.tracker.generate_report()
        self.assertEqual(report_path, 'reports/report_20240725004619.pdf')
        mock_generate_report.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_data(self, mock_json_dump, mock_file):
        t = Transaction(amount=100, category="Test", description="Test transaction")
        self.tracker.transactions = [t]
        self.tracker.save_data()
        mock_file.assert_called_once_with('data/transactions.json', 'w')
        mock_json_dump.assert_called_once()

    @patch('builtins.open', new_callable=mock_open, read_data='[{"amount": 100, "category": "Test", "description": "Test transaction", "date": "2024-07-24", "transaction_type": "expense"}]')
    @patch('json.load')
    def test_load_data(self, mock_json_load, mock_file):
        mock_json_load.return_value = [{"amount": 100, "category": "Test", "description": "Test transaction", "date": "2024-07-24", "transaction_type": "expense"}]
        self.tracker.load_data()
        self.assertEqual(len(self.tracker.transactions), 1)
        t = self.tracker.transactions[0]
        self.assertEqual(t.amount, 100)
        self.assertEqual(t.category, "Test")

    def test_view_transactions(self):
        t1 = Transaction(amount=100, category="Income", description="Salary", date="2024-07-01", transaction_type="income")
        t2 = Transaction(amount=50, category="Food", description="Dinner", date="2024-07-15", transaction_type="expense")
        self.tracker.transactions = [t1, t2]
        
        with patch('builtins.print') as mock_print:
            self.tracker.view_transactions(start_date="2024-07-01", end_date="2024-07-31", category="Income")
            mock_print.assert_called_once()

    def test_edit_transaction(self):
        t = Transaction(amount=100, category="Test", description="Original")
        self.tracker.transactions = [t]
        
        with patch('builtins.input', side_effect=['200', 'Updated', 'New description', '', '']):
            self.tracker.edit_transaction(0)
        
        updated_t = self.tracker.transactions[0]
        self.assertEqual(updated_t.amount, 200)
        self.assertEqual(updated_t.category, 'Updated')
        self.assertEqual(updated_t.description, 'New description')

    def test_delete_transaction(self):
        t = Transaction(amount=100, category="Test", description="To be deleted")
        self.tracker.transactions = [t]
        self.tracker.delete_transaction(0)
        self.assertEqual(len(self.tracker.transactions), 0)

    @patch('csv.writer')
    def test_export_to_csv(self, mock_csv_writer):
        t = Transaction(amount=100, category="Test", description="CSV test")
        self.tracker.transactions = [t]
        
        with patch('builtins.open', new_callable=mock_open) as mock_file:
            self.tracker.export_to_csv('test.csv')
            mock_file.assert_called_once_with('test.csv', 'w', newline='')
            mock_csv_writer.assert_called_once()

    def test_get_statistics(self):
        t1 = Transaction(amount=1000, category="Salary", description="Monthly", transaction_type="income")
        t2 = Transaction(amount=500, category="Rent", description="Monthly", transaction_type="expense")
        t3 = Transaction(amount=200, category="Food", description="Groceries", transaction_type="expense")
        self.tracker.transactions = [t1, t2, t3]
        
        stats = self.tracker.get_statistics()
        self.assertIn("Total Income: $1000.00", stats)
        self.assertIn("Total Expenses: $700.00", stats)
        self.assertIn("Net Savings: $300.00", stats)
        self.assertIn("Most Expensive Category: Salary ($1000.00)", stats)
        self.assertIn("Most Profitable Category: Rent ($500.00)", stats)

if __name__ == '__main__':
    unittest.main()