from tkinter import *

def scherm_1():
    s1 = Tk()
    s1.maxsize(600,400)
    s1.minsize(600,400)
    s1.configure(background='#ffcc33')

    blauweBalk = Canvas(s1, bg="#003366", width=600, height=30, highlightthickness=0)
    blauweBalk.pack(side=BOTTOM)

    text1 = Label(s1, text="Welkom bij NS", bg="#ffcc33", fg="#003366", font=("Frutiger", 30))
    text1.pack()
    text1.place(anchor=CENTER, x=300, y=50)

    NSFoto = PhotoImage(file="NS.png")
    fotoLabel = Label(s1, image=NSFoto, bg="#ffcc33")
    fotoLabel.pack()
    fotoLabel.place(anchor=CENTER, x=300, y=170)

    visaMaster = PhotoImage(file="visaMaster.png")
    visaMasterLabel = Label(s1, image=visaMaster, bg="#003366")
    visaMasterLabel.pack()
    visaMasterLabel.place(anchor=CENTER, x=300, y=385)

    s1.title("NS Vertrektijden")

    beginButton = Button(s1, text="Actuele vertrektijden", width=20, height=2, bg="#003366", fg="white", activebackground="#003366", activeforeground="white",
                     command=lambda : scherm_2())
    beginButton.pack()
    beginButton.place(anchor=CENTER, x=300,y=300)
    s1.mainloop()

def scherm_2():

    s2 = Toplevel()
    s2.maxsize(600,400);
    s2.minsize(600,400);
    s2.configure(background="#ffcc33")

    canvas = Canvas(s2, bg="#003366", width=600, height=30, highlightthickness=0)
    canvas.pack(side=BOTTOM)

    text1 = Label(s2, text="Utrecht Centraal", bg="#ffcc33", fg="#003366", font=("Frutiger", 15))
    text1.pack(side=TOP)

    button_terug = Button(s2, width=10, height=5,text="Terug", fg="white", bg="#003366",  font=("Frutiger", 10), activebackground="#003366", activeforeground="white",
                          command = lambda : s2.destroy())
    button_terug.pack()
    button_terug.place(x=0,y=0)

    button_ander_station = Button(s2, width=10, height=5,text="Ander station", fg="white", bg="#003366", font=("Frutiger", 10), activebackground="#003366", activeforeground="white",
                           command = lambda : scherm_3())
    button_ander_station.pack()
    button_ander_station.place(x=0,y=80)

    s2.title("NS Vertrektijden")
    s2.mainloop()

def scherm_3():
    s3 = Toplevel()
    s3.maxsize(600,400);
    s3.minsize(600,400);
    s3.configure(background="#ffcc33")

    def output():
        mtext = ment.get()
        text2 = Label(s3, text=mtext, bg="#ffcc33", fg="#003366", font=("Frutiger",10))
        text2.pack(side=TOP)
        return

    def ok_button():
        inputfieldLabel.destroy()
        output()
        inputfield.destroy()
        inputButton.destroy()

    ment = StringVar()
    inputfieldLabel = Label(s3,text="Voer een station in", bg="#ffcc33", fg="#003366", font=("Frutiger",15))
    inputfieldLabel.pack(side=TOP)

    inputfield = Entry(s3, bd=1,textvariable=ment, bg="#ffcc33", fg="#003366", highlightthickness=0)
    inputfield.pack()
    inputfield.place(anchor=CENTER,x=300,y=39)

    inputButton = Button(s3, text = 'OK', command = ok_button, bg="#ffcc33", fg="#003366", activebackground="#ffcc33",font=("Frutiger",7) )
    inputButton.pack()
    inputButton.place(anchor=CENTER,x=373,y=39)


    button_terug = Button(s3, width=10, height=5,text="Terug", fg="white", bg="#003366",  font=("Frutiger", 10), activebackground="#003366", activeforeground="white",
                    command = lambda : s3.destroy())
    button_terug.pack()
    button_terug.place(x=0,y=0)

    s3.title("NS Vertrektijden")
    s3.mainloop()

scherm_1()
