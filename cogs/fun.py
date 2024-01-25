from datetime import datetime
import disnake
from disnake import Embed
from disnake.ext import commands
import random
from random import randint
import requests
from core.utilities.embeds import descriptions, errors, img_boobs, img_sucks, desc_suk_boob, desc_bite, desc_hug, desc_kiss_ship, desc_pat, desc_slap_punch, desc_feed, desck_poke

TENOR_API_KEY = 'AIzaSyDIzri_pLPwTV_49BI3sDGcgJPSQ6DD3-g'

class EntertainmentCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.proposals = {}

    @commands.slash_command(description="Реальная жизнь.")
    async def rp(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User, action: str = commands.Param(choices=["Обнять", "Поцеловать", "Погладить", "Потыкать", "Пощёчина", "Ударить", "Укусить", "Накормить", "Отсосать", "Изнасиловать"])):
        author = inter.author
        nsfw_actions = ['Изнасиловать', 'Отсосать']

        response = requests.get(f"https://tenor.googleapis.com/v2/search?q=anime_{action}&key={TENOR_API_KEY}&media_filter=gif&limit=1&random=True")
        if response.status_code == 200:
            data = response.json()
            gif_url = data['results'][0]['media_formats']['gif']['url']
        else:
            await inter.response.send_message('Произошла ошибка при поиске гиф изображения.')

        if action in nsfw_actions and not inter.channel.is_nsfw():
            m = disnake.Embed(title="<:loading:968523760753836092> Произошла ошибка!", description="Что-то пошло не так во время выполнения заданной задачи.", color=0xff6969)
            m.add_field(name="От чего все проблемы?", value=f"```Эту действие доступно только в NSFW канале!```")
            m.set_footer(text=random.choice(errors), icon_url=self.bot.user.avatar.url)
            await inter.response.send_message(embed=m, ephemeral=True)
            return

        if action == "Обнять":
            emb2 = disnake.Embed(title=f"**{author.name} обнял(а) {user.name}**", color=disnake.Color.random())
            emb2.set_image(url=gif_url)
            emb2.set_footer(text=random.choice(desc_hug), icon_url=author.avatar)
            await inter.send(embed=emb2)

        elif action == "Поцеловать":
            emb2 = disnake.Embed(title=f"**{author.name} поцеловал(а) {user.name}**", color=disnake.Color.random())
            emb2.set_image(url=gif_url)
            emb2.set_footer(text=random.choice(desc_kiss_ship), icon_url=author.avatar)
            await inter.send(embed = emb2)

        elif action == "Погладить":
            emb2 = disnake.Embed(title=f"**{author.name} погладил(а) {user.name}**", color=disnake.Color.random())
            emb2.set_image(url=gif_url)
            emb2.set_footer(text=random.choice(desc_pat), icon_url=author.avatar)
            await inter.send(embed = emb2)

        elif action == "Пощёчина":
            emb2 = disnake.Embed(title=f"**{author.name} дал(а) пощёчину {user.name}**", color=disnake.Color.random())
            emb2.set_image(url=gif_url)
            emb2.set_footer(text=random.choice(desc_slap_punch), icon_url=author.avatar)
            await inter.send(embed = emb2)

        elif action == 'Потыкать':
            emb2 = disnake.Embed(title=f"**{author.name} тыкнул(а) {user.name}**", color=disnake.Color.random())
            emb2.set_image(url=gif_url)
            emb2.set_footer(text=random.choice(desck_poke), icon_url=author.avatar)
            await inter.send(embed = emb2)

        elif action == "Ударить":
            emb2 = disnake.Embed(title=f"**{author.name} ударил(а) {user.name}**", color=disnake.Color.random())
            emb2.set_image(url=gif_url)
            emb2.set_footer(text=random.choice(desc_slap_punch), icon_url=author.avatar)
            await inter.send(embed = emb2)

        elif action == "Укусить":
            emb2 = disnake.Embed(title=f"**{author.name} укусил(а) {user.name}**", color=disnake.Color.random())
            emb2.set_image(url=gif_url)
            emb2.set_footer(text=random.choice(desc_bite), icon_url=author.avatar)
            await inter.send(embed = emb2)

        elif action == "Накормить":
            emb2 = disnake.Embed(title=f"**{author.name} накормил(а) {user.name}**", color=disnake.Color.random())
            emb2.set_image(url=gif_url)
            emb2.set_footer(text=random.choice(desc_feed), icon_url=author.avatar)
            await inter.send(embed = emb2)

        elif action == "Отсосать":
            emb2 = disnake.Embed(title=f"**{author.name} отсосал(а) {user.name}**", color=disnake.Color.random())
            emb2.set_image(url=f'{random.choice(img_sucks)}')
            emb2.set_footer(text=random.choice(desc_suk_boob), icon_url=author.avatar)
            await inter.send(embed = emb2)

        elif action == "Изнасиловать":
            if user.id == inter.bot.user.id:
                emb4 = disnake.Embed(title="Что, что?", color=disnake.Color.blurple())
                emb4.add_field(name="Что же не так?", value="```Я бы с радостью поиграл в эротичные игры с вами, но у меня слишком много работы. Извините.```", inline=False)
                emb4.set_footer(text=random.choice(errors), icon_url=inter.bot.user.avatar.url)
                await inter.send(embed = emb4)
                return
            else:
                emb2 = disnake.Embed(title=f"**{author.name} трахнул(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=f'{random.choice(img_boobs)}')
                emb2.set_footer(text=random.choice(desc_suk_boob), icon_url=author.avatar)
                await inter.send(embed = emb2)
            
    @commands.command(description="Покажу все декорации профиля.")
    async def decor(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User = None):
        if user is None:
            user = inter.author

        banner = await self.bot.fetch_user(user.id)
        bann = f' | [Скачать баннер]({banner.banner})'
        ava = f'[Скачать аватар]({user.avatar.url})'
        warn = '[ Аватарка находится справа сверху, а баннер снизу на весь Embed. ]'

        E = Embed(description=f'{ava if user.avatar else ""}{bann if banner.banner else ""} \n\n{warn if banner.banner else ""}', color=disnake.Color.random())
        E.set_author(name=user.name, icon_url=user.avatar.url)

        if user.avatar and banner.banner != None:
            E.set_thumbnail(url=user.avatar)
        else:
            E.set_image(url=user.avatar)

        if banner and banner.banner:
            E.set_image(url=banner.banner.url)
        if banner is None:
            pass

        await inter.send(embed=E)

    @commands.slash_command(name="ship", description="Создай влюблённую парочку.")
    async def ship(self, inter: disnake.ApplicationCommandInteraction, user1: disnake.User, user2: disnake.User):
        percantage = randint(1, 110)
        await inter.response.defer()

        if user1.id == inter.bot.user.id: 
            emb4 = disnake.Embed(title="Что, что?", color=disnake.Color.blurple())
            emb4.add_field(name="Почему команда не сработала?", value="```Ты хочешь меня с кем-то зашиперить? Это конечно мило, но я не думаю что это можно реализовать.```", inline=False)
            emb4.set_footer(text="Давай ты других будешь сводить. У меня много работы.", icon_url=inter.bot.user.avatar.url)
            await inter.send(embed = emb4)
            return
        elif user2.id == inter.bot.user.id:
            emb4 = disnake.Embed(title="Что, что?", color=disnake.Color.blurple())
            emb4.add_field(name="Почему команда не сработала?", value="```Ты хочешь меня с кем-то зашиперить? Это конечно мило, но я не думаю что это можно реализовать.```", inline=False)
            emb4.set_footer(text="Давай ты других будешь сводить. У меня много работы.", icon_url=inter.bot.user.avatar.url)
            await inter.send(embed = emb4)
            return
        else:
            if percantage > 100:
                emb4 = disnake.Embed(title="Вместе навсегда", description=f"**{user1.name}** и **{user2.name}** любят друг друга на **{percantage}%**!!", color=disnake.Color.blurple())
                emb4.set_footer(text="Обязательно позовите меня на свою свадьбу.", icon_url=inter.bot.user.avatar.url)
                await inter.send(embed = emb4)
            if percantage > 55:
                emb = disnake.Embed(title="Вы чудесная парочка. 🔥", description=f"**{user1.name}** и **{user2.name}** любят друг друга на **{percantage}%**!", color=disnake.Color.blurple())
                emb.set_footer(text="", icon_url=inter.bot.user.avatar.url)
                await inter.send(embed = emb)
            if percantage <= 50:
                emb2 = disnake.Embed(title="Кхм... 💔", description=f"**{user1.name}** и **{user2.name}** любят друг друга на **{percantage}%**...", color=disnake.Color.blurple())
                emb2.set_footer(text="Любви не существует...", icon_url=inter.bot.user.avatar.url)
                await inter.send(embed = emb2)
        
    @commands.command(description="Украду эмодзи.")
    @commands.has_permissions(manage_emojis=True)
    async def emoji(self, ctx, emoji: disnake.PartialEmoji, name: str = None):
        guild = ctx.message.guild

        if not guild:
            return
        
        emoji_bytes = await emoji.read()
        emoji_name = name or emoji.name
        
        if any(emoji_name.lower() == existing_emoji.name.lower() for existing_emoji in guild.emojis):
            embed = disnake.Embed(
                title='⚠️ Упс!',
                description='Это имя уже существует на сервере Discord.',
                color=disnake.Color.yellow()
            )
            embed.set_footer(text=random.choice(errors), icon_url=self.bot.user.avatar.url)
            await ctx.send(embed=embed)
            return
        
        new_emoji = await guild.create_custom_emoji(name=emoji_name, image=emoji_bytes)

        embed = disnake.Embed(
            title='✅ Эмодзи добавлен.',
            description=f'Эмодзи {new_emoji} успешно добавлен на сервер с именем: `{emoji_name}`',
            color=disnake.Color.green()
        )
        embed.set_footer(text=random.choice(descriptions), icon_url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)
        
def setup(bot: commands.Bot):
    bot.add_cog(EntertainmentCog(bot))