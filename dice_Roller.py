import random

class Dice_Roller:
    def __init__(self):
        self.message = ""
        self.command = ""

    def roll_dice(self, message, command):
        message = message.replace(f"{command}", "").strip()
        messages = []
        
        rollsResults = []

        if " " in message:
            message = message.replace(" ", "")

        if "," in message:
            messages = message.split(",")
        else:
            messages.append(message)

        for i in messages:
            roll_results=[]
            positiveInt=0
            negativeInt=0
            rolls = []
            negativeString = ""
            messageFormatted = []
            diceRollMultiplier = 1
            g=0
            
            if "x" in i:
                diceRollMultiplier = int(i.split("x")[1])
                i = i.split("x")[0].replace("(", "").replace(")", "")

            if "+" in i:
                if "-" in i:
                    negativeString = i.split("-")[1]
                    if negativeString.isdigit():
                        negativeInt = -int(negativeString)
                    i = i.split("-")[0]
                
                messageFormatted = i.split("+")
                
                for item in messageFormatted:
                    if "d" in item:
                        rolls.append(item)
                    if not "d" in item and item.isdigit():
                        positiveInt = int(item)
                
            elif "-" in i and "+" not in i:
                negativeString = i.split("-")[1]
                messageFormatted = i.split("-")[0]

                if negativeString.isdigit():
                    negativeInt = -int(negativeString)
                if "d" in messageFormatted:
                    rolls.append(messageFormatted)
            else:
                if "d" in i:
                    rolls.append(i)
            
            while g < diceRollMultiplier:
                g +=1
                if len(rolls) > 0:
                    for roll in rolls:
                        times_to_roll_dice = int(roll.split("d")[0])
                        dice = int(roll.split("d")[1])
                        i=0
                        while i < times_to_roll_dice:
                            i += 1
                            roll_results.append(random.randint(1, dice))

            rollsString = "+".join(rolls)
            rollsStringer = f"{rollsString}{f'+{positiveInt}' if positiveInt > 0 else ''}{f'{negativeInt}' if negativeInt < 0 else ''}"
            roll_results_string = list(map(str, roll_results))
            seperateRolls = "+".join(roll_results_string)
            rollsResults.append(f"Dice Input: {rollsStringer}  --->  Dice Rolls: {seperateRolls} == {sum(roll_results) + positiveInt + negativeInt}")
            

        return(rollsResults) 