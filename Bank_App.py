import os, random, string

# 🌍 Global variables
balance = []
generated_key = None
access_granted = False

# 🔐 Generate a secure key
def generate_random_key(length=13):
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    random.seed(os.urandom(1024))
    return ''.join(random.choice(chars) for _ in range(length))

def generate_key():
    global generated_key
    generated_key = generate_random_key()
    print(f"🔐 Your generated key is: {generated_key}")
    print("Save this key! You'll need it to access your balance.")

def input_key():
    global access_granted
    if not generated_key:
        print("❌ No key has been generated yet. Please generate a key first.")
        return

    user_input = input("Enter your access key: ")
    if user_input == generated_key:
        access_granted = True
        print("✅ Access granted! You can now access all features.")
    else:
        print("❌ Incorrect key. Try again.")

def add_money():
    if not access_granted:
        print("🔒 Access denied. You must input the correct key first.")
        return
    try:
        add_balance = float(input("Add Money: "))
        balance.append(add_balance)
        print(f"You Added {add_balance}")
    except ValueError:
        print("Please only enter numbers.")

def withdraw_money():
    if not access_granted:
        print("🔒 Access denied. You must input the correct key first.")
        return
    try:
        amount = float(input("Withdraw Amount: "))
        if amount <= sum(balance):
            balance.append(-amount)
            print(f"You withdrew {amount}")
        else:
            print("❌ Insufficient funds.")
    except ValueError:
        print("Please enter a valid number.")

def show_balance():
    if not access_granted:
        print("🔒 Access denied. You must input the correct key first.")
        return

    print(f"Your current balance is: {sum(balance)}")
    while True:
        go_back = input("Go back to dashboard? (yes/no): ").strip().lower()
        if go_back == "yes":
            break
        elif go_back == "no":
            print("Okay, staying on balance screen.")
        else:
            print("Please enter 'yes' or 'no'.")

def dashboard():
    while True:
        print("\n=== DASHBOARD ===")
        print("1. Generate Random Key")
        print("2. Input Random Key")
        print("3. Show Balance")
        print("4. Add Money")
        print("5. Withdraw Money")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            generate_key()
        elif choice == "2":
            input_key()
        elif choice == "3":
            show_balance()
        elif choice == "4":
            add_money()
        elif choice == "5":
            withdraw_money()
        elif choice == "6":
            print("👋 Exiting... Bye!")
            break
        else:
            print("❌ Invalid choice.")

# 🚀 Start the app
dashboard()





