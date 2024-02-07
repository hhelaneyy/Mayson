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
    async def rp(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User, action: str = commands.Param(choices=["Hug / Обнять", "Kiss / Поцеловать", 'Feed / Накормить', "Pat / Погладить", "Slap / Пощёчина", 'Poke / Потыкать', "Punch / Ударить", "Bite / Укусить", "Suck / Отсосать", "Rape / Изнасиловать"], description='Выбор действия над участником.'), ping: str = commands.Param(choices=['Да', 'Нет'], description='Упомянуть участника или нет.')):
        author = inter.author

        if action == 'Feed / Накормить':
            response = requests.get(f"https://tenor.googleapis.com/v2/search?q=anime_feed&key={TENOR_API_KEY}&media_filter=gif&limit=1&random=True")
        elif action == 'Poke / Потыкать':
            response = requests.get(f"https://tenor.googleapis.com/v2/search?q=anime_poke&key={TENOR_API_KEY}&media_filter=gif&limit=1&random=True")            
        else:
            response = requests.get(f"https://tenor.googleapis.com/v2/search?q=anime_{action}&key={TENOR_API_KEY}&media_filter=gif&limit=1&random=True")
        if response.status_code == 200:
            data = response.json()
            gif_url = data['results'][0]['media_formats']['gif']['url']
        else:
            await inter.response.send_message('Произошла ошибка при поиске гиф изображения.')
        
        if user.id == author.id:
            E = disnake.Embed(title='⚠️ Произошла ошибка.', description='Кажется, что пользователь был автором.', color=0xd7e363)
            E.add_field(name='Что же не так?', value=f'```Вы не можете выполнить действие над самим собой.```')
            E.set_footer(text=random.choice(errors), icon_url=self.bot.user.avatar)
            await inter.response.send_message(embed=E, ephemeral=True)
            return

        if action == "Hug / Обнять":
            if ping == 'Нет':
                emb2 = disnake.Embed(title=f"**{author.name} обнял(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(desc_hug), icon_url=author.avatar)
                await inter.send(embed=emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} обнял(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(desc_hug), icon_url=author.avatar)
                await inter.send(user.mention, embed=emb2)

        elif action == 'Feed / Накормить':
            if ping == 'Нет':
                emb2 = disnake.Embed(title=f"**{author.name} накормил(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(descriptions), icon_url=author.avatar)
                await inter.send(embed = emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} накормил(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(descriptions), icon_url=author.avatar)
                await inter.send(user.mention, embed = emb2)

        elif action == 'Poke / Потыкать':
            if author.id == self.bot.owner.id:
                if ping == 'Нет':
                    emb2 = disnake.Embed(title=f"**{author.name} потыкал(а) {user.name}**", color=disnake.Color.random())
                    emb2.set_image(url=gif_url)
                    emb2.set_footer(text=random.choice(descriptions), icon_url=author.avatar)
                    await inter.send(embed = emb2)
                else:
                    emb2 = disnake.Embed(title=f"**{author.name} потыкал(а) {user.name}**", color=disnake.Color.random())
                    emb2.set_image(url=gif_url)
                    emb2.set_footer(text=random.choice(descriptions), icon_url=author.avatar)
                    await inter.send(user.mention, embed = emb2)
            else:
                E = disnake.Embed(title='⚠️ Произошла ошибка', description='Проблемы с выполнением действия над пользователем.', color=disnake.Color.yellow())
                E.add_field(name='Что же не так?', value=f'```Прошу прощения, но данное действие ещё не доступно для пользователей бота. Идёт бета-тестирование действия. Разработчик сообщит на официальном сервере разработки как только действие станет доступно.```')
                E.set_footer(text=random.choice(errors), icon_url=self.bot.user.avatar)
                await inter.response.send_message(embed=E, ephemeral=True)

        elif action == "Kiss / Поцеловать":
            if ping == 'Нет':
                emb2 = disnake.Embed(title=f"**{author.name} поцеловал(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(desc_kiss_ship), icon_url=author.avatar)
                await inter.send(embed = emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} поцеловал(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(desc_kiss_ship), icon_url=author.avatar)
                await inter.send(user.mention, embed = emb2)

        elif action == "Pat / Погладить":
            if ping == 'Нет':
                emb2 = disnake.Embed(title=f"**{author.name} погладил(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(desc_pat), icon_url=author.avatar)
                await inter.send(embed = emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} погладил(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(desc_pat), icon_url=author.avatar)
                await inter.send(user.mention, embed = emb2)

        elif action == "Slap / Пощёчина":
            if ping == 'Нет':
                emb2 = disnake.Embed(title=f"**{author.name} дал(а) пощёчину {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(desc_slap_punch), icon_url=author.avatar)
                await inter.send(embed = emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} дал(а) пощёчину {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(desc_slap_punch), icon_url=author.avatar)
                await inter.send(user.mention, embed = emb2)

        elif action == "Punch / Ударить":
            if ping == 'Нет':
                emb2 = disnake.Embed(title=f"**{author.name} ударил(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(desc_slap_punch), icon_url=author.avatar)
                await inter.send(embed = emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} ударил(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(desc_slap_punch), icon_url=author.avatar)
                await inter.send(user.mention, embed = emb2)

        elif action == "Bite / Укусить":
            if ping == 'Нет':
                emb2 = disnake.Embed(title=f"**{author.name} укусил(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(desc_bite), icon_url=author.avatar)
                await inter.send(embed = emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} укусил(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(desc_bite), icon_url=author.avatar)
                await inter.send(user.mention, embed = emb2)

        elif action == "Feed / Накормить":
            if ping == 'Нет':
                emb2 = disnake.Embed(title=f"**{author.name} накормил(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(desc_feed), icon_url=author.avatar)
                await inter.send(embed = emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} накормил(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(desc_feed), icon_url=author.avatar)
                await inter.send(user.mention, embed = emb2)
            
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
        percantage = randint(0, 101)
        await inter.response.defer()

        if user1.id == 585427658775461909 and user2.id == self.bot.owner.id or user2.id == 585427658775461909 and user1.id == self.bot.owner.id:
            emb4 = disnake.Embed(title="Вместе навсегда 💗💗", description=f"На этой платформе, кажется, нашлась идеальная парочка.", color=disnake.Color.blurple())
            emb4.add_field(name='Результат сведения:', value=f'```{user1.name} и {user2.name} любят друг друга на все 200%.```', inline=False)
            emb4.add_field(name='Совместное имя:', value=f'```{user1.name[:4] + user2.name[-5:]}```')
            emb4.set_footer(text="Обязательно позовите меня на свою свадьбу.", icon_url=inter.bot.user.avatar.url)
            await inter.send(embed = emb4)
            return
        else:
            if percantage > 100:
                emb4 = disnake.Embed(title="Вместе навсегда 💗💗", description=f"На этой платформе, кажется, нашлась идеальная парочка.", color=disnake.Color.blurple())
                emb4.add_field(name='Результат сведения:', value=f'```{user1.name} и {user2.name} любят друг друга на все 200%.```', inline=False)
                emb4.add_field(name='Совместное имя:', value=f'```{user1.name[:4] + user2.name[-5:]}```')
                emb4.set_footer(text="Обязательно позовите меня на свою свадьбу.", icon_url=inter.bot.user.avatar.url)
                await inter.send(embed = emb4)
            elif percantage > 50:
                emb = disnake.Embed(title="Вы чудесная парочка. 🔥", description=f"На этой платформе, кажется, нашлась парочка.", color=disnake.Color.blurple())
                emb.add_field(name='Результат сведения:', value=f'```{user1.name} и {user2.name} любят друг друга на все {percantage}%.```', inline=False)
                emb.add_field(name='Совместное имя:', value=f'```{user1.name[:4] + user2.name[-5:]}```')               
                emb.set_footer(text="Не забудьте сыграть свадьбу и пожалуйста, без беременна в 16.", icon_url=inter.bot.user.avatar.url)
                await inter.send(embed = emb)
            elif percantage == 50:
                emb2 = disnake.Embed(title="Неопределено.", description=f"Кажется, эти люди обычные друзья.", color=disnake.Color.blurple())
                emb2.add_field(name='Результат сведения:', value=f'```{user1.name} и {user2.name} любят друг друга на все {percantage}%.```', inline=False)
                emb2.set_footer(text="Френдзонишь его(-ёё), да?", icon_url=inter.bot.user.avatar.url)
                await inter.send(embed = emb2)
            elif percantage < 50:
                emb2 = disnake.Embed(title="Кхм... 💔", description=f"Кажется, эти люди слегка недолюбливают друг друга...", color=disnake.Color.blurple())
                emb2.add_field(name='Результат сведения:', value=f'```{user1.name} и {user2.name} любят друг друга на все {percantage}%.```', inline=False)
                emb2.set_footer(text="Любви не существует. Среди вас, по крайней мере.", icon_url=inter.bot.user.avatar.url)
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