import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('wordle_guess_counts_compare_keith.csv')
fig, ax = plt.subplots()
ax.hist(df['irate'], bins=[2, 3, 4, 5, 6, 7], align='left', rwidth=0.7, orientation='horizontal', color='gray')
plt.title('Guess Distribution', fontweight='bold')
ax.set_ylim(7,1)
ax.set_yticks([6, 5, 4, 3, 2])
ax.set_xticks([])

for val in range(2,7):
    cnt = len(df[df['irate']==val])
    shift = 0.5
    if val == 3 or val == 4:
        shift = 1
    ax.text(cnt - shift, val+0.1, cnt, color='white')


plt.savefig('freq_count_plot.png')