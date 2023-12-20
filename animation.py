import asyncio
import curses
import os
import random
from itertools import cycle

import global_state
from curses_tools import draw_frame
from curses_tools import get_frame_size
from curses_tools import read_controls


STAR_SYMBOLS = ["+", "*", ".", ":"]

obstacles = list()
obstacles_in_last_collisions = list()


def animate_stars(max_stars_number):
    max_row, max_column = global_state.canvas_game.getmaxyx()
    for star in range(max_stars_number):
        star = blink(
            global_state.canvas_game,
            random.randint(2, max_row - 2),
            random.randint(2, max_column - 2),
            symbol=random.choice(STAR_SYMBOLS),
        )
        global_state.coroutines.append(star)


async def blink(canvas, row, column, symbol="*"):
    await sleep(random.randint(0, 20))
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(20)

        canvas.addstr(row, column, symbol)
        await sleep(6)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(10)

        canvas.addstr(row, column, symbol)
        await sleep(6)


async def sleep(ticks=1):
    for i in range(ticks):
        await asyncio.sleep(0)


# read_controls() -> draw_frame() -> sleep() -> draw_frame(negative=True) вот такая примерно должна схема получиться внутри функции с кораблем. Вы считываете управление - расcчитываете новые координаты корабля, перезаписываете переменные row и column и отрисовываете и по новой


def animate_spaceship(dir):
    frames = []
    folder_files = os.listdir(dir)
    for rocket_file in folder_files:
        with open(os.path.join(dir, rocket_file), "r") as file:
            frames.append(file.read())
    spaceship = animate_rocket(global_state.canvas_game, frames)
    global_state.coroutines.append(spaceship)


async def animate_rocket(canvas, frames):
    for frame in cycle(frames):
        row, column = get_frame_size(frame)
        height, width = canvas.getmaxyx()
        y = (height - row) // 2
        x = (width - column) // 2

        draw_frame(canvas, y, x, text=frame)
        await sleep(2)

        draw_frame(canvas, y, x, text=frame, negative=True)
