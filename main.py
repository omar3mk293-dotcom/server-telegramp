import discord
from discord import app_commands
from discord.ext import commands

# إعداد البوت مع الصلاحيات (Intents)
intents = discord.Intents.default()
intents.members = True # حظر الأعضاء للإرسال لهم بالخاص

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # مزامنة أوامر السلاش كوماندر مع ديسكورد
        await self.tree.sync()
        print("Slash Commands Synced successfully!")

bot = MyBot()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# أمر البرودكاست بالسلاش كوماند
@bot.tree.command(name="broadcast", description="إرسال برودكاست لجميع أعضاء السيرفر")
@app_commands.describe(message="الرسالة التي تريد إرسالها للأعضاء")
@app_commands.checks.has_permissions(administrator=True) # مخصص للأدمنية فقط
async def broadcast(interaction: discord.Interaction, message: str):
    await interaction.response.send_message("جاري إرسال البرودكاست...", ephemeral=True)
    
    guild = interaction.guild
    success = 0
    fail = 0

    for member in guild.members:
        if member.bot:
            continue
        try:
            # إرسال الرسالة كـ DM لكل عضو
            await member.send(f"**رسالة من سيرفر {guild.name}:**\n\n{message}")
            success += 1
        except Exception:
            fail += 1

    await interaction.followup.send(f"تم الإرسال بنجاح إلى: **{success}** عضو.\nفشل الإرسال إلى: **{fail}** عضو (خاصهم مقفول).", ephemeral=True)

# التعامل مع خطأ عدم وجود صلاحية الأدمن
@broadcast.error
async def broadcast_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("ما عندك صلاحية الأدمن لاستخدام هذا الأمر!", ephemeral=True)

# ضع توكن البوت مالتك هنا
bot.run('MTU2MzU2ODk5ODA0MDM0NjcxNQ.GZiFIb.Dy2jFiua72r0_lcEopKO_RfMcFweoC_DoxU3kY')
