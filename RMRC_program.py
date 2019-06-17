
import RPi.GPIO as GPIO
import pickle #Knjiznica za shranjevanje 
from evdev import InputDevice,ecodes
from pyax12.connection import Connection
from time import sleep
#import Function #Lastna knjiznica

#Nastavitve
enable_position_control = 0
enable_position_control = 0
enable_max_min_control = 0



#Programu povemo na katerem USB vmesniku imamo prikljuceno tipkovnico
Gamepad = InputDevice("/dev/input/event4")

#Programu povemo na katerem USB vmesniku imamo prikljuceno tipkovnico
sc=Connection(port="/dev/ttyACM0", baudrate=1000000)

#Prikazemo podatke podane tipkovnice
print(Gamepad)

#GPIO 16 -> Ventilator st.1
#GPIO 20 -> Ventilator st.2
#GPIO 21 -> Ventilator st.3

Output_Pins = [16, 20, 21] #V seznam shranimo nase izhode
Drive_Motors = [1,2,3,4] #Ustvarimo seznam v katerih imamo shranjene pogonske motorje

Number_Of_Gears = 4 #Stevilo prestav
Number_Of_Gears_Tracks = 3 #Stevilo prestav gosenic(premikanje v paralelogramu)


GPIO.setmode(GPIO.BCM)


for i in range(0, len(Output_Pins), 1):
    GPIO.setup(Output_Pins[i], GPIO.OUT, initial = 0)




#Ustvarimo svojo funkcijo, katero bomo uporabili, ko se bodo pojavile napake
def Error_output():

    for i in range(0, len(Output_Pins), 1):
        GPIO.output(Output_Pins[i], 0)

    for i in range(0,len(Drive_Motors), 1):
        sc.set_speed(i, 0)
    sc.close()
    GPIO.cleanup()
    

def Motor_Stop():
    for i in range(0,len(Drive_Motors), 1):
        sc.set_speed(Drive_Motors[i], 0)
    
    
    
    
def Motor_Forward(speed):
    sc.set_speed(1, speed+1023)
    sc.set_speed(2, speed)
    sc.set_speed(3, speed+1023)
    sc.set_speed(4, speed)
    
    

def Motor_Backward(speed):
    sc.set_speed(1, speed)
    sc.set_speed(2, speed+1023)
    sc.set_speed(3, speed)
    sc.set_speed(4, speed+1023)
    
    
    

def Motor_Right(speed):
    sc.set_speed(1, speed)
    sc.set_speed(2, speed)
    sc.set_speed(3, speed)
    sc.set_speed(4, speed)
    

def Motor_Left(speed):
    speed = speed+1023
    sc.set_speed(1, speed)
    sc.set_speed(2, speed)
    sc.set_speed(3, speed)
    sc.set_speed(4, speed)
    

def Right_Tracks(pos,Speed):
    sc.set_ccw_angle_limit(7, 1023, degrees = False)
    sc.set_cw_angle_limit(7, 0, degrees = False)
    sc.goto(7, pos, speed = Speed, degrees = False)
    

def Left_Tracks(pos, Speed):
    sc.set_ccw_angle_limit(5, 1023, degrees = False)
    sc.set_cw_angle_limit(5, 0, degrees = False)
    sc.goto(5, pos, speed = Speed, degrees = False)

def Gripper_Rotation(pos, Speed):
    sc.set_ccw_angle_limit(10, 1023, degrees = False)
    sc.set_cw_angle_limit(10, 0, degrees = False)
    sc.goto(10, pos, speed = Speed, degrees = False)

#Pozicija na zacetku programa
def Beginning_State():
    sc.set_ccw_angle_limit(10, 1023, degrees = False)
    sc.set_cw_angle_limit(10, 0, degrees = False)
    sc.goto(10, 0, speed = 1023, degrees = False)

    #Vklop ventilatorjev
    for i in range(0,len(Output_Pins),1):
        GPIO.output(Output_Pins[i], 1)

def Eight_Joint(pos, Speed):
    sc.set_ccw_angle_limit(8, 1023, degrees = False)
    sc.set_cw_angle_limit(8, 0, degrees = False)
    sc.goto(8, pos, speed = Speed, degrees = False)

def Ninth_Joint(pos, Speed):
    sc.set_ccw_angle_limit(9, 1023, degrees = False)
    sc.set_cw_angle_limit(9, 0, degrees = False)
    sc.goto(9, pos, speed = Speed, degrees = False)
    
        

try:
    
    #Sporocila uporabniku o delovanju robota
    print("")
    print("FUNKCIJA TIPK: ")
    print("")
    print("D-PAD GOR/DOL      ->   Pomik robota NAPREJ / Pomik robota NAZAJ")
    print("D-PAD LEVO/DESNO   ->   Pomik robota LEVO/ Pomik robota DESNO")
    print("Tipka RB/LB        ->   Pomik DESNIH gosenic NAPREJ / Pomik LEVIH gosenic NAPREJ")
    print("Tipka RT           ->   Prestave HITROSTI")
    print("Tipka START        ->   Vklop VENTILATORJEV")

    print("")
    print("DYNAMIXLE AX-18A MOTORJI SO POVEZANI")
    print("")
    #print("NAPETOST BATERIJE: " + str(Voltage) + " V")
    print("")

    
   
    count_0 = 0
    count_1 = 1
    count_2 = 0
    count_3 = 0

    position = 0 #Ukaz za pomik obeh gosenic hkrati
    Count_Speed_Tracks = 1
    index = 1


    Beginning_State()

    Speed = []

    #Napolnimo prazni seznam(array)
    for x in range(0, Number_Of_Gears+1,1):
        Speed.append(x)
    print(Speed)

    #Program za avtomatsko nastavljanje prestav glede na spremenljivko "Number_Of_Gears"
    Speed_Of_First_Gear = int(1023/Number_Of_Gears)

    for i in range(0, Number_Of_Gears+1, 1):
        Speed[i] = (Speed_Of_First_Gear)*i

    print("")
    print("Prestava št: " + str(count_1))
    print("")





    Speed_Tracks = []

    #Napolnimo prazni seznam
    for x in range(0, Number_Of_Gears_Tracks+1,1):
        Speed_Tracks.append(x)
    print(Speed_Tracks)

    Speed_Of_First_Gear_Tracks = int(1023/Number_Of_Gears_Tracks)

    for i in range(0, Number_Of_Gears_Tracks+1, 1):
          Speed_Tracks[i] = (Speed_Of_First_Gear_Tracks)*i


    if(enable_position_control == 1): #V primeru, da smo v nastavitvah nastavili vrednost na 1 se naj zgodi naslednje:
        print("")
        usr_in = int(input("Prosim vpišite št. 1 v primeru, da želite vklopiti pozicioniranje gosenic. "))
        if(usr_in == 1):
            usr_pos_1 = int(input("Ko boste nastavili pozicijo 1, vtipkajte 1. "))
            if(usr_pos_1 == 1):
                pos_1_right = sc.get_present_position(7)
                pos_1_left = sc.get_present_position(5)

                print(str(pos_1_right))
                print(str(pos_1_left))

                usr_pos_2 = int(input("Ko boste nastavili pozicijo 2, vtipkajte 2."))

                if(usr_pos_2 == 2):
                    pos_2_right = sc.get_present_position(7)
                    pos_2_left = sc.get_present_position(5)

                    print(str(pos_2_right))
                    print(str(pos_2_left))

                    usr_pos_3 = int(input("Ko boste nastavili pozicijo 3, vtipkajte 3."))

                    if(usr_pos_3 == 3):
                        pos_3_right = sc.get_present_position(7)
                        pos_3_left = sc.get_present_position(5)

                        print(str(pos_3_right))
                        print(str(pos_3_left))

                        position_tracks = [pos_1_left, pos_1_right, pos_2_left, pos_2_right, pos_3_left, pos_3_right]
                        print(str(position_tracks))

                        #Podatke shranimo v datoteko, da lahko do njih dostopamo 

                        pickle_out = open("pozicija.pickle","wb")
                        pickle.dump(position_tracks, pickle_out)
                        pickle_out.close()


    pickle_in = open("pozicija.pickle","rb")
    position_tracks = pickle.load(pickle_in)

    if(enable_max_min_control == 1):
        print("")
        usr_in = int(input("Prosim vpišite št. 1 v primeru, da želite določiti maksimalno in minimalno vrednost gosenic "))
        if(usr_in == 1):
            usr_pos_max = (input("Ko boste nastavili maksimalno pozicijo, vpišite MAX "))

            if(usr_pos_max == "MAX"):
                pos_1_max = sc.get_present_position(7)
                pos_2_max = sc.get_present_position(5)

                print("Maksimalna pozicija desnih gosenic: " + str(pos_1_max))
                print("Maksimalna pozicija levih gosenic: " + str(pos_2_max))

                print("")
                usr_pos_min = (input("Ko boste nastavili minimalno pozicijo, vpišite MIN "))

                if(usr_pos_min == "MIN"):
                    pos_1_min = sc.get_present_position(7)
                    pos_2_min = sc.get_present_position(5)

                    print("Minimalna pozicija desnih gosenic: " + str(pos_1_min))
                    print("Minimalna pozicija levih gosenic: " + str(pos_2_min))

                    max_min_position_tracks = [pos_1_max, pos_2_max, pos_1_min, pos_2_min]
                    print(str(max_min_position_tracks))

                    pickle_out = open("pozicija_min_max.pickle","wb")
                    pickle.dump( max_min_position_tracks, pickle_out)
                    pickle_out.close()

    pickle_in = open("pozicija_min_max.pickle", "rb")
    max_min_position_tracks = pickle.load(pickle_in)
    print(str(max_min_position_tracks))
    
                

       
    for event in Gamepad.read_loop():

                 #Vklop ventilatorjev s tipko start na Gamepadu
                 #if(event.value == 1 and event.code == 313):
                     #count_0 = count_0+1

                     #if(count_0 == 1):
                         #print("")
                         #print("STANJE VENTILATORJEV: VKLOPLJENI")
                         #print("")
                         #for i in range(0,len(Output_Pins),1):
                             #GPIO.output(Output_Pins[i], 1)

                     #if(count_0 == 2):
                         #print("")
                         #print("STANJE VENTILATORJEV: IZKLOPLJENI")
                         #print("")
                         #for i in range(0,len(Output_Pins),1):
                             #GPIO.output(Output_Pins[i], 0)
                         #count_0 = 0
                 

                

                 #Določanje Prestav, za vsako, ko pritisnemo se prestava mora povečati  
                 if(event.value == 1 and event.code == 311):
                     count_1 = count_1+1
                     if(count_1 == len(Speed)):
                         print("")
                         count_1 = 1
                     print("Prestava št. : " + str(count_1))


                 #Določanje prestav gosenic(premikanje v paralelogramu), vsakič, ko pritisnemo se prestava poveča
                 if(event.value == 1 and event.code == 310):
                     Count_Speed_Tracks = Count_Speed_Tracks+1
                     if(Count_Speed_Tracks == len(Speed_Tracks)):
                         print("")
                         Count_Speed_Tracks = 1
                     print("Prestava št. : " + str(Count_Speed_Tracks))
                    




                 #Pomik robota naprej/nazaj
                 if(event.value == -1 and event.code == 17):
                     Motor_Forward(Speed[count_1])

                 if(event.value == 0 and event.code == 17):
                     Motor_Stop()

                 if(event.value == 1 and event.code == 17):
                     Motor_Backward(Speed[count_1])



                 #Pomik robota desno/levo
                 if(event.value == 1 and event.code == 16):
                     Motor_Right(Speed[count_1])

                 if(event.value == 0 and event.code == 16):
                     Motor_Stop()
                     
                 if(event.value == -1 and event.code == 16):
                     Motor_Left(Speed[count_1])

                
                 #Pomik desnih gosenic v paralelogramu
                 if(event.value == 1 and event.code == 309):
                     Motor_Stop()
                     print("Pomikanje desnih gosenic")
                     pos = sc.get_present_position(7)
                     while(1 == 1):
                         if(pos > 670 and count_2 == 0 or pos < 230 and count_2 == 1):
                             Right_Tracks(pos, 0)
                             break
                         else:
                             if Gamepad.active_keys(309):
                                 if(count_2 == 0):
                                     pos = pos+20
                                     Right_Tracks(pos, 300)
                                 if(count_2 == 1):
                                     pos = pos-20
                                     Right_Tracks(pos, 1023+300)
                                     
                                 
                                 
                                     
                             else:
                                 break

                                 

                             if(event.value == -1 and event.code == 17):
                                     print("OK")    
                 

                 #Spreminjanje smeri vrtenja motorja-> desne gosenice
                 if(event.value == 1 and event.code == 315): 
                     count_2 = count_2+1
                     if(count_2 == 2):
                         count_2 = 0
                     

                 if(event.value == 0 and event.code == 309):
                     print("Prenehanje premikanja gosenic")


                 #Premikanje levih gosenic
                 if(event.value == 1 and event.code == 308):
                     Motor_Stop()
                     print("Pomikanje levih gosenic")
                     pos = sc.get_present_position(5)
                     while(1 == 1):
                         if(pos > 810 and count_3 == 0 or pos < 460 and count_3 == 1):
                             Left_Tracks(pos, 0)
                             break
                         else:
                             if Gamepad.active_keys(308):
                                 if(count_3 == 0):
                                     pos = pos+20
                                     Left_Tracks(pos, 600)
                                 if(count_3 == 1):
                                     pos = pos-20
                                     Left_Tracks(pos, 600)
                             else:
                                 break
                             

                 #Spreminjanje smeri vrtenja motorja -> leve gosenice
                 if(event.value == 1 and event.code == 314):
                     count_3 = count_3 + 1
                     if(count_3 == 2):
                            count_3 = 0
                     
                     
                 if(event.value == 0 and event.code == 308):
                     print("Prenehanje premikanja gosenic")



                 #Premikanje obeh gosenic skupaj
                 if(event.value == 1 and event.code == 312):
                     #position_tracks = [pos_1_left, pos_1_right, pos_2_left, pos_2_right, pos_3_left, pos_3_right]
                     if(index == 1):
                         count_2 = 1
                         index = 0
                     pos_1 = sc.get_present_position(7)
                     pos_2 = sc.get_present_position(5)
                     print(str(pos_2))
                     position = position+1
                     if(position == 3):
                         position = 1

                     print(str(position))

                     if(position == 1):
                         Right_Tracks(position_tracks[1], Speed_Tracks[Count_Speed_Tracks])
                         Left_Tracks(position_tracks[0], Speed_Tracks[Count_Speed_Tracks])

                     if(position == 2 and count_2 == 0):
                         Right_Tracks(position_tracks[3], Speed_Tracks[Count_Speed_Tracks])
                         Left_Tracks(position_tracks[2], Speed_Tracks[Count_Speed_Tracks])

                     if(position == 2 and count_2 == 1):
                         Right_Tracks(position_tracks[5], Speed_Tracks[Count_Speed_Tracks])
                         Left_Tracks(position_tracks[4], Speed_Tracks[Count_Speed_Tracks])

                 if(event.value == 1 and event.code == 305):
                     pos_8 = sc.get_present_position(8)
                     pos_9 = sc.get_present_position(9)
                     while(1 == 1):
                         if Gamepad.active_keys(305):
                             sc.set_speed(0,  400)
                             pos_8 = pos_8-2
                             pos_9 = pos_9+10
                             if(pos_8 < 5):
                                 pos_8 = sc.get_present_position(8)
                             if(pos_9 >= 550):
                                 pos_9 = sc.get_present_position(9)
                             Eight_Joint(pos_8, 1023+1023)
                             Ninth_Joint(pos_9, 1023)
                             
                         else:
                             sc.set_speed(0,0)
                             break
               

                 if(event.value == 1 and event.code == 307):
                     pos_8 = sc.get_present_position(8)
                     pos_9 = sc.get_present_position(9)
                     while(1 == 1):
                         if Gamepad.active_keys(307):
                             sc.set_speed(0, 1023+400)
                             pos_8 = pos_8+2
                             pos_9 = pos_9-10
                             if(pos_9 <= 5):
                                 pos_9 = sc.get_present_position(9)
                             Eight_Joint(pos_8, 1023)
                             Ninth_Joint(pos_9, 1023+1023)
                             
                         else:
                             sc.set_speed(0, 0)
                             break               

                 

                 
                 
                 #Obracanje gripperja za 360 stopinj, ko prvic pritisnemo gre na 360, ko drugic gre na 0 stopinj
                 if(event.value == 1 and event.code == 313):
                     count_0 = count_0+1
                     if(count_0 == 1):
                         Gripper_Rotation(1023, 1023)#Gripper_Rotation(pos, speed)
                         print("Gripper se je obrnil za 360 stopinj!")
                         

                     if(count_0 == 2):
                         Gripper_Rotation(0, 1023)
                         count_0 = 0
                         print("Gripper se je obrnil na 0 stopinj!")


                 if(event.value == 1 and event.code == 304):
                     #pos = sc.get_present_position(8)
                     #print(str(pos))
                     Eight_Joint(0, 200)
                 
                     
                    

                
                     

                     
                         
                     
                     
                

                 
                     
#except Function.VoltageError:
    #print("")
    #print("Prenizka napetost, zamenjajte baterijo!")
    #Error_output()

except ValueError:
    print("")
    print("DYNAMIXLE motorji se niso uspeli povezati, napaka v napajanju ali priklopu motorjev!")
    GPIO.cleanup()


except KeyboardInterrupt: #ctrl+c
    GPIO.cleanup()
