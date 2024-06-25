def option():
    prompt=""
    menuOptions={
        "leads": changeLeads,
        "colors": changeColors,
        "subtitle": changeSubtitle,
    }
    while (prompt!="exit"):
        prompt=input().lower()
        try:
            menuOptions.get(prompt)()
        except TypeError:
            print("That does not seem to be a valid option as of this moment. Please try again")


def changeLeads():
    numLeads=int(input("How many leads would you like to show?: "))


def changeSubtitle():
    print("sad")


def changeColors():
    print("sad")

"print(f'{person} is {ages[person]} years old.')"
#Good way of printing stuff out