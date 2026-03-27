import tkinter as tk
from tkinter import messagebox
import sqlite3
import secrets
import string
from cryptography.fernet import Fernet


def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("secret.key", "rb").read()

try:
    key = load_key()
except FileNotFoundError:
    generate_key()
    key = load_key()

cipher = Fernet(key)

conn = sqlite3.connect('password_manager.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service TEXT NOT NULL,
    email TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)''')
conn.commit()
conn.close()

def encrypt_password(password):
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()

def store_password():
    service = service_entry.get()
    email = email_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if not service or not email or not username or not password:
        messagebox.showwarning("Error", "All fields are required!")
        return

    encrypted_pw = encrypt_password(password)
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (service, email, username, password) VALUES (?, ?, ?, ?)",
                   (service, email, username, encrypted_pw))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Password stored securely!")

def get_password():
    email = email_entry.get()
    if not email:
        messagebox.showwarning("Error", "Email field is required!")
        return

    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()
    cursor.execute("SELECT service, username, password FROM passwords WHERE email=?", (email,))
    result = cursor.fetchone()
    conn.close()

    if result:
        service, username, encrypted_pw = result
        decrypted_pw = decrypt_password(encrypted_pw)
        messagebox.showinfo("Retrieved", f"Service: {service}\nUsername: {username}\nPassword: {decrypted_pw}")
    else:
        messagebox.showwarning("Not Found", "No password found for this email.")

def generate_password():
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(chars) for _ in range(16))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

# GUI
root = tk.Tk()
root.title("🔐 Password Manager")
root.geometry("700x600")

tk.Label(root, text="Service:").grid(row=0, column=0, padx=10, pady=5)
tk.Label(root, text="Email:").grid(row=1, column=0, padx=10, pady=5)
tk.Label(root, text="Username:").grid(row=2, column=0, padx=10, pady=5)
tk.Label(root, text="Password:").grid(row=3, column=0, padx=10, pady=5)

service_entry = tk.Entry(root, width=30)
service_entry.grid(row=0, column=1, padx=10, pady=5)
email_entry = tk.Entry(root, width=30)
email_entry.grid(row=1, column=1, padx=10, pady=5)
username_entry = tk.Entry(root, width=30)
username_entry.grid(row=2, column=1, padx=10, pady=5)
password_entry = tk.Entry(root, width=30)
password_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Button(root, text="Store Password", command=store_password).grid(row=4, column=0, columnspan=2, pady=10)
tk.Button(root, text="Retrieve Password", command=get_password).grid(row=5, column=0, columnspan=2, pady=5)
tk.Button(root, text="Generate Password", command=generate_password).grid(row=6, column=0, columnspan=2, pady=5)

root.mainloop()
