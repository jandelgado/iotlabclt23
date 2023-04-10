// a simple "backend" for the IoT workshop
//
// Listens on configured MQTT topic for messages and deserializes received
// messages and write prometheus metrics with temperature and pressure read
// from the messages. Sends ACK message back to device upon receival.
//
// (C) copyright 2023 by Jan Delgado, Licence MIT
package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"time"

	"net/http"

	mqtt "github.com/eclipse/paho.mqtt.golang"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

var (
	metricTempGauge = promauto.NewGaugeVec(prometheus.GaugeOpts{
		Name: "temperature",
		Help: "Observed temperature",
	}, []string{"deviceid"})

	metricPressureGauge = promauto.NewGaugeVec(prometheus.GaugeOpts{
		Name: "pressure",
		Help: "Observed pressure"},
		[]string{"deviceid"},
	)
)

// SensorMessage models the message sent from the devices in JSON format
type SensorMessage struct {
	DeviceID    string  `json:"deviceid"`
	Temperature float64 `json:"temperature"`
	Pressure    float64 `json:"pressure"`
}

func onConnectHandler(client mqtt.Client) {
	log.Println("Connected to broker")
}

func onConnectionLostHandler(client mqtt.Client, err error) {
	log.Printf("Connection lost: %v\n", err)
}

func main() {
	config, err := parseConfig()
	if err != nil {
		panic(err)
	}

	opts := mqtt.NewClientOptions()
	opts.AddBroker(fmt.Sprintf("tcp://%s:%d", config.MQTTHost, config.MQTTPort))
	opts.SetClientID(config.MQTTClientID)
	opts.SetUsername(config.MQTTUser)
	opts.SetPassword(config.MQTTPassword)

	onConnectHandler := func(client mqtt.Client) {
		log.Println("(re-)connected to broker")
		subscribe(client, config.MQTTSubTopic, config.MQTTAckTopic)
	}

	opts.OnConnect = onConnectHandler
	opts.OnConnectionLost = onConnectionLostHandler

	client := mqtt.NewClient(opts)
	if token := client.Connect(); token.Wait() && token.Error() != nil {
		panic(token.Error())
	}

	if len(config.SimulateDevices) > 0 {
		// randomly generate metrics for given devices
		go simulation(config.SimulateDevices)
	}

	http.Handle("/metrics", promhttp.Handler())
	http.ListenAndServe(fmt.Sprintf(":%d", config.Port), nil)
}

// sgenerate simulated metrics
func simulation(devices []string) {
	log.Printf("starting simulation for %+v", devices)
	for _, deviceID := range devices {
		metricTempGauge.WithLabelValues(deviceID).Set(20.)
		metricPressureGauge.WithLabelValues(deviceID).Set(1020.)
	}

	for {
		deltaT := rand.Float64() - 0.5
		deltaP := rand.Float64()*2 - 1
		deviceID := devices[rand.Intn(len(devices))]
		metricTempGauge.WithLabelValues(deviceID).Add(deltaT)
		metricPressureGauge.WithLabelValues(deviceID).Add(deltaP)
		time.Sleep(time.Second * 5)
	}
}

// ackTopic constructs the topic from the given "template" and the deviceID
func ackTopic(topicTpl, deviceID string) string {
	return fmt.Sprintf(topicTpl, deviceID)
}

func publish(client mqtt.Client, topic, message string) {
	token := client.Publish(topic, 0, false, message)
	token.Wait()
}

func unmarshalMessage(msg mqtt.Message) (SensorMessage, error) {
	var message SensorMessage
	err := json.Unmarshal(msg.Payload(), &message)
	return message, err
}

func subscribe(client mqtt.Client, subTopic, pubACKTopic string) {

	handler := func(client mqtt.Client, mqttMsg mqtt.Message) {
		log.Printf("Received message: %s from topic: %s", mqttMsg.Payload(), mqttMsg.Topic())

		message, err := unmarshalMessage(mqttMsg)
		if err != nil {
			log.Printf("ERROR: unmarshalling %s: %v", mqttMsg, err)
			return
		}
		// update metrics
		metricTempGauge.WithLabelValues(message.DeviceID).Set(message.Temperature)
		metricPressureGauge.WithLabelValues(message.DeviceID).Set(message.Pressure)
		// send ACK
		publish(client, ackTopic(pubACKTopic, message.DeviceID), "ack")
	}

	token := client.Subscribe(subTopic, 1, handler)
	token.Wait()
	log.Printf("Subscribed to topic: %s", subTopic)
}
