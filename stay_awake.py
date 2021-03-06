from flask import Flask
from threading import Thread

app = Flask("")

@app.route('/')
def home():
  return '<a href="https://discord.com/api/oauth2/authorize?client_id=817805657738444800&permissions=523328&scope=bot" target="_blank">Invite this bot to your channel</a>'

def run():
  app.run(host='0.0.0.0', port=8080)

def stay_awake():
  t = Thread(target=run)
  t.start()