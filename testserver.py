import paho.mqtt.client as mqtt
import time
import json

task = [""]
koordinaten1 = [0]
koordinaten2 = [0]
benötigte_fahrzeuge = [0]
task = input("Task angeben: ")
koordinaten1 = input("X Koordinaten eingeben: ")
koordinaten2 = input("Y Koordinaten eingeben: ")
benötigte_fahrzeuge = input("Fahrzeug Anzahl angeben")
a = [0]
b = [0]
c = [0]
d = [0]

    #Event, dass beim Verbindungsaufbau aufgerufen wird
def on_connect(client, userdata, flags, rc):
    client.subscribe([('/hshl/polices/police 2', 2),
                      ('/hshl/polices/sende', 2),
                      ('/hshl/polices/Aktualisierung', 2),
                      ('/hshl/polices/kvf', 2),
                      ('/hshl/polices/ngfv', 2),
                      ('/hshl/polices/verfügbaren Fahrzeuge', 2),
                      ('/hshl/polices/Koordinaten', 2)
                      ])
    task_abfragen(task, koordinaten1, koordinaten2, benötigte_fahrzeuge)

def verfügbaren_fahrzeuge_abfragen():
    data = {
        "topic": "hshl/police/verfügbaren Fahrzeuge"}
    client.publish("/hshl/polices/verfügbaren Fahrzeuge", json.dumps(data))

def momentane_koordinaten_abfragen():
    data = {
        "topic": "hshl/police/momentanen Koordinaten"}
    client.publish("/hshl/polices/momentanen Koordinaten", json.dumps(data)) 
        
def task_abfragen(task, koordinaten1, koordinaten2, benötigte_fahrzeuge):
    data = {
        "task": task,
        "XKoor": koordinaten1,
        "YKoor": koordinaten2,
        "Benötigte Fahrzeuge": benötigte_fahrzeuge,
        "topic": "hshl/police/task"}
    client.publish("hshl/polices/task", json.dumps(data))



def register_police(data, koordinaten1, koordinaten2, benötigte_fahrzeuge):
    js = json.load(data)
    a = js["task"]
    b = js["XKoor"]
    c = js["YKoor"]
    d = js["benFah"]
    if str(task) != str(a):
        stop()
    elif koordinaten1 != b:
        stop()
    elif koordinaten2 != c:
        stop()
    elif benötigte_fahrzeuge != d:
        stop()
    else:
        data = {
            "bestätigung": "bestätigung",
            "topic": "/hshl/polices/bestätigung"}
        client.publish("/hshl/polices/bestätigung", json.dumps(data))

def stop():
    data = {
            "STOP": "STOP",
            "topic": "/hshl/police/stop"}
    print("sending stop")
    client.publish("/hshl/polices/stop", json.dumps(data))
    print("send")
    
def empfangen(data):
    ja = json.loads(data)
    fahrzeuge = js["Fahrzeuge"] #Vehicles that have been sent
    verfügbaren_fahrzeuge = js["verfügbaren Fahrzeuge"] #amount of avalible vehicles at base
    topic = js["topic"]

def verfügbaren_fahrzeuge (data):
    js = json.loads(data)
    vf = js["verfübaren Fahrzeuge"]

def speicher_koordianten(data):
    js = json.loads(data)
    koordinaten = js["Koordinaten"]

def on_message(client, userdata, msg):
    msgp = str(msg.payload.decode("utf-8")) #Nachricht Dekodieren
    currentDT = datetime.datetime.now() #Aktuelle Uhrzeit
    print(currentDT.strftime("%Y-%m-%d %H:%M:%S")+" Nachricht erhalten: "+str(msgp))
    if(msg.topic.endswith('police 2')):
        register_police(msg.payload)

    if(msg.topic.endswith('sende')):
        empfangen(msg.payload)

    if(msg.topic.endswith('kvf')):
        print("-")
    if(msg.topic.endswith('ngfv')):
        print("-")
    if(msg.topic.endswith('verfügbaren Fahrzeuge')):
        verfügbaren_fahrzeuge(msg.payload)

    if(msg.topic.endswith('Koordinaten')):
        speicher_koordianten(msg.payload)

    if(msg.topic.endswith('Aktualisierung')):
        print("Fahrzeug ist angekommen ")

    

#Dont change anything from here!!
BROKER_ADDRESS = "mr2mbqbl71a4vf.messaging.solace.cloud" #Adresse des MQTT Brokers
client = mqtt.Client()
client.on_connect = on_connect #Zuweisen des Connect Events
client.on_message = on_message
client.username_pw_set("solace-cloud-client", "nbsse0pkvpkvhpeh3ll5j7rpha") # Benutzernamen und Passwort zur Verbindung setzen
client.connect(BROKER_ADDRESS, port = 20614) #Verbindung zum Broker aufbauen

print("Connected to MQTT Broker: " + BROKER_ADDRESS)
client.loop_forever()#Endlosschleife um neue Nachrichten empfangen zu können


