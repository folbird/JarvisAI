import openai
import pyttsx3
import os
from whisper_mic.cli import *
os.environ["http_proxy"] = "http://localhost:7890"
os.environ["https_proxy"] = "http://localhost:7890"
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold =  0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-US")
            print(f"sir said: {query}")
            return query
        except Exception as e:
            return ""
    # r = sr.recognizers
    # try:
    #     whisper_mic()
    # except Exception as e:
    #     print(e)
    #     return ""


def get_website_url_from_command():
    query = takeCommand()
    sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.org"],
             ["google", "https://www.google.com"], ]
    for site in sites:
        if f"Open {site[0]}".lower() in query.lower():
            url = site[1]
            name = site[0]
            return [name, url]
        return ["default", "https://www.google.com"]


chatStr = ""

def ai_improve(query):
    global chatStr
    chatStr += f"Clong: {query}\n Jarvis: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Find the most related to my prompt:{query} .Please select the appropriate response from the following options:\
        A) Hey Jarvis\
        B) Open music\
        C) The time\
        D) Using artificial intelligence\
        E) Send the message"+chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response["choices"][0]["text"]


def chat(query):
    global chatStr
    chatStr += f"Clong: {query}\n Jarvis: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def ai(prompt):
    text = ""

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    text = response["choices"][0]["text"]
    lines = text.splitlines()
    NoEmpty_text = [line for line in lines if line.strip()]
    new_text = '\n'.join(NoEmpty_text)
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
    # with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
    with open("Openai/1.txt", "w") as f:
        f.write(new_text)
    say(f"Sir,written done,please check out:{new_text}...Over")


def say(text):
    engine = pyttsx3.init()

    # engine.setProperty('rate',250)
    #
    voices = engine.getProperty('voices')

    # for voice in voices:
    #     engine.setProperty('voice',voice.id)
    #     engine.say("hello")
    # engine.setProperty('voice', voices[1].id)

    engine.say(text)

    engine.runAndWait()
if __name__ == '__main__':
    takeCommand()