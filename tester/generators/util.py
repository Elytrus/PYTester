def join_all(join_list, *join_chars):
    """
    Helper function for recursively joining nested lists.  The function also casts all non-list elements to strings

    :param join_list: The nested list
    :param join_chars: The different characters to join each layer of the list by.
    :return: The joined data
    """

    def recur(curr_list, layer):
        typ = type(curr_list)

        if typ == list or typ == tuple:
            return join_chars[layer].join([recur(elem, layer + 1) for elem in curr_list])

        return str(curr_list)

    return recur(join_list, 0)


class QueryGenerator:
    """
    A generator that allows for different generators to be run depending on queries.
    This is useful in cases where you have many different of queries that need to be supported.
    A good example of this is https://dmoj.ca/problem/ds3

    I.e. 
    """

    def __init__(self, type_generator, **mappings):
        """
        Constructor

        :param type_generator: A generator that creates all of the different query types
        :param mappings: A mapping of each type query to a generator
        """


class Joiner:
    """
    A generator that joins the results of other generators
    """

    def __init__(self, *generators):
        """
        Constructor

        :param generators: Argument list of generators that are being joined
        """

        self.generators = generators

    def __call__(self):
        lis = []
        for generator in self.generators:
            lis.extend(generator())
        return lis


class Repeater:
    """
    A generator that repeatedly generates results from a generator and returns the results as a list
    """

    def __init__(self, generator, count=1):
        """
        Constructor

        :param generator: The generator being used
        :param count: The amount of times to repeat the generation process
        """

        self.count = count
        self.generator = generator

    def __call__(self):
        return [self.generator() for _ in range(self.count)]


"""
Aliases for the generators (their names can be very long)
"""

qugen = QueryGenerator
join = Joiner
rep = Repeater