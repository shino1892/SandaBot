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
        import asyncio
        asyncio.run_coroutine_threadsafe(channel.send(message), client.loop)
    else:
        print(f"チャンネルが見つかりません。通知を送信できません。")

@client.event
async def on_voice_state_update(member, before, after):
    # 入室
    if before.channel is None and after.channel is not None:
        if member.id == 823778651681193984 and len(after.channel.members) == 1:
            msg = f"@everyone 三田が現れた！"
            send_notify(msg)
    # チャンネル移動 or 既に入っているチャンネルでの状態変化
    elif before.channel is not None and after.channel is not None:
        # チャンネルが変わった場合のみ通知
        if before.channel != after.channel:
            if member.id == 918743342374854657 and len(after.channel.members) > 1:
                msg = f"ゆうなが参戦した！"
                send_notify(msg)
            elif member.id == 1200611206382243933 and len(after.channel.members) > 1:
                msg = f"もっさんが参戦した！"
                send_notify(msg)

client.run(TOKEN)