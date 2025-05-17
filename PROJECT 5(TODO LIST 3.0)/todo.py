import os
import time
import hashlib
import getpass
from datetime import datetime, timedelta
from cryptography.fernet import Fernet

if os.name == 'nt':
    os.system('cls')
    print("\033[3J", end='')
else:
    os.system('clear')
    print("\033[3J", end='')

curr_dir = os.getcwd()
app_data_dir = f'{curr_dir}/app-data/to-do'
lists_dir = os.path.join(app_data_dir, 'lists')
credentials_dir = os.path.join(app_data_dir, 'credentials')
os.makedirs(lists_dir, exist_ok=True)
os.makedirs(credentials_dir, exist_ok=True)

def load_or_generate_key():
    key_path = os.path.join(credentials_dir, 'key.key')
    if not os.path.exists(key_path):
        key = Fernet.generate_key()
        with open(key_path, 'wb') as f:
            f.write(key)
    else:
        with open(key_path, 'rb') as f:
            key = f.read()
    return key

cipher = Fernet(load_or_generate_key())

CREDENTIALS = {}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_credentials():
    with open(os.path.join(credentials_dir, 'credentials.txt'), 'w') as f:
        for user, hashed in CREDENTIALS.items():
            f.write(f"{user}:{hashed}\n")

def load_credentials():
    path = os.path.join(credentials_dir, 'credentials.txt')
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if ':' in line:
                    user, hashed = line.strip().split(":", 1)
                    CREDENTIALS[user] = hashed

def encrypt_data(data):
    return cipher.encrypt(data.encode())

def decrypt_data(data):
    return cipher.decrypt(data).decode()

def save_tasks_to_file(user_file, tasks):
    with open(user_file, 'wb') as f:
        f.write(encrypt_data("\n".join(tasks)))

def load_tasks_from_file(user_file):
    try:
        with open(user_file, 'rb') as f:
            return decrypt_data(f.read()).splitlines()
    except FileNotFoundError:
        return []

def get_user_file(username):
    return os.path.join(lists_dir, f"tasks_{username}.txt")

hour = datetime.now().hour
greeting = "MORNING" if 4 <= hour < 12 else "AFTERNOON" if 12 <= hour < 17 else "EVENING"

load_credentials()

while True:
    print(f"\nGOOD {greeting} SIR. WHAT WOULD YOU LIKE ME TO DO.")
    print("1. Create a new account")
    print("2. Login")

    try:
        choice = int(input(": "))
    except ValueError:
        print("Please enter a valid number.")
        continue

    if choice == 1:
        username = input("Enter your desired username: ")
        if username in CREDENTIALS:
            print("Username already exists.")
            continue
        password = getpass.getpass("Enter your desired password: ")
        CREDENTIALS[username] = hash_password(password)
        save_credentials()
        print("Account created successfully.")

    elif choice == 2:
        username = input("Enter your username: ")
        if username not in CREDENTIALS:
            print("Username not found.")
            continue

        attempts = 0
        while attempts < 3:
            password = getpass.getpass("Enter your password: ")
            if CREDENTIALS[username] == hash_password(password):
                print("Login successful.\n")
                break
            else:
                attempts += 1
                print(f"Incorrect password. Attempts left: {3 - attempts}")
                if attempts < 3:
                    print("1. Retry password")
                    print("2. Back to Main Menu")
                    print("3. Quit")
                    try:
                        retry_choice = int(input(": "))
                        if retry_choice == 2:
                            break
                        elif retry_choice == 3:
                            print("Goodbye!")
                            quit()
                        elif retry_choice != 1:
                            print("Invalid input. Returning to main menu.")
                            break
                    except ValueError:
                        print("Invalid input. Returning to main menu.")
                        break
        else:
            print("Too many failed attempts.")
            continue

        user_file = get_user_file(username)
        TOTAL, HIGH_PRIORITY, LOW_PRIORITY = [], [], []

        try:
            load_choice = int(input("Load previously saved list? (1 = Yes, 2 = No): "))
            if load_choice == 1:
                TOTAL = load_tasks_from_file(user_file)
                HIGH_PRIORITY = [t for t in TOTAL if t.startswith("High:")]
                LOW_PRIORITY = [t for t in TOTAL if t.startswith("Low:")]
        except ValueError:
            print("Invalid input. Starting with an empty list.")

        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        due_today = []
        due_tomorrow = []

        for task in TOTAL:
            try:
                parts = task.split("|")
                if len(parts) >= 3:
                    task_date = datetime.strptime(parts[1], "%Y-%m-%d").date()
                    if task_date == today:
                        due_today.append(task)
                    elif task_date == tomorrow:
                        due_tomorrow.append(task)
            except Exception:
                continue

        if due_today or due_tomorrow:
            print("\n=== PENDING TASKS ===")
            if due_today:
                print("1. Tasks Due Today:")
                for t in due_today:
                    print(f"- {t}")
            if due_tomorrow:
                print("2. Tasks Due Tomorrow:")
                for t in due_tomorrow:
                    print(f"- {t}")

        while True:
            print("\n1. Add task")
            print("2. Show tasks")
            print("3. Delete task")
            print("4. Clear task list")
            print("5. Pending tasks")
            print("6. Quit")
            cmd = input(": ").strip()

            if cmd == "1":
                try:
                    priority = int(input("1. High priority\n2. Low priority\nChoose: "))
                    task = input("Task: ")
                    date = input("Due Date (YYYY-MM-DD): ")
                    time_ = input("Due Time (HH:MM): ")
                    entry = f"{task}|{date}|{time_}"
                    full_entry = f"{'High' if priority == 1 else 'Low'}: {entry}"
                    TOTAL.append(full_entry)
                    if priority == 1:
                        HIGH_PRIORITY.append(full_entry)
                    else:
                        LOW_PRIORITY.append(full_entry)
                except ValueError:
                    print("Invalid input.")

            elif cmd == "2":
                print("1. High Priority\n2. Low Priority\n3. All Tasks")
                try:
                    v = int(input(": "))
                    task_list = {1: HIGH_PRIORITY, 2: LOW_PRIORITY, 3: TOTAL}.get(v, [])
                    if task_list:
                        for i, task in enumerate(task_list, 1):
                            print(f"{i}. {task}")
                    else:
                        print("No tasks.")
                except ValueError:
                    print("Invalid input.")

            elif cmd == "3":
                print("1. High Priority\n2. Low Priority")
                try:
                    d = int(input("Choose list to delete from: "))
                    task_list = HIGH_PRIORITY if d == 1 else LOW_PRIORITY
                    for i, task in enumerate(task_list, 1):
                        print(f"{i}. {task}")
                    idx = int(input("Enter task number to delete: ")) - 1
                    task_to_remove = task_list.pop(idx)
                    TOTAL.remove(task_to_remove)
                    print("Task deleted.")
                except (ValueError, IndexError):
                    print("Invalid task number.")

            elif cmd == "4":
                print("1. Clear High Priority\n2. Clear Low Priority\n3. Clear All")
                try:
                    c = int(input("Choose option: "))
                    if c == 1:
                        HIGH_PRIORITY.clear()
                        TOTAL = [t for t in TOTAL if not t.startswith("High:")]
                    elif c == 2:
                        LOW_PRIORITY.clear()
                        TOTAL = [t for t in TOTAL if not t.startswith("Low:")]
                    elif c == 3:
                        HIGH_PRIORITY.clear()
                        LOW_PRIORITY.clear()
                        TOTAL.clear()
                except ValueError:
                    print("Invalid input.")

            elif cmd == "5":
                if due_today or due_tomorrow:
                    print("\n=== PENDING TASKS ===")
                    if due_today:
                        print("1. Tasks Due Today:")
                        for t in due_today:
                            print(f"- {t}")
                    if due_tomorrow:
                        print("2. Tasks Due Tomorrow:")
                        for t in due_tomorrow:
                            print(f"- {t}")
                else:
                    print("No pending tasks due today or tomorrow.")

            elif cmd == "6":
                save = input("Save before quitting? (y/n): ").strip().lower()
                if save == 'y':
                    save_tasks_to_file(user_file, TOTAL)
                    print("Tasks saved.")
                print("Goodbye!")
                if hour >= 17:
                    print("GOOD NIGHT SIR. SLEEP WELL!!!!")
                time.sleep(2)
                quit()

            else:
                print("Invalid command.")

    else:
        print("Invalid option. Please enter 1 or 2.")
