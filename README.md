# Find My Medic - Location Monitor 🚑

Hey! This is my project for tracking medical staff locations and making sure they're staying safe in their work zones. It's pretty straightforward - just checks where everyone is and sends out alerts if someone wanders too far.

## Quick Setup 🚀

1. First, set up your virtual environment (trust me, you want this):
```bash
python -m venv venv
source venv/bin/activate  # for Mac/Linux
# or if you're on Windows:
# venv\Scripts\activate
```

2. Get all the packages you need:
```bash
pip install -r requirements.txt
```

3. Make a `.env` file for your settings:
```
ALERT_EMAIL=your-email@example.com
POLLING_INTERVAL=60  # seconds between checks
```

4. Run it!
```bash
python monitor.py
```

## What This Thing Does 🤔

- Keeps an eye on where medical staff are through the API
- Sends email alerts if anyone goes outside their work zone
- Doesn't crash when the API acts up (which happens more than you'd think)

## Important Stuff to Know 📝

- Checks staff locations every minute (configurable if you want it different)
- Sends alerts within 5 mins of someone leaving their zone
- If someone's right on the edge of their zone, we count them as outside (better safe than sorry!)

## Email Setup 📧

The email config is in `config.py` - just update it with your details if you need to change where alerts go.

## Notes 📌

Made this for my software engineering project. It's not fancy but it gets the job done! Let me know if you run into any issues or have questions.

PS: Remember to keep your API keys and email passwords safe! Don't commit them to git (learned that one the hard way... 😅) 