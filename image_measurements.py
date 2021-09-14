import sys
import cv2
import numpy as np
import math


def get_contour(image):
    kernel = np.ones((3,3),np.uint8)
    averaging_kernel = np.ones((3,3),np.float32)/9 
    filtered_image = cv2.filter2D(image,-1,kernel) 
    #calculate the edges using Canny edge algorithm
    edged = cv2.Canny(filtered_image,10,10) 
    edged = cv2.dilate(edged, None, iterations=5)
    edged = cv2.erode(edged, None, iterations=5)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    image_n = cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    
    contours_new=[]
    shirt_contour=contours[0] 
    for c in contours:
        area = cv2.contourArea(c)
        if(area>cv2.contourArea(shirt_contour)):
            shirt_contour=c
            contours_new.append(c)
    
    
    max_x=max(shirt_contour[:,0,0])
    min_x=min(shirt_contour[:,0,0])
    max_y=max(shirt_contour[:,0,1])
    min_y=min(shirt_contour[:,0,1])
    
    mid_x=(max_x+min_x)/2
    mid_y=(max_y+min_y)/2
    
    card_dist=2*(max_x-min_x)
    card_contour=contours[0]
    for c in contours:
        area = cv2.contourArea(c)
        if(area<cv2.contourArea(shirt_contour)):
            M = cv2.moments(c)
            if(M!=0):
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
            dist=math.sqrt((cx-mid_x)**2+(cy-mid_y)**2)
            if(dist<card_dist):
                card_dist=dist
                card_contour=c
                
      
    return (card_contour,shirt_contour)     
    
    
    
def card_dim(area):#3(3/8) * 2(1/8)
    conv_base=math.sqrt(area*64/27*17) 
    
    return conv_base    
    
def get_p1p2p6p8(shirt_contour):

    p1_x=1300
    p2_x=0
    p6_x=1300
    p8_x=0
    max_x=max(shirt_contour[:,0,0])
    min_x=min(shirt_contour[:,0,0])
    max_y=max(shirt_contour[:,0,1])
    min_y=min(shirt_contour[:,0,1])
    point_y=min_y+(max_y-min_y)*0.8
    for i in shirt_contour:
        if(p6_x>i[0][0]):
            p6_x=i[0][0]
            p6_y=i[0][1]
            
        if(p8_x<i[0][0]):
            p8_x=i[0][0]
            p8_y=i[0][1]   
    
        if(i[0][1]>point_y):
            if(p1_x>i[0][0]):
                p1_x=i[0][0]
                p1_y=i[0][1]
            
            if(p2_x<i[0][0]):
                p2_x=i[0][0]
                p2_y=i[0][1]            
        #c1_new.append(i)
        #c1_new.append([i[0][0],i[0][1]])
    return(p1_x,p1_y,p2_x,p2_y,p6_x,p6_y,p8_x,p8_y) 


def get_p5p7(shirt_contour,p1_x,p1_y,p2_x,p2_y,p6_x,p6_y,p8_x,p8_y):
    p5_y=0
    p7_y=0

    ref_pl=p6_x+(p1_x-p6_x)*0.5
    ref_pr=p2_x+(p8_x-p2_x)*0.5
    for i in shirt_contour:

    
        if(i[0][0]<ref_pl):
            if(p5_y<i[0][1]):
                p5_x=i[0][0]
                p5_y=i[0][1]
            
        if(i[0][0]>ref_pr):
            if(p7_y<i[0][1]):
                p7_x=i[0][0]
                p7_y=i[0][1]         
            #c1_new.append(i)
        
    return(p5_x,p5_y,p7_x,p7_y)
        
        
def get_p3p4(shirt_contour,p5_x,p5_y,p2_x,p2_y):
    flag=0
    p3_y=700
    p4_y=700
    c2=shirt_contour.reshape(-1,2)
    for e in c2:
        if((e[0]==p5_x) and(e[1]==p5_y)):
            flag=1
        if(flag==1):
            if(p3_y>=e[1]):
                #print(e)
                p3_y=e[1]
                p3_x=e[0]
            else:
                flag=2
            
        if((e[0]==p2_x) and(e[1]==p2_y)):
            flag=3
    
        if(flag==3):
            if(p4_y>e[1]):
                p4_y=e[1]
                p4_x=e[0]
            else:
                flag=2
            
    
    return(p3_x,p3_y,p4_x,p4_y)    
    #print(e)
        
def get_dist(x1,y1,x2,y2):
    return (math.sqrt((x1-x2)**2+(y1-y2)**2))
        
    
def get_measurements(shirt_contour):
    p1_x,p1_y,p2_x,p2_y,p6_x,p6_y,p8_x,p8_y=get_p1p2p6p8(shirt_contour)
    p5_x,p5_y,p7_x,p7_y=get_p5p7(shirt_contour,p1_x,p1_y,p2_x,p2_y,p6_x,p6_y,p8_x,p8_y)
    p3_x,p3_y,p4_x,p4_y=get_p3p4(shirt_contour,p5_x,p5_y,p2_x,p2_y)
    chest= get_dist(p3_x,p3_y,p4_x,p4_y)
    waist= get_dist((p3_x+p1_x)/2,(p3_y+p1_y)/2,(p4_x+p2_x)/2,(p4_y+p2_y)/2)
    hip=dist(p1_x,p1_y,p2_x,p2_y)
    cuffs=(dist(p8_x,p8_y,p7_x,p7_y)+dist(p6_x,p6_y,p5_x,p5_y))/2
    
    #print(p3_x,p3_y,p4_x,p4_y)
    return chest,waist, hip, cuffs
    
    
    
    
    
    

def measure(img_ip):
    #print("Hi", argv[0])
    img=cv2.imread(img_ip)
    image = cv2.GaussianBlur(img, (3, 3), 0) 
    card_contour,shirt_contour=get_contour(image)
    conv_base=card_dim(cv2.contourArea(card_contour))
    chest_base,waist_base,hip_base, cuffs_base=get_measurements(shirt_contour)
    chest=conv_base* chest_base
    waist=waist_base*conv_base
    hip=hip_base*conv_base
    cuffs=cuffs_base*conv_base
    
    return (chest, waist, hip, cuffs)
    
    
    