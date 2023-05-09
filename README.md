# Greenhouse Monitor Project - Documentation

## Description

The project to be undertaken is a greenhouse monitoring system. This system will consist of sensors that monitor environmental conditions inside the greenhouse and relay this information over the internet in order to facilitate remote monitoring. The system should be able to run on a single board computer, in this case a Raspberry Pi 4 Model B is chosen, which then gathers sensor data via a Physical sensor and this data is sent to a server which in turn sends the data over the cloud for remote access.



## What - The Problem 

The onset of climate change has brought about variations in our seasons in terms of length and intensity of the weather elements associated with the seasons; specifically hotter summers and more rainy spring and fall seasons. These seasonal changes provide environments that are unfavorable for crop growth. For crops to grow, they require a certain amount of moisture content, air supply and sunlight exposure. Hotter summers make it too hot for plants to thrive and wetter seasons drown the crops. As a result of this unfavorable weather, crop production is unpredictable and poses a risk to food security. 
One way to combat this is to introduce artificial spaces that provide optimal conditions for plants to thrive, in this case, greenhouses. In order to have efficient greenhouses, the crops being grown require constant monitoring. In this scenario, a monitoring system will be built that will monitor the temperature of the environment, the relative humidity, as well as the barometric pressure. This system will ensure that the temperature in the greenhouse is a constant 20 degrees C and the relative humidity at 40%. The barometric pressure is taken so as to perform a study on the impact of varying pressures on plant growth. A humidifier and HVAC system are set up as actuators and these will turn on in case the humidity and temperature exceed the preset thresholds with the aim of bringing back the conditions to their optimum values. 



## Why - Who Cares? 

[The world's population has hit 8 billion,](https://www.un.org/en/desa/world-population-hits-8-billion-people) a milestone that signals a major improvement in public health and increased life expectancy. The growing population requires to be adequately fed and the adverse effects of climate change are leading to existing resources being underutilized. Technology can bridge this gap and facilitate a better utilization of natural resources for efficient food production. This is the inspiration behind designing the greenhouse monitoring system. This system tracks the crops vitals and replenishes them only when required, thus saving water and also providing optimal growth temperature for these crops. 
[A recent study](https://sbir.nasa.gov/SBIR/abstracts/87/sbir/phase1/SBIR-87-1-12.06-3053.html#:~:text=Abstract%3A,massive%20and%20rapid%20root%20growth.) has been conducted by NASA which indicates that subjecting plants to varying pressures may lead to shortened germination time, improve the rate of growth of young plants and cause massive root growth. A finding that corroborates this research will be vital for future greenhouse farmers and facilitate faster crop growth, leading to more output for the same parcel of land and this justifies the inclusion and tracking of temperature pressure in this system.




## How - Expected Technical Approach

![Labmodule12_diagram](https://user-images.githubusercontent.com/65710427/232360655-188be1ba-0134-4251-b458-9e732a6a5b93.png)

The system will be divided into two sections, namely the Constrained Device Application (CDA) and the Gateway Device Application (GDA). The purpose of the Constrained Device Application is to handle all interaction with the phyisical sensors and actuators while the Gateway Device Application serves to connect the sensors and actuators to the internet.

The greenhouse monitoring system reference architecture is shown above. The CDA will collect data from three physical sensors. For the temperature and humudity sensors, the HTS221 microcontroller will be used and for pressure, the LPS25H microcontroller will be used. Both of these are manfactured by ST Microelectronics.

The sensors will communicate via an i2c bus to send data to the CDA. The CDA will send a specific request to an individual sensor which will in turn respond with its sensor data. The CDA to be used here is a Raspberry Pi 4B with 2GB RAM. It contains a Broadcom BCM2711 Quad Core Cortex A72 (Arm v8) 64 bit processor that is capable of this operation. In addition to processing sensor data, this Raspberry Pi will also be running a local Mosquitto Broker which services publish and subscribe requests from both the CDA and GDA. The broker has been programmed to carry out client authentication and to listen on port 8883 which is the port designated for MQTT TLS communication. Self signed certificates have been generated and will be used for the purpose of authentication. The CDA will also perform local temperature analysis and send an actuation event to the actuators connected via a digital output pin; in this case a HVAC will be triggered on or off based on the preset threshold values.
The GDA is a HP Pavilion 15 laptop with a Intel Core i7 processor and 16GB of RAM. It will be used to transmit the telemetry generated from the CDA to the cloud as well as perform humidity analysis by sending an actuation if the humidity exceeds a preset maximum or minimum. It will also have the ability to store data locally and the database chosen for this operation is the Redis database. The application layer protocol that is chosen for communicating between the CDA and GDA is MQTT. This will lie on top of TLS on port 8883 and in turn this will be transmitted over IP. The link layer medium chosen here is ethernet and the physical medium being a Cat-6 ethernet patch cable that is capable of transmitting at a rate of 1Gbps.

The GDA will then send data to a Cloud Service Provider. The Cloud Service Provider chosen in this instance is Ubidots. Ubidots is a robust cloud service provider which offers a STEM package that enables access to their hosting services at discounted rates. The medium used to communicate to the Ubidots servers is MQTT over TLS and IP. The GDA will use its Wi-Fi ssetup to transmit data to this cloud. The Ubidots cloud will store data generated by the CDA, as well as track the pressure and send an alarm to the CDA in case the pressure exceeds a certain threshold.


### System Diagram

![block_diagram](https://user-images.githubusercontent.com/65710427/234704655-df7acc64-91cb-462f-94fd-8f234e97d0ba.png)



The application layer communication protocol that is chosen for this design is MQTT. A benefit of MQTT is that the payload can comprise different data types. In this instance, the payload is set to a standardized JSON format. From a security standpoint, the MQTT messages will run over TLS and thus be encrypted which will prevent any man-in-the-middle attacks from sniffing the data. The broker also has client authentication using self signed certificates to guarantee that only authorized clients can participate in the session. The GDA then publishes the data to the Ubidots MQTT broker and this in turn provides storage facilities in order to store our telemetry. In addition to these resources, Ubidots has a web interface where the user can access visualized data from the CDA from any location as well as configure events that will be published back to the GDA and eventually the CDA for actuation. 



### What sensors and actuator did I use?

- CDA Sensor 1: Temperature Sensor (ST HTS221)

- CDA Sensor 2: Humidity Sensor (ST HTS221)

- CDA Sensor 3: Pressure Sensor (ST LPS25H)

- CDA Actuator 1: SenseHAT LED Display



### What CDA protocols and GDA protocols did I implement?

- CDA to GDA Protocol: MQTT via TLS using port 8883

- GDA to CDA Protocol: MQTT via TLS using port 8883

- GDA to Cloud Protocol: MQTT via TLS using port 8883

- Cloud to GDA Protocol: MQTT via TLS using port 8883


 
### What cloud services / capabilities did I use?

- Cloud Service 1 (data ingress - all inputs): GDA Cpu-util, GDA mem-util, CDA Cpu-util, CDA mem-util, humidity sensor data, pressure sensor data, temerature sensor data

- Cloud Service 2 (data egress - all actuation events): LED actuation
- Cloud Service 3 (notificaiton): Alert user once actuation event is triggered



## Screen Shots Representing Cloud Services
1. The Ubidots dashboard 
![Ubidots_dashboard](https://user-images.githubusercontent.com/65710427/234707205-b9193e51-f927-4fd2-90fc-3a43ee2941d0.png)

2. 

### Screen Shots Representing Visualized Data

NOTE: Include (at least) TWO (2) screen shots - one showing at least 1 hour
of time-series data from the CDA, and one showing an event being triggered
that results in an actuation event sent to your GDA and then to your CDA.

1. Email sent notifying user of actuation
![Ubidots_email](https://user-images.githubusercontent.com/65710427/234707339-83589464-9ccd-40a7-86e0-b64813f72de7.png)

2. Time series data for the various parameters
CDA Cpu Util
![cda_cpu_util](https://user-images.githubusercontent.com/65710427/234707559-5f09e037-71d5-434e-a8d1-77d7e169f69d.png)

3. Humidity Sensor Readings
![cda_humidity_sensor](https://user-images.githubusercontent.com/65710427/234707643-d1457ff0-f49c-49fa-8671-87483985e83c.png)

4. LED Actuator Data
![cda_led_actuator](https://user-images.githubusercontent.com/65710427/234707734-0556654c-440b-45ca-a2aa-8232053946c8.png)

5. CDA Mem Util
![cda_mem_util](https://user-images.githubusercontent.com/65710427/234707796-5ed72379-c468-40e3-840c-a03fb9224cad.png)

6. CDA Pressure Sensor
![cda_pressure_sensor](https://user-images.githubusercontent.com/65710427/234707873-e204cc59-b224-4dc5-9b28-adcef2c38349.png)

7. CDA Temperature Sensor
![cda_temp_sensor](https://user-images.githubusercontent.com/65710427/234707946-a0444c02-1118-4425-aa6b-899d77310ac1.png)

8. GDA Cpu Util
![gda_cpu_util](https://user-images.githubusercontent.com/65710427/234708006-22537021-0d38-4e4d-be18-30f7335b1f11.png)

9. GDA Mem Util
![gda_mem_util](https://user-images.githubusercontent.com/65710427/234708073-0034e761-29d1-4e55-b0fc-39309c6bb634.png)

EOF.
