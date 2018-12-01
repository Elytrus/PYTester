import random
import tester.generators.number as numbers


class GraphGenerator:
    def __init__(self, nodes, edges, number_generator=None, allow_duplicate=False, increasing=True):
        """
        Constructor

        :param nodes: The number of nodes
        :param edges: The number of edges
        :param number_generator: Function (or class that implements __call__) that generates the numbers.  This is optional
        :param allow_duplicate: Whether duplicate edges are allowed
        :param increasing: Whether edges have to be in increasing order
        """

        self.increasing = increasing
        self.allow_duplicate = allow_duplicate
        self.nodes = nodes
        self.edges = edges

        if number_generator:
            self.number_generator = number_generator
        else:
            self.number_generator = numbers.RandomGenerator(1, self.nodes)

        if not self.allow_duplicate:
            self.max_edge_count = nodes * (nodes - 1) // 2

            if self.max_edge_count < edges:
                raise ValueError('Edge count too large!')

            # The method being used is selected based on the edge count compared to the maximum amount of edges being
            #  generated.  If the amount of edges being added is greater than half of the maximum edge count,
            # then method 1 (where all possible edges is pre-calculated is used).  Otherwise, method 0 (where edges
            # are randomly generated and checked if they are duplicates) will be used

            self._method = edges > (self.max_edge_count // 2)
            self._method_fun = self._run_method1 if self._method else self._run_method0

            if self._method:
                self._init_method1()
            else:
                self._init_method0()

    def _swap_if_non_increase(self, a, b):
        """
        Randomly swaps the given pair if self.increase is False

        :param a: The first number of the pair
        :param b: The second number of the pair
        :return: A tuple of (int, int)
        """

        if not self.increasing:
            return (a, b) if random.randint(0, 1) else (b, a)
        return a, b

    def _make_node_pair(self):
        """
        Makes a pair of two random nodes.  They will be in increasing order if self.increasing evaluates to true

        :return: A tuple of (int, int)
        """

        a = self.number_generator()
        b = a

        while b == a:
            b = self.number_generator()

        if b < a:
            return b, a

        return a, b

    def _init_method0(self):
        """
        Initialization for method 0: Randomly generate edges
        :return:
        """

        self.used_edges = set()

    def _init_method1(self):
        """
        Initialization for method 1: Pre-calculate all edges and shuffle the list
        :return:
        """

        edges = []

        for i in range(1, self.nodes + 1):
            for j in range(i + 1, self.nodes + 1):
                edges.append((i, j))

        random.shuffle(edges)
        self.edge_iter = iter(edges)

    def _run_method0(self):
        """
        Getting new edge for method 0: Keep generating edges until we have a non-duplicate edge

        :return: A tuple of (int, int)
        """

        edge = self._make_node_pair()

        while edge in self.used_edges:
            edge = self._make_node_pair()

        self.used_edges.add(edge)
        return self._swap_if_non_increase(*edge)

    def _run_method1(self):
        """
        Getting new edge for method 1: Return next element in edge list

        :return: A tuple of (int, int)
        """

        return self._swap_if_non_increase(*next(self.edge_iter))

    def new_edge(self):
        """
        Creates a new edge

        :return: A tuple of (int, int)
        """

        if self.allow_duplicate:
            return self._swap_if_non_increase(*self._make_node_pair())
        else:
            return self._method_fun()

    def __call__(self):
        edges = [self.new_edge() for _ in range(self.edges)]

        if (not self.allow_duplicate) and self._method == 0:
            self.used_edges = set()

        return edges


class TreeGenerator(GraphGenerator):
    def __init__(self, nodes, number_generator=None, increasing=True):
        super().__init__(nodes, nodes - 1, number_generator, True, increasing)

    def __call__(self):
        omitted = self.number_generator()
        edges_start = []
        edges_end = [omitted]
        used_edges = [set() for _ in range(self.nodes + 1)]

        for i in range(1, self.nodes + 1):
            if i != omitted:
                edges_start.append(i)

        for i in range(1, self.nodes - 1):
            val = edges_start[i]

            while val == edges_start[i] or val in used_edges[i]:
                val = self.number_generator()

            used_edges[val].add(i)
            edges_end.append(val)


        if self.increasing:
            return [(j, i) if j < i else (i, j) for i, j in zip(edges_start, edges_end)]

        return list(zip(edges_start, edges_end))


class ConnectedGenerator:
    def __init__(self):
        pass

    def __call__(self):
        pass


class WeightedGenerator:
    def __init__(self, graph_generator, weight_generator=None, min_weight=0, max_weight=0):
        self.graph_generator = graph_generator
        self.weight_generator = weight_generator

        if not self.weight_generator:
            self.weight_generator = numbers.RandomGenerator(min_weight, max_weight)

    def __call__(self):
        edges = self.graph_generator()
        return [edge + (self.weight_generator(),) for edge in edges]