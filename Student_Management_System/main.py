
import re
import tkinter as tk
from tkinter.ttk import Combobox
from tkinter.filedialog import askopenfilename,askdirectory
from PIL import Image,ImageTk,ImageDraw, ImageFont,ImageOps
from PIL import Image
from io import BytesIO
Image.MAX_IMAGE_PIXELS = None  # Disable the warning
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import my_email

from tkinter.ttk import Combobox, Treeview
from tkinter.scrolledtext import ScrolledText



import random
import sqlite3
import os
import win32api

import threading



            


root = tk.Tk()
root.geometry('800x800')
root.title('Tkinter Hub (Student Management System)')

bg_color = '#273b7a'

login_student_icon = tk.PhotoImage(file="C:\\Users\\sunai\\OneDrive\\Desktop\\Student_Management_System\\Images\\login_student_img.png")
login_admin_icon = tk.PhotoImage(file="C:\\Users\\sunai\\OneDrive\\Desktop\\Student_Management_System\\Images\\admin_img.png")
add_student_icon = tk.PhotoImage(file="C:\\Users\\sunai\\OneDrive\\Desktop\\Student_Management_System\\Images\\add_student_img.png")
locked_icon = tk.PhotoImage(file="C:\\Users\\sunai\\OneDrive\\Desktop\\Student_Management_System\\Images\\locked.png")
unlocked_icon = tk.PhotoImage(file="C:\\Users\\sunai\\OneDrive\\Desktop\\Student_Management_System\\Images\\unlocked.png")
add_student_pic_icon = tk.PhotoImage(file="C:\\Users\\sunai\\OneDrive\\Desktop\\Student_Management_System\\Images\\add_image.png")


def init_database():
    with sqlite3.connect('C:\\Users\\sunai\\OneDrive\\Desktop\\Student_Management_System\\student_acounts.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id_number TEXT PRIMARY KEY,
            password TEXT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            phone_number TEXT,
            student_class TEXT,
            email TEXT,
            
            
            pic_data BLOB
        )
        ''')
        connection.commit()

def check_id_already_exists(id_number):
    connection = sqlite3.connect('student_acounts.db')
    cursor = connection.cursor()
   
    cursor.execute('SELECT id_number FROM data WHERE id_number = ?', (id_number,))
    connection.commit()
    response = cursor.fetchall()
        
    connection.close()
    return response

def check_valid_password(id_number, password):
    connection = sqlite3.connect('student_acounts.db')
    cursor = connection.cursor()
    
    cursor.execute('SELECT * FROM data WHERE id_number = ? AND password = ?', (id_number, password))
    connection.commit()
    response = cursor.fetchall()
    connection.close()          
    return response

def add_data(id_number, password, name, age, gender, phone_number, student_class, email, pic_data):
    connection = sqlite3.connect('student_acounts.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (id_number, password, name, age, gender, phone_number, student_class, email, pic_data))
    connection.commit()
    connection.close()

    

    
def confirmation_box(message):
    answer = tk.BooleanVar()
    answer.set(False)
    
    def action(ans):
        answer.set(ans)
        confirmation_box_fm.destroy()
        
    confirmation_box_fm = tk.Frame(root, highlightbackground=bg_color, highlightthickness=3)
    message_lb = tk.Label(confirmation_box_fm, text=message, font=('Bold', 15))
    message_lb.pack(pady=20)
    
    cancel_btn = tk.Button(confirmation_box_fm, text='Cancel', font=('Bold', 15), bd=0, bg=bg_color, fg='white', command=lambda: action(False))
    cancel_btn.place(x=50, y=160)
    yes_btn = tk.Button(confirmation_box_fm, text='Yes', font=('Bold', 15), bd=0, bg=bg_color, fg='white', command=lambda: action(True))
    yes_btn.place(x=190, y=160, width=80)
    
    confirmation_box_fm.place(x=233, y=120, width=320, height=220)
    root.wait_window(confirmation_box_fm)
     
    return answer.get()  # Corrected line


def message_box(message):
    message_box_fm = tk.Frame(root,highlightbackground=bg_color,highlightthickness=3)
    message_box_fm.place(x=240, y=120, width=350, height=200) 
    close_btn = tk.Button(message_box_fm, text= 'X', bd =0 , font = ('Bold',13),fg=bg_color, command=lambda: message_box_fm.destroy())
    close_btn.place(x = 320, y=5 )
    message_lb = tk.Label(message_box_fm,text= message, font=('Bold',15))
    message_lb.pack(pady=50)  

def darw_student_card(student_pic_path, student_data):
    labels ="""  
ID Number:
Name:
Gender:
Age:
Class:
Contact:
Email:
"""

    stud_data = f'''
396943,
Sit,
male,
27,
12th,
9758658575,
sit@gmail.com 



'''
    
    student_card = Image.open("C:\\Users\\sunai\\OneDrive\\Desktop\\Student_Management_System\\Images\\resized_student_card.png")
    
   
    
    
    
    

# Open the image
    pic = Image.open(student_pic_path)
    





    student_card.paste(pic, (40, 35))
    draw = ImageDraw.Draw(student_card)
    
    
    heading_font = ImageFont.truetype("bahnschrift.ttf", 30, encoding="unic")
    labels_font = ImageFont.truetype("arial.ttf", 22, encoding="unic")
    data_font =  ImageFont.truetype("bahnschrift.ttf", 22, encoding="unic")


# Change size as needed




    draw.text(xy=(250, 60), text= 'Student Card', fill=(0, 0, 0),font = heading_font)
    draw.multiline_text(xy=(35,225),text=labels,fill=(0,0,0),font=labels_font,spacing=6)
    draw.multiline_text(xy=(185,235),text=student_data,fill=(0,0,0),font=data_font,spacing=6)
    
    return  student_card
import os
import tkinter as tk
from tkinter.filedialog import askdirectory
from PIL import ImageTk
import win32api

def student_card_page(student_card_obj, bypass_login_page=False):
    
    def save_student_card():
        path = askdirectory()
        
        if path:
            print(path)
            # Construct the full path for saving
            full_path = os.path.join(path, "Stored_student_Image.png")
            student_card_obj.save(full_path)
            print(f"Student card saved at: {full_path}")

    def print_student_card():
        path = askdirectory()
        
        if path:
            print(path)
            # Construct the full path for saving
            full_path = os.path.join(path, "temp_pic.png")
            student_card_obj.save(full_path)
            win32api.ShellExecute(0, 'print', full_path, None, '.', 0)
            print(f"Student card sent to printer from: {full_path}")
    
    def close_page():
        student_card_page_fm.destroy()
        
        if not bypass_login_page:
        
            root.update()
            student_login_page()
        
    student_card_img = ImageTk.PhotoImage(student_card_obj)
    student_card_page_fm = tk.Frame(root, highlightbackground=bg_color, highlightthickness=3)
    
    heading_lb = tk.Label(student_card_page_fm, text='Student Card', bg=bg_color, fg='white', font=('Bold', 18))
    heading_lb.place(x=0, y=0, width=750)
    close_btn = tk.Button(student_card_page_fm, text='X', bg=bg_color, fg='white', font=('Bold', 13), bd=0, command=close_page)
    close_btn.place(x=715, y=0)
    
    student_card_lb = tk.Label(student_card_page_fm, image=student_card_img)
    student_card_lb.place(x=190, y=50)
    student_card_lb.image = student_card_img
   
    student_card_page_fm.place(x=50, y=30, width=750, height=800)   
    save_student_card_btn = tk.Button(student_card_page_fm, text='Save Student Card', bg=bg_color, fg='white', font=('Bold', 15), bd=1, command=save_student_card) 
    save_student_card_btn.place(x=325, y=575)  
    print_student_card_btn = tk.Button(student_card_page_fm, text='🖨️', bg=bg_color, fg='white', font=('Bold', 15), bd=1, command=print_student_card) 
    print_student_card_btn.place(x=515, y=575)
    
    
    

    

def welcome_page():
    
    def forward_to_student_login_page():
        welcome_page_fm.destroy()
        student_login_page()
    def forward_to_admin_login():
        welcome_page_fm.destroy()
        admin_login_page()
    def forward_to_add_acount_page():
        welcome_page_fm.destroy()
        root.update()
        add_acount_page()        
        

    welcome_page_fm = tk.Frame(root ,highlightbackground=bg_color,highlightthickness=3)
    heading_lb = tk.Label(welcome_page_fm,text='Welcome To\n Student Management System',bg=bg_color, fg ='white',font=('Bold',18))
    heading_lb.place(x=0,y=0,width=600)

    student_login_img = tk.Button(welcome_page_fm, image=login_student_icon,bd=0)
    student_login_img.place(x=-50, y=150, width =400)

    student_login_btn = tk.Button(welcome_page_fm, text='Login Student',bg =bg_color,fg='white', font =('Bold',15),bd=3,command=forward_to_student_login_page)
    student_login_btn.place(x=230, y=175)


 
    admin_login_img = tk.Button(welcome_page_fm, image=login_admin_icon,bd=0)
    admin_login_img.place(x=-50, y=250, width =400)

    admin_login_btn = tk.Button(welcome_page_fm, text='Login Admin',bg =bg_color,fg='white', font =('Bold',15),bd=3,command=forward_to_admin_login)
    admin_login_btn.place(x=230, y=275)





    add_student_img = tk.Button(welcome_page_fm, image=add_student_icon,bd=0)
    add_student_img.place(x=-50, y=350, width =400)

    add_student_btn = tk.Button(welcome_page_fm, text='Add Student',bg =bg_color,fg='white', font =('Bold',15),bd=3,command=forward_to_add_acount_page)
    add_student_btn.place(x=230, y=375)


    welcome_page_fm.pack(pady=30)
    welcome_page_fm.pack_propagate(False)
    welcome_page_fm.configure(width=600,height=600)
    
def sendmail_to_student(email, message, subject):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    username = my_email.email_address
    password = my_email.password
    msg = MIMEMultipart()
    
    msg['Subject']= subject
    msg['From'] = username
    msg["To"] = email
    
    msg.attach(MIMEText(_text=message, _subtype='html'))
    smtp_connection = smtplib.SMTP(host=smtp_server, port= smtp_port)
    smtp_connection.starttls()
    smtp_connection.login(user=username, password=password)
    smtp_connection.sendmail(from_addr=username, to_addrs=email,msg=msg.as_string())
    
    smtp_connection.quit()
    print("Mail Sent Succesful.")
    
def forget_password_page():
    def recover_password():
        student_id = student_id_ent.get()
        print('Student ID Entered:', student_id)
        
        if check_id_already_exists(id_number=student_id):
            print('Correct ID')
            try:
                with sqlite3.connect('C:\\Users\\sunai\\OneDrive\\Desktop\\Student_Management_System\\student_acounts.db') as connection:
                    cursor = connection.cursor()
                    
                    # Combine queries to fetch both password and email in one go
                    cursor.execute("SELECT password, email FROM data WHERE id_number = ?", (student_id,))
                    result = cursor.fetchone()
                    
                    if result:
                        recovered_password, recovered_email = result  # Unpack the results
                        print(f'Recovered password for ID {student_id}: {recovered_password}')
                        print(f'Recovered email for ID {student_id}: {recovered_email}')
                        confirmation = confirmation_box(message=f"""We will Send\nYour Forget Password   
Via Your Email Address:
{recovered_email}
Do You Want to Continue""")
                        
                        if confirmation:
                            msg = f"""<h1>Your forget Password is:</h1>
                            <h2>{recover_password}</h2>
                            <p>Once Remember Your Password, After Delete This Message </p>"""  
                            sendmail_to_student(email=recovered_email, message=msg,subject="Password Recovery")  
                        
                        
                    else:
                        print('No data found for this ID.')
                        
            except sqlite3.Error as e:
                print(f"Database error: {e}")
        else:
            print('Incorrect ID')
            message_box(message='!Invalid ID Number')
        
   
            
    
    
    forget_password_page_fm = tk.Frame(root, highlightbackground=bg_color,highlightthickness=3 )
    heading_lb = tk.Label(forget_password_page_fm,text="⚠️ Forgetting Password", font=('Bold',15), bg=bg_color, fg='white' )
    heading_lb.place(x=0, y=0, width=350)
    close_btn = tk.Button(forget_password_page_fm, text='X',font=('Bold',13), bg=bg_color, fg='white', bd=0,command=lambda:forget_password_page_fm.destroy())
    close_btn.place(x=320, y=0)
    student_id_lb =  tk.Label(forget_password_page_fm, text='Enter Student ID Number.',font=('Bold',13))
    student_id_lb.place(x=70, y=40 )
    student_id_ent = tk.Entry(forget_password_page_fm, font=('Bold,15'),justify= tk.CENTER)
    student_id_ent.place(x=70, y=70, width=180)
    info_lb = tk.Label(forget_password_page_fm, text= """ Via Email Address Studenty
    We will Send to You
    Your Forget Password.""",justify= tk.LEFT)
    info_lb.place(x = 70, y=110)
    
    next_btn = tk.Button(forget_password_page_fm, text='Next',font=('Bold',13), bg=bg_color, fg='white', command=recover_password)
    next_btn.place(x=130, y=200, width=80)
    forget_password_page_fm.place(x=220, y=120, width=350, height=250)    

def fetch_student_data(query, params=None):
    connection = sqlite3.connect("C:\\Users\\sunai\\OneDrive\\Desktop\\Student_Management_System\\student_acounts.db")
    cursor = connection.cursor()
    
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
        
    response = cursor.fetchall()
    connection.close()
    return response

def student_dashboard(student_id):
    get_student_details = fetch_student_data("""
        SELECT name, age, gender, student_class, phone_number, email FROM data WHERE id_number = ?
    """, (student_id,))
    get_student_pic = fetch_student_data(f"""
    SELECT pic_data FROM data WHERE id_number == {student_id}
    """)
    student_pic =BytesIO(get_student_pic[0][0])
    print(student_pic)
    
    #print(get_student_details)
    
    
    
    def logout():
        confirm = confirmation_box(message='Do You Want to\n Logout Your Account')
        if confirm:
            dashboard_fm.destroy()
            welcome_page()
            root.update()
    
    def switch(indicator, page):
        home_btn_indicator.config(bg="#c3c3c3")
        student_card_btn_indicator.config(bg="#c3c3c3")
        secuirity_btn_indicator.config(bg="#c3c3c3")
        edit_btn_indicator.config(bg="#c3c3c3")
        delete_btn_indicator.config(bg="#c3c3c3")
        logout_btn_indicator.config(bg="#c3c3c3")
        indicator.config(bg=bg_color)
        for child in pages_fm.winfo_children():
            child.destroy()
            root.update()
            
        page()

        
        
    
    dashboard_fm = tk.Frame(root, highlightbackground=bg_color, highlightthickness=3)
    options_fm = tk.Frame(dashboard_fm,highlightbackground=bg_color,highlightthickness=2,bg='#c3c3c3')
    options_fm.place(x=0, y=0, width=180, height=700)
    home_btn = tk.Button(options_fm, text="Home", font=("Bold",15), fg=bg_color,bg="#c3c3c3",bd=0,command=lambda:switch(indicator=home_btn_indicator,page=home_page))
    home_btn.place(x=40, y=110)
    home_btn_indicator = tk.Label(options_fm,bg="#c3c3c3")
    home_btn_indicator.place(x=5, y=106, width=3, height=40)
    
    student_card_btn = tk.Button(options_fm, text="Student\nCard ", font=("Bold",15), fg=bg_color,bg="#c3c3c3",bd=0,justify=tk.LEFT,command=lambda:switch(indicator=student_card_btn_indicator,page=Student_Card_Page))
    student_card_btn.place(x=40, y=180)
    student_card_btn_indicator = tk.Label(options_fm,bg="#c3c3c3")
    student_card_btn_indicator.place(x=5, y=176, width=3, height=40)
    
    
    secuirity_btn = tk.Button(options_fm, text="Secuirity", font=("Bold",15), fg=bg_color,bg="#c3c3c3",bd=0,command=lambda:switch(indicator=secuirity_btn_indicator,page=secuirity_page))
    secuirity_btn.place(x=40, y=250)
    secuirity_btn_indicator = tk.Label(options_fm,bg="#c3c3c3")
    secuirity_btn_indicator.place(x=5, y=246, width=3, height=40)
    
    edit_data_btn = tk.Button(options_fm, text="Edit Data", font=("Bold",15), fg=bg_color,bg="#c3c3c3",bd=0,command=lambda:switch(indicator=edit_btn_indicator,page=edit_data_page))
    edit_data_btn.place(x=40, y=320)
    edit_btn_indicator = tk.Label(options_fm,bg="#c3c3c3")
    edit_btn_indicator.place(x=5, y=316, width=3, height=40)
    
    
    delete_account_btn = tk.Button(options_fm, text="Delete\nAccount", font=("Bold",15), fg=bg_color,bg="#c3c3c3",bd=0,justify=tk.LEFT,command=lambda:switch(indicator=delete_btn_indicator,page=delete_account_page))
    delete_account_btn.place(x=40, y=390)
    delete_btn_indicator = tk.Label(options_fm,bg="#c3c3c3")
    delete_btn_indicator.place(x=5, y=386, width=3, height=40)
    
    logout_btn = tk.Button(options_fm, text="Logout", font=("Bold",15), fg=bg_color,bg="#c3c3c3",bd=0,command=logout)
    logout_btn.place(x=40, y=460)
    logout_btn_indicator = tk.Label(options_fm,bg="#c3c3c3")
    logout_btn_indicator.place(x=5, y=456, width=3, height=40)
    
    def home_page():
        student_pic_image_obj = Image.open(student_pic)
        size = 100
        mask = Image.new(mode='L',size=(size,size))
        draw_circle = ImageDraw.Draw(im=mask)
        draw_circle.ellipse(xy=(0,0,size, size),fill=255,outline=True)
        
        output = ImageOps.fit(image=student_pic_image_obj,size=mask.size,centering=(1,1))
        output.putalpha(mask)
        
        student_picture =ImageTk.PhotoImage(output)
        
        home_page_fm = tk.Frame(pages_fm)
        
        student_pic_lb = tk.Label(home_page_fm,image=student_picture)
        student_pic_lb.image = student_picture
        
        student_pic_lb.place(x=10, y=10)
        
        hi_lb = tk.Label(home_page_fm, text=f"!Hi {get_student_details[0][0]}",font=('Bold', 15))
        hi_lb.place(x=130, y=50)
        
        student_details = f"""
Student ID: {student_id}\n
Name: {get_student_details[0][0]}\n
Age: {get_student_details[0][1]}\n
Gender: {get_student_details[0][2]}\n
Class: {get_student_details[0][3]}\n
Contact: {get_student_details[0][4]}\n
Email: {get_student_details[0][5]}\n
        
        """
        
        student_details_lb = tk.Label(home_page_fm,text=student_details,font=('Bold',13),justify=tk.LEFT)
        student_details_lb.place(x=20,y=130)
        home_page_fm.pack(fill=tk.BOTH, expand=True)
        
     
    def Student_Card_Page():
        student_details = f"""
{student_id}
{get_student_details[0][0]}
{get_student_details[0][2]}
{get_student_details[0][1]}
{get_student_details[0][3]}
{get_student_details[0][4]}
{get_student_details[0][5]}
        
        """
        student_card_image_obj = darw_student_card(student_pic_path=student_pic,student_data=student_details)
        
        def save_student_card():
            path = askdirectory()
            
            if path:
                print(path)
                # Construct the full path for saving
                full_path = os.path.join(path, "Stored_student_Image.png")
                student_card_image_obj.save(full_path)
                print(f"Student card saved at: {full_path}")

        def print_student_card():
            path = askdirectory()
            
            if path:
                print(path)
                # Construct the full path for saving
                full_path = os.path.join(path, "temp_pic.png")
                student_card_image_obj.save(full_path)
                win32api.ShellExecute(0, 'print', full_path, None, '.', 0)
                print(f"Student card sent to printer from: {full_path}")
        
        
        
        
        student_card_img = ImageTk.PhotoImage(student_card_image_obj)
        Student_Card_page_fm = tk.Frame(pages_fm)
        
        card_lb = tk.Label(Student_Card_page_fm, image=student_card_img)

        card_lb.image = student_card_img
        card_lb.place(x=20, y=50)
        save_student_card_btn = tk.Button(Student_Card_page_fm,text='Save Student Card',font=('Bold',15),bd=1, fg='White', bg=bg_color,command=save_student_card)
        save_student_card_btn.place(x=140, y=600)
        
        print_student_card_btn = tk.Button(Student_Card_page_fm,text='🖨️',font=('Bold',15),bd=1, fg='White', bg=bg_color,command=print_student_card)
        print_student_card_btn.place(x=340, y=600)
        
        
        
        Student_Card_page_fm.pack(fill=tk.BOTH, expand=True)
        
    def edit_data_page():
        edit_data_page_fm = tk.Frame(pages_fm)
        pic_path = tk.StringVar()
        pic_path.set("")
        
        def open_pic():
            path = askopenfilename()
            if path:
                try:
                    img = ImageTk.PhotoImage(Image.open(path).resize((180, 130), Image.Resampling.LANCZOS))
                    pic_path.set(path)

                    add_pic_btn.config(image=img)
                    add_pic_btn.image = img  # Maintain a reference
                except Exception as e:
                    print("Error loading image:", e)
                    
        def remove_highlight_warning(entry):
            if entry["highlightbackground"] != "gray":
                if entry.get() != "":
                    entry.config(highlightcolor=bg_color,highlightbackground="gray")   
                    
                    
        def check_invalid_email(email):
 
            pattern = r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$"

    
            match = re.match(pattern=pattern, string=email)
    
            return match  
                    
        def check_inputs():
            nonlocal get_student_details, get_student_pic, student_pic
            
            
            
            if student_name_ent.get() == "":
                student_name_ent.config(highlightcolor='red',highlightbackground='red')
                student_name_ent.focus()
                message_box(message='Student Full Name is Required')  
            
            
            elif student_age_ent.get() == "":
                student_age_ent.config(highlightcolor='red',highlightbackground='red')
                student_age_ent.focus()
                message_box(message='Student Age is Required')    
                
            elif student_contact_ent.get() == "":
                student_contact_ent.config(highlightcolor='red',highlightbackground='red')
                student_contact_ent.focus()
                message_box(message='Student Contact is Required')    
                
            elif student_email_ent.get() == "":
                student_email_ent.config(highlightcolor='red',highlightbackground='red')
                student_email_ent.focus()
                message_box(message='Student Email Address is Required')  
                
            elif not check_invalid_email(email= student_email_ent.get().lower()):
                student_email_ent.config(highlightcolor='red',highlightbackground='red')
                student_email_ent.focus()
                message_box(message='Pleaseb Enter a Valid\n Email Address')
                
            else :
                if pic_path.get()!= "":
                    new_student_picture = Image.open(pic_path.get()).resize((200,200))
                    new_student_picture.save('C:\\Users\\sunai\\OneDrive\\Desktop\\Student_Management_System\\student_card\\Stored_student_Image.png')
                    
                    with open('C:\\Users\\sunai\\OneDrive\\Desktop\\Student_Management_System\\student_card\\Stored_student_Image.png', 'rb') as read_new_pic:
                        new_picture_binary = read_new_pic.read()
                        read_new_pic.close()
                        
                    connection = sqlite3.connect('C:\\Users\\sunai\\OneDrive\\Desktop\\Student_Management_System\\student_acounts.db')
                    cursor = connection.cursor()
                    
                    cursor.execute(f"UPDATE data SET pic_data=? WHERE id_number == '{student_id}' ",[new_picture_binary])
                    
                    connection.commit()
                    connection.close()
                    
                    message_box(message='Data Successfully Updated')
                    
                name = student_name_ent.get()
                age = student_age_ent.get()
                selected_class = select_class_btn.get()
                contact_number = student_contact_ent.get()
                email_address = student_email_ent.get()
                
                connection = sqlite3.connect('C:\\Users\\sunai\\OneDrive\\Desktop\\Student_Management_System\\student_acounts.db')
                cursor = connection.cursor()
                    
                cursor.execute("""
                UPDATE data SET name=?, age=?, student_class=?, phone_number=?, email=? WHERE id_number=?
                """, (name, age, selected_class, contact_number, email_address, student_id))

                    
                connection.commit()
                connection.close()
                
                get_student_details = fetch_student_data("""
                SELECT name, age, gender, student_class, phone_number, email FROM data WHERE id_number = ?
                """, (student_id,))
                get_student_pic = fetch_student_data(f"""
                SELECT pic_data FROM data WHERE id_number == {student_id}
                """)
                student_pic =BytesIO(get_student_pic[0][0])
                        
                
                
                
                message_box(message='Data Successfully Updated')
                        
                
                         
        
               
        student_current_pic = ImageTk.PhotoImage(Image.open(student_pic))    
        add_pic_section_fm = tk.Frame(edit_data_page_fm,highlightbackground=bg_color,highlightthickness=3)
        add_pic_section_fm.place(x=12, y=11, width=180, height=130)
        add_pic_btn = tk.Button(add_pic_section_fm, image=student_current_pic, bd =0,command=open_pic)
        add_pic_btn.image = student_current_pic
        
        add_pic_btn.pack()
        
        student_name_lb = tk.Label(edit_data_page_fm,text='Enter Student Full Name.',font=('Bold',12))
        student_name_lb.place(x=5,y =155)
        student_name_ent = tk.Entry(edit_data_page_fm,font=('Bold',15),highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
    
    
    
        student_name_ent.place(x=5, y=185, width=180)
        student_name_ent.bind("<KeyRelease>",lambda e:remove_highlight_warning(entry=student_name_ent))
        student_name_ent.insert(tk.END, get_student_details[0][0])
        
        
        student_age_lb = tk.Label(edit_data_page_fm,text='Enter Student Age.',font=('Bold',12))
        student_age_lb.place(x=5,y =225)
        student_age_ent = tk.Entry(edit_data_page_fm,font=('Bold',15),highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
        student_age_ent.bind("<KeyRelease>",lambda e:remove_highlight_warning(entry=student_age_ent))
        student_age_ent.place(x=5, y=255, width=180)
        student_age_ent.insert(tk.END, get_student_details[0][1])
        
        student_contact_lb = tk.Label(edit_data_page_fm,text='Enter Contact Phone Number.',font=('Bold',12))
        student_contact_lb.place(x=5,y =295)
        student_contact_ent = tk.Entry(edit_data_page_fm,font=('Bold',15),highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
        student_contact_ent.place(x=5, y=320, width=180)
        student_contact_ent.bind("<KeyRelease>",lambda e:remove_highlight_warning(entry=student_contact_ent))
        student_contact_ent.insert(tk.END, get_student_details[0][4])
        
        student_class_lb = tk.Label(edit_data_page_fm,text="Select Student Class",font=('Bold',12))
        student_class_lb.place(x=5,y=365)
            
        select_class_btn =  Combobox(edit_data_page_fm, font=('Bold',15),state='readonly',values=class_list)
        select_class_btn.place(x=5, y=390, width=180, height=30)
        select_class_btn.set(get_student_details[0][3])
        
        student_email_lb = tk.Label(edit_data_page_fm,text="Select Student Email Address.",font=('Bold',12))
        student_email_lb.place(x=5,y=425)

        student_email_ent = tk.Entry(edit_data_page_fm,font=('Bold',15),highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
        student_email_ent.place(x=5, y=455, width=180)
        student_email_ent.bind("<KeyRelease>",lambda e:remove_highlight_warning(entry=student_email_ent))
        student_email_ent.insert(tk.END, get_student_details[0][-1])
            
        update_data_btn = tk.Button(edit_data_page_fm,text='Update',font=('bold',15),fg='white',bg=bg_color,bd=0, command=check_inputs)
        update_data_btn.place(x=300, y=455)
        edit_data_page_fm.pack(fill=tk.BOTH, expand=True)
        
    def secuirity_page():
        
        def show_hide_password():
            if current_password_ent['show']  =='*':
                current_password_ent.config(show='')
                show_hide_btn.config(image=unlocked_icon)
                
            else:
                current_password_ent.config(show='*')
                show_hide_btn.config(image=locked_icon)
                
        def set_password():
            if new_password_ent.get() != '':
                confirm = confirmation_box(message="Do You Want to Change\n Your Password?")
                if confirm:
                    connection = sqlite3.connect('C:\\Users\\sunai\\OneDrive\\Desktop\\Student_Management_System\\student_acounts.db ')
                    cursor = connection.cursor()
                    cursor.execute(f"""UPDATE data SET password = '{new_password_ent.get()}' WHERE id_number == '{student_id}' """)
                    connection.commit()
                    connection.close()
                    message_box(message='Password Change Succesfully')
                    
                    current_password_ent.config(state=tk.NORMAL)
                    current_password_ent.delete(0,tk.END)
                    current_password_ent.insert(0, new_password_ent.get())
                    current_password_ent.config(state='readonly')
                    current_password_ent.delete(0, tk.END)
                    
            else:
                message_box(message="Enter New Password Required")        
        
        secuirity_page_fm = tk.Frame(pages_fm)
        current_password_lb = tk.Label(secuirity_page_fm, text="Your Current Password",font=('Bold',17))
        current_password_lb.place(x=160, y=30)
        
        current_password_ent = tk.Entry(secuirity_page_fm, font=('Bold',15),justify=tk.CENTER, show='*')
        current_password_ent.place(x=166, y=90)
        
        student_current_password = fetch_student_data("SELECT password FROM data WHERE id_number = ?", (student_id,))
        
        
        current_password_ent.insert(tk.END, student_current_password[0][0])
        current_password_ent.config(state='readonly')
        
        show_hide_btn = tk.Button(secuirity_page_fm,image=locked_icon, bd =0,command=show_hide_password)
        show_hide_btn.place(x=400,y=77)
        
        change_password_lb = tk.Label(secuirity_page_fm, text='Change Password', font=('Bold', 15), bg='red', fg='white')
        change_password_lb.place(x=100,y=220, width=400)
        
        new_password_lb = tk.Label(secuirity_page_fm,text='Set New Password', font=("Bold",16))
        new_password_lb.place(x=200, y=290)
        
        new_password_ent = tk.Entry(secuirity_page_fm, font=('Bold',15),justify=tk.CENTER)
        new_password_ent.place(x=180, y=350)
        
        change_password_btn = tk.Button(secuirity_page_fm, text='SET Password', font=('Bold',13), bg=bg_color,fg='white',command=set_password)
        change_password_btn.place(x=230, y=410)
        
        
        
        secuirity_page_fm.pack(fill=tk.BOTH, expand=True)
        
        
        
    def delete_account_page():
        
        def confirm_delete_account():
            confirm = confirmation_box(message='Do You Want to Delete\nYour Account?')
            if confirm:
                connection = sqlite3.connect('C:\\Users\\sunai\\OneDrive\\Desktop\\Student_Management_System\\student_acounts.db')
                cursor = connection.cursor()
                
                cursor.execute(f"""
                DELETE FROM data WHERE id_number == '{student_id}'
                
                """)
                
                connection.commit()
                connection.close()
                dashboard_fm.destroy()
                welcome_page()
                root.update()
                message_box(message='Account Successfully Deleted')
        
        delete_account_page_fm = tk.Frame(pages_fm)
        
        delete_account_lb = tk.Label(delete_account_page_fm, text = '⚠️ Delete Account', bg='red', fg='white', font=('Bold',15) )
        delete_account_lb.place(x=55, y=100, width=430)
        
        delete_account_button = tk.Button(delete_account_page_fm,text='Delete Account', bg='red', fg='white',font=('Bold',13), command=confirm_delete_account)
        delete_account_button.place(x=225, y=200)
        
        delete_account_page_fm.pack(fill=tk.BOTH, expand=True)
        
        
    
    pages_fm = tk.Frame(dashboard_fm,bg='gray')
    pages_fm.place(x=190 ,y=5, width=550, height=665)
    home_page()
    
    dashboard_fm.pack(pady=5)
    dashboard_fm.pack_propagate(False)
    dashboard_fm.configure(width=750, height=700)


    
def student_login_page():
    
    def show_hide_password():
        if password_ent['show']  =='*':
            password_ent.config(show='')
            show_hide_btn.config(image=unlocked_icon)
            
        else:
            password_ent.config(show='*')
            show_hide_btn.config(image=locked_icon)
        
        
        
            
    def forward_to_welcome_page():
        student_login_page_fm.destroy()
        root.update()
        welcome_page()            

    def remove_highlight_warning(entry):
        if entry["highlightbackground"] != "gray":
            if entry.get() != "":
                entry.config(highlightcolor=bg_color,highlightbackground="gray")      
    
    
    
    def login_account():
        id_number = id_number_ent.get()
        verify_id_number = check_id_already_exists(id_number)
        print(f"Verification response: {verify_id_number}")  # Debug line
        if verify_id_number:
            print('ID is Correct')
            verify_password = check_valid_password(id_number=id_number_ent.get(),password=password_ent.get())
            if verify_password:
                id_number=id_number_ent.get()
                student_login_page_fm.destroy()
                student_dashboard(student_id=id_number)
                root.update()
            else:
                print('!Oops, Password is Incorrect') 
                password_ent.config(highlightcolor='red',highlightbackground="red")   
            
                message_box(message='Incorrect Password')      
                
        else:
            print('!Oops, ID is Incorrect') 
            id_number_ent.config(highlightcolor='red',highlightbackground="red")   
            
            message_box(message='Please Enter Valid Student ID')   

            
            
            
    student_login_page_fm = tk.Frame(root,highlightbackground=bg_color,highlightthickness=3)  
    heading_lb = tk.Label(student_login_page_fm,text='Student Login Page',bg=bg_color, fg ='white',font=('Bold',18))
    heading_lb.place(x=0,y=0,width=600)
    
    back_btn = tk.Button(student_login_page_fm, text='🠀',font=('Bold',20),fg=bg_color,bd=0,command=forward_to_welcome_page)
    back_btn.place(x = 5, y=40)

    stud_icon_lb = tk.Label(student_login_page_fm,image=login_student_icon)
    stud_icon_lb.place(x=260,y=60)

    id_number_lb = tk.Label(student_login_page_fm, text='Enter Student ID Number. ', font=('Bold',15), fg =bg_color )
    id_number_lb.place(x=180,y=200)
    

    id_number_ent = tk.Entry(student_login_page_fm,font=("Bold",15),justify=tk.CENTER, highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
    id_number_ent.place(x=180,y=240)
    id_number_ent.bind('<KeyRelease>',lambda e: remove_highlight_warning(entry=id_number_ent))

    password_lb = tk.Label(student_login_page_fm, text='Enter Student Password. ', font=('Bold',15), fg =bg_color )

    password_lb.place(x=180,y=310)
    password_ent = tk.Entry(student_login_page_fm,font=("Bold",15),justify=tk.CENTER, highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2,show='*')
    password_ent.place(x=180,y=350)
    password_ent.bind('<KeyRelease>',lambda e: remove_highlight_warning(entry=password_ent))

    show_hide_btn = tk.Button(student_login_page_fm,image=locked_icon, bd =0,command=show_hide_password)
    show_hide_btn.place(x=400,y=340)

    login_btn = tk.Button(student_login_page_fm,text='Login', font=('Bold',15),bg=bg_color,fg ='white',command=login_account)
    login_btn.place(x=193,y=410,width=200,height=40) 

    forget_password_btn = tk.Button(student_login_page_fm, text='⚠️\nForget Password',fg=bg_color,bd=0)
    forget_password_btn.place(x=250,y=450)




    student_login_page_fm.pack(pady=30)
    
    student_login_page_fm.pack_propagate(False)

    student_login_page_fm.configure(width=600,height=600)



def admin_dashboard():
    
    
    def switch(indicator,page):
        
        
        home_btn_indicator.config(bg='#c3c3c3')
        find_btn_indicator.config(bg='#c3c3c3')
        announcement_btn_indicator.config(bg='#c3c3c3')
        indicator.config(bg=bg_color)
        
        for child in pages_fm.winfo_children():
            child.destroy()
            root.update()
            
            page()
        
    
    
          
    
        
    
    
    
    
    
    
    dashboard_fm = tk.Frame(root,highlightbackground=bg_color, highlightthickness=3)
    
    
    
        
    options_fm = tk.Frame(dashboard_fm,highlightbackground=bg_color,highlightthickness=2,bg='#c3c3c3')
    options_fm.place(x=0, y=0, width=170, height=700)
    
    home_btn = tk.Button(options_fm, text='Home', font=('Bold',15), fg=bg_color, bg='#c3c3c3',bd=0, command=lambda: switch(indicator=home_btn_indicator,page=home_page))
    home_btn.place(x=45, y=110)
    home_btn_indicator = tk.Label(options_fm, text='', bg=bg_color)
    home_btn_indicator.place(x=5, y=106, width=3, height=50)
    
    
    find_btn = tk.Button(options_fm, text='Find\nStudent', font=('Bold',15), fg=bg_color, bg='#c3c3c3',bd=0,justify= tk.LEFT, command=lambda: switch(indicator=find_btn_indicator,page=find_student_page))
    find_btn.place(x=45, y=210)
    find_btn_indicator = tk.Label(options_fm, text='', bg='#c3c3c3')
    find_btn_indicator.place(x=5, y=206, width=3, height=70)
    
    

    announcement_btn = tk.Button(options_fm, text='Announce\n-Ment 📢', font=('Bold',15), fg=bg_color, bg='#c3c3c3',bd=0,justify= tk.LEFT, command=lambda: switch(indicator=announcement_btn_indicator,page= announcement_page))
    announcement_btn.place(x=45, y=310)
    announcement_btn_indicator = tk.Label(options_fm, text='', bg='#c3c3c3')
    announcement_btn_indicator.place(x=5, y=306, width=3, height=70)
    
    def logout():
        confirm = confirmation_box(message="Do You Want to\nLogout")
        if confirm:
            dashboard_fm.destroy()
            welcome_page()
            root.update()
    
    
    logout_btn = tk.Button(options_fm, text='Logout', font=('Bold',15), fg=bg_color, bg='#c3c3c3',bd=0,justify= tk.LEFT,command=logout)
    logout_btn.place(x=45, y=410)
    logout_btn_indicator = tk.Label(options_fm, text='', bg='#c3c3c3')
    logout_btn_indicator.place(x=5, y=406, width=3, height=50)
    
    
    def home_page():
        home_page_fm = tk.Frame(pages_fm)
        
        admin_icon_lb = tk.Label(home_page_fm, image=login_admin_icon)
        admin_icon_lb.image = login_admin_icon
        admin_icon_lb.place(x=30, y=70)
        
        hi_lb = tk.Label(home_page_fm, text='!Hi Admin', font=('Bold',15))
        hi_lb.place(x=150, y=100)
        
        class_list_lb = tk.Label(home_page_fm, text='Number of Students By Class.', font=('Bold',13),bg=bg_color, fg='white')
        class_list_lb.place(x=30, y=200, width=300)
        
        students_numbers_lb = tk.Label(home_page_fm, text='', font=('Bold',13), justify=tk.LEFT)
        students_numbers_lb.place(x=30, y=270)
        
        for i in class_list:    
            result = fetch_student_data(query=f"SELECT COUNT(*) FROM data WHERE student_class == '{i}' ")
            
            students_numbers_lb['text'] += f"{i} Class:    {result[0][0]}\n\n" 
            print(i,result)
        home_page_fm.pack(fill=tk.BOTH, expand= True) 
    
    
    def find_student_page():
        
        
        def find_student():
            found_data =''
            if find_by_option_btn.get()  == 'id':
                found_data=fetch_student_data(query=f"""     
                SELECT id_number, name, student_class, gender FROM data WHERE id_number == '{search_input.get()}'                   
                
                                   """)
                print(found_data)
                
                
            elif find_by_option_btn.get()  == 'name':
                found_data=fetch_student_data(query=f"""     
                SELECT id_number, name, student_class, gender FROM data WHERE name LIKE '%{search_input.get()}%'                   
                
                                   """)
                print(found_data)   
                
                
                
            elif find_by_option_btn.get()  == 'class':
                found_data=fetch_student_data(query=f"""     
                SELECT id_number, name, student_class, gender FROM data WHERE student_class == '{search_input.get()}'                   
                
                                   """)
                print(found_data)  
                
                
                
            elif find_by_option_btn.get()  == 'gender':
                found_data=fetch_student_data(query=f"""     
                SELECT id_number, name, student_class, gender FROM data WHERE gender == '{search_input.get()}'                   
                
                                   """)
                print(found_data)
                
                
            if found_data:
                
                for item in record_table.get_children():
                    record_table.delete(item)
                
                for details in found_data:
                    record_table.insert(parent='', index='end', values=details)
                
                    
            else:
                for item in record_table.get_children():
                    record_table.delete(item)
                    
                    
        def generate_student_card():
            
            selection = record_table.selection()
            selected_id = record_table.item(item=selection, option='values')[0] 
            get_student_details = fetch_student_data("""
            SELECT name, age, gender, student_class, phone_number, email FROM data WHERE id_number = ?
            """, (selected_id,))
            get_student_pic = fetch_student_data(f"""
            SELECT pic_data FROM data WHERE id_number == {selected_id}
            """)
            student_pic =BytesIO(get_student_pic[0][0])   
            
            student_details = f"""
{selected_id}
{get_student_details[0][0]}
{get_student_details[0][2]}
{get_student_details[0][1]}
{get_student_details[0][3]}
{get_student_details[0][4]}
{get_student_details[0][5]}
                    
        """
            student_card_image_obj = darw_student_card(student_pic_path=student_pic,student_data=student_details)
            student_card_page(student_card_obj=student_card_image_obj,bypass_login_page=True)   
            
                
        def clear_result():
            find_by_option_btn.set('id')
            
            search_input.delete(0, tk.END)
            
            for item in record_table.get_children():
                record_table.delete(item)
                
            generate_student_card_btn.config(state=tk.DISABLED)
                
                        
        
        search_filters = ["id", "name", "class", "gender"]
        
        find_student_page_fm = tk.Frame(pages_fm)
        find_student_record_lb = tk.Label(find_student_page_fm, text='Find Student Record', font=("Bold",13),fg="white", bg=bg_color)
        find_student_record_lb.place(x=20, y=23, width=500)
        
        
        find_by_lb = tk.Label(find_student_page_fm, text="Find By:", font=('Bold',12))
        find_by_lb.place(x=20, y=80)
        
        find_by_option_btn = Combobox(find_student_page_fm, font=("Bold",12),state="readonly", values= search_filters)
        find_by_option_btn.place(x=100, y=80, width=80)
        find_by_option_btn.set("id")
        
        search_input = tk.Entry(find_student_page_fm, font=("Bold",12))
        search_input.place(x=20, y=130)
        search_input.bind('<KeyRelease>',lambda e: find_student())
        
        
        record_table_lb = tk.Label(find_student_page_fm, text="Record Table", font=("Bold",13), bg=bg_color, fg="white")
        record_table_lb.place(x=20, y=190,width=500)
        
        
        record_table = Treeview(find_student_page_fm,show='headings')
        record_table.place(x=0, y=250, width=500 )
        record_table.bind('<<TreeviewSelect>>', lambda e: generate_student_card_btn.config(state=tk.NORMAL))
        
        # Correctly define the columns using a tuple
        record_table['columns'] = ('id', 'name', 'class', 'gender')
        
        record_table.column('#0', stretch=tk.NO, width=0)

        

        
        
        
        record_table.heading('id', text='ID Number', anchor=tk.W)
        record_table.column("id", width=50, anchor=tk.W)
        
        record_table.heading('name', text='Name', anchor=tk.W)
        record_table.column("name", width=90, anchor=tk.W)
        
        record_table.heading('class', text='Class', anchor=tk.W)
        record_table.column("class", width=40, anchor=tk.W)
        
        record_table.heading('gender', text='Gender', anchor=tk.W)
        record_table.column("gender", width=50, anchor=tk.W)
        
        generate_student_card_btn = tk.Button(find_student_page_fm,text='Generate Student Card', font=('Bold',13),bg=bg_color, fg='white',state=tk.DISABLED,command=generate_student_card)
        generate_student_card_btn.place(x=300, y=500)
        
        clear_btn = tk.Button(find_student_page_fm,text='Clear', font=('Bold',13),bg=bg_color, fg='white',command=clear_result)
        clear_btn.place(x=10, y=500)
        
        
        find_student_page_fm.pack(fill=tk.BOTH, expand=True)
        
        
    def announcement_page():
        
        
        selected_classes=[]
        def add_class(name):
            
            if selected_classes.count(name):
                selected_classes.remove(name)
                
            else:    
                selected_classes.append(name)
            print(selected_classes)
        
        
        
        def collect_emails():
            fetched_emails = []
            
            for _class in selected_classes:
                # Fetching emails from the database
                emails = fetch_student_data(f"SELECT email FROM data WHERE student_class == '{_class}'")
                
                for email_tuple in emails:
                    # Extract the email from the tuple
                    fetched_emails.append(email_tuple[0])  # Assuming email_tuple is like (email,)
                    
            # Start the email sending in a new thread
            thread = threading.Thread(target=send_announcement, args=(fetched_emails,))
            thread.start()

        def send_announcement(email_addresses):
            box_fm = tk.Frame(root, highlightbackground=bg_color, highlightthickness=3)
            
            heading_lb = tk.Label(box_fm, text='Sending Email', font=('Bold', 15), bg=bg_color, fg='white')
            heading_lb.place(x=0, y=0, width=300)
            
            sending_lb = tk.Label(box_fm, font=('Bold', 12), justify=tk.LEFT)
            sending_lb.pack(pady=50)
            
            box_fm.place(x=300, y=180, width=300, height=200)  
            
            subject = announcement_subject.get()  # Ensure this is a string
            message = f"<h3 style='white-space: pre-wrap; '>{announcement_message.get('0.0', tk.END)}</h3>"  # Ensure this is formatted as a string
            sent_count = 0
            
            for email in email_addresses:
                sending_lb.config(text=f"Sending To:\n{email}\n\n{sent_count + 1}/{len(email_addresses)}")  # Correct count display
                
                # Call the function to send the email
                try:
                    sendmail_to_student(email=email, subject=subject, message=message)
                    sent_count += 1  # Increment sent count only if email is sent successfully
                except Exception as e:
                    print(f"Failed to send to {email}: {e}")  # Handle any exceptions during sending

                # Update the label with the current sending status
                sending_lb.config(text=f"Sending To:\n{email}\n\n{sent_count}/{len(email_addresses)}")
                
            box_fm.destroy()
            message_box(message="Announcement Sent\nSuccessfully")

                    
                    
            
            
           
            
                    
                                  
            
            
           
            
        
        
        announcement_page_fm = tk.Frame(pages_fm)
        
        subject_lb = tk.Label(announcement_page_fm, text='Enter Announcement Subject.',font=('Bold',15))
        subject_lb.place(x=10,y=20)
        
        announcement_subject = tk.Entry(announcement_page_fm, font=('Bold',12))
        announcement_subject.place(x=10, y=65, width=310,height=25)
        
        announcement_message = ScrolledText(announcement_page_fm,font=('Bold',12))
        announcement_message.place(x=10, y=120, width=450, height=250)
        
        classes_list_lb = tk.Label(announcement_page_fm, text='Select Classes to Announce', font=('Bold',14))
        classes_list_lb.place(x=10, y=400)
        
        y_position = 450
        for grade in class_list:
            class_check_btn = tk.Checkbutton(announcement_page_fm, text=f"class {grade}",command= lambda grade= grade: add_class(name=grade))
            class_check_btn.place(x=10, y=y_position)
            y_position += 25
        
        send_announcement_btn = tk.Button(announcement_page_fm,text="Send Announcement",font=('Bold',12),bg=bg_color,fg='white',command=collect_emails)
        send_announcement_btn.place(x=300, y=620)
        
        announcement_page_fm.pack(fill=tk.BOTH,expand=True)    
    
        
    pages_fm =tk.Frame(dashboard_fm, background='gray')
    pages_fm.place(x=182, y=5, width=500, height=680)
    
    
    
    
    
    #announcement_page()
    #find_student_page()
    home_page()
     

    
    dashboard_fm.pack(padx=5)
    dashboard_fm.pack_propagate(False)
    dashboard_fm.configure(width=700, height=700)
    



    
def admin_login_page():    
    def show_hide_password():
            if password_ent['show']  =='*':
                password_ent.config(show='')
                show_hide_btn.config(image=unlocked_icon)
                
            else:
                password_ent.config(show='*')
                show_hide_btn.config(image=locked_icon)   
    
    def forward_to_welcome_page():
        admin_login_page_fm.destroy()
        root.update()
        welcome_page()                   
        
        
    def login_account():
        if admin_user_name_ent.get() == "admin":
            if password_ent.get()  == 'admin':
                admin_login_page_fm.destroy()
                root.update()
                
                admin_dashboard()
            
            else:
                message_box(message="Wrong Password")
        
        else:
            message_box(message="Wrong Usernme")
    
    
    admin_login_page_fm = tk.Frame(root,highlightbackground=bg_color,highlightthickness=3)  
    heading_lb = tk.Label(admin_login_page_fm,text='Admin Login Page',bg=bg_color, fg ='white',font=('Bold',18))
    heading_lb.place(x=0,y=0,width=600)
    admin_icon_lb = tk.Label(admin_login_page_fm,image=login_admin_icon)
    admin_icon_lb.place(x=260,y=60)
    
    back_btn = tk.Button(admin_login_page_fm, text='🠀',font=('Bold',20),fg=bg_color,bd=0,command=forward_to_welcome_page)
    back_btn.place(x = 5, y=40)

    admin_user_name_lb = tk.Label(admin_login_page_fm, text='Enter Admin User Name. ', font=('Bold',15), fg =bg_color )
    admin_user_name_lb.place(x=180,y=200)
        

    admin_user_name_ent = tk.Entry(admin_login_page_fm,font=("Bold",15),justify=tk.CENTER, highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
    admin_user_name_ent.place(x=180,y=240)

    password_lb = tk.Label(admin_login_page_fm, text='Enter Admin Password. ', font=('Bold',15), fg =bg_color )

    password_lb.place(x=180,y=310)
    password_ent = tk.Entry(admin_login_page_fm,font=("Bold",15),justify=tk.CENTER, highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2,show='*')
    password_ent.place(x=180,y=350)

    admin_login_page_fm.pack(pady=30)
    admin_login_page_fm.pack(pady=30)
    admin_login_page_fm.pack_propagate(False)
    admin_login_page_fm.configure(width=600,height=600)
    
    show_hide_btn = tk.Button(admin_login_page_fm,image=locked_icon, bd =0,command=show_hide_password)
    show_hide_btn.place(x=400,y=340)

    login_btn = tk.Button(admin_login_page_fm,text='Login', font=('Bold',15),bg=bg_color,fg ='white',command=login_account)
    login_btn.place(x=193,y=410,width=200,height=40) 

    forget_password_btn = tk.Button(admin_login_page_fm, text='⚠️\nForget Password',fg=bg_color,bd=0)
    forget_password_btn.place(x=250,y=450)
            

student_gender = tk.StringVar()
class_list = ['5th','6th','7th','8th','9th','10th','11th','12th']

def add_acount_page():
    pic_path = tk.StringVar()
    pic_path.set("")
    
    def open_pic():
        path = askopenfilename()
        if path:
            try:
                img = ImageTk.PhotoImage(Image.open(path).resize((180, 130), Image.Resampling.LANCZOS))
                pic_path.set(path)

                add_pic_btn.config(image=img)
                add_pic_btn.image = img  # Maintain a reference
            except Exception as e:
                print("Error loading image:", e)

            

    def forward_to_welcome_page():
        ans=confirmation_box(message='Do You Want To Leave\nRegisteration Form')
        if ans:
            add_acount_page_fm.destroy()
            root.update()
            welcome_page()
            
    def remove_highlight_warning(entry):
        if entry["highlightbackground"] != "gray":
            if entry.get() != "":
                entry.config(highlightcolor=bg_color,highlightbackground="gray")      
    
    def check_invalid_email(email):
 
        pattern = r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$"

 
        match = re.match(pattern=pattern, string=email)
 
        return match  
    
    def generate_id_number():
        generated_id =''
        for r in range(6):
            generated_id += str(random.randint(0,9))
            
        if not check_id_already_exists(id_number=generated_id):    
            print('id number:', generated_id)    
            
            student_id.config(state=tk.NORMAL)
            student_id.delete(0,tk.END)
            student_id.insert(tk.END, generated_id)
            student_id.config(state='readonly')
            
        else:
            generate_id_number()    
            
                
                
    def check_input_validation():
        if student_name_ent.get() == "":
            student_name_ent.config(highlightcolor='red',highlightbackground='red')
            student_name_ent.focus()
            message_box(message='Student Full Name is Required')
       
        elif student_age_ent.get() == "":
            student_age_ent.config(highlightcolor='red',highlightbackground='red')
            student_age_ent.focus()
            message_box(message='Student Age is Required') 
            
        elif student_contact_ent.get() == "":
            student_contact_ent.config(highlightcolor='red',highlightbackground='red')
            student_contact_ent.focus()
            message_box(message='Student Contact is Required')     
            
         
            
        elif select_class_btn.get()  == "":
                
            select_class_btn.focus()
            message_box(message="Select Student class is Required")
            
        elif student_email_ent.get() == "":
            student_email_ent.config(highlightcolor='red',highlightbackground='red')
            student_email_ent.focus()
            message_box(message='Student Email is Required') 
            
            
        elif acount_password_ent.get() == "" :
            acount_password_ent.config(highlightcolor='red' , highlightbackground='red')
            acount_password_ent.focus() 
            message_box(message="Create a Password is Required") 
            
        else :
            pic_data = b''
            if pic_path.get() != '':
                resize_pic = Image.open(pic_path.get()).resize((200, 200), Image.Resampling.LANCZOS)

                resize_pic.save('temp_pic.png')
                read_data = open('temp_pic.png','rb')
                pic_data = read_data.read()
                read_data.close()
                
            else:
                read_data = open('C:\\Users\\sunai\\OneDrive\\Desktop\\Student_Management_System\\Images\\add_image.png','rb')
                pic_data = read_data.read()
                read_data.close()
                pic_path.set('C:\\Users\\sunai\\OneDrive\\Desktop\\Student_Management_System\\Images\\add_image.png')
                
            
            add_data(id_number=student_id.get(),
                     password=acount_password_ent.get(),
                     name=student_name_ent.get(),
                     age = student_age_ent.get(),
                     gender= student_gender.get(),
                     phone_number = student_contact_ent.get(),
                     student_class=select_class_btn.get(),
                     email=student_email_ent.get(),
                     pic_data = pic_data
                     )
            
            
            data = f"""
{student_id.get()}

{student_name_ent.get()}
{student_gender.get()}
{student_age_ent.get()}
{select_class_btn.get()}
{student_contact_ent.get()}
{student_email_ent.get()}

            
"""
    
            
            get_student_card=darw_student_card(student_pic_path="C:\\Users\\sunai\\OneDrive\\Desktop\\Student_Management_System\\temp_pic.png",student_data=data) 
            student_card_page(student_card_obj=get_student_card)
            add_acount_page_fm.destroy()
            root.update()
            message_box('Account Successful Created')
            
        
                    
               
        
                        
                        
    add_acount_page_fm = admin_login_page_fm = tk.Frame(root,highlightbackground=bg_color,highlightthickness=3)


    add_pic_section_fm = tk.Frame(add_acount_page_fm,highlightbackground=bg_color,highlightthickness=3)
    add_pic_section_fm.place(x=10, y=0, width=180, height=130)
    add_pic_btn = tk.Button(add_pic_section_fm, image=add_student_pic_icon, bd =0,command=open_pic)
    add_pic_btn.pack()
    student_name_lb = tk.Label(add_acount_page_fm,text='Enter Student Full Name.',font=('Bold',12))
    student_name_lb.place(x=5,y =130)
    student_name_ent = tk.Entry(add_acount_page_fm,font=('Bold',15),highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
    
    
    
    student_name_ent.place(x=5, y=160, width=180)
    student_name_ent.bind("<KeyRelease>",lambda e:remove_highlight_warning(entry=student_name_ent))
    
    
    student_gender_lb = tk.Label(add_acount_page_fm,text= 'Select Student Gender.',font=('Bold',12))
    student_gender_lb.place(x=5, y=210)
    male_gender_btn = tk.Radiobutton(add_acount_page_fm,text='Male',font=('Bold',12),variable=student_gender,value='male')
    male_gender_btn.place(x=85,y=235)

    female_gender_btn = tk.Radiobutton(add_acount_page_fm,text='Female',font=('Bold',12),variable=student_gender,value='female')
    female_gender_btn.place(x=5,y=235)

    student_gender.set('male')
    student_age_lb = tk.Label(add_acount_page_fm,text='Enter Student Age.',font=('Bold',12))
    student_age_lb.place(x=5,y =275)
    student_age_ent = tk.Entry(add_acount_page_fm,font=('Bold',15),highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
    student_age_ent.bind("<KeyRelease>",lambda e:remove_highlight_warning(entry=student_age_ent))
    student_age_ent.place(x=5, y=310, width=180)
    
    
    add_acount_page_fm.pack(pady=5)

    student_contact_lb = tk.Label(add_acount_page_fm,text='Enter Contact Phone Number.',font=('Bold',12))
    student_contact_lb.place(x=5,y =345)
    student_contact_ent = tk.Entry(add_acount_page_fm,font=('Bold',15),highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
    student_contact_ent.place(x=5, y=370, width=180)
    student_contact_ent.bind("<KeyRelease>",lambda e:remove_highlight_warning(entry=student_contact_ent))
    student_class_lb = tk.Label(add_acount_page_fm,text="Select Student Class",font=('Bold',12))
    student_class_lb.place(x=5,y=400)
        
    select_class_btn =  Combobox(add_acount_page_fm, font=('Bold',15),state='readonly',values=class_list)
    select_class_btn.place(x=5, y=440, width=180, height=30)

    acount_password_lb = tk.Label(add_acount_page_fm, text='Create Account Password.',font=('Bold',12))
    acount_password_lb.place(x=300,y=170)

    acount_password_ent = tk.Entry(add_acount_page_fm,font=('Bold',15),highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
    acount_password_ent.place(x=328, y=200, width=180)
    acount_password_ent.bind("<KeyRelease>",lambda e:remove_highlight_warning(entry=acount_password_ent))

    add_acount_page_fm.pack_propagate(False)
    add_acount_page_fm.configure(width=600,height=600)

    student_id_lb = tk.Label(add_acount_page_fm,text='Student ID Number.',font=('Bold',12))
    student_id_lb.place(x=5,y =480)
    student_id = tk.Entry(add_acount_page_fm,font=('Bold',18),bd=0)
    student_id.place(x=150,y=480,width=80)
    
    student_id.config(state="readonly") 
    generate_id_number()
    
    id_info_lb =tk.Label(add_acount_page_fm,text="""  Autometically Generated ID Number
        ! Remeber Using This ID Number
        Student will Login Account.""",justify=tk.LEFT)
    id_info_lb.place(x=5, y=520)

    student_email_lb = tk.Label(add_acount_page_fm,text="Select Student Email Address.",font=('Bold',12))
    student_email_lb.place(x=300,y=25)

    student_email_ent = tk.Entry(add_acount_page_fm,font=('Bold',15),highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
    student_email_ent.place(x=330, y=60, width=180)
    student_email_ent.bind("<KeyRelease>",lambda e:remove_highlight_warning(entry=student_email_ent))
    
    email_info_lb =tk.Label(add_acount_page_fm,text="""  Via Email Address Student
    Can Recover Account
    ! In Case Forgetting Password And Also
    Student will get Future Notification.""",justify=tk.LEFT)
    email_info_lb.place(x=330, y=100)

    acount_password_lb = tk.Label(add_acount_page_fm,text='Create Account Password.',font=('Bold',12))


    acount_password_info_lb = tk.Label(add_acount_page_fm,text='''Via Student Created Password
            And Provided Student ID Number 
    Student Can Login Account.
                                    ''')
    acount_password_info_lb.place(x=300,y=250)
    home_btn = tk.Button(add_acount_page_fm, text ='Home', font =('Bold',15),bg='red',fg='white', bd=0,command=forward_to_welcome_page)
    home_btn.place(x=330,y=320)
 

    submit_btn = tk.Button(add_acount_page_fm, text ='Submit', font =('Bold',15),bg=bg_color,fg='white', bd=0,command=check_input_validation)
    submit_btn.place(x=450,y=320)



#init_database()
#add_acount_page()
#student_login_page()
#forget_password_page()
#student_dashboard(student_id=748358)
#student_card_page()
welcome_page()
#sendmail_to_student(email="shivamchoudhary1913@gmail.com",message="<h1>Hello World</h1>",subject="Testing")
#admin_dashboard()
#admin_login_page()

try:
    root.mainloop()
except KeyboardInterrupt:
    print("Application closed.")
