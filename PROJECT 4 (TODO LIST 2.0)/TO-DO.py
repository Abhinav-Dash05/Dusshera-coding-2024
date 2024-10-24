from cryptography.fernet import Fernet
from datetime import datetime as dt
import hashlib
import time
import os

# Initialize user lists
USERID = []
PASS = []

# Base directory for app data
app_data_dir = 'app_data/to-do'

# Create 'app_data/to-do/lists' and 'app_data/to-do/credentials' folders if they don't exist
lists_dir = os.path.join(app_data_dir, 'lists')
credentials_dir = os.path.join(app_data_dir, 'credentials')

if not os.path.exists(lists_dir):
    os.makedirs(lists_dir)
if not os.path.exists(credentials_dir):
    os.makedirs(credentials_dir)

# Generate or load encryption key for tasks
def load_or_generate_key():
    key_file = os.path.join(credentials_dir, 'key.key')
    if not os.path.exists(key_file):
        key = Fernet.generate_key()
        with open(key_file, 'wb') as keyfile:
            keyfile.write(key)
    else:
        with open(key_file, 'rb') as keyfile:
            key = keyfile.read()
    return key

# Initialize Fernet with the loaded key
key = load_or_generate_key()
cipher = Fernet(key)

# Function to hash passwords (non-reversible)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to encrypt data (reversible)
def encrypt_data(data):
    return cipher.encrypt(data.encode())

# Function to decrypt data
def decrypt_data(data):
    return cipher.decrypt(data).decode()

# Function to save encrypted tasks to a file
def save_tasks_to_file(user_file, tasks):
    encrypted_tasks = encrypt_data("\n".join(tasks))
    with open(user_file, 'wb') as file:
        file.write(encrypted_tasks)

# Function to load encrypted tasks from a file
def load_tasks_from_file(user_file):
    try:
        with open(user_file, 'rb') as file:
            encrypted_data = file.read()
            decrypted_data = decrypt_data(encrypted_data)
            tasks = decrypted_data.splitlines()
            return tasks
    except FileNotFoundError:
        print("No saved file found. Starting with an empty list.")
        return []

# Function to save credentials
def save_credentials():
    with open(os.path.join(credentials_dir, 'usernames.txt'), 'w') as user_file:
        for userid in USERID:
            user_file.write(f"{userid}\n")
    with open(os.path.join(credentials_dir, 'passwords.txt'), 'w') as pass_file:
        for password in PASS:
            pass_file.write(f"{password}\n")

# Load usernames and passwords from files
def load_credentials():
    try:
        with open(os.path.join(credentials_dir, 'usernames.txt'), 'r') as user_file:
            for line in user_file:
                USERID.append(line.strip())
    except FileNotFoundError:
        print("No usernames file found. CREATE ONE NOW!")

    try:
        with open(os.path.join(credentials_dir, 'passwords.txt'), 'r') as pass_file:
            for line in pass_file:
                PASS.append(line.strip())
    except FileNotFoundError:
        print("No passwords file found. CREATE ONE NOW!")

# Function to generate user-specific file name
def get_user_file(login_userid):
    return os.path.join(lists_dir, f"tasks_{login_userid}.txt")

# Load credentials at the start
load_credentials()
time1 = dt.now()
real_time = time1.strftime("%H:%M:%S")

part_time = real_time.partition(":")
hour = int(part_time[0])

if 12 > hour >= 4:
    greeting = "MORNING"
elif 17 > hour >= 12:
    greeting = "AFTERNOON"
else:
    greeting = "EVENING"

while True:
    print(f"GOOD {greeting} SIR. WHAT WOULD YOU LIKE ME TO DO.")
    print("PRESS 1 TO CREATE A NEW ACCOUNT.")
    print("PRESS 2 TO LOGIN")
    login_prompt = int(input(": "))

    if login_prompt == 1:
        print("ENTER YOUR DESIRED USERNAME")
        new_userid = input(": ")
        hashed_userid = hash_password(new_userid)
        USERID.append(hashed_userid)
        print("ENTER YOUR DESIRED PASSWORD")
        new_pass = input(": ")
        hashed_pass = hash_password(new_pass)
        PASS.append(hashed_pass)
        print("YOUR USERID AND PASSWORD HAVE BEEN SAVED.")
        save_credentials()
    elif login_prompt == 2:
        print("ENTER YOUR USERID")
        login_userid = hash_password(input(": "))
        print("ENTER YOUR PASSWORD")
        login_pass = hash_password(input(": "))
        if login_userid in USERID and login_pass in PASS:
            print("Credentials matched. Logging you in...")
            time.sleep(1.5)  # Adding a brief pause for better user experience
            os.system('cls' if os.name == 'nt' else 'clear')

            # Initialize lists
            TOTAL = []
            HIGH_PRIORITY = []
            LOW_PRIORITY = []
            fixed_operator = "|"

            # Load tasks for the user
            user_file = get_user_file(login_userid)
            print("Do you want to load any previously stored lists?")
            print("Press 1 for yes")
            print("Press 2 for no")
            load = int(input())
            if load == 1:
                TOTAL = load_tasks_from_file(user_file)
                HIGH_PRIORITY = [task for task in TOTAL if "High:" in task]
                LOW_PRIORITY = [task for task in TOTAL if "Low:" in task]
            elif load == 2:
                print("OKAY STARTING WITH AN EMPTY LIST")
            print("------------------------------------------------------")

            # Task management loop
            while True:
                print("What do you want me to do?")
                print("1. Add a new task (Press 1 and enter)")
                print("2. Display current tasks (Press 2 and enter)")
                print("3. Kill a task (Press 3 and enter)")
                print("4. Clear To-Do List (Press 4 and enter)")
                print("5. Quit (Press 5 and enter)")
                print("------------------------------------------------------")

                user_input_1 = input().strip()

                if user_input_1 == "1":
                    print("Do you want your task to be added as a high priority task or low priority task?")
                    print("Press 1 for high priority")
                    print("Press 2 for low priority")
                    C1 = int(input())
                    TASK = input("Enter task to be added: ")
                    DATE = input("Final date of completion: ")
                    TIME = input("Completion time: ")
                    TASK_DETAILS = f"{TASK}{fixed_operator}{DATE}{fixed_operator}{TIME}"
                    if C1 == 1:
                        HIGH_PRIORITY.append(f"High: {TASK_DETAILS}")
                        TOTAL.append(f"High: {TASK_DETAILS}")
                    elif C1 == 2:
                        LOW_PRIORITY.append(f"Low: {TASK_DETAILS}")
                        TOTAL.append(f"Low: {TASK_DETAILS}")
                    os.system('cls' if os.name == 'nt' else 'clear')

                elif user_input_1 == "2":
                    print("1. High Priority List")
                    print("2. Low Priority List")
                    print("3. All Tasks")
                    C2 = int(input())
                    if C2 == 1:
                        for i, task in enumerate(HIGH_PRIORITY, 1):
                            print(f"{i}: {task}")
                    elif C2 == 2:
                        for i, task in enumerate(LOW_PRIORITY, 1):
                            print(f"{i}: {task}")
                    elif C2 == 3:
                        for i, task in enumerate(TOTAL, 1):
                            print(f"{i}: {task}")
                    os.system('cls' if os.name == 'nt' else 'clear')

                elif user_input_1 == "3":
                    print("1. High priority list")
                    print("2. Low priority list")
                    C3 = int(input())
                    if C3 == 1:
                        for i, task in enumerate(HIGH_PRIORITY, 1):
                            print(f"{i}: {task}")
                        TASK_KILL = int(input("Select the task number to delete: ")) - 1
                        TOTAL.remove(HIGH_PRIORITY[TASK_KILL])
                        HIGH_PRIORITY.pop(TASK_KILL)
                    elif C3 == 2:
                        for i, task in enumerate(LOW_PRIORITY, 1):
                            print(f"{i}: {task}")
                        TASK_KILL = int(input("Select the task number to delete: ")) - 1
                        TOTAL.remove(LOW_PRIORITY[TASK_KILL])
                        LOW_PRIORITY.pop(TASK_KILL)
                    os.system('cls' if os.name == 'nt' else 'clear')

                elif user_input_1 == "4":
                    print("1. Clear High Priority List")
                    print("2. Clear Low Priority List")
                    print("3. Clear All")
                    C4 = int(input())
                    if C4 == 1:
                        HIGH_PRIORITY.clear()
                        TOTAL = [task for task in TOTAL if not task.startswith("High:")]
                    elif C4 == 2:
                        LOW_PRIORITY.clear()
                        TOTAL = [task for task in TOTAL if not task.startswith("Low:")]
                    elif C4 == 3:
                        HIGH_PRIORITY.clear()
                        LOW_PRIORITY.clear()
                        TOTAL.clear()
                    os.system('cls' if os.name == 'nt' else 'clear')

                elif user_input_1 == "5":
                    print("Save your list before quitting?")
                    print("1. Yes")
                    print("2. No")
                    quit_save = int(input())
                    if quit_save == 1:
                        save_tasks_to_file(user_file, TOTAL)
                        print("The list has been saved.")
                    print("Thanks for using. :)")
                    save_credentials()
                    if hour >= 17:
                        print("GOOD NIGHT SIR. SLEEP WELL!!!!")
                    time.sleep(3.5)
                    quit()

                os.system('cls' if os.name == 'nt' else 'clear')

        else:
            print("SORRY! Credentials didn't match. Try to remember them again.")
            time.sleep(1.5)
            os.system('cls' if os.name == 'nt' else 'clear')
