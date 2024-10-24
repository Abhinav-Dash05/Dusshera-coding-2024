from datetime import datetime as dt
import hashlib
import time
import os

# Initialize user lists
USERID = []
PASS = []

# Function to generate user-specific file name
def get_user_file(login_userid):
    """Generates a filename based on the hashed username."""
    return f"tasks_{login_userid}.txt"

# Function to load tasks from a specific user file
def load_tasks_from_file(user_file):
    try:
        with open(user_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(fixed_operator)
                    if len(parts) == 3:
                        task, date, time = parts
                        TASK_DETAILS = f"{task}{fixed_operator}{date}{fixed_operator}{time}"
                        TOTAL.append(TASK_DETAILS)
                        HIGH_PRIORITY.append(TASK_DETAILS)
                    else:
                        print(f"Skipping invalid line: {line}")
    except FileNotFoundError:
        print("No saved file found for this user. Starting with an empty list.")

# Function to save tasks to a specific user file
def save_tasks_to_file(user_file):
    """Saves tasks for the specific user."""
    with open(user_file, 'w') as file:
        for item in TOTAL:
            file.write(f"{item}\n")
    print(f"Tasks saved to {user_file}.")

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def wait_and_clear():
    time.sleep(1.5)  # Wait for 1.5 seconds
    input("Press Enter to clear the window and show the menu...")
    clear_terminal()

# Load usernames and passwords from files
def load_credentials():
    try:
        with open('usernames.txt', 'r') as user_file:
            for line in user_file:
                USERID.append(line.strip())
    except FileNotFoundError:
        print("No usernames file found. CREATE ONE NOWWWW!!!!!")

    try:
        with open('passwords.txt', 'r') as pass_file:
            for line in pass_file:
                PASS.append(line.strip())
    except FileNotFoundError:
        print("No passwords file found. CREATE ONE NOWWWW!!!!!")

# Save usernames and passwords to files
def save_credentials():
    with open('usernames.txt', 'w') as user_file:
        for userid in USERID:
            user_file.write(f"{userid}\n")
    with open('passwords.txt', 'w') as pass_file:
        for password in PASS:
            pass_file.write(f"{password}\n")

# Load credentials at the start
load_credentials()
time1 = dt.now()
real_time = time1.strftime("%H:%M:%S")

part_time = real_time.partition(":")
hour = int(part_time[0])

if(12 > hour >= 4):
    greeting = "MORNING"
elif(17 > hour >= 12):
    greeting = "AFTERNOON"
else:
    greeting = "EVENING"

while True:
    print(f"GOOD {greeting} SIR. WHAT WOULD YOU LIKE ME TO DO.")
    print("PRESS 1 TO CREATE A NEW ACCOUNT.")
    print("PRESS 2 TO LOGIN")
    login_prompt = int(input(": "))

    if(login_prompt == 1):
        print("ENTER A YOUR DESIRED USERNAME")
        new_userid = input(": ")
        USERID.append((hashlib.sha256(new_userid.encode())).hexdigest())
        print("ENTER YOUR DESIRED PASSWORD")
        new_pass = input(": ")
        PASS.append((hashlib.sha256(new_pass.encode())).hexdigest())
        print("YOUR USERID AND PASSWORD HAS BEEN SAVED.")
    elif(login_prompt == 2):
        print("ENTER YOUR USERID")
        login_userid = (hashlib.sha256(input(": ").encode())).hexdigest()
        print("ENTER YOUR PASSWORD")
        login_pass = (hashlib.sha256(input(": ").encode())).hexdigest()

        if(login_userid in USERID and login_pass in PASS):
            print("Credentials matched. Logging you in......................")
            wait_and_clear()
            TOTAL = []
            HIGH_PRIORITY = []
            LOW_PRIORITY = []
            fixed_operator = "|"

            user_file = get_user_file(login_userid)  # Generate the unique filename

            print("Do you want to load any previously stored lists")
            print("Press 1 for yes")
            print("Press 2 for no")

            load = int(input())

            if load == 1:
                load_tasks_from_file(user_file)  # Load tasks for this user
            elif load == 2:
                print("OKAY STARTING WITH AN EMPTY LIST")
            print("---------------------------------------------------------------------------------------------")

            while True:
                print("What do you want me to do.")
                print("1. Add a new task (Press 1 and enter)")
                print("2. Display the current tasks (Press 2 and enter)")
                print("3. Kill a task (Press 3 and enter)")
                print("4. Clear To-Do List (Press 4 and enter)")
                print("5. Quit (Press 5 and enter)")
                print("---------------------------------------------------------------------------------------------")
                
                user_input_1 = input().strip()
                
                if user_input_1 == "1":
                    print("Do you want your task to be added as a high priority task or low priority task.")
                    print("Press 1 for high priority")
                    print("Press 2 for low priority")
                    C1 = int(input())
                    
                    TASK = input("Enter task to be added: ")
                    DATE = input("When is the final date of Completion: ")
                    TIME = input("What is the Completion time: ")
                    
                    TASK_DETAILS = f"{TASK}{fixed_operator}{DATE}{fixed_operator}{TIME}"
                    
                    if C1 == 1:
                        HIGH_PRIORITY.append(TASK_DETAILS)
                        TOTAL.append(TASK_DETAILS)
                    elif C1 == 2:
                        LOW_PRIORITY.append(TASK_DETAILS)
                        TOTAL.append(TASK_DETAILS)
                    else:
                        print("Not a valid option.")
                    print("---------------------------------------------------------------------------------------------")
                    
                    wait_and_clear()
                    
                elif user_input_1 == "2":
                    print("DO YOU WANT TO SEE YOUR HIGH PRIORITY LIST OR LOW PRIORITY LIST")
                    print("PRESS 1 for HIGH PRIORITY LIST")
                    print("PRESS 2 for LOW PRIORITY LIST")
                    print("PRESS 3 for all TASKS")
                    C2 = int(input())
                    
                    if C2 == 1:
                        index = 1
                        for task in HIGH_PRIORITY:
                            print(f"{index}: {task}")
                            index += 1
                    elif C2 == 2:
                        index = 1
                        for task in LOW_PRIORITY:
                            print(f"{index}: {task}")
                            index += 1
                    elif C2 == 3:
                        index = 1
                        for task in TOTAL:
                            print(f"{index}: {task}")
                            index += 1
                    else:
                        print("Not a valid Command.")
                    print("---------------------------------------------------------------------------------------------")
                    
                    wait_and_clear()
                    
                elif user_input_1 == "3":
                    print("DO you want to delete task from high priority list or low priority list.")
                    print("PRESS 1 for high priority list")
                    print("PRESS 2 for low priority list")
                    C3 = int(input())
                    
                    if C3 == 1:
                        index = 1
                        for task in HIGH_PRIORITY:
                            print(f"{index}: {task}")
                            index += 1
                        TASK_KILL = int(input("Press which task is to be removed by indicating its number: ")) - 1
                        if TASK_KILL < 0 or TASK_KILL >= len(HIGH_PRIORITY):
                            print("Number beyond range.")
                        else:
                            print("Is the task given below the one to be killed")
                            print(HIGH_PRIORITY[TASK_KILL])
                            print("Press 1 for yes")
                            print("Press 2 for no")
                            confirm_C3 = int(input())
                            if confirm_C3 == 1:
                                TOTAL.remove(HIGH_PRIORITY[TASK_KILL])
                                HIGH_PRIORITY.pop(TASK_KILL)
                                print("Task mentioned terminated.")
                            else:
                                print("Process Terminated")
                    elif C3 == 2:
                        index = 1
                        for task in LOW_PRIORITY:
                            print(f"{index}: {task}")
                            index += 1
                        TASK_KILL = int(input("Press which task is to be removed by indicating its number: ")) - 1
                        if TASK_KILL < 0 or TASK_KILL >= len(LOW_PRIORITY):
                            print("Number beyond range.")
                        else:
                            print("Is the task given below the one to be killed")
                            print(LOW_PRIORITY[TASK_KILL])
                            print("Press 1 for yes")
                            print("Press 2 for no")
                            confirm_C3 = int(input())
                            if confirm_C3 == 1:
                                TOTAL.remove(LOW_PRIORITY[TASK_KILL])
                                LOW_PRIORITY.pop(TASK_KILL)
                                print("Task mentioned terminated.")
                            else:
                                print("Process Terminated")
                    else:
                        print("Not a valid command.")
                    print("---------------------------------------------------------------------------------------------")

                    wait_and_clear()

                elif user_input_1 == "4":
                    print("Which list do you want to clear?")
                    print("Press 1 for HIGH PRIORITY LIST")
                    print("Press 2 for LOW PRIORITY LIST")
                    print("Press 3 to clear all")
                    C4 = int(input())
                    
                    if C4 == 1:
                        HIGH_PRIORITY.clear()
                        TOTAL = [task for task in TOTAL if task not in HIGH_PRIORITY]
                    elif C4 == 2:
                        LOW_PRIORITY.clear()
                        TOTAL = [task for task in TOTAL if task not in LOW_PRIORITY]
                    elif C4 == 3:
                        TOTAL.clear()
                        HIGH_PRIORITY.clear()
                        LOW_PRIORITY.clear()
                    print("---------------------------------------------------------------------------------------------")
                    
                    wait_and_clear()

                elif user_input_1 == "5":
                    print("You sure that you want to exit? Just making sure of no possible accidents.")
                    print("Press 1 for yes.")
                    print("Press 2 for no.")
                    
                    try:
                        acc_quit = int(input())
                        if acc_quit == 1:
                            print("Do you want to save your List?")
                            print("Press 1 for Yes.")
                            print("Press 2 for No.")
                            
                            quit_save = int(input())
                            if quit_save == 1:
                                save_tasks_to_file(user_file)  # Save tasks for this user
                            print("Thanks for using. :)")
                            save_credentials()
                            print("---------------------------------------------------------------------------------------------")
                            if(hour >= 17):
                                print("GOOD NIGHT SIR. SLEEP WELL!!!!")
                            time.sleep(3.5)
                            quit()
                        elif acc_quit == 2:
                            print("Accidental Quitting prevented :)")
                            print("---------------------------------------------------------------------------------------------")
                        else:
                            print("Invalid Command")
                    except ValueError:
                        print('Insert recommended options.')
                        print("---------------------------------------------------------------------------------------------")
                
                wait_and_clear()

        else:
            print("SORRY! Credentials didn't match. Try to remember it again.")
            wait_and_clear()
