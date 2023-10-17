import pandas as pd
import sys
import random
import pygame
import os
from beautifultable import BeautifulTable
from datetime import date
from PIL import Image


def get_plots(ev):
    dens_arr = get_sim_dens(ev)
    df_dens = pd.DataFrame({"Density": dens_arr})
    df_dens.to_csv("./data/density.csv", index=True)
    os.system("Rscript graph_ECA.R")


def screenshot():
    os.system(
        f"flameshot full --path ./screenshots/rule:{rule}_n:{n}_{date.today()}.png"
    )


def save_state(ev):

    with open(f"./saved_states/rule:{rule}_n:{n}_{date.today()}.txt", "w") as f:
        f.write(ev)


def get_sim_dens(ev):
    dens = []
    dens.append(density(int(ev, 2)))

    for i in range(1, n):
        ev = Compute(ev, i, flag=False)
        dens.append(density(int(ev, 2)))

    return dens


def density(s: int) -> int:
    d = 0
    while s:
        d += s & 1
        s = s >> 1
    return d


def get_bins(n):
    return [bin(i)[2:].zfill(n) for i in range(2**n)]


def DrawCell(x, y):
    pygame.draw.rect(
        background, colorCell, [x * cellSize, cellSize * y, cellSize, cellSize]
    )


def fun(x: int) -> bool:
    return rule & 1 << x


def Compute(eval_str, y, flag) -> str:
    new = ""
    for i, _ in enumerate(eval_str):
        if i == 0:
            if fun(int(eval_str[-1]) << 2 | int(eval_str[0]) << 1 | int(eval_str[1])):
                new += "1"
                if flag:
                    DrawCell(i, y)
            else:
                new += "0"
        elif i == n - 1:
            if fun(
                int(eval_str[i - 1]) << 2 | int(eval_str[i]) << 1 | int(eval_str[0])
            ):
                new += "1"
                if flag:
                    DrawCell(i, y)
            else:
                new += "0"
        else:
            if fun(
                int(eval_str[i - 1]) << 2 | int(eval_str[i]) << 1 | int(eval_str[i + 1])
            ):
                new += "1"
                if flag:
                    DrawCell(i, y)
            else:
                new += "0"
    return new


def colorMenu():
    table = BeautifulTable()
    table.rows.append(["black"])
    table.rows.append(["white"])
    table.rows.append(["gray"])
    table.rows.append(["red"])
    table.rows.append(["green"])
    table.rows.append(["blue"])
    table.rows.append(["yellow"])
    table.rows.append(["cyan"])
    table.rows.append(["magneta"])
    table.columns.header = ["Color"]
    table.rows.header = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    print(table)


def RandStr() -> str:
    s = ""
    for i in range(n):
        s += str(random.choice([0, 1]))
    return s


def main():
    global rule
    global cellSize
    global n
    global colorBackground
    global colorCell
    global background

    running = True

    colors = {
        "1": (0, 0, 0),
        "2": (255, 255, 255),
        "3": (127, 127, 127),
        "4": (255, 0, 0),
        "5": (0, 255, 0),
        "6": (0, 0, 255),
        "7": (255, 255, 0),
        "8": (255, 255, 0),
        "9": (255, 0, 255),
    }

    banner = """

 .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. |
| |  _________   | || |     ______   | || |      __      | |
| | |_   ___  |  | || |   .' ___  |  | || |     /  \     | |
| |   | |_  \_|  | || |  / .'   \_|  | || |    / /\ \    | |
| |   |  _|  _   | || |  | |         | || |   / ____ \   | |
| |  _| |___/ |  | || |  \ `.___.'\  | || | _/ /    \ \_ | |
| | |_________|  | || |   `._____.'  | || ||____|  |____|| |
| |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------' 

"""

    if len(sys.argv) != 4:
        print(
            "Usage: python3 ECA.py <rule> <cellSize> <n> or python3 ECA.py <file.txt> <rule> <cellSize>"
        )
        sys.exit()
    else:
        print(banner)
        print("\n\n\n\n”")
        print("*" * 100)
        print("**   Press <g> for the plots of the simulation ")
        print("**   Press <s> for take a screenshot ")
        print("**   Press <a> for save the state ")
        print("*" * 100)
        print("\n\n\n\n”")

        if ".txt" in sys.argv[1]:
            file = sys.argv[1]
            rule = int(sys.argv[2])
            cellSize = int(sys.argv[3])
            colorMenu()
            colorBackground = colors[input("Select background color: ")]
            colorCell = colors[input("Select color cell: ")]

            with open(file, "r") as f:
                evalStr = f.read().strip()

            n = len(evalStr)

        else:
            rule = int(sys.argv[1])
            cellSize = int(sys.argv[2])
            n = int(sys.argv[3])
            colorMenu()
            colorBackground = colors[input("Select background color: ")]
            colorCell = colors[input("Select color cell: ")]
            evalStr = RandStr()

        print(evalStr)

        evOg = evalStr
        pygame.init()
        infoObject = pygame.display.Info()
        window = (infoObject.current_w, infoObject.current_h)
        windowSurface = (n * cellSize, n * cellSize)
        screen = pygame.display.set_mode(window, pygame.NOFRAME)

        background = pygame.Surface(windowSurface)
        background.fill(colorBackground)

        screen.fill(colorBackground)

        for i, v in enumerate(evalStr):
            if v == "1":
                DrawCell(i, 0)

        for i in range(1, n):
            evalStr = Compute(evalStr, i, flag=True)

        backgroundOg = background
        screen.blit(background, (0, 0))
        pygame.display.flip()

    vert = 0
    horz = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    # background.fill(colorBackground)
                    vert -= n * 0.10
                    bk1 = backgroundOg
                    screen.fill(colorBackground)
                    screen.blit(bk1, (horz, vert))
                    pygame.display.flip()
                if event.key == pygame.K_UP:
                    vert += n * 0.10
                    bk1 = backgroundOg
                    screen.fill(colorBackground)
                    screen.blit(bk1, (horz, vert))
                    pygame.display.flip()
                if event.key == pygame.K_LEFT:
                    horz += n * 0.10
                    bk1 = backgroundOg
                    screen.fill(colorBackground)
                    screen.blit(bk1, (horz, vert))
                    pygame.display.flip()
                if event.key == pygame.K_RIGHT:
                    horz -= n * 0.10
                    bk1 = backgroundOg
                    screen.fill(colorBackground)
                    screen.blit(bk1, (horz, vert))
                    pygame.display.flip()
                if event.key == pygame.K_g:
                    get_plots(evOg)
                    running = False
                    img = Image.open("./img/density.png")
                    img.show()
                if event.key == pygame.K_s:
                    screenshot()
                    running = False
                if event.key == pygame.K_a:
                    save_state(evOg)
                    running = False

    pygame.quit()


if __name__ == "__main__":
    main()
