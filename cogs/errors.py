import random
import disnake
from disnake.ext import commands
from datetime import datetime

class ErrorsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    @commands.is_owner()
    async def on_command_error(self, inter: disnake.ApplicationCommandInteraction, e):
            #хули ты взрываешься?
            opp = None
            em = str(e)
            
            if isinstance(e, commands.CommandNotFound):
                return
            elif isinstance(e, commands.BotMissingPermissions):
                em = "Задание, которое вы мне дали, невыполнимо с моим количеством полномочий."
                opp = "Эту задачку будет трудно решить без..."
                a = "Дай, дай админку!"
            elif isinstance(e, commands.TooManyArguments):
                em = "Задано слишком много аргументов для меня."
                opp = "Кажется, в ваших зарпросах есть некоторая проблема."
                a = "Мой мозг... он... lol = {property cogs}"
            elif isinstance(e, commands.NotOwner):
                em = "Кажется, вы не мой разработчик!"
                opp = "Произошла ошибка при исполнении команды."
                a = "Не используй это."
            elif isinstance(e, commands.UserNotFound):
                em = "Пользователь не найден!"
                opp = "Произошла ошибка при исполнении команды."
                a = "Напиши существующего человека))"
            elif isinstance(e, commands.MissingPermissions):
                em = "У вас недостаточно прав, чтобы использовать это!"
                opp = "Произошла ошибка при исполнении команды."
                a = "Вовращайся когда подрастёшь."
            elif isinstance(e, commands.MemberNotFound):
                em = "Пользователь не найден."
                opp = "Произошла ошибка при исполнении команды."
                a = "Напиши существующего человека))"
            elif isinstance(e, commands.MissingRequiredArgument):
                ma = str(e.param).split(":")[0]
                command_name = inter.invoked_with
                em = f"Отсутствует недостающий аргумент \"{ma}\", пожалуйста, используйте этот вариант: ⟮ ml.{command_name} {inter.command.signature} ⟯"
                opp = "Произошла ошибка при выполнении команды."
                a = "Попробуй ещё раз, малыш)"
            else:
                em = str(e)
                opp = "Произошла неизвестная ошибка, пожалуйста, сообщите о ней на [сервере технической поддержки.](https://discord.gg/NzhFk75SnD)"
                a = "Попытаемся исправить в лучшем виде!"
            if em!="": em=f"```{em}```"
            timestamp = datetime.now()
            m = disnake.Embed(title="<:error:1171436923592638474> Произошла ошибка!", description=opp, color=0xff6969)
            m.add_field(name="От чего все проблемы?", value=f"{em}")
            m.set_footer(text=f"{a} ∙ {timestamp.strftime('%d %b %Y')}", icon_url=self.bot.user.avatar.url)
            await inter.send(embed=m)

    @commands.Cog.listener()
    @commands.is_owner()
    async def on_slash_command_error(self, inter: disnake.ApplicationCommandInteraction, e):
            em = str(e)

            if isinstance(e, commands.CommandNotFound):
                pass
            elif isinstance(e, commands.BotMissingPermissions):
                em = "Задание, которое вы мне дали, невыполнимо с моим количеством полномочий."
                d = "Эту задачку будет трудно решить без..."
                a = "Дай, дай админку!"
            elif isinstance(e, commands.TooManyArguments):
                em = "Задано слишком много аргументов для меня."
                d = "Кажется, в ваших зарпросах есть некоторая проблема."
                a = "Мой мозг... он... lol = {property cogs}"
            elif isinstance(e, commands.NotOwner):
                em = "Кажется, вы не мой разработчик!"
                d = "Произошла ошибка при исполнении команды."
                a = "Не используй это."
            elif isinstance(e, commands.MissingRequiredArgument):
                ma = str(e.param).split(":")[0]
                command_name = inter.invoked_with
                em = f"Отсутствует недостающий аргумент \"{ma}\", пожалуйста, используйте этот вариант: ⟮ ml.{command_name} {inter.command.signature} ⟯"
                d = "Произошла ошибка при исполнении команды."
                a = "Ой-ой."
            elif isinstance(e, commands.MissingPermissions):
                em = "У вас недостаточно прав, чтобы использовать это!"
                d = "Произошла ошибка при исполнении команды."
                a = "Вовращайся когда подрастёшь."
            elif isinstance(e, commands.UserNotFound):
                em = "Пользователь не найден!"
                d = "Произошла ошибка при исполнении команды."
                a = "Напиши существующего человека))"
            elif isinstance(e, commands.MemberNotFound):
                em = "Пользователь не найден."
                d = "Произошла ошибка при исполнении команды."
                a = "Напиши существующего человека))"
            elif isinstance(e, commands.NSFWChannelRequired):
                em = "Это можно использовать только в NSFW канале!"
                d = "Произошла ошибка при исполнении команды."
                a = "Ай ты шалунишка))"
            else:
                em = str(e)
                d = "Произошла неизвестная ошибка, пожалуйста, сообщите о ней на [сервере технической поддержки.](https://discord.gg/NzhFk75SnD)"
                a = "Попытаемся исправить в лучшем виде!"
            if em!="": em=f"```{em}```"
            timestamp = datetime.now()
            m = disnake.Embed(title="<:error:1171436923592638474> Произошла ошибка!", description=d, color=0xff6969)
            m.add_field(name="От чего все проблемы?", value=f"{em}")
            m.set_footer(text=f"{a} ∙ {timestamp.strftime('%d %b %Y')}", icon_url=self.bot.user.avatar.url)
            await inter.send(embed=m, ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(ErrorsCog(bot))