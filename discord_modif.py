import discord
import asyncio
import threading
from discord import utils
from datetime import timedelta

class DiscordModifClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        super().__init__(intents=intents)
        self._ready_event = threading.Event()

    async def on_ready(self):
        print(f"[dm] ✅ Connecté en tant que {self.user}")
        self._ready_event.set()

    async def list_guild(self, guild_id):
        guild = discord.utils.get(self.guilds, id=guild_id)
        if not guild:
            print("[dm] ❌ Serveur introuvable.")
            return
        print(f"[dm] 📋 Salons dans {guild.name} :")
        for c in guild.channels:
            print(f" - {c.name} ({c.type})")

client = DiscordModifClient()
_bot_thread = None


def _start_bot(token):
    asyncio.run(client.start(token))

def start(token_path="token.txt"):
    global _bot_thread
    try:
        with open(token_path, "r") as f:
            token = f.read().strip()
    except FileNotFoundError:
        print(f"[dm] ❌ Token introuvable dans {token_path}")
        return

    _bot_thread = threading.Thread(target=_start_bot, args=(token,))
    _bot_thread.start()

    print("[dm] 🕓 Démarrage du bot...")
    client._ready_event.wait()  # Attend que le bot soit prêt
    print("[dm] 🚀 Bot prêt !")



def list(guild_id: int):
    if guild_id is None:
        guild_id = _current_guild_id
    if guild_id is None:
        print("[dm] Aucun serveur spécifié.")
        return
    if not client.is_ready():
        print("[dm] ❌ Le bot n'est pas encore prêt.")
        return

    future = asyncio.run_coroutine_threadsafe(client.list_guild(guild_id), client.loop)
    try:
        future.result()  # Attend que la tâche se termine
    except Exception as e:
        print(f"[dm] ❌ Erreur dans dm.list : {e}")


async def _create_category(guild_id: int, name: str, visibility: str):
    guild = discord.utils.get(client.guilds, id=guild_id)
    if not guild:
        print(f"[dm] ❌ Serveur introuvable : {guild_id}")
        return

    overwrites = {}

    if visibility.lower() == "private":
        overwrites[guild.default_role] = discord.PermissionOverwrite(view_channel=False)
    elif visibility.lower() == "public":
        overwrites[guild.default_role] = discord.PermissionOverwrite(view_channel=True)
    else:
        print(f"[dm] ❌ Visibilité invalide : {visibility} (utilise 'Public' ou 'Private')")
        return

    try:
        await guild.create_category(name=name, overwrites=overwrites)
        print(f"[dm] ✅ Catégorie '{name}' créée avec visibilité '{visibility}'")
    except Exception as e:
        print(f"[dm] ❌ Erreur lors de la création de la catégorie : {e}")

def CreateCategory(guild_id: int , name: str, visibility: str = "Public"):
    if guild_id is None:
        guild_id = _current_guild_id
    if guild_id is None:
        print("[dm] Aucun serveur spécifié.")
        return
    future = asyncio.run_coroutine_threadsafe(
        _create_category(guild_id, name, visibility),
        client.loop
    )
    try:
        future.result()
    except Exception as e:
        print(f"[dm] ❌ Erreur CreateCategory: {e}")

async def _create_text_channel(guild_id: int, name: str, category_name: str = None, visibility: str = "Public"):
    guild = discord.utils.get(client.guilds, id=guild_id)
    if not guild:
        print(f"[dm] Serveur introuvable : {guild_id}")
        return

    overwrites = {}
    if visibility.lower() == "private":
        overwrites[guild.default_role] = discord.PermissionOverwrite(view_channel=False)
    else:
        overwrites[guild.default_role] = discord.PermissionOverwrite(view_channel=True)

    category = None
    if category_name:
        category = discord.utils.get(guild.categories, name=category_name)
        if not category:
            print(f"[dm] Catégorie '{category_name}' introuvable, création d'une catégorie par défaut")
            category = await guild.create_category(category_name, overwrites=overwrites)

    await guild.create_text_channel(name, overwrites=overwrites, category=category)
    print(f"[dm] Salon texte '{name}' créé dans la catégorie '{category_name}' avec visibilité '{visibility}'")

def CreateTextChannel(guild_id: int, name: str, category_name: str = None, visibility: str = "Public"):
    if guild_id is None:
        guild_id = _current_guild_id
    if guild_id is None:
        print("[dm] Aucun serveur spécifié.")
        return
    if not client.is_ready():
        print("[dm] Le bot n'est pas prêt.")
        return
    future = asyncio.run_coroutine_threadsafe(
        _create_text_channel(guild_id, name, category_name, visibility),
        client.loop
    )
    try:
        future.result()
    except Exception as e:
        print(f"[dm] Erreur CreateTextChannel: {e}")


async def _create_vocal_channel(guild_id: int, name: str, category_name: str = None, visibility: str = "Public"):
    guild = discord.utils.get(client.guilds, id=guild_id)
    if not guild:
        print(f"[dm] Serveur introuvable : {guild_id}")
        return

    overwrites = {}
    if visibility.lower() == "private":
        overwrites[guild.default_role] = discord.PermissionOverwrite(view_channel=False)
    else:
        overwrites[guild.default_role] = discord.PermissionOverwrite(view_channel=True)

    category = None
    if category_name:
        category = discord.utils.get(guild.categories, name=category_name)
        if not category:
            print(f"[dm] Catégorie '{category_name}' introuvable, création d'une catégorie par défaut")
            category = await guild.create_category(category_name, overwrites=overwrites)

    await guild.create_voice_channel(name, overwrites=overwrites, category=category)
    print(f"[dm] Salon vocal '{name}' créé dans la catégorie '{category_name}' avec visibilité '{visibility}'")

def CreateVocalChannel(guild_id: int, name: str, category_name: str = None, visibility: str = "Public"):
    if guild_id is None:
        guild_id = _current_guild_id
    if guild_id is None:
        print("[dm] Aucun serveur spécifié.")
        return
    if not client.is_ready():
        print("[dm] Le bot n'est pas prêt.")
        return
    future = asyncio.run_coroutine_threadsafe(
        _create_vocal_channel(guild_id, name, category_name, visibility),
        client.loop
    )
    try:
        future.result()
    except Exception as e:
        print(f"[dm] Erreur CreateVocalChannel: {e}")

async def _rename_channel(guild_id: int, old_name: str, new_name: str):
    guild = discord.utils.get(client.guilds, id=guild_id)
    if not guild:
        print(f"[dm] Serveur introuvable : {guild_id}")
        return

    channel = discord.utils.get(guild.channels, name=old_name)
    if not channel:
        print(f"[dm] Salon '{old_name}' introuvable dans le serveur {guild.name}")
        return

    # Détection du type de channel
    if isinstance(channel, discord.TextChannel):
        channel_type = "salon textuel"
    elif isinstance(channel, discord.VoiceChannel):
        channel_type = "salon vocal"
    elif isinstance(channel, discord.CategoryChannel):
        channel_type = "catégorie"
    else:
        channel_type = "type inconnu"

    try:
        await channel.edit(name=new_name)
        print(f"[dm] {channel_type} '{old_name}' renommé en '{new_name}'")
    except Exception as e:
        print(f"[dm] Erreur lors du renommage : {e}")


def RenameChannel(guild_id: int, old_name: str, new_name: str):
    if guild_id is None:
        guild_id = _current_guild_id
    if guild_id is None:
        print("[dm] Aucun serveur spécifié.")
        return
    if not client.is_ready():
        print("[dm] Le bot n'est pas prêt.")
        return
    future = asyncio.run_coroutine_threadsafe(
        _rename_channel(guild_id, old_name, new_name),
        client.loop
    )
    try:
        future.result()
    except Exception as e:
        print(f"[dm] Erreur RenameChannel: {e}")

# delete un ou plusieurs salons/catégories
async def _delete(guild_id: int, names):
    guild = client.get_guild(guild_id)
    if not guild:
        print(f"[dm] ❌ Serveur introuvable avec l'ID {guild_id}")
        return

    if isinstance(names, str):
        names = [names]  # convertir en liste si un seul nom

    found = False
    for channel in guild.channels:
        if channel.name in names:
            await channel.delete()
            print(f"[dm] 🗑️ Supprimé : {channel.name} ({type(channel).__name__})")
            found = True

    if not found:
        print(f"[dm] ❌ Aucun des éléments spécifiés n'a été trouvé : {names}")

def delete(guild_id: int, names):
    asyncio.run_coroutine_threadsafe(_delete(guild_id, names), client.loop)

async def _delete_all(guild_id: int):
    guild = client.get_guild(guild_id)
    if not guild:
        print(f"[dm] ❌ Serveur introuvable avec l'ID {guild_id}")
        return

    for channel in guild.channels:
        await channel.delete()
        print(f"[dm] 🗑️ Supprimé : {channel.name} ({type(channel).__name__})")

def delete_all(guild_id: int):
    asyncio.run_coroutine_threadsafe(_delete_all(guild_id), client.loop)

def RenameServer(guild_id, new_name):
    async def _rename():
        guild = client.get_guild(guild_id)
        if not guild:
            print(f"[RenameServer] ❌ Serveur introuvable avec ID : {guild_id}")
            return

        try:
            await guild.edit(name=new_name)
            print(f"[RenameServer] ✅ Serveur renommé en : {new_name}")
        except Exception as e:
            print(f"[RenameServer] ❌ Erreur lors du renommage : {e}")

    asyncio.run_coroutine_threadsafe(_rename(), client.loop)


import os
import json
from datetime import datetime

async def _check(guild_id, log=True):
    guild = client.get_guild(guild_id)
    if guild is None:
        print("[dm] ❌ Serveur introuvable.")
        return

    suspects = []
    for member in guild.members:
        if member.bot:
            continue
        conditions = [
            member.default_avatar == member.avatar,
            (member.joined_at and (discord.utils.utcnow() - member.joined_at).days < 3),
            member.public_flags.value == 0,
            not member.activity
        ]
        if sum(conditions) >= 3:
            suspects.append({
                "username": f"{member.name}#{member.discriminator}",
                "id": member.id,
                "joined_at": str(member.joined_at),
                "avatar_url": str(member.avatar.url if member.avatar else "Aucun"),
                "reason": "Compte suspect (inactif / récent / sans photo de profil / sans bio)"
            })
            try:
                await member.send("⚠️ Votre compte semble suspect (inactif, récent ou sans profil). Vous êtes désormais surveillé par l'équipe de modération.")
            except Exception:
                print(f"[dm] ❌ DM échoué à {member.name}#{member.discriminator}")

    print(f"[dm] 🚨 Comptes suspects détectés: {len(suspects)}")

    if log:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = f"suspects_{guild.id}_{timestamp}.json"
        os.makedirs("logs", exist_ok=True)
        with open(os.path.join("logs", log_file), "w", encoding="utf-8") as f:
            json.dump(suspects, f, indent=4, ensure_ascii=False)
        print(f"[dm] 📝 Suspects enregistrés dans logs/{log_file}")

def check(guild_id, log=True):
    asyncio.run_coroutine_threadsafe(_check(guild_id, log), client.loop)


async def _warn(guild_id, member_id, reason="Vous avez été averti pour comportement inapproprié."):
    guild = client.get_guild(guild_id)
    member = guild.get_member(member_id)
    if member:
        try:
            await member.send(f"⚠️ Avertissement sur **{guild.name}** : {reason}")
            print(f"[dm] ⚠️ Avertissement envoyé à {member}")
        except:
            print(f"[dm] ❌ Impossible d'envoyer un avertissement à {member}")
    else:
        print("[dm] ❌ Membre introuvable")

def warn(guild_id, member_id, reason="Comportement inapproprié."):
    asyncio.run_coroutine_threadsafe(_warn(guild_id, member_id, reason), client.loop)

async def _ban(guild_id, member_id, reason="Violation du règlement."):
    guild = client.get_guild(guild_id)
    member = guild.get_member(member_id)
    if member:
        try:
            await guild.ban(member, reason=reason, delete_message_days=1)
            print(f"[dm] 🔨 {member} banni.")
        except:
            print(f"[dm] ❌ Échec du bannissement de {member}")
    else:
        print("[dm] ❌ Membre introuvable")

def ban(guild_id, member_id, reason="Violation du règlement."):
    asyncio.run_coroutine_threadsafe(_ban(guild_id, member_id, reason), client.loop)

async def _kick(guild_id, member_id, reason="Comportement inacceptable."):
    guild = client.get_guild(guild_id)
    member = guild.get_member(member_id)
    if member:
        try:
            await guild.kick(member, reason=reason)
            print(f"[dm] 👢 {member} expulsé.")
        except:
            print(f"[dm] ❌ Échec de l'expulsion de {member}")
    else:
        print("[dm] ❌ Membre introuvable")

def kick(guild_id, member_id, reason="Comportement inacceptable."):
    asyncio.run_coroutine_threadsafe(_kick(guild_id, member_id, reason), client.loop)

async def _mute(guild_id, member_id, reason="Silence temporaire", duration=None):
    guild = client.get_guild(guild_id)
    member = guild.get_member(member_id)

    if not member:
        print("[dm] ❌ Membre introuvable")
        return

    muted_role = utils.get(guild.roles, name="Muted")
    if not muted_role:
        muted_role = await guild.create_role(name="Muted", reason="Création auto pour mute")
        for channel in guild.channels:
            try:
                await channel.set_permissions(muted_role, speak=False, send_messages=False, add_reactions=False)
            except:
                pass

    try:
        await member.add_roles(muted_role, reason=reason)
        await member.send(f"🔇 Vous avez été réduit au silence sur **{guild.name}**. Raison : {reason}")
        print(f"[dm] 🔇 {member} a été mute.")
    except:
        print(f"[dm] ❌ Impossible de mute {member}")

    if duration:
        await asyncio.sleep(duration)
        try:
            await member.remove_roles(muted_role)
            print(f"[dm] 🔈 {member} a été automatiquement unmute après {duration} secondes.")
        except:
            pass

def mute(guild_id, member_id, reason="Silence temporaire", duration=None):
    asyncio.run_coroutine_threadsafe(_mute(guild_id, member_id, reason, duration), client.loop)


async def _prepare_community(guild_id):
    guild = client.get_guild(guild_id)

    try:
        rules = await guild.create_text_channel("📜-règles")
        welcome = await guild.create_text_channel("👋-bienvenue")
        news = await guild.create_text_channel("📢-annonces")

        await guild.edit(
            verification_level=discord.VerificationLevel.high,
            default_notifications=discord.NotificationLevel.only_mentions
        )

        print(f"[dm] ✅ Canaux créés et paramètres ajustés.")
        for member in guild.members:
            try:
                await member.send(
                    f"📢 Le serveur **{guild.name}** se prépare à devenir une communauté officielle ! 🎉"
                )
            except:
                pass

        print(f"[dm] ✅ Préparation communautaire effectuée.")
    except Exception as e:
        print(f"[dm] ❌ Erreur lors de la configuration communautaire : {e}")

def PrepareCommunity(guild_id):
    asyncio.run_coroutine_threadsafe(_prepare_community(guild_id), client.loop)

