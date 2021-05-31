import copy
from math import sqrt


class GameNode:
    def __init__(self, parent, info, cost, estimate):
        self.parent = parent
        self.info = info
        self.cost = cost
        self.estimate = estimate
        self.print_depth = 0

    def on_branch(self, new_info):
        """
        short function to see if the state of the node has already been reached
        :param new_info: (GameNode) a potential child
        :return: (bool)
        """
        nod = self
        while nod is not None:
            if new_info == nod.info:
                return True
            nod = nod.parent
        return False

    def __repr__(self):
        sir = ""
        sir += str(self.info)
        return sir

    def __str__(self):
        """
        a long ass function to make the result look like on the site
        :return: (str)
        """
        if self.parent is None:
            return 'Pas 0). Incepe drumul cu cizme de culoare ' + self.info[2] + ' din locatia(' + str(self.info[0]) + \
                   ', ' + str(self.info[1]) + '). Incaltat: ' + self.info[2] + ' (purtari: ' + str(self.info[3]) + \
                   '). Desaga: nimic. Fara piatra.\n'

        sir = str(self.parent)
        sir = sir + 'C: ' + str(self.cost) + ' E: ' + str(self.estimate) + ' '
        self.print_depth = self.parent.print_depth + 1
        sir = sir + 'Pas ' + str(self.print_depth) + '). '

        plus_drum = False

        if len(set([self.info[2], self.info[4], self.parent.info[2], self.parent.info[4]])) != 2:
            plus_drum = True
            if self.info[2] != self.parent.info[2]:
                if self.parent.info[2] == self.info[4]:
                    sir = sir + 'A gasit cizme ' + self.info[2] + \
                          '. Muta cizmele incaltate in desaga si le incalta pe cele din patratel '
                else:
                    sir = sir + 'I s-au tocit cizmele ' + self.parent.info[2] + '. '
                    if self.parent.info[4] == self.info[2]:
                        sir = sir + 'Incalta cizmele din desaga '
                    else:
                        sir = sir + 'A gasit cizme ' + self.info[2] + '. Incalta aceste cizme '
            else:
                sir = sir + 'A gasit cizme ' + self.info[4] + '. Schimba cizmele din desaga cu cele din patratel '
        elif self.info[2] != self.parent.info[2]:
            plus_drum = True
            sir = sir + 'A schimbat cizmele '

        if self.info[6] != self.parent.info[6]:
            if plus_drum:
                sir = sir + 'ia piatra '
            else:
                sir = sir + 'Ia piatra '
                plus_drum = True

        if plus_drum:
            sir = sir + 'si porneste la drum. '

        sir = sir + 'Paseste din (' + str(self.parent.info[0]) + ', ' + str(self.parent.info[1]) + ') in (' + \
            str(self.info[0]) + ', ' + str(self.info[1]) + '). Incaltat: ' + self.info[2] + \
            ' (purtari: ' + str(self.info[3]) + '). Desaga: '

        if self.info[4] == '0':
            sir = sir + 'nimic. '
        else:
            sir = sir + self.info[4] + ' (purtari: ' + str(self.info[5]) + '). '

        if self.info[6]:
            sir = sir + 'Cu piatra.'
        else:
            sir = sir + 'Fara piatra.'

        return sir + '\n'

    def feet_boot_possible(self, x, y, game_map):
        """
        helper function to see if we can traverse into the (x, y) tile with the boots on the feet
        :param x: (int) x coord
        :param y: (itn) y coord
        :param game_map: (GameMap) the map of the game
        :return: (bool)
        """
        if game_map.relief[x][y] == self.info[2] and self.info[3] < 4:
            return True
        return False

    def bag_boot_possible(self, x, y, game_map):
        """
        helper function to see if we can traverse into the (x, y) tile with the boots in the bag
        :param x: (int) x coord
        :param y: (itn) y coord
        :param game_map: (GameMap) the map of the game
        :return: (bool)
        """
        if game_map.relief[x][y] == self.info[4] and self.info[5] < 4:
            return True
        return False

    def floor_boot_possible(self, x, y, game_map):
        """
        helper function to see if we can traverse into the (x, y) tile with the boots on the floor
        :param x: (int) x coord
        :param y: (itn) y coord
        :param game_map: (GameMap) the map of the game
        :return: (bool)
        """
        if game_map.relief[x][y] == game_map.items[self.info[0]][self.info[1]]:
            return True
        return False

    def boot_possible(self, x, y, game_map):
        """
        helper function to see if we can traverse into the (x, y) tile with the boots available
        :param x: (int) x coord
        :param y: (itn) y coord
        :param game_map: (GameMap) the map of the game
        :return: (bool)
        """
        if self.feet_boot_possible(x, y, game_map) \
                or self.bag_boot_possible(x, y, game_map) \
                or self.floor_boot_possible(x, y, game_map):
            return True
        return False

    def replenish_boot(self, game_map):
        """
        longer function that handles boot logic after each move
        :param game_map: (GameMap) the map of the game
        :return:
        """
        if self.info[3] >= 3:  # if boots wear out we change
            self.info[2] = self.info[4]
            self.info[4] = '0'
            self.info[3] = self.info[5]
            self.info[5] = 0

        if game_map.items[self.info[0]][self.info[1]] != '0' \
                and game_map.items[self.info[0]][self.info[1]] != '*' \
                and game_map.items[self.info[0]][self.info[1]] != '@' \
                and self.info[4] == '0':  # add boots if inventory empty
            self.info[4] = game_map.items[self.info[0]][self.info[1]]
        # if inventory full refresh
        elif game_map.items[self.info[0]][self.info[1]] == self.info[2] == self.info[4]:
            if self.info[3] > self.info[5]:
                self.info[3] = 0
            else:
                self.info[5] = 0
        elif game_map.items[self.info[0]][self.info[1]] == self.info[2]:
            self.info[3] = 0
        elif game_map.items[self.info[0]][self.info[1]] == self.info[4]:
            self.info[5] = 0

        # edge case in which we wore out boots with no boots in back but we just added them from floor
        if self.info[2] == '0':
            self.info[2] = self.info[4]
            self.info[4] = '0'
            self.info[3] = self.info[5]
            self.info[5] = 0

    def give_children(self, game_map, heuristic):
        """
        another long ass function, this function gives the direct children of the current node
        :param game_map: (GameMap) the map of the game
        :param heuristic: (int) which heuristic to use from 0 to 3
        :return: (list(GameNode)) the children
        """
        directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        children = []
        # we make new node copy to preserve this nodes state
        # and because it is easier to write self affecting methods
        new_nod = GameNode(None, copy.deepcopy(self.info), self.cost, self.estimate)

        # quick getting stone logic
        if new_nod.info[6] or game_map.items[new_nod.info[0]][new_nod.info[1]] == '@':
            new_nod.info[6] = True

        # quick boot replenishment logic
        new_nod.replenish_boot(game_map)

        for direction in directions:
            # we see if move is valid
            if 0 <= self.info[0] + direction[0] < len(game_map.relief) and \
                    0 <= self.info[1] + direction[1] < len(game_map.relief[0]):

                x, y = self.info[0] + direction[0], self.info[1] + direction[1]

                # we see if we can move forward
                if new_nod.boot_possible(x, y, game_map):  # when making node also check for in branch
                    # we see if we can move forward with the boots we have
                    if new_nod.feet_boot_possible(x, y, game_map):
                        nympho = copy.deepcopy(new_nod.info)
                        # we make new node with no new boots
                        children.append([x, y, new_nod.info[2], new_nod.info[3] + 1, new_nod.info[4], new_nod.info[5],
                                         new_nod.info[6], 0])
                        # we see if we have new boots on the floor different from feet or back and back not empty
                        if game_map.items[new_nod.info[0]][new_nod.info[1]] != new_nod.info[2] \
                                and game_map.items[new_nod.info[0]][new_nod.info[1]] != new_nod.info[4] \
                                and new_nod.info[4] != '0' \
                                and game_map.items[new_nod.info[0]][new_nod.info[1]] != '0' \
                                and game_map.items[new_nod.info[0]][new_nod.info[1]] != '*' \
                                and game_map.items[new_nod.info[0]][new_nod.info[1]] != '@':
                            # if so we check if we have feet boots in the back
                            if new_nod.info[2] == new_nod.info[4]:
                                # if so we take on feet the least used ones
                                new_nod.info[3] = min(new_nod.info[3], new_nod.info[5])
                            # we take in back the new ones
                            new_nod.info[4] = game_map.items[new_nod.info[0]][new_nod.info[1]]
                            new_nod.info[5] = 0
                            # we make new node
                            children.append(
                                [x, y, new_nod.info[2], new_nod.info[3] + 1, new_nod.info[4], new_nod.info[5],
                                 new_nod.info[6], 0])
                        new_nod.info = nympho
                    elif new_nod.bag_boot_possible(x, y, game_map):
                        nympho = copy.deepcopy(new_nod.info)
                        # we put bag boots on feet
                        auxb = new_nod.info[2]
                        auxc = new_nod.info[3]
                        new_nod.info[2] = new_nod.info[4]
                        new_nod.info[3] = new_nod.info[5]
                        new_nod.info[4] = auxb
                        new_nod.info[5] = auxc
                        # we make new node with no new boots
                        children.append([x, y, new_nod.info[2], new_nod.info[3] + 1, new_nod.info[4], new_nod.info[5],
                                         new_nod.info[6], 0])
                        # we see if we have new boots on the floor different from feet or back
                        if game_map.items[new_nod.info[0]][new_nod.info[1]] != new_nod.info[2] \
                                and game_map.items[new_nod.info[0]][new_nod.info[1]] != new_nod.info[4] \
                                and new_nod.info[4] != '0' \
                                and game_map.items[new_nod.info[0]][new_nod.info[1]] != '0' \
                                and game_map.items[new_nod.info[0]][new_nod.info[1]] != '*' \
                                and game_map.items[new_nod.info[0]][new_nod.info[1]] != '@':
                            # if so we take in back the new ones
                            new_nod.info[4] = game_map.items[new_nod.info[0]][new_nod.info[1]]
                            new_nod.info[5] = 0
                            # we make new node
                            children.append(
                                [x, y, new_nod.info[2], new_nod.info[3] + 1, new_nod.info[4], new_nod.info[5],
                                 new_nod.info[6], 0])
                        new_nod.info = nympho
                    elif new_nod.floor_boot_possible(x, y, game_map):
                        nympho = copy.deepcopy(new_nod.info)
                        # we check if we have feet boots in the back
                        if new_nod.info[2] == new_nod.info[4]:
                            # if so we take in back the least used ones and make new node
                            new_nod.info[5] = min(new_nod.info[3], new_nod.info[5])
                            new_nod.info[2] = game_map.items[new_nod.info[0]][new_nod.info[1]]
                            new_nod.info[3] = 0
                            children.append(
                                [x, y, new_nod.info[2], new_nod.info[3] + 1, new_nod.info[4], new_nod.info[5],
                                 new_nod.info[6], 0])
                        else:
                            # we make new node with floor and back
                            auxb = new_nod.info[2]
                            auxc = new_nod.info[3]
                            new_nod.info[2] = game_map.items[new_nod.info[0]][new_nod.info[1]]
                            new_nod.info[3] = 0
                            if new_nod.info[4] != '0':
                                children.append(
                                    [x, y, new_nod.info[2], new_nod.info[3] + 1, new_nod.info[4], new_nod.info[5],
                                     new_nod.info[6], 0])
                            # and we make new node with floor and feet
                            new_nod.info[4] = auxb
                            new_nod.info[5] = auxc
                            children.append(
                                [x, y, new_nod.info[2], new_nod.info[3] + 1, new_nod.info[4], new_nod.info[5],
                                 new_nod.info[6], 0])
                        new_nod.info = nympho
        children = filter(lambda child: not self.on_branch(child), children)
        return list(map(lambda child: GameNode(self, child,
                                               self.cost + game_map.costs[game_map.relief[child[0]][child[1]]],
                                               self.cost + self.estimate_cost(child, game_map, heuristic)),
                        children))

    @staticmethod
    def estimate_cost(info, game_map, heuristic):
        """
        a smaller function that takes a nodes information and estimates how far it is from the goal
        :param info: (GameNode.info)
        :param game_map: (GameMap) the map of the game
        :param heuristic: (int) which heuristic to use from 0 to 3
        :return: (int/float) estimated cost to the goal
        """
        if heuristic == 0:  # the basic
            return 0
        elif heuristic == 1:  # the Manhattan
            estimate = 0
            if info[6]:
                estimate = estimate + abs(info[0] - game_map.start_coord[0]) + abs(info[1] - game_map.start_coord[1])
            else:
                estimate = estimate + abs(info[0] - game_map.stone_coord[0]) + abs(info[1] - game_map.stone_coord[1])
                estimate = estimate + abs(game_map.start_coord[0] - game_map.stone_coord[0])
                estimate = estimate + abs(game_map.start_coord[1] - game_map.stone_coord[1])
            return estimate * min(game_map.costs.values())
        elif heuristic == 2:  # the euclidean
            estimate = 0
            if info[6]:
                estimate = estimate + sqrt((info[0] - game_map.start_coord[0]) ** 2 +
                                           (info[1] - game_map.start_coord[1]) ** 2)
            else:
                estimate = estimate + sqrt((info[0] - game_map.stone_coord[0]) ** 2 +
                                           (info[1] - game_map.stone_coord[1]) ** 2)
                estimate = estimate + sqrt((game_map.start_coord[0] - game_map.stone_coord[0]) ** 2 +
                                           (game_map.start_coord[1] - game_map.stone_coord[1]) ** 2)
            return estimate * min(game_map.costs.values())
        elif heuristic == 3:  # the invalid one
            # a more interesting one would be to add the cost of each tile in a direct path to the objectives
            # but it's more costly to implement then the distance to the stone * the biggest cost
            return abs(info[0] - game_map.start_coord[0]) + abs(info[1] - game_map.start_coord[1]) * \
                   max(game_map.costs.values())
        return 0
