from typing import List
from datetime import datetime

class Transaction:
    def __init__(self, amount: float, category: str, description: str, 
                 date: str = None, transaction_type: str = "expense", 
                 tags: List[str] = None):
        self.amount: float = float(amount)
        self.category: str = category
        self.description: str = description
        self.date: str = date or datetime.now().strftime("%Y-%m-%d")
        self.transaction_type: str = transaction_type
        self.tags: List[str] = tags or []

    def to_dict(self) -> dict:
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
            "transaction_type": self.transaction_type,
            "tags": self.tags
        }

    @staticmethod
    def from_dict(data: dict) -> 'Transaction':
        return Transaction(
            amount=data["amount"],
            category=data["category"],
            description=data["description"],
            date=data["date"],
            transaction_type=data["transaction_type"],
            tags=data.get("tags", [])
        )

    def __str__(self) -> str:
        return f"{self.date} - {self.transaction_type.capitalize()}: ${self.amount:.2f} ({self.category}) - {self.description}"