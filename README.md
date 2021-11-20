# Motion-Planning-RRT

## Implementations

## 1. RRT Algorithm on a .pgm file
I have implemented the RRT Algorithm on a .pgm file of a 2D occupancy grid map generated using [Hector-SLAM](http://wiki.ros.org/hector_slam)

### To run the code:
* In the file ``` RRT.py``` change the path to the .pgm file of the map in the lines 131,132,133 according to your system. 
* Go to the directory containing ```RRT.py``` file and run the python script using the command ``` python3 RRT.py```

### Results:

<p align="center">
<img src="https://user-images.githubusercontent.com/64685403/142718492-33ef31c9-fb83-48a5-9385-46633dfa4bb7.png" width="400">
</p>

<p align="center">
<img src="https://user-images.githubusercontent.com/64685403/142722682-fbd967b1-7ea0-46df-8b13-96820912c3db.gif">
</p>

## 2. RRT Algorithm on Sahayak
I have implemented the RRT Algorithm using Sahayak as a base robot.
I have previously worked on this robot hence I used the same robot to test the algorithm.

### To run the code:
* Build the Sahayak Robot as per the instructions given in [GitHub Repository](https://github.com/IvLabs/Sahayak-v3). 
* Run ```roslaunch sahayak launch_all.launch``` 
* Run ```rosrun sahayak_mapping  odom-pub.py```
* Add the ```RRT_ros.py``` to the sahayak_navigation/src folder
* Run ```rosrun sahayak_navigation RRT_ros.py``` 
