import discord
import discord.errors
from main import GUILD_ID
from discord import app_commands
from discord.ext import commands

class ticket_view(discord.ui.View):
    def __init__(self, button_label: str = "Create Ticket"):
        super().__init__(timeout=None)

        self.ticket_button = discord.ui.Button(label=button_label,
                                               style=discord.ButtonStyle.primary,
                                               emoji="📩", custom_id="ticket_btn")
        self.ticket_button.callback = self.ticket_button_callback
        self.add_item(self.ticket_button)

    async def ticket_button_callback(self, inter: discord.Interaction):
        ticket_category = discord.utils.get(inter.guild.categories, name="Ticket")
        overwrites = {
            inter.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            inter.user: discord.PermissionOverwrite(view_channel=True),
        }
        ticket_channel = await inter.guild.create_text_channel(name=f"Ticket-{inter.user.name.lower()}", overwrites=overwrites,
                                                               reason=f"Ticket for {inter.user}", category=ticket_category)

        await ticket_channel.send(f"This ticket is created by {inter.user.mention}. Please wait patiently for our support team to reach you.")
        await inter.response.send_message(f"Ticket is opened at: {ticket_channel.mention}", ephemeral=True)

class ticket(commands.Cog, name="ticket"):
    def __init__(self, bot):
        self.bot=bot

    async def cog_load(self):
        self.bot.add_view(ticket_view())

    @app_commands.command(name="ticket", description="Setup the ticket system.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.describe(channel_name="The channel name that will have the ticket message.", label="Ticket button's message.")
    async def ticket(self, inter: discord.Interaction, channel_name: str, label: str):
        ticket_category = discord.utils.get(inter.guild.categories, name="Ticket")
        if ticket_category is None:
            ticket_category = await inter.guild.create_category(name="Ticket", reason="No category named \"Ticket\" was found.")
        ticket_channel = await inter.guild.create_text_channel(name=channel_name, reason="Created Ticket System!", category=ticket_category)

        embed = discord.Embed(description="For opening a ticket, please click the button below!", color=discord.Color.blurple())
        view = ticket_view(button_label=label)
        await ticket_channel.send(embed=embed, view=view)

        await inter.response.send_message(f"Ticket System Setup was successful at: {ticket_channel.mention}")

    @commands.command()
    async def pong(self, ctx):
        await ctx.reply("Ping!")
        await ctx.send(self.bot.user.mention)

async def setup(bot):
    await bot.add_cog(ticket(bot))
