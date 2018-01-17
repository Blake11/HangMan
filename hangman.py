import codecs
import hangmanClient

# online params
id_student = "ciureapaul@gmail.com"
password = "CWUMHN"
online = False

# input/output files
input_file = codecs.open("cuvinte_de_verificat.txt", "r", "utf-8")  # input file
output_file = codecs.open("date_iesire_timestamp.txt", "w", "utf-8")  # results file

# data structures
all_words = codecs.open("dictionar.txt", "r", "utf-8").read().split("\r\n")  # array with all words from dictionary
chars = "aăâàåäbcçdeêéèfghiîjklmnñoöpqrsștţțuüùvwxyz"  # all chars from dictionary file


def patter_match(word1, word2):  # match the pattern of 1st word with 2nd word
    for i in range(0, len(word1)):
        if word1[i] != "*":  # where there is * there can be any character
            if word1[i] != word2[i]:  # if is not * then it must be same char as word2 in that same position
                return False
    return True  # returns true only if patter matches


def read_games():
    games = []
    global online

    if not online:
        for lines in input_file.readlines():
            game_line = []
            for game in lines.split(";"):
                game_line.append(game.replace("\r\n", ""))
            games.append(Game(game_line[0], game_line[1].lower(), game_line[2].lower()))
    else:
        while True:
            game = hangmanClient.new_game()
            game = {"id": game["game_id"], "cuvant": game["word_to_guess"]}
            if game["id"] == 100:
                break
            games.append(Game(game["id"], game["cuvant"]))

    # returns a list of game objects from the file
    return games


def most_probable_letter(trimmed_words, known_letters):

    picked_letter = ''
    possible_letters = most_used_letters(trimmed_words)  # make a map of most used letters from trimmed words
    max_occurances = 0

    for x in known_letters:  # from possible latters take out those who are already used
        if x != "":
            del possible_letters[x]

    for key, value in possible_letters.items():
        if possible_letters[key] > max_occurances:
            max_occurances = possible_letters[key]
            picked_letter = key

    return picked_letter  # return the letter with most occurances


def most_used_letters(word_array):  # returns a ordered list of most used letter in a array of words
    dic = {}  # dictionary of letters and no occurences

    for c in chars:  # init keys
        dic[c] = 0

    for word in word_array:
        for ch in word:
            if ch != '\ufeff':
                dic[ch] += 1

    return dic


class Game:
    game_id = 0
    word = ""
    correct_word = ""
    tries = 0
    solved = False

    def __init__(self, game_id, word, correct_word=""):
        self.game_id = game_id
        self.word = word
        self.correct_word = correct_word

    def add_letter(self, letter, letter_positions):  # adds one or more letter at givel positions
        new_word = list(self.word)  # strings cant be modified so a new string must be made
        for poz in letter_positions:
            new_word[poz] = letter
        self.word = "".join(new_word)

    def check_word(self, new_word):
        print(self.game_id)

        if not online:
            return self.correct_word == new_word
        else:
            return hangmanClient.check_word(self.game_id, new_word)

    def letter_positions(self, letter):
        self.tries += 1
        letter_positions = []

        if not online:
            for x in range(0, len(self.correct_word)):
                if self.correct_word[x] == letter:
                    letter_positions.append(x)
        else:
            letter_positions = hangmanClient.check_letter(self.game_id, letter)

        # return a array or positions
        return letter_positions

    def solve(self):
        trimmed_list = []
        used_letters = []
        word_length = len(self.word)  # word len

        used_letters = list(set([x for x in self.word if x not in used_letters and x != "*"]))
        # makes a list of knows letters excluding char "*"

        possible_words = [x for x in all_words if len(x) == word_length]
        # possible words which have same len as given word
        for letter in used_letters:
            possible_words = [x for x in possible_words if x.count(letter) == self.word.count(letter)]

        while len(trimmed_list) != 1:
            # while there are more than 1 result
            trimmed_list = [x for x in possible_words if patter_match(self.word, x)]
            # trim possible words with those that match pattern

            if len(trimmed_list) == 1:  # if one result is left then we found the word
                if self.check_word(trimmed_list[0]):
                    self.solved = True
                    break

            if len(trimmed_list) == 0:
                # if word is not in dictionary file then use algorithm  number 2
                self.solve2()
                break

            # else pick the most probable letter
            letter = most_probable_letter(trimmed_list, used_letters)
            if not letter:  # if no probable letter use brute force
                self.solve2()

            used_letters.append(letter)  # mark picked word as used
            letter_positions = self.letter_positions(letter)

            if len(letter_positions) != 0:  # if there are positions where selected letter can be added then add it
                self.add_letter(letter, letter_positions)

    def solve2(self):
        letter_array_index = 0  # index of letter array

        used_letters = []
        used_letters = list(set([x for x in self.word if x not in used_letters and x != "*"]))
        # get a list of already known letters

        letters = most_used_letters(all_words)  # make a map of most used letters
        letters = sorted(letters, key=letters.get, reverse=True)  # sort them by n. of appearances
        letters = [x for x in letters if x not in used_letters]  # delete letters already guessed

        while "*" in self.word:  # if there are * then there must be more letters to be guessed
            letter = letters[letter_array_index]  # get a letter
            letter_array_index += 1  # point to next letter
            letter_positions = self.letter_positions(letter)

            if len(letter_positions) != 0:  # if there are positions where selected letter can be added then add it
                self.add_letter(letter, letter_positions)

        if self.check_word(self.word):  # if word matches then its solved
            self.solved = True


def main():
    global online
    online = True
    if online:
        hangmanClient.login(id_student, password)

    games = read_games()
    total_tries = 0

    for game in games:
        game.solve()
        if game.solved:
            total_tries += game.tries

    print("Nr total de jocuri: " + str(len(games)) + " ... nr total de incercari: " + str(total_tries))

    for game in games:
        if game.solved:
            print(str(game.game_id) + " : " + str(game.tries) + " incercari")
            output_file.write(str(game.game_id) + ":" + str(game.tries))
            output_file.write("\r\n")
        else:
            print(str(game.id_joc + ": cuvantul este scris gresit sau nu exista in limba romana"))


if __name__ == '__main__':
    main()
