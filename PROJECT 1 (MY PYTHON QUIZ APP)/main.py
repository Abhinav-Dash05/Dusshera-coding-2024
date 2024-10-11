import random as r

QUESTIONS = [
    'What is the method to convert a string to lowercase? | lower()',
    'How do you access the first element of a list? | list[0]',
    'What is the output of "Hello".upper()? | HELLO',
    'How do you append an item to a list? | list.append(item)',
    'What method would you use to find the length of a string? | len()',
    'How do you create a list in Python? | []',
    'What method is used to remove whitespace from the ends of a string? | strip()',
    'How do you concatenate two strings? | +',
    'What is the output of list(range(5))? | [0, 1, 2, 3, 4]',
    'How do you check if an item exists in a list? | item in list',
    'What method returns a substring from a string? | slice',
    'How do you create a string from a list? | str.join()',
    'What will be the output of "Python"[0:2]? | Py',
    'How do you sort a list in ascending order? | list.sort()',
    'What does the index() method do for a list? | Returns the index of an item',
    'How can you make a string repeat multiple times? | string * n',
    'What is the method to split a string into a list? | split()',
    'How do you remove an item from a list by value? | list.remove(value)',
    'What will be the output of len("Hello World")? | 11',
    'How do you access the last element of a list? | list[-1]',
    'What is the output of "abc".replace("a", "A")? | Abc',
    'How do you find the first occurrence of a substring in a string? | str.find()',
    'How do you create a list with 5 zeros? | [0] * 5',
    'What method would you use to reverse a list? | list.reverse()',
    'How do you check the count of a specific element in a list? | list.count(item)',
    'What is the output of "Hello".find("e")? | 1',
    'How can you combine two lists? | list1 + list2',
    'What is the method to convert a list to a string? | join()',
    'How do you get a substring from a string? | str[start:end]',
    'What will be the output of "123".isdigit()? | True',
    'How do you clear all elements from a list? | list.clear()',
    'What method is used to capitalize the first letter of a string? | capitalize()',
    'How do you create a shallow copy of a list? | list.copy()',
    'What is the output of ["a", "b", "c"] * 2? | ["a", "b", "c", "a", "b", "c"]',
    'How do you extend a list with another list? | list.extend(other_list)',
    'What does the string method count() do? | Returns the count of a substring',
    'How do you create a list of numbers from 0 to 9? | list(range(10))',
    'What is the output of "Hello".startswith("H")? | True',
    'How do you convert a list to a set? | set(list)',
    'What method would you use to find the index of an element? | list.index(item)',
    'What does the method pop() do for a list? | Removes and returns an item at the given index',
    'How do you create a string from a list of characters? | "".join(list)',
    'What is the output of "abc"[1] + "def"[1]? | be',
    'How do you create a list with mixed data types? | [1, "two", 3.0]',
    'What will be the output of list("abc")? | ["a", "b", "c"]',
    'How do you check if a list is empty? | len(list) == 0',
    'What does the method capitalize() do? | Capitalizes the first character of a string',
    'How do you access a slice of a list? | list[start:end]',
    'What is the output of "Hello".title()? | Hello',
    'How do you find all occurrences of a substring in a string? | str.find() in a loop',
    'How do you join a list of strings with a comma? | ",".join(list)',
    'What will be the output of "abc".count("a")? | 1',
    'How do you create a tuple from a list? | tuple(list)',
    'What is the output of "Hello".endswith("o")? | True',
    'How do you insert an item at a specific index in a list? | list.insert(index, item)',
    'What is the method to replace a substring in a string? | str.replace(old, new)'
]

Total = 0
entry_field = input('Do you wanna play my game of a few questions of strings and lists? ').lower()
if entry_field != "yes":
    quit()

for x in range(10):
    random_num = r.randint(0,len(QUESTIONS)-1)
    kunal = random_num-1
    Randque_field = QUESTIONS.pop(kunal)
    v = Randque_field.partition('|')
    print(v[0])
    answer = input('What is the answer? ').strip()

    if answer == v[2].strip():
        print("Correct")
        print('----------------------------------------------')
        Total +=1
        kunal -= 1
    else:
        print(f"Incorrect")
        print(f"The answer is {v[2]}")
        print('----------------------------------------------')
        kunal -= 1
print(f"You scored {Total} out of 10.")
if (Total>=8):
    print("good job")
elif(8>Total>=5):
    print("You can do better")
else:
    print("Go and study.")