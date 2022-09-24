from tictactoe import Cell, GameField


def check_cell():
    cell = Cell(' ')

    assert cell.is_empty()
    assert cell.get_internal_symbol() == ' '

    cell.update_internal_symbol('X')
    assert cell.get_internal_symbol() == 'X'
    assert not cell.is_empty()


# next_payer_step, next_bot_step
def check_game_field():
    N = 3
    field = GameField(N)
    new_field = [[' ' for i in range(N)] for j in range(N)]
    assert field.get_field_matrix() == new_field

    field.next_player_step(1, 1)
    new_field[0][0] = 'X'
    assert field.matrix[0][0].get_internal_symbol() == 'X'
    field.next_player_step(1, 0)
    assert field.get_field_matrix() == new_field

    field.next_player_step(2, 3)
    new_field[1][2] = '0'
    field.next_player_step(2, 3)

    assert field.get_field_matrix() == new_field

    field.next_player_step(2, 1)
    new_field[1][0] = 'X'
    field.next_player_step(1, 3)
    new_field[0][2] = '0'

    # do some internal changes
    field.matrix[2][0].update_internal_symbol('X')
    new_field[2][0] = 'X'
    assert field.check_player_won('X', False) == True
    assert field.get_field_matrix() == new_field


def check_bot_steps():
    field = GameField(5)
    new_field = [
        [' ', ' ', ' '],
        [' ', 'X', ' '],
        [' ', ' ', '0']
    ]

    field.set_field_matrix(new_field)
    assert field.get_field_matrix() == new_field

    field.next_player_step(1, 2)
    new_field[0][1] = 'X'
    assert field.get_field_matrix() == new_field

    field.next_bot_step()
    new_field[2][1] = '0'
    assert field.get_field_matrix() == new_field


if __name__ == '__main__':
    check_cell()
    check_game_field()
    check_bot_steps()
    print('All tests passed!\n')


