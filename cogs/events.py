import asyncio
import random
import disnake
from disnake.ext import commands, tasks

class EventsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.status.start()

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