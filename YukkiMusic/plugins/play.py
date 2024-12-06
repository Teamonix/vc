import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputAudioStream, InputStream
from pytgcalls.types.input_stream.quality import HighQualityAudio
from pytgcalls.exceptions import GroupCallNotFound
from youtube_dl import YoutubeDL
from YukkiMusic import app, bot, calls


# Download options
ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "%(title)s.%(ext)s",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
    "quiet": True,
}

# Start the PyTgCalls client
@calls.on_closed_voice_chat
async def close_chat(_, chat_id):
    print(f"Voice chat ended in chat: {chat_id}")


@app.on_message(filters.command("start"))
async def start_command(_, message):
    await message.reply("Hello! Use `/play <link>` to play audio/video in the voice chat.")


@app.on_message(filters.command("play") & filters.text)
async def play_command(_, message):
    chat_id = message.chat.id

    if len(message.command) < 2:
        await message.reply("❌ Please provide a link or text to play!")
        return

    query = " ".join(message.command[1:])
    await message.reply(f"🔍 Searching for `{query}`...")

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            file_name = ydl.prepare_filename(info)
            audio_stream = InputStream(
                InputAudioStream(file_name, HighQualityAudio())
            )
    except Exception as e:
        await message.reply(f"❌ Error: {e}")
        return

    try:
        calls.join_group_call(chat_id, audio_stream)
        await message.reply(f"✅ Now playing: **{info['title']}**")
    except GroupCallNotFound:
        await message.reply("❌ Please start a voice chat in this group first.")
    except Exception as e:
        await message.reply(f"❌ Error joining the call: {e}")


@app.on_message(filters.command("stop"))
async def stop_command(_, message):
    chat_id = message.chat.id
    try:
        calls.leave_group_call(chat_id)
        await message.reply("✅ Playback stopped.")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")
