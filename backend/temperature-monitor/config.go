package main

import (
	"github.com/kelseyhightower/envconfig"
)

type Configuration struct {
	MQTTHost        string   `required:"true" split_words:"true"`
	MQTTPort        int      `required:"true" split_words:"true"`
	MQTTUser        string   `split_words:"true"`
	MQTTPassword    string   `split_words:"true"`
	MQTTSubTopic    string   `required:"true" split_words:"true"`
	MQTTAckTopic    string   `required:"true" split_words:"true"`
	MQTTClientID    string   `default:"iot-backend" split_words:"true"`
	Port            int      `required:"false" default:"2121"`
	SimulateDevices []string `required:"false" split_words:"true"`
}

func parseConfig() (Configuration, error) {
	var s Configuration
	err := envconfig.Process("iot", &s)
	return s, err
}
