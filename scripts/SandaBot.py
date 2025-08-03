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
    # 純粋な入室時のみ
    if before.channel is None and after.channel is not None:
        # 三田が入室したとき（1人目なら全員通知）
        if member.id == 823778651681193984 and len(after.channel.members) == 1:
            msg = f"@everyone 三田が現れた！"
            send_notify(msg)
        # ゆうな or もっさんが入室したとき（2人以上なら参戦通知）
        elif member.id == 918743342374854657 and len(after.channel.members) > 1:
            msg = f"ゆうなが参戦した！"
            send_notify(msg)
        elif member.id == 1200611206382243933 and len(after.channel.members) > 1:
            msg = f"もっさんが参戦した！"
            send_notify(msg)
        elif member.id == 491861700962942976 and len(after.channel.members) > 1:
            msg = f"こなかが参戦した！"
            send_notify(msg)
        elif member.id == 1401544325497884865 and len(after.channel.members) > 1:
            msg = f"いいんちょーが三田を殴りに来た！"
            send_notify(msg)

client.run(TOKEN)