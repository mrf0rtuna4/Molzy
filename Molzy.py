import disnake
from disnake.ext import commands
import openai
import json
import os

file = open('config.json', 'r')
config = json.load(file)

intents = disnake.Intents.all()
intents.guilds = True
intents.members = True
bot = commands.Bot(config['prefix'], intents=intents, help_command=None)
openai.api_key = config['token_openai']
token = config['token']

@bot.event
async def on_ready():
    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_command_error(ctx: commands.Context, e):
    try:
        em = str(e.original)
    except:
        em = str(e)
    if em!="": em=f"```{em}```"
    m = disnake.Embed(title=":x: Произошла ошибка!", color=0xff6969)
    m.add_field(name="Ошибка", value=f"{em}")
    await ctx.reply(embed=m)

@bot.event
async def on_slash_command_error(inter: disnake.ApplicationCommandInteraction, e):
    em = str(e.original)
    if em!="": em=f"```{em}```"
    m = disnake.Embed(title=":x: Произошла ошибка!", color=0xff6969)
    m.add_field(name="Ошибка", value=f"{em}")
    try:
        await inter.response.send_message(embed=m)
    except:
        await inter.followup.send(embed=m)

@bot.slash_command(name="reload", description="Перезагрузка коков.")
async def reload(inter: disnake.ApplicationCommandInteraction, cog: str):
    if inter.author.id == bot.owner_id:
        bot.reload_extension("cogs."+cog)
        await inter.response.send_message("Успешно!",ephemeral=True)

bot.run(token)