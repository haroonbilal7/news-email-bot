import requests 
import smtplib, ssl
from email.mime.text import MIMEText

api_key = "9db54cbc35c5447dbe1ed79f97798c7f"
url = "https://newsapi.org/v2/everything?q=tesla&from=2025-08-28&sortBy=publishedAt&apiKey=9db54cbc35c5447dbe1ed79f97798c7f"

#getting request from the url
r = requests.get(url)

#converting into dict/list format using json
content = r.json()

def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "hb80128@gmail.com"
    password = "bsvy alwj wvsk memm"

    receiver = "haroonbilal128@gmail.com"
    context = ssl.create_default_context()
    
    # Create proper email message to handle special characters
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] = username
    msg['To'] = receiver
    msg['Subject'] = "Tesla News"
    
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, msg.as_string())  # Use msg.as_string() not message

# Fixed: Move this outside the function and fix syntax errors
for article in content['articles']:
    print(article['title'])
    print(article['description'])
    
    # Fixed: Add missing + sign and use consistent quotes
    message = article['title'] + "\n" + article['description']
    send_email(message)