
import doctest

def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    keys = ("board", "dimensions", "state", "visible")
    # ^ Uses only default game keys. If you modify this you will need
    # to update the docstrings in other functions!
    for key in keys:
        val = game[key]
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)


# 2-D IMPLEMENTATION


def new_game_2d(nrows, ncolumns, mines):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Parameters:
       nrows (int): Number of rows
       ncolumns (int): Number of columns
       mines (list): List of mines, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    state: ongoing
    visible:
        [False, False, False, False]
        [False, False, False, False]
    """
    return new_game_nd((nrows, ncolumns), mines)


def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['visible'] to reveal (row, col).  Then, if (row, col) has no
    adjacent mines (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one mine
    is visible on the board after digging (i.e. game['visible'][mine_location]
    == True), 'victory' when all safe squares (squares that do not contain a
    mine) and no mines are visible, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    state: victory
    visible:
        [False, True, True, True]
        [False, False, True, True]

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    state: defeat
    visible:
        [True, True, False, False]
        [False, False, False, False]
    """
    return dig_nd(game, (row, col))


def render_2d_locations(game, all_visible=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (mines), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    mines).  game['visible'] indicates which squares should be visible.  If
    all_visible is True (the default is False), game['visible'] is ignored
    and all cells are shown.

    Parameters:
       game (dict): Game state
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                    by game['visible']

    Returns:
       A 2D array (list of lists)

    >>> game = {'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible':  [[False, True, True, False],
    ...                   [False, False, True, False]]}
    >>> render_2d_locations(game, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d_locations(game, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    return render_nd(game, all_visible)


def render_2d_board(game, all_visible=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                           by game['visible']

    Returns:
       A string-based representation of game

    >>> render_2d_board({'dimensions': (2, 4),
    ...                  'state': 'ongoing',
    ...                  'board': [['.', 3, 1, 0],
    ...                            ['.', '.', 1, 0]],
    ...                  'visible':  [[True, True, True, False],
    ...                            [False, False, True, False]]})
    '.31_\\n__1_'
    """
    locations = render_2d_locations(game, all_visible)
    big_str = ""
    for row in locations:
        small_str = ""
        for col in row:
            small_str += col
        small_str += "\n"
        big_str += small_str
    return big_str[:-1]


def recursive_helper(mine, n, dimensions):
    """
    Finds all valid neighbors
    """
    neighbor_set = set()
    if n == 1:
        if 0 <= mine[0] + 1 < dimensions[0]:
            neighbor_set.add((mine[0] + 1,))
        if 0 <= mine[0] - 1 < dimensions[0]:
            neighbor_set.add((mine[0] - 1,))
        return neighbor_set
    else:
        new_set = set()
        if 0 <= mine[n - 1] + 1 < dimensions[n - 1]:
            new_set.add((mine[n - 1] + 1,))
        if 0 <= mine[n - 1] - 1 < dimensions[n - 1]:
            new_set.add((mine[n - 1] - 1,))
        new_set.add((mine[n - 1],))
        newer_set = recursive_helper(mine, n - 1, dimensions)
        newer_set.add(
            mine[0 : n - 1],
        )
        for neighbor in newer_set:
            for new_neighbor in new_set:
                if neighbor + new_neighbor != mine:
                    neighbor_set.add(neighbor + new_neighbor)
        return neighbor_set


# N-D IMPLEMENTATION
def increment_squares_around_mine_nd(board, n, dimensions, mines):
    """
    Given a board and where the mines are placed,
    all squares around mines are incremented by 1
    if they are inside the board and are not a mine
    """

    for mine in mines:
        neighbors = recursive_helper(mine, n, dimensions)
        for n_1 in neighbors:
            if slice_array(board, n_1) != ".":
                slice_and_update_array(board, n_1, (slice_array(board, n_1) + 1))
    return board


def generate_nested_list_false(dimensions, current_dimension):
    """
    Function to generate n-dimensional nested list using recursion.

    Parameters:
        dimensions (tuple): A tuple containing the size of each dimension.
        current_dimension (int): The current dimension to generate.

    Returns:
        list: A nested list of specified dimensions.
    """
    if current_dimension == len(dimensions):
        return [False] * dimensions[
            current_dimension - 1
        ]  # Base case: return a list of zeros of specified length

    # Recursive case: generate nested lists for each dimension
    return [
        generate_nested_list_false(dimensions, current_dimension + 1)
        for _ in range(dimensions[current_dimension - 1])
    ]


def generate_nested_list(dimensions, current_dimension):
    """
    Function to generate n-dimensional nested list using recursion.

    Parameters:
        dimensions (tuple): A tuple containing the size of each dimension.
        current_dimension (int): The current dimension to generate.

    Returns:
        list: A nested list of specified dimensions.
    """
    if current_dimension == len(dimensions):
        return [0] * dimensions[
            current_dimension - 1
        ]  # Base case: return a list of zeros of specified length

    # Recursive case: generate nested lists for each dimension
    return [
        generate_nested_list(dimensions, current_dimension + 1)
        for _ in range(dimensions[current_dimension - 1])
    ]


def slice_and_update_array(arr, indices, value):
    """
    Slices at indices and updates value to value indicated
    """

    # Base case: If the indices tuple is empty, update the value
    if len(indices) == 1:
        arr[indices[0]] = value
    else:
        # Get the first index from the tuple
        idx = indices[0]

        # Recursively slice into the array using the remaining indices
        slice_and_update_array(arr[idx], indices[1:], value)


def slice_array(arr, indices):
    """
    Simplies returns whatever is at the index in question
    """
    # Base case: If indices is empty, return the array
    if len(indices) == 0:
        return arr
    # Get the first index from the tuple
    idx = indices[0]
    # Slice into the array using the index
    sliced_array = arr[idx]
    # Recursively slice the sliced array with the remaining indices
    return slice_array(sliced_array, indices[1:])


def new_game_nd(dimensions, mines):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Args:
       dimensions (tuple): Dimensions of the board
       mines (list): mine locations as a list of tuples, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    """
    visible = generate_nested_list_false(dimensions, 1)
    board = generate_nested_list(dimensions, 1)
    for mine in mines:
        slice_and_update_array(board, mine, ".")
    board = increment_squares_around_mine_nd(board, len(dimensions), dimensions, mines)
    return {
        "dimensions": dimensions,
        "board": board,
        "visible": visible,
        "state": "ongoing",
    }


def generate_coordinates(dimensions, current_coordinate=None, depth=0):
    """
    Generates all possible coordinates in the board
    """
    if current_coordinate is None:
        current_coordinate = []
    if depth == len(dimensions):
        yield tuple(current_coordinate)
        return

    for i in range(dimensions[depth]):
        current_coordinate.append(i)
        yield from generate_coordinates(dimensions, current_coordinate, depth + 1)
        current_coordinate.pop()


def revealed_squares(game, coordinates, visited):
    """
    Returns a list of revealed coordinates
    """
    if slice_array(game["board"], coordinates) != 0:
        visited.add(coordinates)
        return [coordinates]

    else:
        potential_neighbors = recursive_helper(
            coordinates, len(game["dimensions"]), game["dimensions"]
        )
        final_list = [coordinates]
        visited.add(coordinates)
        for neighbor in potential_neighbors:
            if neighbor not in visited:
                final_list.extend(revealed_squares(game, neighbor, visited))
                visited.add(neighbor)
        return final_list


def dig_nd(game, coordinates):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the visible to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    mine.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one mine is visible on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a mine) and no mines are visible, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [False, False],
    ...                [False, False]],
    ...               [[False, False], [False, False], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, True], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [False, False],
    ...                [False, False]],
    ...               [[False, False], [False, False], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: defeat
    visible:
        [[False, True], [False, True], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    """
    if game["state"] == "defeat" or game["state"] == "victory":
        game["state"] = game["state"]  # keep the state the same
        return 0

    if slice_array(game["board"], coordinates) == ".":
        slice_and_update_array(game["visible"], coordinates, True)
        game["state"] = "defeat"
        return 1

    revealed = 0
    for tile in revealed_squares(game, coordinates, set()):
        if slice_array(game["visible"], tile) is False:
            slice_and_update_array(game["visible"], tile, True)
            revealed += 1

    counter = 0
    for i in generate_coordinates(game["dimensions"]):
        if (
            slice_array(game["visible"], i) is False
            and slice_array(game["board"], i) != "."
        ):
            counter += 1
    if counter != 0:
        game["state"] = "ongoing"
        return revealed
    else:
        game["state"] = "victory"
        return revealed


def render_nd(game, all_visible=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), '.'
    (mines), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    mines).  The game['visible'] array indicates which squares should be
    visible.  If all_visible is True (the default is False), the game['visible']
    array is ignored and all cells are shown.

    Args:
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                           by game['visible']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [True, True],
    ...                [True, True]],
    ...               [[False, False], [False, False], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    coordinates = generate_coordinates(game["dimensions"])
    new_board = generate_nested_list(game["dimensions"], 1)
    if all_visible:
        for i in coordinates:
            i_board = slice_array(game["board"], i)
            if slice_array(game["board"], i) == ".":
                slice_and_update_array(new_board, i, ".")
            elif i_board != 0:
                slice_and_update_array(new_board, i, str(i_board))
            else:
                slice_and_update_array(new_board, i, " ")
    else:
        for i in coordinates:
            i_val = slice_array(game["visible"], i)
            i_board = slice_array(game["board"], i)
            if i_val is True:
                if slice_array(game["board"], i) == ".":
                    slice_and_update_array(new_board, i, ".")
                elif i_board != 0:
                    slice_and_update_array(new_board, i, str(i_board))
                else:
                    slice_and_update_array(new_board, i, " ")
            else:
                slice_and_update_array(new_board, i, "_")

    return new_board


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d_locations or any other function you might want.  To
    # do so, comment out the above line, and uncomment the below line of code.
    # This may be useful as you write/debug individual doctests or functions.
    # Also, the verbose flag can be set to True to see all test results,
    # including those that pass.
    #
    # doctest.run_docstring_examples(
    #    render_2d_locations,
    #    globals(),
    #    optionflags=_doctest_flags,
    #    verbose=False
    # )
    # arr = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
    # indices = (1, 0, 1)  # Indices to slice: arr[1][0][1]

    # sliced_value = slice_array(arr, indices)
    # print(sliced_value)  # Output the sliced value
    # Example usage:
