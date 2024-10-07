from abc import ABC
from datetime import datetime

class User(ABC):

    def __init__(self, name, email, address, account_type) -> None:
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type


class UserAction(User):

    def __init__(self, name, email, address, account_type) -> None:
        super().__init__(name, email, address, account_type)
        self.__balance = 0
        self.account_number = account_type[:3].upper() + email[:3].upper()
        admin.account_info[self.account_number] = self
        self.transaction_history = []
        self.loan_count = 0
        self.is_loan_feature = True

    def withdraw(self, amount, admin):
        if amount > self.__balance:
            print("Insufficient Balance")
            return
        if admin.bank_is_not_bankrupt(amount) == True and admin.total_balance + admin.total_loan > amount and self.loan_count == 0:
            self.__balance -= amount
            admin.total_balance -=amount
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.transaction_history.append(f"Transaction Type: Withdraw, {amount} has been Debited from your account no :{self.account_number} at {current_time}")
            print(f"{amount} has been withdrawn Successfully\n")
        elif admin.bank_is_not_bankrupt(amount) == True and admin.total_balance + admin.total_loan > amount and self.loan_count > 0:
            self.__balance -= amount
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.transaction_history.append(f"Transaction Type: Withdraw, {amount} has been Debited from your account no :{self.account_number} at {current_time}")
            print(f"{amount} has been withdrawn Successfully\n")
        else:
            print("Bank is Bankrupt, you can't withdraw money\n")

    def deposit(self, amount, bank_admin):
        self.__balance += amount
        bank_admin.total_balance += amount
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_history.append(f"Transaction Type: Deposit, {amount} has been Credited to your account no : {self.account_number} at {current_time}")
        print(f"{amount} has been deposited Successfully !!\n")

    def check_balance(self):
        print(f"Your Current Balance is : {self.__balance}\n")
    
    def print_transaction_history(self):
        print("----- Transaction History -----\n")
        for transaction in self.transaction_history:
            print(transaction)

    def get_loan(self, amount, bank_admin):
        if bank_admin.loan == False:
            print("Loan Feature is turned off by Admin\n")
            return
        if bank_admin.total_balance <= amount and bank_admin.loan == True:
            print("You can't ask more than or equal to the Bank total capital\n")
        else:
            if self.loan_count < 2 and self.is_loan_feature == True and bank_admin.total_balance > amount:
                self.loan_count += 1
                self.__balance += amount
                bank_admin.check_total_loan(amount)
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.transaction_history.append(f"Transaction Type: Loan, {amount} has been deposited to your account no {self.account_number} at {current_time}")
                print(f"Loan of {amount} has been approved and deposited to your account\n")
            else:
                print("You have already taken 2 loans\n")

    def transfer_money(self, amount, to_account):
        if amount > self.__balance:
            print("Insufficient Balance")
            return 
        self.__balance -= amount
        to_account.__balance += amount
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_history.append(f"Transaction Type: Transfer, {amount} has been transfered to account no :{self.to_account} at {current_time}")
        print(f"Amount :{amount} has been transferred to account number : {to_account.account_number}successfully")

class Admin(User):
    
    account_info = {} # {account_number: object of user}
    def __init__(self, name, email, address, account_type) -> None:
        super().__init__(name, email, address, account_type)
        # self.account_info = {} # {account_number: object of Account}
        # self.account_info[self.account_number] = self
        self.account_number = account_type[:3].upper() + email[:3].upper()
        self.account_info[self.account_number] = self
        self.total_balance = 100000
        self.total_loan = 0
        self.is_bankrupt = False
        self.loan = True
    
    def add_user(self, name, email, address, account_type):
        return UserAction(name, email, address, account_type)

    def delete_user(self, account_number):
        del self.account_info[account_number]

    def get_all_users(self):
        print("----- All Users -----\n")
        for account_no, user in self.account_info.items():
            print(f"Account Number : {account_no}")
            print(f"Account Name :{user.name}")
            print(f"Account Email :{user.email}")
            print(f"Account Address :{user.address}")
            print(f"Account Type :{user.account_type}")
            print()
    
    def total_balance_of_bank(self):
        print(f"Total Balance of the bank is : {self.total_balance}\n")

    def check_total_loan(self, amount):
        self.total_balance -=amount
        self.total_loan += amount
        
    def get_total_loan_amount(self):
        print(f"Total Laon amount of the bank is : {self.total_loan}\n")

    def turn_off_loan_feature(self):
        self.loan = False

    def turn_on_loan_feature(self):
        self.loan = True

    def bank_is_not_bankrupt(self, amount):
        if amount > self.total_balance:
           return False
        else:
            return True


# admin = Admin("admin", 'admin@gmail.com', "Dhaka", "Admin_Acc")
# user = admin.add_user("Rahim", "rahim@gmail.com", "Dhaka", "Savings")
# admin.get_all_users()
# user.get_loan(1000, admin)
# print(admin.get_total_loan_amount())
# print(admin.total_balance_of_bank())
# print(user.check_balance())


admin = Admin('admin', "admin@gmail.com", "Dhaka", "Admin_Acc")

print("Welcome to Bank Management System\n")

while True:
    print("1. Admin Login")
    print("2. User Login")
    print("3. Exit from System")
    print()
    choice = input("Enter your choice: ")

    if choice == "1":

        user_name = input("Enter your User Name: ")
        password = input("Enter your password: ")
        print()
        if user_name == "admin" and password == "admin":
            print("Welcome to Admin Panel\n")

            while True:
                print("1. Add User")
                print("2. Delete User")
                print("3. Get all User")
                print("4. Get total balance of Bank")
                print("5. Get Total loan Amount")
                print("6. Turn on Loan Feature")
                print("7. Turn off Loan Feature")
                print("8. Logout")
                print()
                choice = input("Enter your choice : ")
                print()

                if choice == "1":
                    name = input("Enter user full name: ")
                    email = input("Enter user email: ")
                    address = input("Enter user address: ")
                    account_type = input("Enter user account type: ")
                    admin.add_user(name, email, address, account_type)
                    print("User Added Successfully !!")
                    print()

                elif choice == "2":
                    account_number = input("Enter account number : ")
                    if account_number in admin.account_info:
                        admin.delete_user(account_number)
                        print("User Deleted Successfully !!")
                    else:
                        print("User not found !!")
                    print()
                elif choice == "3":
                    admin.get_all_users()
                    print()
                elif choice == "4":
                    admin.total_balance_of_bank()
                    print()
                elif choice == "5":
                    admin.get_total_loan_amount()
                    print()
                elif choice == "6":
                    admin.turn_on_loan_feature()
                    print("Loan Feature Turned on Successfully !!")
                    print()
                elif choice == "7":
                    admin.turn_off_loan_feature();
                    print("Loan Feature Turned off Successfully !!")
                    print()
                elif choice == "8":
                    break
                else:
                    print("Invalid Choice !!\n")
    elif choice == "2":

        print("Welcome to the User Panel\n")

        while True:
            print("1. Create Account")
            print("2. Deposit to the Account")
            print("3. Withdraw from the Account")
            print("4. Check Balance of the Account")
            print("5. Get Loan")
            print("6. Get the Transaction History")
            print("7. Transfer Money")
            print("8. Logout")
            print()
            choice = input("Enter your choice : ")

            if choice == "1":
                name = input("Enter your Full Name : ")
                email = input("Enter your email address : ")
                address = input("Enter your address : ")
                account_type = input("Enter your account Type : ")
                UserAction(name, email, address, account_type)
                print()
                print("Account Created Successfully !!\n")
            elif choice == "2":
                account_number = input("Enter your account number : ")
                amount = int(input("Enter the amount that you want to deposit : "))
                print()
                if account_number in admin.account_info:
                    user = admin.account_info[account_number]
                    user.deposit(amount, admin)
                else:
                    print("Account not found !!")
                print()
            elif choice == "3":
                account_number = input("Enter your account number : ")
                amount = int(input("Enter the amount that you want to withdraw : "))
                print()
                if account_number in admin.account_info:
                    user = admin.account_info[account_number]
                    user.withdraw(amount, admin)
                else:
                    print("Account not found !!")
                print()
            elif choice == "4":
                account_number = input("Enter your account number : ")
                print()
                if account_number in admin.account_info:
                    user = admin.account_info[account_number]
                    user.check_balance()
                else:
                    print("Account not found !!")
                print()
            elif choice == "5":
                account_number = input("Enter your account number : ")
                amount = int(input("Enter the amount that you want to get as a loan : "))
                print()
                if account_number in admin.account_info:
                    user = admin.account_info[account_number]
                    user.get_loan(amount, admin)
                else:
                    print("Account not found !!")
                print()
            elif choice == "6":
                account_number = input("Enter your account number : ")
                print()
                if account_number in admin.account_info:
                    user = admin.account_info[account_number]
                    user.print_transaction_history()
                else:
                    print("Account not found !!")
                print()

            elif choice == "7":
                account_number = input("Enter your account number : ")
                to_account_number = input("Enter the account number where you want to transfer : ")
                amount = int(input("Enter the amount that you want to tranfer : "))
                print()
                if account_number in admin.account_info and to_account_number in admin.account_info and account_number != to_account_number:
                    user = admin.account_info[account_number]
                    to_account = admin.account_info[to_account_number]
                    user.transfer_money(amount, to_account)
                else:
                    print("Account not found !!\n")
            elif choice == "8":
                break
            else:
                print("Invalid Choice !!\n")

    elif choice == "3":
        break
    else:
        print("Invalid Choice !!\n")
