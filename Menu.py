#These are the values that are acquired from the file, these should not be changed at all
leads=1
maxTime=1
#Time do not need a second version as it is just a way we see if a chosen max time is valid or not
time=1

#These values are copies of the ones above but they can be changed to liking for viewing
shownLeads=1
shownMaxTime=1

#Colors for required things that are either missing or is complete
statusMissing="\e[0;31m"
statusComplete="\e[0;32m"
status=statusMissing

def getInfo(lead,hz,max):
    print("You will now be giving us information about the file so that it can be shown properly. Any mistake in the information will cause the program to crash")
    print("Press enter whenever you are ready to start")
    input()
    #flush screen
    print("How many leads does the file have?: ")
    leads=int(input())
    #flush screen
    print("How many Hz is the ECG itself?: ")
    hz=int(input())
    time=(1/hz)*1000
    #Update the color of the menu option to green to show that they have set it up for cool effects


def option():
    prompt=""
    menuOptions={
        "leads": changeLeads,
        "colors": changeColors,
        "subtitle": changeSubtitle,
        "Setup":getInfo,
    }
    while (prompt!="exit"):
        menuPrint()
        prompt=input()
        if(prompt in menuOptions):
            menuOptions.get(prompt)()
        else:
            print("That does not seem to be a valid option as of this moment. Please try again")


def changeLeads():
    validity=False
    while (validity==False):
        numLeads=int(input("How many leads would you like to show?: "))
        if (numLeads>leads):
            print("This is not a possible answer, please try again")
        else:
            shownLeads=numLeads



def changeSubtitle():
    print("sad")


def changeColors():
    print("sad")

def menuPrint():
    print("\u001B[47m Start\nColors\nLeads\nSubtitles\n",status,"Settings")

#print(f'{person} is {ages[person]} years old.')
#Good way of printing stuff out