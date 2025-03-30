from youtube_transcript_api import YouTubeTranscriptApi
import urllib.parse as urlparse
from g4f.client import Client

client = Client()

ytt_api = YouTubeTranscriptApi()

y = lambda x: "0" + str(x) if len(str(x)) == 1 else str(x)
c = lambda x: y(int(x / 3600)) + ":" + y(int(x % 3600 / 60)) + ":" + y(int(x % 60))

def getVideoid(video_id):
    url_data = urlparse.urlparse(video_id)
    query = urlparse.parse_qs(url_data.query)
    video_id = query["v"][0] if (video_id.startswith("https:") or video_id.startswith("www.") or "youtube" in video_id) else video_id
    return video_id

def transcript(video_id, u=False):
    video_id = getVideoid(video_id)
    ts = ytt_api.fetch(video_id)

    txt = ''.join([i.text for i in ts])
    
    if u:
        txt = [{"text": i.text, "timestamp": c(i.start)} for i in ts]
    
    return txt


def summary(transcript):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "This is the transcript of a video. Your job is to provide a detailed summary of this such that the user doesn't have to watch the video to get a clear understanding of the video: " + transcript}],
        web_search=False
    )
    return response.choices[0].message.content