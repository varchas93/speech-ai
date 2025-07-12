import whisper
import openai
import os

# Load whisper model once
model = whisper.load_model("base")

# Set your OpenAI API key
openai.api_key = "your-openai-api-key"

def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result['text']

def generate_question(concept):
    prompt = f"Generate one short open-ended question to test understanding of the concept: {concept}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def evaluate_answer(user_answer, concept):
    prompt = f"""
    The user was asked a question about "{concept}" and gave the following answer: "{user_answer}".
    Provide a score from 1 to 10 and a short explanation of how well they answered.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
