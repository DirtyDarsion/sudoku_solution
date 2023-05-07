import pandas as pd
import xlsxwriter


def printing_table(table):
    for line in table:
        print(*line)


def zeros_to_list(table):
    new_table = []
    for line in table:
        line = [[] if x == 0 else x for x in line]
        new_table.append(line)

    return new_table


def item_in_list(line, item):
    for obj in line:
        if isinstance(obj, list):
            if item in obj:
                obj.remove(item)


def item_not_in_list(line, item):
    for obj in line:
        if isinstance(obj, list):
            if item not in obj:
                obj.append(item)


def main():
    table = [
        [9, 8, 2, 0, 0, 1, 0, 6, 3],
        [6, 0, 0, 3, 2, 9, 0, 0, 8],
        [0, 0, 0, 0, 8, 0, 0, 0, 0],
        [0, 0, 1, 5, 0, 3, 0, 0, 0],
        [3, 0, 9, 0, 1, 0, 7, 5, 0],
        [0, 0, 8, 0, 0, 7, 0, 1, 6],
        [1, 0, 0, 0, 0, 0, 6, 3, 0],
        [7, 0, 0, 0, 0, 0, 0, 2, 0],
        [0, 0, 0, 0, 3, 0, 0, 9, 0],
    ]

    table = zeros_to_list(table)
    cols = []

    for i in range(9):
        col = []
        for j in range(9):
            col.append(table[j][i])
        cols.append(col)

    for i in range(1, 10):
        print(f'Start {i}')

        for line in table:
            if i in line:
                item_in_list(line, i)
            else:
                item_not_in_list(line, i)

        for line in cols:
            if i in line:
                item_in_list(line, i)
            else:
                item_not_in_list(line, i)

    excel = pd.DataFrame(table)

    writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
    excel.to_excel(writer, 'Sheet1')
    writer._save()

    print(excel.to_string())


if __name__ == '__main__':
    main()
