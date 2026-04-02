"""Party meta test bot.

Tests all updated party member meta setter functions introduced in the
"Party meta changes" commit. Commands are sent as friend messages with the
configured prefix (default: '!').

Usage
-----
1. Copy this file next to your ``device_auths.json`` (or let it create one).
2. Run: ``python party_meta_test_bot.py``
3. Send any of the commands below from a friend's account or your own.

Commands
--------
!outfit <CID>
    Set the bot's outfit (character). Example: ``!outfit CID_028_Athena_Commando_F``

!backpack <BID>
    Set the bot's back bling. Example: ``!backpack BID_001``

!pickaxe <PID>
    Set the bot's pickaxe. Example: ``!pickaxe DefaultPickaxe``

!contrail <ID>
    Set the bot's contrail. Example: ``!contrail DefaultContrail``

!kicks <ID>
    Set the bot's kicks (shoes). Example: ``!kicks KID_001``

!banner <icon> <color>
    Set the bot's banner icon and color (season level removed in new meta).
    Example: ``!banner StandardBanner1 DefaultColor1``

!ready
    Set the bot to ready state.

!notready
    Set the bot to not-ready state.

!sittingout
    Set the bot to sitting-out state.

!emote <EID>
    Play an emote. Example: ``!emote EID_Floss``

!clearemote
    Stop the currently playing emote.

!victorycrownson
    Give the bot one victory crown.

!victorycrownsoff
    Remove victory crowns.

!equip_crown
    Toggle the bot wearing a crown (sets has_crown=1).

!unequip_crown
    Remove the bot's crown (sets has_crown=0).

!battlepass <level>
    Set battlepass purchased=True and the given level.
    Example: ``!battlepass 100``

!instruments <bass> <guitar> <drums> <keytar> <mic>
    Set all five Festival instruments at once.
    Example: ``!instruments Sparks_Bass_Electric Sparks_Guitar_Generic Sparks_Drum_Generic Sparks_Keytar_Generic Sparks_Mic_Generic``

!jam <EID>
    Play a jam / Festival emote. Example: ``!jam EID_Jam_Generic``

!backpackrating <int>
    Set backpack rating. Example: ``!backpackrating 130``

!info
    Print the current values of all party member meta properties to stdout
    and send a short confirmation message.
"""

import rebootpy
import json
import os

from rebootpy.ext import commands
from rebootpy.enums import ReadyState

filename = 'device_auths.json'


def get_device_auth_details():
    if os.path.isfile(filename):
        with open(filename, 'r') as fp:
            return json.load(fp)
    return {}


def store_device_auth_details(details):
    with open(filename, 'w') as fp:
        json.dump(details, fp)


device_auth_details = get_device_auth_details()
bot = commands.Bot(
    command_prefix='!',
    auth=rebootpy.AdvancedAuth(
        prompt_device_code=True,
        open_link_in_browser=True,
        **device_auth_details
    )
)


@bot.event
async def event_device_auth_generate(details):
    store_device_auth_details(details)


@bot.event
async def event_ready():
    print(f'[party_meta_test_bot] Ready as {bot.user.display_name} ({bot.user.id})')


@bot.event
async def event_friend_request(request):
    await request.accept()


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _me():
    """Return the bot's own ClientPartyMember, or None if not in a party."""
    return bot.party.me if bot.party else None


# ---------------------------------------------------------------------------
# Cosmetic setter commands
# ---------------------------------------------------------------------------

@bot.command()
async def outfit(ctx, asset: str):
    """Set the bot's outfit. Usage: !outfit <CID>"""
    me = _me()
    if me is None:
        return await ctx.send('Not in a party.')
    await me.set_outfit(asset)
    await ctx.send(f'Outfit set to: {asset}')


@bot.command()
async def backpack(ctx, asset: str):
    """Set the bot's back bling. Usage: !backpack <BID>"""
    me = _me()
    if me is None:
        return await ctx.send('Not in a party.')
    await me.set_backpack(asset)
    await ctx.send(f'Backpack set to: {asset}')


@bot.command()
async def pickaxe(ctx, asset: str):
    """Set the bot's pickaxe. Usage: !pickaxe <PID>"""
    me = _me()
    if me is None:
        return await ctx.send('Not in a party.')
    await me.set_pickaxe(asset)
    await ctx.send(f'Pickaxe set to: {asset}')


@bot.command()
async def contrail(ctx, asset: str):
    """Set the bot's contrail. Usage: !contrail <ID>"""
    me = _me()
    if me is None:
        return await ctx.send('Not in a party.')
    await me.set_contrail(asset)
    await ctx.send(f'Contrail set to: {asset}')


@bot.command()
async def kicks(ctx, asset: str):
    """Set the bot's kicks (shoes). Usage: !kicks <ID>"""
    me = _me()
    if me is None:
        return await ctx.send('Not in a party.')
    await me.set_kicks(asset)
    await ctx.send(f'Kicks set to: {asset}')


# ---------------------------------------------------------------------------
# Banner (season_level parameter was removed; only icon + color now)
# ---------------------------------------------------------------------------

@bot.command()
async def banner(ctx, icon: str, color: str):
    """Set the bot's banner. Usage: !banner <icon> <color>"""
    me = _me()
    if me is None:
        return await ctx.send('Not in a party.')
    await me.set_banner(icon=icon, color=color)
    await ctx.send(f'Banner set — icon: {icon}, color: {color}')


# ---------------------------------------------------------------------------
# Ready state
# ---------------------------------------------------------------------------

@bot.command()
async def ready(ctx):
    """Set the bot to ready."""
    me = _me()
    if me is None:
        return await ctx.send('Not in a party.')
    await me.set_ready(ReadyState.READY)
    await ctx.send('Ready state set to: Ready')


@bot.command()
async def notready(ctx):
    """Set the bot to not-ready."""
    me = _me()
    if me is None:
        return await ctx.send('Not in a party.')
    await me.set_ready(ReadyState.NOT_READY)
    await ctx.send('Ready state set to: NotReady')


@bot.command()
async def sittingout(ctx):
    """Set the bot to sitting-out."""
    me = _me()
    if me is None:
        return await ctx.send('Not in a party.')
    await me.set_ready(ReadyState.SITTING_OUT)
    await ctx.send('Ready state set to: SittingOut')


# ---------------------------------------------------------------------------
# Emotes
# ---------------------------------------------------------------------------

@bot.command()
async def emote(ctx, asset: str):
    """Play an emote. Usage: !emote <EID>"""
    me = _me()
    if me is None:
        return await ctx.send('Not in a party.')
    await me.set_emote(asset)
    await ctx.send(f'Emote set to: {asset}')


@bot.command()
async def clearemote(ctx):
    """Stop the currently playing emote."""
    me = _me()
    if me is None:
        return await ctx.send('Not in a party.')
    await me.clear_emote()
    await ctx.send('Emote cleared.')


# ---------------------------------------------------------------------------
# Victory crowns / has_crown (LoadoutMeta stats)
# ---------------------------------------------------------------------------

@bot.command()
async def victorycrownson(ctx):
    """Give the bot 1 victory crown."""
    me = _me()
    if me is None:
        return await ctx.send('Not in a party.')
    await me.set_victory_crowns(1)
    await ctx.send('Victory crowns set to 1.')


@bot.command()
async def victorycrownsoff(ctx):
    """Remove victory crowns from the bot."""
    me = _me()
    if me is None:
        return await ctx.send('Not in a party.')
    await me.set_victory_crowns(0)
    await ctx.send('Victory crowns cleared.')


@bot.command()
async def equip_crown(ctx):
    """Make the bot wear a victory crown (has_crown=1)."""
    me = _me()
    if me is None:
        return await ctx.send('Not in a party.')
    await me.equip_crown(True)
    await ctx.send('Crown equipped.')


@bot.command()
async def unequip_crown(ctx):
    """Remove the bot's victory crown (has_crown=0)."""
    me = _me()
    if me is None:
        return await ctx.send('Not in a party.')
    await me.equip_crown(False)
    await ctx.send('Crown unequipped.')


# ---------------------------------------------------------------------------
# Battlepass info
# ---------------------------------------------------------------------------

@bot.command()
async def battlepass(ctx, level: int):
    """Set battlepass purchased + level. Usage: !battlepass <level>"""
    me = _me()
    if me is None:
        return await ctx.send('Not in a party.')
    await me.set_battlepass_info(has_purchased=True, level=level)
    await ctx.send(f'Battlepass info set — purchased: True, level: {level}')


# ---------------------------------------------------------------------------
# Festival / Jam instruments (set_instruments uses MpLoadout1)
# ---------------------------------------------------------------------------

@bot.command()
async def instruments(ctx, bass: str, guitar: str, drums: str,
                      keytar: str, mic: str):
    """Set all five Festival instruments.
    Usage: !instruments <bass> <guitar> <drums> <keytar> <mic>
    """
    me = _me()
    if me is None:
        return await ctx.send('Not in a party.')
    await me.set_instruments(
        bass=bass,
        guitar=guitar,
        drums=drums,
        keytar=keytar,
        microphone=mic
    )
    await ctx.send(
        f'Instruments set — bass: {bass}, guitar: {guitar}, '
        f'drums: {drums}, keytar: {keytar}, mic: {mic}'
    )


@bot.command()
async def jam(ctx, asset: str):
    """Play a jam/Festival emote. Usage: !jam <EID>"""
    me = _me()
    if me is None:
        return await ctx.send('Not in a party.')
    await me.set_jam_emote(asset)
    await ctx.send(f'Jam emote set to: {asset}')


# ---------------------------------------------------------------------------
# Backpack rating (StW)
# ---------------------------------------------------------------------------

@bot.command()
async def backpackrating(ctx, rating: int):
    """Set backpack rating. Usage: !backpackrating <int>"""
    me = _me()
    if me is None:
        return await ctx.send('Not in a party.')
    await me.set_backpack_rating(rating)
    await ctx.send(f'Backpack rating set to: {rating}')


# ---------------------------------------------------------------------------
# Info dump — reads back all updated meta properties
# ---------------------------------------------------------------------------

@bot.command()
async def info(ctx):
    """Print all party member meta property values to stdout."""
    me = _me()
    if me is None:
        return await ctx.send('Not in a party.')

    meta = me.meta
    lines = [
        '--- Party Member Meta ---',
        f'outfit          : {me.outfit}',
        f'backpack        : {me.backpack}',
        f'pickaxe         : {me.pickaxe}',
        f'contrail        : {me.contrail}',
        f'kicks           : {me.kicks}',
        f'outfit_variants : {me.outfit_variants}',
        f'backpack_variants: {me.backpack_variants}',
        f'pickaxe_variants: {me.pickaxe_variants}',
        f'contrail_variants: {me.contrail_variants}',
        f'kicks_variants  : {me.kicks_variants}',
        f'banner          : {me.banner}',
        f'has_crown       : {me.has_crown}',
        f'victory_crowns  : {me.victory_crowns}',
        f'rank            : {me.rank}',
        f'scratchpad      : {me.scratchpad}',
        f'eos_product_user_id: {me.eos_product_user_id}',
        f'battlepass_info : {me.battlepass_info}',
        '-------------------------',
    ]
    for line in lines:
        print(line)

    await ctx.send('Meta info printed to console.')


bot.run()
