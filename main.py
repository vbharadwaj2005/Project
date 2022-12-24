import tkinter
from tkinter.font import Font
from PIL import ImageTk, Image
import mysql.connector as sql
import yfinance
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplfinance as mpf

root = tkinter.Tk()
root.geometry("640x480")
root.resizable(width = False, height = False)
root.title("Stock Market Analysis")
frame = tkinter.Frame(root)
frame.pack(expand = True, fill = "both")
font = Font(size = 14)
font1 = Font(family = "Comic Sans MS", size = 10)

connect = sql.connect(host = "localhost", user = "root", passwd = "", db = "stock")
cursor = connect.cursor()

stockSeen = dict(); companyNameText = str()

def login():
    # Login Page
    for widgets in frame.winfo_children():
        widgets.destroy()
    global bg
    global personIcon
    global userNameText
    global userNameValue
    global passwordText
    global show
    global hide
    photo = tkinter.PhotoImage(file="Icons/login.png")
    root.iconphoto(False, photo)
    cursor.execute("select * from user")
    a = cursor.fetchall(); u = list(); p = list(); ac = list()
    for i in a:
        u.append(i[0]); p.append(i[1]); ac.append(i[2])
    def check():
        if userNameText.get() in u and passwordText.get() in p:
            if ac[u.index(userNameText.get())].lower() == "a":
                adminHome()
            else:
                home()
        else:
            tkinter.Label(frame, text = "Incorrect User Name Or Password", bg = "#dcdcdc", fg = "red", font = font1).place(x = 220, y = 260)
            tkinter.Button(frame, text = "Forgot Password",  bg = "#dcdcdc", fg = "red", font = font1, borderwidth = 0, cursor = "hand2", command = forgot).place(x = 280, y = 285)
            tkinter.Button(frame, text = "Do You Want To Create An Account", bg = "#dcdcdc", font = font1, padx = 8, pady = 3, cursor = "hand2", command = signup).place(x = 205, y = 320)
    def my_show():
        if(seeText.get() == "1"):
            passwordText.config(show="")
            see.configure(image = hide)
            seeText.set("0")
        else:
            passwordText.config(show="*")
            see.configure(image = show)
            seeText.set("1")
    bg = ImageTk.PhotoImage(Image.open("Icons/bg.jpg"))
    tkinter.Label(frame, image = bg, height = 640, width = 450).pack(expand = True, fill = "both")
    tkinter.Frame(frame, height = 300, width = 290, bg = "#dcdcdc", borderwidth = "2", highlightbackground = "black",  relief = "raised").place(x = 180, y = 70)
    personIcon = tkinter.PhotoImage(file = "Icons/person.png", height = 40, width = 40)
    tkinter.Label(frame, image = personIcon, bg = "#dcdcdc").place(x = 220, y = 90)
    tkinter.Label(frame, text = "Login Page", bg = "#dcdcdc", font = font).place(x = 280, y = 100)
    tkinter.Label(frame, text = "User Name", bg = "#dcdcdc", font = font1).place(x = 220, y = 150)
    userNameValue = tkinter.StringVar()
    userNameText = tkinter.Entry(frame, width = 20, textvariable = userNameValue)
    userNameText.place(x = 300, y = 150)
    tkinter.Label(frame, text = "Password", bg = "#dcdcdc", font = font1).place(x = 220, y = 180)
    passwordText = tkinter.Entry(frame, width = 20, show = "*")
    passwordText.place(x = 300, y = 180)
    show = tkinter.PhotoImage(file = "Icons/show.png")
    hide = tkinter.PhotoImage(file = "Icons/hide.png")
    seeText = tkinter.StringVar(value = "1")
    see = tkinter.Button(frame, image = show, height = 20, width = 20, bg = "#dcdcdc", borderwidth = 0, textvariable = seeText, command = my_show)
    see.place(x = 430, y = 180)
    tkinter.Button(frame, text = "Submit", bg = "#dcdcdc", font = font1, padx = 8, pady = 3, cursor = "hand2", command = check).place(x = 290, y = 220)

def forgot():
    # Forgot Password Page
    for widgets in frame.winfo_children():
        widgets.destroy()
    global bg
    global personIcon
    global backIcon
    global userNameText
    global passwordText
    global retypePasswordText
    global show
    global hide
    photo = tkinter.PhotoImage(file="Icons/login.png")
    root.iconphoto(False, photo)
    def check():
        cursor.execute("select id from user")
        a = cursor.fetchall(); u = list()
        for i in a:
            u.append(i[0])
        if userNameText.get() == "":
            tkinter.Label(frame, text = "     Please Enter User Name      ", bg = "#dcdcdc", fg = "red", font = font1).place(x = 225, y = 315)
        elif passwordText.get() == "":
            tkinter.Label(frame, text = "      Please Enter Password      ", bg = "#dcdcdc", fg = "red", font = font1).place(x = 225, y = 315)
        elif passwordText.get() != retypePasswordText.get():
            tkinter.Label(frame, text = "        Password Not Same        ", bg = "#dcdcdc", fg = "red", font = font1).place(x = 225, y = 315)
        elif userNameText.get() not in u:
            tkinter.Label(frame, text = "       User Name Not Found       ", bg = "#dcdcdc", fg = "red", font = font1).place(x = 225, y = 315)
        else:
            cursor.execute("update user set pwd = '" + passwordText.get() + "' where id like'" + userNameText.get() + "'")
            connect.commit()
            login()
    def my_show():
        if(seeText.get() == "1"):
            passwordText.config(show = "")
            retypePasswordText.config(show = "")
            see.configure(image = hide)
            seeText.set("0")
        else:
            passwordText.config(show = "*")
            retypePasswordText.config(show = "*")
            see.configure(image = show)
            seeText.set("1")
    bg = ImageTk.PhotoImage(Image.open("Icons/bg.jpg"))
    tkinter.Label(frame, image = bg, height = 640, width = 480, borderwidth = 1).pack(expand = True, fill = "both")
    backIcon = tkinter.PhotoImage(file = "Icons/back.png")
    tkinter.Button(frame, image = backIcon, height = 40, width = 40, bg = "#dcdcdc", cursor = "hand2", command = login).place(x = 10, y = 10)
    tkinter.Frame(frame, height = 300, width = 290, bg = "#dcdcdc", borderwidth = "2", highlightbackground = "black",  relief = "raised").place(x = 180, y = 70)
    personIcon = tkinter.PhotoImage(file = "Icons/person.png", height = 40, width = 40)
    tkinter.Label(frame, image = personIcon, bg = "#dcdcdc").place(x = 220, y = 90)
    tkinter.Label(frame, text = "Change Password", bg = "#dcdcdc", font = font).place(x = 270, y = 100)
    tkinter.Label(frame, text = "User Name", bg = "#dcdcdc", font = font1).place(x = 220, y = 150)
    userNameText = tkinter.Entry(frame, width = 20)
    userNameText.place(x = 300, y = 150)
    tkinter.Label(frame, text = "Password", bg = "#dcdcdc", font = font1).place(x = 220, y = 180)
    passwordText = tkinter.Entry(frame, width = 20, show = "*")
    passwordText.place(x = 300, y = 180)
    tkinter.Label(frame, text = "Retype Password", bg = "#dcdcdc", font = font1).place(x = 190, y = 210)
    retypePasswordText = tkinter.Entry(frame, width = 20, show = "*")
    retypePasswordText.place(x = 300, y = 210)
    show = tkinter.PhotoImage(file = "Icons/show.png")
    hide = tkinter.PhotoImage(file = "Icons/hide.png")
    seeText = tkinter.StringVar(value = "1")
    see = tkinter.Button(frame, image = show, height = 20, width = 20, bg = "#dcdcdc", borderwidth = 0, textvariable = seeText, command = my_show)
    see.place(x = 430, y = 180)
    tkinter.Button(frame, text = "Submit", bg = "#dcdcdc", font = font1, padx = 8, pady = 3, cursor = "hand2", command = check).place(x = 290, y = 260)

def signup():
    # Signup Page
    for widgets in frame.winfo_children():
        widgets.destroy()
    global bg
    global personIcon
    global backIcon
    global userNameText
    global show
    global hide
    global passwordText
    global retypePasswordText
    global accountTypeText
    photo = tkinter.PhotoImage(file = "Icons/login.png")
    root.iconphoto(False, photo)
    def check():
        if userNameText.get() == "":
            tkinter.Label(frame, text = "     Please Enter User Name          ", bg = "#dcdcdc", fg = "red", font = font1).place(x = 225, y = 325)
        elif passwordText.get() == "":
            tkinter.Label(frame, text = "      Please Enter Password          ", bg = "#dcdcdc", fg = "red", font = font1).place(x = 225, y = 325)
        elif len(passwordText.get()) < 8:
            tkinter.Label(frame, text = "Please Enter A Stronger Password", bg = "#dcdcdc", fg = "red", font = font1).place(x = 225, y = 325)
        elif accountTypeText.get() == "":
            tkinter.Label(frame, text = "     Please Enter Account Type       ", bg = "#dcdcdc", fg = "red", font = font1).place(x = 225, y = 325)
        elif len(accountTypeText.get()) > 1:
            tkinter.Label(frame, text = "Account Type Should Be Of Len 1", bg = "#dcdcdc", fg = "red", font = font1).place(x = 225, y = 325)
        elif passwordText.get() != retypePasswordText.get():
            tkinter.Label(frame, text = "        Password Not Same            ", bg = "#dcdcdc", fg = "red", font = font1).place(x = 225, y = 325)
        else:
            cursor.execute("insert into user values('" + userNameText.get() + "','" + passwordText.get() + "','" + accountTypeText.get() + "', '')")
            connect.commit()
            login()
    def my_show():
        if (seeText.get() == "1"):
            passwordText.config(show="")
            retypePasswordText.config(show="")
            see.configure(image=hide)
            seeText.set("0")
        else:
            passwordText.config(show="*")
            retypePasswordText.config(show="*")
            see.configure(image=show)
            seeText.set("1")
    bg = ImageTk.PhotoImage(Image.open("Icons/bg.jpg"))
    tkinter.Label(frame, image = bg, height = 640, width = 480, borderwidth = 1).pack(expand = True, fill = "both")
    backIcon = tkinter.PhotoImage(file = "Icons/back.png")
    tkinter.Button(frame, image = backIcon, height = 40, width = 40, bg = "#dcdcdc", cursor = "hand2", command = login).place(x = 10, y = 10)
    tkinter.Frame(frame, height = 300, width = 290, bg = "#dcdcdc", borderwidth = "2", highlightbackground = "black",  relief = "raised").place(x = 180, y = 70)
    personIcon = tkinter.PhotoImage(file = "Icons/person.png", height = 40, width = 40)
    tkinter.Label(frame, image = personIcon, bg = "#dcdcdc").place(x = 220, y = 90)
    tkinter.Label(frame, text = "Sign Up Page", bg = "#dcdcdc", font = font).place(x = 270, y = 100)
    tkinter.Label(frame, text = "User Name", bg = "#dcdcdc", font = font1).place(x = 220, y = 150)
    userNameText = tkinter.Entry(frame, width = 20)
    userNameText.place(x = 300, y = 150)
    tkinter.Label(frame, text = "Password", bg = "#dcdcdc", font = font1).place(x = 220, y = 180)
    show = tkinter.PhotoImage(file = "Icons/show.png")
    hide = tkinter.PhotoImage(file = "Icons/hide.png")
    passwordText = tkinter.Entry(frame, width = 20, show = "*")
    passwordText.place(x = 300, y = 180)
    tkinter.Label(frame, text = "Retype Password", bg = "#dcdcdc", font = font1).place(x = 190, y = 210)
    retypePasswordText = tkinter.Entry(frame, width = 20, show = "*")
    retypePasswordText.place(x = 300, y = 210)
    seeText = tkinter.StringVar(value = "1")
    see = tkinter.Button(frame, image = show, height = 20, width = 20, bg = "#dcdcdc", borderwidth = 0, textvariable = seeText, command = my_show)
    see.place(x = 430, y = 180)
    tkinter.Label(frame, text = "Account Type", bg = "#dcdcdc", font = font1).place(x = 210, y = 240)
    accountTypeText = tkinter.Entry(frame, width = 20)
    accountTypeText.place(x = 300, y = 240)
    tkinter.Button(frame, text = "Submit", bg = "#dcdcdc", font = font1, padx = 8, pady = 3, cursor = "hand2", command = check).place(x = 290, y = 280)

def adminHome():
    # Admin Home Page
    for widgets in frame.winfo_children():
        widgets.destroy()
    global backIcon
    global userNameText
    photo = tkinter.PhotoImage(file = "Icons/home.png")
    root.iconphoto(False, photo)
    def remove():
        cursor.execute("delete from user where id like '" + userNameText.get() + "'")
        connect.commit()
        adminHome()
    frame.configure(bg="#f5ffeb")
    backIcon = tkinter.PhotoImage(file = "Icons/back.png")
    tkinter.Button(frame, image = backIcon, height = 40, width = 40, bg = "#f5ffeb", borderwidth = 0, cursor = "hand2", command = login).place(x = 10, y = 10)
    cursor.execute("select * from user")
    a = cursor.fetchall()
    x = "Account\t\tPassword\n"
    for i in a:
        if i[2].lower() != "a":
            x += i[0] + "\t\t" + i[1] + "\n"
    tkinter.Label(frame, text = "Admin Home", bg = "#f5ffeb", font = font).place(x = 270, y = 10)
    tkinter.Label(frame, text = x, bg = "#f5ffeb", font = font1).place(x = 140, y = 50)
    tkinter.Label(frame, text = "User Name", bg = "#f5ffeb", font = font1).place(x = 150, y = 200)
    userNameText = tkinter.Entry(frame, width = 20)
    userNameText.place(x = 230, y = 200)
    tkinter.Button(frame, text = "Delete", bg = "#f5ffeb", font = font1, padx = 8, pady = 3, cursor = "hand2", command = remove).place(x = 150, y = 230)

def home():
    # Home Page
    for widgets in frame.winfo_children():
        widgets.destroy()
    global menuIcon
    global walletIcon
    global shoppingIcon
    global searchIcon
    global personIcon
    photo = tkinter.PhotoImage(file = "Icons/home.png")
    root.iconphoto(False, photo)
    def menu():
        # Menu Bar
        home()
        global backIcon
        menuFrame = tkinter.Frame(frame, height = 640, width = 200, bg = "#e6e6e6", borderwidth = "2", highlightbackground = "black", relief = "raised")
        menuFrame.place(x = 0, y = 0)
        backIcon = tkinter.PhotoImage(file = "Icons/smallBack.png")
        tkinter.Button(menuFrame, image = backIcon, height = 24, width = 24, bg = "#e6e6e6", borderwidth = 0, cursor = "hand2", command = home).place(x = 10, y = 10)
        tkinter.Label(menuFrame, text = "Menu", bg = "#e6e6e6", font = font).place(x = 70, y = 10)
        tkinter.Button(menuFrame, text = "Recents", bg = "#e6e6e6", font = font1, borderwidth = 0, cursor = "hand2", command = recents).place(x = 50, y = 50)
    def search():
        # Search Bar
        home()
        global backIcon
        global companyValue
        global dataValue
        global timeValue
        def check():
            if companyText.get() == "":
                tkinter.Label(searchFrame, text = "Please Enter The Company's Name", bg = "#e6e6e6", fg = "red", font = font1).place(x = 18, y = 160)
            else:
                stockSeen[companyValue.get().upper()] = [dataValue.get(), timeValue.get()]
                stock()
        searchFrame = tkinter.Frame(frame, height = 200, width = 250, bg = "#e6e6e6", borderwidth = "2", highlightbackground = "black",  relief = "raised")
        searchFrame.place(x = 295, y = 65)
        backIcon = tkinter.PhotoImage(file = "Icons/smallBack.png")
        tkinter.Button(searchFrame, image = backIcon, height = 24, width = 24, bg = "#e6e6e6", borderwidth = 0, cursor = "hand2", command = home).place(x = 10, y = 10)
        tkinter.Label(searchFrame, text = "Search", bg = "#e6e6e6", font = font).place(x = 90, y = 10)
        tkinter.Label(searchFrame, text = "Company", bg = "#e6e6e6", font = font1).place(x = 10, y = 50)
        companyValue = tkinter.StringVar()
        companyText = tkinter.Entry(searchFrame, width = 20, textvariable = companyValue)
        companyText.place(x = 90, y = 50)
        tkinter.Label(searchFrame, text = "Data", bg = "#e6e6e6", font = font1).place(x = 10, y = 85)
        options = ["Open", "High", "Low", "Close", "Volume", "OHLC"]
        dataValue = tkinter.StringVar()
        dataValue.set("Open")
        dataDrop = tkinter.OptionMenu(searchFrame, dataValue, *options)
        dataDrop.place(x = 90, y = 80)
        tkinter.Label(searchFrame, text = "Time", bg = "#e6e6e6", font = font1).place(x = 10, y = 120)
        timeOptions = ["7d", "1mo", "6mo", "12mo", "24mo", "36mo", "max"]
        timeValue = tkinter.StringVar()
        timeValue.set("max")
        timeDrop = tkinter.OptionMenu(searchFrame, timeValue, *timeOptions)
        timeDrop.place(x = 90, y = 120)
        tkinter.Button(searchFrame, text = "Submit", bg = "#e6e6e6", font = font1, padx = 5, pady = 1, borderwidth = 0, cursor = "hand2", command = check).place(x = 170, y = 120)
    def shopping():
        # Shopping Bar
        home()
        global backIcon
        global companyValue
        global noOfStocksValue
        def add():
            if companyText.get() == "":
                tkinter.Label(shoppingFrame, text = "Please Enter The Company's Name", bg = "#e6e6e6", fg = "red", font = font1).place(x = 18, y = 150)
            else:
                companyNameText = companyValue.get().upper()
                yfinance.download(companyNameText).to_csv("data.csv", mode = "w")
                cursor.execute("Select stockList from user where id like '" + userNameValue.get() + "'")
                x = cursor.fetchall()
                if x == [(None,)]:
                    stockList = str()
                else:
                    for i in x:
                        stockList = i[0]
                stockList += companyValue.get().upper() + "\t" + noOfStocksValue.get() + "\n"
                cursor.execute("update user set stockList = '" + stockList + "' where id like'" + userNameValue.get() + "'")
                connect.commit()
                home()
        shoppingFrame = tkinter.Frame(frame, height = 190, width = 250, bg = "#e6e6e6", borderwidth = "2", highlightbackground = "black",  relief = "raised")
        shoppingFrame.place(x = 345, y = 65)
        backIcon = tkinter.PhotoImage(file = "Icons/smallBack.png")
        tkinter.Button(shoppingFrame, image = backIcon, background = "#e6e6e6", height = 24, width = 24, borderwidth = 0, cursor = "hand2", command = home).place(x = 10, y = 10)
        tkinter.Label(shoppingFrame, text = "Purchase", bg = "#e6e6e6", font = font).place(x = 90, y = 10)
        tkinter.Label(shoppingFrame, text = "Company", bg = "#e6e6e6", font = font1).place(x = 10, y = 50)
        companyValue = tkinter.StringVar()
        companyText = tkinter.Entry(shoppingFrame, width = 20, textvariable = companyValue)
        companyText.place(x = 105, y = 50)
        tkinter.Label(shoppingFrame, text = "No Of Stocks", bg = "#e6e6e6", font = font1).place(x = 10, y = 80)
        noOfStocksValue = tkinter.StringVar()
        noOfStocksText = tkinter.Entry(shoppingFrame, width = 20, textvariable = noOfStocksValue)
        noOfStocksText.place(x = 105, y = 80)
        tkinter.Button(shoppingFrame, text = "Purchase", bg = "#e6e6e6", font = font1, padx = 6, pady = 1, cursor = "hand2", command = add).place(x = 120, y = 115)
    frame.configure(bg = "#f5ffeb")
    menuIcon = tkinter.PhotoImage(file = "Icons/menu.png")
    tkinter.Button(frame, image = menuIcon, height = 40, width = 40, bg = "#f5ffeb", borderwidth = 0, cursor = "hand2", command = menu).place(x = 10, y = 10)
    tkinter.Label(frame, text = "Home", bg = "#f5ffeb", font = font).place(x = 270, y = 10)
    walletIcon = tkinter.PhotoImage(file = "Icons/wallet.png")
    tkinter.Button(frame, image = walletIcon, height = 40, width = 40, bg = "#f5ffeb", borderwidth = 0, cursor = "hand2", command = wallet).place(x = 590, y = 10)
    shoppingIcon = tkinter.PhotoImage(file = "Icons/shopping.png")
    tkinter.Button(frame, image = shoppingIcon, height = 40, width = 40, bg = "#f5ffeb", borderwidth = 0, cursor = "hand2", command = shopping).place(x = 540, y = 10)
    searchIcon = tkinter.PhotoImage(file = "Icons/search.png")
    tkinter.Button(frame, image = searchIcon, height = 40, width = 40, bg = "#f5ffeb", borderwidth = 0, cursor = "hand2", command = search).place(x = 490, y = 10)
    personIcon = tkinter.PhotoImage(file = "Icons/bigPerson.png")
    tkinter.Label(frame, image = personIcon, height = 48, width = 48, bg = "#f5ffeb").place(x = 200, y = 70)
    tkinter.Label(frame, text = "Welcome " + userNameValue.get(), bg = "#f5ffeb", font = Font(size = 20, family = "Comic Sans MS")).place(x = 250, y = 80)

def wallet():
    # Wallet Page
    for widgets in frame.winfo_children():
        widgets.destroy()
    global backIcon
    global companyText
    photo = tkinter.PhotoImage(file = "Icons/accountWallet.png")
    root.iconphoto(False, photo)
    def remove():
        cursor.execute("Select stockList from user where id like '" + userNameValue.get() + "'")
        a = cursor.fetchall()[0][0]
        x = str()
        if a != "":
            if companyText.get() == "":
                tkinter.Label(frame, text = "Enter Company Name", bg = "#f5ffeb", fg = "red", font = font1).place(x = 170, y = 370)
            elif companyText.get().upper() not in a:
                tkinter.Label(frame, text = "Not In Wallet          ", bg = "#f5ffeb", fg = "red", font = font1).place(x = 170, y = 370)
            else:
                b = a.split("\n")
                b.pop()
                for i in b:
                    j = i.split("\t")
                    if j[0] != companyText.get():
                        x += j[0] + "/t" + j[1] + "/n"
                cursor.execute("update user set stockList = '" + x + "' where id like'" + userNameValue.get() + "'")
                connect.commit()
                wallet()
        else:
            tkinter.Label(frame, text = "Wallet Is Empty            ", bg = "#f5ffeb", fg = "red", font = font1).place(x = 170, y = 370)
    frame.configure(bg="#f5ffeb")
    tkinter.Label(frame, text = "Wallet", bg = "#f5ffeb", font = font).place(x = 270, y = 10)
    backIcon = tkinter.PhotoImage(file = "Icons/back.png")
    tkinter.Button(frame, image = backIcon, height = 40, width = 40, bg = "#f5ffeb", borderwidth = 0, cursor = "hand2", command = home).place(x = 10, y = 10)
    cursor.execute("Select stockList from user where id like '" + userNameValue.get() + "'")
    x = "Company\tNo. Of Stocks\tAmount\tRecommendation\n\n"
    a = cursor.fetchall()[0][0]
    if a != None:
        b = a.split("\n")
        b.pop()
        for i in b:
            j = i.split("\t")
            z = yfinance.Ticker(j[0]).info
            k = int(z["currentPrice"] * float(j[1]))
            l = z["recommendationKey"]
            x += i + "\t" + str(k) + "\t" + l + "\n"
    tkinter.Label(frame, text = x, bg = "#f5ffeb", font = Font(family = "ComicSans MS", size = 12)).place(x = 150, y = 50)
    tkinter.Label(frame, text = "Sell", bg = "#f5ffeb", font = font1).place(x = 150, y = 300)
    companyText = tkinter.Entry(frame, width = 20)
    companyText.place(x = 200, y = 300)
    tkinter.Button(frame, text = "Submit", bg = "#f5ffeb", font = font1, padx = 5, pady = 1, cursor = "hand2", command = remove).place(x = 170, y = 330)

def recents():
    # Reacents Page
    for widgets in frame.winfo_children():
        widgets.destroy()
    global backIcon
    photo = tkinter.PhotoImage(file="Icons/home.png")
    root.iconphoto(False, photo)
    frame.configure(bg = "#f5ffeb")
    tkinter.Label(frame, text = "Recents", bg = "#f5ffeb", font = font).place(x = 270, y = 10)
    backIcon = tkinter.PhotoImage(file = "Icons/back.png")
    tkinter.Button(frame, image = backIcon, height = 40, width = 40, bg = "#f5ffeb", borderwidth = 0, cursor = "hand2", command = home).place(x = 10, y = 10)
    c = "Company\tData\tTime\n"
    x = stockSeen
    for i in x:
        c += i + "\t" + x[i][0] + "\t" + x[i][1] + "\n"
    tkinter.Label(frame, text = c, bg = "#f5ffeb", font = Font(family = "ComicSans MS", size = 12)).place(x = 200, y = 50) 

def stock():
    # Stock Page
    for widgets in frame.winfo_children():
        widgets.destroy()
    global backIcon
    photo = tkinter.PhotoImage(file = "Icons/graph.png")
    root.iconphoto(False, photo)
    frame.configure(bg = "#f5ffeb")
    backIcon = tkinter.PhotoImage(file = "Icons/back.png")
    tkinter.Button(frame, image = backIcon, height = 40, width = 40, bg = "#f5ffeb", borderwidth = 0, cursor = "hand2", command = home).place(x = 10, y = 10)
    company = companyValue.get().upper(); data = dataValue.get(); time = timeValue.get()
    tkinter.Label(frame, text = company + " - " + data, bg = "#f5ffeb", font = font).place(x = 270, y = 10)
    stock = yfinance.Ticker(company)
    info = stock.info
    tkinter.Label(frame, text = "Industry: " + info["industry"] + "; Sector: " + info["sector"] + "; \nCountry: " + info["city"] + "\tRecommendation: " + info["recommendationKey"], bg = "#f5ffeb", font = font1).place(x = 70, y = 40)
    if company == companyNameText:
        df = pd.read_csv("data.csv")
    else:
        df = stock.history(period = time)
    if data == "OHLC":
        plot = mpf.figure(figsize = (6, 4), dpi = 100)
        subPlot = plot.add_subplot(111, xlabel = "Time", ylabel = "Value")
        for tick in subPlot.get_xticklabels():
            tick.set_rotation(20)
        for tick in subPlot.get_yticklabels():
            tick.set_rotation(20)
        bar = FigureCanvasTkAgg(plot, frame)
        bar.get_tk_widget().pack(side = tkinter.BOTTOM)
        mpf.plot(df, type = "candle", ax = subPlot, warn_too_much_data = len(df) + 1)
    else:
        plot = plt.Figure(figsize = (6, 4), dpi = 100)
        subPlot = plot.add_subplot(111, xlabel = "Time", ylabel = "Value")
        for tick in subPlot.get_xticklabels():
            tick.set_rotation(20)
        for tick in subPlot.get_yticklabels():
            tick.set_rotation(20)
        bar = FigureCanvasTkAgg(plot, frame)
        bar.get_tk_widget().pack(side = tkinter.BOTTOM)
        subPlot.plot(df[data])
    plot.set_facecolor("#f5ffeb")
    subPlot.set_facecolor("#f5ffeb")


# Each Page Is A Seperate Function And The Program Starts With The Login Page

login()

root.mainloop()
