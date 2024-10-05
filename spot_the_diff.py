import matplotlib.pyplot as plt
from matplotlib.colors import CSS4_COLORS, XKCD_COLORS
from matplotlib.patches import Circle
from random import random, choice
from math import sqrt


def draw_game(n_circ, r_min, r_max, chance, difficulty):

    def is_inside(x, y, r):
        for circle in drawn:
            d = sqrt((x-circle[0])**2+(y-circle[1])**2)
            if d < r+circle[2]:
                return True
        return False

    def is_outside(x, y, r):
        if x + r > 1 or x - r < 0:
            return True
        if y + r > 1 or y - r < 0:
            return True
        return False

    if difficulty == '5':
        COLORS = list(XKCD_COLORS)
    else:
        COLORS = list(CSS4_COLORS)

    fig, axes = plt.subplots(1, 2, figsize=(10, 10), tight_layout=True)
    for ax in axes:
        ax.set(xlim=[0, 1], ylim=[0, 1],
               xticks=[], yticks=[], aspect='equal')
    drawn = []
    while len(drawn) < n_circ:
        r = (r_max-r_min)*random()+r_min
        x, y = (1-2*r)*random()+r, (1-2*r)*random()+r
        nudge = r
        while is_inside(x, y, r):
            x = x - nudge if x < 0.5 else x + nudge
            y = y - nudge if y < 0.5 else y + nudge
        if is_outside(x, y, r):
            continue
        c = choice(COLORS)
        to_change = True if random() <= chance else False
        this = [x, y, r, to_change, None]
        drawn.append(this)
        circle = Circle((x, y), r, fill=True, facecolor=c, edgecolor='k')
        axes[0].add_artist(circle)
        if to_change:
            c2 = choice(COLORS)
            while c2 == c:
                c2 = choice(COLORS)
            circle = Circle((x, y), r, fill=True, facecolor=c2, edgecolor='k')
            axes[1].add_artist(circle)
        else:
            circle = Circle((x, y), r, fill=True, facecolor=c, edgecolor='k')
            axes[1].add_artist(circle)

    diff = [circle for circle in drawn if circle[3]]
    not_diff = [circle for circle in drawn if not circle[3]]
    axes[0].set(title=f"{len(drawn)} circles.")
    if difficulty in ['1', '2', '3']:
        axes[1].set(title=f"{len(diff)} differences.")
    input = plt.ginput(n=-1, timeout=-1, show_clicks=True)
    return drawn, diff, not_diff, input, fig, axes


if __name__ == "__main__":

    welcome_message = f"{'#'*23}\n# Spot the difference #\n{'#'*23}\n"\
            f"Type 'exit' to quit. Type 'help' for help.\n"\
            f"Select the difficulty level:\n{'-'*28}\n"\
            f"Childish:\t1\nBeginner:\t2\nIntermediate:\t3\nHard:\t\t4\nExtreme:\t5"

    help_message = f"{'-'*45}\n"\
            "Click on the different circles using mouse 1.\n"\
            "Use mouse 2 or backspace to remove last click.\n"\
            "When you have clicked all differences, press middle mouse.\n"\
            f"{'-'*45}\n"

    settings = {'1': [10, 0.03, 0.2, 0.5, '1'],
                '2': [25, 0.03, 0.2, 0.4, '2'],
                '3': [50, 0.01, 0.2, 0.3, '3'],
                '4': [100, 0.01, 0.2, 0.3, '4'],
                '5': [200, 0.01, 0.2, 0.2, '5']}

    n_circ = 100
    r_min = 0.01
    r_max = 0.2
    chance = 0.3

    while True:
        difficulty = input(welcome_message+"\n\n>> ")
        if difficulty.lower() == 'exit':
            exit(0)
        elif difficulty.lower() == 'help':
            print(help_message)
        while difficulty not in ['1', '2', '3', '4', '5']:
            difficulty = input(welcome_message +
                               "\nPlease select one of the difficulties!\n\n>> ")
            if difficulty.lower() == 'exit':
                exit(0)
            elif difficulty.lower() == 'help':
                print(help_message)

        drawn, diff, not_diff, clicks, fig, axes = draw_game(*settings[difficulty])

        found = 0
        for circ in diff:
            for click in clicks:
                d = sqrt((click[0]-circ[0])**2+(click[1]-circ[1])**2)
                if d <= circ[2]:
                    circ[4] = True
                    c = 'g'
                    found += 1
                    break
                circ[4] = False
                c = 'r'
            axes[1].scatter(circ[0], circ[1], marker='o', s=100, c=c, edgecolor='k')

        axes[0].set(title="Game finished!")
        axes[1].set(title=f"You found {found}/{len(diff)} differences.")
        plt.show()
