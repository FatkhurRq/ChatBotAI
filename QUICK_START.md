# ⚡ Quick Start - Copy & Paste Commands

## 🔥 Super Fast Setup (5 Menit)

### 1️⃣ Setup Project
```bash
# Buat folder project
mkdir discord-ai-bot
cd discord-ai-bot

# Buat virtual environment
python -m venv venv

# Aktivasi venv
# ========== WINDOWS ==========
venv\Scripts\activate

# ========== LINUX/MAC ==========
source venv/bin/activate
```

### 2️⃣ Install Dependencies (COPY INI)
```bash
# Setelah venv aktif, install semua dependencies
pip install discord.py>=2.3.0 openai>=1.0.0 python-dotenv>=1.0.0 requests>=2.31.0 aiohttp>=3.9.0

# Atau buat requirements.txt dulu, lalu:
pip install -r requirements.txt
```

### 3️⃣ Buat File .env
```bash
# Buat file .env
touch .env  # Linux/Mac
# Windows: buat manual dengan Notepad

# Isi dengan (ganti dengan token Anda):
echo "DISCORD_TOKEN=your_discord_token_here" >> .env
echo "GROQ_API_KEY=your_groq_api_key_here" >> .env
```

**Atau edit manual `.env` dengan isi:**
```env
DISCORD_TOKEN=MTIzNDU2Nzg5MDEyMzQ1Njc4OQ.GaBcDe.xxxxxx
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 4️⃣ Buat Folder Data
```bash
# Buat folder untuk logs dan cache
mkdir -p data/logs
mkdir -p data/cache

# Windows (jika mkdir -p tidak work):
mkdir data
mkdir data\logs
mkdir data\cache
```

### 5️⃣ Copy File Bot
- Copy isi `bot.py` dari artifact yang saya berikan
- Paste ke file `bot.py` di folder project Anda

### 6️⃣ Run Bot
```bash
# Pastikan venv masih aktif (ada tanda (venv) di terminal)
python bot.py
```

---

## 🎯 Cara Dapat Token & API Key

### Discord Bot Token

1. **Buka:** https://discord.com/developers/applications
2. **Klik:** "New Application" → Beri nama → Create
3. **Klik:** Tab "Bot" → "Add Bot"
4. **PENTING:** Scroll ke bawah → "Privileged Gateway Intents"
   - ✅ **MESSAGE CONTENT INTENT** (WAJIB!)
   - ✅ SERVER MEMBERS INTENT
   - ✅ PRESENCE INTENT
5. **Save Changes**
6. **Klik:** "Reset Token" → Copy token
7. **Paste** ke `.env` file

### Groq API Key

1. **Buka:** https://console.groq.com/
2. **Sign Up** dengan email atau Google
3. **Klik:** "API Keys" → "Create API Key"
4. **Copy** API key
5. **Paste** ke `.env` file

---

## 🔗 Invite Bot ke Server

1. **Buka Developer Portal:** https://discord.com/developers/applications
2. **Pilih** aplikasi bot Anda
3. **Klik:** Tab "OAuth2" → "URL Generator"
4. **Pilih Scopes:**
   - ✅ `bot`
   - ✅ `applications.commands`
5. **Pilih Permissions:**
   - ✅ Read Messages/View Channels
   - ✅ Send Messages
   - ✅ Manage Messages
   - ✅ Embed Links
   - ✅ Attach Files
   - ✅ Read Message History
   - ✅ Add Reactions
6. **Copy URL** di bagian bawah
7. **Paste** ke browser → Pilih server → Authorize

---

## ✅ Verifikasi Setup

### Test Commands di Discord:
```
!ping          # Harus dapat response latency
!help          # Harus muncul menu help
!ask Halo      # Harus dapat jawaban AI
@BotName Hai   # Mention harus respond
```

### Jika Error:

#### ❌ "MESSAGE CONTENT INTENT is required"
```
→ Buka Developer Portal
→ Tab "Bot" → Scroll ke "Privileged Gateway Intents"
→ ✅ Enable "MESSAGE CONTENT INTENT"
→ Save & restart bot
```

#### ❌ "ModuleNotFoundError: No module named 'discord'"
```bash
# Pastikan venv aktif!
pip install discord.py openai python-dotenv requests aiohttp
```

#### ❌ Bot online tapi tidak respond
```
→ Cek MESSAGE CONTENT INTENT sudah enabled
→ Pastikan bot punya permission "Read Messages"
→ Re-invite bot dengan URL permission yang benar
```

---

## 🚀 Run di Background (Linux/Mac)

```bash
# Install screen
sudo apt install screen  # Ubuntu/Debian
brew install screen      # Mac

# Jalankan bot di background
screen -S discord-bot
python bot.py
# Tekan: Ctrl+A lalu D (untuk detach)

# Untuk kembali ke bot:
screen -r discord-bot

# Untuk stop bot:
screen -r discord-bot
# Tekan: Ctrl+C
```

---

## 📦 Checklist Instalasi

- [ ] Python 3.8+ installed
- [ ] Virtual environment dibuat & aktif
- [ ] Dependencies installed (`pip list` untuk cek)
- [ ] File `.env` dibuat dengan token yang benar
- [ ] Folder `data/logs` dan `data/cache` dibuat
- [ ] File `bot.py` ada di root folder
- [ ] MESSAGE CONTENT INTENT enabled di Developer Portal
- [ ] Bot sudah di-invite ke server dengan permission yang benar
- [ ] Bot berhasil login (cek output terminal)
- [ ] Test command `!ping` berhasil

---

## 🎉 Done!

Jika semua checklist ✅, bot Anda sudah siap digunakan!

### Test dengan:
```
!ping
!help
!ask Apa itu Discord bot?
@BotName Jelaskan Python
!model
!status
```

---

## 💡 Tips

- **Venv selalu aktif** saat run bot (lihat `(venv)` di terminal)
- **Jangan share** `.env` file atau token ke siapapun
- **Check logs** di `data/logs/bot.log` jika ada error
- **Use `!reset`** jika bot bingung karena conversation history

---

## 🆘 Still Having Issues?

1. Cek `data/logs/bot.log` untuk error details
2. Verify semua environment variables di `.env`
3. Test API key di https://console.groq.com/playground
4. Verify Discord token masih valid
5. Baca SETUP.md untuk detailed troubleshooting

**Need help?** Check full documentation di SETUP.md dan README.md