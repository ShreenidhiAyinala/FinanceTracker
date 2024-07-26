import unittest
from tracker.transaction import Transaction

class TestTransaction(unittest.TestCase):
    def test_transaction_creation(self):
        t = Transaction(100, "Food", "Dinner", "2024-07-24", "expense", ["restaurant", "dinner"])
        self.assertEqual(t.amount, 100)
        self.assertEqual(t.category, "Food")
        self.assertEqual(t.description, "Dinner")
        self.assertEqual(t.date, "2024-07-24")
        self.assertEqual(t.transaction_type, "expense")
        self.assertEqual(t.tags, ["restaurant", "dinner"])

    def test_to_dict(self):
        t = Transaction(100, "Food", "Dinner", "2024-07-24", "expense", ["restaurant", "dinner"])
        d = t.to_dict()
        self.assertEqual(d["amount"], 100)
        self.assertEqual(d["category"], "Food")
        self.assertEqual(d["description"], "Dinner")
        self.assertEqual(d["date"], "2024-07-24")
        self.assertEqual(d["transaction_type"], "expense")
        self.assertEqual(d["tags"], ["restaurant", "dinner"])

    def test_from_dict(self):
        d = {
            "amount": 100,
            "category": "Food",
            "description": "Dinner",
            "date": "2024-07-24",
            "transaction_type": "expense",
            "tags": ["restaurant", "dinner"]
        }
        t = Transaction.from_dict(d)
        self.assertEqual(t.amount, 100)
        self.assertEqual(t.category, "Food")
        self.assertEqual(t.description, "Dinner")
        self.assertEqual(t.date, "2024-07-24")
        self.assertEqual(t.transaction_type, "expense")
        self.assertEqual(t.tags, ["restaurant", "dinner"])

    def test_str_representation(self):
        t = Transaction(100, "Food", "Dinner", "2024-07-24", "expense")
        self.assertEqual(str(t), "2024-07-24 - Expense: $100.00 (Food) - Dinner")

if __name__ == '__main__':
    unittest.main()