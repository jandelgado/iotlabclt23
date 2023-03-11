# Sensordaten per MQTT versenden

In dieser Übung machen wir unsere Device internetfähig. Wir bauen auf der 
vorherigen Übung auf und erweitern den Code so, dass Sensordaten über das
[MQTT](https://de.wikipedia.org/wiki/MQTT) Protokoll an einen MQTT-Broker geschickt werden.

## Anpassungen am Code

Damit wir die Daten per MQTT verschicken können, haben wir unser Programm um
folgende Funktionen erweitert:

* eine WiFi-Netzwerkverbindung herstellen
* die Verbindung zum MQTT-Broker herstellen
* Funktion `daten_senden` um Messwerte als JSON-Nachricht auf ein MQTT-Topic
  publizieren hinzugefügt

### Aufgabe 

Erweitere jetzt den [Code](code-template.py) um die Funktionen `sensor_lesen`
und `daten_ausgeben` aus der vorherigen Übung, und baue den Aufruf der
Funktionen und der neuen Funktion `daten_senden` an der richtigen Stelle ein.
Der Aufruf von `daten_senden` sollte wie folgt aussehen:

```python
daten_senden(mqtt_client, counter, temperature, pressure, secrets["deviceid"])
```

Die Stellen sind im Code mit **TODO** Kommentaren markiert.

### Test

Wenn alles funktioniert, sollte nun fortlaufend Temperatur- und Luftdruckwerte
per MQTT an das Backend gesendet werden. Die aktuelle Temperatur wird zudem 
auf dem Display ausgegeben.

#### Fehlersuche

* Stimmt die Verkabelung?
  * Sensor
  * Display
* Ist die Syntax korrekt?
  * Meldet der Python-Interpreter Syntax-Fehler?
* Kann die Netzwerkverbindung aufgebaut werden?

