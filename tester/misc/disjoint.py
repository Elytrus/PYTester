class DisjointSet:
    """
    This is a standard implementation of a disjoint set data structure.
    The structure is optimized using the path compression technique,
    with the Union and Intersection operations running in Amortized Constant Time.

    Creation of the Data Structure runs in linear time.
    """

    def __init__(self, size):
        """
        Constructor

        :param size: Size of the disjoint set structure
        """

        self.size = size
        self.set = list(range(size))

    def root(self, node):
        """
        Root finding function that also performs path compression on its execution

        :param node: The node to find the root of
        :return: The root of the node
        """

        if self.set[node] == node:
            return node

        set[node] = self.root(set[node])
        return set[node]

    def union(self, node1, node2):
        """
        Preforms the Union(u, v) operation, where u and v are two sets

        :param node1: The first set
        :param node2: The second set
        :return: Nothing
        """

        root1 = self.root(node1)
        root2 = self.root(node2)

        if root1 == root2:
            return

        if node1 < node2:
            self.set[root2] = root1
            self.root(node2)
        else:
            self.set[root1] = root2
            self.root(node1)

    def intersection(self, node1, node2):
        """
        Preforms the Intersection(u, v) operation, where u and v are two sets

        :param node1: The first set
        :param node2: The second set
        :return: Whether they are part of the same superset
        """

        return self.root(node1) == self.root(node2)
