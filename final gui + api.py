import requests
import xmltodict
import DateTime
from tkinter.tix import *

screen_width = 950
screen_height = 700


def get_vertrektijden(station='ut'):
    """
        Input: stationscode
        Aanroepen database,
        Output: dict met vertrektijden vanuit de stations
    """
    auth_details = ('philip.vanexel@student.hu.nl', 'u6H5dlZpHsjHbIBac4aMHJNPfLtliEZ7cQJJDYjd-ijeBWF4-Zawbw')
    response = requests.get('http://webservices.ns.nl/ns-api-avt?station='+station, auth=auth_details)
    final = xmltodict.parse(response.text)
    printvar = {}
    x = 0
    for i in final['ActueleVertrekTijden']['VertrekkendeTrein']:
        vertrekkende_trein = dict(i)
        printvar[x] = vertrekkende_trein
        x += 1
    return printvar


def get_stations():
    """
        Aanroepen database
        output: dict met alle gegevens van stations
    """
    auth_details = ('philip.vanexel@student.hu.nl', 'u6H5dlZpHsjHbIBac4aMHJNPfLtliEZ7cQJJDYjd-ijeBWF4-Zawbw')
    response = requests.get('http://webservices.ns.nl/ns-api-stations-v2', auth=auth_details)

    final = xmltodict.parse(response.text)
    printvar = {}
    x = 0
    for i in final['Stations']['Station']:
        station = dict(i)
        printvar[x] = station
        x += 1
    return printvar


def change_time(time):
    """
        Input: Datum en Tijd
        Veranderen van de tijd naar het goede formaat.
        Output: Tijd in HH:MM
    """
    dt = DateTime.DateTime(time)
    return str(dt.TimeMinutes())


def get_stations_code(inputvar):
    """
        Input: Stationsnaam in string
        Output: Stationscode die gebruikt kan worden in de API.
    """
    stations = get_stations()
    for station in stations:
        st = stations[station]
        if inputvar == st['Namen']['Kort']:
            return st['Code']
        if inputvar == st['Namen']['Middel']:
            return st['Code']
        if inputvar == st['Namen']['Lang']:
            return st['Code']
        if st['Synoniemen']:
            if st['Synoniemen']['Synoniem']:
                if isinstance(st['Synoniemen']['Synoniem'], list):
                    for synoniem in st['Synoniemen']['Synoniem']:
                        if inputvar == synoniem:
                            return st['Code']
                else:
                    if inputvar == st['Synoniemen']['Synoniem']:
                        return st['Code']


def geef_vertrektijden(inputvar):
    """
        Input: output van de functie get_vertrektijden()
        Output: Een geformatteerde lijst zoals weergegeven in de schermen.
    """
    returnvar = '{0:14s} {1:25s} {2:45s} {3:6s} {4:10s}'.format("Tijd", "Eindstation", "Route", "Sp.", "Treinsoort")
    for trein in inputvar:
        x = inputvar[trein]
        if 'VertrekTijd' in x:
            vertrek_tijd = change_time(x['VertrekTijd'])
        else:
            vertrek_tijd = ""
        if 'VertrekVertragingTekst' in x:
            vertrek_vertraging_tekst = " "+x['VertrekVertragingTekst']
        else:
            vertrek_vertraging_tekst = ""
        if 'EindBestemming' in x:
            eind_bestemming = x['EindBestemming']
        else:
            eind_bestemming = ""
        if "TreinSoort" in x:
            trein_soort = x['TreinSoort']
        else:
            trein_soort = ""
        if 'RouteTekst' in x:
            route_tekst = x['RouteTekst']
        else:
            route_tekst = ""
        if 'VertrekSpoor' in x:
            vertrek_spoor = x['VertrekSpoor']['#text']
        else:
            vertrek_spoor = ""
        if x['VertrekSpoor']['@wijziging'] == 'true':
            spoor_wijziging = " !"
        else:
            spoor_wijziging = ""
        returnvar += '\n'+'{0:14s} {1:25s} {2:45s} {3:6s} {4:10s}'.format(str(vertrek_tijd)+str(vertrek_vertraging_tekst), str(eind_bestemming), str(route_tekst), str(vertrek_spoor)+str(spoor_wijziging), str(trein_soort))
    return returnvar


def schermindeling(scherm):
    """
        Input: Variabele scherm
        Hierin wordt de basis van elk scherm aangemaakt.
    """
    blauwe_balk = Canvas(scherm, bg="#003366", width=screen_width, height=50, highlightthickness=0)
    blauwe_balk.pack(side=BOTTOM)
    scherm.maxsize(screen_width, screen_height)
    scherm.minsize(screen_width, screen_height)
    scherm.wm_state("zoomed")
    scherm.configure(background='#ffcc33')
    scherm.title("NS Vertrektijden")


def scherm_1():
    """
        Welkomstscherm
    """
    s1 = Tk()
    schermindeling(s1)

    text1 = Label(s1, text="Welkom bij NS", bg="#ffcc33", fg="#003366", font=("Frutiger", 36))
    text1.pack()
    text1.place(anchor=CENTER, x=screen_width/2, y=100)

    ns_foto = PhotoImage(file="NS.png")
    ns_foto_label = Label(s1, image=ns_foto, bg="#ffcc33")
    ns_foto_label.pack()
    ns_foto_label.place(anchor=CENTER, x=screen_width/2, y=270)

    visa_master_foto = PhotoImage(file="visaMaster.png")
    visa_master_foto_label = Label(s1, image=visa_master_foto, bg="#003366")
    visa_master_foto_label.pack()
    visa_master_foto_label.place(anchor=CENTER, x=screen_width/2, y=675)

    begin_button = Button(s1, text="Actuele vertrektijden", width=20, height=2, bg="#003366", fg="white", font=("Frutiger", 10), activebackground="#003366", activeforeground="white", command=lambda: scherm_2())
    begin_button.pack()
    begin_button.place(anchor=CENTER, x=screen_width/2-100, y=520)

    afsluit_button = Button(s1, width=20, height=2, text="Afsluiten", fg="white", bg="#003366",  font=("Frutiger", 10), activebackground="#003366", activeforeground="white", command=lambda: s1.destroy())
    afsluit_button.pack()
    afsluit_button.place(anchor=CENTER, x=screen_width/2+100, y=520)

    s1.mainloop()


def scherm_2():
    """
        Scherm met de output van de vertrektijden van het standaardstation (Utrecht Centraal).
    """
    s2 = Toplevel()
    schermindeling(s2)

    text1 = Label(s2, text="Utrecht Centraal", bg="#ffcc33", fg="#003366", font=("Frutiger", 25))
    text1.pack(side=TOP)

    button_terug = Button(s2, width=12, height=3, text="Terug", fg="white", bg="#003366",  font=("Frutiger", 10), activebackground="#003366", activeforeground="white", command=lambda: s2.destroy())
    button_terug.pack()
    button_terug.place(x=10, y=10)

    button_ander_station = Button(s2, width=12, height=3, text="Ander station", fg="white", bg="#003366", font=("Frutiger", 10), activebackground="#003366", activeforeground="white", command=lambda: scherm_3())
    button_ander_station.pack()
    button_ander_station.place(x=10, y=75)

    scroll_win = ScrolledWindow(s2, width=800, height=600)
    scroll_win.config_all("background", "#ffcc33")
    scroll_win.config_all("borderwidth", "0")
    scroll_win.pack(side=RIGHT)
    win = scroll_win.window

    label_widget = Label(win, text=geef_vertrektijden(get_vertrektijden()), justify=LEFT, font=("Courier New", 8), bg="#ffcc33")
    label_widget.pack()

    scroll_win.mainloop()
    s2.mainloop()


def scherm_3():
    """
        Scherm met de output van de vertrektijden van het inputstation.
    """
    s3 = Toplevel()
    schermindeling(s3)

    def vraag_station():
        """
            Output: formuliergegevens voor de aanvraag van welk station de vertrektijden opgevraagd worden
        """
        def ok_button():
            """
                Wat er gebeurt als je op de OK button klikt.
            """
            inputfieldLabel.destroy()
            inputfield.destroy()
            inputButton.destroy()
            inputvar = inputtext.get()
            return controleer_station(inputvar)

        inputtext = StringVar()
        inputfieldLabel = Label(s3, text="Voer een station in", bg="#ffcc33", fg="#003366", font=("Frutiger", 25))
        inputfieldLabel.pack(side=TOP)

        inputfield = Entry(s3, bd=1, textvariable=inputtext, bg="#ffcc33", fg="#003366", highlightthickness=0)
        inputfield.pack()
        inputfield.place(anchor=CENTER, x=screen_width/2, y=55)

        inputButton = Button(s3, text='OK', command=ok_button, bg="#ffcc33", fg="#003366", activebackground="#ffcc33", font=("Frutiger", 7))
        inputButton.pack()
        inputButton.place(anchor=CENTER, x=screen_width/2+73, y=55)

    def output(inputvar):
        """
            input: Gecontroleerde stationsnaam
            Output: Weergave van de vertrektijden van het station wat ingevoerd is.
        """
        text2 = Label(s3, text=inputvar, bg="#ffcc33", fg="#003366", font=("Frutiger", 25))
        text2.pack(side=TOP)

        scroll_win = ScrolledWindow(s3, width=800, height=600, bg="#ffcc33")
        scroll_win.config_all("background", "#ffcc33")
        scroll_win.config_all("borderwidth", "0")
        scroll_win.pack(side=RIGHT)
        win = scroll_win.window

        label_widget = Label(win, text=geef_vertrektijden(get_vertrektijden(get_stations_code(inputvar))), justify=LEFT, font=("Courier New", 8), bg="#ffcc33")
        label_widget.pack()

        scroll_win.mainloop()

    def controleer_station(inputvar):
        """
            Input: Input die de user geeft.
            Controleren of het ingevoerde overeenkomt met een station in de API van de NS. Als dit niet zo is dan wordt opnieuw voor een station gevraagd.
            Output:
            - Opnieuw aanvragen station
            - Doorgaan naar output() functie.
        """
        stations = get_stations()
        namen_lijstje = []
        for station in stations:
            st = stations[station]
            if st['Namen']['Kort']:
                namen_lijstje += [st['Namen']['Kort']]
            if st['Namen']['Middel']:
                namen_lijstje += [st['Namen']['Middel']]
            if st['Namen']['Lang']:
                namen_lijstje += [st['Namen']['Lang']]
            if st['Synoniemen']:
                if st['Synoniemen']['Synoniem']:
                    if isinstance(st['Synoniemen']['Synoniem'], list):
                        namen_lijstje += (st['Synoniemen']['Synoniem'])
                    else:
                        namen_lijstje += [st['Synoniemen']['Synoniem']]

        if inputvar not in namen_lijstje:
            return vraag_station()
        else:
            return output(inputvar)

    vraag_station()

    button_terug = Button(s3, width=12, height=3, text="Terug", fg="white", bg="#003366",  font=("Frutiger", 10), activebackground="#003366", activeforeground="white", command=lambda: s3.destroy())
    button_terug.pack()
    button_terug.place(x=10, y=10)

    s3.mainloop()

scherm_1()