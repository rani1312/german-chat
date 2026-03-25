from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from deep_translator import GoogleTranslator

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    try:
        username = data.get('username', 'User')
        msg = data.get('message', '')

        msg = str(msg)

        translated = GoogleTranslator(
            source='auto',
            target='de'
        ).translate(msg)

    except Exception as e:
        print("Error:", e)
        translated = "Translation error"

    emit('message', {
        "username": username,
        "original": msg,
        "german": translated
    })

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001, use_reloader=False)