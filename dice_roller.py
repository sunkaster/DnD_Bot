import random

class Dice_Roller:
    def __init__(self):
        self.dice = ""

    def roll_dice(self, dice: str):
        results = []
        input_string = dice.lower().replace(" ", "")
        
        # Split by commas for multiple dice groups
        dice_groups = input_string.split(",")
        
        for dice_group in dice_groups:
            dice_group = dice_group.replace("(", "").replace(")", "")
            
            # Handle multiplier (e.g., (2d6)x3)
            multiplier = 1
            if "x" in dice_group:
                parts = dice_group.split("x")
                if len(parts) == 2 and parts[1].isdigit():
                    multiplier = int(parts[1])
                    dice_group = parts[0]
            
            # Process each multiplier iteration
            for _ in range(multiplier):
                roll_results = []
                group_modifiers = 0
                
                # Parse dice and modifiers using replace method
                dice_group_processed = dice_group.replace("-", "+-")
                parts = [part for part in dice_group_processed.split("+") if part]
                
                for part in parts:
                    is_negative = part.startswith("-")
                    if is_negative:
                        part = part[1:]  # Remove the minus sign
                    
                    if "d" in part:
                        # It's a dice roll
                        try:
                            dice_parts = part.split("d")
                            num_dice = int(dice_parts[0]) if dice_parts[0] else 1
                            dice_sides = int(dice_parts[1])
                            
                            for _ in range(num_dice):
                                roll = random.randint(1, dice_sides)
                                if is_negative:
                                    roll = -roll
                                roll_results.append(roll)
                        except (ValueError, IndexError):
                            print(f"Invalid dice format: {part}")
                    elif part.isdigit():
                        # It's a modifier
                        modifier = int(part)
                        if is_negative:
                            modifier = -modifier
                        group_modifiers += modifier
                
                # Calculate total for this group
                total = sum(roll_results) + group_modifiers
                
                # Format the result string
                dice_rolled_string = f"Dice: {dice_group}"
                if multiplier > 1:
                    dice_rolled_string = f"({dice_group})x{multiplier}"
                
                roll_details = "+".join([str(r) for r in roll_results if r > 0])
                negative_rolls = "".join([str(r) for r in roll_results if r < 0])
                
                if roll_details and negative_rolls:
                    roll_breakdown = f"{roll_details}{negative_rolls}"
                elif roll_details:
                    roll_breakdown = roll_details
                elif negative_rolls:
                    roll_breakdown = negative_rolls
                else:
                    roll_breakdown = "0"
                
                if group_modifiers != 0:
                    if group_modifiers > 0:
                        roll_breakdown += f"+{group_modifiers}"
                    else:
                        roll_breakdown += str(group_modifiers)
                
                results.append(f"{dice_rolled_string} --> {roll_breakdown} = {total}")
        
        return results