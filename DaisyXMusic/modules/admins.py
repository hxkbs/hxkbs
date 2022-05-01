from asyncio import QueueEmpty

from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls.types.input_stream import AudioPiped

from DaisyXMusic.function.admins import set
from DaisyXMusic.helpers.channelmusic import get_chat_id
from DaisyXMusic.helpers.decorators import authorized_users_only, errors
from DaisyXMusic.helpers.filters import command, other_filters
from DaisyXMusic.services.pytgcalls import pytgcalls
from DaisyXMusic.services.queues import queues

ACTV_CALLS = []


@Kl_t3.on_message(filters.command("adminreset"))
async def update_admin(client, message: Message):
    chat_id = get_chat_id(message.chat)
    set(
        chat_id,
        [
            member.user
            for member in await message.chat.get_members(filter="administrators")
        ],
    )
    await message.reply_text("تم تحديث ذاكرة التخزين المؤقت للمسؤول❇️ !")


@Kl_t3.on_message(command("pause") & other_filters)
@a_s_g_ki
@hJskpv
async def pause(_, message: Message):
    chat_id = get_chat_id(message.chat)
    for x in pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await message.reply_text("لا شيء يلعب❗ !")
    else:
        await pytgcalls.pause_stream(chat_id)
        await message.reply_text("متوقف مؤقتًا▶️ !")


@Kl_t3.on_message(command("resume") & other_filters)
@a_s_g_ki
@hJskpv
async def resume(_, message: Message):
    chat_id = get_chat_id(message.chat)
    for x in pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await message.reply_text("لم يتم إيقاف أي شيء مؤقتًا❗!")
    else:
        await pytgcalls.resume_stream(chat_id)
        await message.reply_text("مستأنف⏸ !")


@Kl_t3.on_message(command("end") & other_filters)
@a_s_g_ki
@hJskpv
async def stop(_, message: Message):
    chat_id = get_chat_id(message.chat)
    for x in pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await message.reply_text("لا شيء يتدفق!")
    else:
        try:
            queues.clear(message.chat.id)
        except QueueEmpty:
            pass

        await pytgcalls.leave_group_call(chat_id)
        await message.reply_text("توقف البث ❌!")


@Kl_t3.on_message(command("skip") & other_filters)
@a_s_g_ki
@hJskpv
async def skip(_, message: Message):
    global que
    chat_id = get_chat_id(message.chat)
    for x in pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await message.reply_text("لا شيء يلعب للتخطي ❌!")
    else:
        queues.task_done(chat_id)

        if queues.is_empty(chat_id):
            await pytgcalls.leave_group_call(chat_id)
        else:
            await pytgcalls.change_stream(
                chat_id,
                AudioPiped(
                    queues.get(chat_id)["file"],
                ),
            )

    qeue = que.get(chat_id)
    if qeue:
        skip = qeue.pop(0)
    if not qeue:
        return
    await message.reply_text(f"- Skipped **{skip[0]}**\n- Now Playing **{qeue[0][0]}**")


@Kl_t3.on_message(command("mute") & other_filters)
@a_s_g_ki
@hJskpv
async def mute(_, message: Message):
    chat_id = get_chat_id(message.chat)
    result = await pytgcalls.mute_stream(chat_id)
    await message.reply_text("كتم الصوت✅")
    if mute:
        result == 0
    else:
        await message.reply_text("صامت بالفعل❌")
    if not mute:
        result == 1
    else:
        await message.reply_text("ليس في المكالمه ❌")


@Kl_t3.on_message(command("unmute") & other_filters)
@a_s_g_ki
@hJskpv
async def unmute(_, message: Message):
    chat_id = get_chat_id(message.chat)
    result = await pytgcalls.unmute_stream(chat_id)
    await message.reply_text("غير صامت✅")
    if unmute:
        result == 0
    else:
        await message.reply_text("غير صامت ❌")
    if not unmute:
        result == 1
    else:
        await message.reply_text("ليس في المكالمه ❌ ")

@Kl_t3.on_message(filters.command("admincache"))
@a_s_g_ki
async def admincache(client, message: Message):
    set(
        message.chat.id,
        [
            member.user
            for member in await message.chat.get_members(filter="administrators")
        ],
    )
    await message.reply_text("❇️ تم تحديث ذاكرة التخزين المؤقت للمسؤول!")
