.PHONY=phony

all: build

phony:

build: phony
	go build -o bin/iot-temperature-monitor

export IOT_MQTT_HOST=broker.hivemq.com
export IOT_MQTT_PORT=1883
export IOT_MQTT_USER=
export IOT_MQTT_PASSWORD=
export IOT_MQTT_SUB_TOPIC=iotlabclt23/+/temperature
export IOT_MQTT_ACK_TOPIC=iotlabclt23/%s/ack
export IOT_PORT=2121
export IOT_SIMULATE_DEVICES=team99,team1,team2,team3,team4,team5

run: phony
	./bin/iot-temperature-monitor

