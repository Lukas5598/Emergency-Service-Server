import paho.mqtt.client as mqtt
import time
import datetime
import random
task = []
of = [] 
avv = 2 #anzahl Fahrzeuge
vf=0 #verfügbare Fahrzeuge
tr = []

def feuerwehr(avv):
    global of
    global vf
    ff = ["Feuerwehrmann1", "Einsatzleiter1", "Feuerwehrmann2", "Feuerwehrmann3", "Feuerwehrmann4", "Feuerwehrmann5",
          "Feuerwehrmann6", "Feuerwehrmann7", "Feuerwehrmann8", "Feuerwehrmann9", "Einsatzleiter2", "Feuerwehrmann10",
          "Feuerwehrmann11", "Feuerwehrmann12", "Feuerwehrmann13", "Feuerwehrmann14", "Feuerwehrmann15", "Feuerwehrmann16", ]
    pos = [51.67, 8.34]
    i = 0
    j=0
    for x in range (0, avv):
        if (len(ff) >= 9):
            for x in range(0, 9):
                of.append(ff[0])
                ff.remove(ff[0])
            randpos1 = pos[0]+(random.randint(-9, 9)/10)
            randpos2 = pos[1]+(random.randint(-9, 9)/10)
            randpos1 = round(randpos1, 2)
            randpos2 = round(randpos2, 2)
            of.append("s"+str(i+1))
            of.append(str(randpos1)+","+str(randpos2))
            topic="/hshl/firefighters/"
            payload = (str(of[0+j])+" "+str(randpos1)+","+str(randpos2)+" "+"True"+" "+"s"+str(i+1))
            j= j+11
            i=i+1
            vf = vf+1            
            print(payload)
            client.publish(topic, payload)

def task_saver(split, b, of):
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    global vf
    global task
    global tr
    b = str(b[0]+b[1])
    if(vf >= 1):
        task.append(split[0])#Reason
        task.append(split[1])#Coordinates
        task.append(split[2])#Dist
        task.append(b)#ID
        x = task.index(b)
        try:
            print("Task: ")
            print(task[x])
            print(task[x-3])
            print(task[x-2])
            print(task[x-1])
        except:
            print("Error - No Tasks")
        topic = ("/hshl/firefighters/"+b)
        payload = (b+" "+"True"+" "+currentDT.strftime("%Y-%m-%d %H:%M:%S"))
        client.publish(topic, str(payload))
        topic = ("/hshl/firefighters/sendeFahrzeug")
        y = of.index(str(b))
        payload = (b+" "+task[x-2]+" "+of[y+1])
        client.publish(topic, str(payload))
        print("Send confirmation")
        tr.append(str(b))
        tr.append("True")
        vf = vf-1
    else:
        print("No Vehicles avalible")
        topic = ("/hshl/firefighters/"+b)
        payload = (b+" "+"False"+" "+currentDT.strftime("%Y-%m-%d %H:%M:%S"))
        client.publish(topic, str(payload))
            
def fahrzeug_rückkehr(split):
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    global tr
    try:
        y = tr.index(split[0])
        if((str(tr[y]) == str(split[0])) and (str(tr[y+1]) == "False")):
            try:
                b = split[1]
                b = list(b.split(",", 1))
                if(isinstance(float(b[0]), float) == True):
                    if(isinstance(float(b[1]), float) == True):
                        koordinaten(split)
                        global task
                        global vf
                        x = task.index(split[0])
                        topic = ("/hshl/firefighters/"+task[x])
                        payload = (str(task[x])+" "+"Vehicle_Avalible"+" "+"True"+" "+currentDT.strftime("%Y-%m-%d %H:%M:%S"))
                        client.publish(topic, str(payload))
                        print("Vehicle Returned")
                        print(task[x])
                        task.remove(task[x-3])
                        task.remove(task[x-3])
                        task.remove(task[x-3])
                        task.remove(task[x-3])
                        tr.remove(tr[y])
                        tr.remove(tr[y])
                        vf = vf+1
            except:
                ("Wrong Data")
    except:
        print("Error -")

def control(split):
    try:
        b = split[1]
        b = list(b.split(",", 1))
        if(isinstance(float(b[0]), float) == True):
            if(isinstance(float(b[1]), float) == True):
                global tr
                x = tr.index(str(split[0]))
                if((str(tr[x]) == str(split[0])) and (str(tr[x+1]) == "True")):
                    tr[x+1] = "False"
                    koordinaten(split)
    except:
        print("Wrong Data")

def koordinaten(split):
    topic = ("/hshl/firefighters/"+split[0])
    payload = (split[1])
    client.publish(topic, str(payload))
        
#Event, dass beim eintreffen einer Nachricht aufgerufen wird
def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8")) #Nachricht Dekodieren
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    print(currentDT.strftime("%Y-%m-%d %H:%M:%S")+" Nachricht erhalten: "+str(msg))
    split = msg.split(" ")
    i=0
    a = message.topic.split("/")
    print(a)
    b = list(a[3])
    try:
        if(a[3] == 'FahrzeugRückkehr'):
            fahrzeug_rückkehr(split)
        elif(a[3] == 'FahrzeugAnkunft'):
                control(split)
        elif(b[0] == "s"):
            try:
                c = str(b[0]+b[1])
                c =(task.index(c))
            except:
                try:
                    if(str(split[1]) != "Vehicle_Avalible"):
                        if(len(split) == 3):
                            print("Checking...")
                            task_saver(split, b, of)
                except:
                    print("")
    except:
        print("Unknown topic")


        
#Event, dass beim Verbindungsaufbau aufgerufen wird
def on_connect(client, userdata, flags, rc):
    client.subscribe('/hshl/firefighters/FahrzeugRückkehr')
    client.subscribe('/hshl/firefighters/FahrzeugAnkunft')
    i = 1
    global vf
    for x in range(0, avv):
        a = ("/hshl/firefighters/s"+str(i))
        print(a)
        client.subscribe(str(a))
        i = i+1
    print("subsribed")
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
