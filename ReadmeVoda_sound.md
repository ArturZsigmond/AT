# Security Alarm System with Sound Detector

## Overview

This project is a simple **security alarm system** built with **Arduino**.  
It uses a **sound detector (microphone module)** to detect sudden noise.

When the sensor detects sound:
- the **buzzer starts beeping**
- the **LED turns on**

This simulates a basic alarm system that reacts to sound disturbances, such as claps or knocks.

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
![Schematic plan](./images/team_scheme.png)

---

## How It Works

The system constantly reads values from the sound sensor.

- If the detected sound level exceeds a chosen threshold:
  - the **LED lights up**
  - the **buzzer is activated**
- If the environment is quiet:
  - the **LED stays off**
  - the **buzzer stays off**

Note: The sound sensor detects **sudden changes (spikes)** in sound rather than continuous volume.

---

## Schematics Plan

The schematic / circuit plan was created using Circuit Canva

The circuit includes:
- Arduino board
- sound sensor / microphone module
- LED
- buzzer
- resistors
- jumper wires
- breadboard

---

## Pre-requisites / Components

- [ ] Arduino board: `Arduino Uno R3`
- [ ] Sound sensor / microphone module
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
  - a sound sensor
  - an LED
  - a buzzer
- Tested the behavior of the system
- Confirmed that:
  - when sound is detected, the LED turns on
  - when sound is detected, the buzzer starts beeping
- Created a schematic diagram for the circuit

### What we plan to do next
- Improve the design and cable management
- Fine-tune the light sensitivity
- Add more sensors and alarm conditions
- Extend the project with additional sensors (light, proximity, etc.)
- Potentially create a more advanced multi-sensor security alarm system

---
