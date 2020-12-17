import tkinter as tk                
import pymysql.cursors
import pymysql
import array
    
import os
from pygame import mixer
from gtts import gTTS

class db:
    
    def __init__(self):
        connection = pymysql.connect('localhost','root','1598', db='filereader')
        self.connector = connection
        
    def insertTable(self, table_name, inserted_array ):
        inserted = False
        insert_val = responce = []
        if table_name :
            sql = "INSERT INTO "+table_name+" ("
            for key, value in inserted_array.items():
                sql += " `"+key+"`, "
            sql = sql[:-2]
            sql += ") values ( "
            for key, value in inserted_array.items():
                sql += "%s, "
                insert_val.append(value)
            sql = sql[:-2]
            sql += " ) "
            
            try:
                with self.connector.cursor() as cursor:
                    cursor.execute(sql, insert_val)
                    self.connector.commit()
                    inserted = True
            finally:
                self.connector.close()
            
            if inserted:
                responce = {"message": "inserted succesfully"}
            else:
                responce = {"message": "problem occured"}
                
            return responce
    
    def fetchAll(self, table_name, collum_name, where_arr = []):
        where_cond = ' WHERE 1'
        insert_val = result = response = []
        try:
            with self.connector.cursor() as cursor:
                sql = "SELECT "

                for collums in collum_name:
                    sql += "`"+collums+"`, ";                
                sql = sql[:-2]
                sql += " FROM "+table_name
                if where_arr:
                    for key, value in where_arr.items():
                        where_cond += ' and `'+key+'`= %s'

                    for key, value in where_arr.items():
                        insert_val.append(value)

                sql = sql+where_cond
                cursor.execute(sql, (insert_val))
                result = cursor.fetchall()
                response = result
        finally:
            self.connector.close()
            
        return response


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, MenuPage, RegisterPage,SuccessPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#6666ff')
        self.controller = controller
       
        self.controller.title("File Reader")
        self.controller.state("zoomed")
        self.controller.iconphoto(False,tk.PhotoImage(file='D:/Study/CODE/Python/TextToSpeechApp/Reader.png'))
        
        heading_label = tk.Label(self,
                                text='File Reader',
                                font=('Helvetica',45,'bold'),
                                fg='white',
                                bg= '#6666ff')
        heading_label.pack(pady=25)

        space_label = tk.Label(self,height=4,bg='#6666ff')
        space_label.pack()
        
        userpass_label = tk.Label(self,
                                text='Enter Your Username and Password',
                                font=('Helvetica',17),
                                bg='#6666ff',
                                fg='white')
        userpass_label.pack(pady=15)

        my_user=tk.StringVar()
        my_password=tk.StringVar()
        
        username_label = tk.Label(self,
                                text='Username',
                                font=('Helvetica',13),
                                bg='#6666ff',
                                fg='white')
        username_label.pack(pady=2)
        username_entry_box = tk.Entry(self,
                                    textvariable=my_user,
                                    font=('Helvetica',13),
                                    width=22)
        username_entry_box.focus_set()
        username_entry_box.pack(ipady=7)
        
        password_label = tk.Label(self,
                                text='Password',
                                font=('Helvetica',13),
                                bg='#6666ff',
                                fg='white')
        password_label.pack(pady=2)
        password_entry_box = tk.Entry(self,
                                    textvariable=my_password,
                                    font=('Helvetica',13),
                                    width=22)
        password_entry_box.pack(ipady=7)
        
        def handle_focus_in(_):
            password_entry_box.configure(fg='black',show='*')
        password_entry_box.bind('<FocusIn>',handle_focus_in)
        
        def check_password():
            db_obj = db()
            get_info = db_obj.fetchAll('registereduser', ['username','userpass'],{"username":my_user.get(),
                                                                                    "userpass":my_password.get()})
            if my_user.get() and my_password.get():   
                if get_info:
                    verify_user = get_info[0][0]
                    verify_pass = get_info[0][1]
                    if my_password.get() == verify_pass or my_user.get() == verify_user:
                            my_password.set('')
                            my_user.set('')
                            incorrect_password_label['text']=''
                            controller.show_frame('MenuPage')
                    else:
                        incorrect_password_label['text']='Incorrect Username or Password'
                else:
                    incorrect_password_label['text']='Incorrect Username or Password'
            else:
                incorrect_password_label['text']='Fields can\'t be Empty'
        
        login_button = tk.Button(self,
                                text='Login',
                                command=check_password,
                                relief='raised',
                                borderwidth=3,
                                width=28,
                                height=3)
        login_button.pack(pady=20)

        incorrect_password_label = tk.Label(self,
                                            text='',
                                            font=('Helvetica',13),
                                            fg='white',
                                            bg='#6666ff')
        incorrect_password_label.pack()

        register_label =  tk.Label(self,
                                text='New User ? Register Here',
                                font=('Helvetica',17,'italic'),
                                bg='#6666ff',
                                fg='black')
        register_label.pack(pady=30)

        def show_register_page():
            incorrect_password_label['text']=''
            controller.show_frame('RegisterPage')
        
        register_button = tk.Button(self,
                                text='Register',
                                command=show_register_page,
                                relief='raised',
                                borderwidth=3,
                                width=28,
                                height=3)
        register_button.pack(pady=10)


class MenuPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#6666ff')
        self.controller = controller
        var=0
        heading_label = tk.Label(self,
                                text='MAIN MENU',
                                font=('Helvetica',45,'bold'),
                                fg='white',
                                bg= '#6666ff')
        heading_label.pack(pady=20)

        type_label = tk.Label(self,
                                text='Type your Text Below',
                                font=('Helvetica',17),
                                bg='#6666ff',
                                fg='white')
        type_label.pack(pady=10)
        type_text_box = tk.Text(self,
                                font=('Helvetica',13),
                                width=90,
                                height=10)
        type_text_box.pack(pady=5)
        
        def write_file():
            file = open("Read.txt", "w")
            file.write(type_text_box.get("1.0", "end-1c"))
            file.close()
            read_file()
       
        def read_file():
            v=0
            file = open("Read.txt", "r")
            file_text = file.read()
            file.close()
            if(var==1):
                v=1
            if(var==2):
                v=2
            play_text_file(file_text,v)
        
        def play_text_file(file_text,v):
            if(v==1):
                myobj = gTTS(text=file_text, lang='en', slow=True)
            else:
                myobj = gTTS(text=file_text, lang='en', slow=False)
        
            if (os.path.exists("D:/Study/CODE/Python/TextToSpeechApp/readcon.mp3")):
                os.remove("D:/Study/CODE/Python/TextToSpeechApp/readcon.mp3")
    
            myobj.save("readcon.mp3");
            mixer.init()
            mixer.music.load('D:/Study/CODE/Python/TextToSpeechApp/readcon.mp3')
            mixer.music.play()
            while mixer.music.get_busy() == True:
                continue
            mixer.stop()    
            mixer.quit()
        
        slow_read=tk.Radiobutton(self,
                                text="Slow speech",
                                font=('Helvetica',12,'bold'),
                                variable=var,
                                value=1,
                                bg='#6666ff',
                                fg='black')
        slow_read.pack(pady=5)
        
        fast_read=tk.Radiobutton(self,
                                text="Fast speech",
                                font=('Helvetica',12,'bold'),
                                variable=var,
                                value=2,
                                bg='#6666ff',
                                fg='black')
        fast_read.pack(pady=5)
        
        voice_button = tk.Button(self,
                                text='Read',
                                command=write_file,
                                relief='raised',
                                borderwidth=3,
                                width=38,
                                height=3)
        voice_button.pack(pady=10)
        
        def goto_login_page():
            type_text_box.delete('1.0','end-1c')
            controller.show_frame('StartPage')
        
        back_button = tk.Button(self,
                                text='Back',
                                command=goto_login_page,
                                relief='raised',
                                borderwidth=3,
                                width=38,
                                height=3)
        back_button.pack(pady=40)


class RegisterPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#6666ff')
        self.controller = controller

        heading_label = tk.Label(self,
                                text='File Reader',
                                font=('Helvetica',45,'bold'),
                                fg='white',
                                bg= '#6666ff')
        heading_label.pack(pady=25)

        userpass_label = tk.Label(self,
                                text='Enter your Registration Details ',
                                font=('Helvetica',17),
                                bg='#6666ff',
                                fg='white')
        userpass_label.pack(pady=15)

        my_user=tk.StringVar()
        my_password=tk.StringVar()
        my_email=tk.StringVar()
        my_confirmpass =tk.StringVar()
        
        # Username 
        username_label = tk.Label(self,
                                text='Username*',
                                font=('Helvetica',13),
                                bg='#6666ff',
                                fg='white')
        username_label.pack(pady=2)
        username_entry_box = tk.Entry(self,
                                    textvariable=my_user,
                                    font=('Helvetica',13),
                                    width=30)
        username_entry_box.focus_set()
        username_entry_box.pack(ipady=7)
        #Email ID
        email_label = tk.Label(self,
                                text='Email ID*',
                                font=('Helvetica',13),
                                bg='#6666ff',
                                fg='white')
        email_label.pack(pady=2)
        email_entry_box = tk.Entry(self,
                                    textvariable=my_email,
                                    font=('Helvetica',13),
                                    width=30)
        email_entry_box.pack(ipady=7)
        #Password
        password_label = tk.Label(self,
                                text='Password*',
                                font=('Helvetica',13),
                                bg='#6666ff',
                                fg='white')
        password_label.pack(pady=2)
        password_entry_box = tk.Entry(self,
                                    textvariable=my_password,
                                    font=('Helvetica',13),
                                    width=30)
        password_entry_box.pack(ipady=7)
        #Confirm Password
        confirmpass_label = tk.Label(self,
                                text='Confirm Password*',
                                font=('Helvetica',13),
                                bg='#6666ff',
                                fg='white')
        confirmpass_label.pack(pady=2)
        confirmpass_entry_box = tk.Entry(self,
                                    textvariable=my_confirmpass,
                                    font=('Helvetica',13),
                                    width=30)
        confirmpass_entry_box.pack(ipady=7)
        
        def handle_focus_in_pass(_):
            password_entry_box.configure(fg='black',show='*')
        
        def handle_focus_in_conpass(_):
            confirmpass_entry_box.configure(fg='black',show='*')
        
        password_entry_box.bind('<FocusIn>',handle_focus_in_pass)
        confirmpass_entry_box.bind('<FocusIn>',handle_focus_in_conpass)                                                                       
        
        def check_existing_user():
            db_obj = db()
            exist_user_info = db_obj.fetchAll('registereduser', ['username'],{"username":my_user.get()})
            if not exist_user_info:
                flag = 0
            else:
                flag = 1
            return flag
        
        def check_existing_mail(): 
            db_obj = db()
            exist_mail_info = db_obj.fetchAll('registereduser', ['usermail'],{"usermail":my_email.get()}) 
            if not exist_mail_info:
                flag = 0
            else:
                flag = 1  
            return flag  
        
        def check_register():
            if my_user.get() and my_email.get() and my_password.get() and my_confirmpass.get():
                if len(my_password.get()) >=8 and len(my_confirmpass.get()) >=8:
                    user_flag = check_existing_user()
                    mail_flag = check_existing_mail()
                    if user_flag == 0:
                        if mail_flag == 0:
                            if my_password.get() == my_confirmpass.get():
                                db_obj = db()
                                inserting_arr = {"username":my_user.get(), 
                                                "usermail":my_email.get(),
                                                "userpass":my_password.get(), 
                                                "userconfirmpass":my_confirmpass.get()}
                                db_obj.insertTable('registereduser', inserting_arr)
                                my_user.set('')
                                my_email.set('')
                                my_password.set('')
                                my_confirmpass.set('')
                                matching_password_label['text']=''
                                controller.show_frame('SuccessPage')
                            else:
                                matching_password_label['text']='Password Doesn\'t match'
                        else:
                            matching_password_label['text']='Email already Taken'
                    else:
                        matching_password_label['text']='User already Exists'
                else:
                    matching_password_label['text']='Password must be atleast 8 Characters'
            else:
                matching_password_label['text']='* All Fields are Mandatory'


        register_button = tk.Button(self,
                                text='Submit',
                                command=check_register,
                                relief='raised',
                                borderwidth=3,
                                width=38,
                                height=3)
        register_button.pack(pady=20)
        matching_password_label = tk.Label(self,
                                            text='',
                                            font=('Helvetica',13),
                                            fg='white',
                                            bg='#6666ff')
        matching_password_label.pack()
        
        def goto_login_page():
            my_user.set('')
            my_email.set('')
            my_password.set('')
            my_confirmpass.set('')
            matching_password_label['text']=''
            controller.show_frame('StartPage')
            
        back_button = tk.Button(self,
                                text='Back',
                                command=goto_login_page,
                                relief='raised',
                                borderwidth=3,
                                width=38,
                                height=3)
        back_button.pack(pady=40)


class SuccessPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#6666ff')
        self.controller = controller

        success_label = tk.Label(self,
                                text='Registration Successful',
                                font=('Helvetica',20),
                                bg='#6666ff',
                                fg='white')
        success_label.pack(pady=15)

        def goto_login_page():
            controller.show_frame('StartPage')

        back_button = tk.Button(self,
                                text='Click Here to Login',
                                command=goto_login_page,
                                relief='raised',
                                borderwidth=3,
                                width=25,
                                height=3)
        back_button.pack(pady=40)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()