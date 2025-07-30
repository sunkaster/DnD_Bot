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
    

    def base_modifier_dice(self, base: int, dice: str):
        self.base = base
        self.dice = 6
        if dice.replace("d", "").isdigit():
            self.dice = int(dice.replace("d", ""))
        dice_values_rolled = []
        for x in range(6):
            dice_values_rolled.append(random.randint(1, self.dice))

        result = []
        stat_total_list = []
        for v in range(5):
            vv = v+1
            row_result = self.base + dice_values_rolled[v] - dice_values_rolled[vv]
            result.append(f"{self.base} + {dice_values_rolled[v]} - {dice_values_rolled[vv]} = {row_result}")
            stat_total_list.append(row_result)
        result.append(f"{self.base} + {dice_values_rolled[5]} - {dice_values_rolled[0]} = {self.base + dice_values_rolled[5] - dice_values_rolled[0]}")
        stat_total_list.append(self.base + dice_values_rolled[5] - dice_values_rolled[0])
        stat_total = sum(stat_total_list)

        return(result, stat_total)