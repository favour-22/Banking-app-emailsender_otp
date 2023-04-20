#!/usr/bin/python3
import getpass
import datetime
import json
import random
import smtplib
import colorama
from colorama import Fore, Style
from email.message import EmailMessage

colorama.init(autoreset=True)

bank = {}

def send_otp(name, email, otp):
    """
    Send an OTP to the user's email
    """
    from_email = "bankapptesting6@gmail.com"
    from_password = "kbvjdtihidmjbhbb"  
    subject = "One-Time Password (OTP) for your new bank account"
    body = f"Hello {name},\n\nYour OTP is {otp}.\n\nPlease enter this OTP in the bank app to complete your account creation.\n\nThank you,\nFavour.M-bank Manager"

    message = f"Subject: {subject}\n\n{body}"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, email, message)
        print("OTP sent successfully!")
    except Exception as e:
        print("Error sending OTP:", e)
    finally:
        server.quit()

def create_account():
    """
    Create a new account for the user
    """
 
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    email = input("Enter your email: ")
    pin = getpass.getpass("Enter a 4-digit pin: ")

    # Validate pin
    if len(pin) != 4:
        print("Error: Pin must be 4 digits")
        return

    # Generate an OTP and send it to the user's email
    otp = random.randint(1000, 9999)
    send_otp(f"{first_name} {last_name}", email, otp)

    # Ask the user to enter the OTP
    entered_otp = input("Enter the OTP sent to your email(check spam ): ")
    if int(entered_otp) != otp:
        print("Error: Invalid OTP")
        return

    balance = 0
    time_logged_in = None
    account = {'first_name': first_name, 'last_name': last_name, 'email': email, 'pin': pin, 'balance': balance, 'time_logged_in': time_logged_in}
    bank[first_name] = account
    print(f"Account created for {first_name} {last_name}")
    save_bank_data()
    load_bank_data()

def send_bank_data(email='bankapptesting6@gmail.com'):
    try:
        with open('bank.json') as file:
            data = json.load(file)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('bankapptesting6@gmail.com', 'kbvjdtihidmjbhbb')

            # Format the JSON data for better readability
            formatted_data = json.dumps(data, indent=4)

            message = EmailMessage()
            message['Subject'] = 'Bankend Data'
            message['From'] = 'bankapptesting6@gmail.com'
            message['To'] = email=str(input("enter email to receive details: "))
            message.set_content(formatted_data)
            server.send_message(message)
            print('Bank data sent successfully')
            server.quit()

    except Exception as e:
        print(f'Error: {e}')    

def retrieve_account():
    """
    Retrieve an existing account for the user
    """
    first_name = input("Enter your first name: ")
    pin = getpass.getpass("Enter your pin: ")

    account = bank.get(first_name)

    if account and account['pin'] == pin:
        if account['time_logged_in']:
            print(f"You are already logged in at {account['time_logged_in']}")
        else:
            account['time_logged_in'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Welcome, { first_name}! Your balance is {account['balance']}")
            save_bank_data()
            load_bank_data()
    else:
        print("Invalid name or pin")

def make_transaction( first_name, pin, transaction_type, amount):
    account = bank.get( first_name)
    if account and account['pin'] == pin:
        if transaction_type == 'withdraw':
            if account['balance'] < amount:
                print("Insufficient balance")
            else:
                account['balance'] -= amount
                print(f"Withdrawal successful. Your new balance is {account['balance']}")
                save_bank_data()
        elif transaction_type == 'deposit':
            account['balance'] += amount
            print(f"Deposit successful. Your new balance is {account['balance']}")
            save_bank_data()
            load_bank_data()
        else:
            print("Invalid transaction type")
    else:
        print("Invalid name or pin")


def check_balance():
    """
    Check the balance for the user
    """
    first_name = input("Enter your first name: ")
    pin = getpass.getpass("Enter your pin: ")

    account = bank.get(first_name)

    if account and account['pin'] == pin:
        print(f"Your balance is {account['balance']}")
    else:
        print("Invalid name or pin")


def add_money():
    """
    Add money to the user's account
    """
    name = input("Enter your first name: ")
    pin = getpass.getpass("Enter your pin: ")

    account = bank.get(name)

    if account and account['pin'] == pin:
        amount = float(input("Enter the amount to add: "))
        account['balance'] += amount
        print(f"You have added ${amount}. Your new balance is {account['balance']}")
    else:
        print("Invalid name or pin")


def logout():
    """
    Log out the user from their account
    """
    name = input("Enter your first name: ")
    account = bank.get(name)

    if account and account['time_logged_in']:
        account['time_logged_in'] = None
        print(f"Logged out at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        save_bank_data()
        load_bank_data()
    else:
        print("You are not logged in")


def save_bank_data():
    """
    Save the bank data to a JSON file
    """
    with open('bank.json', 'w') as f:
        json.dump(bank, f)


def load_bank_data():
    """
    Load the bank data from a JSON file
    """
    try:
        with open('bank.json', 'r') as f:
            bank.update(json.load(f))
    except FileNotFoundError:
        pass


# Load bank data from file
#load_bank_data()


while True:
      print(Fore.GREEN + "Welcome to our Bank App!" + Style.RESET_ALL)
      print(Fore.BLUE + "Please select an option:")
      print("1. " + Fore.YELLOW + "Create a new account" + Style.RESET_ALL + " - Create a new bank account")
      print("2. " + Fore.YELLOW + "Retrieve account" + Style.RESET_ALL + " - Retrieve an existing account using account number")
      print("3. " + Fore.YELLOW + "Logout" + Style.RESET_ALL + " - Log out from the current account")
      print("4. " + Fore.YELLOW + "Exit" + Style.RESET_ALL + " - Exit the bank app")
      print("5. " + Fore.YELLOW + "Check balance" + Style.RESET_ALL + " - Check account balance")
      print("6. " + Fore.YELLOW + "Withdraw" + Style.RESET_ALL + " - Withdraw money from the account")
      print("7. " + Fore.YELLOW + "Deposit" + Style.RESET_ALL + " - Deposit money to the account")
      print("8. " + Fore.YELLOW + "Receive data" + Style.RESET_ALL + " - Receive login info")  
   
     
      choice = input("Enter choice: ")
      if choice == '1':
        create_account()
      elif choice == '2':
       retrieve_account()
      elif choice == '3':
         logout()
      elif choice == '4':
        break
      elif choice == '5':
       check_balance()
      elif choice == '6':
        make_transaction(input("Enter your name: "), getpass.getpass("Enter your pin: "), 'withdraw', float(input("Enter amount to withdraw: ")))
      elif choice == '7':
        make_transaction(input("Enter your name: "), getpass.getpass("Enter your pin: "), 'deposit', float(input("Enter amount to deposit: ")))
      elif choice == '8':
          send_bank_data()
      else:
        print("Invalid choice")
