# GREENHOUSE PLANS
### Must haves
  1. Ability to lose power, start back up, and continue to run without issue.

### Nice to haves
  1. Closed failure irrigation system
    - solenoid_valve http://www.davidhunt.ie/water-droplet-photography-with-raspberry-pi/
  2. run via API - receives api call from home server/scheduler, executes a task
    - done: Flask with dispatcher
    - can I hook up an email scrape for this too?

### Monitoring
  1. Temp/Humidity Sensor to ensure that we're in expected ranges.
  2. Sun sensor to measure how much sunlight the greenhouse is getting.
    
  3. Picture of the greenhouse captured, uploaded, and deleted.
  4. Soil Sensors to check moisture content
    - https://computers.tutsplus.com/tutorials/build-a-raspberry-pi-moisture-sensor-to-monitor-your-plants--mac-52875

### Watering
  1. Automated drip lines to handle watering
    - Need a solenoid valve (ordered)
    - Need a switching relay to turn on and off the 12v current for the valve (ordered)
    - Need a 12v power supply for solenoid valve (ordered)
      - GPIO drives switching valve, 12v current drives solenoid valve, on/off goes from there.

### Notification System
  1. Daily email summary
  2. Failure SMS notifictions

### Logging
  1. Log files saved for 30 days, then deleted.
