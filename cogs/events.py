import disnake
from disnake.ext import commands, tasks
import asyncio
import random
from datetime import timedelta

class EventCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.status.start()
    
    def cog_unload(self):
        self.status.cancel()

    @tasks.loop(seconds=1)
    async def status(self):
        activities = [
            disnake.Activity(name="/write", type=disnake.ActivityType.watching),
            disnake.Activity(name="helaney", type=disnake.ActivityType.listening),
            disnake.Activity(name="/imagine", type=disnake.ActivityType.watching),
            disnake.Activity(name="Heypers Project", type=disnake.ActivityType.watching)
        ]
        for activity in activities:
            await self.bot.change_presence(status=disnake.Status.dnd, activity=activity)
            await asyncio.sleep(20)
    
    @status.before_loop
    async def before_status(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener("on_message")
    async def on_message(self, message):

            if self.bot.user.mentioned_in(message) and len(message.content) == len(self.bot.user.mention):
                response = f"🔥 Приветствую, **{message.author.name}**! \n🥶 Команда, чтобы увидеть мои команды: `m.help` \n\n🤨 Официальный сервер: https://discord.gg/4Wp6V3vrn2 \n❤️ Я уверен, мы подружимся с тобой! (Пригласить бота можно по кнопке в профиле)"
                await message.reply(response)

            forbidden_words = ["фортуна гей", "фортуна клоун", "хеланей клоун", "фoртуна гeй", "helaney гей", "helaney гей", "хеланей клoyн", "хeлaнeй гeй", "фортуна гeй"]

            if any(word in message.content.lower() for word in forbidden_words):
                hours = random.randint(13, 24 * 7)
                duration = timedelta(hours=hours)
                await message.author.timeout(duration)
                emb = disnake.Embed(title="✅ Тайм-Аут выдан!",
                                    description=f"Пользователь {message.author.mention} был лишён права говорить на **{hours} часов**. Причина: Плохое поведение.",
                                    color=disnake.Color.blurple())
                await message.channel.send(embed=emb)

def setup(bot: commands.Bot):
    bot.add_cog(EventCog(bot))