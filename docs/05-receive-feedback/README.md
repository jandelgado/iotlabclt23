# Sensordaten per MQTT versenden

In dieser Übung empfangen wir Daten vom Backend und stellen diese durch 
ein visuelles Feedback dar.

Jedesmal wenn das Backend eine Messung empfängt, schickt es eine Bestätigung
(auch Ackknowledge oder ACK genannt) an das sendende Gerät zurück. Das geschieht
über das MQTT-Topic `iotlabclt23/<deviceID>/ack`. Als Nachricht wird dabei immer
die Zeichenfolge `ack` übertragen.

## Anpassungen am Code

Damit wir die Daten per MQTT empfangen können, müssen wir das Programm um 
folgende Funktionen erweitern:

* unser Device muss sich auf das Topic `iotlabclt23/<deviceid>/ack` subscriben
* wenn eine Nachricht empfangen wird, dann wird ein LED-Statusobjekt initialisiert
* in der Hauptschleife muss kontinuierlich das LED-Statusobjekt aktualisiert 
  werden

### Aufgabe 

Die Funktion `mqtt_on_connect` muss erweitert werden, so dass unser Client
sich beim Topic `iotlabclt23/<deviceid>/ack` subscribed. Erweitere den Code um

```python
def mqtt_on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    # Wir möchten Nachrichten vom Backend auf dem Topic ack_topic empfangen
    client.subscribe(ack_topic)
```

Die Variable `ack_topic`, die das MQTT-Topic enthält, ist schon weiter oben
im Code definiert worden.

Die Funktion `mqtt_on_message` wird nun immer dann aufgerufen, wenn eine
Nachricht über das MQTT empfangen wurde. Dort intialisieren wir unsere Status
LED mit einem neuen Effekt:

```python
def mqtt_on_message(client, topic, message):
    # Diese Methode wird aufgerufen, wenn wir eine Nachricht empfangen
    print(f"New message on topic {topic}: {message}")
    # Effekt für Status LED setzen
    statusLED.fade_off(750)
```

Die Variable `statusLED`, die die LED darstellt, ist schon weiter oben im Code
definiert worden. (Die LED wird mit der JLed Bibliothek gesteuert, siehe auch
https://jandelgado.github.io/jled-circuitpython/)

Zum Schluss müssen wir die Status LED kontinuierlich in der Hauptschleife
aktualisieren:

```python
while True:
    # MQTT message queue pollen
    mqtt_client.loop()
    # Status LED aktualisieren
    statusLED.update()
...
```

Die Stellen sind im Code mit **TODO** Kommentaren markiert.

### Test

Wenn alles funktioniert, sollte jede vom Backend empfangene Nachricht mit
einem Blinken der LED quittiert werden.


