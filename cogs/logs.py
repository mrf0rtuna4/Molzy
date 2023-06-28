import disnake
from disnake.ext import commands
import os
import json

VOICE_CHANNEL_SETTINGS_FILE = "voice_channel_settings.json"
SETTINGS_FILE = "log_settings.json"

class LogsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #<--------------Логи----------------->

    @commands.Cog.listener("on_member_join")
    async def on_member_join(self, member):
        guild = member.guild
        log_channel = await self.get_log_channel(guild)
        if log_channel:
            embed = disnake.Embed(description=f"{member.mention} присоединился к серверу", color=disnake.Color.blurple())
            await log_channel.send(embed=embed.set_footer(text="Molzy Production", icon_url=self.bot.user.avatar))

    @commands.Cog.listener("on_message_remove")
    async def on_member_remove(self, member):
        guild = member.guild
        log_channel = await self.get_log_channel(guild)
        if log_channel:
            embed = disnake.Embed(description=f"{member.mention} покинул сервер", color=disnake.Color.blurple())
            await log_channel.send(embed=embed.set_footer(text="Molzy Production", icon_url=self.bot.user.avatar))

    @commands.Cog.listener("on_message_delete")
    async def on_message_delete(self, message):
        guild = message.guild
        log_channel = await self.get_log_channel(guild)
        if log_channel:
            embed = disnake.Embed(title="Сообщение удалено", color=disnake.Color.blurple())
            embed.add_field(name="Автор", value=message.author.mention)
            embed.add_field(name="Канал", value=message.channel.mention)
            embed.add_field(name="Содержание", value=message.content)
            await log_channel.send(embed=embed.set_footer(text="Molzy Production", icon_url=self.bot.user.avatar))

    @commands.Cog.listener("on_message_edit")
    async def on_message_edit(self, before, after):
        guild = before.guild
        log_channel = await self.get_log_channel(guild)
        if log_channel:
            embed = disnake.Embed(title="Сообщение изменено", color=disnake.Color.blurple())
            embed.add_field(name="Автор", value=before.author.mention)
            embed.add_field(name="Канал", value=before.channel.mention)
            embed.add_field(name="Изменения", value=f"**До**: {before.content}\n**После**: {after.content}")
            await log_channel.send(embed=embed.set_footer(text="Molzy Production", icon_url=self.bot.user.avatar))

    @commands.Cog.listener("on_member_update")
    async def on_member_update(self, before, after):
        guild = before.guild
        log_channel = await self.get_log_channel(guild)
        if log_channel:
            if before.roles != after.roles:
                member = after
                roles_before = [role.name for role in before.roles]
                roles_after = [role.name for role in after.roles]
                added_roles = [role for role in roles_after if role not in roles_before]
                removed_roles = [role for role in roles_before if role not in roles_after]
                embed = disnake.Embed(title="Роли изменены", color=disnake.Color.blurple())
                embed.add_field(name="Пользователь", value=member.mention)
                if added_roles:
                    embed.add_field(name="Добавлены роли", value=", ".join(added_roles))
                if removed_roles:
                    embed.add_field(name="Удалены роли", value=", ".join(removed_roles))
                await log_channel.send(embed=embed.set_footer(text="Molzy Production", icon_url=self.bot.user.avatar))

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def setlogchannel(self, ctx, channel: disnake.TextChannel):
        guild = ctx.guild
        if channel:
            settings = self.load_log_channel_settings()
            settings[str(guild.id)] = str(channel.id)
            self.save_log_channel_settings(settings)
            await ctx.send(f"Канал {channel.mention} был установлен как канал для логов")
        else:
            embed = disnake.Embed(title="❌ Ошибка", description="Укажите существующий текстовый канал для логов!", color=disnake.Color.red())
            await ctx.send(embed=embed.set_footer(text="Molzy Production", icon_url=self.bot.user.avatar))

    async def get_log_channel(self, guild):
        settings = self.load_log_channel_settings()
        guild_id = str(guild.id)
        if guild_id in settings:
            channel_id = settings[guild_id]
            return guild.get_channel(int(channel_id))
        return None

    def load_log_channel_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as file:
                return json.load(file)
        return {}

    def save_log_channel_settings(self, settings):
        with open(SETTINGS_FILE, "w") as file:
            json.dump(settings, file)

def setup(bot: commands.Bot):
    bot.add_cog(LogsCog(bot))