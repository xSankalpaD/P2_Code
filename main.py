
import random 

import time

cage_ID= None 
color= None 
size= None
red_bin= False
green_bin= False
blue_bin= False
cageID_list = [1,2,3,4,5,6]

#This function spawns in a random container from a list of predetermined container id's, then removes the selected cage id from the list 
def spawn(): #sean
    global cage_ID
    global cageID_list
    index= random.randint(0, len(cageID_list)-1) #assigns index a random value between 0 and 5, corresponding to the indexes of the list cage ID = cageID_list [index] #selects cage ID from a random number from the cage ID list
    cage_ID= arm.spawn_cage (cage_ID) #spawns the selected cage id
    cageID_list.remove (cageID_list [index]) #removes the cage ID that has already been spawned from the list return None
    return none

#this function picks up the container
def pickup(): #sean
    arm.move_arm (0.574, 0.076, 0.044) #moves arm to pickup location
    time.sleep(2)
    if cage_ID<=3: #conditional to determine the value of final gripper position 
        arm.control_gripper (40)
    elif cage_ID>3: #conditional to determine the value of the final gripper psoition 
        arm.control_gripper (30)
    time.sleep(2)
    arm.move_arm (0.406, 0.0, 0.483) #move arm to the home position
    time.sleep(2)
    return None

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

#This function drops off the container at its specific drop off location
def dropoff(): #sarah
    global size
    global color
    global cage_ID
    global red_bin
    global green_bin
    global blue_bin
    while potentiometer.left() == 0.5:
        time.sleep(1)
    pot_val= potentiometer.left()

    if (pot_val> 0.5): #if left potentiometer value is greater than 50%, place the container in the autoclave drawer 
        size = 'big'

    elif (pot_val< 0.5): #if the left potentiomter value is less than 50%, place the container on top of the autoclave 
        size = 'small'

    if color=='red' and size=='small': #case 1
        arm.move_arm(-0.628,0.254,0.32) #moves arm to predetermined [x, y, z] coordinates

    elif color=='green' and size=='small': #case 2
        arm.move_arm (0.0, -0.600,0.32) #moves arm to predetermined [x, y, z] coordinates

    elif color=='blue' and size=='small': #case 3
        arm.move_arm (0.0,0.600,0.32) #moves arm to predetermined [x, y, z] coordinates
        
    elif color=='red' and size=='big': #case 4
        arm.open_autoclave ('red')
        red_bin = True #assigns the bin a value corresponding to it's drawer position drawer open = true 
        arm.move_arm (-0.404, 0.156, 0.2) #moves arm to predetermined [x, y, z] coordinates

    elif color== 'green' and size== 'big': #case 5
        arm.open_autoclave ('green')
        green_bin= True #assigns the bin a value corresponding to it's drawer position drawer open = true 
        arm.move_arm (0.0, -0.383, 0.15) #moves arm to predetermined [x, y, z] coordinates

    elif color== 'blue' and size== 'big': #case 6
        arm.open_autoclave ('blue')
        blue_bin = True #assigns the bin a value corresponding to it's drawer position drawer open = true 
        arm.move_arm (0.0, 0.389, 0.15) #moves arm to predetermined [x, y, z] coordinates
        
        
    time.sleep(3)

    #once the contianer is dropped off, release the gripper
    if cage_ID<=3:
        arm.control_gripper (-40)
    elif cage_ID>3:
        arm.control_gripper (-30)
    time.sleep(3)
    arm.home()
    
    return None


#this function relates movement of right potentiometer to rotation of the base of the q arm, stopping when within range of the correct autoclave 
def rotate_base(): #sean 
    global cage_ID
    global color
    if cage_ID == 1 or cage_ID == 4: #assigns the selected cage ID a colour
        color= 'red'
    elif cage_ID == 2 or cage_ID == 5: #assigns the selected cage ID a colour 
        color= 'green'
    elif cage_ID == 3 or cage_ID==6: #assigns the selected cage ID a colour
        color= 'blue'
    initial= 0.5 #inital position is when the right potentiometer is at 50%
    while arm.check_autoclave (color) == False: #while the arm is not close to its assigned autoclave drawer, continue rotating the base
        final1= potentiometer. right () #final
        change= float (final1- initial) #assigns change a value equal to the difference between the final and inital potentiometer values 
        angle=change*350 #converts change to an angle
        
        arm.rotate_base (angle) #rotates the arm by predetermiend angle
        initial =final1 #the final position becomes the intial position for when the while loop restarts
    return None

#This function closes the autoclave drawer if the container is big
def close_bin(): #sarah
    global red_bin
    global green_bin
    global blue_bin
    if red_bin == True:
        arm.open_autoclave ('red', False)
        red_bin= False
    elif green_bin == True:
        arm.open_autoclave ('green', False) 
        green_bin= False
    elif blue_bin == True:
        arm.open_autoclave ('blue', False) 
        blue_bin=False
    return None


#This function combines and calls all the functions with breaks inbetween 
def main(): #sarah
    arm.home ()
    for i in range (6): #loop runs for all six contianers
        spawn()
        time.sleep (3)
        pickup()
        time.sleep(3) 
        rotate_base ()
        time.sleep(3)
        dropoff()
        time.sleep(3) 
        close_bin() 
        time.sleep (3) 
        arm.home()

arm.activate_autoclaves () #activates autoclaves
main ()
arm.deactivate_autoclaves () #deactivates the autoclaves


