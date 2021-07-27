from . import *
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest

async def check_user(id):
    if CHANNEL is None:
        return True
    ok = True
    try:
        await bot(GetParticipantRequest(channel=CHANNEL, participant=id))
        ok = True
    except UserNotParticipantError:
        ok = False
    return ok

if CHANNEL.startswith('@'):
    username = CHANNEL.split('@')[1]
    invite = f"https://t.me/{username}"
else:
    invite = CHANNEL
