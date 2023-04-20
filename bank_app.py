import getpass
import datetime
import json
import random
import smtplib

bank = {}

def send_otp(name, email, otp):
    """
    Send an OTP to the user's email
    """
    from_email = "bankapptesting6@gmail.com" 
    from_password = "bankapp@121"  

    subject = "One-Time Password (OTP) for your new bank account"
    body = f"Hello {name},\n\nYour OTP is {otp}.\n\nPlease enter this OTP in the bank app to complete your account creation.\n\nThank you,\nFavour.M{bank Manager]"

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
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    pin = getpass.getpass("Enter a 4-digit pin: ")

    # Validate pin
    if len(pin) != 4:
        print("Error: Pin must be 4 digits")
        return

    # Generate an OTP and send it to the user's email
    otp = random.randint(1000, 9999)
    send_otp(name, email, otp)

    # Ask the user to enter the OTP
    entered_otp = input("Enter the OTP sent to your email: ")
    if int(entered_otp) != otp:
        print("Error: Invalid OTP")
        return

    balance = 0
    time_logged_in = None
    account = {'name': name, 'email': email, 'pin': pin, 'balance': balance, 'time_logged_in': time_logged_in}
    bank[name] = account
    print(f"Account created for {name}")
    save_bank_data()


def retrieve_account():
    """
    Retrieve an existing account for the user
    """
    name = input("Enter your name: ")
    pin = getpass.getpass("Enter your pin: ")

    account = bank.get(name)

    if account and account['pin'] == pin:
        if account['time_logged_in']:
            print(f"You are already logged in at {account['time_logged_in']}")
        else:
            account['time_logged_in'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Welcome, {name}! Your balance is {account['balance']}")
            save_bank_data()
    else:
        print("Invalid name or pin")

def make_transaction(name, pin, transaction_type, amount):
    account = bank.get(name)
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
        else:
            print("Invalid transaction type")
    else:
        print("Invalid name or pin")


def check_balance():
    """
    Check the balance for the user
    """
    name = input("Enter your name: ")
    pin = getpass.getpass("Enter your pin: ")

    account = bank.get(name)

    if account and account['pin'] == pin:
        print(f"Your balance is {account['balance']}")
    else:
        print("Invalid name or pin")


def add_money():
    """
    Add money to the user's account
    """
    name = input("Enter your name: ")
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
    name = input("Enter your name: ")
    account = bank.get(name)

    if account and account['time_logged_in']:
        account['time_logged_in'] = None
        print(f"Logged out at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        save_bank_data()
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
      print("1. Create account")
      print("2. Retrieve account")
      print("3. Logout")
      print("4. Exit")
      print("5. check_balnce")
      print("6. withdraw")
      print("7. deposite")
     
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
      else:
        print("Invalid choice")
