from tracker.finance_tracker import FinanceTracker
import argparse

def main_menu():
    tracker = FinanceTracker()
    while True:
        print("\n--- Finance Tracker ---")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. View Balance")
        print("4. Generate Category Report")
        print("5. Generate Monthly Report")
        print("6. Add Recurring Transaction")
        print("7. Process Recurring Transactions")
        print("8. Export to CSV")
        print("9. Clear All Transactions")
        print("10. Save and Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            description = input("Enter description: ")
            trans_type = input("Enter type (income/expense): ")
            tags = input("Enter tags (comma-separated): ").split(',')
            tracker.add_transaction(amount, category, description, trans_type, tags)
        elif choice == "2":
            tracker.process_recurring_transactions()
            start_date = input("Enter start date (YYYY-MM-DD) or press enter to skip: ")
            end_date = input("Enter end date (YYYY-MM-DD) or press enter to skip: ")
            category = input("Enter category to filter by or press enter to skip: ")
            tracker.view_transactions(start_date or None, end_date or None, category or None)
        elif choice == "3":
            balance = tracker.calculate_balance()
            print(f"Current balance: ${balance:.2f}")
        elif choice == "4":
            tracker.generate_category_report()
        elif choice == "5":
            tracker.generate_monthly_report()
        elif choice == "6":
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            description = input("Enter description: ")
            trans_type = input("Enter type (income/expense): ")
            frequency = input("Enter frequency (daily/weekly/monthly): ")
            tracker.add_transaction(amount, category, description, trans_type, recurring=True, frequency=frequency)
        elif choice == "7":
            tracker.process_recurring_transactions()
            print("Recurring transactions processed.")
        elif choice == "8":
            filename = input("Enter the filename for the CSV export: ")
            tracker.export_to_csv(filename)
        elif choice == "9":
            tracker.clear_transactions()
        elif choice == "10":
            tracker.save_data()
            print("Data saved. Exiting program.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main_menu()