import discord
from discord.ext import commands, tasks
import os

from random import choice

bot = commands.Bot(command_prefix='?', case_insensitive=True)
TOKEN = 'ODEwMTgxNDkxMzg4NzEwOTQy.YCf6Tw.GdY8-RK_1oHSJd1rApesIrPztgI'


# 상태 랜덤
status = ['혈귀 멸살', '귀멸학원 교사', '멍때리기']


# Read the Data files and store them in a variable
TokenFile = open("./data/Token.txt", "r") # Make sure to paste the token in the txt file
TOKEN = TokenFile.read()

OWNERID = 459325415463321611


# 봇 구동시 메시지와 상태 변경 시작
@bot.event
async def on_ready():
    change_status.start()
    print('[알림][冨岡 義勇 봇(음악)이 성공적으로 구동되었습니다.]')


# 서버 입성 인사
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='general')
    await channel.send(f'어서와라 {member.mention}')


# 음성 채널 노래
# A simple and small ERROR handler
@bot.event
async def on_command_error(ctx,error):
    embed = discord.Embed(
    title='',
    color=discord.Color.blue())
    if isinstance(error, commands.CommandNotFound):
        pass
    if isinstance(error, commands.MissingPermissions):
        embed.add_field(name=f'Invalid Permissions', value=f'You dont have {error.missing_perms} permissions.')
        await ctx.send(embed=embed)
    else:
        embed.add_field(name = f':x: Terminal Error', value = f"```{error}```")
        await ctx.send(embed = embed)
        raise error

# Load command to manage our "Cogs" or extensions
@bot.command()
async def load(ctx, extension):
    # Check if the user running the command is actually the owner of the bot
    if ctx.author.id == OWNERID:
        bot.load_extension(f'Cogs.{extension}')
        await ctx.send(f"Enabled the Cog!")
    else:
        await ctx.send(f"You are not cool enough to use this command")

# Unload command to manage our "Cogs" or extensions
@bot.command()
async def unload(ctx, extension):
    # Check if the user running the command is actually the owner of the bot
    if ctx.author.id == OWNERID:
        bot.unload_extension(f'Cogs.{extension}')
        await ctx.send(f"Disabled the Cog!")
    else:
        await ctx.send(f"You are not cool enough to use this command")

# Reload command to manage our "Cogs" or extensions
@bot.command(name = "reload")
async def reload_(ctx, extension):
    # Check if the user running the command is actually the owner of the bot
    if ctx.author.id == OWNERID:
        bot.reload_extension(f'Cogs.{extension}')
        await ctx.send(f"Reloaded the Cog!")
    else:
        await ctx.send(f"You are not cool enough to use this command")

# Automatically load all the .py files in the Cogs folder
for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'Cogs.{filename[:-3]}')
        except Exception:
            raise Exception
#

# 간단한 대화 메시지
@bot.command()
async def 안녕(ctx):
    embed = discord.Embed(color=discord.Colour.blue(), title="난 토미오카 기유 라고 한다")
    await ctx.message.channel.send(embed=embed)

# 랜덤 답변 메시지
@bot.command()
async def 요즘뭐해(ctx):
    responses = ['평소처럼 혈귀들을 잡는다', '귀멸학원 교사를 한다', '...']
    await ctx.send(choice(responses))

# 상태 랜덤 변경
@tasks.loop(seconds=60)
async def change_status():
    await bot.change_presence(activity=discord.Game(choice(status)))


bot.run(os.environ['token'])
