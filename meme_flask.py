from flask import Flask, render_template
import requests
import json
import threading
import time

global memes_list,n, init_s
n = 0
memes_list = []
init_s = 0

app = Flask(__name__)

def download_memes(num_memes):
    try:
        memes = []
        for _ in range(num_memes):
            url = "https://meme-api.com/gimme"
            response = json.loads(requests.get(url).text)
            meme_large = response["preview"][-2]
            subreddit = response["subreddit"]
            memes.append((meme_large, subreddit))
        return memes
    except:
        print("skip")

def update_memes_list():
    try:
        global memes_list,n, init_s
        memes_list = download_memes(20)
        print("Done")
        if init_s == 0:
            n = 1
        else:
            n = 2
        init_s = 1
    except:
        print("skip")
def get_memes():
    try:
        while True:
            update_memes_list()
			# Sleep for some time before updating again
			#time.sleep(60)
    except:
        print("skip")

@app.route("/")
def index():
    global init_s
    return render_template("meme_index.html", memes_list=memes_list, n = n, loading = "activity_indicator.gif")
if __name__ == "__main__":
    # Start the thread for updating memes_list
    thread = threading.Thread(target=get_memes)
    thread.start()

    # Run the Flask app
    app.run(host="0.0.0.0", port=90)
