import discord
from discord.ext import commands
from discord import ui

class PointBuyConfigModal(ui.Modal):
    def __init__(self, calculator):
        super().__init__(title="Point Buy Configuration")
        self.calculator = calculator
        
        # Create input fields for all settings
        self.num_stats = ui.TextInput(
            label="Number of Stats",
            placeholder="6",
            default=str(len(self.calculator.stats)),
            max_length=2
        )
        
        self.stat_names_input = ui.TextInput(
            label="Stat Names (comma separated)",
            placeholder="Strength,Dexterity,Constitution,Intelligence,Wisdom,Charisma",
            default=",".join(self.calculator.full_stat_names),
            max_length=300
        )
        
        self.max_points_input = ui.TextInput(
            label="Max Points",
            placeholder="27",
            default=str(self.calculator.max_points),
            max_length=3
        )
        
        self.min_max_stats = ui.TextInput(
            label="Min and Max Stat (format: min,max)",
            placeholder="8,15",
            default=f"{self.calculator.min_stat},{self.calculator.max_stat}",
            max_length=10
        )
        
        self.point_costs_input = ui.TextInput(
            label="Point Costs (format: value:cost,value:cost)",
            placeholder="8:0,9:1,10:2,11:3,12:4,13:5,14:7,15:9",
            default=",".join([f"{k}:{v}" for k, v in self.calculator.point_costs.items()]),
            max_length=500,
            style=discord.TextStyle.paragraph
        )
        
        # Add all inputs to the modal
        self.add_item(self.num_stats)
        self.add_item(self.stat_names_input)
        self.add_item(self.max_points_input)
        self.add_item(self.min_max_stats)
        self.add_item(self.point_costs_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            # Parse number of stats
            num_stats = int(self.num_stats.value)
            if num_stats < 1 or num_stats > 10:
                await interaction.response.send_message("Number of stats must be between 1 and 10!", ephemeral=True)
                return
            
            # Parse stat names
            full_stat_names = [name.strip().title() for name in self.stat_names_input.value.split(",")]
            if len(full_stat_names) != num_stats:
                await interaction.response.send_message(f"You specified {num_stats} stats but provided {len(full_stat_names)} names!", ephemeral=True)
                return
            
            # Generate short names from full names
            stat_names = []
            for name in full_stat_names:
                if len(name) <= 3:
                    stat_names.append(name.upper())
                else:
                    stat_names.append(name[:3].upper())
            
            # Parse max points
            max_points = int(self.max_points_input.value)
            if max_points < 1:
                await interaction.response.send_message("Max points must be positive!", ephemeral=True)
                return
            
            # Parse min/max stats
            min_stat, max_stat = map(int, self.min_max_stats.value.split(","))
            if min_stat >= max_stat:
                await interaction.response.send_message("Min stat must be less than max stat!", ephemeral=True)
                return
            
            # Parse point costs
            point_costs = {}
            for pair in self.point_costs_input.value.split(","):
                value_str, cost_str = pair.split(":")
                value, cost = int(value_str.strip()), int(cost_str.strip())
                point_costs[value] = cost
            
            # Validate point costs cover the range
            for stat_value in range(min_stat, max_stat + 1):
                if stat_value not in point_costs:
                    await interaction.response.send_message(f"Missing point cost for stat value {stat_value}!", ephemeral=True)
                    return
            
            # Update calculator with new settings
            self.calculator.stats = [min_stat] * num_stats
            self.calculator.stat_names = stat_names
            self.calculator.full_stat_names = full_stat_names
            self.calculator.max_points = max_points
            self.calculator.min_stat = min_stat
            self.calculator.max_stat = max_stat
            self.calculator.point_costs = point_costs
            
            # Recreate the view with new settings
            self.calculator.recreate_buttons()
            
            await interaction.response.edit_message(
                content="Configuration updated!",
                embed=self.calculator.create_embed(),
                view=self.calculator
            )
            
        except ValueError as e:
            await interaction.response.send_message(f"ERROR: Invalid input format: {e}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"ERROR: {e}", ephemeral=True)

class PointBuyCalculator(ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        
        # Default D&D 5e settings
        self.stats = [8, 8, 8, 8, 8, 8]
        self.stat_names = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
        self.full_stat_names = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
        self.point_costs = {
            8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5,
            14: 7, 15: 9
        }
        self.max_points = 27
        self.min_stat = 8
        self.max_stat = 15
        
        self.create_buttons()
    
    def get_point_cost(self, value):
        return self.point_costs.get(value, 0)
    
    def calculate_total_cost(self):
        return sum(self.get_point_cost(stat) for stat in self.stats)
    
    def get_remaining_points(self):
        return self.max_points - self.calculate_total_cost()
    
    def can_increase(self, stat_index):
        if self.stats[stat_index] >= self.max_stat:
            return False
        
        current_cost = self.get_point_cost(self.stats[stat_index])
        new_cost = self.get_point_cost(self.stats[stat_index] + 1)
        cost_increase = new_cost - current_cost
        
        return self.get_remaining_points() >= cost_increase
    
    def can_decrease(self, stat_index):
        return self.stats[stat_index] > self.min_stat
    
    def create_embed(self):
        embed = discord.Embed(
            title="Point Buy Calculator",
            description="Interactable Point Buy Calculator",
            color=0x00ff00
        )
        # Add stat fields
        for i, (name, value) in enumerate(zip(self.stat_names, self.stats)):
            cost = self.get_point_cost(value)
            embed.add_field(
                name=f"{name}: {value}",
                value=f"Cost: {cost} pts",
                inline=True
            )
        
        # Add summary
        total_cost = self.calculate_total_cost()
        remaining = self.get_remaining_points()
        
        embed.add_field(
            name="Summary",
            value=f"**Used:** {total_cost}/{self.max_points} points\n**Remaining:** {remaining} points",
            inline=False
        )
        
        # Add current configuration
        embed.add_field(
            name="Configuration",
            value=f"**Stats:** {len(self.stats)}\n**Range:** {self.min_stat}-{self.max_stat}\n**Max Points:** {self.max_points}",
            inline=False
        )
        
        if remaining == 0:
            embed.add_field(
                name="Status", 
                value="**Complete!** All points used.",
                inline=False
            )
        elif remaining < 0:
            embed.add_field(
                name="Status", 
                value="**Over budget!** Reduce some stats.",
                inline=False
            )
        
        return embed
    
    def recreate_buttons(self):
        """Recreate all buttons when configuration changes"""
        self.clear_items()
        self.create_buttons()
    
    def create_buttons(self):
        """Create buttons dynamically based on current configuration"""
        num_stats = len(self.stats)
        
        # Create + buttons (max 5 per row)
        for i in range(num_stats):
            button = ui.Button(
                label=f"{self.stat_names[i]} +",
                style=discord.ButtonStyle.green,
                row=i // 5,
                custom_id=f"inc_{i}"
            )
            button.callback = self.create_increase_callback(i)
            self.add_item(button)
        
        # Create - buttons
        for i in range(num_stats):
            button = ui.Button(
                label=f"{self.stat_names[i]} -",
                style=discord.ButtonStyle.red,
                row=(i // 5) + 2,
                custom_id=f"dec_{i}"
            )
            button.callback = self.create_decrease_callback(i)
            self.add_item(button)
        
        # Utility buttons
        reset_button = ui.Button(label="Reset", style=discord.ButtonStyle.secondary, row=4)
        reset_button.callback = self.reset_stats
        self.add_item(reset_button)
        
        config_button = ui.Button(label="Configure", style=discord.ButtonStyle.secondary, row=4)
        config_button.callback = self.show_config
        self.add_item(config_button)
        
        finalize_button = ui.Button(label="Finalize", style=discord.ButtonStyle.primary, row=4)
        finalize_button.callback = self.finalize_build
        self.add_item(finalize_button)
        
        close_button = ui.Button(label="Close", style=discord.ButtonStyle.danger, row=4)
        close_button.callback = self.close_calculator
        self.add_item(close_button)
    
    def create_increase_callback(self, stat_index):
        async def callback(interaction):
            if self.can_increase(stat_index):
                self.stats[stat_index] += 1
                await interaction.response.edit_message(embed=self.create_embed(), view=self)
            else:
                await interaction.response.send_message(f"ERROR:Cannot increase {self.stat_names[stat_index]} further!", ephemeral=True)
        return callback
    
    def create_decrease_callback(self, stat_index):
        async def callback(interaction):
            if self.can_decrease(stat_index):
                self.stats[stat_index] -= 1
                await interaction.response.edit_message(embed=self.create_embed(), view=self)
            else:
                await interaction.response.send_message(f"ERROR:Cannot decrease {self.stat_names[stat_index]} below {self.min_stat}!", ephemeral=True)
        return callback
    
    async def reset_stats(self, interaction):
        self.stats = [self.min_stat] * len(self.stats)
        await interaction.response.edit_message(embed=self.create_embed(), view=self)
    
    async def show_config(self, interaction):
        modal = PointBuyConfigModal(self)
        await interaction.response.send_modal(modal)
    
    async def finalize_build(self, interaction):
        if self.get_remaining_points() != 0:
            await interaction.response.send_message("ERROR: You must use all points before finalizing!", ephemeral=True)
            return
        
        final_stats = []
        for full_name, value in zip(self.full_stat_names, self.stats):
            final_stats.append(f"{full_name}: {value}")
        
        final_embed = discord.Embed(
            title="Character Build Finalized!",
            description="\n".join(final_stats),
            color=0x00ff00
        )
        final_embed.add_field(name="Total Points Used", value=f"{self.max_points}/{self.max_points}", inline=False)
        
        # Disable all buttons
        for item in self.children:
            item.disabled = True
        
        await interaction.response.edit_message(embed=final_embed, view=self)
    
    async def close_calculator(self, interaction):
        """Close the calculator and clear the message"""
        await interaction.response.edit_message(
            content="Point Buy Calculator closed.",
            embed=None,
            view=None
        )
    
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True