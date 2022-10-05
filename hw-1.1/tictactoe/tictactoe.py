import sys


class Cell:
    def __init__(self, internal_symbol: str):
        self.__field = ['-----', '| ' + internal_symbol + ' |', '-----']

    def update_internal_symbol(self, new_symbol: str) -> None:
        self.__field[1] = '| ' + new_symbol + ' |'

    def get_internal_symbol(self) -> str:
        return self.__field[1][2]

    def is_empty(self) -> bool:
        return self.__field[1][2] == ' '

    def __str__(self) -> str:
        res = ''
        for i in self.__field:
            res += str(i) + '\n'
        return res

    def print_cell_line(self, index: int) -> None:
        print(self.__field[index], end=' ')


class GameField:
    def __init__(self, n: int):
        self.__size = n
        self.__matrix = [[Cell(' ') for _ in range(n)] for _ in range(n)]
        self.__current_symbol = 'X'
        self.__best_bot_step = (-1, -1)
        self.__max_tree_lvl = 2
        if n < 3:
            self.__size = 0
            print('Too small field')
        self.max_seq_value = min(n, 5)

    def __print_line(self, index: int) -> None:
        for j in range(3):
            for cell in self.__matrix[index]:
                cell.print_cell_line(j)
            print()

    def draw_game_field(self) -> None:
        for i in range(self.__size):
            self.__print_line(i)

    def get_field_matrix(self) -> list:
        matrix = [[' ' for _ in range(self.__size)] for _ in range(self.__size)]
        for i in range(self.__size):
            for j in range(self.__size):
                matrix[i][j] = self.__matrix[i][j].get_internal_symbol()
        return matrix

    def set_field_matrix(self, new_matrix) -> bool:
        if len(new_matrix) < 2:
            return False
        if len(new_matrix) != len(new_matrix[0]):
            return False

        self.__size = len(new_matrix)
        self.__init__(self.__size)
        for i in range(self.__size):
            for j in range(self.__size):
                self.__matrix[i][j].update_internal_symbol(new_matrix[i][j])

        return True

    def __update_cell_by_index(self, x: int, y: int, new_value: str) -> None:
        self.__matrix[x][y].update_internal_symbol(new_value)

    def __check_cell_is_empty(self, x: int, y: int) -> bool:
        return self.__matrix[x][y].is_empty()

    def __check_line(self, index: int, symbol: str) -> bool:
        current_len = 0
        max_len = 0
        for i in range(self.__size):
            if self.__matrix[index][i].get_internal_symbol() == symbol:
                current_len += 1
            else:
                current_len = 0
            max_len = max(max_len, current_len)
        return max_len >= self.max_seq_value

    def __check_column(self, index: int, symbol: str) -> bool:
        current_len = 0
        max_len = 0
        for i in range(self.__size):
            if self.__matrix[i][index].get_internal_symbol() == symbol:
                current_len += 1
            else:
                current_len = 0
            max_len = max(max_len, current_len)
        return max_len >= self.max_seq_value

    def __check_lines(self, symbol) -> bool:
        for i in range(self.__size):
            if self.__check_line(i, symbol):
                return True
        return False

    def __check_columns(self, symbol: str) -> bool:
        for i in range(self.__size):
            if self.__check_column(i, symbol):
                return True
        return False

    def __check_diagonals(self, symbol: str) -> bool:
        current_len = 0
        max_len = 0
        x, y = 0, 0
        for i in range(self.__size):
            x = self.__size - i - 1
            y = 0
            current_len = 0
            max_len = 0
            while x < self.__size and y < self.__size:
                if self.__matrix[x][y].get_internal_symbol() == symbol:
                    current_len += 1
                else:
                    current_len = 0
                max_len = max(max_len, current_len)
                x += 1
                y += 1
            if max_len >= self.max_seq_value:
                return True
        for i in range(self.__size - 1):
            x = 0
            y = self.__size - i - 1
            current_len = 0
            max_len = 0
            while x < self.__size and y < self.__size:
                if self.__matrix[x][y].get_internal_symbol() == symbol:
                    current_len += 1
                else:
                    current_len = 0
                max_len = max(max_len, current_len)
                x += 1
                y += 1
            if max_len >= self.max_seq_value:
                return True
        return False

    def __check_diagonals_reversed(self, symbol: str) -> bool:
        x, y = 0, 0
        for i in range(self.__size):
            x = self.__size - i - 1
            y = 0
            current_len = 0
            max_len = 0
            while x >= 0 and y < self.__size:
                if self.__matrix[x][y].get_internal_symbol() == symbol:
                    current_len += 1
                else:
                    current_len = 0
                max_len = max(max_len, current_len)
                x -= 1
                y += 1
            if max_len >= self.max_seq_value:
                return True

        for i in range(self.__size - 1):
            x = self.__size - i - 1
            y = 0
            current_len = 0
            max_len = 0
            while x >= 0 and y < self.__size:
                if self.__matrix[x][y].get_internal_symbol() == symbol:
                    current_len += 1
                else:
                    current_len = 0
                max_len = max(max_len, current_len)
                x -= 1
                y += 1
            if max_len >= self.max_seq_value:
                return True
        return False

    def __check_no_possible_steps(self):
        for i in range(self.__size):
            for j in range(self.__size):
                if self.__matrix[i][j].get_internal_symbol() == ' ':
                    return False
        return True

    def __check_player_won(self, symbol: str, exit_if_end: bool) -> bool:
        if self.__check_lines(symbol) or \
                self.__check_columns(symbol) or \
                self.__check_diagonals(symbol) or \
                self.__check_diagonals_reversed(symbol):
            if exit_if_end:
                self.draw_game_field()
                print('Player with symbol ' + symbol + ' won!!!')
                sys.exit(0)
            return True
        elif self.__check_no_possible_steps():
            if exit_if_end:
                self.draw_game_field()
                print('Draw!')
                sys.exit(0)
        return False

    def __check_win_after(self, step: tuple, symbol: str) -> bool:
        if self.__check_line(step[0], symbol) or self.__check_column(step[1], symbol) or \
           self.__check_diagonals(symbol) or self.__check_diagonals_reversed(symbol):
            return True
        return False

    def next_player_step(self, x: int, y: int) -> None:
        x -= 1
        y -= 1
        if x >= self.__size or y >= self.__size or x < 0 or y < 0:
            print('Invalid coordinates, check them and try again')
            return
        elif not self.__check_cell_is_empty(x, y):
            print('Invalid coordinates, check them and try again')
            return
        self.__update_cell_by_index(x, y, self.__current_symbol)
        self.__check_player_won(self.__current_symbol, True)
        self.__current_symbol = '0' if self.__current_symbol == 'X' else 'X'

    def next_bot_step(self) -> None:
        possible_steps = set()
        for i in range(self.__size):
            for j in range(self.__size):
                if self.__matrix[i][j].is_empty():
                    possible_steps.add((i, j))

        p_size = len(possible_steps)
        if p_size > 20:
            self.__max_tree_lvl = 2
        elif p_size > 16:
            self.__max_tree_lvl = 3
        elif p_size > 9:
            self.__max_tree_lvl = 4
        else:
            self.__max_tree_lvl = 15
        self.__minimax(possible_steps, self.__max_tree_lvl, '0')
        self.__update_cell_by_index(self.__best_bot_step[0], self.__best_bot_step[1], '0')
        self.__check_player_won(self.__current_symbol, True)
        self.__current_symbol = '0' if self.__current_symbol == 'X' else 'X'

    def __minimax(self, possible_steps: set, lvl: int, symbol: str) -> int:
        if lvl < 0 or len(possible_steps) == 0:
            return 0

        result_step = []
        result_degree = 0
        ps_list = list(possible_steps)
        weights = []
        for step in ps_list:
            possible_steps.discard(step)
            self.__update_cell_by_index(step[0], step[1], symbol)
            if self.__check_win_after(step, symbol):
                self.__best_bot_step = step
                possible_steps.add(step)
                self.__update_cell_by_index(step[0], step[1], ' ')
                return -pow(2, lvl) if symbol == 'X' else (pow(2, lvl) + 1)  # because X is player
            ret = self.__minimax(possible_steps, lvl - 1, '0' if symbol == 'X' else 'X')
            if lvl < self.__max_tree_lvl:
                result_degree += ret
            else:
                weights.append([ret, step])
            possible_steps.add(step)
            self.__update_cell_by_index(step[0], step[1], ' ')
        if lvl == self.__max_tree_lvl:
            cur_max = weights[0][0]
            for w in weights:
                if w[0] >= cur_max:
                    cur_max = w[0]
                    self.__best_bot_step = w[1]
            return cur_max
        self.__best_bot_step = result_step
        return result_degree


def get_field_size() -> int:
    while True:
        size = input('Input Field Size: ')
        if not str.isnumeric(size):
            print('Invalid size, it should be integer!\n Try again.')
        else:
            return int(size)


def get_game_type() -> bool:
    while True:
        t = input('Input type of game. 1 if you want play with bot, 0 if PvP.\n').strip().rstrip()
        if t == '0' or t == '1':
            return bool(t)
        else:
            print('Invalid type. It should be 1 or 0')


if __name__ == '__main__':
    field_size = get_field_size()
    play_with_bot = get_game_type()

    game = GameField(field_size)
    while True:
        print('Your step')
        game.draw_game_field()
        x, y = tuple(map(int, input('Input your coordinates: ').split()))
        game.next_player_step(x, y)
        game.draw_game_field()
        if play_with_bot:
            print('Bot step')
            game.next_bot_step()
