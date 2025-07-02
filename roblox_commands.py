import aiohttp
import discord
from discord.ext import commands

async def get_roblox_user(username):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.roblox.com/users/get-by-username?username={username}") as resp:
            data = await resp.json()
            if "Id" not in data or data["Id"] == 0:
                return None
            user_id = data["Id"]

        async with session.get(f"https://users.roblox.com/v1/users/{user_id}") as resp:
            profile = await resp.json()

        async with session.get(
            f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user_id}&size=420x420&format=Png&isCircular=false"
        ) as resp:
            avatar_data = await resp.json()
            avatar_url = avatar_data["data"][0]["imageUrl"]

        return {
            "username": profile.get("name"),
            "display_name": profile.get("displayName"),
            "description": profile.get("description", ""),
            "id": user_id,
            "avatar": avatar_url
        }

def roblox_command_setup(bot: commands.Bot):
    @bot.command(name="roblox")
    async def roblox(ctx, username):
        await ctx.send(f"🔍 Searching for `{username}` on Roblox...")
        user = await get_roblox_user(username)
        if not user:
            await ctx.send("❌ Roblox user not found.")
            return

        embed = discord.Embed(
            title=f"{user['display_name']} (@{user['username']})",
            description=user['description'] or "*No bio provided*",
            color=0x00b0f4
        )
        embed.set_thumbnail(url=user['avatar'])
        embed.set_footer(text=f"User ID: {user['id']}")
        await ctx.send(embed=embed)
        
