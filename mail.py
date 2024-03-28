import requests
import os

MAIL_KEY = os.environ.get("MAIL_KEY")
MAIL_DOMAIN = os.environ.get("MAIL_DOMAIN")
TO_EMAIL = os.environ.get("TO_EMAIL")

with open('email.html', 'r') as f:
    EMAIL_HTML = f.read()

with open('a49a507f9dd765f4e7d5b6b9f928ff433e069a648b75f1cbb0658304089d727b-final-summary.txt', 'r') as f:
   EMAIL_BODY = f.read()

def split_text_to_p(text):
    ps = text.split('\n')
    return '\n'.join([f'<p>{p}</p>' for p in ps])

url = f'https://api.mailgun.net/v3/{MAIL_DOMAIN}/messages'
auth = ('api', MAIL_KEY)
data = {
'from': f'Pawdcasts Newsletter <postmaster@{MAIL_DOMAIN}>',
'to': [TO_EMAIL],
'subject': 'Pawdcast Newsletter: Ezra Klein and Paul Krugman',
'html': EMAIL_HTML.replace('$BODY_TEXT', split_text_to_p(EMAIL_BODY))
}
response = requests.post(url, auth=auth, data=data)
print(response.text)
