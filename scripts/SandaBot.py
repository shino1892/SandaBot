import discord
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("SANDA_BOT_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

client = discord.Client(intents=intents)

def send_notify(message):
    channel_id = 1329714791442284566  # SandaBotの通知用チャンネルID
    channel = client.get_channel(channel_id)
    if channel:
        mention = f"@everyone"
        send_msg = f"{mention} {message}"
        import asyncio
        asyncio.run_coroutine_threadsafe(channel.send(send_msg), client.loop)
    else:
        print(f"チャンネルが見つかりません。通知を送信できません。")

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        if member.id == 823778651681193984 and len(after.channel.members) == 1:
            msg = f"三田が現れた！"
            send_notify(msg)

@client.event
async def on_presence_update(before, after):
    target_user_id = 491861700962942976  # こなかのID
    if after.id != target_user_id:
        return

    before_games = {a.name for a in before.activities if a.type == discord.ActivityType.playing}
    after_games = {a.name for a in after.activities if a.type == discord.ActivityType.playing}

    new_games = after_games - before_games

    if new_games:
        game_list = ', '.join(new_games)
        msg = f"古中がゲームを始めた！"
        msg += f"{game_list}"
        send_notify(msg)

client.run(TOKEN)