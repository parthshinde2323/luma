from flask import Flask, render_template, request, jsonify
from backend.autism import Autism
import os, glob

app = Flask(__name__)

# to create the object of the Autism class
autism_game = Autism()

@app.route("/")
def index_page():
    return render_template("index.html")

@app.route("/dyslexia")
def dyslexia_page():
    for f in glob.glob("static/*.mp3"):
        os.remove(f)
    return render_template("dyslexia.html")
    

@app.post("/dyslexia/audio")
def dyslexia_audio():
    data = request.json
    text = data["text"]

    # to generate audio file using the gTTS
    from gtts import gTTS
    import uuid
    filename = f"static/audio_{uuid.uuid4()}.mp3"

    tts = gTTS(text)
    tts.save(filename)

    return { "audio_url": "/" + filename }


@app.route("/get-question")
def get_question():
    data = autism_game.generate_question()
    print(data)
    return jsonify(data)


@app.route("/check-answer", methods=["POST"])
def check_answer():
    body = request.json
    user_answer = body.get("answer")
    correct = body.get("correct")

    result = autism_game.check_answer(user_answer, correct)
    print(result)

    return jsonify({"correct": result})


if __name__ == "__main__":
    app.run(debug=True)