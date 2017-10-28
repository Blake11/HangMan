import codecs

id_student = "Paul Ciurea"
input_file = codecs.open("cuvinte_de_verificat.txt", "r", "utf-8")  # input file
output_file = codecs.open("date_iesire_timestamp.txt", "w", "utf-8")
all_words = codecs.open("dictionar.txt", "r", "utf-8").read().split("\r\n")  # array with all words from language
chars = "aăâàäbcçdeêèfghiîjklmnñoöpqrsștțuüvwxyz"  # all chars from dictionary file


def patter_match(word1, word2):  # match the pattern of 1st word with 2nd word
    for i in range(0, len(word1)):
        if word1[i] != "*":  # where there is * there can be any character
            if word1[i] != word2[i]:  # if is not * then it must be same char as word2 in that same position
                return False
    return True  # returns true only if patter matches


def read_games():
    games = []
    for lines in input_file.readlines():
        lista = []
        for game in lines.split(";"):
            lista.append(game.replace("\r\n", ""))
        games.append(Joc(lista[0], lista[1].lower(), lista[2].lower()))
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
            dic[ch] += 1
    return dic


class Joc:
    id_joc = 0
    cuvant = ""
    cuvant_corect = ""
    tries = 0
    solved = False

    def __init__(self, id_joc, cuvant, cuvant_corect):
        self.id_joc = id_joc
        self.cuvant = cuvant
        self.cuvant_corect = cuvant_corect

    def add_letter(self, letter, pozitii_litere):  # adds one or more letter at givel positions
        new_word = list(self.cuvant)
        for poz in pozitii_litere:
            new_word[poz] = letter
        self.cuvant = "".join(new_word)

    def verifica_cuvantul(self, cuvant_compus):
        return self.cuvant_corect == cuvant_compus

    def unde_se_potriveste_litera(self, litera):
        self.tries += 1
        letter_positions = []
        for x in range(0, len(self.cuvant_corect)):
            if self.cuvant_corect[x] == litera:
                letter_positions.append(x)
        return letter_positions

    def solve(self):
        trimmed_list = []
        used_letters = []
        used_letters = list(set([x for x in self.cuvant
                                 if x not in used_letters and x != "*"]))
        # makes a list of knows lettes excluding char "*"
        lungime_cuvant = len(self.cuvant)  # word len
        possible_words = [x for x in all_words if
                          len(x) == lungime_cuvant]  # possible words which have same len as given word
        while len(trimmed_list) != 1:
            # while there are more than 1 result we need to cut those that doesn't match patter
            trimmed_list = [x for x in possible_words
                            if patter_match(self.cuvant, x)]  # trim possible words with those that match pattern
            if len(trimmed_list) == 1:  # if one result is left then we found the word
                self.cuvant = trimmed_list[0]
                break
            # else pick the most probable letter
            letter = most_probable_letter(trimmed_list, used_letters)
            used_letters.append(letter)  # mark picked word as used
            letter_positions = self.unde_se_potriveste_litera(letter)
            if len(letter_positions) != 0:  # if there are positions where selected letter can be added then add it
                self.add_letter(letter, letter_positions)

        if self.verifica_cuvantul(trimmed_list[0]):
            self.solved = True


def main():
    games = read_games()
    total_tries = 0
    for game in games:
        game.solve()
        if game.solved:
            total_tries += game.tries
    print("Nr total de jocuri " + str(len(games)))
    print("Nr total de incercari: " + str(total_tries))
    for game in games:
        if game.solved:
            print(str(game.id_joc) + " : " + str(game.tries) + " incercari")
            output_file.write(str(game.id_joc) + ":" + str(game.tries))
            output_file.write("\r\n")
        else:
            print(str(game.id_joc + ": cuvantul este scris gresit sau nu exista in limba romana"))


if __name__ == '__main__':
    main()

