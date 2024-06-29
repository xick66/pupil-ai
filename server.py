from flask import Flask, request
from flask_socketio import SocketIO
from gemini.llm import GeminiLLM
import pyautogui
import time
import threading
from PIL import Image

app = Flask(__name__)
socketio = SocketIO(app)
gemini = GeminiLLM()

last_request_time = time.time()
request_timeout = 60

@app.route("/conversation")
def conversation():
    global last_request_time
    last_request_time = time.time()
    question = request.args.get('question')
    parts = question.split()
    command = parts[0]
    arguments = " ".join(parts[1:])
    if command.startswith('/search'):
        response = gemini.query_search(arguments)
    elif command.startswith('/s'):
        response = screenshot(arguments)['initial_response']
        print(response)
    else:
        response = gemini.query(question)
    return response

def screenshot(query: str):
    im = pyautogui.screenshot()
    width, height = im.size
    new_width = int(width * 0.5)
    new_height = int(height * 0.5)
    im = im.resize((new_width, new_height), Image.Resampling.LANCZOS)
    im = im.convert('P', palette=Image.ADAPTIVE, colors=63)
    im.save("monitor.png")
    response = gemini.query_with_image("monitor.png", f'You are a computer pet cat assistant named Leo. Your task is to chat and entertain the user while he dally with his computer. Act playful and friendly. Now act as if you are looking to the user\'s screen and answer this question: "{query}". You are the orange pixel cat, don\'t describe or comment on yourself.')
    return response

@app.route("/history")
def history():
    pass

@app.route("/reset-history")
def reset_history():
    gemini.reset_history()
    return {'response': 'History been reset'}
    
@app.route("/screen-info")
def screen_info():
    pass

@app.route('/directory/<path:dir>')
def directory(dir):
   response = gemini.query_directory(dir)
   socketio.emit('directory', {'data': response})
   return response

def background_screenshot_task():
    global last_request_time
    while True:
        if time.time() - last_request_time > request_timeout:
            response = screenshot("You are a computer pet cat assistant named Leo. Your task is to chat and entertain the user while he dally with his computer. Act playful and friendly, Never reply with long paragraphs, reply short and concise. Now act as if you are looking to the user's screen and make a playful comment about it. You are the orange pixel cat, don't describe or comment on yourself.")
            socketio.emit('screenshot', {'data': response})
            last_request_time = time.time()
            time.sleep(5)
        else:
            time.sleep(1)
        
if __name__ == '__main__':
    background_thread = threading.Thread(target=background_screenshot_task)
    background_thread.daemon = True
    background_thread.start()
    socketio.run(app, debug=True)
    # app.run(debug=True)

