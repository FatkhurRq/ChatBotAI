# 🤖 Discord AI Chatbot - Setup Guide

## 📋 Prerequisites

- Python 3.8 atau lebih baru
- Discord Account
- Groq API Account

---

## 🚀 Langkah-Langkah Instalasi

### 1️⃣ **Clone atau Download Project**

```bash
# Jika dari Git
git clone <repository-url>
cd discord-ai-bot

# Atau buat folder manual
mkdir discord-ai-bot
cd discord-ai-bot
```

### 2️⃣ **Buat Virtual Environment**

```bash
# Buat venv
python -m venv venv

# Aktifkan venv
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### 3️⃣ **Install Dependencies**

```bash
# Setelah venv aktif (lihat tanda (venv) di terminal)
pip install -r requirements.txt

# Atau install satu-satu:
pip install discord.py>=2.3.0
pip install openai>=1.0.0
pip install python-dotenv>=1.0.0
pip install requests>=2.31.0
pip install aiohttp>=3.9.0
```

### 4️⃣ **Setup Discord Bot**

1. **Buka Discord Developer Portal**
   - Kunjungi: https://discord.com/developers/applications
   - Login dengan akun Discord Anda

2. **Buat New Application**
   - Klik "New Application"
   - Beri nama bot Anda (contoh: "AI Assistant")
   - Klik "Create"

3. **Setup Bot**
   - Klik tab "Bot" di sidebar kiri
   - Klik "Add Bot" → "Yes, do it!"
   - **IMPORTANT:** Di bagian "Privileged Gateway Intents":
     - ✅ Enable **MESSAGE CONTENT INTENT** (WAJIB!)
     - ✅ Enable **SERVER MEMBERS INTENT** (Opsional)
     - ✅ Enable **PRESENCE INTENT** (Opsional)
   - Klik "Save Changes"

4. **Copy Bot Token**
   - Di bagian "TOKEN", klik "Reset Token"
   - Copy token yang muncul (hanya tampil sekali!)
   - **JANGAN SHARE TOKEN INI KE SIAPAPUN!**

5. **Setup Bot Permissions**
   - Klik tab "OAuth2" → "URL Generator"
   - **Scopes:** Pilih `bot` dan `applications.commands`
   - **Bot Permissions:** Pilih:
     - ✅ Read Messages/View Channels
     - ✅ Send Messages
     - ✅ Manage Messages
     - ✅ Embed Links
     - ✅ Attach Files
     - ✅ Read Message History
     - ✅ Add Reactions
     - ✅ Use External Emojis
   - Copy URL yang dihasilkan di bagian bawah

6. **Invite Bot ke Server**
   - Paste URL ke browser
   - Pilih server Discord Anda
   - Klik "Authorize"
   - Selesaikan CAPTCHA

### 5️⃣ **Setup Groq API**

1. **Daftar Groq Account**
   - Kunjungi: https://console.groq.com/
   - Sign up dengan email atau Google

2. **Generate API Key**
   - Setelah login, klik "API Keys"
   - Klik "Create API Key"
   - Beri nama (contoh: "Discord Bot")
   - Copy API Key yang dihasilkan

### 6️⃣ **Setup Environment Variables**

1. **Buat file `.env`** di root project:

```bash
# Copy dari template
cp .env.example .env

# Atau buat manual
touch .env
```

2. **Isi file `.env`**:

```env
```

**⚠️ PENTING:** Ganti dengan token & API key Anda sendiri!

### 7️⃣ **Buat Struktur Folder**

```bash
mkdir -p data/logs data/cache
```

Struktur final:
```
discord-ai-bot/
├── bot.py
├── .env
├── .env.example
├── requirements.txt
├── SETUP.md
├── venv/
└── data/
    ├── logs/
    └── cache/
```

### 8️⃣ **Test Run Bot**

```bash
# Pastikan venv masih aktif
python bot.py
```

Output yang diharapkan:
```
✅ Bot logged in as YourBotName (ID: 123456789)
📊 Connected to 1 servers

==================================================
🤖 YourBotName is ONLINE!
📝 Prefix: !
🔗 Invite URL: https://discord.com/api/oauth2/...
==================================================
```

---

## 🧪 Testing Bot

1. **Buka Discord** dan masuk ke server tempat bot diinvite

2. **Test Commands:**

```
!ping                    # Cek latency
!help                    # Lihat semua commands
!ask Apa itu Python?     # Tanya AI
@BotName Halo!          # Mention bot
!status                  # Lihat status bot
```

---

## 🛠️ Troubleshooting

### ❌ Error: "MESSAGE CONTENT INTENT is required"

**Solusi:**
1. Buka Discord Developer Portal
2. Pilih aplikasi bot Anda
3. Tab "Bot" → Privileged Gateway Intents
4. ✅ Enable "MESSAGE CONTENT INTENT"
5. Save & restart bot

### ❌ Error: "Improper token has been passed"

**Solusi:**
1. Cek file `.env` → pastikan `DISCORD_TOKEN` benar
2. Reset token di Developer Portal
3. Update `.env` dengan token baru

### ❌ Error: "ModuleNotFoundError: No module named 'discord'"

**Solusi:**
```bash
# Pastikan venv aktif (ada tanda (venv) di terminal)
# Jika belum:
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### ❌ Bot online tapi tidak respond

**Solusi:**
1. Cek MESSAGE CONTENT INTENT sudah enabled
2. Pastikan bot punya permission "Read Messages"
3. Coba kick & re-invite bot dengan URL permission yang benar

### ❌ Error: "Rate limit exceeded" di Groq

**Solusi:**
1. Cek quota API di console.groq.com
2. Tunggu beberapa menit (free tier punya limit)
3. Upgrade plan jika perlu

---

## 📊 Monitoring

### Log Files

Bot secara otomatis membuat log di:
```
data/logs/bot.log
```

Untuk melihat log real-time:
```bash
tail -f data/logs/bot.log
```

### Metrics yang Dicatat

- ✅ Command usage
- ✅ Error messages
- ✅ API calls
- ✅ Rate limit hits

---

## 🚀 Deploy 24/7 (Optional)

### Option 1: Railway.app

1. Daftar di railway.app
2. Connect GitHub repo
3. Add environment variables
4. Deploy!

### Option 2: Replit

1. Buka replit.com
2. Import dari GitHub
3. Set Secrets (DISCORD_TOKEN, GROQ_API_KEY)
4. Jalankan dengan "Always On"

### Option 3: VPS/Server

```bash
# Install screen untuk background process
sudo apt install screen

# Buat session baru
screen -S discord-bot

# Jalankan bot
python bot.py

# Detach: Ctrl+A lalu D
# Reattach: screen -r discord-bot
```

---

## 📚 Resources

- **Discord.py Docs:** https://discordpy.readthedocs.io/
- **Groq API Docs:** https://console.groq.com/docs
- **Bot Invite URL Generator:** https://discordapi.com/permissions.html

---

## 🆘 Need Help?

Jika masih ada masalah:
1. Cek logs di `data/logs/bot.log`
2. Pastikan semua environment variables benar
3. Verify Discord bot permissions
4. Check Groq API quota

---

## 🎉 Bot Ready!

Selamat! Bot Anda sekarang sudah siap digunakan. Enjoy! 🚀