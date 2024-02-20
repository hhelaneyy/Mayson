import random
import sqlite3
import disnake
from disnake.ext import commands
from disnake.errors import Forbidden
from datetime import datetime
from core.utilities.embeds import errors

class ErrorsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, inter: disnake.ApplicationCommandInteraction, e):
            opp = None
            em = str(e)
            
            if isinstance(e, commands.CommandNotFound):
                return
            elif isinstance(e, commands.CommandInvokeError):
                em = "Задание, которое вы мне дали, невыполнимо с моим количеством полномочий."
                opp = f"Эту задачку будет трудно решить без требуемых команде прав."
            elif isinstance(e, commands.TooManyArguments):
                em = "Задано слишком много аргументов для меня."
                opp = "Кажется, в ваших запросах есть некоторая проблема."
            elif isinstance(e, commands.TooManyArguments):
                em = "Задано слишком много аргументов для меня."
                opp = "Кажется, в ваших зарпросах есть некоторая проблема."
            elif isinstance(e, commands.NotOwner):
                em = "Кажется, вы не работаете в этом отделе."
                opp = "Возникла ошибка из-за отсутствия доступа."
            elif isinstance(e, commands.UserNotFound):
                em = "Пользователь не найден!"
                opp = "А кто указан-то?"
            elif isinstance(e, commands.MissingPermissions):
                em = "У вас недостаточно прав, чтобы использовать эту команду."
                opp = "Возникла ошибка из-за недостатка прав."
            elif isinstance(e, commands.MemberNotFound):
                em = "Пользователь не найден."
                opp = "Произошла ошибка при исполнении команды."
            elif isinstance(e, commands.MissingRequiredArgument):
                ma = str(e.param).split(":")[0]
                command_name = inter.invoked_with
                em = f"Отсутствует недостающий аргумент \"{ma}\", пожалуйста, используйте этот вариант: ⟮ ml.{command_name} {inter.command.signature} ⟯"
                opp = "Произошла ошибка при выполнении команды."
            else:
                em = str(e)
                opp = "Произошла неизвестная ошибка, пожалуйста, сообщите о ней на [сервере технической поддержки.](https://discord.gg/ucJzQTbwQC)"
            if em!="": em=f"```{em}```"
            timestamp = datetime.now()
            m = disnake.Embed(title="<:error:1171436923592638474> Произошла ошибка!", description=opp, color=0xff6969)
            m.add_field(name="От чего все проблемы?", value=f"{em}")
            m.set_footer(text=f"{random.choice(errors)} ∙ {timestamp.strftime(('%d.%m.%Y, %H:%M'))}", icon_url=self.bot.user.avatar.url)
            await inter.send(embed=m)

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter: disnake.ApplicationCommandInteraction, e):
            em = str(e)

            if isinstance(e, commands.NotOwner):
                em = "Кажется, вы не мой разработчик!"
                d = "Произошла ошибка при исполнении команды."
            elif isinstance(e, commands.MissingRequiredArgument):
                ma = str(e.param).split(":")[0]
                command_name = inter.invoked_with
                em = f"Отсутствует недостающий аргумент \"{ma}\", пожалуйста, используйте этот вариант: ⟮ ml.{command_name} {inter.command.signature} ⟯"
                d = "Произошла ошибка при исполнении команды."
            elif isinstance(e, commands.MissingPermissions):
                em = "У вас недостаточно прав, чтобы использовать это!"
                d = "Произошла ошибка при исполнении команды."
            elif isinstance(e, commands.UserNotFound):
                em = "Пользователь не найден!"
                d = "Произошла ошибка при исполнении команды."
            elif isinstance(e, commands.MemberNotFound):
                em = "Пользователь не найден."
                d = "Произошла ошибка при исполнении команды."
            else:
                em = str(e)
                d = "Произошла неизвестная ошибка, пожалуйста, сообщите о ней на [сервере технической поддержки.](https://discord.gg/NzhFk75SnD)"
            if em!="": em=f"```{em}```"
            timestamp = datetime.now()
            m = disnake.Embed(title="<:error:1171436923592638474> Произошла ошибка!", description=d, color=0xff6969)
            m.add_field(name="От чего все проблемы?", value=f"{em}")
            m.set_footer(text=f"{random.choice(errors)} ∙ {timestamp.strftime(('%d.%m.%Y, %H:%M'))}", icon_url=self.bot.user.avatar.url)
            await inter.send(embed=m, ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(ErrorsCog(bot))