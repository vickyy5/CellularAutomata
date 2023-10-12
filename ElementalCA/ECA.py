import sys
import random
import pygame
from beautifultable import BeautifulTable


def get_bins(n):
    return [bin(i)[2:].zfill(n) for i in range(2**n)]


def DrawCell(x, y):
    pygame.draw.rect(
        background, colorCell, [x * cellSize, cellSize * y, cellSize, cellSize]
    )


def fun(x: int) -> bool:
    return rule & 1 << x


def Compute(eval_str, y) -> str:
    new = ""
    for i, _ in enumerate(eval_str):
        if i == 0:
            if fun(int(eval_str[-1]) << 2 | int(eval_str[0]) << 1 | int(eval_str[1])):
                new += "1"
                DrawCell(i, y)
            else:
                new += "0"
        elif i == n - 1:
            if fun(
                int(eval_str[i - 1]) << 2 | int(eval_str[i]) << 1 | int(eval_str[0])
            ):
                new += "1"
                DrawCell(i, y)
            else:
                new += "0"
        else:
            if fun(
                int(eval_str[i - 1]) << 2 | int(eval_str[i]) << 1 | int(eval_str[i + 1])
            ):
                new += "1"
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
    # print(s)
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

        # print(evalStr)

        pygame.init()
        infoObject = pygame.display.Info()
        window = (infoObject.current_w, infoObject.current_h)
        windowSurface = (n * cellSize, n * cellSize)
        screen = pygame.display.set_mode(window, pygame.NOFRAME)
        # screen.fill(colorBackground)

        background = pygame.Surface(windowSurface)
        background.fill(colorBackground)

        for i, v in enumerate(evalStr):
            if v == "1":
                DrawCell(i, 0)

        for i in range(1, n):
            evalStr = Compute(evalStr, i)

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

    pygame.quit()


if __name__ == "__main__":
    main()
