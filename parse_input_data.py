import json


def replace_unicode(lines: list[str]) -> list[str]:
    replace_dict: dict = {
        "\u2019": "'",
        "\u2018": "'",
        # "\u00e9": "é",
        # "\u00eb": "ë",
        # "\u00ef": "ï",
        # "\u00e8": "è",
    }
    for idx in range(len(lines)):
        for _old, _new in replace_dict.items():
            lines[idx] = lines[idx].replace(_old, _new)

    # test for duplicates
    duplicates = 0
    for line in lines:
        if lines.count(line) != 1:
            duplicates += 1 / lines.count(line)
            # print(f"{lines.count(line)}: {line.strip()}")
    print(f"removing {int(duplicates)} duplicates from list")
    # removing the duplicates
    lines = list(dict.fromkeys(lines))

    return lines


def parse_words(course):
    # open the raw words to parse from (multi-)tab separated file
    with open("words.tsv") as f:
        words = replace_unicode(f.readlines())

    # parse the words adding vocabulary dictionaries to the parsed_words list
    parsed_words = []
    for index, word in enumerate(words):
        split_word = [entry.strip() for entry in word.strip().split("\t")]
        words = [word for word in split_word if word]
        assert len(words) == 2, f"additional tabs in {split_word}!"
        assert len(split_word) >= 2
        assert len(split_word[0].strip()) >= 1
        assert len(split_word[-1].strip()) >= 1
        parsed_word = {
            "id": f"{course}-{index+1}",  # 1-based index instead of 0-based
            "course": f"{course}",
            "dutch": split_word[0].strip(),
            "english": split_word[-1].strip(),
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
        interlaced_sentences = f.readlines()

    # parse the interlaced sentences (nl \n en \n nl \n en)
    nl_sentences = interlaced_sentences[0::2]
    en_sentences = interlaced_sentences[1::2]
    assert len(nl_sentences) == len(en_sentences)
    sentences = [
        f"{nl_sentences[i].strip()}\n{en_sentences[i].strip()}"
        for i in range(len(nl_sentences))
    ]
    sentences = replace_unicode(sentences)

    # adding to vocabulary dictionaries to the parsed_sentences list
    parsed_sentences = []
    for index, sentence in enumerate(sentences):
        nl_sentence, en_sentence = [s.strip() for s in sentence.split("\n")]
        assert len(nl_sentence) >= 0
        assert len(en_sentence) >= 0
        parsed_sentence = {
            "id": f"{course}-{index+1}",  # 1-based index instead of 0-based
            "course": f"{course}",
            "dutch": nl_sentence,
            "english": en_sentence,
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
