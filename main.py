from user import User
from record import Record
from helper import Helper

help=Helper()
person=User()

class budget_machine:
    def __init__(self):
        while True:
            print("\n***Welcome to Budget Machine***")
            print(" 1-Sign In")
            print(" 2-Sign Up")
            print(" 3-Exit")
            option=help.number_input()
            match option:
                case 1:
                    name=person.Signin()
                    if name:
                        record=Record(name)
                    else:
                        continue
                    while True:
                        print("\n**Sign-in Section**")
                        print(" 1-Add amount")
                        print(" 2-Withdraw amount")
                        print(" 3-Show Account Details")
                        print(" 4-Add Record for today")
                        print(" 5-Full Record")
                        print(" 7-Exit..")
                        option=help.number_input()
                        match option:
                            case 1:
                                print("\n *Amount Adding section*")
                                amount=help.number_input()
                                record.update_total_balance(amount)
                            case 2:
                                print("\n *Amount withdrawing section*")
                                amount=help.number_input()
                                record.update_total_balance(-amount)
                            case 3:
                                print("\n *Account Detail section*")
                                record.get_balance_details()
                            case 4:
                                print("\n *Transaction Record section*")
                                record.transaction_record()
                            case 5:
                                print("\n *Transaction Record section*")
                                record.show_full_record_table()
                            case 6:
                                print("Returing...")
                                break
                            case _:
                                print("\nInvalid opiton..")
                               
                case 2:
                    print("\n**Sign-up Section**")
                    person.Signup()
                    print("Returing to main menu..")
                case 3:
                    print("\nGood-Bye Sir")
                    break
                case _:
                    print("\nInvalid opiton..")


start=budget_machine()