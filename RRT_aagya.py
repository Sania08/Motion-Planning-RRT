#! /usr/bin/env python3

#This code is fully working code jiska result notion pe dala hai

import matplotlib.pyplot as plt
import numpy as np
import cv2
import math 

parent=[]
def dist_cal(x1,y1,x2,y2):
    dist=abs(math.sqrt(((x1-x2)**2)+((y1-y2)**2)))
    return dist

#TO FIND A POINT THAT IS AT A DISTANCE d FROM THE NODE AND ALONG THE LINEJOINING THE RANDOM POINT AND THE NODE
def point_finder(a1,b1,a2,b2,d): 
    m=(b2-b1)/(a2-a1)
    x1= (d/math.sqrt(1+m**2))+a1
    y1= b1+(d*m/math.sqrt(1+m**2))
    x2= (-d/math.sqrt(1+m**2))+a1
    y2= b1-(d*m/math.sqrt(1+m**2))
    ran_dist=dist_cal(a1,b1,a2,b2)
    d1=dist_cal(a2,b2,x1,y1)
    d2=dist_cal(a2,b2,x2,y2)
    if d1<ran_dist:
        x=x1
        y=y1
    else:
        x=x2
        y=y2
    #print(x,y)
    return int(x),int(y)

def collision_avoider(gmap,h1,k1,h2,k2):
    r=3
    g= True
    for i in range(1,8):
        print("hemlo",r) 
        r=r+1
        point_x,point_y=point_finder(h1,k1,h2,k2,r)
        if gmap[point_y,point_x,0] ==0:
            print("r is",r)
            
            g=False
            print("g is",g)
            break
        
    return g

#INITIALIZING THE FIRST NODE
def first_node(image,x_start,y_start):
    global nodes
    print(image.shape)
    shape=image.shape
    node_init=np.random.randint(0, [shape[1], shape[0]])
    
    if image[node_init[1],node_init[0],0] == 254:
        node_x,node_y = point_finder(x_start,y_start,node_init[0],node_init[1],20)
        cv2.line(image,(x_start,y_start),(node_x,node_y),(255,0,0),1)
        cv2.circle(image,(node_x,node_y),3 , (0,0,255), 1)
        print("white")
        node_init_array=np.array([[node_x,node_y]])
        nodes=np.concatenate((nodes, node_init_array), axis=0)
    else:
        first_node(image,x_start,y_start)

#FIND A NODE IN THE EXISTING TREE WHICH IS CLOSEST TO THE RANDOM POINT
def closest_finder(c,d):
    global nodes
    N_c=np.array([c,d])
    d=nodes-N_c
    d=np.square(d)
    d[:,0]=d[:,0]+d[:,1]
    d0=np.min(d[:,0])
    p=np.where(d[:,0]==d0)
    z=nodes[p]
    return z[0][0],z[0][1]

def initializer(h):
    if h==1 or h%4==1:
        init=np.random.randint(0, [186,403])
        t=1
    if h==2 or h%4==2:
        init=np.random.randint([186,0], [370,403])
        t=2
    if h==3 or h%4==3:
        init=np.random.randint([0,404], [186,830])
        t=3
    if h%4==0:
        init=np.random.randint([186,404], [370,830])
        t=4
    return init,t  

def new_node(map,n,g_x,g_y):
    global nodes, parents
    i=1
    shape=map.shape
    while i<n+1:
        node,l=initializer(i)        
        x_close,y_close= closest_finder(node[0],node[1])
        #print(node[0],node[1])
        if x_close != node[0]: #TO AVOID INFINITE SLOPE
            node_fin_x,node_fin_y=point_finder(x_close,y_close,node[0],node[1],20)
            print("nodes are",node_fin_x,node_fin_y)
            if x_close-node_fin_x!=0:
                if collision_avoider(map,x_close,y_close,node_fin_x,node_fin_y)==True:
                    print("hi")
                    if map[node_fin_y,node_fin_x,0] ==254: #TO CHECK IF THE POINT IS UNOCCUPIED
                        g_dist=dist_cal(g_x,g_y,node_fin_x,node_fin_y)
                        if g_dist< 25:
                            #TO END THE TREE IF GOAL IS NEARBY
                            cv2.line(map,(g_x,g_y),(node_fin_x,node_fin_y),(255,0,0),1)
                            cv2.circle(map,(node_fin_x,node_fin_y),3 , (0,0,255), 1)
                            cv2.line(map,(x_close,y_close),(node_fin_x,node_fin_y),(255,0,0),1)
                            break
                        else:
                            cv2.circle(map,(node_fin_x,node_fin_y),3 , (0,0,255), 1)
                            cv2.line(map,(x_close,y_close),(node_fin_x,node_fin_y),(255,0,0),1)        
                            node_array=np.array([[node_fin_x,node_fin_y]])
                            nodes=np.concatenate((nodes, node_array), axis=0)
                            parents=np.concatenate((parents, np.array([[x_close,y_close]])), axis=0)
                            #print("quad is",l)
                            print(i)
                            i=i+1


def main():
    global nodes
    global parents


    #LOADING THE MAP
    img = cv2.imread("/home/sania/catkin_ws/src/Sahayak-v3/sahayak_navigation/src/new_map.pgm")
    img = img[1218:2050,1470:1843]

    #START LOCATION
    begin_x=284
    begin_y=748
    # begin_x=int(input("enter x coordiante of start"))
    # begin_y=int(input("enter y coordiante of start"))
    nodes=np.array([[begin_x,begin_y]])
    cv2.circle(img,(begin_x,begin_y),3 , (0,0,255), 1)

    #GOAL LOCATION
    goal_x=73
    goal_y=543
    cv2.circle(img,(goal_x,goal_y),3 , (0,255,0), 1)

    node_list=np.array([[begin_x,begin_y]])
    parents =np.array([[begin_x,begin_y]])
    #INITIALIZING FIRST RANDOM NODE
    first_node(img,begin_x,begin_y)
    number=350
    new_node(img,number,goal_x,goal_y)
   
    cv2.imshow("RRT",img)
    cv2.waitKey(1000)
    print("nodes are", nodes)
    print("parents are",parents)
    #cv2.destroyAllWindows()

main()
