# Motion-Planning-RRT

## Environment
<p align="center">
<img src="https://user-images.githubusercontent.com/64685403/142732461-619aae52-417f-4a92-95db-b18cb9ffc288.png">
</p>

## Implementations

## 1. RRT Algorithm on a .pgm file
I have implemented the RRT Algorithm on a .pgm file of a 2D occupancy grid map generated using [Hector-SLAM](http://wiki.ros.org/hector_slam)

### To run the code:
* In the file ``` RRT.py``` change the path to the .pgm file of the map in the lines 131,132,133 according to your system. 
* Go to the directory containing ```RRT.py``` file and run the python script using the command ``` python3 RRT.py```

### Results:

<p align="center">
<img src="https://user-images.githubusercontent.com/64685403/142731979-a7d1eb86-4296-4d39-be3b-4cb61d6e01ec.png" width="400">
</p>

<p align="center">
<img src="https://user-images.githubusercontent.com/64685403/142732059-37e6662e-ff12-4ed5-9190-fd74f54d22d8.gif">
</p>

## 2. RRT Algorithm on Sahayak
I have implemented the RRT Algorithm using Sahayak as a base robot.
I have previously worked on it hence I used the same robot as a base to test the algorithm.

### To run the code:
* Build the Sahayak Robot as per the instructions given in [GitHub Repository](https://github.com/IvLabs/Sahayak-v3). 
* Run ```roslaunch sahayak launch_all.launch``` 
* Run ```rosrun sahayak_mapping  odom-pub.py```
* Add the ```RRT_ros.py``` to the sahayak_navigation/src folder
* Run ```rosrun sahayak_navigation RRT_ros.py``` 
* Use ```2D Nav Goal in RVIZ``` to give a goal to Sahayak.


### Results:

<p align="center">
<img src="https://user-images.githubusercontent.com/64685403/142733159-deda4435-384a-4586-85f5-170026f1efe2.png" width="800">
</p>

<p align="center">
<img src="https://user-images.githubusercontent.com/64685403/142733356-b7c60d97-8980-4033-bc37-33b8b41bcc2c.gif" width="600">
</p>



