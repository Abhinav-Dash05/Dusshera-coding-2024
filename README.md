# 🗂️ Secure To-Do List CLI App

A secure, command-line based to-do list manager built with Python. Designed with encryption, user authentication, and priority-based task organization. 
This app is a great way to manage your tasks while keeping your data safe.

## 📜 Table of Contents

- [Description](#-description)
- [Requirements](#-requirements)
- [Features](#-features)
- [Getting Started](#-getting-started)
  - [Clone the Repository](#1-clone-the-repository)
  - [Install Dependencies](#2-install-dependencies)
  - [Run the App](#3-run-the-app)
- [File Structure](#-file-structure)
- [Example Use](#-example-use)
- [Security Notes](#-security-notes)
- [About the Author](#-about-the-author)
- [Support](#-support)
- [License](#-license)
- [Contributing](#-contributing)


## 📜 Description

This is a simple command-line to-do list application that allows users to create, view, and manage tasks securely. The app uses AES encryption to protect user data and provides a user-friendly interface for managing tasks.
The app is designed to be easy to use, with a focus on security and privacy. It allows users to create accounts, log in, and manage their tasks securely. The app also includes features such as task prioritization, due dates, and the ability to mark tasks as done.
The app is built using Python and the `cryptography` library for encryption. It is designed to be run from the command line, making it easy to use on any platform that supports Python.

## 📦 Requirements

- Python 3.x
- `cryptography` library
- Basic knowledge of command-line interfaces
- Basic knowledge of Python programming
- Basic knowledge of encryption and security concepts
- Basic knowledge of file handling in Python
- Basic knowledge of data structures in Python
- Basic knowledge of object-oriented programming in Python
- Basic knowledge of error handling in Python
- Basic knowledge of user authentication and authorization concepts
- Basic knowledge of hashing algorithms
- Basic knowledge of symmetric encryption algorithms
- Basic knowledge of asymmetric encryption algorithms
- Basic knowledge of public key infrastructure (PKI)
- Basic knowledge of digital signatures
- Basic knowledge of secure coding practices
- Basic knowledge of secure software development techniques

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

## 📜 License

This project is licensed under the Apache License. See the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any changes or improvements.
