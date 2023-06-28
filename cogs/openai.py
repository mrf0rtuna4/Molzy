import disnake
from disnake.ext import commands
import openai
import time

owner_id = 386439272455995394

command_count = {}

class OpenaiCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="write", description="Задайте вопрос нейросети при помощи «GPT-3».")
    async def write(self, ctx, *, prompt):
            owner = self.bot.get_user(owner_id)
            result = str(prompt)
            await ctx.response.defer()

            user_id = ctx.author.id

            if user_id in command_count:
                command_count[user_id] += 1
            else:
                command_count[user_id] = 1

            if command_count[user_id] > 2:
                emb = disnake.Embed(title="⚠️ Достигнут лимит.", description="Вы достигли лимита использования команды.", color=disnake.Color.yellow())
                await ctx.followup.send(embed=emb, ephemeral=True)
                return

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k-0613",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": prompt}
                ],
            )
            reply = response.choices[0].message.content
            embed = disnake.Embed(title=f"⟩ {result}", description=reply, color=disnake.Color.blurple())
            embed.set_footer(text=f"Поддерживается благодаря {owner.name}", icon_url=owner.avatar.url)
            await ctx.followup.send(embed=embed)

            if command_count[user_id] == 2:
                embed = disnake.Embed(title="⚠️ Превышен лимит.", description="Вы превысили лимит использования. Пожалуйста, подождите 5 минут перед следующим использованием.", color=disnake.Color.yellow())
                await ctx.followup.send(embed=embed, ephemeral=True)
                time.sleep(300)
                command_count[user_id] = 0
        
def setup(bot: commands.Bot):
    bot.add_cog(OpenaiCog(bot))