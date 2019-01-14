import tester.misc.disjoint as disjoint

count = 0
batch_count = 0

def test(test_function, parameters, invert=False, name=None, show_output=True):
    """
    Runs the given test function with the parameters and checks whether the answer was correct.  (The answer is considered correct if the test function
    returns true.

    :param test_function: The test function
    :param parameters: Any parameters for the test function
    :param invert: Whether to invert the results of the test function. (False becomes correct and True becomes wrong)
    :param name: The name of the test, defaults to the name of the test function if not specified
    :param show_output: Whether the output is shown
    :return: While the results are outputted to stdout, the result is returned
    """

    global count

    if not name:
        name = test_function.__name__

    # Actual Testing

    result = test_function(*parameters)

    if invert:
        result = not result

    # Printing Results

    if show_output:
        print('Test #%d: \'%s\' -- ' % (count, name), end='')

        if result:
            print('PASS')
        else:
            print('FAIL')

    count += 1

    return result

def random_test(test_function, parameters, passes=10, invert=False, name=None, show_inner_output=True, show_output=True):
    """
    This is similar to the test function but it runs the tests multiple times to ensure that random generator functions are correct.
    Note that any elements that are callable in the `parameters` iterable will be executed instead for the test function

    :param test_function: The test function
    :param parameters: Any parameters for the test function
    :param passes: The amount of passes to do
    :param invert: Whether to invert the results of the test function. (False becomes correct and True becomes wrong)
    :param name: The name of the test, defaults to the name of the test function if not specified
    :param show_inner_output: Controls whether the output of each test case is shown
    :param show_output: Controls whether the output of the random test itself is shown
    :return: While the results are outputted to stdout, the result is returned
    """

    global batch_count

    if not name:
        name = test_function.__name__

    if not show_output:
        show_inner_output = False

    if show_output:
        print('-- Batch Case #%d: \'%s\' with %d passes -- ' % (batch_count, name, passes))

    # Actual Testing

    verdict = True
    inner_name = name + ' inner batch case'

    for i in range(passes):
        curr_parameters = []

        for parameter in parameters:
            if hasattr(parameter, '__call__'):
                curr_parameters.append(parameter())
            else:
                curr_parameters.append(parameter)

        verdict &= test(test_function, curr_parameters, invert, inner_name, show_inner_output)

    batch_count += 1

    if show_output:
        print('-- Final Verdict: %s --' % ('PASS' if verdict else 'FAIL'))

    return verdict

def graph_is_connected(node_count, edges):
    """
    Returns whether the supplied graph is connected

    :param node_count: The amount of nodes in the graph
    :param edges: The edges of the graph as a list of tuples (or any other iterable) (i.e. [(1, 2), (2, 3), (1, 3)])
    :return: A bool value specifying whether the graph is connected
    """

    disjoint_set = disjoint.DisjointSet(node_count + 1)

    for a, b in edges:
        disjoint_set.union(a, b)

    # Check if all nodes are part of the same set

    root = disjoint_set.root(1)

    for i in range(2, node_count + 1):
        if disjoint_set.root(i) != root:
            return False

    return True

def graph_has_self_loops(edges):
    """
    Returns whether the supplied graph has any self-loops.  Note that for this check, no node count is necessary

    :param edges: The edges of the graph as a list of tuples (or any other iterable) (i.e. [(1, 2), (2, 3), (1, 3)])
    :return: A bool value specifying whether the graph has any self-loops
    """

    for a, b in edges:
        if a == b:
            return True

    return False

def graph_has_duplicates(edges, is_bidirectional=True):
    """
    Returns whether the supplied graph has any duplicate edges.  Note that for this check, no node count is necessary

    :param edges: The edges of the graph as a list of tuples (or any other iterable) (i.e. [(1, 2), (2, 3), (1, 3)])
    :param is_bidirectional: Whether the graph is bidirectional.  If it is bidirectional, edges like (1, 2) and (2, 1) will be considered duplicate
    :return: A bool value specifying whether the graph has any duplicate edges
    """

    curr_edges = set()

    for edge in edges:
        if is_bidirectional and edge[0] > edge[1]:
            edge = (edge[1], edge[0])

        if edge in curr_edges:
            return True
        else:
            curr_edges.add(edge)

    return False

def sequence_is_increasing(sequence, strict=False):
    """
    Returns whether the sequence is an increasing sequence

    :param sequence: The sequence to test
    :param strict: Whether the sequence must be strictly increasing
    :return: Whether the sequence passes the test
    """

    curr = sequence[0]

    for i in range(1, len(sequence)):
        if (strict and curr == sequence[i]) or curr > sequence[i]:
            return False

        curr = sequence[i]

    return True

def sequence_is_decreasing(sequence, strict=False):
    """
    Returns whether the sequence is an decreasing sequence

    :param sequence: The sequence to test
    :param strict: Whether the sequence must be strictly decreasing
    :return: Whether the sequence passes the test
    """

    return sequence_is_increasing(list(reversed(sequence)), strict)