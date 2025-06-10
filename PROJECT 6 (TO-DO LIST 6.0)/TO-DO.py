import os,time,getpass,re,hashlib,stat,platform,ctypes       # os, time, hashlib, getpass, re modules
from argon2 import PasswordHasher                       # Password Hasher
from argon2.exceptions import VerifyMismatchError       # Module to identify mismatch
from datetime import datetime,timedelta         # datetime and timedelta
from cryptography.fernet import Fernet          # Fernet
ph = PasswordHasher()
curr_dir=os.getcwd()                            # Getting the path of the current directory
app_data_dir=f'{curr_dir}/app-data/to-do'       # Directory for information storage
log_file_path = os.path.join(app_data_dir, 'activity.log')  # Log file path
def log_event(message):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    log_file_exists = os.path.exists(log_file_path)
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            if not log_file_exists or date_str not in open(log_file_path, encoding = 'utf-8').read():
                f.write(f"\nDate-{date_str}\n")
            f.write(f"{time_str}-{message}\n")
    except Exception as e:
        print(f"[Logging Error] {e}")
        log_event(f"[Logging Error] {str(e)}", error = True)
log_event('Program started and all necessary imports checked')
lists_dir=os.path.join(app_data_dir,'lists')    # Lists folder directory
def create_secure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        system = platform.system()
        if system in ['Linux','Darwin']:
            try:
                os.chmod(path, stat.S_IRWXU)
                log_event(f"Secure Folder for {path} created.")
            except Exception as e:
                print(f"Warning: Could not set perissions for {path}:{e}")
                log_event(f"Failure in creating secure path for {path}:{str(e)}")
        elif system == 'Windows':
            try:
                FILE_ATTRIBUTE_HIDDEN = 0x02
                ctypes.windll.kernel32.SetFileAttributesW(str(path), FILE_ATTRIBUTE_HIDDEN)
                log_event(f"Secure Folder for {path} created.")
            except Exception as e:
                print(f"Warning: Could not hide folder {path}: {e}")
                log_event(f"Failure in creating secure path for {path}: {str(e)}")
credentials_dir=os.path.join(app_data_dir,'credentials')        # LOGIN ID FOLDER
create_secure_folder(app_data_dir)
create_secure_folder(lists_dir)
create_secure_folder(credentials_dir)
def protect_folder(folder_path):
    try:
        if os.name == 'nt':
            os.system(f'attrib+h"{folder_path}"')
        else:
            os.chmod(folder_path, 0o700)
        log_event("Folders Protected.")
    except Exception as e:
        print(f"Warning: Could not protect {folder_path}: {e}")
        log_event('[Security Error]: {str(e)}')
protect_folder(app_data_dir)
protect_folder(credentials_dir)
protect_folder(lists_dir)
def load_or_generate_key():                                         # Key Generation for encryption
    key_path=os.path.join(credentials_dir,'key.key')                
    if not os.path.exists(key_path):
        key=Fernet.generate_key()
        with open(key_path,'wb') as f:
            f.write(key)
        os.chmod(key_path,0o600)
        log_event("Key generated.")
    else:
        with open(key_path,'rb') as f:
            key=f.read()
        log_event('Key retrieved.')
    return key
cipher=Fernet(load_or_generate_key())                           # Key
CREDENTIALS={}                                                  # DIctionary with the credentials 
def hash_password(pw):                                          # Password hashing
    return ph.hash(pw)
def verify_password(hashed_pw, plain_pw):
    try:
        return ph.verify(hashed_pw, plain_pw)
    except VerifyMismatchError:
        return False
    except Exception as e:
        print(f"Verification Error: {e}")
        return False
def encrypt_username(username):                                 # Username Encryption
    return hashlib.sha256(username.encode()).hexdigest()
def decrypt_username(enc_username):                             # Username Decryption
    return None
def save_credentials():                                                         # Saving of credetials in credentials folder
    with open(os.path.join(credentials_dir,'credentials.txt'),'w') as f:
        for enc_user,hashed in CREDENTIALS.items():
            f.write(f"{enc_user}:{hashed}\n")
def load_credentials():                                                         # Loading of credentials if they exist in a preexisting folder of previous runs if those exist.
    path=os.path.join(credentials_dir,'credentials.txt')
    if os.path.exists(path):
        with open(path,'r') as f:
            for line in f:
                if ':' in line:
                    enc_user,hashed=line.strip().split(':',1)
                    CREDENTIALS[enc_user]=hashed
def encrypt_data(data):                                                     # Encryption of Data using the cipher created earlier.
    return cipher.encrypt(data.encode())
def decrypt_data(data):                                                     # Decryption of Data using the key saved earlier
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
def sanitize_filename(name):
    return re.sub(r'[^A-Za-z0-9_\-]','_',name)  # Sanitize filename to avoid issues with special characters
def get_user_file(enc_username):
    safe_name = sanitize_filename(enc_username)
    return os.path.join(lists_dir,f"tasks_{safe_name}.txt")
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
def parse_task(task):
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
        priority,parts=parse_task(task)
        task_name,date_,time_,status=parts
        status_emoji='✔' if status=='done' else '⏳'
        return f"{priority} {task_name} (Due {date_} {time_}) Status: {status_emoji}"
    except:
        return task
def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')
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
            log_event('Username duplication prevented.')
            continue
        password=getpass.getpass("Enter your desired password: ")
        if not password:
            print("Password cannot be empty.")
            continue
        CREDENTIALS[enc_user]=hash_password(password)
        save_credentials()
        log_event(f'Account for {username} was created.')
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
            if verify_password(CREDENTIALS[enc_user], password):
                if ph.check_needs_rehash(CREDENTIALS[enc_user]):
                    CREDENTIALS[enc_user] = hash_password(password)
                    save_credentials()
                    log_event(f'User logged in.')
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
            log_event("TOO many login attempts.")
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
                _,parts=parse_task(task)
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
            clear_screen()
            print("\n=== TO-DO LIST ===")
            print("What would you like me to do?")
            print("\n1. Add task")
            print("2. Show tasks")
            print("3. Delete task")
            print("4. Clear task list")
            print("5. Edit task")
            print("6. Pending tasks")
            print("7. Quit")
            print("8. Toggle task status")
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
                    print("A task was added")
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
                        log_event("Tasks displayed")
                except:
                    print("Invalid input.")
                    log_event("Unable to display tasks")
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
                        log_event("A Task was deleted.")
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
                        log_event("HP list was cleared for user")
                    elif clr==2:
                        for t in LOW_PRIORITY:
                            if t in TOTAL:
                                TOTAL.remove(t)
                        LOW_PRIORITY.clear()
                        print("Low priority tasks cleared.")
                        log_event("LP list was cleared for user")
                    elif clr==3:
                        TOTAL.clear()
                        HIGH_PRIORITY.clear()
                        LOW_PRIORITY.clear()
                        print("All tasks cleared.")
                        log_event("All tasks were cleared for user.")
                    else:
                        print("Invalid choice.")
                except:
                    print("Invalid input.")
            elif cmd == "5":
                try:
                    print("1. High Priority\n2. Low Priority\n3. All Tasks")
                    list_choice = int(input("Choose list to edit: "))
                    if list_choice == 1:
                        task_list = HIGH_PRIORITY
                    elif list_choice == 2:
                        task_list = LOW_PRIORITY
                    elif list_choice == 3:
                        task_list = TOTAL
                    else:
                        print("Invalid choice.")
                        continue
                    if not task_list:
                        print("No tasks to edit.")
                        continue
                    for i, task in enumerate(task_list, 1):
                        print(f"{i}. {format_task_display(task)}")
                    idx = int(input("Enter task number to edit: ")) - 1
                    if idx < 0 or idx >= len(task_list):
                        print("Invalid task number.")
                        continue
                    original_task = task_list[idx]
                    priority, parts = parse_task(original_task)
                    task_name, date_, time_, status = parts
                    print("Press enter to keep existing value.")
                    new_name = input(f"Task name [{task_name}]: ").strip() or task_name
                    new_date = input(f"Due date (YYYY-MM-DD) [{date_}]: ").strip() or date_
                    if new_date and not valid_date(new_date):
                        print("Invalid date.")
                        continue
                    new_time = input(f"Due time (HH:MM) [{time_}]: ").strip() or time_
                    if new_time and not valid_time(new_time):
                        print("Invalid time.")
                        continue
                    edited_task = f"{priority}: {new_name}|{new_date}|{new_time}|{status}"
                    # Update all lists
                    task_list[idx] = edited_task
                    total_idx = TOTAL.index(original_task)
                    TOTAL[total_idx] = edited_task
                    if priority == "High":
                        hp_idx = HIGH_PRIORITY.index(original_task)
                        HIGH_PRIORITY[hp_idx] = edited_task
                    elif priority == "Low":
                        lp_idx = LOW_PRIORITY.index(original_task)
                        LOW_PRIORITY[lp_idx] = edited_task
                    print("Task updated.")
                    log_event(f"Edited task: {edited_task}")
                except Exception as e:
                    log_event(f"Exception occurred in edit task: {str(e)}")
                    print("An error occurred while editing the task.")
            elif cmd == "6":
                pending_tasks=[t for t in TOTAL if t.endswith("pending")]
                if not pending_tasks:
                    print("No pending tasks")
                else:
                    for i,t in enumerate(pending_tasks, 1):
                        print(f'{i}. {format_task_display(t)}')
                log_event("Pending tasks enumerated for user.")
            elif cmd=="7":
                save_tasks_to_file(user_file,TOTAL)
                print("Tasks saved. Goodbye!")
                log_event("User logged out and data saved.")
                quit()
            elif cmd=="8":
                print("1. High Priority\n2. Low Priority\n3. All Tasks")
                try:
                    toggle_list_choice=int(input("Choose list: "))
                    if toggle_list_choice==1:
                        task_list=HIGH_PRIORITY
                    elif toggle_list_choice==2:
                        task_list=LOW_PRIORITY
                    elif toggle_list_choice==3:
                        task_list=TOTAL
                    else:
                        print("Invalid choice.")
                        continue
                    if not task_list:
                        print("No tasks in that list.")
                        continue
                    for i,task in enumerate(task_list,1):
                        print(f"{i}. {format_task_display(task)}")
                    idx=int(input("Enter task number to toggle status: "))-1
                    if idx<0 or idx>=len(task_list):
                        print("Invalid task number.")
                        continue
                    priority,parts=parse_task(task_list[idx])
                    task_name,date_,time_,status=parts
                    new_status='done' if status=='pending' else 'pending'
                    new_task_str=f"{priority}: {task_name}|{date_}|{time_}|{new_status}"
                    # Update all lists
                    total_idx=TOTAL.index(task_list[idx])
                    TOTAL[total_idx]=new_task_str
                    if priority=="High":
                        hp_idx=HIGH_PRIORITY.index(task_list[idx])
                        HIGH_PRIORITY[hp_idx]=new_task_str
                    else:
                        lp_idx=LOW_PRIORITY.index(task_list[idx])
                        LOW_PRIORITY[lp_idx]=new_task_str
                    print(f"Task status toggled to '{new_status}'.")
                except Exception as e:
                    print(f"Error toggling task status: {e}")
            else:
                print("Invalid command.")
            clear = input("Press Enter to clear screen.")
            clear_screen()
