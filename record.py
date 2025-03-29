from datetime import datetime
from user import User
from helper import Helper
import sqlite3

# Database connection
conn = sqlite3.connect("user_data.db")
cursor = conn.cursor()
help = Helper()

class Record(User):
    def __init__(self, name):
        self.name = name
        self.insert_date()

    def today_date(self):
        return datetime.today().strftime("%Y-%m-%d")

    def insert_date(self): 
        today_date = self.today_date()

        # Ensure ID 1 exists in name_details
        cursor.execute(f"SELECT id FROM {self.name}_details WHERE id = 1")
        result = cursor.fetchone()

        if not result:
            cursor.execute(f"""
                INSERT INTO {self.name}_details (id, total_balance, remaining_balance, average_balance) 
                VALUES (1, 0, 0, 0)
            """)
            conn.commit()
            print(f"{today_date} - Welcome Sir")

        # Ensure today's date exists in name_records
        cursor.execute(f"SELECT id FROM {self.name}_records WHERE date = ?", (today_date,))
        result = cursor.fetchone()

        if not result:
            cursor.execute(f"""
                INSERT INTO {self.name}_records (id, date, food, transport, bill, other, total_today) 
                VALUES (1, ?, 0, 0, 0, 0, 0)
            """, (today_date,))
            conn.commit()
        else:
            print(f"{today_date} - Welcome Back Sir")

    def update_value(self, date, column, new_value, table_name):
        # Fetch the existing value
        cursor.execute(f"SELECT {column} FROM {self.name}_{table_name} WHERE date = ?", (date,))
        result = cursor.fetchone()

        if result:
            existing_value = result[0] if result[0] is not None else 0  # Handle NULL case
            updated_value = existing_value + new_value  # Add new value

            # Update the column with the new total
            query = f"UPDATE {self.name}_{table_name} SET {column} = ? WHERE date = ?"
            cursor.execute(query, (updated_value, date))
            conn.commit()

            print(f"Updated {column}: {existing_value} + {new_value} = {updated_value} for date {date}")
        else:
            print(f"Date {date} not found in table {self.name}_{table_name}.")
       
    def update_total_balance(self, new_value):
        cursor.execute(f"SELECT total_balance FROM {self.name}_details WHERE id = 1")
        result = cursor.fetchone()

        if not result:
            print(f"Error: ID 1 not found in {self.name}_details.")
            return

        existing_balance = result[0] if result[0] is not None else 0
        updated_balance = existing_balance + new_value
        existing_balance_1 = result[0] if result[0] is not None else 0
        updated_balance_1 = existing_balance_1 + new_value

        if updated_balance < 0:
            print(f"Error: Invalid amount. Final total_balance cannot be negative.")
            return  

        query = f"UPDATE {self.name}_details SET total_balance = ? WHERE id = 1"
        cursor.execute(query, (updated_balance,))
        conn.commit()
        query = f"UPDATE {self.name}_details SET remaining_balance = ? WHERE id = 1"
        cursor.execute(query, (updated_balance_1,))
        conn.commit()
        print(f"Updated total_balance: {existing_balance} + {new_value} = {updated_balance}")
        print(f"Updated remaining_balance: {existing_balance_1} + {new_value} = {updated_balance_1}")
   
    def update_remaining_balance(self):
        cursor.execute(f"SELECT SUM(total_today) FROM {self.name}_records")
        result = cursor.fetchone()
        total_sum = result[0] if result[0] is not None else 0

        cursor.execute(f"SELECT total_balance FROM {self.name}_details WHERE id = 1")
        result = cursor.fetchone()
        total_balance = result[0] if result and result[0] is not None else 0

        remaining_balance = total_balance - total_sum

        if remaining_balance < 0:
            print("Error: Remaining balance cannot be negative.")
            return False  

        cursor.execute(f"UPDATE {self.name}_details SET remaining_balance = ? WHERE id = 1", (remaining_balance,))
        conn.commit()
        print(f"Updated remaining_balance: {remaining_balance}")
        return True
     
    def update_total_today(self):
        today_date = self.today_date()

        cursor.execute(f"SELECT food, transport, bill, other FROM {self.name}_records WHERE date = ?", (today_date,))
        result = cursor.fetchone()

        if not result:
            print(f"No records found for {today_date}.")
            return False

        food, transport, bill, other = result
        today_total = food + transport + bill + other
        print(f"{today_date}")
        cursor.execute(f"UPDATE {self.name}_records SET total_today = ? WHERE date = ?", (today_total, today_date))
        conn.commit()
        print(f"Updated total_today to {today_total} for {today_date}.")
        return today_date
        
    def get_remaining_balance(self):
        cursor.execute(f"SELECT remaining_balance FROM {self.name}_details WHERE id = 1")
        result = cursor.fetchone()
        
        if result:
            return result[0]  # Return the remaining balance
        else:
            print("Error: ID 1 not found in name_details.")
            return None
    
    def transaction_record(self):
        today_date = self.today_date()
        success = True  # Keeps track of whether transactions should continue

        print("\n🔹 Starting Transaction Recording 🔹")
        remaining=self.get_remaining_balance()
        print(f"Your acount Balance is {remaining}")
        food_price = help.price_input("Food")
        transport_price = help.price_input("Transport")
        bill_price = help.price_input("Bill")
        other_price = help.price_input("Other")
        subtotal=food_price+bill_price+other_price+other_price
        if subtotal<remaining:
            self.update_value(today_date, "food", food_price, "records")
            self.update_value(today_date, "transport", transport_price, "records")
            self.update_value(today_date, "bill", bill_price, "records")
            self.update_value(today_date, "other", other_price, "records")
            self.update_total_today()
            self.update_remaining_balance()
            self.update_average_balance()
            print("Record updated!")
            print("✅ Transaction recording completed.")
        else:
            print("👎 Transaction recording canceled. Invalid Balance")

    def get_balance_details(self):
        cursor.execute(f"SELECT total_balance, remaining_balance, average_balance FROM {self.name}_details WHERE id = 1")
        result = cursor.fetchone()
        
        if result:
            total_balance, remaining_balance, average_balance = result
            print(f"Total Balance: {total_balance}")
            print(f"Remaining Balance: {remaining_balance}")
            print(f"Average Balance: {average_balance}")
            return {
                "Total Balance": total_balance,
                "Remaining Balance": remaining_balance,
                "Average Balance Spent": average_balance
            }
        else:
            print("Error: ID 1 not found in name_details.")
            return None

    def update_average_balance(self):
        cursor.execute(f"SELECT AVG(total_today) FROM {self.name}_records")
        result = cursor.fetchone()
        
        if result and result[0] is not None:
            average_total_today = result[0]
        else:
            average_total_today = 0  # Default if no records exist

        # Update the average_balance column in details table
        cursor.execute(f"UPDATE {self.name}_details SET average_balance = ? WHERE id = 1", (average_total_today,))
        conn.commit()

        print(f"Updated average_balance: {average_total_today}")
        return average_total_today

    def show_full_record_table(self):
        cursor.execute(f"SELECT * FROM {self.name}_records")
        records = cursor.fetchall()

        if not records:
            print("No records found.")
            return

        # Get column names for better readability
        cursor.execute(f"PRAGMA table_info({self.name}_records)")
        columns = [col[1] for col in cursor.fetchall()]

        # Print the records in a structured table format
        print("\nFull Records Table:\n" + "-" * 65)
        print("\t".join(columns))  # Print column headers
        print("-" * 65)

        for row in records:
            print("\t".join(str(value) for value in row))  # Print row values

        print("-" * 65)
