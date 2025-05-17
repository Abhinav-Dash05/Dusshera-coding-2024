import os,time,hashlib,getpass,re
from datetime import datetime,timedelta
from cryptography.fernet import Fernet
curr_dir=os.getcwd()
app_data_dir=f'{curr_dir}/app-data/to-do'
lists_dir=os.path.join(app_data_dir,'lists')
credentials_dir=os.path.join(app_data_dir,'credentials')
os.makedirs(lists_dir,exist_ok=True)
os.makedirs(credentials_dir,exist_ok=True)
def load_or_generate_key():
    key_path=os.path.join(credentials_dir,'key.key')
    if not os.path.exists(key_path):
        key=Fernet.generate_key()
        with open(key_path,'wb') as f:
            f.write(key)
        os.chmod(key_path,0o600)
    else:
        with open(key_path,'rb') as f:
            key=f.read()
    return key
cipher=Fernet(load_or_generate_key())
CREDENTIALS={}
def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()
def encrypt_username(username):
    return cipher.encrypt(username.encode()).decode()
def decrypt_username(enc_username):
    try:
        return cipher.decrypt(enc_username.encode()).decode()
    except:
        return None
def save_credentials():
    with open(os.path.join(credentials_dir,'credentials.txt'),'w') as f:
        for enc_user,hashed in CREDENTIALS.items():
            f.write(f"{enc_user}:{hashed}\n")
def load_credentials():
    path=os.path.join(credentials_dir,'credentials.txt')
    if os.path.exists(path):
        with open(path,'r') as f:
            for line in f:
                if ':' in line:
                    enc_user,hashed=line.strip().split(':',1)
                    CREDENTIALS[enc_user]=hashed
def encrypt_data(data):
    return cipher.encrypt(data.encode())
def decrypt_data(data):
    return cipher.decrypt(data).decode()
def save_tasks_to_file(user_file,tasks):
    try:
        with open(user_file,'wb') as f:
            f.write(encrypt_data("\n".join(tasks)))
    except Exception as e:
        print(f"Error saving tasks: {e}")
def load_tasks_from_file(user_file):
    try:
        with open(user_file,'rb') as f:
            return decrypt_data(f.read()).splitlines()
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error loading tasks: {e}")
        return []
def get_user_file(enc_username):
    return os.path.join(lists_dir,f"tasks_{enc_username}.txt")
def valid_date(date_str):
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',date_str):
        return False
    try:
        datetime.strptime(date_str,'%Y-%m-%d')
        return True
    except:
        return False
def valid_time(time_str):
    if not re.fullmatch(r'\d{2}:\d{2}',time_str):
        return False
    try:
        datetime.strptime(time_str,'%H:%M')
        return True
    except:
        return False
def date_split(task):
    try:
        priority,rest=task.split(': ',1)
        parts=rest.split('|')
        if len(parts)==3:
            parts.append('pending')
        return priority,parts
    except:
        return None,[]
def format_task_display(task):
    try:
        priority,text=date_split(task)
        task_name,date_,time_,status=text
        status_emoji='✔' if status=='done' else '⏳'
        return f"{priority} {task_name} (Due {date_} {time_}) Status: {status_emoji}"
    except:
        return task
hour=datetime.now().hour
greeting="MORNING" if 4<=hour<12 else "AFTERNOON" if 12<=hour<17 else "EVENING"
load_credentials()
while True:
    print(f"\nGOOD {greeting} SIR. Let's log you back in.")
    print("1. Create a new account")
    print("2. Login")
    try:
        choice=int(input(": "))
    except:
        print("Please enter a valid number.")
        continue
    if choice==1:
        username=input("Enter your desired username: ").strip()
        if not username or ':' in username:
            print("Invalid username.")
            continue
        enc_user=encrypt_username(username)
        if enc_user in CREDENTIALS:
            print("Username already exists.")
            continue
        password=getpass.getpass("Enter your desired password: ")
        if not password:
            print("Password cannot be empty.")
            continue
        CREDENTIALS[enc_user]=hash_password(password)
        save_credentials()
        print("Account created successfully.")
    elif choice==2:
        username=input("Enter your username: ").strip()
        enc_user=encrypt_username(username)
        if enc_user not in CREDENTIALS:
            print("Username not found.")
            continue
        attempts=0
        while attempts<5:
            password=getpass.getpass("Enter your password: ")
            if CREDENTIALS[enc_user]==hash_password(password):
                break
            attempts+=1
            print(f"Incorrect password. Attempts left: {5-attempts}")
            time.sleep(1)
            if attempts<5:
                print("1. Retry password\n2. Back to Main Menu\n3. Quit")
                try:
                    retry_choice=int(input(": "))
                    if retry_choice==2:
                        break
                    elif retry_choice==3:
                        print("Goodbye!")
                        quit()
                    elif retry_choice!=1:
                        print("Invalid input. Returning to main menu.")
                        break
                except:
                    print("Invalid input. Returning to main menu.")
                    break
        else:
            print("Too many failed attempts. Returning to main menu.")
            continue
        if attempts==5:
            continue
        user_file=get_user_file(enc_user)
        TOTAL,HIGH_PRIORITY,LOW_PRIORITY=[],[],[]
        try:
            load_choice=int(input("Load previously saved list? (1=Yes,2=No): "))
            if load_choice==1:
                TOTAL=load_tasks_from_file(user_file)
                HIGH_PRIORITY=[t for t in TOTAL if t.startswith("High:")]
                LOW_PRIORITY=[t for t in TOTAL if t.startswith("Low:")]
        except:
            print("Invalid input. Starting empty.")
        today=datetime.now().date()
        tomorrow=today+timedelta(days=1)
        due_today,due_tomorrow=[],[]
        for task in TOTAL:
            try:
                _,parts=date_split(task)
                task_date=datetime.strptime(parts[1],"%Y-%m-%d").date()
                if task_date==today:
                    due_today.append(task)
                elif task_date==tomorrow:
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
            print("What would you like me to do?")
            print("\n1. Add task")
            print("2. Show tasks")
            print("3. Delete task")
            print("4. Clear task list")
            print("5. Edit task")
            print("6. Pending tasks")
            print("7. Quit")
            cmd=input(": ").strip()
            if cmd=="1":
                try:
                    priority=int(input("1. High priority\n2. Low priority\nChoose: "))
                    if priority not in [1,2]:
                        print("Invalid priority choice.")
                        continue
                    task=input("Task: ").strip()
                    date_=input("Due Date (YYYY-MM-DD): ").strip()
                    if not valid_date(date_):
                        print("Invalid date format.")
                        continue
                    time_=input("Due Time (HH:MM): ").strip()
                    if not valid_time(time_):
                        print("Invalid time format.")
                        continue
                    entry=f"{task}|{date_}|{time_}|pending"
                    full_entry=f"{'High' if priority==1 else 'Low'}: {entry}"
                    TOTAL.append(full_entry)
                    if priority==1:
                        HIGH_PRIORITY.append(full_entry)
                    else:
                        LOW_PRIORITY.append(full_entry)
                    print("Task added.")
                except:
                    print("Invalid input.")
            elif cmd=="2":
                print("1. High Priority\n2. Low Priority\n3. All Tasks")
                try:
                    v=int(input(": "))
                    task_list={1:HIGH_PRIORITY,2:LOW_PRIORITY,3:TOTAL}.get(v,[])
                    if not task_list:
                        print("No tasks.")
                        continue
                    for i,t in enumerate(task_list,1):
                        print(f"{i}. {format_task_display(t)}")
                except:
                    print("Invalid input.")
            elif cmd=="3":
                print("1. High Priority\n2. Low Priority")
                try:
                    d=int(input("Choose list to delete from: "))
                    task_list=HIGH_PRIORITY if d==1 else LOW_PRIORITY
                    if not task_list:
                        print("List is empty.")
                        continue
                    while True:
                        for i,t in enumerate(task_list,1):
                            print(f"{i}. {format_task_display(t)}")
                        idx=int(input("Enter task number to delete: "))-1
                        if idx<0 or idx>=len(task_list):
                            print("Invalid task number.")
                            continue
                        to_delete=task_list.pop(idx)
                        TOTAL.remove(to_delete)
                        if to_delete.startswith("High:") and to_delete in HIGH_PRIORITY:
                            HIGH_PRIORITY.remove(to_delete)
                        elif to_delete.startswith("Low:") and to_delete in LOW_PRIORITY:
                            LOW_PRIORITY.remove(to_delete)
                        print("Task deleted.")
                        if not task_list:
                            print("List is empty now.")
                            break
                        cont=input("Delete another task from this list? (y/n): ").strip().lower()
                        if cont!="y":
                            break
                except:
                    print("Invalid input.")
            elif cmd=="4":
                print("1. Clear High Priority\n2. Clear Low Priority\n3. Clear All")
                try:
                    clr=int(input(": "))
                    if clr==1:
                        for t in HIGH_PRIORITY:
                            if t in TOTAL:
                                TOTAL.remove(t)
                        HIGH_PRIORITY.clear()
                        print("High priority tasks cleared.")
                    elif clr==2:
                        for t in LOW_PRIORITY:
                            if t in TOTAL:
                                TOTAL.remove(t)
                        LOW_PRIORITY.clear()
                        print("Low priority tasks cleared.")
                    elif clr==3:
                        TOTAL.clear()
                        HIGH_PRIORITY.clear()
                        LOW_PRIORITY.clear()
                        print("All tasks cleared.")
                    else:
                        print("Invalid choice.")
                except:
                    print("Invalid input.")
            elif cmd=="5":
                print("Edit feature not implemented yet.")
            elif cmd=="6":
                pending_tasks=[t for t in TOTAL if t.endswith("pending")]
                if not pending_tasks:
                    print("No pending tasks.")
                else:
                    for i,t in enumerate(pending_tasks,1):
                        print(f"{i}. {format_task_display(t)}")
            elif cmd=="7":
                save_tasks_to_file(user_file,TOTAL)
                print("Tasks saved. Goodbye!")
                quit()
            else:
                print("Invalid command.")
    else:
        print("Invalid choice. Please try again.")
        continue