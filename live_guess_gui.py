from tkinter import *
from tkinter import ttk
from guess_words import *
import pandas as pd


def create_wordle_gui():
    root = Tk()

    frame = ttk.Frame(root)

def cycle_colors(event):
    cur_color = event.widget.cget('bg')
    if cur_color == 'gray':
        event.widget.config(background='yellow')
    elif cur_color == 'yellow':
        event.widget.config(background='green')
    elif cur_color == 'green':
        event.widget.config(background='gray')

def process_feedback():
    feedback_btn['state'] = DISABLED
    global cur_row

    feedback = []
    guess = []
    fb_dict = {'gray': 'k', 'yellow': 'y', 'green': 'g'}
    for col in range(5):
        fb = grid[cur_row][col].cget('bg')
        feedback.append(fb_dict[fb])
        letter = (grid[cur_row][col].get()).lower()
        guess.append(letter)
        if cur_row < 5:
            # grid[cur_row][col]['state'] = DISABLED
            grid[cur_row+1][col]['state'] = NORMAL

    word_guess_obj.guess = ''.join(guess)
    word_guess_obj.feedback = ''.join(feedback)
    # suggestions = word_guess_obj.remaining_word_data['word'].iloc[0:2]
    lb.delete(0, END)
    if word_guess_obj.feedback == 'ggggg':
        lb.insert(0, 'Congrats!')
    else:
        if len(word_guess_obj.remaining_word_data) > 0:
            if cur_row == 5:
                lb.insert(0, 'Sorry :(')
            else:
                word_guess_obj.process_feedback()
                for i in range(min(10, len(word_guess_obj.remaining_word_data))):
                    lb.insert(i, word_guess_obj.remaining_word_data['word'].iloc[i])
                cur_row += 1
                grid[cur_row][0].focus_set()
        else:
            lb.insert(0, 'No Remaining words... ')
            lb.insert(1, 'Either the word is obscure or something is wrong')

# def create_suggestions(frame):
#     suggestions = word_guess_obj.remaining_word_data['word'].iloc[0:3]
#     lb = Listbox(frame, width=10)
#     lb.grid(row=1, column=0, columnspan=2)
#     for s in range(3):
#         lb.insert(s, suggestions[s])

    # return lb
def use_selected_word():
    selected_word = lb.selection_get()
    # word_split = selected_word.split()
    for col in range(len(selected_word)):
        grid[cur_row][col].delete(0, END)
        grid[cur_row][col].insert(0, selected_word[col])
    feedback_btn['state'] = NORMAL



def create_suggestion_area(root):
    global feedback_btn
    frame = ttk.Frame(root)
    feedback_btn = Button(frame, text='>>>', command=process_feedback)
    feedback_btn['state'] = DISABLED
    feedback_btn.grid(row=0, column=0)

    Label(frame, text='Suggestions:').grid(row=0, column=1)
    use_suggestion_btn = Button(frame, text='<<<', command=use_selected_word)
    use_suggestion_btn.grid(row=1, column=0, sticky=N)
    # create_suggestions(frame)
    # suggestions = word_guess_obj.remaining_word_data['word'].iloc[0:3]
    global lb
    lb = Listbox(frame, width=10)
    lb.grid(row=1, column=1)
    for i in range(min(10, len(word_guess_obj.remaining_word_data))):
        lb.insert(i, word_guess_obj.remaining_word_data['word'].iloc[i])

    return frame

def press_tab(event):
    global feedback_btn

    if event.char.isalnum():
        row = event.widget.grid_info()['row']
        col = event.widget.grid_info()['column']

        new_col = col + 1
        if new_col == 5:
            new_col = 4
            # row = row + 1
        if row > 5:
            row = 5
        grid[row][new_col].focus_set()

        cur_entry = [grid[cur_row][col].get() for col in range(5)]
        if len(''.join(cur_entry)) == 4:
            feedback_btn['state'] = NORMAL
    elif event.keysym == 'BackSpace':
        press_delete(event)

def press_delete(event):
    row = event.widget.grid_info()['row']
    col = event.widget.grid_info()['column']

    new_col = col - 1
    if new_col < 0:
        new_col = 0
    grid[row][new_col].focus_set()

def create_entry_panel(root):
    frame = ttk.Frame(root)

    for row in range(6):
        grid.append([])
        for col in range(5):
            entry = Entry(frame, width=2, bg='gray', justify='center')
            entry.grid(column=col, row=row, sticky=W)

            grid[row].append(entry)
            grid[row][col].bind("<1>", cycle_colors)
            entry.bind("<Key>", press_tab)
            # entry.bind("<Delete>", press_delete)
            entry.configure(font=("Arial", 36, "bold"))
            entry['state'] = DISABLED
            if row == 0:
                entry['state'] = NORMAL
                if col == 0:
                    entry.focus_set()

    return frame


if __name__ == '__main__':
    grid = []

    cur_row = 0
    flw_data = pd.read_csv('out_with_wordfreqs.csv')
    word_guess_obj = WordGuess('', '', flw_data)


    root = Tk()
    entry_panel = create_entry_panel(root)
    entry_panel.grid(column=0, row=0, padx=5)
    suggestion_area = create_suggestion_area(root)
    suggestion_area.grid(column=1, row=0, sticky=N, padx=5)
    root.mainloop()



