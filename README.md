# Dron ml
This is a system ment to integrate tellopy or any drone api with a ML system developed with Keras & tensorflow.

Is structured as follows:
GUI or user interaction 
AUTONOMOUS_CONTROLLER module to connect to the IA/ML system 
IN gets the video/audio/indicators feed
OUT issues instructions from the GUI or the AUTONOMOUS_CONTROLLER systems.
SAMPLER takes the input from IN and saves it in a classified manner, controlled by the GUI.
ORQUESTRATOR is the main program and has control over all the other systems

# Why?
I have already started this project some time ago to manage the Tello DJI drone from my computer and being able to connect it to a ML system so I want to polish it a little bit and keep going with the investigation.

# Dependencies:
To run this project is necessary to have:
- python3
- av (PyAv)
- opencv
- tellopy
- tensorflow