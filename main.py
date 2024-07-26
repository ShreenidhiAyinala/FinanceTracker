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
        print("11. Set Budget")
        print("12. Check Budget Status")
        print("13. Generate Trend Analysis")
        print("14. Generate Category Comparison")
        print("15. Advanced Search")
        print("16. Check Notifications")
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
        elif choice == "11":
            category = input("Enter category for budget: ")
            amount = float(input("Enter budget amount: "))
            period = input("Enter budget period (daily/weekly/monthly): ")
            tracker.set_budget(category, amount, period)
        elif choice == "12":
            tracker.check_budget_status()
        elif choice == "13":
            tracker.generate_trend_analysis()
        elif choice == "14":
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            tracker.generate_category_comparison(start_date, end_date)
        elif choice == "15":
            print("\n--- Advanced Search ---")
            start_date = input("Enter start date (YYYY-MM-DD) or press enter to skip: ") or None
            end_date = input("Enter end date (YYYY-MM-DD) or press enter to skip: ") or None
            category = input("Enter category or press enter to skip: ") or None
            tags = input("Enter tags (comma-separated) or press enter to skip: ")
            tags = tags.split(',') if tags else None
            min_amount = input("Enter minimum amount or press enter to skip: ")
            min_amount = float(min_amount) if min_amount else None
            max_amount = input("Enter maximum amount or press enter to skip: ")
            max_amount = float(max_amount) if max_amount else None

            results = tracker.advanced_search(start_date, end_date, category, tags, min_amount, max_amount)
            
            if results:
                print("\nSearch Results:")
                for transaction in results:
                    print(transaction)
            else:
                print("No transactions found matching the search criteria.")
            pass
        elif choice == "16":
            tracker.check_notifications()
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main_menu()