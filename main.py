import pandas as pd
global in_word
global not_in_word
from guess_words import *
import cProfile


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def solve(initial_guess, final_word, print_steps):
    word_guess_obj = WordGuess(initial_guess, final_word, flw_data)
    guess_count = 1
    while word_guess_obj.guess != final_word:
        word_guess_obj.check_guess()
        if print_steps:
            print(word_guess_obj.feedback)
        word_guess_obj.process_feedback()
        if print_steps:
            print(word_guess_obj.guess)
        guess_count += 1
        if print_steps:
            print(len(word_guess_obj.remaining_word_data))
        if guess_count > 10:
            print("couldn't get it")
            break

    return guess_count

# Press the green button in the gutter to run the script.
def main():
    global flw_data
    flw_data = pd.read_csv('out_with_wordfreqs.csv')
    mode = 'test'  # can be 'test', 'live guess', or 'evaluate'

    if mode == 'test':
        initial_guess = input('What is your initial guess?')
        final_word = input('What should final word be?')
        guess_count = solve(initial_guess, final_word, True)
        print('Got it in {} guesses'.format(guess_count))
    elif mode == 'live guess':
        initial_guess = input('What is your guess?')
        final_word = ''
        word_guess_obj = WordGuess(initial_guess, final_word, flw_data)
        correct = 'n'
        while True:
            feedback = input('What was the feedback?')
            word_guess_obj.feedback = list(feedback)
            word_guess_obj.process_feedback()
            # print('Suggest guessing:', word_guess_obj.guess)
            print('Suggest Guessing:')
            for i in range(min(3, len(word_guess_obj.remaining_word_data))):
                print(word_guess_obj.remaining_word_data['word'].iloc[i])
            word_guess_obj.guess = input('What is your actual guess?')
            correct = input('Was it right?')
            if correct[0] == 'y':
                break
        print('Congrats!')


    elif mode == 'evaluate':
        f = open('wordle_past.csv', 'r')
        wordles = f.readlines()
        wordles = [wordle.rstrip('\n').lower() for wordle in wordles]
        wordles = [wordle.lstrip().lower() for wordle in wordles]
        wordles[0] = wordles[0].lstrip('\ufeff')
        f.close()

        f2 = open('initial_guesses.csv', 'r')
        guesses = f2.readlines()
        guesses = [guess.rstrip('\n') for guess in guesses]
        guesses[0] = guesses[0].lstrip('\ufeff')

        out_dict = {'wordles': wordles}
        for initial_guess in guesses:
            print(initial_guess)
            out_dict[initial_guess] = []
            for wordle in wordles:
                if wordle in list(flw_data['word']):
                    print(wordle)
                    guess_count = solve(initial_guess, wordle, False)
                else:
                    guess_count = 0
                    print(wordle, "Not in DB")
                print(guess_count)
                out_dict[initial_guess].append(guess_count)

        wordle_guesses_out = pd.DataFrame.from_dict(out_dict)
        wordle_guesses_out.to_csv('wordle_guess_counts_compare_keith.csv')

    # cProfile.run("main()")

if __name__ == '__main__':
    import cProfile, pstats
    from io import StringIO
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()

    profiler.dump_stats('output.prof')

    stream = open('output.txt', 'w')
    stats = pstats.Stats('output.prof', stream=stream)
    stats.sort_stats('cumtime')
    stats.print_stats()

    # profiler.dump_stats('program_stats.txt')
    # sortby = 'ncalls'
    # ps = pstats.Stats(profiler).sort_stats(sortby)
    #
    # ps.dump_stats('stats.dmp')
    # stats = pstats.Stats(profiler).sort_stats('ncalls')
    # stats.print_stats()
