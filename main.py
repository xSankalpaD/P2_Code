import random

import time


cage_ID = random.randint(1,6) #generate  random container
def pick_up(cage_ID):
    arm.home()
    arm.spawn_cage(cage_ID)
    arm.move_arm(0.574, 0.076, 0.044)
    time.sleep(2)
    if cage_ID< 4:
        arm.control_gripper(40)
    elif cage_ID >3:
        arm.control_gripper(30)
    time.sleep(2)
    arm.move_arm(0.406, 0.0, 0.483)
    time.sleep(2)

def rotate_base(cage_ID):
    check = True
    while check == True:
        coordinate_general= [[-0.379, 0.146, 0.483], [0.0, -0.406, 0.483], [-0.0, 0.383, 0.15]] #general coordinates for where each coordinates
        if potentiometer.right()> 0.5: #if the potentiometer is greater than 50%, rotate it to the right
            position = potentiometer.right() -0.5
            arm.rotate_base(position)
        elif potentiometer.right()<0.5: #if the potentiometer is less than 50%, rotate it to the left 
            position = potentiometer.right()-0.5
            arm.rotate_base(position)
        #If the coordinate of the Q arm is in the range of one of the autoclaves, send the Q arm to the right autoclave
        if cage_ID == 1 or cage_ID == 4 and arm.check_autoclave("red")==True:
            new_coordinate = coordinate_general[0]
            arm.move_arm(new_coordinate[0], new_coordinate[1], new_coordinate[2])
            check = False   #exit the loop
            return True     #return true value so the loop can continue when the function is called the next time
        elif cage_ID == 2 or cage_ID ==5 and arm.check_autoclave("green")==True:
            new_coordinate = coordinate_general[1]
            arm.move_arm(new_coordinate[0], new_coordinate[1], new_coordinate[2])
            check=False     
            return True
        elif cage_ID==3 or cage_ID==6 and arm.check_autoclave("blue")== True:
            new_coordinate = coordinate_general[2]
            arm.move_arm(new_coordinate[0], new_coordinate[1], new_coordinate[2])
            check= False        
            return True 

def drop_off(cage_ID, command, threshold):  #the argument command considers if the autoclave drawer is open or closed
    matchFlag=True 
    while matchFlag==True:
        location_small_autoclaves=[[-0.6022, 0.2433, 0.4393], [0.0, -0.6495, 0.4394], [0.0, 0.6495, 0.4394]] #list of all the coordinates for the small autoclaves
        location_large_autoclaves=[[-0.404, 0.156, 0.2], [0.0, -0.383, 0.15], [0.0, 0.389, 0.15]] #list of all the coordinates for the large autoclaves
        if potentiometer.left() > threshold and potentiometer.left()< 1.0 and cage_ID<4:    #if the left potentiometer is greater than the threshold and less than 100%, find the bin location from the list and move the q arm to the container drop off point
            bin_location= location_small_autoclaves[cage_ID-1]
            arm.move_arm(bin_location[0], bin_location[1], bin_location[2])
            time.sleep(1)
            arm.control_gripper(-30)
            matchFlag= False    #exit the loop
            return True     #return true value so the loop can contirnue when the function is called the next time 
        elif potentiometer.left()==1.0 and command==1 and cage_ID >3:   #if the left potentiometer is 100% and if the drawer needs to be opened, find the drop off point in the list and send the q arm to the location
            bin_location=location_large_autoclaves[cage_ID-4]
            arm.activate_autoclaves()
            time.sleep(3)
            if cage_ID==4:  
                arm.open_autoclave("red")
                arm.move_arm(bin_location[0], bin_location[1], bin_location[2])
                time.sleep(2)
                arm.control_gripper(-30)
                matchFlag= False    
                return True 
            elif cage_ID ==5:
                arm.open_autoclave("green")
                arm.move_arm(bin_location[0], bin_location[1], bin_location[2])
                time.sleep(2)
                arm.control_gripper(-30)
                matchFlag= False    
                return True 
            elif cage_ID==6:
                arm.open_autoclave("blue")
                arm.move_arm(bin_location[0], bin_location[1], bin_location[2])
                time.sleep(2)
                arm.control_gripper(-30)
                matchFlag= False    
                return True 
        elif command ==0:   #if the drawer needs to be closed, command is set to zero
            if cage_ID==4:
                arm.open_autoclave("red", False)
                matchFlag= False
                return True 
            elif cage_ID ==5:
                arm.open_autoclave("green", False)
                matchFlag= False
                return True 
            elif cage_ID ==6:
                arm.open_autoclave("blue", False)
                matchFlag= False
                return True 

def continue_terminate():
    arm.home()
    threshold=0.6 #threshold for the left potentiometer
    for num in range(6): #for the range of 6 autoclave containers, pick up, rotate the q arm base, and drop off the container.
        cage_ID= random.randint(1,6)
        pick_up(cage_ID)
        time.sleep(2)
        rotate_base(cage_ID)
        time.sleep(2)
        drop_off(cage_ID, 1, threshold) 
        time.sleep(2)
        arm.home()
        print("Change potentiometer to 50") #reset the potentiometer so it can be used again
        time.sleep(10)
        if cage_ID>3:
            drop_off(cage_ID, 0, threshold)
            time.sleep(2)
    print("All containers have been sorted")
continue_terminate()
    
