import random
import disnake
from disnake.ext import commands
from disnake import ui
from typing import List

text = ['📕 Записная книжка Mayson', '🚫 Книга жалоб', '🫗 Пролитый сок']

class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def get_custom_commands(self, ignored_commands='jishaku') -> List[commands.Command]:
        custom_commands = []
        for cog in self.bot.cogs:
            for command in self.bot.get_cog(cog).get_commands():
                if isinstance(command, commands.Command) and command.name not in ignored_commands:
                    custom_commands.append(command)
        return custom_commands

    def get_slash_commands(self, ignored_commands=['reload', 'blacklist', 'user-status', 'global-warn']) -> List[disnake.ApplicationCommand]:
        custom_slash_commands = []
        for cmd in self.bot.slash_commands:
            if cmd.name not in ignored_commands:
                custom_slash_commands.append(cmd)
        return custom_slash_commands

    @commands.command(description="Вызовет это меню.")
    async def help(self, ctx):
        custom_commands = self.get_custom_commands()
        slash_commands = self.get_slash_commands()

        view = HelpView(custom_commands, slash_commands)
        embed = disnake.Embed(title=random.choice(text), description="Здесь, я собрал все доступные команды Mayson и разбил их на две категории. Вы в любое время можете ознакомиться с ними просто прописав команду `mn.help`.", color=disnake.Color.random())
        await ctx.send(embed=embed, view=view)

class HelpView(ui.View):
    def __init__(self, custom_commands, slash_commands):
        super().__init__()
        self.custom_commands = custom_commands
        self.slash_commands = slash_commands

    @ui.button(label="Пользовательские команды", custom_id="custom_commands", style=disnake.ButtonStyle.green)
    async def custom_commands_button(self, button: ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(title="Список пользовательских команд", description="Здесь собраны все команды с префиксом `mn.`", color=disnake.Color.random())
        for cmd in self.custom_commands:
            embed.add_field(name=f"**mn.{cmd.name}**", value=f"{cmd.description}" or "Описание отсутствует")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @ui.button(label="Слэш-команды", custom_id="slash_commands", style=disnake.ButtonStyle.red)
    async def slash_commands_button(self, button: ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(title="Список слэш-команд", description="Здесь собраны все команды с префиксом `/`", color=disnake.Color.random())
        for cmd in self.slash_commands:
            embed.add_field(name=f"**/{cmd.name}**", value=f"{cmd.description}" or "Описание отсутствует")
        await interaction.response.send_message(embed=embed, ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(HelpCog(bot))