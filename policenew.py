import paho.mqtt.client as mqtt
import time
import datetime
import random

task = []
of = []
k = 0
vf = 2

        
#Event, dass beim eintreffen einer Nachricht aufgerufen wird
def on_message(client, userdata, msg):
    msgp = str(msg.payload.decode("utf-8")) #Nachricht Dekodieren
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    print(currentDT.strftime("%Y-%m-%d %H:%M:%S")+" Nachricht erhalten: "+str(msgp))
    split = str(msg).split(" ")
    if(msg.topic.split == "task"):
        speichertask(split, vf)

    elif(msg.topic.endwish('bestätige')):
        bestätige(split, task)

    elif(msg.topic.endswith('stop')):
        print("")

    elif(msg.topic.endswith('verfügbaren Fahrzeuge')):
        sende_vf(vf)
    
    elif(msg.topic.endswith('momentane Koordinaten')):###doesn't do anything as long as the vehicles return istantly
        sende_koordinaten(task, split, of)###




def polizist_hinzufügen(vf):
    global of
    officers = ["Polizist1", "Polizist2", "Polizist3", "Polizist4"]
    pos = [51.67, 8.34]
    fahrzeuge = vf
    i = 0
    j=0
    for x in range (0, vf):
        if (len(officers) >= 2):
            of.append(officers[0])
            officers.remove(of[0+j])
            of.append(officers[0])
            officers.remove(of[1+j])
            randpos1 = pos[0]+(random.randint(-9, 9)/10)
            randpos2 = pos[1]+(random.randint(-9, 9)/10)
            randpos1 = round(randpos1, 2)
            randpos2 = round(randpos2, 2)
            of.append("Polizeiwagen "+str(i))
            of.append(str(randpos1)+","+str(randpos2))
            polizei = (str(of[0+j])+" "+str(randpos1)+","+str(randpos2)+" "+"isFree"+" "+"p"+str(i))
            j = j+4
            i=i+1
            print(polizei)
            client.publish("/hshl/polizei/Koordinaten", polizei)
    print(of)


def speichertask (split):
    if (vf >= 1):
        global task
        global k
        task.append(split[0]) #Task
        task.append(split[1]) #Koordinaten
        task.append(split[2]) #ID
        bestä = (str(task[0]))+" "+(str(task[1+k]))+" "+(str(task[2+k]))
        k = k+3
        print(bestä)
        client.publish("/hshl/polizei/", bestä)
        

def bestätige(split, task):
    global k
    x = task.index(split[0])
    send = (task[x+2]+" "+"wirdBenutzt")
    client.publish("/hshl/polizei/", sende)
    vf = vf-1
    sende = (task[x+2]+" "+"Ankunft")
    client.publish("/hshl/polizei/", sende)
    sende = (task[x+2]+" "+"Rückkehr")
    client.publish("/hshl/polizei/", sende)
    task.remove(task[x])
    task.remove(task[x])
    task.remove(task[x])
    k = k-3
    vf = vf+1
    

def get_vf(vf):
    client.publish("/hshl/polizei/", vf)

def get_koordinaten(task, split):
    if len(task) >=1 :
        ko = []
        kof = []
        mk = []
        x = task.index(split[0])
        ko = task[1+x].split(",")
        ko[0] = float(ko[0])
        ko[1] = float(ko[1])
        kof = of[x+4].split("2")
        kof[0] = float(kof[0])
        kof[1] = float(kof[1])
        mk[0] = (ko[0]+kof[0])/2
        mk[1] = (ko[1]+kof[1])/2
        kok = (str(mk[0])+","+str(mk[1]))
        client.publish("/hshl/polices/", ccc)
    else:
        
        a = "No vehilces send"
        client.publish("/hshl/polices/", a)


        


#Event, dass beim Verbindungsaufbau aufgerufen wird
def on_connect(client, userdata, flags, rc):
    client.subscribe('/hshl/polizei/')
    polizist_hinzufügen(vf)
    

#Dont change anything from here!!
BROKER_ADDRESS = "mr2mbqbl71a4vf.messaging.solace.cloud" #Adresse des MQTT Brokers
client = mqtt.Client()
client.on_connect = on_connect #Zuweisen des Connect Events
client.on_message = on_message #Zuweisen des Message Events
client.username_pw_set("solace-cloud-client", "nbsse0pkvpkvhpeh3ll5j7rpha") # Benutzernamen und Passwort zur Verbindung setzen
client.connect(BROKER_ADDRESS, port = 20614) #Verbindung zum Broker aufbauen

print("Connected to MQTT Broker: " + BROKER_ADDRESS)
client.loop_forever()#Endlosschleife um neue Nachrichten empfangen zu können


        





        
