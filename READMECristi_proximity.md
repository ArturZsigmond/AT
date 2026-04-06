# Security Alarm System with Proximity Detector

## Overview

This project is a simple **security alarm system** built with **Arduino**.  
It uses a **proximity sensor (infrared obstacle detection module)** to detect nearby objects.

When the sensor detects an object:
- the **buzzer starts beeping**
- the **LED turns on**

This simulates a basic intrusion detection system.

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

The system constantly reads values from the proximity sensor.

- If an object is detected in front of the sensor:
  - the **LED lights up**
  - the **buzzer is activated**
- If no object is present:
  - the **LED stays off**
  - the **buzzer stays off**

The sensor provides a digital signal:
- LOW (0) → object detected
- HIGH (1) → no object

---

## Schematics Plan

The schematic / circuit plan was created using Circuit Canva

The circuit includes:
- Arduino board
- proximity sensor / obstacle avoidance module
- LED
- buzzer
- resistors
- jumper wires
- breadboard

---

## Pre-requisites / Components

- [ ] Arduino board: `Arduino Uno R3`
- [ ] Proximity sensor / obstacle avoidance module
- [ ] LED: `LTL-307G Led`
- [ ] Buzzer: `Arduino buzzer`
- [ ] Resistor(s): `0.25w 10K Omega resitors * 2`
- [ ] Breadboard: `Basic Breadboard`
- [ ] Jumper wires: `Male to Male wires * 6`

---

## Setup and Build Plan

### What has already been done
- Built the physical circuit on a breadboard
- Connected the Arduino to:
  - a proximity sensor
  - an LED
  - a buzzer
- Tested the behavior of the system
- Confirmed that:
  - when object is not detected(the door opens), the LED turns on
  - when object is not detected(the door opens), the buzzer starts beeping
- Created a schematic diagram for the circuit

### What we plan to do next
- Improve the design and cable management
- Fine-tune the light sensitivity
- Add more sensors and alarm conditions
- Extend the project with a **light detector**
- Potentially create a more advanced multi-sensor security alarm system

---

