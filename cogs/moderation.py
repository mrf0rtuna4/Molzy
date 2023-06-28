import disnake
from disnake.ext import commands
import string
import random
import os
from datetime import timedelta
import shutil
import typing

class ModerationCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_punish_channel(self, ctx, channel: disnake.TextChannel):
        saved_channel_id = self.load_channel_id(ctx.guild.id)
        if saved_channel_id is not None:
            emb = disnake.Embed(
                title="❌ Ошибка",
                description="На этом сервере уже установлен канал для отправки сообщений о нарушениях.",
                color=0xFF0004
            )
            await ctx.send(embed=emb)
            return

        self.save_channel_id(ctx.guild.id, channel.id)
        emb = disnake.Embed(
            title="✅ Готово!",
            description=f"Канал {channel.mention} успешно установлен для отправки сообщений о нарушениях.",
            color=disnake.Color.blurple()
        )
        await ctx.send(embed=emb)

    def remove_channel_id(self, guild_id):
        lines = []
        with open("punish.txt", "r") as file:
            lines = file.readlines()

        with open("punish.txt", "w") as file:
            for line in lines:
                saved_guild_id = line.strip().split(":")
                if len(saved_guild_id) < 2:
                    continue
                saved_guild_id, _ = saved_guild_id
                if str(guild_id) != saved_guild_id:
                    file.write(line)

    @commands.slash_command(name="change-punish", description="Изменяет канал для отправки выданных наказаний")
    @commands.has_permissions(administrator=True)
    async def change_punish_channel(self, ctx, channel: disnake.TextChannel):
        saved_channel_id = self.load_channel_id(ctx.guild.id)
        if saved_channel_id is None:
                emb = disnake.Embed(
                    title="❌ Ошибка",
                    description="На этом сервере еще не установлен канал для отправки сообщений о нарушениях.",
                    color=0xFF0004
                    )
                await ctx.response.send_message(embed=emb, ephemeral=True)
                return
        
        self.remove_channel_id(ctx.guild.id)  
        self.save_channel_id(ctx.guild.id, channel.id)
            
        self.save_channel_id(ctx.guild.id, channel.id)
        emb = disnake.Embed(
                title="✅ Готово!",
                description=f"Канал для отправки сообщений о нарушениях успешно изменен на {channel.mention}.",
                color=disnake.Color.blurple()
                )
        await ctx.response.send_message(embed=emb)

    @commands.slash_command(name="password", description="Генерирует случайный пароль.")
    async def password(self, ctx, length=None):
        if length is None:
            length = random.randint(8, 23)
        else:
            length = int(length)

        if length > 24:
            emb = disnake.Embed(title="❌ Ошибка", description="Длина пароля не может превышать 24 символа.", color=0xFF0004)
            await ctx.response.send_message(embed = emb, ephemeral = True)
            return
        if length < 8:
            emb1 = disnake.Embed(title="❌ Ошибка", description="Длина пароля не может быть ниже 8 символов.", color=0xFF0004)
            await ctx.response.send_message(embed = emb1, ephemeral = True)
            return

        password_characters = string.ascii_letters + string.digits + string.punctuation

        password = ''.join(random.choice(password_characters) for _ in range(length))

        await ctx.response.send_message(f"Ваш пароль: `{password}`", ephemeral=True)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=1):
        messages = await ctx.channel.history(limit=amount + 1).flatten()
        await ctx.channel.delete_messages(messages)
        
        embed = disnake.Embed(title="✅ Чат очищен!", description=f"Было удалено **{amount}** сообщение(-я; -ий)!", color=0x50c878)
        author = ctx.author
        embed.set_footer(text=f"Спасибо за очистку, {author.name}!", icon_url=author.avatar.url)
        await ctx.send(embed=embed)

    @commands.slash_command(name="message", description="Отправь сообщение пользователю через бота.")
    async def message(ctx,member:disnake.Member,*,msg):
            author2 = ctx.author.mention
            author = ctx.author
            await ctx.response.send_message(f"Проверяю и отправляю твоё сообщение {author2}...")
            
            await member.send(embed=disnake.Embed(title=f"**Вам поступило новое сообщение от {author.name} !**",description=f"{msg}",colour=disnake.Colour.blue()))

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, user: disnake.Member, *, reason=None):
        author = ctx.author

        warnings_folder = "warnings"
        guild_folder = f"{warnings_folder}/{ctx.guild.id}"
        user_warnings_folder = f"{guild_folder}/{user.id}"

        if not os.path.exists(warnings_folder):
            os.makedirs(warnings_folder)

        if not os.path.exists(guild_folder):
            os.makedirs(guild_folder)

        if not os.path.exists(user_warnings_folder):
            os.makedirs(user_warnings_folder)

        warning_count = self.get_warning_count(user, ctx.guild)

        warning_count += 1
        self.add_warning(user, ctx.guild, warning_count, reason)

        await ctx.message.add_reaction("✅")
        
        saved_channel_id = self.load_channel_id(ctx.guild.id)
        if saved_channel_id:
            channel = self.bot.get_channel(saved_channel_id)
            if channel:
                warning_message = disnake.Embed(
                    title="⚠️ Информация о варне:",
                    description=f"Администратор: {author.mention} \nВарн выдан: {user.mention} \n\nПричина: **{reason or 'Не указана'}**. \nКол-во предупреждений: **{warning_count}**",
                    color=0x740B0B
                )
                await channel.send(embed=warning_message)
            else:
                print("Канал не найден.")


    def add_warning(self, user, guild, warning_count, reason):
        guild_folder = f"warnings/{guild.id}"
        user_warnings_folder = f"{guild_folder}/{user.id}"
        warning_file = f"{user_warnings_folder}/{warning_count}.txt"

        with open(warning_file, "w") as f:
            f.write(reason)


    def get_warning_count(self, user, guild):
        guild_folder = f"warnings/{guild.id}"
        user_warnings_folder = f"{guild_folder}/{user.id}"
        warning_files = os.listdir(user_warnings_folder)

        return len(warning_files)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unwarn(self, ctx, user: disnake.Member, count: int = 1):
        if count <= 0:
            await ctx.send("Количество предупреждений для удаления должно быть положительным числом.")
            return

        warnings_folder = "warnings"
        guild_folder = f"{warnings_folder}/{ctx.guild.id}"
        user_warnings_folder = f"{guild_folder}/{user.id}"

        if not os.path.exists(user_warnings_folder):
            embed = disnake.Embed(
                title="❌ Ошибка",
                description=f"У пользователя {user.mention} нет предупреждений.",
                color=0xFF0004
            )
            await ctx.send(embed=embed)
            return

        warning_files = os.listdir(user_warnings_folder)
        warning_files.sort(reverse=True)

        if count >= len(warning_files):
            shutil.rmtree(user_warnings_folder)
            await ctx.message.add_reaction("✅")
        else:
            for i in range(count):
                warning_file = os.path.join(user_warnings_folder, warning_files[i])
                os.remove(warning_file)

            await ctx.message.add_reaction("✅")

        saved_channel_id = self.load_channel_id(ctx.guild.id)
        if saved_channel_id:
            channel = self.bot.get_channel(saved_channel_id)
            if channel:
                embed = disnake.Embed(
                    title="✅ Успешно",
                    description=f"У пользователя {user.mention} удалено **{count}** предупреждений(-е; -я).",
                    color=disnake.Color.green()
                )
                embed.set_footer(text="Molzy Production", icon_url=ctx.author.avatar)
                await channel.send(embed=embed)
            else:
                print("Канал не найден.")


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warns(self, ctx, user: disnake.Member):
        warnings_folder = "warnings"
        guild_folder = f"{warnings_folder}/{ctx.guild.id}"
        user_warnings_folder = f"{guild_folder}/{user.id}"

        if not os.path.exists(user_warnings_folder):
            embed = disnake.Embed(
                title="❌ Ошибка",
                description=f"У пользователя {user.mention} нет предупреждений.",
                color=0xFF0004
            )
            await ctx.send(embed=embed)
            return

        warning_files = os.listdir(user_warnings_folder)
        warning_count = len(warning_files)

        emb = disnake.Embed(
            title=f"Количество предупреждений {user.name}.",
            description=f"Он имеет **{warning_count}** предупреждений.",
            color=disnake.Color.blurple()
        )
        emb.set_thumbnail(url=user.avatar)
        emb.set_footer(text="Molzy Production", icon_url=ctx.author.avatar)
        await ctx.send(embed=emb)

    @commands.slash_command(name="timeout", description="Заткни рот этим нарушителям.")
    @commands.has_permissions(mute_members=True)
    async def timeout(self, ctx, member: disnake.Member, time: str, reason=None):
        unit = time[-1]
        value = int(time[:-1])

        if unit == 's':
            duration = timedelta(seconds=value)
            unit_name = 'Секунд'
        elif unit == 'm':
            duration = timedelta(minutes=value)
            unit_name = 'Минут'
        elif unit == 'h':
            duration = timedelta(hours=value)
            unit_name = 'Часов'
        elif unit == 'd':
            duration = timedelta(days=value)
            unit_name = 'Дней'
        else:
            emb = disnake.Embed(
                title="❌ Ошибка",
                description="Недопустимая единица измерения времени. Пожалуйста, используйте <s> для обозначения секунд, <m> для обозначения минут, <h> для обозначения часов или <d> для обозначения дней.",
                color=0xFF0004
            )
            await ctx.response.send_message(embed=emb, ephemeral=True)
            return
        
        await member.timeout(duration=duration, reason=reason)
        
        emb1 = disnake.Embed(
            title="✅ Готово!",
            description=f"Информация о тайм-ауте была выслана в канал с наказаниями.",
            color=disnake.Color.blurple()
        )
        emb1.set_footer(text="Molzy Production", icon_url=ctx.bot.user.avatar)
        await ctx.response.send_message(embed=emb1)

        saved_channel_id = self.load_channel_id(ctx.guild.id)
        if saved_channel_id:
            channel = self.bot.get_channel(saved_channel_id)
            if channel:
                embed = disnake.Embed(
                    title="✅ Тайм-Аут выдан!",
                    description=f"Пользователь {member.mention} больше не может разговаривать в течение **{value} {unit_name}**. Причина: {reason or 'Причина отсутствует.'}",
                    color=disnake.Color.blurple()
                )
                embed.set_footer(text="Molzy Production", icon_url=ctx.bot.user.avatar)
                await channel.send(embed=embed)
            else:
                print("Канал не найден.")

    @commands.command(pass_context=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: disnake.Member, *, reason):
        if member.top_role >= ctx.author.top_role:
            emb3 = disnake.Embed(
                title="❌ Ошибка",
                description="Вы не можете выгнать этого пользователя.",
                color=0xFF0004
            )
            await ctx.send(embed=emb3)
            return

        author = ctx.author
        if member.id == ctx.author.id:
            emb1 = disnake.Embed(
                title="⛔ Заблокировано.",
                description="Вы не можете выгнать с сервера **самого себя**.",
                color=0xFF0004
            )
            await ctx.send(embed=emb1)
            return

        await member.kick(reason=reason)
        await ctx.channel.purge(limit=0)
        await ctx.message.add_reaction("✅")

        saved_channel_id = self.load_channel_id(ctx.guild.id)
        if saved_channel_id:
            channel = self.bot.get_channel(saved_channel_id)
            if channel:
                embed = disnake.Embed(
                    title="🔨 Пользователь выгнан!",
                    description=f"Администратор {author.mention} выгнал пользователя {member.mention}. Причина: {reason or 'Причина отсутствует'}",
                    color=disnake.Color.random()
                )
                embed.set_footer(text="Molzy Production", icon_url=author.avatar)
                await channel.send(embed=embed)
            else:
                print("Канал не найден.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: typing.Union[int, str], *, reason: str = None):
        if isinstance(user, int):
            try:
                member = await self.bot.fetch_user(user)
            except disnake.NotFound:
                emb = disnake.Embed(title="❌ Ошибка", description="Пользователь не найден.", color=0xFF0004)
                await ctx.send(embed=emb)
                return
        elif isinstance(user, str):
            member = disnake.utils.get(ctx.guild.members, name=user)
            if member is None:
                emb = disnake.Embed(title="❌ Ошибка", description="Вы указали самого себя, либо несуществующего пользователя.", color=0xFF0004)
                await ctx.send(embed=emb)
                return
        else:
            emb = disnake.Embed(title="❌ Ошибка", description="Некорректный формат пользователя.", color=0xFF0004)
            await ctx.send(embed=emb)
            return

        await ctx.guild.ban(member, reason=reason)
        await ctx.message.add_reaction("✅")
        
        saved_channel_id = self.load_channel_id(ctx.guild.id)
        if saved_channel_id:
            channel = self.bot.get_channel(saved_channel_id)
            if channel:
                ban_message = disnake.Embed(title='⛔ Блокировка', description=f"Администратор {ctx.author.mention} заблокировал пользователя {member.mention}. \nПричина: **{reason or 'Причина отсутствует.'}**", color=0xFF0004)
                ban_message.set_footer(text="Molzy Production", icon_url=ctx.author.avatar)
                await channel.send(embed=ban_message)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int):
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user)
            embed = disnake.Embed(
                title='⛔ Блокировка разжалована',
                description=f"Пользователь {user.mention} разблокирован на сервере.",
                color=disnake.Color.green()
            )
            channel_id = self.load_channel_id(ctx.guild.id)
            channel = self.bot.get_channel(channel_id)
            await channel.send(embed=embed)
            await ctx.message.add_reaction("✅")
        except disnake.NotFound:
            embed = disnake.Embed(
                title="❌ Ошибка",
                description="Указанный пользователь не найден либо не забанен на этом сервере.",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)

    def save_channel_id(self, guild_id, channel_id):
        with open("punish.txt", "r+") as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                saved_guild_id, saved_channel_id = line.strip().split(":")
                if str(guild_id) == saved_guild_id:
                    if int(saved_channel_id) == channel_id:
                        continue
                file.write(line)
            file.write(f"{guild_id}:{channel_id}\n")
            file.truncate()

    def load_channel_id(self, guild_id):
        with open("punish.txt", "r+") as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                saved_guild_id, saved_channel_id = line.strip().split(":")
                if str(guild_id) == saved_guild_id:
                    channel = self.bot.get_channel(int(saved_channel_id))
                    if channel is None:
                        continue
                    return int(saved_channel_id)
                else:
                    file.write(line)
            file.truncate()
        return None

def setup(bot: commands.Bot):
    bot.add_cog(ModerationCog(bot))