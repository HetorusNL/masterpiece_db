import json


def parse_words(course):
    # open the raw words to parse from (multi-)tab separated file
    with open("words.tsv") as f:
        words = f.readlines()

    # parse the words adding vocabulary dictionaries to the parsed_words list
    parsed_words = []
    for index, word in enumerate(words):
        split_word = word.strip().split("\t")
        assert len(split_word) >= 2
        assert len(split_word[0].strip()) >= 1
        assert len(split_word[-1].strip()) >= 1
        parsed_word = {
            "id": f"{course}-{index+1}",  # 1-based index instead of 0-based
            "course": f"{course}",
            "dutch": split_word[0],
            "english": split_word[-1],
        }
        parsed_words.append(parsed_word)

    # read the 'old' dictionary
    with open("dictionary.json") as f:
        dictionary = json.load(f)

    # REPLACE the vocabulary list with the parsed words
    dictionary["vocabulary"] = parsed_words

    # write the dictionary back to file
    with open("dictionary.json", "w") as f:
        json.dump(dictionary, f, indent=2)


def parse_sentences(course):
    # open the raw sentences to parse from interlaced file
    with open("sentences.intl") as f:
        sentences = f.readlines()

    # parse the interlaced sentences (nl \n en \n nl \n en)
    # adding to vocabulary dictionaries to the parsed_sentences list
    nl_sentences = sentences[0::2]
    en_sentences = sentences[1::2]
    assert len(nl_sentences) == len(en_sentences)
    parsed_sentences = []
    for index in range(len(nl_sentences)):
        parsed_sentence = {
            "id": f"{course}-{index+1}",  # 1-based index instead of 0-based
            "course": f"{course}",
            "dutch": nl_sentences[index].strip(),
            "english": en_sentences[index].strip(),
        }
        parsed_sentences.append(parsed_sentence)

    # read the words dictionary
    with open("dictionary.json") as f:
        dictionary = json.load(f)

    # APPEND the sentences to the vocabulary list
    dictionary["vocabulary"] = [*dictionary["vocabulary"], *parsed_sentences]

    # write the dictionary back to file
    with open("dictionary.json", "w") as f:
        json.dump(dictionary, f, indent=2)


if __name__ == "__main__":
    parse_words("words")
    parse_sentences("sentences")
