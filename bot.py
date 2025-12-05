import os
import discord
from discord.ext import commands
from openai import OpenAI
from dotenv import load_dotenv
import asyncio
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/logs/bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('DiscordAI')

# Load environment variables
load_dotenv()

# Initialize Groq client
groq_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True  # WAJIB untuk membaca pesan
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Conversation history storage (per channel)
conversation_history = {}

# Rate limiting storage
user_cooldowns = {}
COOLDOWN_SECONDS = 3
MAX_REQUESTS_PER_MINUTE = 10

# Model configuration
MODELS = {
    'groq': 'groq/compound',
    'whisper': 'whisper-large-v3-turbo',
    'openai': 'openai/gpt-oss-safeguard-20b'
}
current_model = MODELS['groq']


def check_rate_limit(user_id: int) -> bool:
    """Check if user is rate limited"""
    now = datetime.now().timestamp()
    
    if user_id not in user_cooldowns:
        user_cooldowns[user_id] = []
    
    # Remove old requests (older than 1 minute)
    user_cooldowns[user_id] = [
        req_time for req_time in user_cooldowns[user_id] 
        if now - req_time < 60
    ]
    
    # Check if exceeded limit
    if len(user_cooldowns[user_id]) >= MAX_REQUESTS_PER_MINUTE:
        return False
    
    user_cooldowns[user_id].append(now)
    return True


async def get_ai_response(messages: list, model: str = None) -> str:
    """Get response from Groq API"""
    try:
        response = await asyncio.to_thread(
            groq_client.chat.completions.create,
            model=model or current_model,
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error getting AI response: {e}")
        raise


def get_channel_history(channel_id: int) -> list:
    """Get conversation history for a channel"""
    if channel_id not in conversation_history:
        conversation_history[channel_id] = []
    return conversation_history[channel_id]


def add_to_history(channel_id: int, role: str, content: str):
    """Add message to conversation history"""
    history = get_channel_history(channel_id)
    history.append({"role": role, "content": content})
    
    # Keep only last 10 messages for context
    if len(history) > 10:
        conversation_history[channel_id] = history[-10:]


def create_embed(title: str, description: str, color: discord.Color, 
                 footer: str = None, author=None) -> discord.Embed:
    """Create a formatted embed"""
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=datetime.now()
    )
    
    if footer:
        embed.set_footer(text=footer)
    
    if author:
        embed.set_footer(
            text=f"Requested by {author.name}",
            icon_url=author.avatar.url if author.avatar else None
        )
    
    return embed


@bot.event
async def on_ready():
    """Bot startup event"""
    logger.info(f'✅ Bot logged in as {bot.user.name} (ID: {bot.user.id})')
    logger.info(f'📊 Connected to {len(bot.guilds)} servers')
    
    # Set bot status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="!help | @mention me"
        )
    )
    
    # Create data directories if not exist
    os.makedirs('data/logs', exist_ok=True)
    os.makedirs('data/cache', exist_ok=True)
    
    print("\n" + "="*50)
    print(f"🤖 {bot.user.name} is ONLINE!")
    print(f"📝 Prefix: !")
    print(f"🔗 Invite URL: https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot")
    print("="*50 + "\n")


@bot.event
async def on_message(message):
    """Handle all incoming messages"""
    # Ignore bot's own messages
    if message.author == bot.user:
        return
    
    # Handle mentions
    if bot.user.mentioned_in(message) and not message.mention_everyone:
        # Remove the mention from content
        question = message.content.replace(f'<@{bot.user.id}>', '').strip()
        
        if not question:
            embed = create_embed(
                "❓ Pertanyaan Kosong",
                "Silakan mention saya dengan pertanyaan Anda!\nContoh: `@bot Apa itu Python?`",
                discord.Color.orange(),
                author=message.author
            )
            await message.reply(embed=embed)
            return
        
        # Check rate limit
        if not check_rate_limit(message.author.id):
            embed = create_embed(
                "⏳ Rate Limit",
                f"Anda terlalu banyak request! Tunggu sebentar.\nMax {MAX_REQUESTS_PER_MINUTE} requests per menit.",
                discord.Color.red(),
                author=message.author
            )
            await message.reply(embed=embed)
            return
        
        # Show typing indicator
        async with message.channel.typing():
            try:
                # Get conversation history
                add_to_history(message.channel.id, "user", question)
                history = get_channel_history(message.channel.id)
                
                # Get AI response
                ai_response = await get_ai_response(history)
                add_to_history(message.channel.id, "assistant", ai_response)
                
                # Create response embed
                embed = discord.Embed(
                    title="💬 Balasan AI",
                    color=discord.Color.blue(),
                    timestamp=datetime.now()
                )
                embed.add_field(name="📝 Pertanyaan", value=question[:1024], inline=False)
                embed.add_field(name="🤖 Jawaban", value=ai_response[:1024], inline=False)
                embed.set_footer(
                    text=f"Requested by {message.author.name} | Model: {current_model}",
                    icon_url=message.author.avatar.url if message.author.avatar else None
                )
                
                await message.reply(embed=embed)
                logger.info(f"✅ Mention response sent to {message.author} in {message.guild.name}")
                
            except Exception as e:
                logger.error(f"❌ Error in mention handler: {e}")
                embed = create_embed(
                    "❌ Error",
                    f"Maaf, terjadi kesalahan:\n```{str(e)[:200]}```",
                    discord.Color.red(),
                    author=message.author
                )
                await message.reply(embed=embed)
    
    # Process commands
    await bot.process_commands(message)


@bot.command(name='ask')
async def ask(ctx, *, question: str = None):
    """Ask AI a question: !ask [pertanyaan]"""
    if not question:
        embed = create_embed(
            "❓ Format Salah",
            "**Usage:** `!ask [pertanyaan]`\n**Contoh:** `!ask Apa itu Discord bot?`",
            discord.Color.orange(),
            author=ctx.author
        )
        await ctx.reply(embed=embed)
        return
    
    # Check rate limit
    if not check_rate_limit(ctx.author.id):
        embed = create_embed(
            "⏳ Rate Limit",
            f"Anda terlalu banyak request! Tunggu sebentar.\nMax {MAX_REQUESTS_PER_MINUTE} requests per menit.",
            discord.Color.red(),
            author=ctx.author
        )
        await ctx.reply(embed=embed)
        return
    
    async with ctx.typing():
        try:
            # Get conversation history
            add_to_history(ctx.channel.id, "user", question)
            history = get_channel_history(ctx.channel.id)
            
            # Get AI response
            ai_response = await get_ai_response(history)
            add_to_history(ctx.channel.id, "assistant", ai_response)
            
            # Create response embed
            embed = discord.Embed(
                title="💬 Balasan AI",
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )
            embed.add_field(name="📝 Pertanyaan", value=question[:1024], inline=False)
            embed.add_field(name="🤖 Jawaban", value=ai_response[:1024], inline=False)
            embed.set_footer(
                text=f"Requested by {ctx.author.name} | Model: {current_model}",
                icon_url=ctx.author.avatar.url if ctx.author.avatar else None
            )
            
            await ctx.reply(embed=embed)
            logger.info(f"✅ Ask command used by {ctx.author} in {ctx.guild.name}")
            
        except Exception as e:
            logger.error(f"❌ Error in ask command: {e}")
            embed = create_embed(
                "❌ Error",
                f"Maaf, terjadi kesalahan:\n```{str(e)[:200]}```",
                discord.Color.red(),
                author=ctx.author
            )
            await ctx.reply(embed=embed)


@bot.command(name='ping')
async def ping(ctx):
    """Check bot latency: !ping"""
    latency = round(bot.latency * 1000)
    
    # Color based on latency
    if latency < 100:
        color = discord.Color.green()
        status = "Sangat Baik"
    elif latency < 200:
        color = discord.Color.yellow()
        status = "Baik"
    else:
        color = discord.Color.red()
        status = "Lambat"
    
    embed = create_embed(
        "🏓 Pong!",
        f"**Latency:** {latency}ms\n**Status:** {status}",
        color,
        author=ctx.author
    )
    
    await ctx.reply(embed=embed)
    logger.info(f"📊 Ping: {latency}ms")


@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    """Clear messages: !clear [jumlah] (max: 20)"""
    if amount < 1 or amount > 20:
        embed = create_embed(
            "⚠️ Invalid Amount",
            "Jumlah pesan harus antara 1-20",
            discord.Color.orange(),
            author=ctx.author
        )
        await ctx.reply(embed=embed)
        return
    
    deleted = await ctx.channel.purge(limit=amount + 1)
    
    embed = create_embed(
        "🗑️ Messages Cleared",
        f"Berhasil menghapus {len(deleted) - 1} pesan",
        discord.Color.green(),
        author=ctx.author
    )
    
    msg = await ctx.send(embed=embed)
    await asyncio.sleep(5)
    await msg.delete()
    
    logger.info(f"🗑️ {len(deleted) - 1} messages cleared by {ctx.author} in {ctx.guild.name}")


@bot.command(name='help')
async def help_command(ctx):
    """Show help menu: !help"""
    embed = discord.Embed(
        title="📚 Discord AI Chatbot - Help Menu",
        description="Bot AI dengan Groq API Integration",
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )
    
    embed.add_field(
        name="🤖 AI Commands",
        value=(
            "`!ask [pertanyaan]` - Tanya apapun ke AI\n"
            "`@mention [pertanyaan]` - Chat via mention\n"
            "`!model [nama]` - Ganti AI model"
        ),
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Utility Commands",
        value=(
            "`!ping` - Cek bot latency\n"
            "`!status` - System status\n"
            "`!help` - Menu ini"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🛡️ Admin Commands",
        value=(
            "`!clear [jumlah]` - Hapus pesan (max 20)\n"
            "`!reset` - Reset conversation history"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📊 Info",
        value=(
            f"**Model:** {current_model}\n"
            f"**Prefix:** !\n"
            f"**Servers:** {len(bot.guilds)}\n"
            f"**Latency:** {round(bot.latency * 1000)}ms"
        ),
        inline=False
    )
    
    embed.set_footer(
        text=f"Requested by {ctx.author.name}",
        icon_url=ctx.author.avatar.url if ctx.author.avatar else None
    )
    
    await ctx.reply(embed=embed)


@bot.command(name='status')
async def status(ctx):
    """Check bot status: !status"""
    embed = discord.Embed(
        title="📊 Bot Status",
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )
    
    embed.add_field(
        name="🤖 Bot Info",
        value=(
            f"**Name:** {bot.user.name}\n"
            f"**ID:** {bot.user.id}\n"
            f"**Latency:** {round(bot.latency * 1000)}ms"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📈 Statistics",
        value=(
            f"**Servers:** {len(bot.guilds)}\n"
            f"**Users:** {sum(g.member_count for g in bot.guilds)}\n"
            f"**Channels:** {len(list(bot.get_all_channels()))}"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🧠 AI Model",
        value=(
            f"**Current:** {current_model}\n"
            f"**Provider:** Groq\n"
            f"**Status:** ✅ Online"
        ),
        inline=False
    )
    
    embed.set_footer(
        text=f"Requested by {ctx.author.name}",
        icon_url=ctx.author.avatar.url if ctx.author.avatar else None
    )
    
    await ctx.reply(embed=embed)


@bot.command(name='reset')
@commands.has_permissions(manage_messages=True)
async def reset(ctx):
    """Reset conversation history: !reset"""
    if ctx.channel.id in conversation_history:
        del conversation_history[ctx.channel.id]
    
    embed = create_embed(
        "🔄 History Reset",
        "Conversation history untuk channel ini telah direset.",
        discord.Color.green(),
        author=ctx.author
    )
    
    await ctx.reply(embed=embed)
    logger.info(f"🔄 History reset by {ctx.author} in {ctx.guild.name}")


@bot.command(name='model')
async def change_model(ctx, model_name: str = None):
    """Change AI model: !model [llama|compound|gemma|mixtral]"""
    global current_model
    
    if not model_name:
        embed = discord.Embed(
            title="🧠 Available Models",
            description="Pilih model AI yang ingin digunakan:",
            color=discord.Color.blue()
        )
        
        for name, model in MODELS.items():
            embed.add_field(
                name=f"**{name}**",
                value=f"`{model}`",
                inline=False
            )
        
        embed.add_field(
            name="📝 Usage",
            value="`!model [nama]`\nContoh: `!model llama`",
            inline=False
        )
        
        embed.set_footer(text=f"Current: {current_model}")
        await ctx.reply(embed=embed)
        return
    
    model_name = model_name.lower()
    if model_name not in MODELS:
        embed = create_embed(
            "❌ Invalid Model",
            f"Model tidak ditemukan. Gunakan: {', '.join(MODELS.keys())}",
            discord.Color.red(),
            author=ctx.author
        )
        await ctx.reply(embed=embed)
        return
    
    current_model = MODELS[model_name]
    embed = create_embed(
        "✅ Model Changed",
        f"Model berhasil diganti ke: **{current_model}**",
        discord.Color.green(),
        author=ctx.author
    )
    
    await ctx.reply(embed=embed)
    logger.info(f"🔄 Model changed to {current_model} by {ctx.author}")


@bot.event
async def on_command_error(ctx, error):
    """Global error handler"""
    if isinstance(error, commands.CommandNotFound):
        return
    
    if isinstance(error, commands.MissingPermissions):
        embed = create_embed(
            "🔒 Missing Permissions",
            "Anda tidak memiliki permission untuk command ini.",
            discord.Color.red(),
            author=ctx.author
        )
        await ctx.reply(embed=embed)
    
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = create_embed(
            "❓ Missing Argument",
            f"Command tidak lengkap. Gunakan `!help` untuk info lebih lanjut.",
            discord.Color.orange(),
            author=ctx.author
        )
        await ctx.reply(embed=embed)
    
    else:
        logger.error(f"❌ Unhandled error: {error}")
        embed = create_embed(
            "❌ Error",
            f"Terjadi kesalahan:\n```{str(error)[:200]}```",
            discord.Color.red(),
            author=ctx.author
        )
        await ctx.reply(embed=embed)


# Run bot
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    api = os.getenv("GROQ_API_KEY")
    
    if not token:
        logger.error("❌ DISCORD_TOKEN not found in .env file!")
        exit(1)
    
    if not api:
        logger.error("❌ GROQ_API_KEY not found in .env file!")
        exit(1)
    
    try:
        bot.run(token)
    except Exception as e:
        logger.error(f"❌ Failed to start bot: {e}")