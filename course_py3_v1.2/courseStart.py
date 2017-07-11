from tkinter import *

g_user=''
g_pwd=''
g_mail=''
g_mailpwd=''
g_course=''

def submit(user,pwd,mail,mailpwd,course,root):
    global g_user
    g_user=user.get()
    global g_pwd
    g_pwd=pwd.get()
    global g_mail
    g_mail=mail.get()
    global g_mailpwd
    g_mailpwd=mailpwd.get()
    global g_course
    g_course=course.get()
    root.destroy()

def draw():
    root=Tk()
    root.title('4m3AccessTool')

    l_user=Label(root,text = 'user: ')
    l_user.grid(row = 0,sticky = W)
    l_pwd=Label(root,text = 'password: ')
    l_pwd.grid(row = 1,sticky = W)
    l_mail=Label(root,text = 'QQ mail: ')
    l_mail.grid(row = 2,sticky = W)
    l_mailpwd=Label(root,text = 'mail password: ')
    l_mailpwd.grid(row = 3,sticky = W)
    l_course=Label(root,text = 'course ID: ')
    l_course.grid(row = 4,sticky = W)

    user=StringVar()
    pwd=StringVar()
    mail=StringVar()
    mailpwd=StringVar()
    course=StringVar()

    e_user=Entry(root,textvariable = user)
    e_user.grid(row = 0,column = 1,sticky = E)
    e_pwd=Entry(root,textvariable = pwd)
    e_pwd['show']='*'
    e_pwd.grid(row = 1,column = 1,sticky = E)
    e_mail=Entry(root,textvariable = mail)
    e_mail.grid(row = 2,column = 1,sticky = E)
    e_mailpwd=Entry(root,textvariable = mailpwd)
    e_mailpwd['show']='*'
    e_mailpwd.grid(row = 3,column = 1,sticky = E)
    e_course=Entry(root,textvariable = course)
    e_course.grid(row = 4,column = 1,sticky = E)

    b_confirm=Button(root,text = 'confirm',command = lambda:submit(user,pwd,mail,mailpwd,course,root))
    b_confirm.grid(row = 5,column = 1,sticky = E)

    root.mainloop()

def getUser():
    return g_user

def getPwd():
    return g_pwd

def getMail():
    return g_mail

def getMailPwd():
    return g_mailpwd

def getCourse():
    return g_course

if __name__=='__main__':
    draw()