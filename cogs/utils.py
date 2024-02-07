import asyncio
import random
import disnake
from disnake.ext import commands
from datetime import datetime
import platform
from disnake import ui
from typing import List
import sqlite3
from googletrans import Translator
from core.utilities.embeds import descriptions, errors

conn = sqlite3.connect('Mayson.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users_age (
        user_id INTEGER PRIMARY KEY,
        age INTEGER
    )
''')
conn.commit()

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_cog(UtilsCog(self))

class UtilsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_before_invoke(self, ctx):
        if not hasattr(self.bot, 'start_time'):
            self.bot.start_time = datetime.now()

    @commands.slash_command(name='translator', description='Переводит даже на дотерский!')
    async def trans(self, inter: disnake.ApplicationCommandInteraction, phrase: str, lang):
        await inter.response.defer()
        translator = Translator()
        translation = translator.translate(phrase, dest=lang)
        emb = disnake.Embed(title=f"✅ Перевод выполнен! [ {phrase} ]", description=f"Спасибо, что воспользовались моими услугами переводчика.", color=disnake.Color.random())
        emb.add_field(name='Ваш перевод:', value=f'```{translation.text}```')
        emb.set_footer(text=random.choice(descriptions), icon_url=inter.bot.user.avatar)
        await inter.followup.send(embed = emb)

    @commands.command(name="stats", description='Статистика моя.')
    async def stats(self, inter: disnake.ApplicationCommandInteraction):    
            author = inter.author
            formatted_time = f"<t:{int(self.bot.start_time)}:R>"
            commands = len(inter.bot.commands) + len(inter.bot.slash_commands)
            guilds = len(self.bot.guilds)
            forbidden_users_count = len(self.get_forbidden_users())
            users = len(self.bot.users)

            first_info = (
                f'🕑 | Время работы: __**{formatted_time}**__',
                f"👨🏻‍💻 | Разработчик(и): __**{self.bot.owner.name}**__",
            )

            about_bot = (
                f"🧊 | Язык программирования: __**Python {platform.python_version()}**__",
                f"💽 | Платформа: __**{platform.platform()}**__",
                f'🔄️ | Версия обновления: __**Бета 2.1**__',
                f"🔖 | Статус: __**В разработке...**__",
                f"🏂🏻 | Задержка: __**{round(self.bot.latency * float(1000))}мс.**__",
            )

            other = (
                f"🔥 | Количество команд: __**{commands}**__",
                f'🚫 | Количество пользователей ЧС: __**{forbidden_users_count}**__',
                f"💻 | Количество серверов: __**{guilds}**__",
                f"👤 | Количество пользователей: __**{users}**__",
            )

            emb = disnake.Embed(title="Статистика бота Mayson", url="https://discord.gg/ThpPgFFBHC", color=disnake.Color.random())
            emb.add_field(name="> Основная информация", value='\n'.join(first_info), inline=False)
            emb.add_field(name="> О боте", value= '\n'.join(about_bot), inline=False)
            emb.add_field(name="> Прочее", value='\n'.join(other), inline=False)
            emb.set_thumbnail(url=self.bot.user.avatar.url)
            emb.set_footer(text=random.choice(descriptions), icon_url=author.avatar.url)
            await inter.send(embed=emb)

    @commands.slash_command(name='server', description='Статистика вашего сервера.')
    async def server(self, inter: disnake.ApplicationCommandInteraction):
            guild = inter.guild
            author = inter.author
            rule_channel = guild.rules_channel.mention
            region = inter.guild.preferred_locale
            members = inter.guild.member_count
            mfa_lvl = inter.guild.mfa_level
            verification = inter.guild.verification_level
            max_members = inter.guild.max_members
            roles = len(guild.roles)
            boost_role = inter.guild.premium_subscriber_role
            boosters = guild.premium_subscription_count
            boost_tier = guild.premium_tier
            boost_progress = guild.premium_progress_bar_enabled
            channels = len(guild.channels)
            text_channels = len(guild.text_channels)
            voice_channels = len(guild.voice_channels)
            emojis = len(guild.emojis)
            stikers = len(guild.stickers)

            if boost_progress == False:
                boost_progress = 'Выключен'
            if boost_progress == True:
                boost_progress = 'Включен'

            if mfa_lvl == 0:
                mfa_lvl = "Выключена"
            else:
                mfa_lvl= "Включена"

            about_guild = (
                f'Владелец: **{guild.owner.name}**',
                f'ID сервера: **{guild.id}**',
                f'Регион: **{region}**',
                f'Уровень проверки: **{verification}**',
                f'Двухфакторная Аутентификация: **{mfa_lvl}**',
            )

            roles = (
                f'Ролей: **{roles}**',
                f'Ваша высшая роль: **{author.top_role.mention}**',
                f'Роль поддержавших: **{boost_role.mention if boost_role else "Роль отсутствует."}**',
            )

            channels_and_boosts = (
                f'Прогресс Бар: **{boost_progress}**',
                f'Поддержавших: **{boosters or "Поддерживающих нет."}**',
                f'Уровень поддержки: **{boost_tier}**',
                f'---------------------------------',
                f'Всего каналов: **{channels}**',
                f'Канал правил: **{rule_channel or "Канала правил нет на сервере."}**',
                f'Текстовых каналов: **{text_channels}**',
                f'Голосовых каналов: **{voice_channels}**',
            )

            other = (
                f'Участников: **{members}**',
                f'Стикеры: **{stikers}**',
                f'Эмодзи: **{emojis}**',
                f'Максимальное кол-во участников: **{max_members}**',
                f'Ботов: **{len(([member for member in guild.members if member.bot]))}**',
            )

            emb = disnake.Embed(title=f"Информация о сервере {guild.name}", description=guild.description or 'Описание отсутствует.', color=disnake.Color.random())
            emb.add_field(name="> О сервере:", value='\n'.join(about_guild), inline=False)
            emb.add_field(name="> Роли:", value='\n'.join(roles), inline=False)
            emb.add_field(name="> Каналы и Бусты:", value='\n'.join(channels_and_boosts), inline=False)
            emb.add_field(name="> Прочее:", value='\n'.join(other), inline=False)

            if guild.banner:
                emb.set_image(url=guild.banner)
            else:
                pass
            
            emb.set_thumbnail(url=guild.icon)
            await inter.response.send_message(embed = emb)

    def get_forbidden_users(self):
        connection = sqlite3.connect('Mayson.db')
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM forbidden_users")
        forbidden_users = [row[0] for row in cursor.fetchall()]
        connection.close()
        return forbidden_users
    
    @commands.command(description='Помогу вывести информацию о всех пользователях Discord.')
    async def user(self, ctx, user: disnake.User = None):
        author = ctx.author
        if user is None:
            user = author

        if self.is_user_forbidden(author.id):
            m1 = disnake.Embed(title="⚠️ Произошла ошибка!", description="Я чувствую в вас плохую энергетику.", color=0xff6969)
            m1.add_field(name="Что же не так?", value=f"```Вы не можете использовать команды, т.к находитесь в Чёрном Списке. Если у вас есть вопросы, свяжитесь с {self.bot.owner.name}.```")
            m1.set_footer(text=f"Поддерживается благодаря {self.bot.owner.name}", icon_url=self.bot.owner.avatar.url)
            await ctx.send(embed=m1)
            return
        
        banner = await self.bot.fetch_user(user.id)
        created_at_indicator = f'<t:{int(user.created_at.timestamp())}:F>'

        cursor.execute('SELECT status FROM status WHERE user_id = ?', (user.id,))
        row = cursor.fetchone()
        if row:
            user_status = row[0]
        else:
            user_status = "Пользователь"

        cursor.execute('SELECT warning_count FROM global_warns WHERE user_id = ?', (user.id,))
        row = cursor.fetchone()
        if row:
            gl_count = row[0]
        else:
            gl_count = '0'

        is_forbidden = self.is_user_forbidden(user.id)
        forbidden_status = "Да" if is_forbidden else "Нет"

        all_info = (
            f'**👤  |  Имя пользователя: __{user.name}__**',
            f"**💫  |  ID: __{user.id}__**",
            f'**💥  |  Статус: __{user_status}__**',    
        )

        user_info = (
            f'**🌍  |  Работоспособен: {created_at_indicator}**',
            f'**⚠️  |  Глобальные предупреждения: __{gl_count}__**',
            f'**🚫  |  В черном списке: __{forbidden_status}__**',
        )

        emb = disnake.Embed(color=disnake.Color.random())
        emb.add_field(name="> Общая информация", value='\n'.join(all_info), inline=False)
        emb.add_field(name="> Информация об участнике", value='\n'.join(user_info), inline=False)
        emb.set_author(name=user.name, icon_url=user.avatar)

        if banner and banner.banner:
            emb.set_image(url=banner.banner.url)
        if banner is None:
            return
        
        emb.set_thumbnail(url=user.avatar)
        await ctx.reply(embed=emb)

    @commands.command(description="Информация об участнике сервера.")
    async def profile(self, inter: disnake.ApplicationCommandInteraction, user: disnake.Member | disnake.User = None):
        author = inter.author
        activity = 'Активность отсутствует.'
        if user is None:
            user = inter.author

        if self.is_user_forbidden(author.id):
            m1 = disnake.Embed(title="⚠️ Произошла ошибка!", description="Я чувствую в вас плохую энергетику.", color=0xff6969)
            m1.add_field(name="Что же не так?", value=f"```Вы не можете использовать команды, т.к находитесь в Чёрном Списке. Если у вас есть вопросы, свяжитесь с {self.bot.owner.name}.```")
            m1.set_footer(text=f"Поддерживается благодаря {self.bot.owner.name}", icon_url=self.bot.owner.avatar.url)
            await inter.send(embed=m1)
            return
        
        if user.activity:
            if user.activity.type == disnake.ActivityType.playing:
                activity = f"🎮 Играет в {user.activity.name}"
            elif user.activity.type == disnake.ActivityType.streaming:
                activity = f"📟 Стримит {user.activity.name}"
            elif user.activity.type == disnake.ActivityType.listening:
                activity = f"🎧 Слушает {user.activity.name}"
            elif user.activity.type == disnake.ActivityType.watching:
                activity = f"👁️ Смотрит {user.activity.name}"
            else:
                activity = user.activity
        
        banner = await self.bot.fetch_user(user.id)

        created_at_indicator = f'<t:{int(user.created_at.timestamp())}:F>'
        joined_at_indicator = f'<t:{int(user.joined_at.timestamp())}:F>'

        cursor.execute('SELECT age FROM users_age WHERE user_id = ?', (user.id,))
        row = cursor.fetchone()
        if row:
            age = row[0]
        else:
            age = "Не указан."

        cursor.execute('SELECT status FROM status WHERE user_id = ?', (user.id,))
        row = cursor.fetchone()
        if row:
            user_status = row[0]
        else:
            user_status = "Пользователь"

        cursor.execute('SELECT warning_count FROM warnings WHERE guild_name = ? AND user_id = ?', (inter.guild.name, user.id))
        row = cursor.fetchone()
        if row:
            warning_count = row[0]
        else:
            warning_count = '0'

        cursor.execute('SELECT warning_count FROM global_warns WHERE user_id = ?', (user.id,))
        row = cursor.fetchone()
        if row:
            gl_count = row[0]
        else:
            gl_count = '0'

        is_forbidden = self.is_user_forbidden(user.id)
        forbidden_status = "Да" if is_forbidden else "Нет"

        all_info = (
            f'**👤  |  Имя пользователя: __{user.name}__**',
            f"**💫  |  ID: __{user.id}__**",
            f'**💥  |  Статус: __{user_status}__**',    
        )

        user_info = (
            f'**🌍  |  Работоспособен: {created_at_indicator}**',
            f'**📺  |  Присоединился в: {joined_at_indicator}**',
            f'**🎭  |  Высшая роль: {user.top_role.mention}**',
            f'**⚠️  |  Предупреждения: \n — 🚫 | Глобальные: __{gl_count}__**\n ** —  🔥 | Серверные: __{warning_count}__**',
            f'**🔞  |  Возраст: __{age}__**',
        )

        other_info = (
            f'**🚫  |  В черном списке: __{forbidden_status}__**',
            f'**🧠  |  Аватар: [Открыть]({user.avatar.url})**',
        )

        if banner and banner.banner:
            other_info += (f'**🚩  |  Баннер: [Открыть]({banner.banner.url})**', )

        view = ProfileView(self.bot, inter.author.id)

        if user.id != inter.author.id:
            view.children = []

            view.bot = self.bot

        emb = disnake.Embed(description=activity, color=disnake.Color.random())
        emb.add_field(name="> Общая информация", value='\n'.join(all_info), inline=False)
        emb.add_field(name="> Информация об участнике", value='\n'.join(user_info), inline=False)
        emb.add_field(name="> Прочая информация", value='\n'.join(other_info), inline=False)
        emb.set_author(name=user.name, icon_url=user.avatar)

        if banner and banner.banner:
            emb.set_image(url=banner.banner.url)
        if banner is None:
            return
        
        emb.set_thumbnail(url=user.avatar)
        await inter.reply(embed=emb, view=view)

    def is_user_forbidden(self, user_id):
        connection = sqlite3.connect('Mayson.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM forbidden_users WHERE user_id = ?", (user_id,))
        forbidden_user = cursor.fetchone()
        connection.close()
        return forbidden_user is not None

class ProfileView(ui.View):
    def __init__(self, bot, author_id):
        super().__init__()
        self.timeout = 20
        self.age = None
        self.bot = bot
        self.author_id = author_id

    async def interaction_check(self, interaction: disnake.MessageInteraction) -> bool:
        return interaction.user.id == self.author_id

    @ui.button(label="Указать возраст", style=disnake.ButtonStyle.green)
    async def set_age(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):

        await interaction.response.defer()
        try:
            age_msg = await interaction.channel.send("Введите свой возраст, у вас есть 20 секунд.")

            def check_age(m):
                return m.author == interaction.user and m.channel == age_msg.channel

            age_response = await self.bot.wait_for("message", check=check_age, timeout=self.timeout)

            if age_response.content.isdigit() and 14 <= int(age_response.content) < 100:
                self.age = int(age_response.content)
                await age_msg.delete()
                await age_response.add_reaction("✅")

                # Сохранение возраста в базу данных
                cursor.execute('INSERT OR REPLACE INTO users_age VALUES (?, ?)', (interaction.user.id, self.age))
                conn.commit()
            elif int(age_response.content) < 14:
                await age_msg.delete()
                embed = disnake.Embed(title="❌ Произошла ошибка!", description="Произошла неизвестная ошибка после выполнения команды.", color=disnake.Color.brand_red())
                embed.add_field(name="От чего все проблемы?", value="```Ты как на платформе зарегистрировался, мальчик?```", inline=False)
                embed.set_footer(text=random.choice(errors), icon_url=self.bot.user.avatar)
                await interaction.channel.send(embed=embed)
            elif int(age_response.content) > 100:
                await age_msg.delete()
                embed = disnake.Embed(title="❌ Произошла ошибка!", description="Произошла неизвестная ошибка после выполнения команды.", color=disnake.Color.brand_red())
                embed.add_field(name="От чего все проблемы?", value="```Позвони мне на SCP-1576, а не через чат.```", inline=False)
                embed.set_footer(text=random.choice(errors), icon_url=self.bot.user.avatar)
                await interaction.channel.send(embed=embed)

        except asyncio.TimeoutError:
            await age_msg.delete()
            embed = disnake.Embed(title="❌ Произошла ошибка!", description="Произошла неизвестная ошибка после выполнения команды.", color=disnake.Color.brand_red())
            embed.add_field(name="От чего все проблемы?", value="```Вы не успели указать возраст.```", inline=False)
            await interaction.channel.send(embed=embed, delete_after=5)
            return

def setup(bot: commands.Bot):
    bot.add_cog(UtilsCog(bot))