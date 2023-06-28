import disnake
from disnake.ext import commands
from disnake import ui
import asyncio
import os

owner = 386439272455995394
uowner = 1051530567486808115
testers = 702443229924032512, 846090153583968326

amia = 560145600826572831

class RoflCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def userinfo(self, ctx, member_id: int = None):
        if member_id is None:
            member_id = ctx.author.id

        member = self.bot.get_user(member_id)

        if member is None:
            # Пользователь не найден
            if member_id != amia:
                await ctx.send("Пользователь не найден.")
                return

            # Информация о пользователе
            member = await self.bot.fetch_user(amia)

        roles = [role.mention for role in ctx.author.roles[1:]]

        view = ProfileView(self.bot, ctx.author.id)

        status = 'Разработчик' if member.id == owner else 'Это я!' if member.id == ctx.bot.user.id else 'Тестировщик' if member.id in testers else 'Со-Разработчик' if member.id == uowner else 'Пользователь'

        if member.id == amia:
            amiaa = member
            emb = disnake.Embed(description="No activity?((", color=disnake.Color.random())
            emb.set_author(name=member.name, icon_url=amiaa.avatar.url)
            emb.set_thumbnail(url=amiaa.avatar.url)
            emb.add_field(name="👤 | Username:", value=f"{amiaa.name}", inline=False)
            emb.add_field(name="⚙️ | ID:", value=amiaa.id, inline=False)
            emb.add_field(name="🕵🏻 | Registered:", value=amiaa.created_at.strftime("%d.%m.%Y %H:%M:%S"), inline=False)

            file_path = f'age_folder/{member.id}.txt'
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    content = file.read()
                    age = int(content) if content.isdigit() else "i forgot oopsies)))"
            emb.add_field(name="🔮 | Age:", value=age, inline=False)

            if member.id != ctx.author.id:
                view.children = []

            view.bot = self.bot
            await ctx.send(embed=emb, view=view)

class ProfileView(ui.View):
    def __init__(self, bot, author_id):
        super().__init__()
        self.timeout = 20
        self.age = None
        self.bot = bot
        self.author_id = author_id

    async def interaction_check(self, interaction: disnake.MessageInteraction) -> bool:
        return interaction.user.id == self.author_id

    @ui.button(label="Specify the age", style=disnake.ButtonStyle.primary)
    async def set_age(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):

        await interaction.response.defer()
        try:
            age_msg = await interaction.channel.send("Введите свой возраст, у вас есть 20 секунд.")

            def check_age(m):
                return m.author == interaction.user and m.channel == age_msg.channel

            age_response = await self.bot.wait_for("message", check=check_age, timeout=self.timeout)

            if age_response.content.isdigit() and 13 <= int(age_response.content) < 120:
                self.age = int(age_response.content)
                await age_msg.delete()
                await age_response.add_reaction("✅")
                
                data_folder = "age_folder"
                if not os.path.exists(data_folder):
                    os.makedirs(data_folder)

                file_path = os.path.join(data_folder, f"{interaction.user.id}.txt")
                with open(file_path, "w") as file:
                    file.write(str(self.age))
            else:
                await age_msg.delete()
                embed = disnake.Embed(title="❌ Произошла ошибка!", description="Твой возраст не соответсвует минимальным требованиям. Укажи возраст от 13 до 120 лет.", color=disnake.Color.brand_red())
                await interaction.channel.send(embed=embed, delete_after=10)
                return

        except asyncio.TimeoutError:
            await age_msg.delete()
            await interaction.channel.send("Время ожидания истекло. Попробуйте еще раз.", delete_after=5)
            return
        
def setup(bot: commands.Bot):
    bot.add_cog(RoflCog(bot))