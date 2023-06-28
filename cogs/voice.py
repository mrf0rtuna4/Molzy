import disnake
from disnake.ext import commands
import os
import json

VOICE_CHANNEL_SETTINGS_FILE = "voice_channel_settings.json"

class VoiceCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def voice(self, ctx):
        guild = ctx.guild
        settings = self.load_voice_channel_settings()
        channel_id = settings.get(str(guild.id))
        if channel_id:
            await ctx.send("Голосовой канал уже существует.")
        else:
            channel = await guild.create_voice_channel("Создать Голосовой Канал")
            settings[str(guild.id)] = str(channel.id)
            self.save_voice_channel_settings(settings)
            emb = disnake.Embed(title="✅ Готово!", description=f"Голосовой канал {channel.mention} был создан и запомнен в базе данных.", color=disnake.Color.green())
            await ctx.send(embed = emb)

    def check_empty(self, member, before, after):
        return len(before.channel.members) == 0

    async def create_user_voice_channel(self, member):
        guild = member.guild
        settings = self.load_voice_channel_settings()
        channel_id = settings.get(str(guild.id))
        if channel_id:
            category = member.guild.get_channel(int(channel_id)).category
            channel_name = member.display_name
            overwrites = {
                guild.default_role: disnake.PermissionOverwrite(connect=False),
                member: disnake.PermissionOverwrite(connect=True, manage_channels=True)
            }
            channel = await category.create_voice_channel(channel_name, overwrites=overwrites, user_limit=1)
            await member.move_to(channel)

            folder_path = f"voice_channels/{guild.id}"
            os.makedirs(folder_path, exist_ok=True)
            file_path = f"{folder_path}/{channel.id}"
            open(file_path, 'a').close()


            await self.bot.wait_for('voice_state_update', check=self.check_empty)
            await channel.delete()

    def load_voice_channel_settings(self):
        if os.path.exists(VOICE_CHANNEL_SETTINGS_FILE):
            with open(VOICE_CHANNEL_SETTINGS_FILE, "r") as file:
                return json.load(file)
        return {}

    def save_voice_channel_settings(self, settings):
        with open(VOICE_CHANNEL_SETTINGS_FILE, "w") as file:
            json.dump(settings, file)

    @commands.slash_command(name="delete-voice", description="Удалить голосовой канал из списка Molzy.")
    @commands.has_permissions(manage_channels=True)
    async def delvoice(self, ctx):
        guild = ctx.guild
        settings = self.load_voice_channel_settings()
        channel_id = settings.get(str(guild.id))
        if channel_id:
            del settings[str(guild.id)]
            self.save_voice_channel_settings(settings)
            folder_path = f"voice_channels/{guild.id}"
            file_path = f"{folder_path}/{channel_id}"
            if os.path.exists(file_path):
                os.remove(file_path)
            emb2 = disnake.Embed(title="✅ Готово!", description=f"Голосовой канал удалён из базы данных.", color=disnake.Color.green())
            await ctx.send(embed = emb2)
        else:
            emb1 = disnake.Embed(title="❌ Произошла ошибка!", description=f"Голосовой канал не найден.", color=disnake.Color.red())
            await ctx.response.send_message(embed = emb1, ephemeral = True)

    @commands.Cog.listener("on_voice_state_update")
    async def on_voice_state_update(self, member, before, after):
        if not member.bot:
            guild = member.guild
            if before.channel is None and after.channel is not None:
                settings = self.load_voice_channel_settings()
                channel_id = settings.get(str(guild.id))
                if channel_id:
                    if after.channel.id == int(channel_id):
                        await self.create_user_voice_channel(member)

def setup(bot: commands.Bot):
    bot.add_cog(VoiceCog(bot))