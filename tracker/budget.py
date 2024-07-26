from datetime import datetime

class Budget:
    def __init__(self, category, amount, period='monthly'):
        self.category = category
        self.amount = amount
        self.period = period
        self.start_date = datetime.now().replace(day=1)

    def is_exceeded(self, spent_amount):
        return spent_amount > self.amount

    def remaining(self, spent_amount):
        return self.amount - spent_amount