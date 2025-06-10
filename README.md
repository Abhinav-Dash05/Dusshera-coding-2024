# 📂 Secure To-Do List CLI App

A secure, command-line based to-do list manager built with Python. Designed with encryption, user authentication, and priority-based task organization. This app is a great way to manage your tasks while keeping your data safe.

## 📜 Table of Contents
- Description
- Requirements
- Features
- Getting Started
- File Structure
- Example Use
- Security Notes
- About the Author
- Support
- License
- Contributing

## 📜 Description
This is a simple command-line to-do list application that allows users to create, view, and manage tasks securely. The app uses AES encryption to protect user data and provides a user-friendly interface for managing tasks. It also supports encrypted logging and password hashing for maximum security. It allows users to create accounts, log in, and manage their tasks securely. Features include task prioritization, due dates, account system, encryption, and logging. Built with Python and the `cryptography` and `argon2-cffi` libraries.

## 📦 Requirements
- Python 3.x  
- `cryptography` library  
- `argon2-cffi` library  
- Basic knowledge of:
  - Python programming
  - Command-line usage
  - Encryption and hashing
  - File handling
  - Secure coding practices

## 🔒 Features
✅ Account System — Create & log in securely  
🔐 AES Encryption — Encrypts tasks, usernames with `Fernet`  
🗝️ Per-User AES Keys — Unique key per account  
🔒 Argon2 Password Hashing — High-security password hashing  
🗓️ Due Dates — Add deadlines  
⏳ Priority Sorting — High/Low task categorization  
✔️ Task Status — Mark as done or pending  
🧼 Auto-Cleanup Prompt — Clear list when all tasks complete  
📃 Encrypted Logging — Logs actions in encrypted format  
🔁 Retry Lock — 5 wrong login attempts = lockout  
💾 Persistent Storage — Encrypted local file storage  

## 🧑‍💻 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Abhinav-Dash05/Todo-List.git
cd Todo-List
```

### 2. Install Dependencies
```bash
pip install cryptography argon2-cffi
```

### 3. Run the App
```bash
python todo.py
```

> Replace `todo.py` with your filename if changed.

## 📁 File Structure
```
Todo-List/
├── app-data/
│   ├── credentials/       # Encrypted usernames & Argon2-hashed passwords
│   ├── lists/             # Encrypted task files per user
│   ├── keys/              # Per-user Fernet keys
│   └── logs/              # Encrypted action and error logs per user
├── todo.py                # Main app script
├── README.md              # Project documentation
```

## 🚀 Example Use
```
GOOD MORNING SIR. WHAT WOULD YOU LIKE ME TO DO?
1. Create a new account
2. Login
...
1. Add task
2. Show tasks
3. Delete task
4. Show done
5. Edit task
6. Show pending tasks
7. Mark task done
8. Quit
```

## 🔐 Security Notes
- **Passwords** are hashed using **Argon2**, a memory-hard password hashing algorithm
- **Tasks and usernames** are encrypted using **AES (Fernet)**
- **Per-user encryption keys** are securely generated and stored
- **Log files** are encrypted and include timestamped actions such as login attempts, task additions, deletions, and errors
  ```
  [2025-06-10 10:25] - Task "Buy milk" added.
  [2025-06-10 10:31] - Login failed for user 'alice'.
  ```
- All files stored locally with tight permission control (`chmod 600` style if applicable)

## 👨‍💻 About the Author
Made with patience, focus, and a love for Python by  
**[Abhinav Dash](https://github.com/Abhinav-Dash05)**  
🔗 GitHub Repo: [https://github.com/Abhinav-Dash05/Todo-List](https://github.com/Abhinav-Dash05/Todo-List)

## ⭐️ Support
If you find this helpful, give it a ⭐ on GitHub!

## 📜 License
This project is licensed under the Apache License 2.0.  
See the LICENSE file for more details.

## 🤝 Contributing
Feel free to fork, improve, and submit pull requests.