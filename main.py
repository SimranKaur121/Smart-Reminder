import json
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from notification import notify, check_reminders_thread

class ReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Reminder App")
        self.root.geometry("400x300")  # Set window size
        self.root.configure(bg="#e0f7fa")  # Light blue background

        self.data = self.load_data()

        self.message_var = tk.StringVar()
        self.time_var = tk.StringVar()

        # Frame for the input fields
        frame = ttk.Frame(root, padding="10", relief="raised", borderwidth=2)
        frame.pack(fill=tk.BOTH, expand=True)

        # Title Label
        title_label = ttk.Label(frame, text="Smart Reminder App", font=("Arial", 16), background="#e0f7fa")
        title_label.pack(pady=10)

        # Reminder Message Input
        ttk.Label(frame, text="Reminder Message:", background="#e0f7fa").pack(anchor=tk.W)
        self.message_entry = ttk.Entry(frame, textvariable=self.message_var, width=40)
        self.message_entry.pack(pady=5)

        # Reminder Time Input
        ttk.Label(frame, text="Reminder Time (HH:MM):", background="#e0f7fa").pack(anchor=tk.W)
        self.time_entry = ttk.Entry(frame, textvariable=self.time_var, width=40)
        self.time_entry.pack(pady=5)

        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)

        add_button = ttk.Button(button_frame, text="Add Reminder", command=self.add_reminder)
        add_button.grid(row=0, column=0, padx=5)
        add_button.configure(style="AddButton.TButton")

        show_button = ttk.Button(button_frame, text="Show Reminders", command=self.show_reminders)
        show_button.grid(row=0, column=1, padx=5)
        show_button.configure(style="ShowButton.TButton")

        clear_button = ttk.Button(button_frame, text="Clear Reminders", command=self.clear_reminders)
        clear_button.grid(row=0, column=2, padx=5)
        clear_button.configure(style="ClearButton.TButton")

        # Style configuration for buttons
        style = ttk.Style()
        style.configure("AddButton.TButton", background="#b0bec5", foreground="black", padding=10, font=("Arial", 10))
        style.map("AddButton.TButton", background=[("active", "#90a4ae")])  # Hover color

        style.configure("ShowButton.TButton", background="#b0bec5", foreground="black", padding=10, font=("Arial", 10))
        style.map("ShowButton.TButton", background=[("active", "#90a4ae")])  # Hover color

        style.configure("ClearButton.TButton", background="#b0bec5", foreground="black", padding=10, font=("Arial", 10))
        style.map("ClearButton.TButton", background=[("active", "#90a4ae")])  # Hover color

        check_reminders_thread(self.data)

    def load_data(self):
        try:
            with open('data.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {'reminders': []}

    def save_data(self):
        with open('data.json', 'w') as f:
            json.dump(self.data, f)

    def add_reminder(self):
        try:
            message = self.message_var.get()
            reminder_time = datetime.strptime(self.time_var.get(), "%H:%M").time()
            self.data['reminders'].append({'message': message, 'time': reminder_time.strftime("%H:%M")})
            self.save_data()
            messagebox.showinfo("Success", "Reminder added successfully!")
            self.message_var.set("")  # Clear input field
            self.time_var.set("")  # Clear input field
        except ValueError:
            messagebox.showerror("Error", "Invalid time format. Use HH:MM.")

    def show_reminders(self):
        reminders_str = "\n".join(f"{rem['message']} at {rem['time']}" for rem in self.data['reminders'])
        messagebox.showinfo("Reminders", reminders_str if reminders_str else "No reminders set.")

    def clear_reminders(self):
        self.data = {'reminders': []}
        self.save_data()
        messagebox.showinfo("Success", "All reminders have been cleared.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()
