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

    @commands.command()
    async def info(self, ctx):
        owner_id = 386439272455995394
        owner = self.bot.get_user(owner_id)

        view = disnake.ui.View()
        style = disnake.ButtonStyle.gray
        item = disnake.ui.Button(style=style, label="Официальный сервер", url="https://discord.gg/sXKurQ2nPg")
        view.add_item(item=item)

        emb = disnake.Embed(title="Немного информации обо мне))", description="> Приветствую! Я - Molzy, ваш преданный виртуальный ассистент, готовый разнообразить этот сервер! \n\nВидишь меня впервые? Узнай мои команды - `m.help`! \n\nНадеюсь, мы станем лучшими друзьями!", color=disnake.Color.blurple())
        emb.set_footer(text="Molzy Development", icon_url=owner.avatar.url)
        await ctx.reply(embed=emb, view=view)

def setup(bot: commands.Bot):
    bot.add_cog(EventCog(bot))