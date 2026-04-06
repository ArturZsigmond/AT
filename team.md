# Multi-Sensor Security Alarm System (Light, Sound, Proximity)

## Overview

This project is a simple **multi-sensor security alarm system** built with **Arduino**.  
It can operate using different sensors:

- **Light sensor (photoresistor)**
- **Sound sensor (microphone module)**
- **Proximity sensor (infrared obstacle detection module)**

Each version detects disturbances in the environment and triggers an alarm.

When a disturbance is detected:
- the **buzzer starts beeping**
- the **LED turns on**

This simulates a basic alarm system and can be extended into a more advanced intrusion detection system.
---

## Project Variants

The system was implemented in three different configurations:

### 💡 Light-Based Alarm
- Detects changes in ambient light
- Trigger: light level drops below a threshold
- Input: Analog (A0)

### 🎤 Sound-Based Alarm
- Detects sudden sound spikes (claps, noise)
- Trigger: sound value exceeds threshold
- Input: Analog (A1)

### 🚧 Proximity-Based Alarm
- Detects nearby objects
- Trigger: object detected in front of sensor
- Input: Digital (D7)
---

## Demo Video

You can watch the demo video here:

[▶ Watch the demo video](./small_vid.mp4)
## Demo Video

Click the image below to watch the demo on YouTube.

[![Watch the demo](https://img.youtube.com/vi/S0TLke4MMKg/0.jpg)](https://youtu.be/S0TLke4MMKg)
## Project Images

### Real Setup
![Real circuit setup](./images/real-circuit.jpeg)

### Schematic Plan
![Schematic plan](./images/schems.jpeg)

---

## How It Works

The system continuously reads data from the selected sensor.

- If the sensor detects abnormal conditions:
  - the **LED turns on**
  - the **buzzer is activated**
- If conditions are normal:
  - the system remains inactive

Each sensor works differently:

- **Light sensor** → measures light intensity (analog)
- **Sound sensor** → detects sound spikes (analog)
- **Proximity sensor** → detects objects (digital)

All versions use the same alarm logic:
1. Alarm activates (LED + buzzer)
2. After a short duration, the system resets
---

## Schematics Plan

The schematic / circuit plan was created using Circuit Canva

The circuit includes:
- Arduino board
- one of the following sensors:
  - light sensor (photoresistor)
  - sound sensor (microphone module)
  - proximity sensor (infrared obstacle module)
- LED
- buzzer
- resistors
- jumper wires
- breadboard

---

## Pre-requisites / Components

- [ ] Arduino board: `Arduino Uno R3`
- [ ] Sensors:
  - Light sensor / LDR module: `hw-072`
  - Sound sensor / microphone module
  - Proximity sensor / obstacle avoidance module
- [ ] LED: `LTL-307G Led`
- [ ] Buzzer: `Arduino buzzer`
- [ ] Resistor(s): `0.25w 10K Omega resistors`
- [ ] Breadboard: `Basic Breadboard`
- [ ] Jumper wires: `Male to Male wires`

---

## Setup and Build Plan

### What has already been done
- Built the physical circuit on a breadboard
- Connected the Arduino to:
  - one of the sensors (light, sound, or proximity)
  - an LED
  - a buzzer
- Tested the behavior of the system
- Confirmed that:
  - when object is not detected(the door opens) or there is problematic sound or the light is open, the LED turns on
  - when object is not detected(the door opens) or there is problematic sound or the light is open, the buzzer starts beeping
- Created a schematic diagram for the circuit

### What we plan to do next
- Improve the design and cable management
- Fine-tune sensor sensitivity
- Combine multiple sensors into a single system
- Add a desktop or mobile monitoring application
- Extend the project into a full smart security system

---
