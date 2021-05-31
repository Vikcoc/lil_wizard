class GameMap:
    def __init__(self, file):
        self.costs = self.read_costs(file)
        self.relief = self.read_relief(file)
        self.items = self.read_items(file)
        self.start_coord = self.get_start_coord()
        self.stone_coord = self.get_stone_coord()

    @staticmethod
    def read_costs(file):
        """
        from the file it reads the costs of each type of tile
        :param file: (filestream) (maybe)
        :return: (dict(string,int))
        """
        costs = {}
        x = next(file)
        while x != '----\n':
            y = x.split()
            costs[y[0]] = int(y[1])
            x = next(file)
        return costs

    @staticmethod
    def read_relief(file):
        """
        reads the tile map
        :param file: (filestream) (maybe)
        :return: (matrix(str))
        """
        relief = []
        x = next(file)
        while x != '\n':
            y = x.split()
            relief.append(y)
            x = next(file)
        return relief

    @staticmethod
    def read_items(file):
        """
        reads the items map
        :param file: (filestream) (maybe)
        :return: (matrix(str))
        """
        items = []
        for x in file:
            y = x.split()
            items.append(y)
        return items

    def get_start_coord(self):
        """
        returns the coordinates of '*'
        :return: [int, int]
        """
        for i in range(len(self.items)):
            for j in range(len(self.items[i])):
                if self.items[i][j] == '*':
                    return [i, j]

    def get_stone_coord(self):
        """
        returns the coordinates of '@'
        :return: [int, int]
        """
        for i in range(len(self.items)):
            for j in range(len(self.items[i])):
                if self.items[i][j] == '@':
                    return [i, j]
