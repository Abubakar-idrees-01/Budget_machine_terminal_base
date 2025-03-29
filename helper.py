import sqlite3


class Helper:
    def choice(self,min,max):
        while True:
            try:
                option=int(input(f"Enter your option {min}-{max}"))
                if min < option <= max:
                    return option
                else:
                    print("Invalid")
                    continue
            except:
                print("Please enter a Digit only!")

    def number_input(self):
        while True:
            try:
                option=int(input("Enter your option: "))
                return option
            except:
                continue
    def price_input(self,value):
        while True:
            try:
                option=int(input(f"Enter your price for {value}: "))
                return option
            except:
                continue

    def full_table_details(self,name): 
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {name}_details")
        rows = cursor.fetchall()

        # Print column names
        columns = [desc[0] for desc in cursor.description]
        print("\t".join(columns))

        # Print each row
        for row in rows:
            print("\t".join(str(value) for value in row))
        conn.close()
    
    def full_table_records(self,name): 
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {name}_records")
        rows = cursor.fetchall()

        # Print column names
        columns = [desc[0] for desc in cursor.description]
        print("\t".join(columns))

        # Print each row
        for row in rows:
            print("\t".join(str(value) for value in row))
        conn.close()
