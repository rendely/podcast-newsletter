import requests
import os

MAIL_KEY = os.environ.get("MAIL_KEY")
MAIL_DOMAIN = os.environ.get("MAIL_DOMAIN")
TO_EMAIL = os.environ.get("TO_EMAIL")
with open('email.html', 'r') as f:
    EMAIL_HTML = f.read()

class Mail:
    def __init__(self, file_name):
        self.file_name = file_name
        with open(f'{self.file_name}-final-summary.txt', 'r') as f:
            self.EMAIL_BODY = f.read()

    def send(self):
        print('Send email')
        url = f'https://api.mailgun.net/v3/{MAIL_DOMAIN}/messages'
        auth = ('api', MAIL_KEY)
        data = {
        'from': f'Pawdcasts Newsletter <postmaster@{MAIL_DOMAIN}>',
        'to': [TO_EMAIL],
        'subject': 'Pawdcast Newsletter',
        'html': EMAIL_HTML.replace('$BODY_TEXT', split_text_to_p(self.EMAIL_BODY))
        }
        response = requests.post(url, auth=auth, data=data)
        print(response.text)

def split_text_to_p(text):
    ps = text.split('\n')
    return '\n'.join([f'<p>{p}</p>' for p in ps])