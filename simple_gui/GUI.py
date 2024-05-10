#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:36:58 2021

@author: bing
"""

# import all the required  modules
import threading
import select
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from chat_utils import *
import json
from tkinter import PhotoImage

# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""

        self.users = {}

    def login(self):
    # login window
        self.login_window = Toplevel()
    
    # set the title
        self.login_window.title("Welcome!")
        self.login_window.resizable(width = False, 
                             height = False)
        self.login_window.configure(width = 400,
                             height = 300)
        
    # set "WELCOME" 
        welcome_font = ("Arial", 40, "bold italic")
        colors = ['#FF0000', '#FFA500', '#FFFF00', '#008000', '#0000FF', '#4B0082']

        welcome_text = "WELCOME"
        for i, letter in enumerate(welcome_text):
            welcome_label = Label(self.login_window, text=letter, font=welcome_font, fg=colors[i % len(colors)])
            welcome_label.place(relx=0.15 + i * 0.1, rely=0.2)  # Adjust the position as needed
       
        
    #Text: First time user please sign up first
        signup_text = Label(self.login_window, text="First time user please sign up first", font="Helvetica 14 bold")
        signup_text.place(relx=0.1, rely=0.45)

    # Username input
        username_label = Label(self.login_window, text="UserName", font="Helvetica 12")
        username_label.place(relx=0.18, rely=0.585)
        self.entryName = Entry(self.login_window, font="Helvetica 14")
        self.entryName.place(relx=0.35, rely=0.55, relwidth=0.4, relheight=0.1)
        self.entryName.focus()
    
    # Password input
        password_label = Label(self.login_window, text="Password", font="Helvetica 12")
        password_label.place(relx=0.2, rely=0.695)
        self.entryPassword = Entry(self.login_window, font="Helvetica 14", show="*")
        self.entryPassword.place(relx=0.35, rely=0.673, relwidth=0.4, relheight=0.1)

    # Login Button
        self.login_btn = Button(self.login_window, text="Login", font="Helvetica 14 bold",
                            command=lambda: self.goAhead(self.entryName.get(), self.entryPassword.get()))
        self.login_btn.place(relx=0.2, rely=0.85)
        

    # Sign up Button
        self.signup_btn = Button(self.login_window, text="Sign up", font="Helvetica 14 bold",
                             command=self.signup_window)
        self.signup_btn.place(relx=0.383, rely=0.85)

    # Cancel Button
        self.cancel_btn = Button(self.login_window, text="Cancel", font="Helvetica 14 bold",
                             command=self.login_window.destroy)
        self.cancel_btn.place(relx=0.6, rely=0.85)
        self.signup_btn = Button(self.login_window, text = 'Sign up',font="Helvetica 14 bold",
                         command=self.signup_window)


        self.login_window.mainloop()


    def signup_window(self):
        self.signup_window = Toplevel()
        self.signup_window.title("Sign up now!")
        self.signup_window.resizable(width=False, height=False)
        self.signup_window.configure(width=400, height=300)

    # Label: User Name
        username_label = Label(self.signup_window, text="User Name:", font="Helvetica 12")
        username_label.place(relx=0.1, rely=0.1)

    # Entry: User Name
        self.entry_signup_username = Entry(self.signup_window, font="Helvetica 14")
        self.entry_signup_username.place(relx=0.4, rely=0.1, relwidth=0.5)

    # Label: Password
        password_label = Label(self.signup_window, text="Password:", font="Helvetica 12")
        password_label.place(relx=0.1, rely=0.3)

    # Entry: Password
        self.entry_signup_password = Entry(self.signup_window, font="Helvetica 14", show="*")
        self.entry_signup_password.place(relx=0.4, rely=0.3, relwidth=0.5)

    # Label: Confirm Password
        confirm_password_label = Label(self.signup_window, text="Confirm Password:", font="Helvetica 12")
        confirm_password_label.place(relx=0.1, rely=0.5)

    # Entry: Confirm Password
        self.entry_signup_confirm_password = Entry(self.signup_window, font="Helvetica 14", show="*")
        self.entry_signup_confirm_password.place(relx=0.4, rely=0.5, relwidth=0.5)

    # Button: Sign up now
        signup_now_btn = Button(self.signup_window, text="Sign up now", font="Helvetica 14 bold",
                                command=self.signup)
        signup_now_btn.place(relx=0.7, rely=0.7)

        self.signup_window.mainloop()


    def signup(self):
        username = self.entry_signup_username.get()
        password = self.entry_signup_password.get()
        confirm_password = self.entry_signup_confirm_password.get()

        if password == confirm_password:
            # Save the username and password
            # Show a message in a pop-up window
            
            # Close the sign-up window
            self.users[username] = password
            found=False
            f=open('information.txt', 'r')
            lines=f.readlines()
            for i, line in enumerate(lines):
                words = line.split() 
                if words[0] == username: 
                    words[1] = password  
                    lines[i] = ' '.join(words) + '\n' 
                    found = True  
                    messagebox.showinfo("Congratulations!", "You are a member of the chat system now!")                    
                    break
            f.close()

            f=open('information.txt', 'w')
            file=f.writelines(lines)
            f.close()

            if not found:   
                text_to_append = str(username) +" "+str(password)+"\n"
                with open('information.txt', 'a') as file:
                    file.write(text_to_append)
                self.signup_window.destroy()
            
                messagebox.showinfo("Congratulations!", "You are a member of the chat system now!")
            f.close()

        else:
            # Show a message in a pop-up window
            messagebox.showerror("Error", "Your two inputs are different, please check the password.")
        

    
  
    def goAhead(self, name, password):
        if len(name) == 0 or len(password)== 0:
            messagebox.showerror("Error", "Please enter both username and password!")

        else:
            f=open("information.txt","r")
            found = False
            right = False
            for line in f.readlines():
                line=line.strip("\n")
                line=line.split()
                if name==line[0]:
                    found=True
                    if str(password) == line[1]:
                        right=True
            f.close()

            if right==False:
                if found == False:
                    messagebox.showerror("Error","User does not exist, please sign up first!")
                if found == True:
                    messagebox.showerror("Error","Wrong password, please check and input again!") 


            else:
                msg = json.dumps({"action":"login", "name": name})
                self.send(msg)
                response = json.loads(self.recv())

                if response["status"] == 'ok':
                    self.login_window.destroy()
                    self.sm.set_state(S_LOGGEDIN)
                    self.sm.set_myname(name)
                    self.layout(name)
                    self.textCons.config(state = NORMAL)
                        # self.textCons.insert(END, "hello" +"\n\n")   
                    self.textCons.insert(END, menu +"\n\n")      
                    self.textCons.config(state = DISABLED)
                    self.textCons.see(END)
                # while True:
                #     self.proc()
        # the thread to receive messages
                    process = threading.Thread(target=self.proc)
                    process.daemon = True
                    process.start()
                    
                else: 
                    messagebox.showerror("Wrong information, please check and input again!")

 
    # The main layout of the chat
    def layout(self,name):
        
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 470,
                              height = 550,
                              bg = "#17202A")
        self.labelHead = Label(self.Window,
                             bg = "#17202A", 
                              fg = "#EAECEE",
                              text = self.name ,
                               font = "Helvetica 13 bold",
                               pady = 5)
          
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "#ABB2B9")
          
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
          
        self.textCons = Text(self.Window,
                             width = 20, 
                             height = 2,
                             bg = "#17202A",
                             fg = "#EAECEE",
                             font = "Helvetica 14", 
                             padx = 5,
                             pady = 5)
          
        self.textCons.place(relheight = 0.745,
                            relwidth = 1, 
                            rely = 0.08)
          
        self.labelBottom = Label(self.Window,
                                 bg = "#ABB2B9",
                                 height = 80)
          
        self.labelBottom.place(relwidth = 1,
                               rely = 0.825)
          
        self.entryMsg = Entry(self.labelBottom,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")
          
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
          
        self.entryMsg.focus()
          
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton(self.entryMsg.get()))
          
        self.buttonMsg.place(relx = 0.77,
                             rely = 0.008,
                             relheight = 0.06, 
                             relwidth = 0.22)
          
        self.textCons.config(cursor = "arrow")
          
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
          
        # place the scroll bar 
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
          
        scrollbar.config(command = self.textCons.yview)
          
        self.textCons.config(state = DISABLED)
  
    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.my_msg = msg
        # print(msg)
        self.entryMsg.delete(0, END)

    def proc(self):
        # print(self.msg)
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            # print(self.msg)
            if self.socket in read:
                peer_msg = self.recv()
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                # print(self.system_msg)
                self.system_msg += self.sm.proc(self.my_msg, peer_msg)
                self.my_msg = ""
                self.textCons.config(state = NORMAL)
                self.textCons.insert(END, self.system_msg +"\n\n")      
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)

    def run(self):
        self.login()
# create a GUI class object
if __name__ == "__main__": 
    g = GUI()