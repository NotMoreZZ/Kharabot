import asyncio

import discord


class Discordia(discord.Client):
    async def on_message(self, message):
        if not message.content.startswith('!') or message.author == self.user:
            return

        if not message.guild.id == '257743384792399872':
            await message.channel.send(
                "Sorry, but I'm availible only at Dauntless Russian Community by now.\nhttps://discord.gg/AU2gj7w")
            return

        text = message.content[1:].lower()

        if text.startswith('accept') or text.startswith('принять'):
            for role in message.author.roles:
                if role.name == 'Офицер':
                    break
            else:
                await message.channel.send(
                    '{}, ты даже не ~~гражданин~~ офицер!'.format(
                        message.author.mention))
                return

            if not len(message.mentions) == 1:
                await message.channel.send(
                    'Не понял кого принять, нужно упомянуть одного участника.')
                return

            user = message.mentions[0]

            for role in message.guild.roles:
                if role.name == 'Богатырь':
                    giverole = role
                    break
            else:
                await message.channel.send('Не нашел богатырей :(')
                return

            try:
                await user.add_roles(giverole)
            except discord.Forbidden:
                await message.channel.send(
                    'У меня нет прав выдать роль {} :('.format(role.name))
            else:
                await message.channel.send(
                    '{} теперь {} :)'.format(user.mention, role.name))

        return

    async def go(self, *args, **kwargs):
        async def runner():
            try:
                await self.start(*args, **kwargs)
            finally:
                await self.close()

        await asyncio.ensure_future(runner(), loop=self.loop)
