import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class ReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cogni Remind")

        self.reminders = []

        self.reminder_text = tk.StringVar()
        self.reminder_time = tk.StringVar()

        # Configure colors
        bg_color = "#f0f0f0"  # Light gray
        button_color = "#4CAF50"  # Green
        text_color = "#333333"  # Dark gray

        self.root.configure(bg=bg_color)

        tk.Label(root, text="Reminder Text:", bg=bg_color, fg=text_color).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(root, textvariable=self.reminder_text, bg=bg_color, fg=text_color).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Reminder Time (YYYY-MM-DD HH:MM):", bg=bg_color, fg=text_color).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(root, textvariable=self.reminder_time, bg=bg_color, fg=text_color).grid(row=1, column=1, padx=5, pady=5)

        tk.Button(root, text="Add Reminder", command=self.add_reminder, bg=button_color, fg="white").grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.reminder_listbox = tk.Listbox(root, bg=bg_color, fg=text_color)
        self.reminder_listbox.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        tk.Button(root, text="Remove Reminder", command=self.remove_reminder, bg=button_color, fg="white").grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Load reminders from file on startup
        self.load_reminders()

        # Start checking reminders
        self.check_reminders()

    def add_reminder(self):
        try:
            reminder_time = datetime.strptime(self.reminder_time.get(), "%Y-%m-%d %H:%M")
            self.reminders.append((self.reminder_text.get(), reminder_time))
            self.reminder_listbox.insert(tk.END, f"{self.reminder_text.get()} - {reminder_time}")
            self.reminder_text.set("")
            self.reminder_time.set("")
            self.update_file()
        except ValueError:
            messagebox.showerror("Error", "Invalid datetime format. Please use YYYY-MM-DD HH:MM.")

    def remove_reminder(self):
        selected_index = self.reminder_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            del self.reminders[index]
            self.reminder_listbox.delete(index)
            self.update_file()

    def update_file(self):
        with open("reminders.txt", "w") as file:
            for reminder_text, reminder_time in self.reminders:
                file.write(f"{reminder_text},{reminder_time.strftime('%Y-%m-%d %H:%M')}\n")

    def load_reminders(self):
        try:
            with open("reminders.txt", "r") as file:
                for line in file:
                    reminder_text, reminder_time_str = line.strip().split(',')
                    reminder_time = datetime.strptime(reminder_time_str, "%Y-%m-%d %H:%M")
                    self.reminders.append((reminder_text, reminder_time))
                    self.reminder_listbox.insert(tk.END, f"{reminder_text} - {reminder_time}")
        except FileNotFoundError:
            pass

    def check_reminders(self):
        current_time = datetime.now()
        for i, (reminder_text, reminder_time) in enumerate(self.reminders):
            if current_time >= reminder_time:
                messagebox.showinfo("Reminder", reminder_text)
                del self.reminders[i]
                self.reminder_listbox.delete(i)
                self.update_file()

                # Since a reminder has been shown, we break out of the loop to handle only one reminder per check cycle
                break

        self.root.after(1000, self.check_reminders)

def main():
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
