#! /usr/bin/env python3

#This code where I am changing the collision avoider condition by using linear interpolation and working successfully

import matplotlib.pyplot as plt
import numpy as np
import cv2
import math 

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

#AVOID COLLISION
def collision_avoider(gmap,h1,k1,h2,k2):
    r=3
    g= True
    #LINEAR INTERPOLATION
    for i in range(1,20):
        t=i/20
        x=h1*t+h2*(1-t)
        y=k1*t+k2*(1-t)
        if gmap[int(y),int(x)] ==0:                       
            g=False
            print("g is",g)
            break

    return g

#INITIALIZING THE FIRST NODE
def first_node(image,colour_image,x_start,y_start):
    global nodes, parents,parents_dict
    shape=image.shape
    node_init=np.random.randint(0, [shape[1], shape[0]])
    
    if image[node_init[1],node_init[0]] == 254:
        node_x,node_y = point_finder(x_start,y_start,node_init[0],node_init[1],20)
        cv2.line(colour_image,(x_start,y_start),(node_x,node_y),(255,0,0),1)
        cv2.circle(colour_image,(node_x,node_y),3 , (0,0,255), 1)
        node_init_array=np.array([[node_x,node_y]])
        nodes=np.concatenate((nodes, node_init_array), axis=0)
        parents=np.concatenate((parents, np.array([[x_start,y_start]])), axis=0)

    else:
        first_node(image,colour_image,x_start,y_start)

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
    init=np.random.randint([0,0],[404,830])
    return init,h 


def new_node(map,colour_map,n,g_x,g_y):
    global nodes, parents
    i=1
    shape=map.shape
    while i<n+1:
        node,l=initializer(i)        
        x_close,y_close= closest_finder(node[0],node[1])
        if x_close != node[0]: #TO AVOID INFINITE SLOPE
            node_fin_x,node_fin_y=point_finder(x_close,y_close,node[0],node[1],20)
            print("nodes are",node_fin_x,node_fin_y)
            if x_close-node_fin_x!=0:
                if collision_avoider(map,x_close,y_close,node_fin_x,node_fin_y)==True:
                    print("hi")
                    if map[node_fin_y,node_fin_x] ==254: #TO CHECK IF THE POINT IS UNOCCUPIED
                        g_dist=dist_cal(g_x,g_y,node_fin_x,node_fin_y)
                        if g_dist< 25:
                            #TO END THE TREE IF GOAL IS NEARBY
                            cv2.line(colour_map,(g_x,g_y),(node_fin_x,node_fin_y),(255,0,0),1)
                            cv2.circle(colour_map,(node_fin_x,node_fin_y),3 , (0,0,255), 1)
                            cv2.line(colour_map,(x_close,y_close),(node_fin_x,node_fin_y),(255,0,0),1)
                            nodes=np.concatenate((nodes, np.array([[node_fin_x,node_fin_y]])), axis=0)
                            parents=np.concatenate((parents, np.array([[x_close,y_close]])), axis=0)
                            nodes=np.concatenate((nodes, np.array([[g_x,g_y]])), axis=0)
                            parents=np.concatenate((parents, np.array([[node_fin_x,node_fin_y]])), axis=0)
                            print("Hurray goal reached!!!")
                            break
                        else:
                            cv2.circle(colour_map,(node_fin_x,node_fin_y),3 , (0,0,255), 1)
                            cv2.line(colour_map,(x_close,y_close),(node_fin_x,node_fin_y),(255,0,0),1)        
                            node_array=np.array([[node_fin_x,node_fin_y]])
                            nodes=np.concatenate((nodes, node_array), axis=0)
                            parents=np.concatenate((parents, np.array([[x_close,y_close]])), axis=0)
                            i=i+1
def final_path(path_map):
    global nodes,parents,goal_x,goal_y,begin_x,begin_y
    print("shapes",nodes.shape,parents.shape)
    m=goal_x
    n=goal_y
    path=np.array([[m,n]])
    while True:
        j=np.where((nodes[:,0]==m) & (nodes[:,1]==n))
        z=parents[j]
        cv2.circle(path_map,(m,n),3 , (0,0,255), 1)
        cv2.line(path_map,(m,n),(z[0][0],z[0][1]),(255,0,0),1)
        m=z[0][0]
        n=z[0][1]
        print("path is",path)
        path=np.concatenate((path, np.array([[m,n]])), axis=0)
        if (m==begin_x) & (n==begin_y):
            print("break ho gaya")
            cv2.circle(path_map,(m,n),3 , (0,255,0), 1)
            break
 
def main():
    global nodes,parents,goal_x,goal_y,begin_x,begin_y

    #LOADING THE MAP
    img = cv2.imread("/home/sania/catkin_ws/src/Sahayak-v3/sahayak_navigation/src/new_map.pgm")
    img = img[1218:2050,1470:1843]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    colour_img= cv2.imread("/home/sania/catkin_ws/src/Sahayak-v3/sahayak_navigation/src/new_map.pgm")
    colour_img = colour_img[1218:2050,1470:1843]
    path_img=cv2.imread("/home/sania/catkin_ws/src/Sahayak-v3/sahayak_navigation/src/new_map.pgm")
    path_img=path_img[1218:2050,1470:1843]
    
    #START LOCATION
    begin_x=int(input("enter x coordiante of start position:"))
    begin_y=int(input("enter y coordiante of start position:"))
    nodes=np.array([[begin_x,begin_y]])
    cv2.circle(colour_img,(begin_x,begin_y),3 , (0,0,255), 1)

    #GOAL LOCATION
    goal_x=int(input("enter x coordiante of goal position:"))
    goal_y=int(input("enter y coordiante of goal position:"))    
    cv2.circle(colour_img,(goal_x,goal_y),3 , (0,255,0), 1)

    node_list=np.array([[begin_x,begin_y]])
    parents =np.array([[begin_x,begin_y]])
    #INITIALIZING FIRST RANDOM NODE
    first_node(img,colour_img,begin_x,begin_y)
    number=350
    new_node(img,colour_img,number,goal_x,goal_y)
    final_path(path_img)
    Hori = np.concatenate((colour_img,path_img), axis=1)
    cv2.imshow("RRT",Hori)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()
