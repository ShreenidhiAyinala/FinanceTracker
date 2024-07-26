import unittest
from unittest.mock import patch, MagicMock
from reports.report_generator import generate_report, generate_summary_report, generate_detailed_report
from tracker.transaction import Transaction

class TestReportGenerator(unittest.TestCase):
    def setUp(self):
        self.transactions = [
            Transaction(amount=1000, category="Salary", description="Monthly", transaction_type="income", date="2024-07-01"),
            Transaction(amount=500, category="Rent", description="Monthly", transaction_type="expense", date="2024-07-05"),
            Transaction(amount=200, category="Food", description="Groceries", transaction_type="expense", date="2024-07-10")
        ]

    @patch('reports.report_generator.generate_summary_report')
    @patch('reports.report_generator.generate_detailed_report')
    def test_generate_report(self, mock_detailed, mock_summary):
        generate_report(self.transactions, "summary")
        mock_summary.assert_called_once()
        
        generate_report(self.transactions, "detailed")
        mock_detailed.assert_called_once()
        
        with self.assertRaises(ValueError):
            generate_report(self.transactions, "invalid_type")

    @patch('matplotlib.pyplot.savefig')
    @patch('builtins.open', new_callable=MagicMock)
    def test_generate_summary_report(self, mock_open, mock_savefig):
        report_path = generate_summary_report(self.transactions)
        self.assertTrue(report_path.endswith('financial_summary.png'))
        mock_savefig.assert_called_once()
        mock_open.assert_called_once()

    @patch('matplotlib.pyplot.savefig')
    def test_generate_detailed_report(self, mock_savefig):
        report_paths = generate_detailed_report(self.transactions)
        self.assertEqual(len(report_paths), 2)
        self.assertTrue(report_paths[0].endswith('category_breakdown.png'))
        self.assertTrue(report_paths[1].endswith('balance_over_time.png'))
        self.assertEqual(mock_savefig.call_count, 2)

if __name__ == '__main__':
    unittest.main()