import re
from spellchecker import SpellChecker


spell = SpellChecker()


def get_word_count(text: str):
    # Use regular expression to split text into words while preserving words with punctuation
    words = re.findall(r'\b\w+\b', text)
    
    # Return the total number of words
    return len(words)


def get_corrections(text):
    # words = re.split(r'[ ,]+(?!\w)|,\s{2}|  ', text)
    words = re.findall(r'\b\w+\b', text)

    misspelled = spell.unknown(words)

    correction_list = []

    for word in misspelled:
        # Get the one `most likely` answer
        if (spell.correction(word)) != word:
            correction_list.append((word, spell.correction(word)))

        # Get a list of `likely` options
        # print(spell.candidates(word))

    return correction_list


def get_candidates(word: str):
    return spell.candidates(word)


# # find those words that may be misspelled

# for word in misspelled:
#     # Get the one `most likely` answer
#     print(spell.correction(word))

# Get a list of `likely` options
#     print(spell.candidates(word))


# text = "This is a sample text. It (contans sample))    words, like hi,John."

# # Example usage:
# print(mistake_corrector(text))




# import re

# text = "This is a sample text. It (contains sample))    words, like hi,John."
# # text = "This is a sample text. It contains sample words, like hi,John. Here,  are some  spaces."

# words = re.findall(r'\b\w+\b', text)

# # Split the text into words using regular expressions

# print(words)