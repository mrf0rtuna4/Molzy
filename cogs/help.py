import disnake
from disnake.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = disnake.Embed(title=f"Список команд `Molzy`", description="Здесь собраны все команды Molzy и разбиты на различные категории. Используйте `/ (слеш)` чтобы увидеть слеши бота.", color=disnake.Color.random())
        await ctx.send(embed = embed, view=MyView())

class MyView(disnake.ui.View):
    @disnake.ui.select(
        placeholder="Выберите нужную категорию.",
        min_values = 1, 
        max_values = 1, 
        options = [ 
            disnake.SelectOption(
                label="📑Утилиты",
                description="Базовые команды Molzy."
            ),
            disnake.SelectOption(
                label="🔧Административные",
                description="Команды для модераторов серверов."
            ),
            disnake.SelectOption(
        label = "⚙️Настройки",
        description="Как это б#### настроить?!"
            ),
            disnake.SelectOption(
                label="⚔️Безопасность",
                description="И помните - «Ваша безопасность - наш приоритет!»"
            ),
            disnake.SelectOption(
                label="🔥Развлекательные",
                description="Единственная весёлая категория."
            )
        ]
    )
    async def select_callback(self, select, interaction):
        if select.values[0] == "📑Утилиты":
            emb = disnake.Embed(title="Базовые:", color = disnake.Colour.random())
            emb.add_field(name="`m.help` - Вызовет это меню.", value="", inline=False)
            emb.add_field(name="`m.stats` - Показывает статистику бота.", value="", inline=False)
            emb.add_field(name="`m.profile` - Информация о участнике/самом себе.", value="", inline=False)
            emb.add_field(name="`m.numgen` - Генерирует случайное число.", value="", inline=False)
            emb.add_field(name="`m.emoji` - Копирует эмодзи с других серверов.", value="", inline=False)
            await interaction.response.send_message(embed = emb, ephemeral = True)

        elif select.values[0] == "🔧Административные":
            emb1 = disnake.Embed(title="Команды модераторов:", color = disnake.Colour.random())
            emb1.add_field(name="`m.clear` - Очистка сообщений.", value="", inline=False)
            emb1.add_field(name="`m.ban` - Забанить пользователя.", value="", inline=False)
            emb1.add_field(name="`m.kick` - Выгнать участника.", value="", inline=False)
            emb1.add_field(name="`m.warn` - Выдать предупреждение участнику.", value="", inline=False)
            emb1.add_field(name="`m.unwarn` - Удалить предупреждения у участника.", value="", inline=False)
            emb1.add_field(name="`m.warns` - Узнать кол-во предупреждений у участника.", value="", inline=False)
            await interaction.response.send_message(embed = emb1, ephemeral = True)

        elif select.values[0] == "🔥Развлекательные":
            emb2 = disnake.Embed(title="Развлечения:", color = disnake.Colour.random())
            emb2.add_field(name="`m.kiss` - Поцеловать участника.", value="", inline=False)
            emb2.add_field(name="`m.hug` - Обнять участника.", value="", inline=False)
            emb2.add_field(name="`m.slap`- Подщёчина для участника.", value="", inline=False)
            emb2.add_field(name="`m.fuck` - Изнасиловать участника.", value="", inline=False)
            emb2.add_field(name="`m.suck` - Отсосать участнику.", value="", inline=False)
            emb2.add_field(name="`m.pat` - Погладить участника.", value="", inline=False)
            emb2.add_field(name="`m.punch` - Ударить пользователя.", value="", inline=False)
            emb2.add_field(name="`m.bite` - Укусить участника.", value="", inline=False)
            await interaction.response.send_message(embed = emb2, ephemeral = True)

        elif select.values[0] == "⚔️Безопасность":
            emb4 = disnake.Embed(title="Безопасность:", color = disnake.Colour.random())
            emb4.add_field(name="`m.ban` - Забанить пользователя.", value="", inline=False)
            await interaction.response.send_message(embed = emb4, ephemeral = True)
        
        elif select.values[0] == "⚙️Настройки":
            emb5 = disnake.Embed(title="Настройки:", color = disnake.Colour.random())
            emb5.add_field(name="`m.set_punish_channel` - Установить канал для наказаний.", value="", inline=False)
            emb5.add_field(name="`m.setlogchannel` - Установить канал для логов.", value="", inline=False)
            await interaction.response.send_message(embed = emb5, ephemeral = True)

def setup(bot: commands.Bot):
    bot.add_cog(HelpCog(bot))