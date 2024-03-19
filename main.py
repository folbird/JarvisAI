import datetime
import functions
from functions import *
from wechat.wechat import send_message


def handle_query(query):

    if "hey jarvis" in query.lower():
        say("Jarvis at service,sir")

    elif "jarvis are you still here" in query.lower():
        say("always at your service,Sir")

    # elif f"Open {result[0]}".lower() in query.lower():
    #     say(f"Opening {result[0]} sir...")
    #     webrowser.search_on_site(result[1])

    elif "open music" in query.lower():
        musicPath = "D:/Music/duanaojuan/monster_vocal.WAV"
        os.startfile(musicPath)

    elif "the time" in query.lower():
        hour = datetime.datetime.now().strftime("%H")
        min = datetime.datetime.now().strftime("%M")
        say(f"Sir, the time is {hour} o'clock and {min} minutes.")

    elif "open facetime" in query.lower():
        os.startfile("C:/Program Files/FaceTime/FaceTime.exe")

    elif "open pass" in query.lower():
        os.startfile("C:/Program Files/Passky/Passky.exe")

    elif "using artificial intelligence" in query.lower():
        ai(prompt=query)

    elif "jarvis quit" in query.lower():
        exit()

    elif "reset chat" in query.lower():
        functions.chatStr = ""

    elif "send message" in query.lower():
        send_message()

    else:
        print("Chatting...")
        chat(query)


if __name__ == '__main__':

    while True:
        print("Listening...")
        query = takeCommand()
        # final_query = ai_improve(query)
        # print(final_query)
        handle_query(query)
