import random
import disnake
from disnake.ext import commands
import sqlite3
from core.utilities.embeds import descriptions, errors

conn = sqlite3.connect('Mayson.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs_channel (
    guild_id INTEGER PRIMARY KEY,
    channel_id INTEGER
    )
''')

class SettingsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.slash_command(name='settings-logs', description='Настройка канала логов.')
    @commands.has_permissions(administrator=True)
    async def logs(self, inter: disnake.ApplicationCommandInteraction, channel: disnake.TextChannel):
        guild_id = inter.guild.id
        guild_name = inter.guild.name

        if channel:
            cursor.execute('SELECT channel_id FROM logs_channel WHERE guild_id = ?', (guild_id,))
            existing_channel_id = cursor.fetchone()
        
        if existing_channel_id:
            cursor.execute('UPDATE logs_channel SET channel_id = ? WHERE guild_id = ?', (channel.id, guild_id))
            conn.commit()

            titl = '🔄️ Канал логов изменён'
            act = 'Установлен в качестве замены прошлого канала.'
            clr = 0xF2FC58
        else:
            cursor.execute('INSERT INTO logs_channel (guild_id, channel_id) VALUES (?, ?)', (guild_id, channel.id))
            conn.commit()

            titl = '✅ Канал логов установлен'
            act = 'Установлен как новый канал логов.'
            clr = 0x84FE9A

        E = disnake.Embed(title=titl, color=clr)
        E.add_field(name='Название канала:', value=channel.mention)
        E.add_field(name='Действие:', value=act)
        E.set_footer(text=random.choice(descriptions), icon_url=self.bot.user.avatar)
        await inter.response.send_message(embed=E)

def setup(bot: commands.Bot):
    bot.add_cog(SettingsCog(bot))