from datetime import datetime
import random
import disnake
from disnake.ext import commands
import sqlite3
from core.utilities.embeds import descriptions, errors

conn = sqlite3.connect('Mayson.db')
cursor = conn.cursor()

class LogsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def get_log_channel(self, guild):
        connection = sqlite3.connect('Mayson.db')
        cursor = connection.cursor()
        cursor.execute('SELECT channel_id FROM logs_channel WHERE guild_id=?', (str(guild.id),))
        result = cursor.fetchone()
        if result:
            channel_id = result[0]
            return guild.get_channel(channel_id)
        return None
        
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        log_channel = self.get_log_channel(before.guild)
        if log_channel:
            if before.author.bot or before.webhook_id:
                return

            if before.content == after.content:
                return
            else:
                embed = disnake.Embed(title="🔖 Изменение сообщения.", description=f"Сервер зафиксировал, что пользователь изменил сообщение.", color=disnake.Color.gold())
                embed.add_field(name="Автор:", value=f'{before.author.mention}')
                embed.add_field(name="Канал:", value=f'{before.channel.mention}')
                embed.add_field(name="Перейти к сообщению", value=f'[Сообщение]({after.jump_url})')
                embed.add_field(name="Первоначальное сообщение:", value=f'```{before.content}```', inline=False)
                embed.add_field(name="Изменено на:", value=f'```{after.content}```', inline=False)
                await log_channel.send(embed=embed)
        else:
            return

    @commands.Cog.listener()
    async def on_message_delete(self, before):
        log_channel = self.get_log_channel(before.guild)
        if log_channel:
            if before.author.bot or before.webhook_id:
                return
            else:
                embed = disnake.Embed(title="🚫 Удаление сообщения.", description=f"Сервер зафиксировал, что пользователь удалил сообщение.", color=disnake.Color.gold())
                embed.add_field(name="Автор:", value=f'{before.author.mention}')
                embed.add_field(name="Канал:", value=f'{before.channel.mention}')
                embed.add_field(name='Контент сообщения:', value=before.content, inline=False)
                await log_channel.send(embed=embed)
        else:
            return
        
    @commands.Cog.listener()
    async def on_member_join(self, user):
        log_channel = self.get_log_channel(user.guild)
        created_at_indicator = f'<t:{int(user.created_at.timestamp())}:F>'
        if log_channel:
            embed = disnake.Embed(title="👤 Новый участник сервера.", description=f"Сервер зафиксировал присоединение нового участника.", color=disnake.Color.gold())
            embed.add_field(name="Никнейм участник:", value=f'{user.mention}')
            embed.add_field(name='Дата регистрации:', value=created_at_indicator)
            embed.set_thumbnail(url=user.avatar)
            embed.set_footer(text=random.choice(descriptions), icon_url=user.guild.icon)

            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        log_channel = self.get_log_channel(member.guild)
        created_at_indicator = f'<t:{int(member.created_at.timestamp())}:F>'
        if log_channel:
            embed = disnake.Embed(title="👤 Участник покинул сервер.", description=f"Сервер зафиксировал, что на одного участника стало меньше.", color=disnake.Color.gold())
            embed.add_field(name="Никнейм участник:", value=f'{member.mention}')
            embed.add_field(name='Дата регистрации:', value=created_at_indicator)
            embed.set_thumbnail(url=member.avatar)
            embed.set_footer(text=random.choice(descriptions), icon_url=member.guild.icon)

            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        log_channel = self.get_log_channel(guild)
        created_at_indicator = f'<t:{int(user.created_at.timestamp())}:F>'
        if log_channel:
            embed = disnake.Embed(title="🛑 Участник заблокирован.", description=f"Сервер зафиксировал, что кто-то был забанен..", color=disnake.Color.gold())
            embed.add_field(name="Никнейм участник:", value=f'{user.mention}')
            embed.add_field(name='Дата регистрации:', value=created_at_indicator)
            embed.add_field(name='Причина:', value='???')
            embed.set_thumbnail(url=user.avatar)
            embed.set_footer(text=random.choice(descriptions), icon_url=guild.icon)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        log_channel = self.get_log_channel(guild)
        created_at_indicator = f'<t:{int(user.created_at.timestamp())}:F>'
        if log_channel:
            embed = disnake.Embed(title="✅ Участник разблокирован.", description=f"Сервер зафиксировал, что кто-то был разбанен.", color=disnake.Color.gold())
            embed.add_field(name="Никнейм участник:", value=f'{user.mention}')
            embed.add_field(name='Дата регистрации:', value=created_at_indicator)
            embed.set_thumbnail(url=user.avatar)
            embed.set_footer(text=random.choice(descriptions), icon_url=guild.icon)
            await log_channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(LogsCog(bot))