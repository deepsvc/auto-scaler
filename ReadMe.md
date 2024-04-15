# **Auto-Scaler for CPU Utilization: A ReadMe**

## Introduction

This repo contains a code base for an auto-scaler.
The goal is to dynamically adjust the number of replicas of an application based on observed CPU usage.
The auto-scaler checks for the CPU usage at regular intervals and performs horizontal scaling by controling the number of replicas. The code is capable of scaling the application up or down as needed. The scaling is done with a increment or decrement of 1 replica at a time.
#### Note: The code expects that the application is already running on the default port 8123. If the application is not running, the application will simply print the message `Error fetching CPU utilization. Retrying later.` and continue to try forever. We can add an extra layer of exception handling to avoid this.

### Key Concepts

1. Application Overview:

   - We have an application provided by Vimeo.
   - The application:
     - Starts on a user-defined port (defaulting to 8123).
     - Exposes 2 REST API.
       - `/app/status`: For monitoring CPU usage.
       - `/app/replicas`: For changing the number of replicas.

2. Auto-Scaling Logic:

   - The auto-scaler aims to maintain optimal CPU utilization:
     - When CPU usage is high, we scale up (increase the number of replicas).
     - When CPU usage is low, we scale down (decrease the number of replicas).

3. Implementation Steps:
   - Monitoring CPU Usage:
     - Continuously query the application’s API for CPU utilization (currently set to every 2 seconds).
     - Collect and return data on CPU load over time.
   - Thresholds:
     - Define high and low CPU thresholds (upper: 85% | lower: 75%).
     - Trigger scaling actions based on these thresholds.
   - Scaling Actions:
     - If CPU usage exceeds the high threshold, increase the number of replicas.
     - If CPU usage falls below the low threshold (and replicas > 1), decrease replicas.
     - If CPU usage is within the acceptable range (75 < CPU Usage < 85), do nothing.
   - Error Handling:
     - Handle API errors and print appropriate message.
     - Retry failed requests.

### Possible Enhancements

1. **Robust Error Handling**: We could implement comprehensive error handling to manage API failures, network issues, and unexpected responses.
2. **Logging and Monitoring**: There is a need for a detailed logging to track the auto-scaler’s decisions and actions. We can use monitoring tools to observe the application’s performance over time.
3. **Resource Limits**: We should set resource limits (upper and lower) to prevent over-scaling or under-scaling that could lead to resource exhaustion, increased costs or down time.
4. **Alerting**: Alerting mechanism is required to notify stake holders when critical thresholds are breached or when manual intervention is required.
5. **Tests**: This is a psudeo code with a single method, but in a production environment unit and integration tests are critical for ensuring individual and collective component integrity.
6. We should also introduce a cooldown period after each scaling action to prevent frequent, unnecessary scaling.
