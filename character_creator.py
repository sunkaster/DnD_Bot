import random

class Character_Creator:
    def __init__(self):
        pass

    def roll_stats_FourDSix(self):
        attributes_to_roll = 6
        dice = 6
        times_to_roll_dice_for_attribute = 4

        map = [[random.randint(1, dice) for cell in range(times_to_roll_dice_for_attribute)] for row in range(attributes_to_roll)]

        for row in map:
            row.sort()
            
        map.sort(key=lambda row: sum(row), reverse=True)

        # Convert to strings for display
        for i in range(len(map)):
            map[i] = [str(x) for x in map[i]]

        total_sum_rows = 0
        map_str = ''
        for row in map:
            highest_values_in_row = [int(row[1]), int(row[2]), int(row[3])]
            used_rolls_string = [str(row[1]), str(row[2]), str(row[3])]
            row_sum = sum(highest_values_in_row)  # Calculate sum for display
            map_str += f'~~( {row[0]} )~~   ' + ' + '.join(used_rolls_string) + f' = {row_sum}\n'
            total_sum_rows += row_sum

        return(map_str, total_sum_rows)
