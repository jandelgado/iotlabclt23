# IoT-Lab Temperature Monitoring 

The backend consist of 3 services:

* `temperature-monitor` - a go client that subscribes to the MQTT topic on 
  which the devices publish their measurements. The service exposes these 
  measurements as prometheus metrics
* `prometheus` - metrics database that scrapes the measurements and stores the
  data
* `grafana` - visualization tool

## Configuration

Services are configured in the [docker-compose.yml](docker-compose.yml) file.
The most important setting is the MQTT-Server to use. By default we use the 
public `mqtt.hive.com` MQTT service.

## Start

We use docker-compose for orchestration of the services. 

* `docker-compose up` to start 
* `docker-compose up` to stop

## Links

* http://localhost:9090 - prometheus web UI
* http://localhost:3000 - grafana web UI (admin/admin)
* http://localhost:2121/metric - Metrics endpoint of temperature-monitor

## Author

(c) copyright 2023 by Jan Delgado

