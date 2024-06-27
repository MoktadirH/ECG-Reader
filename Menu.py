from os.path import exists
import time
import os

#These are the values that are acquired from the file, these should not be changed at all
global_leads=3
maxTime=60000
#Time do not need a second version as it is just a way we see if a chosen max time is valid or not
global_times=1

#These values are copies of the ones above but they can be changed to liking for viewing
global_shownLeads=1
shownMaxTime=1

directory=""

#Colors for required things that are either missing or is complete
statusMissing="\033[91m"
statusComplete="\033[92m"
defaultColor="\033[38;2;255;255;255m"
global_status=statusMissing
global_statusFile=statusMissing




def option():
    prompt=""
    menuOptions={
        "file": getFile,
        "leads": changeLeads,
        "subtitles": changeSubtitle,
        "settings":getInfo,
    }
    while (prompt!="start"):
        print("\033[2J\033[H", end="", flush=True)
        menuPrint()
        prompt=input()
        if(prompt=="start"):
            if((global_status==statusMissing)or(global_statusFile==statusMissing)):
                print("You have not set up some of the required items. Please visit any of the options with the red text until they are all green")
                prompt=""
                time.sleep(2)
                continue
            else:
                continue
        if(prompt in menuOptions):
            menuOptions.get(prompt)()
        else:
            print("That does not seem to be a valid option as of this moment. Please try again")
            time.sleep(2)
#QUALITY OF LIFE FUNCTIONS

#Sets the console to a color and clears it so that the entire console is that color
def setBackground(ansi):
    print(ansi)
    print("\033[2J\033[H", end="", flush=True)




#SETTER AND GETTER FUNCTIONS

def getFile():
    fileExists=False
    while(fileExists==False):
        print("Please type in the directory of the text file or if it is in the same folder as the executable, type in the file name")
        directory=input()
        fileExists=exists(directory)
        if(fileExists):
            print("This file exists and now will be used to run the program!")
            time.sleep(3)
            print("\033[2J\033[H", end="", flush=True)
            global_statusFile=statusComplete
        else:
            print("This file does not exist! Please try again")

def changeLeads():
    validity=False
    while (validity==False):
        numLeads=int(input("How many leads would you like to show?: "))
        if (numLeads>global_leads):
            print("This is not a possible answer, please try again")
        else:
            global_shownLeads=numLeads
            validity=True
            print("\033[2J\033[H", end="", flush=True)

def changeSubtitle():
    global_status=statusComplete
    global_statusFile=statusComplete

def getInfo():
    print("You will now be giving us information about the file so that it can be shown properly. Any mistake in the information will cause the program to crash")
    print("Press enter whenever you are ready to start")
    input()
    print("\033[2J\033[H", end="", flush=True)
    print("How many leads does the file have?: ")
    global_leads=int(input())
    print("\033[2J\033[H", end="", flush=True)
    print("How many Hz is the ECG itself?: ")
    hz=int(input())
    global_times=(1/hz)*1000
    global_status=statusComplete
    time.sleep(2)
    print("\033[2J\033[H", end="", flush=True)
    #Update the color of the menu option to green to show that they have set it up for cool effects

def menuPrint():
    print(defaultColor,"Start\n",global_statusFile,"File\n",defaultColor,"Leads\nSubtitles\n",global_status,"Settings", sep="")
#print(f'{person} is {ages[person]} years old.')
#Good way of printing stuff out