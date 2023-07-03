import disnake
from disnake.ext import commands
from googletrans import Translator
from disnake import ui
import asyncio
import os

owner = 386439272455995394
uowner = 1051530567486808115
testers = 702443229924032512, 846090153583968326

class classicCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="translator", description="Переводит текст на разные языки.")
    async def translator(self, ctx, lang, *, phrase):
        try:
            await ctx.response.defer()
            translator = Translator()
            translation = translator.translate(phrase, dest=lang)
            emb = disnake.Embed(title=f"✅ Перевод выполнен! [ {phrase} ]", description=f"Ваш перевод - {translation.text}", color=disnake.Color.random())
            emb.set_footer(text="Molzy Production", icon_url=ctx.bot.user.avatar)
            await ctx.followup.send(embed = emb)
        except Exception as e:
            embed = disnake.Embed(title="❌ Ошибка при переводе", description=str(e), color=0xFF0004)
            embed.set_footer(text="Molzy Production", icon_url=ctx.bot.user.avatar)
            await ctx.followup.send(embed=embed)

    @commands.command()
    async def profile(self, ctx, member: disnake.Member = None):
        member = member or ctx.author

        if ctx.message.author.id == 386439272455995394:

            roles = [role.mention for role in member.roles[1:]]

            view = ProfileView(self.bot, ctx.author.id)

            status = 'Разработчик' if member.id == owner else 'Это я!' if member.id == ctx.bot.user.id else 'Тестировщик' if member.id in testers else 'Со-Разработчик' if member.id == uowner else 'Пользователь'

            emb = disnake.Embed(description=member.activity or "Нет активности", color=disnake.Color.random())
            emb.set_author(name=member.name, icon_url=member.avatar.url)
            emb.set_thumbnail(url=member.avatar.url)
            emb.add_field(name="💻 | Статус в боте:", value=status)

            file_path = f'age_folder/{member.id}.txt'
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    content = file.read()
                    age = int(content) if content.isdigit() else "Не указан."
            else:
                age = "Не указан."
            emb.add_field(name="🔮 | Возраст:", value=age)

            if member.id != ctx.author.id:
                view.children = [] 

            view.bot = self.bot
            await ctx.send(embed=emb, view=view)
        else:
            emb1 = disnake.Embed(title="⚠️ Произошла ошибка!", description="Команда находится на переработке.", color=disnake.Color.yellow())
            await ctx.send(embed=emb1)

    @commands.command()
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
            embed.set_footer(text="Molzy Production", icon_url=self.bot.user.avatar.url)
            await ctx.send(embed=embed)
            return
        
        new_emoji = await guild.create_custom_emoji(name=emoji_name, image=emoji_bytes)

        embed = disnake.Embed(
            title='✅ Эмодзи добавлен.',
            description=f'Эмодзи {new_emoji} успешно добавлен на сервер с именем: `{emoji_name}`',
            color=disnake.Color.green()
        )
        embed.set_footer(text="Molzy Production", icon_url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)

    @commands.slash_command(name="server-info", description="Покажу инфу о сервере))")
    async def serverstats(self, ctx):
        member = ctx.author

        guild = ctx.guild
        total_members = guild.member_count
        online_members = sum(1 for member in guild.members if member.status != disnake.Status.offline)
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)
        roles = len(guild.roles)
        emojis = len(guild.emojis)
        created_at = guild.created_at.strftime("%Y-%m-%d %H:%M:%S")
        owner = guild.owner
        premium_tier = guild.premium_tier
        boosters = len(guild.premium_subscribers)
        verification_level = guild.verification_level
        region = guild.region

        if  guild.region == "deprecated":
            region = "Russia"

        embed = disnake.Embed(title=f"Статистика сервера {guild.name}", color=disnake.Color.blurple())

        basic_info = (
            f"Владелец: **{owner.name}**",
            f"Регион: **{region}**",
            f"Уровень буста: **{premium_tier}**",
            f"Бустеры: **{boosters}**",
        )
        guilds_info = (
            f"Уровень проверки: **{verification_level}**",
            f"Участников: **{total_members}**",
            f"Онлайн: **{online_members}**",
            f"Сервер создан: **{created_at}**",
        )
        user_info = (
            f"Вы: **{member.name}**",
            f"Ваша высшая роль: {member.top_role.mention}",
        )
        other_info = (
            f"Текстовые каналы: **{text_channels}**",
            f"Голосовые: **{voice_channels}**",
            f"Категории: **{categories}**",
            f"Роли: **{roles}**",
            f"Эмодзи: **{emojis}**",
        )

        embed.add_field(name="> Основная информация", value='\n'.join(basic_info), inline=False)
        embed.add_field(name="> О сервере", value='\n'.join(guilds_info), inline=False)
        embed.add_field(name="> Пользователь", value='\n'.join(user_info))
        embed.add_field(name="> Каналы, роли и эмодзи", value='\n'.join(other_info), inline=False)
        embed.set_thumbnail(guild.icon.url)
        embed.set_footer(text="Molzy Production", icon_url=ctx.bot.user.avatar.url)

        await ctx.send(embed=embed)

class ProfileView(ui.View):
    def __init__(self, bot, author_id):
        super().__init__()
        self.timeout = 20
        self.age = None
        self.bot = bot
        self.author_id = author_id

    async def interaction_check(self, interaction: disnake.MessageInteraction) -> bool:
        return interaction.user.id == self.author_id

    @ui.button(label="Указать возраст", style=disnake.ButtonStyle.primary)
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
                
                data_folder = "age_folder"
                if not os.path.exists(data_folder):
                    os.makedirs(data_folder)

                file_path = os.path.join(data_folder, f"{interaction.user.id}.txt")
                with open(file_path, "w") as file:
                    file.write(str(self.age))
            else:
                await age_msg.delete()
                embed = disnake.Embed(title="❌ Произошла ошибка!", description="Укажите возраст от 14 до 100 лет.", color=disnake.Color.brand_red())
                await interaction.channel.send(embed=embed, delete_after=10)
                return

        except asyncio.TimeoutError:
            await age_msg.delete()
            await interaction.channel.send("Время ожидания истекло. Попробуйте еще раз.", delete_after=5)
            return

def setup(bot: commands.Bot):
    bot.add_cog(classicCog(bot))