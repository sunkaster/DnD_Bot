import random

class Dice_Roller:
    def __init__(self):
        self.message = ""

    def roll_dice(self, message):
        message = message.strip()
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
            negative_roll_results=[]
            positiveInts = []
            positiveInt = 0
            negativeInts = []
            negativeInt = 0
            negativeRolls=[]
            rolls=[]
            negativeStrings = []
            diceRollMultiplier = 1
            
            if "x" in i:
                diceRollMultiplier = int(i.split("x")[1])
                i = i.split("x")[0].replace("(", "").replace(")", "")
            
            # Parse the expression more carefully
            # Replace - with +- to make splitting easier
            i = i.replace("-", "+-")
            parts = [part for part in i.split("+") if part]  # Remove empty strings

            # Split combined dice inputs into dice piles
            if "+" in i:
                i = i.split("+")
            
            for part in parts:
                if part.startswith("-"):
                    # Negative part
                    part = part[1:]  # Remove the - sign
                    if "d" in part:
                        negativeRolls.append(part)
                    elif part.isdigit():
                        negativeInts.append(-int(part))
                else:
                    # Positive part
                    if "d" in part:
                        rolls.append(part)
                    elif part.isdigit():
                        positiveInts.append(int(part))
                        
        # REMOVE this entire duplicate section (lines 58-71):
        # if isinstance(i, list):
        #     for item in i:
        #         if "d" in item:
        #             rolls.append(item)
        #         elif item.isdigit():
        #             positiveInts.append(int(item))
        # else:
        #     # Handle single string case
        #     if "d" in i:
        #         rolls.append(i)
        #     elif i.isdigit():
        #         positiveInts.append(int(i))
            
            g=0
            while g < diceRollMultiplier:
                g +=1
                if len(negativeRolls) > 0:
                    for negativeRoll in negativeRolls:
                        times_to_roll_negative_dice = int(negativeRoll.split("d")[0])
                        negative_dice = int(negativeRoll.split("d")[1])
                        i=0
                        while i < times_to_roll_negative_dice:
                            i += 1
                            negative_roll_results.append(-random.randint(1, negative_dice))

            g=0
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
            
            if len(positiveInts) > 0:
                positiveInt = sum(positiveInts)
            else:
                positiveInt = 0
            if len(negativeInts) > 0:
                negativeInt = sum(negativeInts)
            else:
                negativeInt = 0

            # Calculate number modifier
            modifierInt = positiveInt + negativeInt

            # Formatting rollsStringer for rollsResults
            rollsStringPositive = "+".join(rolls)
            rollsStringNegative = "-".join(negativeRolls)
            rollsString = f"{rollsStringPositive if rollsStringPositive != '' else ''}{f'-{rollsStringNegative}' if rollsStringNegative != '' else ''}"
            rollsStringer = f"{f'({rollsString})x{diceRollMultiplier}' if diceRollMultiplier != 1 else rollsString}{f'+{modifierInt}' if modifierInt > 0 else ''}{f'{modifierInt}' if modifierInt < 0 else ''}"
            
            # Formatting the rollsResult item for return
            roll_results_strings = list(map(str, roll_results))
            roll_results_string = "+".join(roll_results_strings)
            negative_roll_results_strings = list(map(str, negative_roll_results))
            negative_roll_results_string = "".join(negative_roll_results_strings)
            seperateRollsResult = f"{roll_results_string}{negative_roll_results_string if negative_roll_results_string != '' else ''}"

            result = sum(roll_results) + sum(negative_roll_results) + modifierInt

            # Adding roll(s) to the return list
            rollsResults.append(f"""**Dice Input: **{rollsStringer}
    --> **Dice Rolls:** {seperateRollsResult}(+{modifierInt}) = __**{result}**__""")
            
        # Return all formatted roll(s)
        return(rollsResults) 
