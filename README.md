# Zukun Academy RAG Chatbot

A starter project for answering student questions from Zukun Academy's information. Its knowledge base now includes public academy contact details and course information summarized from the academy website, together with course names supplied by the academy representative. Exact prices, durations, prerequisites, and current schedules still need confirmation from admissions.

## Project files

- `knowledge_base/academy_faq.md` - course names supplied so far and a list of academy details the chatbot still needs.
- `knowledge_base/courses.md` - course topics summarized from the public Zukun course pages, with notes where page titles differ from the supplied course list.
- `bot.py` - retrieval augmented generation chatbot with command-line and local browser modes. It combines Gemini embedding similarity with BM25 keyword matching using weighted reciprocal-rank fusion, then asks a Gemini model to answer from the retrieved passages.
- `web/index.html` - a local website-style preview with the floating chat launcher.
- `web/widget.html` - the compact chat panel shown in the pop-up.
- `web/assets/widget-embed.js` - creates the floating launcher and embeds the chat panel on a host website.
- `web/assets/zukun-logo.png` - the supplied academy logo.
- `web/assets/zukun-cover-full.png` - the full-bleed cover used by the UI, with the empty footer removed and the academy artwork extended to the bottom edge. The earlier clean version and original screenshot remain in the assets folder as backups.
- `.env.example` - required API key setting.
- `requirements.txt` - Gemini's Python SDK dependency.
- `Zukun_Academy_RAG_Guide.pdf` - RAG content plan, data checklist, and setup guide.

## Run on Windows

1. Install Python 3.10 or later.
2. In PowerShell, create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the Gemini SDK and copy the environment example:

   ```powershell
   python -m pip install -r requirements.txt
   if (!(Test-Path .env)) { Copy-Item .env.example .env }
   notepad .env
   ```

   Add your Gemini API key. The default response model is `gemini-3.6-flash`; change `GEMINI_MODEL` in `.env` if you want a different Gemini model supported by your API key.
4. Add current course pricing, durations, prerequisites, schedules, enrollment steps, and policies to the knowledge base when admissions confirms them. Check the noted title differences and the Data Analyst with AI syllabus with the academy.
5. Start the browser chat UI:

   ```powershell
   python bot.py --web
   ```

   It opens `http://127.0.0.1:8000` in your browser. Keep the terminal open while chatting; press `Ctrl+C` there to stop the server. If port 8000 is already in use, choose another port with `python bot.py --web --port 8001`.

   To use the original terminal chat instead, run `python bot.py`.

## Add the chat widget to Zukun's website

The local preview demonstrates the launcher, but it does not change the live Zukun website. First deploy this chatbot app to a public HTTPS host so the website can reach the widget and `/api/chat`. Then add this script near the end of the Zukun site page or through its site-wide custom-code area, replacing the host with the deployed chatbot address:

```html
<script src="https://YOUR-CHATBOT-HOST/assets/widget-embed.js" defer></script>
```

The script adds the small floating Zukun button. Clicking it opens the chat panel; the panel sends questions to the chatbot host. Do not use `localhost` in the live website embed because visitors' browsers would look for a server on their own devices.

The bot builds embeddings on the first run and stores them in `.rag_cache.json`. It detects changed knowledge-base text and refreshes the embeddings when you start it again. To force a rebuild manually:

```powershell
python bot.py --rebuild
```

Press `Ctrl+C` in the terminal to stop the local server. Keep `.env` private and do not commit API keys or student personal data.

## Preview on a phone

To preview the responsive layout on a phone connected to the same trusted Wi-Fi network, start the server so it listens on the local network:

```powershell
python bot.py --web --host 0.0.0.0
```

On the computer, run `ipconfig` and find the active Wi-Fi adapter's IPv4 address (often something like `192.168.1.25`). On the phone, open `http://<computer-ip>:8000`, replacing the example with that address. Keep the terminal open. If Windows Firewall asks, allow access only on a private network.

This preview has no sign-in. Anyone on the same reachable network can send questions through your Gemini API key, so use a trusted Wi-Fi network and stop the server with `Ctrl+C` when you finish. Do not port-forward it or expose it to the public internet.

## How to grow this into the academy bot

The browser interface is for local development. It binds to this computer by default; the optional phone preview listens on the local network. Before publishing it for students, deploy it on a secured web server, add authentication or rate limits as appropriate, and create an admin process for updating documents. For production, use a managed secrets store, clear privacy and retention rules, source versioning, and tests with real student questions. Use a human contact route for unknown, sensitive, or account-specific questions.

This starter sends knowledge-base text and student questions to the configured Gemini API. It sets `store=False` for answer requests so the Interactions API does not retain those Interaction resources. Review Google's current data and privacy terms and your academy's requirements before using real student data.
