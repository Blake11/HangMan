import requests
import ast


SERVER = '85.204.241.122'
PORT = 8000
TOKEN = ""


def login(student_id, password):
    global TOKEN

    TOKEN = requests.post("http://" + SERVER + ":" + str(PORT) + "/login",
                          data={"student_id": student_id, "password": password}).text

    if TOKEN != "":
        print("Login successful!")


def new_game():
    response = requests.post("http://" + SERVER + ":" + str(PORT) + "/new_game", data={"token": TOKEN}).text

    print("Got a new game: ", response)
    return ast.literal_eval(response)


def check_letter(game_id, letter):
    response = requests.post("http://" + SERVER + ":" + str(PORT) + "/check_letter",
                             data={"token": TOKEN, "letter": letter, "game_id": game_id}).text

    print("Asked for letter positions of '" + letter + "' and got: ", response)
    return ast.literal_eval(response)


def check_word(game_id, word):
    if 'list' in str(type(word)):
        word = ''.join(word)

    response = requests.post("http://" + SERVER + ":" + str(PORT) + "/check_word",
                             data={"token": TOKEN, "word": word, "game_id": game_id}).text

    if response == "False":
        print("The word '" + word + "' was incorrect\n\n")
        return False
    else:
        print("The word '" + word + "' was correct\n\n")
        return True

