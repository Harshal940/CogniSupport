import time
import threading
import tkinter as tk
from tkinter import font as tkfont, messagebox, PhotoImage
from subprocess import Popen

from Detector import main_app
from create_classifier import train_classifer
from create_dataset import start_capture
from gender_prediction import emotion, ageAndgender

names = set()


class ReminderPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Set Reminder", font='Helvetica 16 bold').grid(row=0, column=0, sticky="ew", pady=10)
        tk.Label(self, text="Reminder Text:", font='Helvetica 12').grid(row=1, column=0, sticky="w", padx=10)
        self.reminder_text = tk.Entry(self, font='Helvetica 12')
        self.reminder_text.grid(row=1, column=1, sticky="w", padx=10)
        tk.Label(self, text="Minutes:", font='Helvetica 12').grid(row=2, column=0, sticky="w", padx=10)
        self.reminder_minutes = tk.Entry(self, font='Helvetica 12')
        self.reminder_minutes.grid(row=2, column=1, sticky="w", padx=10)
        tk.Button(self, text="Set Reminder", command=self.set_reminder).grid(row=3, column=0, columnspan=2, pady=10)

    def set_reminder(self):
        text = self.reminder_text.get()
        minutes = float(self.reminder_minutes.get())
        threading.Thread(target=self.remind, args=(text, minutes)).start()

    def remind(self, text, minutes):
        time.sleep(minutes * 60)
        messagebox.showinfo("Reminder", text)


class MainUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        with open("nameslist.txt", "r") as f:
            x = f.read()
            z = x.rstrip().split(" ")
            for i in z:
                names.add(i)
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("CogniSupport")
        self.resizable(False, False)
        self.geometry("500x250")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, ReminderPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            with open("nameslist.txt", "w") as f:
                for i in names:
                    f.write(i + " ")
            self.destroy()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Load the image for the background
        render = PhotoImage(file='homepagepic.png')
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=0, column=1, rowspan=6, sticky="nsew")

        # Create labels and buttons
        label = tk.Label(self, text="Home Page", font=self.controller.title_font, fg="#263942")
        label.grid(row=0, column=0, sticky="ew", pady=10)

        # Create the Sign Up button
        signup_button = tk.Button(self, text="Sign up", fg="#ffffff", bg="#263942",
                                  command=lambda: self.controller.show_frame("PageOne"))
        signup_button.grid(row=1, column=0, ipady=3, ipadx=7, pady=10)

        # Create the Set Reminder button
        reminder_button = tk.Button(self, text="Set Reminder", fg="#ffffff", bg="#263942",
                                    command=self.add_reminder)
        reminder_button.grid(row=3, column=0, ipady=3, ipadx=7, pady=10)

        # Create the Chat button
        chat_button = tk.Button(self, text="Chat", fg="#ffffff", bg="#263942",
                                command=self.open_chat)
        chat_button.grid(row=2, column=1, ipady=3, ipadx=7, pady=10)

        # Create the Address Book button
        address_book_button = tk.Button(self, text="Address Book", fg="#ffffff", bg="#263942",
                                         command=self.open_address_book)
        address_book_button.grid(row=1, column=2, ipady=3, ipadx=7, pady=10)

        # Create the Check User button
        check_user_button = tk.Button(self, text="Check a User", fg="#ffffff", bg="#263942",
                                      command=lambda: self.controller.show_frame("PageTwo"))
        check_user_button.grid(row=3, column=2, ipady=3, ipadx=2, pady=10)

        # Create the Quit button
        quit_button = tk.Button(self, text="Quit", fg="#263942", bg="#ffffff", command=self.on_closing)
        quit_button.grid(row=6, column=0, ipady=3, ipadx=32, pady=10)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            with open("nameslist.txt", "w") as f:
                for i in names:
                    f.write(i + " ")
            self.controller.destroy()

    def add_reminder(self):
        self.controller.add_reminder()

    def open_chat(self):
        self.controller.open_chat()

    def open_address_book(self):
        self.controller.open_address_book()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Enter the name", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, pady=10, padx=5)
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_name.grid(row=0, column=1, pady=10, padx=10)
        self.buttoncanc = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("StartPage"))
        self.buttonext = tk.Button(self, text="Next", fg="#ffffff", bg="#263942", command=self.start_training)
        self.buttonclear = tk.Button(self, text="Clear", command=self.clear, fg="#ffffff", bg="#263942")
        self.buttoncanc.grid(row=1, column=0, pady=10, ipadx=5, ipady=4)
        self.buttonext.grid(row=1, column=1, pady=10, ipadx=5, ipady=4)
        self.buttonclear.grid(row=1, ipadx=5, ipady=4, column=2, pady=10)
    def start_training(self):
        global names
        if self.user_name.get() == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif self.user_name.get() in names:
            messagebox.showerror("Error", "User already exists!")
            return
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        name = self.user_name.get()
        names.add(name)
        self.controller.active_name = name
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")
        
    def clear(self):
        self.user_name.delete(0, 'end')


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        self.controller = controller
        tk.Label(self, text="Enter your username", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, padx=10, pady=10)
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_name.grid(row=0, column=1, pady=10, padx=10)
        self.buttoncanc = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        self.buttonclear = tk.Button(self, text="Clear", command=self.clear, fg="#ffffff", bg="#263942")
        self.menuvar = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(self, self.menuvar, *names)
        self.dropdown.config(bg="lightgrey")
        self.dropdown["menu"].config(bg="lightgrey")
        self.buttonext = tk.Button(self, text="Next", command=self.next_foo, fg="#ffffff", bg="#263942")
        self.dropdown.grid(row=0, column=1, ipadx=8, padx=10, pady=10)
        self.buttoncanc.grid(row=1, ipadx=5, ipady=4, column=0, pady=10)
        self.buttonext.grid(row=1, ipadx=5, ipady=4, column=1, pady=10)
        self.buttonclear.grid(row=1, ipadx=5, ipady=4, column=2, pady=10)
        
    def next_foo(self):
        if self.user_name.get() == 'None':
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.user_name.get()
        self.controller.show_frame("PageFour")  
        
    def clear(self):
        self.user_name.delete(0, 'end')
        
    def nextfoo(self):
        if self.menuvar.get() == "None":
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.menuvar.get()
        self.controller.show_frame("PageFour")

    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))
            
class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.numimglabel = tk.Label(self, text="Number of images captured = 0", font='Helvetica 12 bold', fg="#263942")
        self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        self.capturebutton = tk.Button(self, text="Capture Data Set", fg="#ffffff", bg="#263942", command=self.capimg)
        self.trainbutton = tk.Button(self, text="Train The Model", fg="#ffffff", bg="#263942",command=self.trainmodel)
        self.capturebutton.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.trainbutton.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)

    def capimg(self):
        self.numimglabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("INSTRUCTIONS", "We will Capture 300 pic of your Face.")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images captured = "+str(x)))

    def trainmodel(self):
        if self.controller.num_of_images < 300:
            messagebox.showerror("ERROR", "Not enough Data, Capture at least 300 images!")
            return
        train_classifer(self.controller.active_name)
        messagebox.showinfo("SUCCESS", "The model has been successfully trained!")
        self.controller.show_frame("PageFour")
        



class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Face Recognition", font='Helvetica 16 bold')
        label.grid(row=0,column=0, sticky="ew")
        button1 = tk.Button(self, text="Face Recognition", command=self.openwebcam, fg="#ffffff", bg="#263942")
        #button2 = tk.Button(self, text="Emotion Detection", command=self.emot, fg="#ffffff", bg="#263942")
        #button3 = tk.Button(self, text="Gender and Age Prediction", command=self.gender_age_pred, fg="#ffffff", bg="#263942")
        button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        button1.grid(row=1,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        #button2.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        #button3.grid(row=2,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button4.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

    def openwebcam(self):
        main_app(self.controller.active_name)
        
    '''
    def gender_age_pred(self):
       ageAndgender()
    def emot(self):
        emotion()
'''


class MyApp(MainUI):
    def add_reminder(self):
        Popen(["python", "Reminder.py"])

    def open_chat(self):
        Popen(["python", "chat.py"])

    def open_address_book(self):
        Popen(["python", "Address_Book.py"])


app = MyApp()
app.iconphoto(True, tk.PhotoImage(file='icon.ico'))
app.mainloop()
