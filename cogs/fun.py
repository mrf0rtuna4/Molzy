import disnake
from disnake.ext import commands
import random
from random import randint, choices

img_bite = ["https://media.tenor.com/jLoppoafD5EAAAAC/bite.gif", "https://media.tenor.com/y91DzE22_V4AAAAM/anime-bite.gif", "https://media.tenor.com/hd1lz8G0RdwAAAAM/anime-bite.gif", "https://media.tenor.com/ECCpi63jZlUAAAAC/anime-bite.gif", "https://media.tenor.com/1LtA9dSoAIQAAAAC/zero-no-tsukaima-bite.gif"]
img_hug = ["https://media.tenor.com/4D5jSREXInMAAAAd/anime-couple-hug.gif", "https://media.tenor.com/lzKyZchfMzAAAAAM/anime-hug.gif", "https://media.tenor.com/Ct4bdr2ZGeAAAAAC/teria-wang-kishuku-gakkou-no-juliet.gif", "https://media.tenor.com/vpE5_F_oqmsAAAAC/run-hug-hug.gif", "https://media.tenor.com/mB_y2KUsyuoAAAAM/cuddle-anime-hug.gif", "https://media.tenor.com/HYkaTQBybO4AAAAC/hug-anime.gif", "https://media.tenor.com/J7eGDvGeP9IAAAAC/enage-kiss-anime-hug.gif"]
img_kiss = ["https://media.tenor.com/bc4ycl93pIEAAAAC/engage-kiss-anime-kiss.gif", "https://media.tenor.com/IzoHEmuz3u8AAAAM/anime-kiss.gif", "https://media.tenor.com/Sjz7_-I6aCUAAAAd/engage-kiss-kisara.gif", "https://media.tenor.com/Be95uIOnMhEAAAAd/kiss-love.gif", "https://media.tenor.com/U2jTGdkrmloAAAAC/kiss.gif", "https://media.tenor.com/0NYKdRkFwu8AAAAC/yui-komori-ayato-sakamaki.gif", "https://media.tenor.com/TnjL6WcdkkwAAAAd/anime-kiss.gif", "https://media.tenor.com/Ko1AOLzUmyEAAAAd/kiss-anime.gif", "https://media.tenor.com/F02Ep3b2jJgAAAAC/cute-kawai.gif"]
img_boobs = ["https://media.discordapp.net/attachments/1046501823898460230/1096040662253699183/Hjb-min.gif?width=719&height=516", "https://media.discordapp.net/attachments/1046501823898460230/1096040700455424060/7b2e59cebb2f-min.gif?width=539&height=304", "https://cdn.discordapp.com/attachments/1046501823898460230/1095756911942574090/hentay-na-telefon.gif", "https://media.discordapp.net/attachments/1046501823898460230/1095756963289235547/15019452.gif?width=557&height=323", "https://images-ext-1.discordapp.net/external/e8Zo8y3l58tg0ZJttQXnqfaRN89YRcjHbaI3xZ8tf8Q/https/i.redd.it/vhms1i0jh2541.gif?width=719&height=405", "https://images-ext-1.discordapp.net/external/KVpeTULX2Z0KdpBIM2nfLqjulgkfUfoa3v69lLS6yU0/https/hentaigifz.com/content/2021/05/015_001.gif?width=712&height=506", "https://images-ext-1.discordapp.net/external/yMhk31G9VrKfBSF4fdmoXOnH1PS7Bqwm3pZuvGsQLyM/https/i.redd.it/6iq1odjvx2c71.gif?width=816&height=700", "https://media.discordapp.net/attachments/1046501823898460230/1095756963641577612/76124401.gif?width=575&height=359", "https://media.discordapp.net/attachments/1046501823898460230/1095756908931063818/1.gif?width=700&height=700", "https://images-ext-1.discordapp.net/external/G9WzYxYfB9WX0C-XL24rVvkPalzQfU3-vtJMLy-X3Fs/https/psv4.vkuseraudio.net/s/v1/d/MRyQgWm_dcJQDcJyrG4ZDyHv12fzm3PhOi0JXv03oD5orlmqRiVJUvv3LTjemocRgRWryGMSNuNpwt6w9pm2Sadgjsh0F4hV7jVmSz9RamgplF7Nq7Wqpg/UjZbxHn.gif?width=933&height=700", "https://media.discordapp.net/attachments/1046501823898460230/1096040701046816870/111-min.gif?width=647&height=431", "https://media.discordapp.net/attachments/1046501823898460230/1095756910629769307/detail_2.gif?width=633&height=356", "https://media.discordapp.net/attachments/1046501823898460230/1096040699562033153/5e5a6a7ceaff-min.gif?width=539&height=330", "https://images-ext-1.discordapp.net/external/hwTJ7LC0bo_ZUUl11lwu_rwvT2H3Pi4MzuQAfx7pfcg/https/psv4.vkuseraudio.net/s/v1/d/mnVyU2P9zzZL__H3EflbkaulmNG-6iaLyK5HRn3Nd6Z3yQDq8boEbYkYGeYo6TvqjB444royWyxH5QyvTUAnafaCFt_xtOGm1zyM-2LDUnro2RT6yfUtgg/1.gif?width=494&height=699", "https://media.discordapp.net/attachments/1046501823898460230/1095756962223898744/660_1000.gif?width=287&height=377", "https://media.discordapp.net/attachments/1046501823898460230/1095756851355844618/tumblr_op6sq1bwTb1tjgwy0o2_540.gif?width=485&height=273", "https://cdn.discordapp.com/attachments/1046501823898460230/1096040661507129384/hentai-gif-Khentay-sekretnye-razdely-khentay-bez-tsenzury-3238780-min.gif", "https://media.discordapp.net/attachments/1046501823898460230/1096040702913282178/hentai-gif-Khentay-sekretnye-razdely-khentay-bez-tsenzury-3238778-min.gif?width=485&height=269"]
img_sucks = ["https://images-ext-1.discordapp.net/external/pccgaQu75K55a9ZZDV2vlTUsRhanSdzV0ZoQM32TlUM/https/i1.wp.com/static1.e621.net/data/23/5c/235cc857b70b31a6d6a5dacbc308ac9f.gif?width=757&height=535", "https://images-ext-2.discordapp.net/external/-YcpKiy-uCr2iaGR4Y_XGycmo91UAUxuLdccN3gVFeM/https/hentaigifz.com/content/2021/03/deep-suck_001.gif?width=557&height=544", "https://images-ext-1.discordapp.net/external/ShAmL_OIzSwNQjtQtrZfKpJpptIL1feDdpf9DgfS6RQ/https/psv4.vkuseraudio.net/s/v1/d/x6XHL3KOeKMuD-X3FQCK5qDQjClAvEy3cF9mwmeb5Y4AZiYcsSpWzjla7I2Ups0L27oJiV6PAF5pD3rFdey76kY5s_cetwDkWlezIbY4Z1A9dOrdOJb1Hg/14e4b8c33533b6a1bb2ee3b82114a5cf1b9fd3a6.gif?width=809&height=629", "https://thehentaigif.com/wp-content/uploads/2021/08/sucking6.gif", "https://psv4.vkuseraudio.net/s/v1/d/nqWnUohPZa_JKI5IkVwWaVZaaU9o9imyOG-bv9-FCOIfttFHHl0fS-4GJ8Pk5L_6qPwlwUUuRES3hWfh7ZFXJSa_YWy6AYuBAaWzswMPP5F6_XeiB3FTlA/circular-licks-on-your-foreskin-by-zankuro-from-e-c-m_001.gif", "https://64.media.tumblr.com/6e07949e179e394efcf858fb84ca82f6/tumblr_o4a47pYNGR1uao6a1o2_400.gif"]
img_slap = ["https://media.tenor.com/dHNqRCJQSnIAAAAd/slap-%E0%B8%99%E0%B8%8A.gif", "https://media.tenor.com/ZozZrvtEdAkAAAAM/slap.gif", "https://media.tenor.com/jgImPggI1ZMAAAAC/bakugo-anime-slap.gif", "https://media.tenor.com/zkZEHBM_fZIAAAAC/saitei-okoru.gif", "https://media.tenor.com/oYsWol5_exYAAAAM/slap.gif", "https://media.tenor.com/HueTCrExODkAAAAC/slap.gif"]
img_punch = ["https://media.tenor.com/RZ5_kz-MxdUAAAAC/anime-one-piece.gif", "https://media.tenor.com/vBguwqFg-MsAAAAM/kimihito-monster-musume.gif", "https://media.tenor.com/jUAUjptWieQAAAAC/doromizu-jirochou-punch.gif", "https://media.tenor.com/s0bU-NO1QIQAAAAC/anime-punch.gif", "https://media.tenor.com/p3Hgg8D0mFMAAAAC/anime-punch.gif", "https://media.tenor.com/SwMgGqBirvcAAAAC/saki-saki-kanojo-mo-kanojo.gif", "https://media.tenor.com/qDDsivB4UEkAAAAC/anime-fight.gif"]
img_pat = ["https://media.tenor.com/Hgt-mT0KXN0AAAAd/chtholly-tiat.gif", "https://media.tenor.com/K3N8ahlj2YoAAAAC/establife-anime-headpat.gif", "https://media.tenor.com/lVsnDFq21W8AAAAM/pat-head-anime.gif", "https://media.tenor.com/YaFzR7EkabYAAAAC/head-pat-anime.gif", "https://media.tenor.com/K54YVKbOkY8AAAAC/anime-pat.gif", "https://media.tenor.com/LpYeBetRjCQAAAAM/anime-pat.gif", "https://media.tenor.com/YGQYQKrSsCIAAAAM/anime-pat.gif", "https://media.tenor.com/r5F7BApTqwsAAAAC/anime-pat.gif", "https://media.tenor.com/TDqVQaQWcFMAAAAC/anime-pat.gif", "https://media.tenor.com/N41zKEDABuUAAAAC/anime-head-pat-anime-pat.gif", "https://media.tenor.com/pvF8xcytu1YAAAAC/pat.gif", "https://media.tenor.com/wLqFGYigJuIAAAAC/mai-sakurajima.gif"]
img_feed = ["https://media.tenor.com/tJG2atwlNL8AAAAM/anime-feed.gif", "https://media.tenor.com/xS09IqCS1e0AAAAd/anime-anime-boy.gif", "https://media.tenor.com/_qetTKAryEsAAAAC/miyabi-ito-ryu-yamada.gif", "https://media.tenor.com/Kpw8-sodxCcAAAAC/feed.gif", "https://media.tenor.com/Aflxvrwa0woAAAAC/kawaii-wholesome.gif", "https://media.tenor.com/y_xVq9Ea-YUAAAAC/anime-acchi-kocchi.gif"]

class FunCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def hug(self, ctx, member: disnake.Member = None):
            author = ctx.author
            if member == None:
                emb = disnake.Embed(title=f"**{author.name} обнял(а) сам себя.**", color=disnake.Color.random())
                emb.set_image(url=f'{random.choice(img_hug)}')
                emb.set_footer(text=f"Как ты это сделал {author.name}?", icon_url=author.avatar)
                await ctx.send(embed = emb)
                return
            if member == self.bot.user:
                emb1 = disnake.Embed(title=f"**{author.name} обнял(а) бота.**", color=disnake.Color.random())
                emb1.set_image(url=f'{random.choice(img_hug)}')
                emb1.set_footer(text=f"Обнимать металл? Да кто так делает {author.name}?", icon_url=author.avatar)
                await ctx.send(embed = emb1)
                return
            else:
                emb2 = disnake.Embed(title=f"**{author.name} обнял(а) {member.name}**", color=disnake.Color.random())
                emb2.set_image(url=f'{random.choice(img_hug)}')
                emb2.set_footer(text=f"Все заслуживают объятий, {author.name}!", icon_url=author.avatar)
                await ctx.send(embed = emb2)

    @commands.command()
    async def pat(self, ctx, member: disnake.Member = None):
            author = ctx.author
            if member == None:
                emb = disnake.Embed(title=f"**{author.name} погладил(а) сам себя.**", color=disnake.Color.random())
                emb.set_image(url=f'{random.choice(img_pat)}')
                emb.set_footer(text=f"🤨 {author.name}", icon_url=author.avatar)
                await ctx.send(embed = emb)
                return
            if member == self.bot.user:
                emb1 = disnake.Embed(title=f"**{author.name} погладил(а) бота.**", color=disnake.Color.random())
                emb1.set_image(url=f'{random.choice(img_pat)}')
                emb1.set_footer(text=f"Хватит гладить металл {author.name}.", icon_url=author.avatar)
                await ctx.send(embed = emb1)
                return
            else:
                emb2 = disnake.Embed(title=f"**{author.name} погладил(а) {member.name}**", color=disnake.Color.random())
                emb2.set_image(url=f'{random.choice(img_pat)}')
                emb2.set_footer(text=f"Милота, {author.name}).", icon_url=author.avatar)
                await ctx.send(embed = emb2)

    @commands.command()
    async def kiss(self, ctx, member: disnake.Member = None):
            author = ctx.author
            if member == None:
                emb = disnake.Embed(title=f"**{author.name} поцеловал(а) сам себя.**", color=disnake.Color.random())
                emb.set_image(url=f'{random.choice(img_kiss)}')
                emb.set_footer(text=f"ЧСВ..., {author.name}.", icon_url=author.avatar)
                await ctx.send(embed = emb)
                return
            if member == self.bot.user:
                emb1 = disnake.Embed(title=f"**{author.name} поцеловал(а) бота.**", color=disnake.Color.random())
                emb1.set_image(url=f'{random.choice(img_kiss)}')
                emb1.set_footer(text=f"Целовать металл глупо и бессмысленно {author.name}.", icon_url=author.avatar)
                await ctx.send(embed = emb1)
                return
            else:
                emb2 = disnake.Embed(title=f"**{author.name} поцеловал(а) {member.name}**", color=disnake.Color.random())
                emb2.set_image(url=f'{random.choice(img_kiss)}')
                emb2.set_footer(text=f"Поцелуй меня, {author.name}!", icon_url=author.avatar)
                await ctx.send(embed = emb2)

    @commands.command()
    async def slap(self, ctx, member: disnake.Member = None):
            author = ctx.author
            if member == None:
                emb = disnake.Embed(title=f"**{author.name} дал(а) пощёчину сам себе.**", color=disnake.Color.random())
                emb.set_image(url=f'{random.choice(img_slap)}')
                emb.set_footer(text=f"Не причиняй себе боль {author.name}.", icon_url=author.avatar)
                await ctx.send(embed = emb)
                return
            if member == self.bot.user:
                emb1 = disnake.Embed(title=f"**{author.name} дал(а) пощёчину боту.**", color=disnake.Color.random())
                emb1.set_image(url=f'{random.choice(img_slap)}')
                emb1.set_footer(text=f"Повторяюсь, бить металл бесполезно {author.name}.", icon_url=author.avatar)
                await ctx.send(embed = emb1)
                return
            else:
                emb2 = disnake.Embed(title=f"**{author.name} дал(а) пощёчину {member.name}**", color=disnake.Color.random())
                emb2.set_image(url=f'{random.choice(img_slap)}')
                emb2.set_footer(text=f"Ай! Было больно, {author.name}!", icon_url=author.avatar)
                await ctx.send(embed = emb2)

    @commands.command()
    async def punch(self, ctx, member: disnake.Member = None):
            author = ctx.author
            if member == None:
                emb = disnake.Embed(title=f"**{author.name} ударил(а) сам себя.**", color=disnake.Color.random())
                emb.set_image(url=f'{random.choice(img_punch)}')
                emb.set_footer(text=f"Зачем ты себя бьёшь {author.name}?", icon_url=author.avatar)
                await ctx.send(embed = emb)
                return
            if member == self.bot.user:
                emb1 = disnake.Embed(title=f"**{author.name} ударил(а) бота.**", color=disnake.Color.random())
                emb1.set_image(url=f'{random.choice(img_punch)}')
                emb1.set_footer(text=f"Бить металл бесполезно {author.name}.", icon_url=author.avatar)
                await ctx.send(embed = emb1)
                return
            else:
                emb2 = disnake.Embed(title=f"**{author.name} ударил(а) {member.name}**", color=disnake.Color.random())
                emb2.set_image(url=f'{random.choice(img_punch)}')
                emb2.set_footer(text=f"Что плохого он тебе сделал, {author.name}!?", icon_url=author.avatar)
                await ctx.send(embed = emb2)

    @commands.command()
    async def bite(self, ctx, member: disnake.Member = None):
            author = ctx.author
            if member == None:
                emb = disnake.Embed(title=f"**{author.name} укисил(а) сам себя.**", color=disnake.Color.random())
                emb.set_image(url=f'{random.choice(img_bite )}')
                emb.set_footer(text=f"Хватит причинять себе боль {author.name}.", icon_url=author.avatar)
                await ctx.send(embed = emb)
                return
            if member == self.bot.user:
                emb1 = disnake.Embed(title=f"**{author.name} укусил(а) бота.**", color=disnake.Color.random())
                emb1.set_image(url=f'{random.choice(img_bite)}')
                emb1.set_footer(text=f"Зачем ты укусил металл, {author.name}?", icon_url=author.avatar)
                await ctx.send(embed = emb1)
                return
            else:
                emb2 = disnake.Embed(title=f"**{author.name} укусил(а) {member.name}**", color=disnake.Color.random())
                emb2.set_image(url=f'{random.choice(img_bite)}')
                emb2.set_footer(text=f"Вкусно было {author.name}?", icon_url=author.avatar)
                await ctx.send(embed = emb2)

    @commands.command()
    async def feed(self, ctx, member: disnake.Member = None):
            author = ctx.author
            if member == None:
                emb = disnake.Embed(title=f"**{author.name} накормил(а) сам себя.**", color=disnake.Color.random())
                emb.set_image(url=f'{random.choice(img_feed)}')
                emb.set_footer(text=f"Приятного аппетита, {author.name}.", icon_url=author.avatar)
                await ctx.send(embed = emb)
                return
            if member == self.bot.user:
                emb1 = disnake.Embed(title=f"**{author.name} накормил(а) бота.**", color=disnake.Color.random())
                emb1.set_image(url=f'{random.choice(img_feed)}')
                emb1.set_footer(text=f"Зачем ты потратил еду в железяку, {author.name}?", icon_url=author.avatar)
                await ctx.send(embed = emb1)
                return
            else:
                emb2 = disnake.Embed(title=f"**{author.name} накормил(а) {member.name}**", color=disnake.Color.random())
                emb2.set_image(url=f'{random.choice(img_feed)}')
                emb2.set_footer(text=f"Как мило, {author.name}!", icon_url=author.avatar)
                await ctx.send(embed = emb2)
             

    @commands.command()
    async def suck(self, ctx, member: disnake.Member = None):
        if ctx.channel.is_nsfw():
            author = ctx.author
            if member == None:
                emb = disnake.Embed(title=f"**{author.name} отсосал(а) сам себе.**", color=disnake.Color.random())
                emb.set_image(url=f'{random.choice(img_sucks)}')
                emb.set_footer(text=f"КАКИМ ОБРАЗОМ ТЫ ОТСОСАЛ САМ СЕБЕ {author.name}?!", icon_url=author.avatar)
                await ctx.send(embed = emb)
                return
            if member == author:
                emb4 = disnake.Embed(title=f"**{author.name} отсосал(а) сам себе.**", color=disnake.Color.random())
                emb4.set_image(url=f'{random.choice(img_sucks)}')
                emb4.set_footer(text=f"КАКИМ ОБРАЗОМ ТЫ ОТСОСАЛ САМ СЕБЕ {author.name}?!", icon_url=author.avatar)
                await ctx.send(embed = emb4)
                return
            if member == self.bot.user:
                emb1 = disnake.Embed(title=f"**{author.name} отсосал(а) боту.**", color=disnake.Color.random())
                emb1.set_image(url=f'{random.choice(img_sucks)}')
                emb1.set_footer(text=f"Кремпай, {author.name}?", icon_url=author.avatar)
                await ctx.send(embed = emb1)
                return
            else:
                emb2 = disnake.Embed(title=f"**{author.name} отсосал(а) {member.name}**", color=disnake.Color.random())
                emb2.set_image(url=f'{random.choice(img_sucks)}')
                emb2.set_footer(text=f"Кремпай, {author.name}?", icon_url=author.avatar)
                await ctx.send(embed = emb2)
        else:
            embed = disnake.Embed(title="❌ Запрет к исполнению команды.", description="Данная команда предназначена **только** для NSFW канала.", color=0xff0004)
            await ctx.reply(embed = embed)
            return

    @commands.command()
    async def fuck(self, ctx, member: disnake.Member = None):
        if ctx.channel.is_nsfw():
            author = ctx.author
            if ctx.message.author.id == author:
                pass
            if member == None:
                emb = disnake.Embed(title=f"**{author.name} трахнул сам себя.**", color=disnake.Color.random())
                emb.set_image(url=f'{random.choice(img_boobs)}')
                emb.set_footer(text=f"Я промолчу {author.name}...", icon_url=author.avatar)
                await ctx.send(embed = emb)
                return
            else:
                emb2 = disnake.Embed(title=f"**{author.name} трахнул {member.name}**", color=disnake.Color.random())
                emb2.set_image(url=f'{random.choice(img_boobs)}')
                emb2.set_footer(text=f"やめてください {author.name}!", icon_url=author.avatar)
                await ctx.send(embed = emb2)
        else:
             embed = disnake.Embed(title="❌ Запрет к исполнению команды.", description="Данная команда предназначена **только** для NSFW канала.", color=0xff0004)
             await ctx.reply(embed = embed)
             return
        
    @commands.slash_command(name="avatar", description="Выводит аватар пользователя.")
    async def avatar(ctx, member: disnake.Member = None):
        author = ctx.author
        if not member:
            member = author
        
        avatar_url = member.avatar.url
        emb = disnake.Embed(color=disnake.Color.random())
        emb.set_author(name=member.name, icon_url=member.avatar.url)
        emb.set_image(url=avatar_url)
        emb.set_footer(text=f"Укради аватарку! Аой... Аватарку запросил {author.name}", icon_url=ctx.bot.user.avatar.url)
        await ctx.send(embed=emb)

    @commands.slash_command(name="ship", description="Создай влюблённую парочку❤️")
    async def ship(self, ctx, user1: disnake.User, user2: disnake.User):
        percantage = randint(1, 110)
        await ctx.response.defer()


        if percantage > 100:
              emb4 = disnake.Embed(title="МЕГА ЛЮБОВЬ ❤️❤️❤️", description=f"**{user1.name}** и **{user2.name}** любят друг друга на **{percantage}%**!!!!", color=disnake.Color.blurple())
              emb4.set_footer(text="СОВЕТ ВАМ ДА ЛЮБОВЬ, ГОЛУБКИ!!!", icon_url=ctx.bot.user.avatar.url)
              await ctx.send(embed = emb4)
              return
        if percantage == 50:
              emb3 = disnake.Embed(title="Друзья видимо)) <:da:1096300387654455347>", description=f"**{user1.name}** и **{user2.name}** любят друг друга на **{percantage}%**.", color=disnake.Color.blurple())
              emb3.set_footer(text="Что-то среднее, вы друзья?", icon_url=ctx.bot.user.avatar.url)
              await ctx.send(embed = emb3)
              return
        if percantage > 35:
              emb = disnake.Embed(title="Авввв! Шикарная парочка <:huggers:1094954190591242240>", description=f"**{user1.name}** и **{user2.name}** любят друг друга на **{percantage}%**!", color=disnake.Color.blurple())
              emb.set_footer(text="Тили, тили тесто! Жених и невеста, ха!", icon_url=ctx.bot.user.avatar.url)
              await ctx.send(embed = emb)
              return
        if percantage < 35:
              emb2 = disnake.Embed(title="Оу... <:death:1119998441767055420>", description=f"**{user1.name}** и **{user2.name}** любят друг друга на **{percantage}%**...", color=disnake.Color.blurple())
              emb2.set_footer(text="Любви не существует...", icon_url=ctx.bot.user.avatar.url)
              await ctx.send(embed = emb2)
              return
    @commands.slash_command(name="question", description="Задайте вопрос, боту)")
    async def question(self, ctx, *, prompt):
        phrases = ["Да.", "Нет.", "Возможно.", "Никогда."]
        prompt = str(prompt)
        embed = disnake.Embed(title=f"⟩ {prompt}", description=f"Мой ответ: {random.choice(phrases)}", color=disnake.Color.blurple())
        embed.set_footer(text="Molzy Production", icon_url=ctx.bot.user.avatar.url)
        await ctx.send(embed=embed)        
    
def setup(bot: commands.Bot):
    bot.add_cog(FunCog(bot))