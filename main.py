import discord
from discord.ext import commands
from keep_alive import keep_alive
import asyncio
import os

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 無音ループする関数
async def play_silence_loop(voice):
    while True:
        if not voice.is_playing():
            voice.play(discord.FFmpegPCMAudio(
                "silence.wav",
                before_options="-re",
                options="-filter:a volume=0.001"
            ))
        await asyncio.sleep(1)

@bot.command()
async def orusuban(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice = await channel.connect()

        # 無音ループ開始
        bot.loop.create_task(play_silence_loop(voice))

        await ctx.send("VC に参加しました！（無音ループ中）")
    else:
        await ctx.send("VCに入ってから使ってね！")

@bot.command()
async def oyasumi(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("退出しました！")
    else:
        await ctx.send("Bot はVCにいません。")

@bot.event
async def on_voice_state_update(member, before, after):
    voice_client = member.guild.voice_client
    if not voice_client:
        return

    channel = voice_client.channel
    humans = [m for m in channel.members if not m.bot]

    # 人間がいなくなっても抜けない（あなたの希望仕様）
    if len(humans) == 0:
        pass  # ここは何もしない＝残り続ける

keep_alive()
bot.run(os.environ["TOKEN"])
