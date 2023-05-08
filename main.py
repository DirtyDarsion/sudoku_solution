import pandas as pd
import xlsxwriter
import copy


def printing_table(table):
    for line in table:
        print(*line)


def to_log(text):
    with open('log.txt', 'a', encoding='utf-8') as file:
        file.write(text + '\n\n')


def zeros_to_list(table):
    new_table = []
    for line in table:
        line = [[i for i in range(1, 10)] if x == 0 else x for x in line]
        new_table.append(line)

    return new_table


def get_cols(table):
    cols = []
    for i in range(9):
        col = []
        for j in range(9):
            col.append(table[j][i])
        cols.append(col)

    return cols


def get_squads(table):
    squads = []
    squad_indexes = []
    for i in range(0, 7, 3):
        for j in range(0, 7, 3):
            squad = []
            squad_index = []
            for k in range(3):
                for m in range(3):
                    squad.append(table[i + k][j + m])
                    squad_index.append([i + k, j + m])
            squads.append(squad)
            squad_indexes.append(squad_index)

    return squads, squad_indexes


def item_in_list(table, j, item, name, table_print):
    for i in range(9):
        if isinstance(table[j][i], list):
            if len(table[j][i]) == 1:
                to_log(f'удаление скобок, {name}, {j}, {i}')
                pd_table = pd.DataFrame(table_print)
                to_log(pd_table.to_string())
                table[j][i] = table[j][i][0]
                return
            if item in table[j][i]:
                to_log(f'удаление элемента, {item}, {name}, {j}, {i}')
                pd_table = pd.DataFrame(table_print)
                to_log(pd_table.to_string())
                table[j][i].remove(item)


def only_one_option_on_line(line, item):
    count = 0
    for i in range(9):
        if isinstance(line[i], list):
            if item in line[i]:
                count += 1
                indx = i

    if count == 1:
        return indx
    else:
        return None


def two_pairs(line, item):
    for i in range(9):
        if isinstance(line[i], list):
            if line[i] != item:
                if item[0] in line[i]:
                    line[i].remove(item[0])
                if item[1] in line[i]:
                    line[i].remove(item[1])


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

    table1 = [
        [0, 5, 2, 0, 7, 1, 0, 4, 8],
        [0, 0, 6, 0, 4, 0, 1, 2, 5],
        [1, 0, 8, 0, 0, 2, 7, 0, 9],
        [2, 0, 5, 4, 9, 0, 8, 1, 6],
        [8, 0, 4, 0, 1, 6, 5, 3, 7],
        [6, 0, 7, 5, 8, 3, 2, 0, 4],
        [0, 2, 0, 7, 6, 4, 0, 8, 1],
        [7, 6, 1, 8, 0, 9, 4, 5, 2],
        [4, 0, 9, 0, 2, 5, 0, 7, 3],
    ]

    table = zeros_to_list(table)
    cols = get_cols(table)
    squads, squad_index = get_squads(table)
    old_table = []
    count = 0

    for _ in range(1):
        while table != old_table:
            count += 1
            old_table = copy.deepcopy(table)
            for i in range(1, 10):
                for j in range(9):
                    if i in table[j]:
                        item_in_list(table, j, i, "line", table)
                    if i in cols[j]:
                        item_in_list(cols, j, i, "col", table)
                    if i in squads[j]:
                        item_in_list(squads, j, i, "squad", table)

            for i in range(1, 10):
                for j in range(9):
                    indx = only_one_option_on_line(table[j], i)
                    if indx:
                        table[j][indx] = i

                for j in range(9):
                    indx = only_one_option_on_line(cols[j], i)
                    if indx:
                        table[indx][j] = i

                for j in range(9):
                    indx = only_one_option_on_line(squads[j], i)
                    if indx:
                        x, y = squad_index[j][indx]
                        table[x][y] = i

        to_log(f'Прогоны: {count}')

        for j in range(9):
            save_items = []
            for k in range(9):
                if isinstance(table[j][k], list):
                    if len(table[j][k]) == 2:
                        if table[j][k] in save_items:
                            two_pairs(table[j], table[j][k])
                            save_items.remove(table[j][k])
                        save_items.append(table[j][k])

            save_items = []
            for k in range(9):
                if isinstance(cols[j][k], list):
                    if len(cols[j][k]) == 2:
                        save_items.append(cols[j][k])

            save_items = []
            for k in range(9):
                if isinstance(squads[j][k], list):
                    if len(squads[j][k]) == 2:
                        if squads[j][k] in save_items:
                            two_pairs(squads[j], squads[j][k])
                        save_items.append(squads[j][k])

    excel = pd.DataFrame(table)

    '''
    writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
    excel.to_excel(writer, 'Sheet1')
    writer._save()
    '''

    to_log(excel.to_string())
    print(excel.to_string())


if __name__ == '__main__':
    main()
