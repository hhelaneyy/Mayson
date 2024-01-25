import os
import random
import shutil
import typing
import disnake
from disnake import User, Member
from disnake.ext import commands
from datetime import timedelta
from typing import Union
import sqlite3
from core.utilities.embeds import descriptions, errors

conn = sqlite3.connect('Mayson.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS warnings (
                                guild_name TEXT,
                                user_id TEXT,
                                warning_count INTEGER,
                                reason TEXT
                                )''')
conn.commit()

class ModernCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="moderation", description="Модерация всего сервера.")
    @commands.is_owner()
    async def mod(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User | disnake.Member, action: str = commands.Param(choices=["Выдать блокировку пользователю", "Снять блокировку с пользователя", "Выгнать пользователя"]), *, reason = None):
        author = inter.author
        guild = inter.guild

        if action == 'Выдать блокировку пользователю':
            await guild.ban(user, reason=reason)
            wm = disnake.Embed(color=0x740B0B)
            wm.add_field(name="**Сервер:**", value=guild.name)
            wm.add_field(name="    **Администратор:**", value=author.mention)
            wm.add_field(name="    **Нарушитель:**", value=user.name)
            wm.add_field(name="    **Причина выдачи наказания:**", value=f"{reason or 'Причина не указана.'}", inline=False)
            wm.add_field(name="    **Наказание:**", value=action, inline=False)
            wm.set_footer(text="Справедливость восторжествовала!", icon_url=self.bot.user.avatar)
            await inter.response.send_message(embed=wm)

        elif action == "Снять блокировку с пользователя":
            await inter.guild.unban(user)
            wm = disnake.Embed(color=0x740B0B)
            wm.add_field(name="**Сервер:**", value=guild.name)
            wm.add_field(name="    **Администратор:**", value=author.mention)
            wm.add_field(name="    **Пользователь:**", value=user.name)
            wm.add_field(name="    **Действие:**", value=action, inline=False)
            await inter.response.send_message(embed=wm)

        elif action == 'Выгнать пользователя':
            await user.kick(reason=reason)
            wm = disnake.Embed(color=0x740B0B)
            wm.add_field(name="**Сервер:**", value=guild.name)
            wm.add_field(name="    **Администратор:**", value=author.mention)
            wm.add_field(name="    **Пользователь:**", value=user.name)
            wm.add_field(name="    **Действие:**", value=action, inline=False)
            wm.add_field(name="    **Причина:**", value=reason or 'Причина не указана.', inline=False)
            wm.set_footer(text="Надеюсь он не вернётся...", icon_url=self.bot.user.avatar)
            await inter.response.send_message(embed=wm)

    @commands.slash_command(name='timeout', description='Ну что, язык проглотил?')
    @commands.has_permissions(mute_members=True)
    async def mute(self, inter: disnake.ApplicationCommandInteraction, *, user: disnake.Member,  time: int, unit: str = commands.Param(choices=['Минута', 'Час', 'День', 'Неделя']), reason: str = None):
        if unit == 'Минута':
                duration = timedelta(minutes=time)
                unit_name = 'Минут'
        elif unit == 'Час':
                duration = timedelta(hours=time)
                unit_name = 'Часов'
        elif unit == 'День':
                duration = timedelta(days=time)
                unit_name = 'Дней'
        elif unit == 'Неделя':
                duration = timedelta(weeks=time)
                unit_name = 'Недель'
            
        await user.timeout(duration=duration, reason=reason)
        wm = disnake.Embed(color=0x740B0B)
        wm.add_field(name="**Сервер:**", value=inter.guild.name)
        wm.add_field(name="    **Администратор:**", value=inter.author.mention)
        wm.add_field(name="    **Нарушитель:**", value=user.name)
        wm.add_field(name="    **Продолжительность наказания:**", value=f'{time} {unit_name}')
        wm.add_field(name="    **Причина:**", value=f"{reason or 'Причина не указана.'}")
        wm.set_footer(text="Справедливость восторжествовала!", icon_url=self.bot.user.avatar)
        await inter.response.send_message(embed=wm)

        try:
            w = disnake.Embed(title=f'Вы были замьючены на сервере {inter.guild.name}', color=disnake.Color.red())
            w.add_field(name="    **Администратор:**", value=inter.author.mention)
            w.add_field(name="    **Продолжительность наказания:**", value=f'{time} {unit_name}')
            w.add_field(name="    **Причина:**", value=f"{reason or 'Причина не указана.'}")
            await user.send(embed=w)
        except:
            pass

    @commands.slash_command(name='warn', description='Предупреждения.')
    async def warn(self, inter: disnake.ApplicationCommandInteraction, *, user: disnake.User, action: str = commands.Param(choices=['Выдать предупреждение', 'Убрать предупреждение']), count: int = None, reason: str = None):
        if action == 'Убрать предупреждение':
                if count <= 0:
                    m = disnake.Embed(title="⚠️ Произошла ошибка!", description="Кажется, что-то пошло не по плану.", color=0xff6969)
                    m.add_field(name="От чего все проблемы?", value=f"```Вы указали отрицательное значение или ноль.```")
                    m.set_footer(text=random.choice(errors), icon_url=self.bot.user.avatar.url)
                    await inter.response.send_message(embed=m, ephemeral=True)
                    return

                cursor.execute('SELECT warning_count FROM warnings WHERE guild_name = ? AND user_id = ?', (inter.guild.name, user.id))
                row = cursor.fetchone()
                if row:
                    warning_count = row[0]
                else:
                    warning_count = 0

                if warning_count == 0:
                    m1 = disnake.Embed(title="⚠️ Произошла ошибка!", description="Произошла ошибка при исполнении команды.", color=0xff6969)
                    m1.add_field(name="От чего все проблемы?", value=f"```У пользователя нет предупреждений.```")
                    m1.set_footer(text=random.choice(errors), icon_url=self.bot.user.avatar.url)
                    await inter.response.send_message(embed=m1, ephemeral=True)
                    return

                if count >= warning_count:
                    cursor.execute('DELETE FROM warnings WHERE guild_name = ? AND user_id = ?', (inter.guild.name, user.id))
                    conn.commit()
                    embed1 = disnake.Embed(
                            title="✅ Успешно",
                            description=f"У пользователя {user.mention} удалено **{warning_count}** предупреждений(-е; -я).",
                            color=disnake.Color.green()
                        )
                    embed1.set_footer(text=random.choice(descriptions), icon_url=inter.author.avatar)
                    await inter.response.send_message(embed=embed1)
                else:
                    warning_count -= count
                    cursor.execute('UPDATE warnings SET warning_count = ? WHERE guild_name = ? AND user_id = ?', (warning_count, inter.guild.name, user.id))
                    conn.commit()

                    embed = disnake.Embed(
                        title="✅ Успешно",
                        description=f"У пользователя {user.mention} удалено **{count}** предупреждений(-е; -я).",
                        color=disnake.Color.green()
                    )
                    embed.set_footer(text=random.choice(descriptions), icon_url=inter.author.avatar)
                    await inter.response.send_message(embed=embed)

        elif action == "Выдать предупреждение":
                author = inter.author

                cursor.execute('SELECT warning_count FROM warnings WHERE guild_name = ? AND user_id = ?', (inter.guild.name, user.id))
                row = cursor.fetchone()
                if row:
                    warning_count = row[0]
                else:
                    warning_count = 0

                warning_count += 1

                cursor.execute('INSERT INTO warnings VALUES (?, ?, ?, ?)', (inter.guild.name, user.id, warning_count, reason))
                conn.commit()

                wm = disnake.Embed(color=0x740B0B)
                wm.add_field(name="**Сервер:**", value=inter.guild.name)
                wm.add_field(name="    **Администратор:**", value=author.mention)
                wm.add_field(name="    **Нарушитель:**", value=user.name)
                wm.add_field(name="    **Причина предупреждения:**", value=f"{reason or 'Причина не указана.'}", inline=False)
                wm.add_field(name="    **Количество предупреждений:**", value=warning_count, inline=False)
                await inter.send(embed=wm)

    async def get_warning_count(inter: disnake.ApplicationCommandInteraction, user: disnake.User):
        cursor.execute('SELECT warning_count FROM warnings WHERE guild_name = ? AND user_id = ?', (inter.guild.name, user.id))
        row = cursor.fetchone()
        if row:
            warning_count = row[0]
        else:
            warning_count = 'Предупреждений нет.'

    @commands.slash_command(description="Очищу всё до единого!")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        if amount <= 0:
            m1 = disnake.Embed(title="⚠️ Произошла ошибка!", description="Произошла ошибка при исполнении команды.", color=0xff6969)
            m1.add_field(name="От чего все проблемы?", value=f"```Вы указали отрицательное значение или ноль.```")
            m1.set_footer(text=random.choice(errors), icon_url=self.bot.user.avatar.url)
            await ctx.send(embed=m1)
            return
        messages = await ctx.channel.history(limit=amount + 1).flatten()
        messages = [msg for msg in messages if msg.id != ctx.id]
        await ctx.channel.delete_messages(messages)
        
        embed = disnake.Embed(title="✅ Чат очищен!", description=f"Было удалено **{amount}** сообщение(-я; -ий)!", color=0x50c878)
        author = ctx.author
        embed.set_footer(text=f"Спасибо за очистку, {author.name}!", icon_url=author.avatar.url)
        await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(ModernCog(bot))