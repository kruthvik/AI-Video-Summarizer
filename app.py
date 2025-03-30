from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from backend import transcript, summary, getVideoid

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    youtube_url = data.get('url')
    
    video_id = getVideoid(youtube_url)
    t = transcript(video_id, True)
    s = summary(transcript(video_id))
    
    return jsonify({
        'success': True,
        'summary': s,
        'transcript': t,
        'video_id': video_id
    })

if __name__ == '__main__':
    app.run()
