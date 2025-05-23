# Find My Medic - Location Monitor 

Tracking medical staff locations and making sure they're staying safe in their work zones. 



1. set up your virtual environment :
```bash
python -m venv venv
source venv/bin/activate 

```

2. packages needed:
```bash
pip install -r requirements.txt
```

3.`.env` file for your settings:
```
ALERT_EMAIL=your-email@example.com
POLLING_INTERVAL=60  # seconds between checks
```

4. run
```bash
python monitor.py
```

## what it does

- Keeps an eye on where medical staff are through the API
- Sends email alerts if anyone goes outside their work zone
- Doesn't crash when the API acts up 

## what to know 

- Checks staff locations every minute 
- Sends alerts within 5 mins of someone leaving their zone
- If someone's right on the edge of their zone, they are counted as outside 

## Email Setup 

The email config is in `config.py` - just update it with your details if you need to change where alerts go.
