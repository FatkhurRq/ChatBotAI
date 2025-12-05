# 📖 Discord AI Bot - Commands Reference

Complete reference untuk semua commands yang tersedia di bot.

---

## 🤖 AI Commands

### `!ask [pertanyaan]`
Tanya apapun ke AI dengan context conversation.

**Usage:**
```
!ask Apa itu Python?
!ask Jelaskan machine learning secara sederhana
!ask Bagaimana cara membuat Discord bot?
```

**Features:**
- ✅ Menyimpan context conversation (10 messages)
- ✅ Response dalam embed yang rapi
- ✅ Mendukung pertanyaan follow-up
- ✅ Rate limited (10 req/menit per user)

**Cooldown:** 3 detik
**Permission:** Everyone

---

### `@Bot [pertanyaan]`
Mention bot untuk chat secara natural.

**Usage:**
```
@MyBot Halo, apa kabar?
@MyBot Bantu jelaskan konsep OOP
@MyBot Apa perbedaan Python dan JavaScript?
```

**Features:**
- ✅ Natural conversation flow
- ✅ Auto-removes bot mention dari context
- ✅ Same AI capabilities as !ask
- ✅ Supports multi-line messages

**Cooldown:** 3 detik
**Permission:** Everyone

---

### `!model [nama]`
Ganti atau lihat AI model yang tersedia.

**Usage:**
```
!model                 # List semua model
!model compound        # Ganti ke compound (default)
!model llama          # Ganti ke Llama 3.2
!model gemma          # Ganti ke Gemma 2
!model mixtral        # Ganti ke Mixtral
```

**Available Models:**
- `compound` - Groq Compound (balanced, default)
- `llama` - Llama 3.2 1B (fast & efficient)
- `gemma` - Gemma2 9B (Google's model)
- `mixtral` - Mixtral 8x7B (large context window)

**Permission:** Everyone

---

## ⚙️ Utility Commands

### `!ping`
Cek latency bot ke Discord server.

**Usage:**
```
!ping
```

**Response:**
- 🟢 < 100ms: Sangat Baik
- 🟡 100-200ms: Baik  
- 🔴 > 200ms: Lambat

**Permission:** Everyone

---

### `!status`
Lihat informasi lengkap tentang bot.

**Usage:**
```
!status
```

**Information Shown:**
- Bot name & ID
- Current latency
- Server count
- Total users
- Active channels
- Current AI model
- API status

**Permission:** Everyone

---

### `!help`
Tampilkan help menu dengan semua commands.

**Usage:**
```
!help
```

**Shows:**
- AI commands
- Utility commands
- Admin commands
- Bot information
- Current settings

**Permission:** Everyone

---

## 🛡️ Admin Commands

### `!clear [jumlah]`
Bulk delete messages di channel.

**Usage:**
```
!clear           # Delete 5 messages (default)
!clear 10        # Delete 10 messages
!clear 20        # Delete 20 messages (max)
```

**Limits:**
- Min: 1 message
- Max: 20 messages
- Includes the command message itself

**Permission:** Manage Messages

---

### `!reset`
Reset conversation history untuk channel ini.

**Usage:**
```
!reset
```

**Effect:**
- Menghapus semua context conversation
- AI akan "lupa" percakapan sebelumnya
- Useful jika ingin mulai topic baru
- Per-channel (tidak affect channel lain)

**Permission:** Manage Messages

---

## 📊 Rate Limits

### Per-User Limits
- **Requests per minute:** 10 requests
- **Cooldown:** 3 seconds between requests
- **Applies to:** !ask dan @mention

### How It Works
```
User A: !ask Question 1  ✅
User A: !ask Question 2  ⏳ Wait 3 seconds
User A: !ask Question 3  ⏳ Wait 3 seconds
...
User A: !ask Question 11 ❌ Rate limited (10 req/min)
```

### Reset Time
Rate limit counter resets every 60 seconds.

---

## 🎨 Response Format

### Standard Embed Response
```
━━━━━━━━━━━━━━━━━━━━
💬 Balasan AI
━━━━━━━━━━━━━━━━━━━━

📝 Pertanyaan
[Your question here]

🤖 Jawaban  
[AI response here]

━━━━━━━━━━━━━━━━━━━━
Requested by @Username
Model: groq/compound
12:34 PM
```

### Error Response
```
━━━━━━━━━━━━━━━━━━━━
❌ Error
━━━━━━━━━━━━━━━━━━━━

[Error description]
[Suggestion to fix]

━━━━━━━━━━━━━━━━━━━━
Requested by @Username
12:34 PM
```

---

## 🔍 Command Examples

### Basic Q&A
```
User: !ask Apa itu Discord bot?
Bot: [Detailed explanation about Discord bots]

User: !ask Bagaimana cara membuatnya?
Bot: [Step-by-step guide with context from previous question]
```

### Mention Conversation
```
User: @MyBot Hai!
Bot: Halo! Ada yang bisa saya bantu?

User: @MyBot Jelaskan Python
Bot: [Python explanation]

User: @MyBot Bagaimana dengan JavaScript?
Bot: [JavaScript comparison, remembering Python context]
```

### Model Switching
```
User: !model
Bot: [Shows all available models]

User: !model llama
Bot: ✅ Model berhasil diganti ke: llama-3.2-1b-preview

User: !ask Test
Bot: [Response using Llama model]
```

### Admin Tasks
```
Admin: !clear 15
Bot: 🗑️ Berhasil menghapus 14 pesan
[Message auto-deletes after 5 seconds]

Admin: !reset
Bot: 🔄 Conversation history telah direset

User: !ask Remember our last conversation?
Bot: [Won't remember, context cleared]
```

---

## ⚠️ Error Messages

### Rate Limit
```
⏳ Rate Limit
Anda terlalu banyak request! Tunggu sebentar.
Max 10 requests per menit.
```

### Missing Permissions
```
🔒 Missing Permissions
Anda tidak memiliki permission untuk command ini.
```

### Invalid Arguments
```
❓ Format Salah
Usage: !ask [pertanyaan]
Contoh: !ask Apa itu Discord bot?
```

### API Error
```
❌ Error
Maaf, terjadi kesalahan:
[Error details]
```

---

## 💡 Pro Tips

### For Best Results:
1. **Be Specific:** Detail questions get better answers
2. **Use Context:** Bot remembers last 10 messages
3. **Reset When Needed:** Use !reset for new topics
4. **Try Different Models:** Each model has strengths
5. **Check Latency:** Use !ping if bot seems slow

### Example Good Questions:
```
✅ !ask Jelaskan perbedaan list dan tuple di Python dengan contoh
❌ !ask Apa itu list

✅ !ask Bagaimana cara deploy Discord bot ke Railway?
❌ !ask Deploy

✅ @MyBot Buatkan contoh async function di Python untuk fetch API
❌ @MyBot Code
```

---

## 🚫 Limitations

### What Bot CAN'T Do:
- ❌ Execute code
- ❌ Access external websites
- ❌ Remember conversations across channels
- ❌ DM users (only respond in channels)
- ❌ React to edits (only new messages)
- ❌ Process images or files

### What Bot CAN Do:
- ✅ Answer questions with AI
- ✅ Remember conversation context
- ✅ Code explanations & examples
- ✅ Switch AI models
- ✅ Multiple conversations simultaneously
- ✅ Work in multiple servers

---

## 📈 Usage Statistics

Track your usage with:
```
!status    # See bot statistics
```

Logs are saved in: `data/logs/bot.log`

---

## 🆘 Need Help?

If commands not working:

1. **Check bot permissions**
   - ✅ Read Messages
   - ✅ Send Messages
   - ✅ Embed Links

2. **Verify MESSAGE CONTENT INTENT**
   - Go to Discord Developer Portal
   - Bot → Privileged Gateway Intents
   - ✅ Enable "MESSAGE CONTENT INTENT"

3. **Check rate limits**
   - Wait 60 seconds
   - Try again

4. **Check logs**
   - See `data/logs/bot.log`
   - Look for error messages

5. **Test bot status**
   - `!ping` - Should respond
   - `!status` - Should show info
   - `!help` - Should show menu

---

**Last Updated:** December 2024  
**Bot Version:** 1.0  
**Powered by:** Groq API (Llama 3.2)