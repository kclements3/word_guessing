# from english_words import english_words_lower_set
import pickle as pkl
import os
import pandas as pd
global letter_freq
import enchant
import PyDictionary
from nltk.corpus import words as nltk_words
letter_freq = pd.read_csv('common_letters.csv', header=None, index_col=0, squeeze=True).to_dict()

def rank_words(word_list: list):
    words_out = {'word': [], 'value': [], 'uniqueness': []}
    for word in word_list:
        score, uniqueness = get_score(word)
        words_out['word'].append(word)
        words_out['value'].append(score)
        words_out['uniqueness'].append(uniqueness)

    out_df = pd.DataFrame.from_dict(words_out)
    out_df = out_df.sort_values(by=['uniqueness', 'value'], ascending=False)

    # out_dict = {'word': list(words_out.keys()), 'value': list(words_out.values())}
    return out_df



def get_score(word: str) -> (float, int):
    word = word.upper()
    score = 0.0
    for letter in word:
        pct = letter_freq[letter]
        score += pct
    uniqueness = len(set(list(word)))
    return score, uniqueness

# def check_deleted_words(word_list):
#     out_list = []
#     dict_obj = PyDictionary.PyDictionary
#     count = 0
#     for word in word_list:
#         if dict_obj.meaning(word, disable_errors=True) is not None:
#             out_list.append(word)
#             print(word, 'is in dictionary')
#         count += 1
#         if 100 % count == 0:
#             print(count/len(word_list)*100)

def add_word_count(uni_f, flws):
    for flw in flws.iterrows():
        word = flw[1]['word']
        ind = uni_f.index[uni_f['word'] == word]
        if len(ind) > 0:
            flws.loc[flw[0], 'count'] = uni_f.loc[ind[0], 'count']
        else:
            flws.loc[flw[0], 'count'] = 0

    return flws


if __name__ == '__main__':
    if 'five_letter_words.pkl' not in os.listdir():
        f = open('words_alpha.txt', 'r')
        d = enchant.Dict('en_US')
        words = f.readlines()
        words = [word.rstrip('\n') for word in words]
        five_letter_words = [word.lower() for word in words if len(word) == 5]
        # five_letter_words = [word for word in five_letter_words if word in nltk_words.words()]
        five_letter_words_enchant = [word for word in five_letter_words if d.check(word)]
        five_letter_words_nltk = [word for word in nltk_words.words() if len(word) == 5 and word.islower()]
        five_letter_words_total = list(set(five_letter_words_enchant + five_letter_words_nltk))

        # rejected_words = [word for word in five_letter_words if not d.check(word)]
        # rejected_verify = check_deleted_words(rejected_words)
        pkl.dump(five_letter_words_total, open('five_letter_words.pkl', 'wb'))
    else:
        five_letter_words = pkl.load(open('five_letter_words.pkl', 'rb'))

    # word_scores = rank_words(five_letter_words)
    # word_scores.to_csv('out.csv', index=False)
    word_scores = pd.read_csv('out.csv', index_col=None)
    uni_f = pd.read_csv('unigram_freq.csv', index_col=None)
    flws_updated = add_word_count(uni_f, word_scores)
    word_scores = flws_updated.to_csv('out_with_wordfreqs.csv', index=False)
