import pandas as pd
import os
from PIL import Image


def fun(x: int) -> bool:
    return rule & 1 << x


def Compute(eval_str) -> str:
    new = ""
    for i, _ in enumerate(eval_str):
        if i == 0:
            if fun(int(eval_str[-1]) << 2 | int(eval_str[0]) << 1 | int(eval_str[1])):
                new += "1"
            else:
                new += "0"
        elif i == n - 1:
            if fun(
                int(eval_str[i - 1]) << 2 | int(eval_str[i]) << 1 | int(eval_str[0])
            ):
                new += "1"
            else:
                new += "0"
        else:
            if fun(
                int(eval_str[i - 1]) << 2 | int(eval_str[i]) << 1 | int(eval_str[i + 1])
            ):
                new += "1"
            else:
                new += "0"
    return new


def get_bins(n):
    return [bin(i)[2:].zfill(n) for i in range(2**n)]


def atract_frame():
    bins = get_bins(n)
    go_to = []
    for i in bins:
        go_to.append(int(Compute(i), 2))

    no_bin = [int(x, 2) for x in bins]

    return pd.DataFrame({"State": no_bin, "Go to": go_to})


def main():
    global n
    global rule

    n = int(input("N size: "))
    rule = int(input("Rule: "))

    df = atract_frame()
    # print(df)
    df.to_csv(f"./data/attr.csv", index=False)
    os.system("Rscript graph_atractor.R")
    img = Image.open("./img/attractor.png")
    img.show()


if __name__ == "__main__":
    main()
