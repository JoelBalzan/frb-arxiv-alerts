import feedparser
import smtplib
from email.mime.text import MIMEText
import os

RSS_FEEDS = [
    "https://rss.arxiv.org/rss/astro-ph.HE",
    "https://rss.arxiv.org/rss/astro-ph.IM",
]

KEYWORDS = [
    "frb",
    "fast radio burst",
    "pulsar",
    "scintillation",
    "dispersion measure",
    "askap",
    "chime",
    "meerkat",
]

matches = []

for url in RSS_FEEDS:
    feed = feedparser.parse(url)

    for entry in feed.entries:
        text = (entry.title + " " + entry.summary).lower()

        if any(k in text for k in KEYWORDS):
            matches.append(
                f"{entry.title}\n{entry.link}\n"
            )

if not matches:
    body = "No FRB-related papers today."
else:
    body = "\n\n".join(matches)

msg = MIMEText(body)
msg["Subject"] = "Daily FRB arXiv Papers"
msg["From"] = os.environ["SENDER"]
msg["To"] = os.environ["RECEIVER"]

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(
        os.environ["SENDER"],
        os.environ["SENDER_PASSWORD"],
    )

    server.sendmail(
        os.environ["SENDER"],
        os.environ["RECEIVER"],
        msg.as_string(),
    )

print("Email sent.")
