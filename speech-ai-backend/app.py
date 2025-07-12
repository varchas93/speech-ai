from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from ai_utils import generate_question, transcribe_audio, evaluate_answer

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/generate-question", methods=["POST"])
def question_api():
    data = request.get_json()
    topic = data.get("topic")
    if not topic:
        return jsonify({"error": "Topic required"}), 400
    question = generate_question(topic)
    return jsonify({"question": question})

@app.route("/evaluate", methods=["POST"])
def evaluate_api():
    audio = request.files.get("audio")
    concept = request.form.get("concept")

    if not audio or not concept:
        return jsonify({"error": "Audio file and concept are required"}), 400

    filename = secure_filename(audio.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    audio.save(file_path)

    transcription = transcribe_audio(file_path)
    evaluation = evaluate_answer(transcription, concept)

    os.remove(file_path)  # Clean up
    return jsonify({
        "transcription": transcription,
        "evaluation": evaluation
    })

if __name__ == "__main__":
    app.run(debug=True)
