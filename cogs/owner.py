from datetime import datetime
import sqlite3
import disnake
from disnake.ext import commands, tasks
import asyncio
import random
from core.embeds import errors, descriptions

conn = sqlite3.connect('Mayson.db')
cursor = conn.cursor()

cursor.execute('''
            CREATE TABLE IF NOT EXISTS status (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                status TEXT
            )
        ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS forbidden_users (
               user_id INTEGER PRIMARY KEY
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS global_warns (
        user_id INTEGER,
        warning_count INTEGER,
        reason TEXT
    )
''')
conn.commit()

class OwnerCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @tasks.loop(seconds=1)
    async def status(self):
        await self.bot.change_presence(status=disnake.Status.idle, activity=disnake.Activity(name="Сериалы для маленьких девочек", type=disnake.ActivityType.watching))
        await asyncio.sleep(35)
        await self.bot.change_presence(status=disnake.Status.idle, activity=disnake.Activity(name="", type=disnake.ActivityType.playing))
        await asyncio.sleep(20)
        await self.bot.change_presence(status=disnake.Status.idle, activity=disnake.Activity(name=f"с {self.bot.owner.name}", type=disnake.ActivityType.playing))
        await asyncio.sleep(20)
        await self.bot.change_presence(status=disnake.Status.idle, activity=disnake.Activity(name="Мир не справедлив.", type=disnake.ActivityType.watching))
        await asyncio.sleep(20)

    @status.before_loop
    async def before_status(self):
        await self.bot.wait_until_ready()

    def cog_unload(self):
        self.status.cancel()

    @commands.slash_command(name="reload", description="Коги взрыв.", guild_ids=[1171845365339783230])
    @commands.is_owner()
    async def reload(self, inter: disnake.ApplicationCommandInteraction, cog):
            self.bot.reload_extension("cogs."+cog)
            await inter.response.send_message("Ког перезагружен!", ephemeral=True)

    @commands.slash_command(name='global-warn', description='Глобальные предупреждения.', guild_ids=[1171845365339783230])
    @commands.is_owner()
    async def globwarn(self, ctx, *, user: disnake.User, action: str = commands.Param(choices=['Выдать глобальное предупреждение', 'Убрать глобальное предупреждение']), count: int = None, reason: str = None):
        server_id = 1171845365339783230
        guild_id = self.bot.get_guild(server_id)
        
        new_warning_count = 0

        # Используем контекстный менеджер для работы с базой данных
        with sqlite3.connect('Mayson.db') as conn:
            cursor = conn.cursor()

            cursor.execute('SELECT warning_count FROM global_warns WHERE user_id = ?', (user.id,))
            user_warnings = cursor.fetchone()

            if action == 'Выдать глобальное предупреждение':
                if user_warnings:
                    new_warning_count = user_warnings[0] + 1
                    cursor.execute('UPDATE global_warns SET warning_count = ? WHERE user_id = ?', (new_warning_count, user.id))
                else:
                    cursor.execute('INSERT INTO global_warns (user_id, warning_count, reason) VALUES (?, 1, ?)', (user.id, reason))

                    conn.commit()

                E2 = disnake.Embed(title='Выдано глобальное предупреждение.', color=disnake.Color.red())
                E2.add_field(name='**Разработчик/Менеджер:**', value=ctx.author.mention)
                E2.add_field(name='**Наказанный:**', value=user.name)
                E2.add_field(name='**Причина:**', value=reason or 'Причина не указана.')
                E2.add_field(name='**Количество глобальных предупреждений:**', value=new_warning_count, inline=False)
                await ctx.send(embed=E2)

                if new_warning_count == 1:
                    E1 = disnake.Embed(title='Вам было выдано глобальное предупреждение.', color=disnake.Color.red())
                    E1.add_field(name='**Разработчик/Менеджер:**', value=ctx.author.mention)
                    E1.add_field(name='Причина:', value=reason or 'Причина не была указана разработчиком/менеджером.')
                    E1.add_field(name='Ваше кол-во предупреждений:', value=new_warning_count)
                    E1.add_field(name='Комментарий разработчика/менеджера:', value='```Глобальное предупреждение выдаётся навсегда за нарушение политики пользования ботом Mayson. Если вы соберёте 3 варна, то будете перманентно заблокированы в боте и не сможете использовать его команды. С уважением, Mayson Dev. Community.```', inline=False)
                    await user.send(embed=E1)

                elif new_warning_count == 2:
                    E1 = disnake.Embed(title='Вам было выдано глобальное предупреждение.', color=disnake.Color.red())
                    E1.add_field(name='**Разработчик/Менеджер:**', value=ctx.author.mention)
                    E1.add_field(name='Причина:', value=reason or 'Причина не была указана разработчиком/менеджером.')
                    E1.add_field(name='Ваше кол-во предупреждений:', value=new_warning_count)
                    E1.add_field(name='Комментарий разработчика/менеджера:', value='```Вы вновь получили предупреждение за нарушение политики пользования ботом Mayson. В следующий раз, если вы получите предупреждение, вы будете занесены в чёрный список.```', inline=False)
                    await user.send(embed=E1)

                elif new_warning_count == 3:
                    E1 = disnake.Embed(title='Вам было выдано глобальное предупреждение.', color=disnake.Color.red())
                    E1.add_field(name='**Разработчик/Менеджер:**', value=ctx.author.mention)
                    E1.add_field(name='Причина:', value=reason or 'Причина не была указана разработчиком/менеджером.')
                    E1.add_field(name='Ваше кол-во предупреждений:', value=new_warning_count)
                    E1.add_field(name='Комментарий разработчика/менеджера:', value='```Вы получили 3/3 глобальных предупреждений и вам будет будет ограничен доступ к некоторым командам.```', inline=False)
                    await user.send(embed=E1)

            elif action == 'Убрать глобальное предупреждение':
                if user_warnings and user_warnings[0] > 0:
                    new_warning_count = max(user_warnings[0] - (count or 0), 0)
                    cursor.execute('UPDATE global_warns SET warning_count = ? WHERE user_id = ?', (new_warning_count, user.id))
                    conn.commit()
                    E = disnake.Embed(title='Удаление глобальных предупреждений.', color=disnake.Color.green())
                    E.add_field(name='**Разработчик/Менеджер:**', value=ctx.author.mention)
                    E.add_field(name='**Пользователь:**', value=user.name)
                    E.add_field(name='**Количество глобальных предупреждений:**', value=new_warning_count if new_warning_count else '0', inline=False)
                    await ctx.send(embed=E)
                else:
                    Edd = disnake.Embed(title='⚠️ Произошла ошибка.', color=disnake.Color.yellow())
                    Edd.add_field(name='Что же не так?', value='```У пользователя нет предупреждений.```')
                    await ctx.send(embed=Edd)

    def add_forbidden_user(self, user_id):
        connection = sqlite3.connect('Mayson.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO forbidden_users (user_id) VALUES (?)", (user_id,))
        connection.commit()
        connection.close()

    @commands.slash_command(name="blacklist", description="Заблокируйте жалкий мусор.", guild_ids=[1171845365339783230])
    @commands.is_owner()
    async def forbid(self, inter: disnake.ApplicationCommandInteraction, *, user: disnake.User, action: str = commands.Param(choices=['Добавить пользователя в ЧС', 'Убрать пользователя из ЧС'])):
        server_id = 1171845365339783230
        guild = inter.guild
        guild_id = self.bot.get_guild(server_id)
        author = inter.author
        timestamp = datetime.now()
        if action == 'Добавить пользователя в ЧС':
                if user.id == 585427658775461909:
                    m = disnake.Embed(title="⚠️ Произошла ошибка!", description="Кажется, пользователем был указан кто-то знакомый...", color=0xff6969)
                    m.add_field(name="Что же не так?", value=f"```Господин Helaney, вы не можете занести эту госпожу в Чёрный Список.```")
                    m.set_footer(text=f"{random.choice(errors)} ∙ {timestamp.strftime('%d %b %Y')}", icon_url=self.bot.user.avatar.url)
                    await inter.response.send_message(embed=m, ephemeral=True)
                    
                elif user.id == self.bot.owner.id:
                    m = disnake.Embed(title="⚠️ Произошла ошибка!", description="Кажется, пользователем был указан кто-то знакомый...", color=0xff6969)
                    m.add_field(name="Что же не так?", value=f"```Господин Helaney, вы не можете занести себя в Чёрный Список.```")
                    m.set_footer(text=f"{random.choice(errors)} ∙ {timestamp.strftime('%d %b %Y')}", icon_url=self.bot.user.avatar.url)
                    await inter.response.send_message(embed=m, ephemeral=True)
                    return

                if not self.is_user_forbidden(user.id):
                    self.add_forbidden_user(user.id)
                    await guild_id.ban(user, reason='Добавлен в ЧС бота.')
                    wm = disnake.Embed(color=0x740B0B)
                    wm.add_field(name="**Сервер:**", value=guild.name)
                    wm.add_field(name="**Разработчик/Менеджер:**", value=author.mention)
                    wm.add_field(name="**Пользователь:**", value=user.name)
                    wm.add_field(name="**Действие:**", value=action, inline=False)
                    wm.set_footer(text="Не думал, что среди нас окажется предатель...", icon_url=self.bot.user.avatar)
                    await inter.response.send_message(embed=wm)
                else:
                    E = disnake.Embed(title="⚠️ Возникла ошибка.", description="Кажется, этот пользователь уже находится в чёрном списке.", color=disnake.Color.yellow())
                    E.set_footer(text="Может вы ошиблись?", icon_url=self.bot.user.avatar)
                    await inter.response.send_message(embed=E)
                
        elif action == 'Убрать пользователя из ЧС':
            if self.is_user_forbidden(user.id):
                        self.remove_forbidden_user(user.id)
                        await guild_id.unban(user)
                        wm = disnake.Embed(color=0x740B0B)
                        wm.add_field(name="**Сервер:**", value=guild.name)
                        wm.add_field(name="**Разработчик/Менеджер:**", value=author.mention)
                        wm.add_field(name="**Пользователь:**", value=user.name)
                        wm.add_field(name="**Действие:**", value=action, inline=False)
                        wm.set_footer(text="Вы сделали поспешный вывод, господин.", icon_url=self.bot.user.avatar)
                        await inter.response.send_message(embed=wm)
            else:
                        E = disnake.Embed(title="⚠️ Возникла ошибка.", description="Этого пользователя нет в чёрном списке.", color=disnake.Color.blurple())
                        E.set_footer(text="Господин, как вы собрались убирать из ЧС пустоту?", icon_url=self.bot.user.avatar)
                        await inter.response.send_message(embed=E)

    def add_forbidden_user(self, user_id):
        connection = sqlite3.connect('Mayson.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO forbidden_users (user_id) VALUES (?)", (user_id,))
        connection.commit()
        connection.close()

    def remove_forbidden_user(self, user_id):
        connection = sqlite3.connect('Mayson.db')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM forbidden_users WHERE user_id = ?", (user_id,))
        connection.commit()
        connection.close()

    def is_user_forbidden(self, user_id):
        connection = sqlite3.connect('Mayson.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM forbidden_users WHERE user_id = ?", (user_id,))
        forbidden_user = cursor.fetchone()
        connection.close()
        return forbidden_user is not None
    
    @commands.slash_command(name="user-status", description="Управление статусом пользователя.", guild_ids=[1171845365339783230])
    @commands.is_owner()
    async def user_status(self, inter: disnake.ApplicationCommandInteraction, action: str = commands.Param(choices=['Установить статус', 'Убрать статус', 'Изменить статус']), *, user: disnake.User, status: str = ""):
        guild = inter.guild

        if action == 'Установить статус':
            if not self.is_user_added(user.id):
                self.add_user_to_database(user.id, user.name, status)
                E = disnake.Embed(color=0x740B0B)
                E.add_field(name='**Сервер: **', value=guild.name)
                E.add_field(name="**Пользователь: **", value=user.mention)
                E.add_field(name="**Получен статус: **", value=status)
                E.set_footer(text=f"Теперь будет легче обращаться к нему.", icon_url=self.bot.user.avatar)
                await inter.response.send_message(embed=E)

        elif action == 'Убрать статус':
            self.remove_user_status(user.id)
            E = disnake.Embed(color=0x740B0B)
            E.add_field(name='**Сервер: **', value=guild.name)
            E.add_field(name="**Пользователь: **", value=user.mention)
            E.add_field(name="**Статус удалён**", value="Статус пользователя успешно удалён.")
            E.set_footer(text="Теперь он обычный человек.", icon_url=self.bot.user.avatar)
            await inter.response.send_message(embed=E)

        elif action == 'Изменить статус':
            if self.is_user_added(user.id):
                self.update_user_status(user.id, status)
                E = disnake.Embed(color=0x740B0B)
                E.add_field(name='**Сервер: **', value=guild.name)
                E.add_field(name="**Пользователь: **", value=user.mention)
                E.add_field(name="**Статус изменён**", value=f"Новый статус: {status}")
                E.set_footer(text="Обновите информацию о пользователе.", icon_url=self.bot.user.avatar)
                await inter.response.send_message(embed=E)
            else:
                E = disnake.Embed(color=0xff6969)
                E.add_field(name='**Ошибка: **', value="Пользователь не найден в базе данных.")
                E.set_footer(text="Убедитесь, что пользователь был добавлен.", icon_url=self.bot.user.avatar)
                await inter.response.send_message(embed=E)

    def add_user_to_database(self, user_id, username, status):
        connection = sqlite3.connect('Mayson.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO status (user_id, username, status) VALUES (?, ?, ?)", (user_id, username, status))
        connection.commit()
        connection.close()

    def remove_user_status(self, user_id):
        connection = sqlite3.connect('Mayson.db')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM status WHERE user_id = ?", (user_id,))
        connection.commit()
        connection.close()

    def update_user_status(self, user_id, status):
        connection = sqlite3.connect('Mayson.db')
        cursor = connection.cursor()
        cursor.execute("UPDATE status SET status = ? WHERE user_id = ?", (status, int(user_id)))
        connection.commit()
        connection.close()

    def is_user_added(self, user_id):
        connection = sqlite3.connect('Mayson.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM status WHERE user_id = ?", (int(user_id),))
        user = cursor.fetchone()
        connection.close()
        return user is not None

def setup(bot: commands.Bot):
    bot.add_cog(OwnerCog(bot))