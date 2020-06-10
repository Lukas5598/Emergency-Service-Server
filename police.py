import paho.mqtt.client as mqtt
import time
import datetime
import json
import random 
        
k= [0, 0]
task = [["-","-","-"],["-","-","-"],["-","-","-"],["-","-","-"],["-","-","-"],["-","-","-"],["-","-","-"]]
pw1 = []
pw2 = []
pw3 = []
people = ["Polizist1", "Polizist2", "Polizist3", "Polizist4"]
fahrzeug_tracking = [[0],["Polizeiwagen 1","Polizeiwagen 2"], ["-","-"]]

#Event, dass beim eintreffen einer Nachricht aufgerufen wird
def on_message(client, userdata, msg):
    msgp = str(msg.payload.decode("utf-8")) #Nachricht Dekodieren
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    print(currentDT.strftime("%Y-%m-%d %H:%M:%S")+" Nachricht erhalten: "+str(msgp))
    #Hier die Verarbeitung der Nachricht einfügen

    if(msg.topic.endwish('task')):
        print("task")
        speichertask(task, fahrzeug_tracking, k, msg.payload)

    elif(msg.topic.endwish('bestätige')):
        print("bestätige")
        bestätige(task, fahrzeug_tracking, k, msg.payload)

    elif(msg.topic.endswith('stop')):
        print("error")

    elif(msg.topic.endwish('verfügbaren Fahrzeuge')):
            print("verfügbaren Fahrzeuge")
            data = {
                "verfügbaren Fahrzeuge": (len(fahrzeug_tracking[1])-fahrzeug_tracking[0][0]),
                "topic": "/hshl/polices/verfügbaren Fahrzeuge"}
            client.publish("/hshl/polices/verfügbaren Fahrzeuge", (json.dumps(data)))    

    elif (msg.topic.endwish('momentanen Koordinaten')):
            print("momentanen Koordinaten")
            i=0
            for x in range(0, len(task[0])):
                if task[0][i] != "-":
                   Xcoordinates = randint(0, 9)/10
                   Ycoordinates = randint(0, 9)/10
                   data = {
                        "task": task[0][i],
                        "Koordinaten": [51+Xcoordinates, 8+Ycoordinates],
                        "topic": "/hshl/polices/Koordinaten"}
                   client.publish("/hshl/polices/Koordinaten", (json.dumps(data)))
                elif (task[0][0] == "-" and task[0][1] == "-" and task[0][2] == "-" ):
                    data = {
                    "task": "Keine Tasks",
                    "Koordinaten": [51, 8],
                    "topic": "/hshl/polices/Koordinaten"}
                    client.publish("/hshl/polices/Koordinaten", (json.dumps(data)))
                    break
                i=i+1        

def speichertask (task, fahrzeug_tracking, k, data):
        global k
        global task
        i=0
        for x in range(0,len(task[0])):
            if task[0][i] == "-":
                k = i
                js = json.load(data)
                task[0][i] = js ["task"]
                task[1][i] = js["benFah"]
                task[2][i] = js["YKoor"]
                task[3][i] = js["XKoor"]
                data = {
                    "task": task[0][i],
                    "XKoor": task[2][i],
                    "YKoor": task[3][i],
                    "benFah": task[1][i],
                    "topic": "/hshl/polices/police 2"}
                print("sende Polizei 2")
                client.publish("/hshl/polices/police 2", json.dumps(data))
                break
            i = i+1

def bestätige(data, k):
        global task
        global fahrzeug_tracking
        sendefahrzeug(k)
            data = {
                "task":  task[0][k],
                "Fahrzeuge": task[4+k],
                "Informationen": "Die Fahrzeuge wurden an die angebenen Koordinaten versendet",
                "topic": "/hshl/polices/sende"}
            client.publish("/hshl/polices/sende", (json.dumps(data)))
        #wait
        data = {
            "task":  task[0][k],
            "Fahrzeuge": task[4+k],
            "Informationen": "Fahrzeug ist angekommen",
            "topic": "/hshl/polices/Aktualisierung"}
        client.publish("/hshl/polices/Aktualisierung", (json.dumps(data)))
        sendfahrzeugzurück(k)#can instead be used when reciving a message

        
    

def sendefahrzeug (k):
    global task
    global fahrzeug_tracking
    global people
    global pw1
    global pw2
    i=0
    if int(fahrzeug_tracking[0][0]) == int(len(fahrzeug_tracking[1]):#no vehicles avalible
        data = {
        "sende":  "Keine verfügbaren Fahrzeuge",
        "topic": "/hshl/polices/kvf"}
        client.publish("/hshl/polices/kvf", json.dumps(data))
    elif int(task[1][k]) > int(len(fahrzeug_tracking[1]))-int(fahrzeug_tracking[0][0]):
        print("notevic")
        data = {
        "sende":  "Nicht genügend Fahrzeuge vorhanden",
        "topic": "/hshl/polices/ngfv"}
        client.publish("/hshl/polices/ngfv", json.dumps(data))
    else:
        j=0
        for x in range(0, int(task[1][k])):
            for x in range(0, len(fahrzeug_tracking[1])):
                if  fahrzeug_tracking[1][i] != ("-"):
                    fahrzeug_tracking[1][i] = (fahrzeug_tracking[1][i])
                    fahrzeug_tracking[2][i] = ("-")
                    fahrzeug_tracking[0][0] = (fahrzeug_tracking[0][0] + 1)
                    task[4+k][j] = (fahrzeug_tracking[2][i])
                    if i == 0:
                        pw1.append(people[randint0, (len(people)-1))
                        people.remove(pw1[0])
                        pw1.append(people[randint0, (len(people)-1))
                        people.remove(pw2[1])
                    if i == 1:
                        pw2.append(people[randint0, (len(people)-1))
                        people.remove(pw2[0])
                        pw2.append(people[randint0, (len(people)-1))
                        people.remove(pw2[1])
                    break
                i=i+1
            j=j+1


def sendfahrzeugzurück (k):
    global task
    global fahrzeug_tracking
    global people
    global pw1
    global pw2
    i=0
    if fahrzeug_tracking[0][0] == 0:
        print("--")
    else:
        j=0
        for x in range(0, task[k][1]):
            for x in range(0, len(fahrzeug_tracking[2])):
                if task[4+k][j] == fahrzeug_tracking[2][i]:
                    fahrzeug_tracking[1][i] = fahrzeug_tracking[2][i]
                    fahrzeug_tracking[2][i] = "-"
                    fahrzeug_tracking[0][0] = (fahrzeug_tracking[0][0] - 1)
                    if i == 0:
                        people.append(pw1[0])
                        pw1.remove(pw1[0])
                        people.append(vic1[1])
                        pw1.remove(pw1[1])
                    if i == 1:
                        people.append(pw1[0])
                        pw1.remove(pw1[0])
                        people.append(pw1[1])
                        pw1.remove(pw1[1])
                    break
            j=j+1
        task[0][k[1]] = "-"
        task[1][k[1]] = "-"
        task[2][k[1]] = "-"
        task[3][k[1]] = "-"
        task[4][k[1]] = "-"
        



        
#Event, dass beim Verbindungsaufbau aufgerufen wird
def on_connect(client, userdata, flags, rc):
    client.subscribe([  ("/hshl/polices/verfügbaren Fahrzeuge", 2),
                        ("/hshl/polices/momentanen Koordinaten", 2),
                        ("hshl/polices/task", 2),
                        ("/hshl/polices/bestätigung", 2),
                        ("/hshl/polices/stop", 2)
                        ])


#Dont change anything from here!!
BROKER_ADDRESS = "mr2mbqbl71a4vf.messaging.solace.cloud" #Adresse des MQTT Brokers
client = mqtt.Client()
client.on_connect = on_connect #Zuweisen des Connect Events
client.on_message = on_message #Zuweisen des Message Events
client.username_pw_set("solace-cloud-client", "nbsse0pkvpkvhpeh3ll5j7rpha") # Benutzernamen und Passwort zur Verbindung setzen
client.connect(BROKER_ADDRESS, port = 20614) #Verbindung zum Broker aufbauen

print("Connected to MQTT Broker: " + BROKER_ADDRESS)
client.loop_forever()#Endlosschleife um neue Nachrichten empfangen zu können

