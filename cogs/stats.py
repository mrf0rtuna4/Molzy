import disnake
from disnake.ext import commands
import psutil
import platform
import time
from datetime import timedelta

owner_id = 386439272455995394
uowner_id = 1051530567486808115
testers = 702443229924032512, 846090153583968326, 726329794576384010

class StatsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = time.time()

    @commands.command()
    async def stats(self, ctx):
        view = disnake.ui.View()
        style = disnake.ButtonStyle.gray
        item = disnake.ui.Button(style=style, label="Сервер Технической Поддержки", url="https://discord.gg/sXKurQ2nPg")
        view.add_item(item=item)
        
        current_time = time.time()
        uptime_seconds = int(round(current_time - self.start_time))
        uptime = str(timedelta(seconds=uptime_seconds))

        owner = self.bot.get_user(owner_id)
        tester = [self.bot.get_user(tester_id) for tester_id in testers]
        uowner = self.bot.get_user(uowner_id)

        important_info = (
            f"Разработчик: **{owner.name}**",
            f"Со-Разработчик: **{uowner.name}**",
            f"Тестировщик(и): **{', '.join([tester.name for tester in tester])}**"
        )
        guilds_info = (
            f"Количество стикеров: **{len(ctx.bot.stickers)}**",
            f"Количество эмодзи: **{len(ctx.bot.emojis)}**",
        )
        about_me_info = (
            f"Операционная система: **{platform.platform()}**",
            f"Язык программирования: **Python {platform.python_version()}**",
            f"Статус: **Активное действие.**",
            f"RAM: **{psutil.virtual_memory().percent}%**",
            f"CPU: **{psutil.cpu_percent()}%**",
            f"Задержка: **{round(ctx.bot.latency*1000, 2)}ms**",
        )
        command_count = len([i for i in ctx.bot.commands if not i.name == 'jishaku' and not i.name == 'justify'])
        user_count = len(self.bot.users)
        other_info = (
            f"Количество обычных команд: **{command_count}**",
            f"Количество серверов: **{len(ctx.bot.guilds)}**",
            f"Количество пользователей: **{user_count}**",
        )
        embed = disnake.Embed(title=f"Моя статистика и информация обо мне", description=f"Время работы: {uptime}", color=disnake.Color.random())
        embed.add_field(name="Основная информация", value='\n'.join(important_info), inline=False)
        embed.add_field(name=f"Информация о серверах", value='\n'.join(guilds_info), inline=False),
        embed.add_field(name=f"Информация про меня", value='\n'.join(about_me_info), inline=False),
        embed.add_field(name="Всё прочее", value='\n'.join(other_info), inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1100779525962485903/1112304761220382790/img-Tzgw4Gxxj4SlqO22YLpOKkyw.png")
        await ctx.reply(embed=embed, view=view)

def setup(bot: commands.Bot):
    bot.add_cog(StatsCog(bot))