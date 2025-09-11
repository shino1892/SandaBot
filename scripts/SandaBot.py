import discord
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("SANDA_BOT_TOKEN")
GENERALCHAT = int(os.getenv("GENERAL_CHAT_ID"))

SANDA_ID = int(os.getenv("SANDA_ID"))
YUNA_ID = int(os.getenv("YUNA_ID"))
MOSAN_ID = int(os.getenv("MOSAN_ID"))
KONAKA_ID = int(os.getenv("KONAKA_ID"))
INCHO_ID = int(os.getenv("INCHO_ID"))
SHINO_ID = int(os.getenv("SHINO_ID"))

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.message_content = True  

client = discord.Client(intents=intents)

def send_notify(message):
    channel_id = GENERALCHAT  # SandaBotの通知用チャンネルID
    channel = client.get_channel(channel_id)
    if channel:
        import asyncio
        asyncio.run_coroutine_threadsafe(channel.send(message), client.loop)
    else:
        print(f"チャンネルが見つかりません。通知を送信できません。")

@client.event
async def on_voice_state_update(member, before, after):
    # print(f"ボイスアップデート")
    # 純粋な入室時のみ
    if before.channel is None and after.channel is not None:
        # print(f"入出検知")
        # print(member.id)
        # print(type(member.id))
        # 三田が入室したとき（1人目なら全員通知）
        if member.id == SANDA_ID and len(after.channel.members) == 1:
            msg = f"@everyone 三田が現れた！"
            send_notify(msg)
        # ゆうな or もっさんが入室したとき（2人以上なら参戦通知）
        elif member.id == YUNA_ID and len(after.channel.members) > 1:
            msg = f"ゆうなが参戦した！"
            send_notify(msg)
        elif member.id == MOSAN_ID and len(after.channel.members) > 1:
            msg = f"もっさんが参戦した！"
            send_notify(msg)
        elif member.id == KONAKA_ID and len(after.channel.members) > 1:
            msg = f"こなかが参戦した！"
            send_notify(msg)
        elif member.id == INCHO_ID and len(after.channel.members) > 1:
            msg = f"いいんちょーが三田を殴りに来た！"
            send_notify(msg)

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    sanda_words = ["三田", "さんだ", "サンダ", "sanda", "SANDA", "Sanda"]
    if any(word in message.content for word in sanda_words):
        await message.delete()
        sanda = f"<@{SANDA_ID}>"
        await message.channel.send(f"いけ！ {sanda} でてこい！")

    # コマンド処理も忘れずに
    await client.process_commands(message)


client.run(TOKEN)