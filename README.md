# 🗂️ Secure To-Do List CLI App

A secure, command-line based to-do list manager built with Python. Designed with encryption, user authentication, and priority-based task organization. 

> **Note:** This project is part of my Dusshera Coding 2024 challenge. It will be renamed soon to reflect its final purpose.

## 🔒 Features

- ✅ **Account System** — Create & log in to user accounts securely  
- 🔐 **AES Encryption** — Tasks & usernames are encrypted using `cryptography.fernet`  
- ⏳ **Priority Tasks** — Supports High and Low priority categories  
- 🗓️ **Due Dates & Time** — Add deadlines to every task  
- ✔️ **Mark as Done** — Track completed vs pending tasks  
- 🧼 **Auto-Cleanup Prompt** — Option to clear tasks when all are completed  
- 🧠 **Smart Errors** — Graceful handling of invalid inputs  
- 🔁 **Retry System** — 5 retry attempts for login before lockout  
- 💾 **Persistent Storage** — Tasks are saved to encrypted files per user  

## 🧑‍💻 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Abhinav-Dash05/Dusshera-coding-2024.git
cd Dusshera-coding-2024
```

### 2. Install Dependencies

```bash
pip install cryptography
```

### 3. Run the App

```bash
python todo.py
```

> Replace `todo.py` with your actual filename if different.

## 📁 File Structure

```
app-data/
├── credentials/       # Encrypted usernames and password hashes
├── lists/             # User-specific encrypted task lists
```

## 🚀 Example Use

```plaintext
GOOD MORNING SIR. WHAT WOULD YOU LIKE ME TO DO.
1. Create a new account
2. Login
...
1. Add task
2. Show tasks
3. Delete task
...
7. Quit
```

## 🔐 Security Notes

- Passwords are hashed with SHA-256.  
- Usernames and task data are encrypted using symmetric encryption (Fernet).  
- Files are saved with strict permissions (`chmod 600` for key storage).  

## 🙋‍♂️ About the Author

Made with patience, focus, and a love for Python.

> 🧑‍💻 [Abhinav Dash](https://github.com/Abhinav-Dash05)

## ⭐️ Support

If you find this useful, consider giving it a ⭐ on GitHub!

---

> This project will soon be renamed and polished as a full-fledged productivity tool.
