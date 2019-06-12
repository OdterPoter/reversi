import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import os
import json
import inspect
import textwrap
import traceback
from contextlib import redirect_stdout
from discord.voice_client import VoiceClient
from discord import Game, Embed, Color, Status, ChannelType
from datetime import datetime
import discord.object
bot = commands.Bot(command_prefix= "#" )
radom_color_say=[0x32CD32, 0x4169E1, 0x9932CC]
@bot.event
async def on_ready():
    print("Reversi on")
bot.remove_command("help")   
@bot.event
async def on_member_join(member):
    jo = discord.Embed(description=f"Приветствуем на сервере дискорд проекта **Reversi**\n Я **{bot.user.name}** бот этого сервера, у меня есть команды для тебя, чтобы посмотреть их напиши команду #help в любом чате сервера, после чего я поставлю эмоджи <:yes:585843772626173953>. Надеюсь тебе здесь понравиться.\n Ссылка на Вконтакт - https://vk.com/reversiunturned", color=discord.Color.gold())
    jo.set_footer(text=f"{bot.user.name}", icon_url=bot.user.avatar_url)
    jo.set_author(name=member.guild.name, icon_url=member.guild.icon_url)
    await member.send(embed=jo)
    role = discord.utils.get(member.guild.roles, name="Игрок.")
    await member.add_roles(role) 
@bot.command()
async def coin(ctx):
    choice = random.randint(1,2)
    msg  = ctx.message
    if choice == 1:
        await msg.add_reaction("💿")
    if choice == 2:
        await msg.add_reaction("📀")
@bot.command(aliases=["si"])
async def serverinfo(ctx):
    em=discord.Embed(title=f"{ctx.message.guild.name}", color=discord.Color.magenta())
    em.add_field(name="Создатель сервера ", value=ctx.message.guild.owner.mention)
    em.add_field(name="Время когда был создан сервер", value=str(ctx.message.guild.created_at)[:16])
    em.add_field(name="Сколько участников на сервере", value=f"**{ctx.message.guild.member_count}** Игроков")
    reg = str(ctx.message.guild.region)
    if reg == str("russia"):
        reg = ("Россия")
    em.add_field(name="Регион", value=reg)
    afk = str(ctx.message.guild.afk_channel)
    if afk == str("None"):
        afk = ("Нету")
    em.add_field(name="AFK канал", value=afk)
    em.set_author(name=ctx.message.guild.name, icon_url=ctx.message.guild.icon_url)
    em.set_footer(text=f"Все права защищены {ctx.message.guild.name}", icon_url=ctx.message.guild.icon_url)
    await ctx.send(embed=em)
    await ctx.message.delete()
@bot.command(aliases=['pi'])
async def ping(ctx):
    await ctx.message.delete()
    ping = str(bot.latency * 100)[:2]
    em=discord.Embed(description=f"**Пинг {ping}**", colour=0x556B2F)
    msg = await ctx.send(embed=em)
    await msg.add_reaction('⏲')
@bot.command(aliases=['sym'])
@commands.has_permissions(manage_messages=True)
async def sayem(ctx,title, *, words):
    await ctx.message.delete()
    sayforem=discord.Embed(title=title, description=words, color=random.choice(radom_color_say))
    sayforem.set_author(name=f"Все права защищены {ctx.message.guild.name}", icon_url=ctx.message.guild.icon_url)
    sayforem.set_footer(text=str(ctx.message.created_at)[:16], icon_url='https://i.imgur.com/sxwgLq6.png')
    await ctx.send(embed=sayforem)
@bot.command(aliases=['ki'])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Не указана"):
    await ctx.message.delete()
    kicks = discord.Embed(description="**Ошибка**\n Не указан пользователь\n Попробуйте >kick @пользователь Причина!", color=discord.Color.red())
    if not member:
        await ctx.send(embed=kicks, delete_after=6)
    else:
        await ctx.guild.kick(member, reason=reason)
        em=discord.Embed(description=f"Был кикнут {member.mention}",colour=discord.Color.red())
        em.add_field(name="Причина", value=reason)
        em.set_footer(text=f"Все права защищены {ctx.message.guild.name}", icon_url=ctx.message.guild.icon_url)
        channel = bot.get_channel(id=588358136402935850)#ID Канала лог
        await channel.send(embed=em)
@bot.command(aliases=[''])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member=None, *, reason="Не указана"):
    await ctx.message.delete()
    bas = discord.Embed(description="**Ошибка**\n Не указан пользователь\n Попробуйте #ban `@пользователь` `Причина`!", color=discord.Color.red())
    if not member:
        await ctx.send(embed=bas, delete_after=6)
    else:
        await ctx.guild.ban(member, reason=reason)
        em=discord.Embed(description=f"Был забанен {member.mention}",colour=discord.Color.red())
        em.add_field(name="Причина", value=reason)
        em.set_footer(text=f"Все права защищены {ctx.message.guild.name}", icon_url=ctx.message.guild.icon_url)
        channel = bot.get_channel(id=588358136402935850)#ID Канала лог
        await channel.send(embed=em)
@bot.command(aliases=['mu'])
@commands.has_permissions(kick_members=True)
async def mute(ctx, member:discord.Member=None, tm="IF", *, reason="Без причины"):
    mts = discord.Embed(description="**Ошибка**\n Не указан пользователь\n Попробуйте >mute @пользователь Время(в минутах или IF навсегда!) Причина!", color=discord.Color.red())
    if not member:
        await ctx.send(embed=mts)
    await ctx.message.delete()
    if tm == "IF":
        mute = discord.Embed(title=f"Мут", description=f"Пользователь {member.mention} был замучен **навсегда**", color=discord.Color.red())
        mute.add_field(name="Дал мут:", value=ctx.author.mention)
        mute.add_field(name="Причина:", value=reason)
        mute.set_footer(text=f"Все права защищены {ctx.message.guild.name}", icon_url=ctx.message.guild.icon_url)
        role = discord.utils.get(ctx.message.guild.roles, name="Muted")
        await member.add_roles(role)
        channel = bot.get_channel(id=588358136402935850)#ID Канала лог
        await channel.send(embed=mute)
    else: 
        role = discord.utils.get(ctx.message.guild.roles, name= "Muted")
        mute= discord.Embed(title="Мут", description=f"Пользователь {member.mention} был замучен на **{tm}** минут", color=discord.Color.red())
        mute.add_field(name="Дал мут:", value=ctx.author.mention)
        mute.add_field(name="Причина:", value=reason)
        mute.set_footer(text=f"Все права защищены {ctx.message.guild.name}", icon_url=ctx.message.guild.icon_url)
        unmute= discord.Embed(title="Размут", description=f"Пользователь {member.mention} был размучен", color=discord.Color.green())
        unmute.set_footer(text=f"Все права защищены {ctx.message.guild.name}", icon_url=ctx.message.guild.icon_url)
        t = (int(tm) * 60)
        await member.add_roles(role)
        channel = bot.get_channel(id=588358136402935850)#ID Канала лог
        await channel.send(embed=mute)
        await asyncio.sleep(t)
        await member.remove_roles(role)
        channel = bot.get_channel(id=588358136402935850)#ID Канала лог
        await channel.send(embed=unmute)
@bot.command()
@commands.has_permissions(manage_messages=True)
async def d(ctx, message:int):
        if message > 300:
            messages = 300 
        em=discord.Embed(description=f"Удаляем {message} сообщений", colour=discord.Color.dark_red())
        await ctx.channel.purge(limit=message + 1)
        em1=discord.Embed(description=f":white_check_mark: Сообщений удалено: {message}", color=discord.Color.red())
        message2 = await ctx.send(embed=em)
        await asyncio.sleep(0.3)
        await message2.edit(embed=em1, delete_after=6)
@bot.command()
async def io(ctx, mem: discord.Member = None):
    await ctx.message.delete()
    mem = ctx.author if not mem else mem
    em=discord.Embed(title=f":mega: Информация о {mem.name}", colour=0x87CEEB)
    em.add_field(name=":pushpin: Имя", value=mem.name)
    em.add_field(name=":clock12: Когда зашёл на сервер", value= str(mem.joined_at)[:16])
    em.add_field(name=":key: Ид", value=mem.id)
    em.add_field(name=":clock12: Когда был создан аккаунт", value= str(mem.created_at)[:16])
    em.add_field(name="Роли", value=', '.join([f"<@&{roletop.id}>" for roletop in mem.roles if roletop is not ctx.guild.default_role]) if len(mem.roles) > 1 else 'Нет ролей', inline=False)
    stat = str(mem.status)
    if stat == str("dnd"):
        stat = ("Не беспокоить")
    if stat == str("online"):
        stat = ("Онлайн")
    if stat == str("idle"):
        stat = ("Нет на месте")
    if stat == str("offline"):
        stat = ("Не в сети")
    em.add_field(name="Статус", value=stat, inline=True)
    em.add_field(name="Топ роль", value=mem.top_role.mention)
    em.set_thumbnail(url=mem.avatar_url)
    em.set_author(name=bot.user.name, url=bot.user.avatar_url)
    em.set_footer(text=f"Все права защищены {ctx.message.guild.name}", icon_url=ctx.message.guild.icon_url)
    await ctx.send(embed=em)
@bot.command()
async def kiss(ctx, member: discord.Member = None):
    await ctx.message.delete()
    author = ctx.author
    kissgif_im = [
        "https://media1.tenor.com/images/45e529c116a1758fd09bdb27e2172eca/tenor.gif?itemid=11674749",
        "https://media1.tenor.com/images/104b52a3be76b0e032a55df0740c0d3b/tenor.gif?itemid=10194764",
    ]
    choice = random.randint(1,2)
    kiss_author=discord.Embed(description=f"{author.mention} Захотел целоваться :heart: :heart: :heart: ", color=discord.Color.purple())
    kiss_author.set_image(url=kissgif_im[0])
    if not member:
        await ctx.send(embed=kiss_author)
    else:
        if choice == 1:
            kissgif = discord.Embed(description=f"{author.mention} Поцеловал {member.mention}",color=discord.Color.purple())
            kissgif.set_image(url=kissgif_im[0])
            await ctx.send(embed=kissgif)
        if choice == 2:
            kissgif = discord.Embed(description=f"{author.mention} Целует {member.mention}",color=discord.Color.purple())
            kissgif.set_image(url=kissgif_im[1])
            await ctx.send(embed=kissgif)
@bot.command(aliases=['pch'])
async def punch(ctx, member: discord.Member=None):
    await ctx.message.delete()
    punchs_im = [
        "https://media1.tenor.com/images/0422c84416d4ee4466f56936a1a12b10/tenor.gif?itemid=13627939",
        "https://media1.tenor.com/images/df8af24e5756ecf4a4e8af0c9ea6499b/tenor.gif?itemid=4902917",
        "https://media.tenor.com/images/ff0f99b9f8d5aa75657fefd0178dc0c5/tenor.gif",
    ]
    choice = random.randint(1,3)
    punch_em = discord.Embed(description=f"{ctx.author.mention} Хочет драться :punch: ", color=discord.Color.red())
    punch_em.set_image(url=punchs_im[0])
    if not member:
        await ctx.send(embed=punch_em)
    else:
        if choice == 1:
            punch_em = discord.Embed(description=f"{ctx.author.mention} Ударил {member.mention}", color=discord.Color.dark_red())
            punch_em.set_image(url=punchs_im[0])
            await ctx.send(embed=punch_em)
        if choice == 2:
            punch_em = discord.Embed(description=f"{ctx.author.mention} Ударил {member.mention}", color=discord.Color.dark_red())
            punch_em.set_image(url=punchs_im[1])
            await ctx.send(embed=punch_em)
        if choice == 3:
            punch_em = discord.Embed(description=f"{ctx.author.mention} Ударил {member.mention}", color=discord.Color.dark_red())
            punch_em.set_image(url=punchs_im[2])
            await ctx.send(embed=punch_em)
@bot.command(aliases=['ary'])
async def angry(ctx, member:discord.Member=None):
    await ctx.message.delete()
    angry_im = [
        "https://media1.tenor.com/images/12b3b5a0fd2ff64136509dea171b1df4/tenor.gif?itemid=11667704",
        "https://media1.tenor.com/images/33e888c1661b2ce9027618a10f596043/tenor.gif?itemid=4700004",
    ]
    choice = random.randint(1,2)
    angry_em=discord.Embed(description=f"{ctx.author.mention} Злиться", color=discord.Color.red())
    angry_em.set_image(url=angry_im[0])
    if not member:
        await ctx.send(embed=angry_em)
    else:
        if choice == 1:
            angry_em=discord.Embed(description=f"{ctx.author.mention} Злиться на {member.mention}", color=discord.Color.red())
            angry_em.set_image(url=angry_im[0])
            await ctx.send(embed=angry_em)
        if choice == 2:
            angry_em=discord.Embed(description=f"{ctx.author.mention} Злиться на {member.mention}", color=discord.Color.red())
            angry_em.set_image(url=angry_im[1])
            await ctx.send(embed=angry_em)
@bot.command()
async def hug(ctx, member:discord.Member=None):
    await ctx.message.delete()
    im = [
        "https://media1.tenor.com/images/68f16d787c2dfbf23a4783d4d048c78f/tenor.gif?itemid=9512793",
        "https://media1.tenor.com/images/fd47e55dfb49ae1d39675d6eff34a729/tenor.gif?itemid=12687187",
    ]
    choice = random.randint(1,2)
    em=discord.Embed(description=f"{ctx.author.mention} Хочет обнимашек", color=discord.Color.red())
    em.set_image(url=im[0])
    em.set_footer(text=f"{bot.user.name}", icon_url=bot.user.avatar_url)
    if not member:
        await ctx.send(embed=em)
    else:
        if choice == 1:
            em=discord.Embed(description=f"{ctx.author.mention} Обнимает {member.mention}", color=discord.Color.red())
            em.set_image(url=im[0])
            em.set_footer(text=f"{bot.user.name}", icon_url=bot.user.avatar_url)
            await ctx.send(embed=em)
        if choice == 2:
            em=discord.Embed(description=f"{ctx.author.mention} Обнимает {member.mention}", color=discord.Color.red())
            em.set_image(url=im[1])
            em.set_footer(text=f"{bot.user.name}", icon_url=bot.user.avatar_url)
            await ctx.send(embed=em)
@bot.command()
async def sad(ctx, member:discord.Member=None):
    await ctx.message.delete()
    im = [
        "https://media1.tenor.com/images/53e5f4f09f98a2b090ef3f588d53b2f7/tenor.gif?itemid=5586925",
        "https://media1.tenor.com/images/44396a8da3c65f507608a970581fbc94/tenor.gif?itemid=3518394",
    ]
    choice = random.randint(1,2)
    em=discord.Embed(description=f"{ctx.author.mention} Грустит", color=discord.Color.red())
    em.set_image(url=im[0])
    em.set_footer(text=f"{bot.user.name}", icon_url=bot.user.avatar_url)
    if not member:
        await ctx.send(embed=em)
    else:
        if choice == 1:
            em=discord.Embed(description=f"{ctx.author.mention} Грустит из-за его {member.mention}", color=discord.Color.red())
            em.set_image(url=im[0])
            em.set_footer(text=f"{bot.user.name}", icon_url=bot.user.avatar_url)
            await ctx.send(embed=em)
        if choice == 2:
            em=discord.Embed(description=f"{ctx.author.mention} Грустит из-за его {member.mention}", color=discord.Color.red())
            em.set_image(url=im[1])
            em.set_footer(text=f"{bot.user.name}", icon_url=bot.user.avatar_url)
            await ctx.send(embed=em)
@bot.command()
async def help(ctx):
    msg = ctx.message
    em = discord.Embed(title="Команды бота", color=discord.Color.gold(), description="""
    #coin - "Подбросить монетку" Бот сам добавит вам реакцию Орла - 📀 и Решки 💿\n
    #serverinfo(si) - Узнать информацию о сервере\n
    #ping - Узнать пинг бота\n
    #io - Посмотреть информацию о пользователе\n
    #kiss - Поцеловать игрока\n
    #punch - Ударить игрока\n
    #angry - Злиться на игрока\n
    #hug - Обнять кого-то\n
    #sad - Грустить
    """)
    await msg.add_reaction(':yes:585843772626173953')
    em.set_footer(text=f"{bot.user.name}", icon_url=bot.user.avatar_url)
    await ctx.author.send(embed=em)
@bot.command(aliases=["ru"])
async def randomuser(ctx):
    await ctx.message.delete()
    bot = ctx.bot
    members = ctx.guild.members 
    wi = random.choice(members)
    wi_em = discord.Embed( description=f"Был выбран {wi.mention}", color=discord.Color.green())
    ms = await ctx.send(embed=wi_em)
    await ms.add_reaction('🎉')
async def chng_pr():
    await bot.wait_until_ready()
    while not bot.is_closed():
        await bot.change_presence(activity=discord.Streaming(name="на сервере Reversi ♾",url='https://www.twitch.tv/odter_oo7'), status=discord.Status.online)
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Streaming(name=f"unturnedreversi.gamestores.ru",url='https://www.twitch.tv/odter_oo7'), status=discord.Status.idle)
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Streaming(name=f"vk.com/reversiunturned",url='https://www.twitch.tv/odter_oo7'), status=discord.Status.dnd)
        await asyncio.sleep(10)
bot.loop.create_task(chng_pr())
token=os.environ.get('bot_token')
bot.run(token)

