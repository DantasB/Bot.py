"""
The MIT License (MIT)
Copyright (c) 2015-2019 Rapptz
Copyright (c) 2019 DantasB
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import random
import time
import discord
import datetime
import aiohttp
import json
import asyncio

from discord.ext import commands
from forex_python.converter import CurrencyRates
from dhooks import Webhook
from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions
from horario import*

banhammer = [] #banhammer giphy gifs
omg = [] #omg giphy gifs
kick = [] #kick giphy gifs

betina_icon = " " #bot icon

with open('reports.json', encoding='utf-8') as f:
    try:
        report = json.load(f)
    except ValueError:
        report = {}
        report['users'] = []

with open('mutados.json', 'r') as file:
    try:
        cargos_dos_mutados = json.load(file)
    except ValueError:
        cargos_dos_mutados = {}

with open('digitlogs.json', 'r') as file:
    try:
        digit_log = json.load(file)
    except ValueError:
        digit_log = {}

with open('limitador.json', 'r') as file:
    try:
        limitador_log = json.load(file)
    except ValueError:
        limitador_log = {}


class Administração(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.command()
    async def ping(self, ctx):
        """Retorna o Ping do usuario mais uma piadinha tosca!"""
        if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
            avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
        else:
            avi = ctx.message.author.avatar_url_as(static_format='png')
        channel = ctx.channel
        t1 = time.perf_counter()
        async with ctx.message.channel.typing():
            t2 = time.perf_counter()
            await ctx.send('<a:ping:512065320320761867> Pong! Isso me levou {}ms.'.format(round((t2 - t1) * 1000)))
        guild_id = str(ctx.guild.id)

        if guild_id not in digit_log:
            return
        texto = await ctx.get_message(ctx.message.id)
        guild = ctx.guild.get_channel(int(digit_log[guild_id]))
        embed = discord.Embed(title=f"*{ctx.message.author.name} usou o comando Ping* no canal #{texto.channel}",
                              colour=discord.Colour(0x370c5e))

        embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")
        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                   year()))
        await guild.send(embed=embed)

    @commands.guild_only()
    @commands.command(pass_context=True)
    async def pong(self, ctx):
        if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
            avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
        else:
            avi = ctx.message.author.avatar_url_as(static_format='png')

        channel = ctx.channel
        t1 = time.perf_counter()
        async with ctx.message.channel.typing():
            t2 = time.perf_counter()
            await ctx.send('<a:ping:512065320320761867> !ginP ossI em uoveL {} sm'.format(round((t2 - t1) * 1000)))

        guild_id = str(ctx.guild.id)

        if guild_id not in digit_log:
            return
        texto = await ctx.get_message(ctx.message.id)
        guild = ctx.guild.get_channel(int(digit_log[guild_id]))
        embed = discord.Embed(title=f"*{ctx.message.author.name} usou o comando Pong* no canal #{texto.channel}",
                              colour=discord.Colour(0x370c5e))

        embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")
        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                   year()))
        await guild.send(embed=embed)

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='apaga', aliases=['delete', 'clean'])
    @has_permissions(manage_messages=True, read_message_history=True)
    async def apaga(self, ctx, amount: int):
        texto = await ctx.get_message(ctx.message.id)
        if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
            avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
        else:
            avi = ctx.message.author.avatar_url_as(static_format='png')
        await ctx.channel.purge(limit=amount + 1)
        embed = discord.Embed(title=f"{amount + 1} mensagens foram apagadas, {ctx.message.author.name}",
                              colour=discord.Colour(0x370c5e))

        embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")
        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                   year()))

        await ctx.send(embed=embed, delete_after=10)

    @apaga.error
    async def apaga_handler(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title="Comando $apaga:", colour=discord.Colour(0x370c5e),
                                  description="Apaga n+1 linhas acima da ultima mensagem\n \n**Como usar: $apaga <linhas>**")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                       year()))
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Gerenciar Mensagens, Ler o histórico de "
                                                            "mensagens`` *para utilizar este comando!*", inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$apaga 100\n$apaga 10", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$delete, $clean.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")
        elif isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'amount':
                embed = discord.Embed(title="Comando $apaga:", colour=discord.Colour(0x370c5e),
                                      description="Apaga n+1 linhas acima da ultima mensagem\n \n**Como usar: $apaga <linhas>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                                "ter a permissão de* ``"
                                                                "Gerenciar Mensagens, Ler o histórico de "
                                                                "mensagens`` *para utilizar este comando!*",
                                inline=False)
                embed.add_field(name="📖**Exemplos:**", value="$apaga 100\n$apaga 10", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$delete, $clean.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='ban', aliases=['banir', 'bane'])
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, arg=None):
        texto = await ctx.get_message(ctx.message.id)
        guild_id = str(ctx.guild.id)
        if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
            avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
        else:
            avi = ctx.message.author.avatar_url_as(static_format='png')

        if member.top_role >= member.guild.me.top_role:
            embed = discord.Embed(title="Comando $ban:", colour=discord.Colour(0x370c5e),
                                  description="Bane o usuário do servidor por um motivo"
                                              "\n \n**Como usar: $bane <usuário> <motivo> (opcional)**")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                       year()))
            embed.add_field(name="👮**Permissões:**", value="*Você e o bot precisam "
                                                            "ter a permissão de* ``"
                                                            "Banir membros e estar no topo dos cargos`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$ban @fulano\n$ban @fulano xingou o moderador",
                            inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$bane, $banir.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")
            return
        else:
            if arg == None:
                reason = 'Sem motivos específicados!'
            else:
                reason = arg

            gif1 = random.choice(banhammer)
            gif2 = random.choice(omg)
            msg1 = '**Você estava tentando se banir ?**'
            msg2 = '{} foi banido do servidor {} pelo seguinte motivo: {}'.format(member, ctx.guild.name, reason)
            msg3 = 'Você foi banido do servidor {} pelo seguinte motivo: {}'.format(ctx.guild.name, reason)
            if member == ctx.message.author:

                embed = discord.Embed(title="**Pensativa...**", colour=discord.Colour(0x370c5e),
                                      description="{}".format(msg1))
                embed.set_image(url="{}".format(gif2))
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                await ctx.channel.send(embed=embed)
                if guild_id not in digit_log:
                    return

                guild = ctx.guild.get_channel(int(digit_log[guild_id]))

                embed = discord.Embed(
                    title=f"{ctx.message.author.name} Tentou se banir no canal: #{texto.channel}",
                    colour=discord.Colour(0x370c5e))

                embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")

                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                await guild.send(embed=embed)
                return
            else:
                embed = discord.Embed(title="**BAN!**", colour=discord.Colour(0x370c5e), description="{}".format(msg2))
                embed.set_image(url="{}".format(gif1))
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                mbd = discord.Embed(title="**BAN!**", colour=discord.Colour(0x370c5e), description="{}".format(msg3))
                mbd.set_image(url="{}".format(gif1))
                mbd.set_footer(icon_url=betina_icon,
                    text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name, year()))

                if not member.bot:
                    await member.send(embed=mbd)
                    await ctx.channel.send(embed=embed)
                    if guild_id not in digit_log:
                        return

                    guild = ctx.guild.get_channel(int(digit_log[guild_id]))

                    embed = discord.Embed(
                        title=f"{ctx.message.author.name} Baniu o usuário {member.name} no canal: #{texto.channel}",
                        colour=discord.Colour(0x370c5e), description=f"pelo seguinte motivo: {reason}")

                    embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")

                    embed.set_footer(icon_url=betina_icon,
                                     text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                               self.client.user.name,
                                                                                               year()))
                    await guild.send(embed=embed)
                    await ctx.guild.ban(member)

                else:
                    await ctx.channel.send(embed=embed)
                    if guild_id not in digit_log:
                        return

                    guild = ctx.guild.get_channel(int(digit_log[guild_id]))

                    embed = discord.Embed(
                        title=f"{ctx.message.author.name} Baniu o bot {member.name} no canal: #{texto.channel}",
                        colour=discord.Colour(0x370c5e), description=f"pelo seguinte motivo: {reason}")

                    embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")

                    embed.set_footer(icon_url=betina_icon,
                                     text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                               self.client.user.name,
                                                                                               year()))
                    await guild.send(embed=embed)
                    await ctx.guild.ban(member)

    @ban.error
    async def ban_handler(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title="Comando $ban:", colour=discord.Colour(0x370c5e),
                                  description="Bane o usuário do servidor por um motivo"
                                              "\n \n**Como usar: $bane <usuário> <motivo> (opcional)**")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                       year()))
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos"
                                                            "ter a permissão de* ``"
                                                            "Banir membros e estar no topo dos cargos`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$ban @fulano gado demais\n$ban @fulano xingou "
                                                          "o moderador", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$bane, $banir.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")
        elif isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $ban:", colour=discord.Colour(0x370c5e),
                                      description="Bane o usuário do servidor por um motivo"
                                                  "\n \n**Como usar: $bane <usuário> <motivo> (opcional)**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                                "ter a permissão de* ``"
                                                                "Banir membros e estar no topo dos cargos`` *para utilizar este comando!*",
                                inline=False)
                embed.add_field(name="📖**Exemplos:**", value="$ban @fulano\n$ban @fulano xingou o moderador",
                                inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$bane, $banir.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


    @commands.guild_only()
    @commands.command()
    async def ajuda(self, ctx):
        await ctx.invoke(self.client.get_command("help"))

        @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='membro', aliases=['userinfo', 'ui'])
    async def membro(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
            texto = await ctx.get_message(ctx.message.id)
            guild_id = str(ctx.guild.id)
            user_id = str(ctx.author.id)
            if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
                avi1 = ctx.message.author.avatar_url.rsplit("?", 1)[0]
            else:
                avi1 = ctx.message.author.avatar_url_as(static_format='png')
            roles = ', '.join([x.name for x in member.roles if x.name != "@everyone"])
            if member.avatar_url_as(static_format='png')[54:].startswith('a_'):
                avi = member.avatar_url.rsplit("?", 1)[0]
            else:
                avi = member.avatar_url_as(static_format='png')

            if guild_id in limitador_log:
                if str(ctx.message.channel.id) == limitador_log[guild_id]:
                    embed = discord.Embed(title='📟 Informações do Usuário {}'.format(member.name), color=member.color)
                    embed.set_footer(text="Usado às {} Horário de Brasília | {} {} .".format(hora(), ctx.message.author.name , year()),
                                     icon_url=avi1)

                    if member.nick == None:
                        embed.add_field(name='📛 Apelido:', value='Não tem nenhum nick!', inline=True)
                    else:
                        embed.add_field(name='📛 Apelido:', value='{}'.format(member.nick), inline=True)
                    embed.add_field(name='💻 Id:', value='{}'.format(member.id), inline=True)
                    embed.add_field(name='📆 Conta criada em',
                                    value=member.created_at.__format__('%d de %b de %Y às %H:%M:%S'))
                    embed.add_field(name='⭐ Entrou no servidor em:',
                                    value='{}'.format(member.joined_at.__format__('%d de %b de %Y às %H:%M:%S')),
                                    inline=True)
                    embed.add_field(name='📃 Status:', value='{}'.format(member.status), inline=True)
                    embed.add_field(name='🎌 Cargos:', value='{}'.format(roles), inline=True)
                    embed.set_thumbnail(url=avi)
                    if member.id == ctx.message.guild.owner.id:
                        if str(member.status) == 'online':
                            embed.set_author(name='👑 ✅ {}'.format(member))
                        elif str(member.status) == 'dnd':
                            embed.set_author(name='👑 🔴 {}'.format(member))
                        elif str(member.status) == 'idle':
                            embed.set_author(name='👑 🐤 {}'.format(member))
                        elif str(member.status) == 'offline':
                            embed.set_author(name='👑 ⚪ {}'.format(member))
                    else:
                        if str(member.status) == 'online':
                            embed.set_author(name='✅ {}'.format(member))
                        elif str(member.status) == 'dnd':
                            embed.set_author(name='🔴 {}'.format(member))
                        elif str(member.status) == 'idle':
                            embed.set_author(name='🐤 {}'.format(member))
                        elif str(member.status) == 'offline':
                            embed.set_author(name='⚪ {}'.format(member))
                    await ctx.send(embed=embed)
                else:
                    guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                    await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                    return
            else:
                embed = discord.Embed(title='📟 Informações do Usuário {}'.format(member.name), color=member.color)
                embed.set_footer(
                    text="Usado às {} Horário de Brasília | {} {} .".format(hora(), ctx.message.author.name, year()),
                    icon_url=avi1)
                if member.nick == None:
                    embed.add_field(name='📛 Apelido:', value='Não tem nenhum nick!', inline=True)
                else:
                    embed.add_field(name='📛 Apelido:', value='{}'.format(member.nick), inline=True)
                embed.add_field(name='💻 Id:', value='{}'.format(member.id), inline=True)
                embed.add_field(name='📆 Conta criada em', value=member.created_at.__format__('%d de %b de %Y às %H:%M:%S'))
                embed.add_field(name='⭐ Entrou no servidor em:',
                                value='{}'.format(member.joined_at.__format__('%d de %b de %Y às %H:%M:%S')), inline=True)
                embed.add_field(name='📃 Status:', value='{}'.format(member.status), inline=True)
                embed.add_field(name='🎌 Cargos:', value='{}'.format(roles), inline=True)
                embed.set_thumbnail(url=avi)
                if member.id == ctx.message.guild.owner.id:
                    if str(member.status) == 'online':
                        embed.set_author(name='👑 ✅ {}'.format(member))
                    elif str(member.status) == 'dnd':
                        embed.set_author(name='👑 🔴 {}'.format(member))
                    elif str(member.status) == 'idle':
                        embed.set_author(name='👑 🐤 {}'.format(member))
                    elif str(member.status) == 'offline':
                        embed.set_author(name='👑 ⚪ {}'.format(member))
                else:
                    if str(member.status) == 'online':
                        embed.set_author(name='✅ {}'.format(member))
                    elif str(member.status) == 'dnd':
                        embed.set_author(name='🔴 {}'.format(member))
                    elif str(member.status) == 'idle':
                        embed.set_author(name='🐤 {}'.format(member))
                    elif str(member.status) == 'offline':
                        embed.set_author(name='⚪ {}'.format(member))
                await ctx.send(embed=embed)
        else:
            texto = await ctx.get_message(ctx.message.id)
            guild_id = str(ctx.guild.id)
            user_id = str(ctx.author.id)
            if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
                avi1 = ctx.message.author.avatar_url.rsplit("?", 1)[0]
            else:
                avi1 = ctx.message.author.avatar_url_as(static_format='png')
            roles = ', '.join([x.name for x in member.roles if x.name != "@everyone"])
            if member.avatar_url_as(static_format='png')[54:].startswith('a_'):
                avi = member.avatar_url.rsplit("?", 1)[0]
            else:
                avi = member.avatar_url_as(static_format='png')

            if guild_id in limitador_log:
                if str(ctx.message.channel.id) == limitador_log[guild_id]:
                    embed = discord.Embed(title='📟 Informações do Usuário {}'.format(member.name), color=member.color)
                    embed.set_footer(
                        text="Usado às {} Horário de Brasília | {} {} .".format(hora(), ctx.message.author.name,
                                                                                year()),
                        icon_url=avi1)

                    if member.nick == None:
                        embed.add_field(name='📛 Apelido:', value='Não tem nenhum nick!', inline=True)
                    else:
                        embed.add_field(name='📛 Apelido:', value='{}'.format(member.nick), inline=True)
                    embed.add_field(name='💻 Id:', value='{}'.format(member.id), inline=True)
                    embed.add_field(name='📆 Conta criada em',
                                    value=member.created_at.__format__('%d de %b de %Y às %H:%M:%S'))
                    embed.add_field(name='⭐ Entrou no servidor em:',
                                    value='{}'.format(member.joined_at.__format__('%d de %b de %Y às %H:%M:%S')),
                                    inline=True)
                    embed.add_field(name='📃 Status:', value='{}'.format(member.status), inline=True)
                    embed.add_field(name='🎌 Cargos:', value='{}'.format(roles), inline=True)
                    embed.set_thumbnail(url=avi)
                    if member.id == ctx.message.guild.owner.id:
                        if str(member.status) == 'online':
                            embed.set_author(name='👑 ✅ {}'.format(member))
                        elif str(member.status) == 'dnd':
                            embed.set_author(name='👑 🔴 {}'.format(member))
                        elif str(member.status) == 'idle':
                            embed.set_author(name='👑 🐤 {}'.format(member))
                        elif str(member.status) == 'offline':
                            embed.set_author(name='👑 ⚪ {}'.format(member))
                    else:
                        if str(member.status) == 'online':
                            embed.set_author(name='✅ {}'.format(member))
                        elif str(member.status) == 'dnd':
                            embed.set_author(name='🔴 {}'.format(member))
                        elif str(member.status) == 'idle':
                            embed.set_author(name='🐤 {}'.format(member))
                        elif str(member.status) == 'offline':
                            embed.set_author(name='⚪ {}'.format(member))
                    await ctx.send(embed=embed)
                else:
                    guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                    await ctx.send(
                        f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                    return
            else:
                embed = discord.Embed(title='📟 Informações do Usuário {}'.format(member.name), color=member.color)
                embed.set_footer(
                    text="Usado às {} Horário de Brasília | {} {} .".format(hora(), ctx.message.author.name, year()),
                    icon_url=avi1)
                if member.nick == None:
                    embed.add_field(name='📛 Apelido:', value='Não tem nenhum nick!', inline=True)
                else:
                    embed.add_field(name='📛 Apelido:', value='{}'.format(member.nick), inline=True)
                embed.add_field(name='💻 Id:', value='{}'.format(member.id), inline=True)
                embed.add_field(name='📆 Conta criada em',
                                value=member.created_at.__format__('%d de %b de %Y às %H:%M:%S'))
                embed.add_field(name='⭐ Entrou no servidor em:',
                                value='{}'.format(member.joined_at.__format__('%d de %b de %Y às %H:%M:%S')),
                                inline=True)
                embed.add_field(name='📃 Status:', value='{}'.format(member.status), inline=True)
                embed.add_field(name='🎌 Cargos:', value='{}'.format(roles), inline=True)
                embed.set_thumbnail(url=avi)
                if member.id == ctx.message.guild.owner.id:
                    if str(member.status) == 'online':
                        embed.set_author(name='👑 ✅ {}'.format(member))
                    elif str(member.status) == 'dnd':
                        embed.set_author(name='👑 🔴 {}'.format(member))
                    elif str(member.status) == 'idle':
                        embed.set_author(name='👑 🐤 {}'.format(member))
                    elif str(member.status) == 'offline':
                        embed.set_author(name='👑 ⚪ {}'.format(member))
                else:
                    if str(member.status) == 'online':
                        embed.set_author(name='✅ {}'.format(member))
                    elif str(member.status) == 'dnd':
                        embed.set_author(name='🔴 {}'.format(member))
                    elif str(member.status) == 'idle':
                        embed.set_author(name='🐤 {}'.format(member))
                    elif str(member.status) == 'offline':
                        embed.set_author(name='⚪ {}'.format(member))
                await ctx.send(embed=embed)

        if guild_id not in digit_log:
            return

        guild = ctx.guild.get_channel(int(digit_log[guild_id]))

        embed1 = discord.Embed(
            title=f"{ctx.message.author.name} usou o comando userinfo em {member.name} no canal #{texto.channel}",
            colour=discord.Colour(0x370c5e))

        embed1.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")

        embed1.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                   year()))
        await guild.send(embed=embed1)


    @commands.guild_only()
    @commands.command(pass_context=True, name='servidor', aliases=['serverinfo', 'si'])
    async def servidor(self, ctx):
        texto = await ctx.get_message(ctx.message.id)
        guild_id = str(ctx.guild.id)
        if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
            avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
        else:
            avi = ctx.message.author.avatar_url_as(static_format='png')
        embed = discord.Embed(name='Informações do {}'.format(ctx.message.guild.name),
                              description='Aqui está tudo o que pude encontrar sobre esse servidor!', color=0x370c5e)
        embed.set_footer(text="Usado às {} Horário de Brasília | {} {}".format(hora(), ctx.message.author.name, year()),
                         icon_url=avi)
        embed.set_author(name='📟 Informações do servidor {}:'.format(ctx.message.guild.name))
        embed.add_field(name='📛 Nome do Servidor:', value=ctx.message.guild.name, inline=True)
        embed.add_field(name='👑 Dono do Servidor:', value=ctx.message.guild.owner, inline=True)
        embed.add_field(name='🗺️ Região do Servidor:', value=ctx.message.guild.region, inline=True)
        embed.add_field(name='💻 Id do Servidor:', value=ctx.message.guild.id)
        embed.add_field(name='💬 Número de Canais:', value=len(ctx.message.guild.channels), inline=True)
        embed.add_field(name='👥 Número de Membros:', value=len(ctx.message.guild.members), inline=True)
        embed.add_field(name='📆 Criado em:',
                        value=ctx.message.guild.created_at.strftime("%d de %b de %Y"), inline=True)
        embed.add_field(name='🎌 Número de Cargos:', value=len(ctx.message.guild.roles), inline=True)
        embed.add_field(name='🎌 Nome dos Cargos:',
                        value=', '.join([role.name for role in ctx.message.guild.roles if role.name != '@everyone']),
                        inline=False)
        embed.set_thumbnail(url=ctx.message.guild.icon_url)
        await ctx.send(embed=embed)
        if guild_id not in digit_log:
            return

        guild = ctx.guild.get_channel(int(digit_log[guild_id]))

        embed1 = discord.Embed(
            title=f"{ctx.message.author.name} usou o comando serverinfo no canal #{texto.channel}",
            colour=discord.Colour(0x370c5e))

        embed1.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")

        embed1.set_footer(icon_url=betina_icon,
                          text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                    year()))
        await guild.send(embed=embed1)


    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(pass_context=True, name='warn', aliases=['aviso', 'wrn'])
    @has_permissions(kick_members=True)
    async def warn(self, ctx, user: discord.User, *, arg: str = None):
        texto = await ctx.get_message(ctx.message.id)
        guild_id = str(ctx.guild.id)
        if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
            avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
        else:
            avi = ctx.message.author.avatar_url_as(static_format='png')

        if arg == None:
            reason = 'Sem motivos específicados'
        else:
            reason = arg

        for current_user in report['users']:
            if current_user['name'] == user.name:
                current_user['reasons'].append(reason)
                if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
                    avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
                else:
                    avi = ctx.message.author.avatar_url_as(static_format='png')

                embed = discord.Embed(title=f"*O {user.name} foi warnado pelo {ctx.message.author.name}*",
                                      colour=discord.Colour(0x370c5e), description=f"Pelo seguinte motivo: {reason}")

                embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")
                embed.set_footer(icon_url=betina_icon,
                                  text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                            self.client.user.name,
                                                                                            year()))

                await ctx.send(embed=embed, delete_after=10)
                if guild_id not in digit_log:
                    return

                guild = ctx.guild.get_channel(int(digit_log[guild_id]))

                embed = discord.Embed(
                    title=f"{ctx.message.author.name} usou o comando warn em {user.name} no canal #{texto.channel}",
                    colour=discord.Colour(0x370c5e), description=f"Pelo seguinte motivo: {reason}")

                embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")

                embed.set_footer(icon_url=betina_icon,
                                  text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                            self.client.user.name,
                                                                                            year()))
                await guild.send(embed=embed)
                break
        else:
            report['users'].append({
                'name': user.name,
                'reasons': [reason, ]
            })
            if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
                avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
            else:
                avi = ctx.message.author.avatar_url_as(static_format='png')

            embed = discord.Embed(title=f"*O {user.name} foi warnado pelo {ctx.message.author.name}*",
                                  colour=discord.Colour(0x370c5e), description=f"Pelo seguinte motivo: {reason}")

            embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")
            embed.set_footer(icon_url=betina_icon,
                              text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                        self.client.user.name,
                                                                                        year()))

            await ctx.send(embed=embed, delete_after=10)
            if guild_id not in digit_log:
                return

            guild = ctx.guild.get_channel(int(digit_log[guild_id]))

            embed = discord.Embed(
                title=f"{ctx.message.author.name} usou o comando warn em {user.name} no canal #{texto.channel}",
                colour=discord.Colour(0x370c5e), description=f"Pelo seguinte motivo: {reason}")

            embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")

            embed.set_footer(icon_url=betina_icon,
                              text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                        self.client.user.name,
                                                                                        year()))
            await guild.send(embed=embed)
        with open('reports.json', 'w+') as f:
            json.dump(report, f)

    @warn.error
    async def warn_handler(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title="Comando $warn:", colour=discord.Colour(0x370c5e),
                                  description="Dá um warn no usuário"
                                              "\n \n**Como usar: $warn <usuário> <motivo> (opcional)**")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(icon_url=betina_icon,
                              text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                        self.client.user.name,
                                                                                        year()))
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Expulsar membros`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$warn @fulano xingou o moderador", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$aviso, $wrn.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")
        elif isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'user':
                embed = discord.Embed(title="Comando $warn:", colour=discord.Colour(0x370c5e),
                                      description="Dá um warn no usuário"
                                                  "\n \n**Como usar: $warn <usuário> <motivo> (opcional)**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                                "ter a permissão de* ``"
                                                                "Expulsar membros`` *para utilizar este comando!*",
                                inline=False)
                embed.add_field(name="📖**Exemplos:**", value="$warn @fulano xingou o moderador", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$aviso, $wrn.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(pass_context=True, name='warnings', aliases=['avisos', 'wrns'])
    @has_permissions(kick_members=True)
    async def warnings(self, ctx, user: discord.User):
        texto = await ctx.get_message(ctx.message.id)
        guild_id = str(ctx.guild.id)
        if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
            avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
        else:
            avi = ctx.message.author.avatar_url_as(static_format='png')

        if user == None:
            embed = discord.Embed(title="Comando $warnings:", colour=discord.Colour(0x370c5e),
                                  description="Diz quantos warnings um usuário recebeu"
                                              "\n \n**Como usar: $warnings <usuário>**")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                       self.client.user.name,
                                                                                       year()))
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Expulsar membros`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$warnings @fulano\n$warnings @sicrano", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$avisos, $wrns.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")
            return
        else:
            for current_user in report['users']:
                if user.name == current_user['name']:
                    if len(current_user['reasons']) == 1:
                        await ctx.send(f"{user.name} foi warnado {len(current_user['reasons'])} vez : {' ,'.join(current_user['reasons'])}")
                        if guild_id not in digit_log:
                            return

                        guild = ctx.guild.get_channel(int(digit_log[guild_id]))

                        embed = discord.Embed(
                            title=f"*{ctx.message.author.name} usou o comando warnings em {user.name} no canal #{texto.channel}",
                            colour=discord.Colour(0x370c5e))

                        embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")

                        embed.set_footer(icon_url=betina_icon,
                                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                                   self.client.user.name,
                                                                                                   year()))
                        await guild.send(embed=embed)
                        break
                    else:
                        await ctx.send(f"{user.name} foi warnado {len(current_user['reasons'])} vezes : {' ,'.join(current_user['reasons'])}")
                        break
            else:
                await ctx.send(f"{user.name} nunca recebeu um warn!")
                if guild_id not in digit_log:
                    return

                guild = ctx.guild.get_channel(int(digit_log[guild_id]))

                embed = discord.Embed(
                    title=f"{ctx.message.author.name} usou o comando warnings em {user.name} no canal #{texto.channel}",
                    colour=discord.Colour(0x370c5e))

                embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")

                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                await guild.send(embed=embed)

    @warnings.error
    async def warnings_handler(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title="Comando $warnings:", colour=discord.Colour(0x370c5e),
                                  description="Diz quantos warnings o usuário levou"
                                              "\n \n**Como usar: $warnings <usuário>**")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                       self.client.user.name,
                                                                                       year()))
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Expulsar membros`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$warnings @fulano\n$warnings @sicrano", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$avisos, $wrns.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")
        elif isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'user':
                embed = discord.Embed(title="Comando $warnings:", colour=discord.Colour(0x370c5e),
                                      description="Diz quantos warnings o usuário levou"
                                                  "\n \n**Como usar: $warnings <usuário>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                                "ter a permissão de* ``"
                                                                "Expulsar membros`` *para utilizar este comando!*",
                                inline=False)
                embed.add_field(name="📖**Exemplos:**", value="$warnings @fulano\n$warnings @sicrano", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$avisos, $wrns.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='clearlastwarn', aliases=['limpawarn', 'tirawarn'])
    @has_permissions(ban_members=True)
    async def dewarn(self, ctx, user: discord.User):
        texto = await ctx.get_message(ctx.message.id)
        guild_id = str(ctx.guild.id)
        if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
            avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
        else:
            avi = ctx.message.author.avatar_url_as(static_format='png')

        for current_user in report['users']:
            if current_user['name'] == user.name:
                embed = discord.Embed(title=f"*O {user.name} teve o ultimo warn limpo por {ctx.message.author.name}*",
                                      colour=discord.Colour(0x370c5e), description='Ultimo warn limpo: {}'.format(current_user['reasons'][-1]))

                embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))

                await ctx.send(embed=embed, delete_after=10)
                if guild_id not in digit_log:
                    return

                guild = ctx.guild.get_channel(int(digit_log[guild_id]))

                embed = discord.Embed(
                    title=f"{ctx.message.author.name} usou o comando clearlastwarn em {user.name} no canal #{texto.channel}",
                    colour=discord.Colour(0x370c5e), description='Ultimo warn limpo: {}'.format(current_user['reasons'][-1]))

                embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")

                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                await guild.send(embed=embed)
                del current_user['reasons'][-1]
                break
        else:
            embed = discord.Embed(title=f"*O {user.name} não tem nenhum warn para ser apagado!*",
                                  colour=discord.Colour(0x370c5e))

            embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                       self.client.user.name,
                                                                                       year()))

            await ctx.send(embed=embed, delete_after=10)
            if guild_id not in digit_log:
                return

            guild = ctx.guild.get_channel(int(digit_log[guild_id]))

            embed = discord.Embed(
                title=f"{ctx.message.author.name} usou o comando clearlastwarn em {user.name} no canal #{texto.channel}",
                colour=discord.Colour(0x370c5e))

            embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")

            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                       self.client.user.name,
                                                                                       year()))
            await guild.send(embed=embed)

        with open('reports.json', 'w+') as f:
            json.dump(report, f)

    @dewarn.error
    async def tira_warn_handler(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title="Comando $clearlastwarn:", colour=discord.Colour(0x370c5e),
                                  description="Tira o ultimo warn do usuário"
                                              "\n \n**Como usar: $tirawarn <usuário>**")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                       self.client.user.name,
                                                                                       year()))
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Banir membros`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$clearlastwarn @fulano\n$tirawarn @sicrano", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$tirawarn, $limpawarn.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")
        elif isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'user':
                embed = discord.Embed(title="Comando $clearlastwarn:", colour=discord.Colour(0x370c5e),
                                      description="Tira o ultimo warn do usuário"
                                                  "\n \n**Como usar: $tirawarn <usuário>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                                "ter a permissão de* ``"
                                                                "Banir membros`` *para utilizar este comando!*",
                                inline=False)
                embed.add_field(name="📖**Exemplos:**", value="$clearlastwarn @fulano\n$tirawarn @sicrano",
                                inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$tirawarn, $limpawarn.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


    @commands.guild_only()
    @commands.command(name='mute', aliases=['mutar', 'silenciar'])
    @has_permissions(kick_members=True, manage_roles=True)
    async def mute(self, ctx, member: discord.Member, time: int = 1):
        texto = await ctx.get_message(ctx.message.id)
        guild_id = str(ctx.guild.id)
        if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
            avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
        else:
            avi = ctx.message.author.avatar_url_as(static_format='png')

        roles = [cargos.name for cargos in member.roles if cargos.name != "@everyone"]
        cargos_dos_mutados[str(member.id)] = roles
        for cargos in roles:
            if cargos == 'Mutado':
                await ctx.send('O usuário já está mutado!')
                return
            atirar = discord.utils.get(ctx.guild.roles, name=str(cargos))
            await member.remove_roles(atirar)

        role = discord.utils.get(ctx.guild.roles, name='Mutado')
        if role not in ctx.guild.roles:
            await ctx.guild.create_role(name='Mutado', colour=discord.Colour(0x36393F), reason='Foi criado para mutar os usuários')
            await member.add_roles(role)

        await member.add_roles(role)

        if guild_id not in digit_log:
            return

        guild = ctx.guild.get_channel(int(digit_log[guild_id]))

        embed = discord.Embed(
            title=f"{ctx.message.author.name} usou o comando mute em {member.name} no canal #{texto.channel}",
            colour=discord.Colour(0x370c5e))

        embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")

        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                   self.client.user.name,
                                                                                   year()))
        await guild.send(embed=embed)

        with open('mutados.json', 'w') as file:
            json.dump(cargos_dos_mutados, file)

    @mute.error
    async def mute_handler(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title="Comando $mute:", colour=discord.Colour(0x370c5e),
                                  description="Muta o usuário"
                                              "\n \n**Como usar: $mute <usuário>**")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                       self.client.user.name,
                                                                                       year()))
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Expulsar membros e Gerenciar cargos"
                                                            "`` *para utilizar este comando!\n"
                                                            "Eu também preciso de estar com o cargo acima do usuário"
                                                            " a ser mutado!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$mute @fulano\n$mute @sicrano", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$mutar, $silenciar.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")

        elif isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $mute:", colour=discord.Colour(0x370c5e),
                                      description="Muta o usuário"
                                                  "\n \n**Como usar: $mute <usuário>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                                "ter a permissão de* ``"
                                                                "Expulsar membros e Gerenciar cargos"
                                                                "`` *para utilizar este comando!\n"
                                                                "Eu também preciso de estar com o cargo acima do usuário"
                                                                " a ser mutado!*",
                                inline=False)
                embed.add_field(name="📖**Exemplos:**", value="$mute @fulano\n$mute @sicrano", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$mutar, $silenciar.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

    @commands.guild_only()
    @commands.command(name='unmute', aliases=['desmutar', 'semsilenciar'])
    @has_permissions(kick_members=True, manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, time: int = 1):
        texto = await ctx.get_message(ctx.message.id)
        guild_id = str(ctx.guild.id)
        if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
            avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
        else:
            avi = ctx.message.author.avatar_url_as(static_format='png')
        if str(member.id) not in cargos_dos_mutados:
            return
        for cargos in cargos_dos_mutados[str(member.id)]:
            adicionar = discord.utils.get(ctx.guild.roles, name=str(cargos))
            await member.add_roles(adicionar)
        mute = discord.utils.get(ctx.guild.roles, name='Mutado')
        await member.remove_roles(mute)
        del cargos_dos_mutados[str(member.id)]
        if guild_id not in digit_log:
            return

        guild = ctx.guild.get_channel(int(digit_log[guild_id]))

        embed = discord.Embed(
            title=f"{ctx.message.author.name} usou o comando unmute em {member.name} no canal #{texto.channel}",
            colour=discord.Colour(0x370c5e))

        embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")

        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                   self.client.user.name,
                                                                                   year()))
        await guild.send(embed=embed)
        with open('mutados.json', 'w') as file:
            json.dump(cargos_dos_mutados, file)

    @unmute.error
    async def unmute_handler(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title="Comando $unmute:", colour=discord.Colour(0x370c5e),
                                  description="Tira o mute do usuário"
                                              "\n \n**Como usar: $unmute <usuário>**\n \n"
                                              "Para utilizar corretamente, redefina as permissões do cargo ``everyone``"
                                              " para nenhuma permissão.")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                       self.client.user.name,
                                                                                       year()))
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Expulsar membros e Gerenciar"
                                                            " cargos`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$unmute @fulano\n$unmute @sicrano", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$desmutar, $semsilenciar.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")

        elif isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $unmute:", colour=discord.Colour(0x370c5e),
                                      description="Tira o mute do usuário"
                                                  "\n \n**Como usar: $unmute <usuário>**\n \n"
                                                  "Para utilizar corretamente, redefina as permissões do cargo ``everyone``"
                                                  " para nenhuma permissão.")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                                "ter a permissão de* ``"
                                                                "Expulsar membros e Gerenciar"
                                                                " cargos`` *para utilizar este comando!*",
                                inline=False)
                embed.add_field(name="📖**Exemplos:**", value="$unmute @fulano\n$unmute @sicrano", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$desmutar, $semsilenciar.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

    @commands.cooldown(2, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='sugestão', aliases=['suggestion', 'sug'])
    async def suggestion(self, ctx, channel: typing.Optional[discord.TextChannel] = None, *, arg: str):
        if channel is None:
            texto = await ctx.get_message(ctx.message.id)
            guild_id = str(ctx.guild.id)
            if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
                avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
            else:
                avi = ctx.message.author.avatar_url_as(static_format='png')

            if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
                avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
            else:
                avi = ctx.message.author.avatar_url_as(static_format='png')

            embed = discord.Embed(title="Sugestão: ", colour=discord.Colour(0x370c5e),
                                  description=f"{arg}")
            embed.set_footer(text="Usado às {} Horário de Brasília | {} {} .".format(hora(), ctx.message.author.name, year()), icon_url=avi)
            mensagem = await ctx.send(embed=embed)
            await mensagem.add_reaction("confirm:540714191938519071")
            await mensagem.add_reaction("deny:540714208111755265")
            await mensagem.add_reaction("report:540714227585908754")
            if guild_id not in digit_log:
                return

            guild = ctx.guild.get_channel(int(digit_log[guild_id]))

            embed = discord.Embed(
                title=f"{ctx.message.author.name} usou o comando sugestão no canal #{texto.channel}",
                colour=discord.Colour(0x370c5e), description=f'Sugestão: {arg}')

            embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")

            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                       self.client.user.name,
                                                                                       year()))
            await guild.send(embed=embed)
        else:
            texto = await ctx.get_message(ctx.message.id)
            guild_id = str(ctx.guild.id)
            if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
                avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
            else:
                avi = ctx.message.author.avatar_url_as(static_format='png')

            if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
                avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
            else:
                avi = ctx.message.author.avatar_url_as(static_format='png')

            embed = discord.Embed(title="Sugestão: ", colour=discord.Colour(0x370c5e),
                                  description=f"{arg}")
            embed.set_footer(
                text="Usado às {} Horário de Brasília | {} {} .".format(hora(), ctx.message.author.name, year()),
                icon_url=avi)
            await ctx.send(f'Mensagem enviada para o canal {channel}')
            mensagem = await channel.send(embed=embed)
            await mensagem.add_reaction("confirm:540714191938519071")
            await mensagem.add_reaction("deny:540714208111755265")
            await mensagem.add_reaction("report:540714227585908754")
            if guild_id not in digit_log:
                return

            guild = ctx.guild.get_channel(int(digit_log[guild_id]))

            embed = discord.Embed(
                title=f"{ctx.message.author.name} usou o comando sugestão no canal #{texto.channel}",
                colour=discord.Colour(0x370c5e), description=f'Sugestão: {arg}')

            embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")

            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                       self.client.user.name,
                                                                                       year()))
            await guild.send(embed=embed)

    @suggestion.error
    async def suggestion_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'arg':
                embed = discord.Embed(title="Comando $sugestão:", colour=discord.Colour(0x370c5e),
                                      description="Começa a votação sobre uma sugestão!"
                                                  "\n \n**Como usar: $sugestão <#canal> <mensagem>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))

                embed.add_field(name="📖**Exemplos:**", value="$sugestão que tal adicionar uma função e sugestão"
                                                              "\n$sugestão criar um canal de jogos", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$sug, $suggestion.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='kick')
    @has_permissions(kick_members=True)
    async def kickar(self, ctx, member: discord.Member, *, arg=None):
        if str(member.id) == '527565353199337474':
            return await ctx.send('<:stop:540852590083178497> **Não tem como eu me kickar do seu servidor!**')
        texto = await ctx.get_message(ctx.message.id)
        guild_id = str(ctx.guild.id)
        if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
            avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
        else:
            avi = ctx.message.author.avatar_url_as(static_format='png')
        if member.top_role >= member.guild.me.top_role:
            embed = discord.Embed(title="Comando $kick:", colour=discord.Colour(0x370c5e),
                                  description="Kicka o usuário do servidor por um motivo"
                                              "\n \n**Como usar: $kick <usuário> <motivo> (opcional)**")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                       year()))
            embed.add_field(name="👮**Permissões:**", value="*Você e o bot precisam "
                                                            "ter a permissão de* ``"
                                                            "Expulsar membros e estar no topo dos cargos`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$kick @fulano\n$kick @fulano xingou o moderador",
                            inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")
            return
        else:
            if arg == None:
                reason = 'Sem motivos específicados!'
            else:
                reason = arg

            gif1 = random.choice(kick)
            gif2 = random.choice(omg)
            msg1 = '**Você estava tentando se expulsar ?**'
            msg2 = '{} foi Kickado do servidor {} pelo seguinte motivo: {}'.format(member, ctx.guild.name, reason)
            msg3 = 'Você foi Kickado do servidor {} pelo seguinte motivo: {}'.format(ctx.guild.name, reason)
            if member == ctx.message.author:

                embed = discord.Embed(title="**Pensativa...**", colour=discord.Colour(0x370c5e),
                                      description="{}".format(msg1))
                embed.set_image(url="{}".format(gif2))
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                await ctx.channel.send(embed=embed)
                if guild_id not in digit_log:
                    return

                guild = ctx.guild.get_channel(int(digit_log[guild_id]))

                embed = discord.Embed(
                    title=f"{ctx.message.author.name} Tentou se Kickar do servidor no canal: #{texto.channel}",
                    colour=discord.Colour(0x370c5e))

                embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")

                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                await guild.send(embed=embed)
                return
            else:
                embed = discord.Embed(title="**Kick!**", colour=discord.Colour(0x370c5e), description="{}".format(msg2))
                embed.set_image(url="{}".format(gif1))
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                mbd = discord.Embed(title="**Kick!**", colour=discord.Colour(0x370c5e), description="{}".format(msg3))
                mbd.set_image(url="{}".format(gif1))
                mbd.set_footer(icon_url=betina_icon,
                               text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                         year()))

                if not member.bot:
                    await member.send(embed=mbd)
                    await ctx.channel.send(embed=embed)
                    if guild_id not in digit_log:
                        return

                    guild = ctx.guild.get_channel(int(digit_log[guild_id]))

                    embed = discord.Embed(
                        title=f"{ctx.message.author.name} Kickou o usuário {member.name} no canal: #{texto.channel}",
                        colour=discord.Colour(0x370c5e), description=f"pelo seguinte motivo: {reason}")

                    embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")

                    embed.set_footer(icon_url=betina_icon,
                                     text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                               self.client.user.name,
                                                                                               year()))
                    await guild.send(embed=embed)
                    await ctx.guild.kick(member)

                else:
                    await ctx.channel.send(embed=embed)
                    if guild_id not in digit_log:
                        return

                    guild = ctx.guild.get_channel(int(digit_log[guild_id]))

                    embed = discord.Embed(
                        title=f"{ctx.message.author.name} Kickou o usuário {member.name} no canal: #{texto.channel}",
                        colour=discord.Colour(0x370c5e), description=f"pelo seguinte motivo: {reason}")

                    embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")

                    embed.set_footer(icon_url=betina_icon,
                                     text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                               self.client.user.name,
                                                                                               year()))
                    await guild.send(embed=embed)
                    await ctx.guild.kick(member)

    @kickar.error
    async def kickar_handler(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title="Comando $kick:", colour=discord.Colour(0x370c5e),
                                  description="Kicka o usuário do servidor por um motivo"
                                              "\n \n**Como usar: $kick <usuário> <motivo> (opcional)**")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                       year()))
            embed.add_field(name="👮**Permissões:**", value="*Você e o bot precisam "
                                                            "ter a permissão de* ``"
                                                            "Expulsar membros e estar no topo dos cargos`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$kick @fulano\n$kick @fulano xingou o moderador",
                            inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")
        elif isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $kick:", colour=discord.Colour(0x370c5e),
                                      description="Kicka o usuário do servidor por um motivo"
                                                  "\n \n**Como usar: $kick <usuário> <motivo> (opcional)**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                embed.add_field(name="👮**Permissões:**", value="*Você e o bot precisam "
                                                                "ter a permissão de* ``"
                                                                "Expulsar membros e estar no topo dos cargos`` *para utilizar este comando!*",
                                inline=False)
                embed.add_field(name="📖**Exemplos:**", value="$kick @fulano\n$kick @fulano xingou o moderador",
                                inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def emojis(self, ctx):
        server = ctx.message.guild
        emojis = [str(x) for x in server.emojis]
        await ctx.message.delete()
        await ctx.send("".join(emojis))

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='roleinfo', aliases=['ri', 'cargoinfo'])
    async def roleinfo(self, ctx, *, role: discord.Role):
        guild = ctx.message.guild
        guild_roles = ctx.message.guild.roles
        guild_id = guild.id
        all_users = [x for x in role.members]
        em = discord.Embed(title=f'Informações do cargo {role}', color=role.color)
        em.add_field(name='📛 Nome:', value=role.name)
        em.add_field(name='💻ID:', value=role.id)
        em.add_field(name='👥 Usuários:', value=str(len(role.members)))
        em.add_field(name='<a:Conga:518188538114605074> Cor do cargo Hex:', value=str(role.color))
        em.add_field(name='<a:Conga:518188538114605074> Cor do cargo RGB:', value=role.color.to_rgb())
        if role.mentionable:
            em.add_field(name='<a:MEGA:525468489583034368> Mencionavel:', value='Sim')
        else:
            em.add_field(name='<a:MEGA:525468489583034368> Mencionavel:', value='Não')
        if role.hoist:
            em.add_field(name='<a:MEGA:525468489583034368> Separada:', value='Sim')
        else:
            em.add_field(name='<a:MEGA:525468489583034368> Separada:', value='Não')
        em.add_field(name='<a:MEGA:525468489583034368> Posição:', value=role.position)
        if role.managed:
            em.add_field(name='⚙ Gerenciada:', value='Sim')
        else:
            em.add_field(name='⚙ Gerenciada:', value='Não')
        em.add_field(name='⭐ Criado em:', value=role.created_at.__format__('%d de %b de %Y às %H:%M:%S'))
        if len(role.members) >= 1:
            em.add_field(name='👥 Usuários:', value=len(all_users), inline=False)
        else:
            em.add_field(name='👥 Usuários', value=0, inline=False)
        em.set_thumbnail(url='http://www.colorhexa.com/{}.png'.format(str(role.color).strip("#")))
        em.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                   self.client.user.name,
                                                                                   year()))
        await ctx.send(embed=em)

        if guild_id not in digit_log:
            return

        guild = ctx.guild.get_channel(int(digit_log[guild_id]))

        embed1 = discord.Embed(
            title=f"{ctx.message.author.name} usou o comando roleinfo no "
            f"canal {ctx.message.channel.mention}",
            colour=discord.Colour(0x370c5e))

        embed1.set_author(name=f"{ctx.message.author.mention}", icon_url=f"{ctx.message.author.avatar_url}")

        embed1.set_footer(icon_url=betina_icon,
                      text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                year()))
        await guild.send(embed=embed1)

    @roleinfo.error
    async def roleinfo_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'role':
                embed = discord.Embed(title="Comando $roleinfo:", colour=discord.Colour(0x370c5e),
                                      description="Diz as informações sobre o cargo "
                                                  "\n \n**Como usar: $roleinfo <cargo>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                embed.add_field(name="📖**Exemplos:**", value="$ri @fulano\n$roleinfo @membro",
                                inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$cargoinfo, $ri.``", inline=False)
                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


def setup(client):
    client.add_cog(Administração(client))
