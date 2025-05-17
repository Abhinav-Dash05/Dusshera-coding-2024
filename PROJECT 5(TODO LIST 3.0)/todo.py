import os, time, hashlib, getpass, re
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
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
def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()
def save_credentials():
    with open(os.path.join(credentials_dir, 'credentials.txt'), 'w') as f:
        for u, h in CREDENTIALS.items():
            f.write(f"{u}:{h}\n")
def load_credentials():
    path = os.path.join(credentials_dir, 'credentials.txt')
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if ':' in line:
                    u, h = line.strip().split(':', 1)
                    CREDENTIALS[u] = h
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
def valid_date(date_str):
    return bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}', date_str)) and (lambda d: datetime.strptime(d, '%Y-%m-%d'))(date_str) or False
def valid_time(time_str):
    return bool(re.fullmatch(r'\d{2}:\d{2}', time_str)) and (lambda t: datetime.strptime(t, '%H:%M'))(time_str) or False
def date_split(task):
    priority, rest = task.split(': ', 1)
    parts = rest.split('|')
    if len(parts) == 3:
        parts.append('pending')
    return priority, parts
def format_task_display(task):
    try:
        priority, text = date_split(task)
        task_name, date, time_, status = text
        status_emoji = '✔' if status == 'done' else '⏳'
        return f"{priority} {task_name} (Due {date} {time_}) Status: {status_emoji}"
    except:
        return task
hour = datetime.now().hour
greeting = "MORNING" if 4 <= hour < 12 else "AFTERNOON" if 12 <= hour < 17 else "EVENING"
load_credentials()
while True:
    print(f"\nGOOD {greeting} SIR. Let's log you in to your account.")
    print("1. Create a new account")
    print("2. Login")
    try:
        choice = int(input(": "))
    except:
        print("Please enter a valid number.")
        continue
    if choice == 1:
        username = input("Enter your desired username: ").strip()
        if not username or ':' in username or username in CREDENTIALS:
            print("Invalid or existing username.")
            continue
        password = getpass.getpass("Enter your desired password: ")
        if not password:
            print("Password cannot be empty.")
            continue
        CREDENTIALS[username] = hash_password(password)
        save_credentials()
        print("Account created successfully.")
    elif choice == 2:
        username = input("Enter your username: ").strip()
        if username not in CREDENTIALS:
            print("Username not found.")
            continue
        attempts = 0
        while attempts < 5:
            password = getpass.getpass("Enter your password: ")
            if CREDENTIALS[username] == hash_password(password):
                break
            attempts += 1
            print(f"Incorrect password. Attempts left: {5 - attempts}")
            if attempts < 5:
                print("1. Retry password\n2. Back to Main Menu\n3. Quit")
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
                except:
                    print("Invalid input. Returning to main menu.")
                    break
        else:
            print("Too many failed attempts.")
            continue
        user_file = get_user_file(username)
        TOTAL, HIGH_PRIORITY, LOW_PRIORITY = [], [], []
        try:
            load_choice = int(input("Load previously saved list? (1=Yes, 2=No): "))
            if load_choice == 1:
                TOTAL = load_tasks_from_file(user_file)
                HIGH_PRIORITY = [t for t in TOTAL if t.startswith("High:")]
                LOW_PRIORITY = [t for t in TOTAL if t.startswith("Low:")]
        except:
            print("Invalid input. Starting empty.")
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        due_today, due_tomorrow = [], []
        for task in TOTAL:
            try:
                _, parts = date_split(task)
                task_date = datetime.strptime(parts[1], "%Y-%m-%d").date()
                if task_date == today:
                    due_today.append(task)
                elif task_date == tomorrow:
                    due_tomorrow.append(task)
            except:
                continue
        if due_today or due_tomorrow:
            print("\n=== PENDING TASKS ===")
            if due_today:
                print("1. Tasks Due Today:")
                for t in due_today:
                    print(f"- {format_task_display(t)}")
            if due_tomorrow:
                print("2. Tasks Due Tomorrow:")
                for t in due_tomorrow:
                    print(f"- {format_task_display(t)}")
        while True:
            print("\n=== TODO LIST ===")
            print("What do you want me to do?")
            print("\n1. Add task\n2. Show tasks\n3. Delete task\n4. Clear task list\n5. Quit\n6. Pending tasks\n7. Mark task as done\n8. Edit task")
            cmd = input(": ").strip()
            if cmd not in ["1","2","3","4","5","6","7","8"]:
                print("Invalid command.")
                continue
            if cmd == "1":
                try:
                    priority = int(input("1. High priority\n2. Low priority\nChoose: "))
                    if priority not in [1, 2]:
                        print("Invalid priority.")
                        continue
                    task = input("Task: ").strip()
                    if not task:
                        print("Task cannot be empty.")
                        continue
                    date = input("Due Date (YYYY-MM-DD): ").strip()
                    if not valid_date(date):
                        print("Invalid date format.")
                        continue
                    time_ = input("Due Time (HH:MM): ").strip()
                    if not valid_time(time_):
                        print("Invalid time format.")
                        continue
                    entry = f"{task}|{date}|{time_}|pending"
                    full_entry = f"{'High' if priority == 1 else 'Low'}: {entry}"
                    TOTAL.append(full_entry)
                    if priority == 1:
                        HIGH_PRIORITY.append(full_entry)
                    else:
                        LOW_PRIORITY.append(full_entry)
                except:
                    print("Invalid input.")
            elif cmd == "2":
                print("1. High Priority\n2. Low Priority\n3. All Tasks")
                try:
                    v = int(input(": "))
                    task_list = {1: HIGH_PRIORITY, 2: LOW_PRIORITY, 3: TOTAL}.get(v, [])
                    if task_list:
                        for i, task in enumerate(task_list, 1):
                            print(f"{i}. {format_task_display(task)}")
                    else:
                        print("No tasks.")
                except:
                    print("Invalid input.")
            elif cmd == "3":
                print("1. High Priority\n2. Low Priority")
                try:
                    d = int(input("Choose list to delete from: "))
                    task_list = HIGH_PRIORITY if d == 1 else LOW_PRIORITY if d == 2 else None
                    if not task_list:
                        print("Invalid choice.")
                        continue
                    while task_list:
                        for i, task in enumerate(task_list, 1):
                            print(f"{i}. {format_task_display(task)}")
                        idx = input("Enter task number to delete (or 'q' to stop): ").strip()
                        if idx.lower() == 'q':
                            break
                        try:
                            idx_int = int(idx) - 1
                            if 0 <= idx_int < len(task_list):
                                task_to_remove = task_list.pop(idx_int)
                                TOTAL.remove(task_to_remove)
                                print("Task deleted.")
                                if not task_list:
                                    print("List is empty.")
                                    break
                            else:
                                print("Invalid task number.")
                        except:
                            print("Invalid input.")
                except:
                    print("Invalid input.")
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
                    else:
                        print("Invalid choice.")
                        continue
                    print("Cleared successfully.")
                except:
                    print("Invalid input.")
            elif cmd == "5":
                save_tasks_to_file(user_file, TOTAL)
                print("Tasks saved. Goodbye!")
                quit()
            elif cmd == "6":
                today = datetime.now().date()
                tomorrow = today + timedelta(days=1)
                due_today, due_tomorrow = [], []
                for task in TOTAL:
                    try:
                        _, parts = date_split(task)
                        task_date = datetime.strptime(parts[1], "%Y-%m-%d").date()
                        if task_date == today:
                            due_today.append(task)
                        elif task_date == tomorrow:
                            due_tomorrow.append(task)
                    except:
                        continue
                if due_today or due_tomorrow:
                    print("\n=== PENDING TASKS ===")
                    if due_today:
                        print("Tasks Due Today:")
                        for t in due_today:
                            print(f"- {format_task_display(t)}")
                    if due_tomorrow:
                        print("Tasks Due Tomorrow:")
                        for t in due_tomorrow:
                            print(f"- {format_task_display(t)}")
                else:
                    print("No pending tasks for today or tomorrow.")
            elif cmd == "7":
                print("1. High Priority\n2. Low Priority\n3. All Tasks")
                try:
                    v = int(input("Select task list: "))
                    task_list = {1: HIGH_PRIORITY, 2: LOW_PRIORITY, 3: TOTAL}.get(v)
                    if not task_list:
                        print("Invalid choice.")
                        continue
                    if not task_list:
                        print("No tasks in selected list.")
                        continue
                    for i, task in enumerate(task_list, 1):
                        print(f"{i}. {format_task_display(task)}")
                    idx = int(input("Select task number to mark as done: ")) - 1
                    if 0 <= idx < len(task_list):
                        priority, parts = date_split(task_list[idx])
                        parts[3] = 'done'
                        new_task = f"{priority}: {'|'.join(parts)}"
                        TOTAL[TOTAL.index(task_list[idx])] = new_task
                        if task_list is HIGH_PRIORITY:
                            HIGH_PRIORITY[idx] = new_task
                        elif task_list is LOW_PRIORITY:
                            LOW_PRIORITY[idx] = new_task
                        else:
                            if new_task.startswith("High:"):
                                HIGH_PRIORITY.append(new_task)
                            else:
                                LOW_PRIORITY.append(new_task)
                        print("Status effect added to your task.")
                        # Check if all tasks done
                        if all('done' in t for t in TOTAL):
                            clear_all = input("All tasks are done. Clear all tasks? (y/n): ").strip().lower()
                            if clear_all == 'y':
                                TOTAL.clear()
                                HIGH_PRIORITY.clear()
                                LOW_PRIORITY.clear()
                                print("All tasks cleared.")
                    else:
                        print("Invalid task number.")
                except:
                    print("Invalid input.")
            elif cmd == "8":
                print("1. High Priority\n2. Low Priority\n3. All Tasks")
                try:
                    v = int(input("Select task list: "))
                    task_list = {1: HIGH_PRIORITY, 2: LOW_PRIORITY, 3: TOTAL}.get(v)
                    if not task_list:
                        print("Invalid choice.")
                        continue
                    if not task_list:
                        print("No tasks in selected list.")
                        continue
                    for i, task in enumerate(task_list, 1):
                        print(f"{i}. {format_task_display(task)}")
                    idx = int(input("Select task number to edit: ")) - 1
                    if 0 <= idx < len(task_list):
                        priority, parts = date_split(task_list[idx])
                        new_task_name = input(f"New task name (current: {parts[0]}): ").strip() or parts[0]
                        new_date = input(f"New due date (YYYY-MM-DD) (current: {parts[1]}): ").strip() or parts[1]
                        if not valid_date(new_date):
                            print("Invalid date format. Edit cancelled.")
                            continue
                        new_time = input(f"New due time (HH:MM) (current: {parts[2]}): ").strip() or parts[2]
                        if not valid_time(new_time):
                            print("Invalid time format. Edit cancelled.")
                            continue
                        parts[0], parts[1], parts[2] = new_task_name, new_date, new_time
                        new_task = f"{priority}: {'|'.join(parts)}"
                        TOTAL[TOTAL.index(task_list[idx])] = new_task
                        if task_list is HIGH_PRIORITY:
                            HIGH_PRIORITY[idx] = new_task
                        elif task_list is LOW_PRIORITY:
                            LOW_PRIORITY[idx] = new_task
                        print("Task updated.")
                    else:
                        print("Invalid task number.")
                except:
                    print("Invalid input.")
            else:
                print("Invalid command.")