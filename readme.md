# Easy200Translate Bot

A simple Telegram bot that translates any text message into a target language.

## Features
- Translates any text sent to it (auto-detects source language)
- `/setlang <code>` to change target language per chat (e.g. `/setlang fr`)
- `/help` to see language code examples

## 1. Create the bot on Telegram
1. Open Telegram, search for **@BotFather**
2. Send `/newbot`
3. Choose a display name (anything, e.g. "Easy200 Translate")
4. Choose the username: `Easy200TranslateBot`
5. BotFather will give you a **token** — save it, you'll need it below

## 2. Push this project to GitHub
```bash
cd easy200translatebot
git init
git add .
git commit -m "Initial commit - translation bot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/easy200translatebot.git
git push -u origin main
```

## 3. Deploy on Railway
1. Go to https://railway.app and log in
2. Click **New Project** → **Deploy from GitHub repo**
3. Select your `easy200translatebot` repo
4. Once created, go to the project's **Variables** tab and add:
   - `BOT_TOKEN` = the token you got from BotFather
5. Railway will detect the `Procfile` and run `python bot.py` as a worker
6. Check the **Deployments** logs — you should see "Bot is starting..."

## 4. Test it
Open Telegram, search for your bot `@Easy200TranslateBot`, send `/start`, then send any text.

## Notes
- This uses `deep-translator`, which relies on the free/unofficial Google Translate web endpoint. It has no official uptime guarantee — if Google changes something, translations may break. For heavier/production use, consider a paid or officially licensed translation API (e.g. Google Cloud Translation API, DeepL API) and swap it into `translate_text()` in `bot.py`.
- Language preference is currently stored in memory, so it resets if the bot restarts. Let me know if you want it to persist (e.g. using a small database) and I can add that.
