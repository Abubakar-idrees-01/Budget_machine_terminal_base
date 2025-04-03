import sqlite3

conn=sqlite3.connect("user_data.db")
cursor=conn.cursor() 

class User:
    def __init__(self):
        
        cursor.execute("""  
            CREATE TABLE IF NOT EXISTS user_details(  
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                name TEXT NOT NULL UNIQUE,   
                email TEXT NOT NULL UNIQUE,  
                password TEXT NOT NULL  
            )  
        """)  
        conn.commit()
   
    def Signup(self):
        self.name=self.get_name_signup()
        self.email=self.get_email_signup()
        self.password=self.get_password_signup()
        cursor.execute("INSERT INTO user_details (name, email, password) VALUES (?, ?, ?)",  
                           (self.name, self.email, self.password))  
        cursor.execute(f"""  
                CREATE TABLE IF NOT EXISTS {self.name}_records(  
                    id INTEGER PRIMARY KEY AUTOINCREMENT,  
                    date TEXT NOT NULL UNIQUE,   
                    food INTEGER,      
                    transport INTEGER,      
                    bill INTEGER,      
                    other INTEGER,
                    total_today INTEGER   
                )  
            """)  
        cursor.execute(f"""  
                CREATE TABLE IF NOT EXISTS {self.name}_details(  
                    id INTEGER ,
                    total_balance INTEGER,      
                    remaining_balance INTEGER,      
                    average_balance INTEGER    
                )  
            """)  

        conn.commit()
        print(f"✅ {self.name}, New user Added.")
    
    def Signin(self):
        name = self.get_name_signin()
        if name=="exit":
            return 0
        if name:
            if self.get_password_signin(name):
                print(f"✨Welcome back, {name.title()}!")
                return name
            else:
                print("Returning")
    
    def get_name_signup(self):
        cursor.execute("SELECT * FROM user_details")
        members = cursor.fetchall()

        while True:  
            name = input("\nEnter user name: ").lower().strip()
            if any(name == member[1] for member in members):
                print("❌ User name already exists, Try again..")
            else:
                return name
    
    def get_name_signin(self):
        cursor.execute("SELECT * FROM user_details")
        members = cursor.fetchall()
        while True:  
            name = input("\nEnter user name or X to exit: ").lower().strip()
            if any(name == member[1] for member in members):
                print("✅ Name Found.")
                return name
            elif name=="x":
                print("Returning")
                return "exit"

            else:
                print("❌ Name not found")
    
    def get_email_signup(self):
        cursor.execute("SELECT * FROM user_details")
        members = cursor.fetchall()

        while True:
            email = input("\nEnter user email: ").lower().strip()
            if "@" not in email:
                print("❌ Invalid email, try again.")
                continue
            
            if any(email == member[2] for member in members):
                print("❌ User email already exists, try again.")
            else:
                return email
    
    def get_email_signin(self):
        cursor.execute("SELECT * FROM user_details")
        members = cursor.fetchall()
        while True:
            email = input("\nEnter user email or x to exit: ").lower().strip()
            if any(email == member[2] for member in members):
                print("✅ User email Found.")
                return email
            elif email=="x":
                return "exit"
            else:
                print("❌ Email not found")

    def get_password_signup(self):
        while True:
            password = input("\nEnter user password: ").strip()
            if len(password) <8:
                print("🎈Your password must be greater than 8 characters.")
                continue

            check_password = input("\nEnter password again: ").strip()
            if password != check_password:
                print("❌ Passwords do not match, try again.")
                continue

            print("✅ Password matched!")
            return password

    def get_password_signin(self, username):
        cursor.execute("SELECT password FROM user_details WHERE name = ?", (username,))
        result = cursor.fetchone()
        if result:
            stored_password = result[0]
            while True:
                password = input("\nEnter your password : ").strip()
                if password == stored_password:
                    print("✅ Login successful!")
                    return True
                elif password=="Y":
                    password=self.forget_password(username)
                    return True
                elif password=="E":
                    return False  
                else:
                    print("❌ Incorrect password, try again or recover password (Y/N) or Exit (E).")
        else:
            print("❌ Username not found.")
            return False

    def forget_password(self,name):
        email=self.get_email_signin()
        if email=="exit":
            return 0
        cursor.execute("SELECT password FROM user_details WHERE name = ? AND email = ?", (name, email))
        result = cursor.fetchone()
        if result:
            print(f"✅ Password: {result[0]}")
            return result[0]
        else:
            print("❌ User not found!")

    def User_list(self):
        cursor.execute("SELECT * FROM user_details")
        members=cursor.fetchall()

        for member in members:
            print(f"{member[0]}- {member[1].title()} | {member[2]} | {member[3]}")
