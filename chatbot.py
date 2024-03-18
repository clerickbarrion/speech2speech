from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
api_key = os.getenv("api_key")
prompt = os.getenv("prompt")

client = OpenAI(api_key=api_key)

def send_message(message, now):
    file = open("./history.txt", "r")
    history = file.readlines()
    file.close()
    file = open("personas/roxy.txt", "r")
    persona = file.read()
    file.close()

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": f'''
        {prompt}
        You are now the a fictional character with this personality:
        {persona}
        Here is the conversation so far:
        --
        {history}
        --
        '''},
        #
        {"role": "user", "content": message}
    ],
    temperature=1,)
    file = open("history.txt", "a")
    file.write(f"User: {message}\n")
    file.write(f"Roxy: {response.choices[0].message.content}\n")
    client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input=response.choices[0].message.content
    ).stream_to_file(f"{now}.mp3")

    return response.choices[0].message.content

if __name__ == "__main__":
    while True:
        message = input("You: ")
        print(send_message(message))