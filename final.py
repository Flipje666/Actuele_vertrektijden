__author__ = 'Philip'
import requests
import xmltodict

def getVertrektijden(station = 'ut'):
    auth_details = ('philip.vanexel@student.hu.nl', 'u6H5dlZpHsjHbIBac4aMHJNPfLtliEZ7cQJJDYjd-ijeBWF4-Zawbw')
    response = requests.get('http://webservices.ns.nl/ns-api-avt?station='+station, auth=auth_details)

    final = xmltodict.parse(response.text)

    printvar = {}
    int = 0
    for i in final['ActueleVertrekTijden']['VertrekkendeTrein']:
        vertrekkende_trein = dict(i)
        printvar[int] = vertrekkende_trein
        int +=1
    return printvar

def getStations():
    auth_details = ('philip.vanexel@student.hu.nl', 'u6H5dlZpHsjHbIBac4aMHJNPfLtliEZ7cQJJDYjd-ijeBWF4-Zawbw')
    response = requests.get('http://webservices.ns.nl/ns-api-stations-v2', auth=auth_details)

    final = xmltodict.parse(response.text)
    printvar = {}
    int = 0
    for i in final['Stations']['Station']:
        station = dict(i)
        printvar[int] = station
        int +=1
    return printvar

def changeTime(time):
    import DateTime
    dt = DateTime.DateTime(time)
    return str(dt.TimeMinutes())

def getStationscode(stations, inputvar):
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
                if isinstance(st['Synoniemen']['Synoniem'],list):
                    for synoniem in st['Synoniemen']['Synoniem']:
                        if inputvar == synoniem:
                            return st['Code']
                else:
                    if inputvar == st['Synoniemen']['Synoniem']:
                        return st['Code']

def GeefVertrekTijden(input):
    returnvar = ('{0:15s} {1:25s} {2:50s} {3:6s} {4:15s} {5:50s}'.format("Tijd","Eindstation","Route","Sp.","Treinsoort","Opmerking"))
    for trein in input:
        x = input[trein]
        VertrekTijd = changeTime(x['VertrekTijd'])
        if 'VertrekVertragingTekst' in x:
            VertrekVertragingTekst = " "+x['VertrekVertragingTekst']
        else:
            VertrekVertragingTekst = ""
        EindBestemming = x['EindBestemming']
        TreinSoort = x['TreinSoort']
        if 'RouteTekst' in x:
            RouteTekst = x['RouteTekst']
        else:
            RouteTekst = ""
        VertrekSpoor = x['VertrekSpoor']['#text']
        if x['VertrekSpoor']['@wijziging'] == 'true':
            spoorwijziging = " !"
        else:
            spoorwijziging = ""
        if 'Opmerkingen' in x:
            Opmerking = x['Opmerkingen']['Opmerking']
        else:
            Opmerking = ""
        if 'ReisTip' in x:
            ReisTip = x['ReisTip']
        else:
            ReisTip = ""
        Opmerking = Opmerking + ReisTip
        returnvar += '{0:15s} {1:25s} {2:50s} {3:6s} {4:15s} {5:50s}'.format(str(VertrekTijd)+str(VertrekVertragingTekst), str(EindBestemming), str(RouteTekst), str(VertrekSpoor)+str(spoorwijziging), str(TreinSoort), str(Opmerking))+'\n'
    return returnvar

def vraagStation():
    lijstje = []
    for station in stations:
        st = stations[station]
        if st['Namen']['Kort']:
            lijstje += [st['Namen']['Kort']]
        if st['Namen']['Middel']:
            lijstje += [st['Namen']['Middel']]
        if st['Namen']['Lang']:
            lijstje += [st['Namen']['Lang']]
        if st['Synoniemen']:
            if st['Synoniemen']['Synoniem']:
                if isinstance(st['Synoniemen']['Synoniem'],list):
                    lijstje += (st['Synoniemen']['Synoniem'])
                else:
                    lijstje += [st['Synoniemen']['Synoniem']]

    inputvar = ""
    while inputvar not in lijstje:
        inputvar = str(input("Voer uw station in: "))

    return inputvar

stations = getStations()
print("Vertrektijden vanuit station Utrecht:",)
print(GeefVertrekTijden(getVertrektijden()))

inputvar = vraagStation()
stationscode = getStationscode(stations, inputvar)
print("Vertrektijden vanuit station",inputvar,":")
print(GeefVertrekTijden(getVertrektijden(stationscode)))