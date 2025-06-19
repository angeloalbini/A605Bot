# Bot Telegram 24/7 dengan Render.com

### 🔧 Cara Deploy:

1. Upload semua file ini ke GitHub
2. Login ke https://render.com
3. Pilih "New Web Service" → sambungkan repo GitHub ini
4. Isi setting Render:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
   - Environment Variable:  
     - `TOKEN` = isi dengan token dari BotFather
5. Setelah deploy, buka link: