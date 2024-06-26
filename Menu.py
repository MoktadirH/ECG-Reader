def option():
    prompt=""
    menuOptions={
        "leads": changeLeads,
        "colors": changeColors,
        "subtitle": changeSubtitle,
    }
    while (prompt!="exit"):
        menuPrint()
        prompt=input()
        if(prompt in menuOptions):
            menuOptions.get(prompt)()
        else:
            print("That does not seem to be a valid option as of this moment. Please try again")


def changeLeads():
    numLeads=int(input("How many leads would you like to show?: "))


def changeSubtitle():
    print("sad")


def changeColors():
    print("sad")

def menuPrint():
    print("\u001B[47m Start\nColors\nLeads\nSubtitles")

#print(f'{person} is {ages[person]} years old.')
#Good way of printing stuff out