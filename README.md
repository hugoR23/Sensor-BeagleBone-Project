# Sensor-BeagleBone-Project
This solution offer the possibility to monitor sensor data extracted via a beagle bone and preview the data and history in a web application.
The project must be pushed onto the Beaglebone with the appropriate sensor card, and on server for the GUI.

## BeagleBone Side
 * Get the sensor data : Temperature, Humidity, Pressure, Luminosity
 * Send the Data to the Server via a protocol established with Twisted framework
 
## Web Server Side
 * Receiving the data from the BeagleBone
 * Rendering the User interface with dynamic graphic using Pyramid framework
