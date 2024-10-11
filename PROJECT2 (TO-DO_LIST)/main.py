#Making of a cool To-Do list :)

LIST = []

print("Welcome to my free to do list. I apologize if our services aren't upto your expectations. But we will definitely try not to betray your trust. Enjoy!!!")

print("Do you want to import any pre-existing list(Format recommended (.txt))")
print("Press 1 for Yes")
print("Press 2 for No")
Command_1 = int(input())
if (Command_1 == 1):
    try:
        with open('list.txt', 'r') as file:
            print("loading file list.txt")
            print("---------------------------------------------------------------------------------------------")
            for line in file:
                item = line.strip().split('. ', 1)[1]
                LIST.append(item)
    except FileNotFoundError:
        print("File not found. Starting with an empty list.")
        print("---------------------------------------------------------------------------------------------")
else:
    pass

while True:
    print("What do you want me to do.")
    print("1. Add a new tasks(Press 1 and enter)")
    print("2. Display the current tasks(Press 2 and enter)")
    print("3. Kill a task(Press 3 and enter)")
    print("4. Clear To-Do List(Press 4 and enter)")
    print("5. Quit(Press 5 and enter)")
    print("---------------------------------------------------------------------------------------------")
    user_input_1 = input().strip()
    if user_input_1 == "1":
        print("Type the task you want to be entered(One at a time).")
        task_input = input()
        LIST.append(task_input)
        print("The task you have mentioned has been entered to your list.")
        print("---------------------------------------------------------------------------------------------")
    elif user_input_1 == "2":
        if (len(LIST)==0):
            print("Your List is empty.")
            print("---------------------------------------------------------------------------------------------")
        else:
            print("Here is your todo list.")
            y = 1
            for x in LIST:
                print(y, x)
                y += 1
            print("---------------------------------------------------------------------------------------------")
    elif user_input_1 == "3":
        if (len(LIST)==0):
            print("Your list is empty. Can't delete anything.")
            print("---------------------------------------------------------------------------------------------")
        else:
            try:
                print("Which task do you wanna kill(Mention by number).")
                task_kill = int(input())
                if (task_kill > len(LIST)):
                    print("Can't delete. The number is beyond list margins.")
                    print("---------------------------------------------------------------------------------------------") 
                else:
                    Task_to_be_removed = LIST[task_kill-1]
                    print("Is the task below the required task to be killed.")
                    print(Task_to_be_removed)
                    print("Press 1 for yes.")
                    print("Press 2 for no.")
                    check = input()
                    if check == "1":
                        LIST.remove(Task_to_be_removed)
                        print("Your Mentioned Task has been killed.")
                        print("---------------------------------------------------------------------------------------------")
                    else:
                        print("TaskKill process termininated.")
                        print("---------------------------------------------------------------------------------------------")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                print("---------------------------------------------------------------------------------------------")
    elif user_input_1 == "4":
        LIST.clear()
        print("Your list has been cleared.")
        print("---------------------------------------------------------------------------------------------")
    elif user_input_1 == "5":
        print("You sure that you want to exit. Just making sure of no possible accidents to happen.")
        print("Press 1 for yes.")
        print("Press 2 for no.")
        try:
            acc_quit = int(input())
        
            if(acc_quit == 1):
                print("Do you want save your List.")
                print("Press 1 for Yes.")
                print("Press 2 for No")
                quit_save = input().strip()
                if quit_save == "1":
                    n = 1
                    with open('list.txt', 'w') as file:
                        for items in LIST:
                            file.write(f"{n}. {items}\n")
                            n+=1
                        print("The list has been saved in a file named list.txt.")
                        print("Thanks for using. :)")
                        print("---------------------------------------------------------------------------------------------")
                        quit()
                elif quit_save == "2":
                    print("Thanks for using. :)")
                    print("---------------------------------------------------------------------------------------------")
                    quit()
                else:
                    print("Invalid Command")
            elif(acc_quit == 2):
                print("Accidental Quitting prevented :)")
                print("---------------------------------------------------------------------------------------------")
            else:
                print("Invalid Command")
        except ValueError:
            print('insert recommended options.')
            print("---------------------------------------------------------------------------------------------")
    else:
        print("Error: Command not found.")