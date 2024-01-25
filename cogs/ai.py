import disnake
from disnake.ext import commands
import sqlite3

connection = sqlite3.connect('Mayson.db')
cursor = connection.cursor()

# Создание таблицы для запрещенных пользователей
cursor.execute('''
    CREATE TABLE IF NOT EXISTS forbidden_users (
        user_id INTEGER PRIMARY KEY
    )
''')

connection.commit()
connection.close()

class OpenaiCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def handle_who_are_you(self, inter: disnake.ApplicationCommandInteraction):
        bot_name = self.bot.user.name
        developer_name = self.bot.owner.name
        reply = f"Я - **{bot_name}**, ваша виртуальная ассистентка, разработанная чудесным мальчиком - **{developer_name}**. Я здесь, что ответить на множество ваших вопросов и помочь вам. Итак, с чего хочешь начать?"
        embed = disnake.Embed(title="⟩ Ответ нейросети:", description=reply, color=disnake.Color.blurple())
        await inter.followup.send(embed=embed)

    async def handle_vzlom(self, inter: disnake.ApplicationCommandInteraction):
        reply = f"Извините, но я не могу обсуждать такие вопросы. Взлом пользователей - это незаконное действие, преследуемое по закону. К тому же, данная тема нарушает правила платформы Discord, советуем ознакомиться с правилами пользования платформой здесь, и больше не нарушать установленные правила - https://discord.com/terms."
        embed = disnake.Embed(title="⟩ Ответ нейросети:", description=reply, color=disnake.Color.blurple())
        await inter.followup.send(embed=embed)

    #@commands.slash_command(name="write", description="Задайте вопрос нейросети при помощи «GPT-3.5-Turbo».")
    #async def write(self, inter: disnake.ApplicationCommandInteraction, *, prompt):
            #vzriv = [1162058914414731344]
            #user = inter.author
            #if self.is_user_forbidden(user.id):
                #m1 = disnake.Embed(title="⚠️ Произошла ошибка!", description="Кажется, нейросеть сегодня не в духе, чтобы ответить вам.", color=0xff6969)
                #m1.add_field(name="От чего все проблемы?", value=f"```Увы, но кажется, вы находитесь в Чёрном Списке. Если у вас возникли вопросы по поводу вашей блокировки, свяжитесь с разработчиком бота - {self.bot.owner.name} или другим представителем Molzy. Спасибо за понимание.```")
                #m1.set_footer(text=f"Поддерживается благодаря {self.bot.owner.name}", icon_url=self.bot.owner.avatar.url)
                #await inter.response.send_message(embed=m1, ephemeral=True)
                #return
            
            #await inter.response.defer()

            #if "ты кто" in prompt.lower() or "кто ты" in prompt.lower():
                #await self.handle_who_are_you(inter)
            #elif 'взломать' in prompt.lower():
                #await self.handle_vzlom(inter)
            #else:

                #response = openai.ChatCompletion.create(
                    #model="gpt-3.5-turbo-0613",
                    #messages=[
                        #{"role": "system", "content": prompt},
                        #{"role": "user", "content": prompt}
                    #],
                #)
                #reply = response.choices[0].message.content
                #embed = disnake.Embed(title=f"⟩ Ответ нейросети:", description=reply, color=disnake.Color.blurple())
                #embed.set_footer(text=f"Поддерживается благодаря {self.bot.owner.name}", icon_url=self.bot.owner.avatar.url)
                #await inter.followup.send(embed=embed)

    def is_user_forbidden(self, user_id):
        connection = sqlite3.connect('Molzy.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM forbidden_users WHERE user_id = ?", (user_id,))
        forbidden_user = cursor.fetchone()
        connection.close()
        return forbidden_user is not None
        
def setup(bot: commands.Bot):
    bot.add_cog(OpenaiCog(bot))