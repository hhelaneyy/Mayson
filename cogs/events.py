import asyncio
import random
import sqlite3
import disnake
from disnake.ext import commands, tasks

class EventsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.status.start()

    def is_user_forbidden(self, user_id):
        connection = sqlite3.connect('Mayson.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM forbidden_users WHERE user_id = ?", (user_id,))
        forbidden_user = cursor.fetchone()
        connection.close()
        return forbidden_user is not None
    
    async def check_forbidden_users(self):
        for guild in self.bot.guilds:
            creator_id = guild.owner_id
            if self.is_user_forbidden(creator_id):
                await guild.leave()
    
    async def background_task(self):
        while True:
            await self.check_forbidden_users()
            await asyncio.sleep(3600)

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(self.background_task())

    @commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild):
        audit = guild.system_channel
        owner = guild.owner_id

        if self.is_user_forbidden(owner):
            await guild.leave()
            return
        else:
            E = disnake.Embed(title='🌌 Вот я и прибыл на ваш сервер.', description='Я рад, что вы пригласили меня на вашу вечеринку. Теперь, я стану вашим виртуальным ассистентом, который сможет разнообразить ваш сервер новыми различными командами. Вы также можете использовать `mn.help` чтобы узнать какими командами я обладаю. \n\nЕсли у вас возникнут вопросы во время моего использования, не стесняйтесь задавать их на [официальном сервере разработки и технической поддержки](https://discord.gg/MVWBybpf), мы всегда на связи и готовы помочь вам.', color=0x6b80e7)
            E.set_footer(text='Mayson Hub. Все права были защищены.', icon_url=self.bot.user.avatar)
            await audit.send(embed=E)

    @tasks.loop(seconds=1)
    async def status(self):
        all_members = []
        for guild in self.bot.guilds:
            all_members.extend(guild.members)

        if all_members:
            random_member = random.choice(all_members)
            random_username = random_member.name
            
            await self.bot.change_presence(status=disnake.Status.idle, activity=disnake.Activity(name=f'на {random_username}', type=disnake.ActivityType.watching))
        await asyncio.sleep(15)
        await self.bot.change_presence(status=disnake.Status.idle, activity=disnake.Activity(name="🤨🤨🤨", type=disnake.ActivityType.playing))
        await asyncio.sleep(15)
        await self.bot.change_presence(status=disnake.Status.idle, activity=disnake.Activity(name=f"Poker Night", type=disnake.ActivityType.playing))
        await asyncio.sleep(15)
        await self.bot.change_presence(status=disnake.Status.idle, activity=disnake.Activity(name="SCP-1576.", type=disnake.ActivityType.listening))
        await asyncio.sleep(15)

    @status.before_loop
    async def before_status(self):
        await self.bot.wait_until_ready()

    def cog_unload(self):
        self.status.cancel()

def setup(bot: commands.Bot):
    bot.add_cog(EventsCog(bot))