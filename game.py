import curses
import time

import global_state
from animation import animate_spaceship
from animation import animate_stars


TIC_TIMEOUT = 0.1
MAX_STARS = 100
CANVAS_TEXT_ROWS = 3
STAR_SYMBOLS = ["+", "*", ".", ":"]


def draw(canvas):
    dir = "rocket"
    max_row, max_column = canvas.getmaxyx()
    global_state.canvas_text = canvas.derwin(
        CANVAS_TEXT_ROWS, max_column, max_row - CANVAS_TEXT_ROWS, 0
    )
    global_state.canvas_text.border()
    global_state.canvas_text.nodelay(True)

    global_state.canvas_game = canvas.derwin(
        max_row - CANVAS_TEXT_ROWS, max_column, 0, 0
    )

    global_state.canvas_game.nodelay(True)
    global_state.canvas_game.keypad(True)
    global_state.canvas_game.border()
    curses.curs_set(False)

    animate_stars(MAX_STARS)
    animate_spaceship(dir)

    while True:
        for coroutine in global_state.coroutines:
            try:
                coroutine.send(None)
                global_state.canvas_game.refresh()
                global_state.canvas_text.refresh()
            except StopIteration:
                global_state.coroutines.remove(coroutine)

        time.sleep(TIC_TIMEOUT)


def main():
    curses.update_lines_cols()
    curses.wrapper(draw)


if __name__ == "__main__":
    main()
