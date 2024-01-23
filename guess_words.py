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
        self.guess = first_guess # This will update as more guesses are used
        self.final = final_word # Not relevant for the GUI, just for testing lots of words
        self.feedback = ['k']*5 # initial feedback is all gray (black)
        self.word_regex = [r'\w']*5 # initial regex pattern is just "any word characters"
        self.not_in_word = [] # List of letters not in word
        self.in_word = [] # List of letters in the word
        self.remaining_word_data = word_data # giant pandas dataframe of all remaining words and scores

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
        # word_data_update = self.remaining_word_data

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

        # Change sorting method if more than 2 letters have been ID'd in word
        if self.feedback.count('k') < 4:
            if len(self.remaining_word_data) > 0:
                self.remaining_word_data = self.remaining_word_data.sort_values(by='count', ascending=False)

        # update guess to be first remaining word
        self.guess = self.remaining_word_data['word'].iloc[0]
