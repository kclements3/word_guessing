# Input: initial guess, guess mode(final word known or unknown)
# Output: chain of words guessed until the right one is found
import regex

def regex_drop(word, word_regex):
    regex_str = ''.join(word_regex)
    match = regex.match(regex_str, word)
    if match is None:
        return False
    else:
        return True

def eliminate_by_letter_exclusion(word, letters):
    for excluded in letters:
        if excluded in word:
            return False
    return True

def eliminate_by_letter_inclusion(word, letters):
    for included in letters:
        if included not in word:
            return False
    return True

class WordGuess:
    def __init__(self, first_guess, final_word, word_data):
        self.guess = first_guess
        self.final = final_word
        self.feedback = ['k']*5
        self.word_regex = [r'\w']*5
        self.not_in_word = []
        self.in_word = []
        self.remaining_word_data = word_data

    def check_guess(self):
        for i in range(5):
            if self.guess[i] == self.final[i]:
                self.feedback[i] = 'g'
            elif self.guess[i] in self.final:
                self.feedback[i] = 'y'
            else:
                self.feedback[i] = 'k'

    def process_feedback(self):
        for f in range(len(self.feedback)):
            if self.feedback[f] == 'g':
                self.word_regex[f] = self.guess[f]
            elif self.feedback[f] == 'y':
                self.in_word.append(self.guess[f])
                prev_yellows = regex.match('\[\^(\w+)\]', self.word_regex[f])
                if prev_yellows is not None:
                    self.word_regex[f] = '[^{}]'.format(self.guess[f] + prev_yellows.groups()[0])
                else:
                    self.word_regex[f] = '[^{}]'.format(self.guess[f])
            elif self.feedback[f] == 'k':
                if self.guess[f] not in self.in_word:
                    self.not_in_word.append(self.guess[f])
        word_data_update = self.remaining_word_data

        # Drop current guess
        guess_drop_ind = self.remaining_word_data['word'].index[self.remaining_word_data['word'] == self.guess]
        self.remaining_word_data = self.remaining_word_data.drop(guess_drop_ind)
        if len(self.remaining_word_data) == 0:
            return

        # Eliminate by excluded letters
        eliminate_inds = self.remaining_word_data['word'].apply(lambda x: eliminate_by_letter_exclusion(x, self.not_in_word))
        self.remaining_word_data = self.remaining_word_data[eliminate_inds]
        if len(self.remaining_word_data) == 0:
            return

        # Eliminate by letters that must be in word
        eliminate_inds = self.remaining_word_data['word'].apply(lambda x: eliminate_by_letter_inclusion(x, self.in_word))
        self.remaining_word_data = self.remaining_word_data[eliminate_inds]
        if len(self.remaining_word_data) == 0:
            return

        # Apply regex
        regex_check = self.remaining_word_data['word'].apply(lambda x: regex_drop(x, self.word_regex))
        self.remaining_word_data = self.remaining_word_data[regex_check]
        if len(self.remaining_word_data) == 0:
            return


        # for row in self.remaining_word_data.iterrows():
        #     if row[1]['word'] == self.guess:
        #         word_data_update = word_data_update.drop(row[0])
        #         continue
        #     dropped = False
        #     # Remove word if it contains ruled out letters
        #     for excluded in self.not_in_word:
        #         if excluded in row[1]['word']:
        #             word_data_update = word_data_update.drop(row[0])
        #             dropped = True
        #             break
        #     if not dropped:
        #         # Remove word if it doesn't have yellow letters
        #         for included in self.in_word:
        #             if included not in row[1]['word']:
        #                 word_data_update = word_data_update.drop(row[0])
        #                 dropped = True
        #                 break
        #     if not dropped:
        #         # Check if word fits regex
        #         regex_str = ''.join(self.word_regex)
        #         match = regex.match(regex_str, row[1]['word'])
        #         if match is None:
        #             word_data_update = word_data_update.drop(row[0])
        #
        # self.remaining_word_data = word_data_update
        if self.feedback.count('k') < 4:
            if len(self.remaining_word_data) > 0:
                self.remaining_word_data = self.remaining_word_data.sort_values(by='count', ascending=False)

        # update guess to be first remaining word
        self.guess = self.remaining_word_data['word'].iloc[0]



# def check_guess(guess: str, final_word: str):
#     feedback = []
#     for i in range(5):
#         if guess[i] == final_word[i]:
#             feedback.append('g')
#         elif guess[i] in final_word:
#             feedback.append('y')
#         else:
#             feedback.append('b')
#
#     return feedback
#
# def process_feedback(feedback, guess):
#     # Take in feedback and eliminate words to produce new guess
#     guess_regex = [r'\w']*5
#     for f in range(len(feedback)):
#         if feedback[f] == 'g'
#             guess_regex[f] = guess[f]
#         elif
