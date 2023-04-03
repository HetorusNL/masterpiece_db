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
            duplicates += 1
            # print(f"{lines.count(line)}: {line.strip()}")
    print(f"found {duplicates} duplicates")

    return lines


def parse_words(course):
    # open the raw words to parse from (multi-)tab separated file
    with open("words.tsv") as f:
        words = replace_unicode(f.readlines())

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
        sentences = replace_unicode(f.readlines())

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
