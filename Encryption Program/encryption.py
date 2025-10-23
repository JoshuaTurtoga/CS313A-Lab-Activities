import tkinter as tk
from tkinter import messagebox
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

class EncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Encryption Program")
        self.root.geometry("400x250")
        self.root.configure(bg='lightgray')
        self.root.resizable(False, False)
        
        # Generate a key for encryption (in a real app, you'd want to store this securely)
        self.key = get_random_bytes(16)
        
        # Create a frame for the content
        self.frame = tk.Frame(root, bg='lightgray', padx=20, pady=20)
        self.frame.pack(expand=True, fill='both')
        
        # Username field
        self.username_label = tk.Label(self.frame, text="USERNAME", bg='lightgray', font=('Arial', 12, 'bold'))
        self.username_label.grid(row=0, column=0, sticky='e', padx=10, pady=10)
        
        self.username_entry = tk.Entry(self.frame, width=25, font=('Arial', 10), bd=2, relief=tk.SOLID)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Password field
        self.password_label = tk.Label(self.frame, text="PASSWORD", bg='lightgray', font=('Arial', 12, 'bold'))
        self.password_label.grid(row=1, column=0, sticky='e', padx=10, pady=10)
        
        self.password_entry = tk.Entry(self.frame, width=25, font=('Arial', 10), bd=2, relief=tk.SOLID, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Buttons frame
        self.button_frame = tk.Frame(self.frame, bg='lightgray')
        self.button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Encrypt button
        self.encrypt_button = tk.Button(self.button_frame, text="Encrypt", width=15, 
                                        command=self.encrypt_data, font=('Arial', 10), bd=2, relief=tk.SOLID)
        self.encrypt_button.grid(row=0, column=0, padx=10)
        
        # Decrypt button
        self.decrypt_button = tk.Button(self.button_frame, text="Decrypt", width=15, 
                                        command=self.decrypt_data, font=('Arial', 10), bd=2, relief=tk.SOLID)
        self.decrypt_button.grid(row=0, column=1, padx=10)
        
        # Store encrypted data
        self.encrypted_username = None
        self.encrypted_password = None

    def encrypt_data(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        try:
            # Create a new cipher for each encryption
            cipher = AES.new(self.key, AES.MODE_CBC)
            
            # Encrypt username
            username_bytes = username.encode('utf-8')
            encrypted_username = cipher.encrypt(pad(username_bytes, AES.block_size))
            
            # Store the IV with the encrypted data
            self.encrypted_username = base64.b64encode(cipher.iv + encrypted_username).decode('utf-8')
            
            # Create a new cipher for password (each encryption needs a new cipher with a new IV)
            cipher = AES.new(self.key, AES.MODE_CBC)
            
            # Encrypt password
            password_bytes = password.encode('utf-8')
            encrypted_password = cipher.encrypt(pad(password_bytes, AES.block_size))
            
            # Store the IV with the encrypted data
            self.encrypted_password = base64.b64encode(cipher.iv + encrypted_password).decode('utf-8')
            
            # Clear the entries and show success message
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Data encrypted successfully!")
            
            # Display the encrypted data
            self.username_entry.insert(0, self.encrypted_username[:20] + "...")
            self.password_entry.insert(0, self.encrypted_password[:20] + "...")
            
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")

    def decrypt_data(self):
        if not self.encrypted_username or not self.encrypted_password:
            messagebox.showerror("Error", "No encrypted data to decrypt")
            return
        
        try:
            # Decrypt username
            encrypted_data = base64.b64decode(self.encrypted_username)
            iv = encrypted_data[:16]  # Extract the IV (first 16 bytes)
            encrypted_username = encrypted_data[16:]  # Extract the actual encrypted data
            
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted_username = unpad(cipher.decrypt(encrypted_username), AES.block_size).decode('utf-8')
            
            # Decrypt password
            encrypted_data = base64.b64decode(self.encrypted_password)
            iv = encrypted_data[:16]  # Extract the IV
            encrypted_password = encrypted_data[16:]  # Extract the actual encrypted data
            
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted_password = unpad(cipher.decrypt(encrypted_password), AES.block_size).decode('utf-8')
            
            # Display the decrypted data
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.username_entry.insert(0, decrypted_username)
            self.password_entry.insert(0, decrypted_password)
            
            messagebox.showinfo("Success", "Data decrypted successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()