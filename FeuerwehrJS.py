import paho.mqtt.client as mqtt
import time
import datetime
import random
import json
task = []
of = []
koor = []
avv = 2
vf=0
tr = []

def feuerwehr(avv):
    global of
    global vf
    global koor
    officers = ["Feuerwehrmann1", "Einsatzleiter1", "Feuerwehrmann2", "Feuerwehrmann3", "Feuerwehrmann4", "Feuerwehrmann5",
                "Feuerwehrmann6", "Feuerwehrmann7", "Feuerwehrmann8", "Feuerwehrmann9", "Einsatzleiter2", "Feuerwehrmann10",
                "Feuerwehrmann11", "Feuerwehrmann12", "Feuerwehrmann13", "Feuerwehrmann14", "Feuerwehrmann15", "Feuerwehrmann16"]
    pos = [51.67, 8.34]
    i = 0
    j=0
    for x in range (0, avv):
        if (len(officers) >= 2):
            for x in range(0, 2):
                of.append(officers[0])
                officers.remove(officers[0])
            randpos1 = pos[0]+random.randint(-7, 9)+(random.randint(-9, 9)/10)
            randpos2 = pos[1]+random.randint(-7, 9)+(random.randint(-9, 9)/10)
            randpos1 = round(randpos1, 2)
            randpos2 = round(randpos2, 2)
            of.append("s"+str(i+1))
            of.append(str(randpos1)+","+str(randpos2))
            loc = [float(randpos1), float(randpos2)]
            koor.append(pos)
            koor.append(pos)
            koor.append("s"+str(i+1))
            topic="/hshl/firefighters/"
            currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
            data = {
                "time": currentDT.strftime("%Y-%m-%d %H:%M:%S"),
                "driver_name": str(of[0+j]),
                "location": loc,
                "isFree" : "True",
                "id": "s"+str(i+1),
                "topic": topic}
            print(str(of[j])+" "+str(of[j+1])+" "+str(of[j+2])+" "+str(of[j+3]))
            j= j+4
            i=i+1
            vf = vf+1     
            client.publish(topic, json.dumps(data))
            a = ("/hshl/firefighters/s"+str(i))
            print(a)
            client.subscribe(str(a))
        

def task_saver(data, b, of):
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    global vf
    global task
    global tr
    global koor
    b = str(b[0]+b[1])
    try:
        c = (task.index(b))
        print("Vehicle not avalible")
        topic = ("/hshl/firefighters/"+b)
        data = {
        "time": currentDT.strftime("%Y-%m-%d %H:%M:%S"),
        "id": b,
        "isFree": "False",
        "self": "true",
        "acc" : "False",
        "location": koor[koor.index(b)-1],
        "reasons": task[task.index(b)-3],
        "driver_name": of[of.index(b)-2],
        "topic": topic}
        client.publish(topic, json.dumps(data))
    except:
        if(vf >= 1):
            js = json.loads(data)
            task.append(js["reasons"])#Reason
            a = js["location"]
            a = str(a[0])+","+str(a[1])
            task.append(a)#Coordinates
            task.append("Dist")#Dist
            task.append(b)#ID
            x = task.index(b)
            topic = ("/hshl/firefighters/"+b)
            data = {
                "time": currentDT.strftime("%Y-%m-%d %H:%M:%S"),
                "id": b,
                "isFree": "False",
                "self": "true",
                "acc" : "True",
                "location": koor[koor.index(b)-1],
                "reasons": task[task.index(b)-3],
                "driver_name": of[of.index(b)-2],
                "topic": topic}
            client.publish(topic, json.dumps(data))
            topic = ("/hshl/firefighters/sendeFahrzeug")
            payload = (b+" "+task[x-2]+" "+of[x])
            client.publish(topic, str(payload))
            print("Send confirmation")
            tr.append(str(b))
            tr.append("True")
            vf = vf-1
        else:
            print("No Vehicles avalible")
            topic = ("/hshl/firefighters/"+b)
            data = {
                "time": currentDT.strftime("%Y-%m-%d %H:%M:%S"),
                "id": b,
                "isFree": "False",
                "self": "true",
                "acc" : "False",
                "location": koor[koor.index(b)-1],
                "reasons": task[task.index(b)-3],
                "driver_name": of[of.index(b)-2],
                "topic": topic}
            client.publish(topic, json.dumps(data))
            
def fahrzeug_rückkehr(split, of):
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    global tr
    try:
        x = tr.index(split[0])
        if(str(tr[x+1]) == "False"):
            try:
                b = split[1]
                b = list(b.split(",", 1))
                if(isinstance(float(b[0]), float) == True):
                    if(isinstance(float(b[1]), float) == True):
                        global task
                        global vf
                        global koor
                        koor[int(koor.index(tr[x]))-1] = [float(b[0]), float(b[1])]
                        topic = ("/hshl/firefighters/"+str(tr[x]))
                        data = {
                            "time": currentDT.strftime("%Y-%m-%d %H:%M:%S"),
                            "self": "true",
                            "location": koor[koor.index(str(tr[x]))-1],
                            "isFree" : "True",
                            "reasons": task[task.index(str(tr[x]))-3],
                            "driver_name": of[of.index(str(tr[x]))-2],
                            "id": str(tr[x]),
                            "topic": topic}
                        client.publish(topic, json.dumps(data))
                        print("Vehicle Returned")
                        y = task.index(tr[x])
                        task.remove(task[y-3])
                        task.remove(task[y-3])
                        task.remove(task[y-3])
                        task.remove(task[y-3])
                        tr.remove(tr[x])
                        tr.remove(tr[x])
                        vf = vf+1
            except:
                ("Wrong Data")
    except:
        print("Error -")

def control(split, task, of):
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    try:
        b = split[1]
        b = list(b.split(",", 1))
        if(isinstance(float(b[0]), float) == True):
            if(isinstance(float(b[1]), float) == True):
                global tr
                global koor
                x = tr.index(str(split[0]))
                if(str(tr[x+1]) == "True"):
                    koor[int(koor.index(tr[x]))-1] = [float(b[0]), float(b[1])]
                    topic = ("/hshl/firefighters/"+str(tr[x]))
                    data = {
                        "time": currentDT.strftime("%Y-%m-%d %H:%M:%S"),
                        "location": koor[koor.index(str(tr[x]))-1],
                        "id": str(tr[x]),
                        "self": "true",
                        "isFree": "False",
                        "reasons": task[task.index(str(tr[x]))],
                        "driver_name": of[of.index(str(tr[x]))-2],
                        "topic": topic}
                    client.publish(topic, json.dumps(data))
                    tr[x+1] = "False"
    except:
        print("Wrong Data")

#Event, dass beim eintreffen einer Nachricht aufgerufen wird
def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8")) #Nachricht Dekodieren
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    print(currentDT.strftime("%Y-%m-%d %H:%M:%S")+" Nachricht erhalten: "+str(msg))
    i=0
    global task
    a = message.topic.split("/")
    print(a)
    b = list(a[3])
    try:
        if(a[3] == 'FahrzeugRückkehr'):
            split = msg.split(" ")
            print(split)
            fahrzeug_rückkehr(split, of)
        elif(a[3] == 'FahrzeugAnkunft'):
            split = msg.split(" ")
            print(split)
            control(split, task, of)
        elif(b[0] == "s"):
            try:
                js = json.loads(message.payload)
                if (js["self"] == "true"):
                    g = 1
            except:
                task_saver(message.payload, b, of)
    except:
        print("Unknown topic")
        
        
#Event, dass beim Verbindungsaufbau aufgerufen wird
def on_connect(client, userdata, flags, rc):
    client.subscribe('/hshl/firefighters/FahrzeugRückkehr')
    client.subscribe('/hshl/firefighters/FahrzeugAnkunft')
    feuerwehr(avv)

#Dont change anything from here!!
BROKER_ADDRESS = "mr2mbqbl71a4vf.messaging.solace.cloud" #Adresse des MQTT Brokers
client = mqtt.Client()
client.on_connect = on_connect #Zuweisen des Connect Events
client.on_message = on_message #Zuweisen des Message Events
client.username_pw_set("solace-cloud-client", "nbsse0pkvpkvhpeh3ll5j7rpha") # Benutzernamen und Passwort zur Verbindung setzen
client.connect(BROKER_ADDRESS, port = 20614) #Verbindung zum Broker aufbauen

print("Connected to MQTT Broker: " + BROKER_ADDRESS)
client.loop_forever()#Endlosschleife um neue Nachrichten empfangen zu können
