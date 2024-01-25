import disnake
from disnake.ext import commands

class EventsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild):
        for channel in guild.text_channels:
            if "чат" in channel.name.lower() or "chat" in channel.name.lower() or 'hang' in channel.name.lower() or 'основной' in channel.name.lower() or '' in channel.name.lower():
                emb = disnake.Embed(title="Привет-привет!", description="Спасибо что пригласили меня на ваш чудесный сервер! Меня зовут Molzy - и я ваша виртуальная ассистентка! Я могу разнообразить ваш сервер весёлыми командами, которые у меня имеются! Используйте `ml.help` чтобы узнать список моих команд и используйте их. Также, меня наделили технологией OpenAI, благодаря чему я могу помогать вам при помощи искуственного интелекта. \nНадеюсь мы с вами станем лучшими друзьями!", color=disnake.Color.blurple())
                emb.set_thumbnail(url=self.bot.user.avatar.url)
                emb.set_footer(text="Начнём же знакомство!", icon_url=self.bot.user.avatar)
                await channel.send(embed=emb)

def setup(bot: commands.Bot):
    bot.add_cog(EventsCog(bot))