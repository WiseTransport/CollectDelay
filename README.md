## How to use

### Prepare environment

Create python virtual environment:
```bash
python -m venv .venv
```

Then activate it.\
For Windows:
```bash
.venv\Scripts\activate
```
For Linux:
```bash
source .venv/bin/activate
```

### Install requirements
```bash
pip install -r requirements.txt
```

### Setup telegram logging (optional)
Set environment variables `TG_BOT_TOKEN` and `TG_CHAT_ID`.\
Get `TG_BOT_TOKEN` by [creating your bot](https://core.telegram.org/bots/tutorial) 
through Bot Father. Get your `TG_CHAT_ID` (so the bot knows to whom to send the logs)
using bot like `@username_to_id_bot`

### Run the script
```bash
python main.py
```

## Known issues

### Connect call failed
Sometimes crashes due to 
```
Cannot connect to host radar.bdz.bg:443 ssl:default [Connect call failed ('83.228.61.49', 443)]
```

### Substring not found (patched)
Often crashes due to
```
substring not found
```
