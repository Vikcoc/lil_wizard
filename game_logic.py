from game_node import GameNode
import time


class GameLogic:
    def __init__(self, game_map):
        self.game_map = game_map
        self.start_nod = self.start_state_from_map(game_map)

    @staticmethod
    def start_state_from_map(game_map):
        """
        from the map calculates the start point
        :param game_map: (GameMap) the map of the game as read from file
        :return: (GameNode) The start point of the wizard
        """
        x, y = game_map.start_coord
        return GameNode(None, [x, y, game_map.relief[x][y], 1, '0', 0, False, 0], game_map.costs[game_map.relief[x][y]],
                        float('inf'))

    def is_final_nod(self, nod):
        """
        checks if a node is a final state
        :param nod: (GameNode)
        :return:
        """
        if self.start_nod.info[0] == nod.info[0] and self.start_nod.info[1] == nod.info[1] and nod.info[6]:
            return True
        return False

    def ucs(self, sol_number, start_time, time_out):
        """
        ucs search algorithm
        :param sol_number: (int) number of solutions to search for
        :param start_time: (float) the timestamp that the algorithm is considered to have started at
        :param time_out: (float) how long until it stops running
        :return: (list(GameNode, float, int, int)) the list of solutions
        """
        sol = []
        queue = [self.start_nod]
        max_mem = 0
        total_w = 1
        while len(queue) > 0:
            time1 = time.time()
            if time1 - start_time >= time_out:
                sol.append(('Timeout', time1 - start_time, max_mem, total_w))
                return sol
            curr = queue[0]
            queue.pop(0)
            if self.is_final_nod(curr):
                sol.append((curr, time1 - start_time, max_mem, total_w))
                sol_number = sol_number - 1
                if sol_number <= 0:
                    return sol
                continue
            children = curr.give_children(self.game_map, 0)
            total_w = total_w + len(children)
            for nod in children:
                poz = 0
                while poz < len(queue) and nod.cost > queue[poz].cost:
                    poz += 1
                queue.insert(poz, nod)
            max_mem = max(max_mem, len(queue))
        if len(sol) == 0:
            sol.append(('No solution', time.time() - start_time, max_mem, total_w))
        return sol

    def a_star(self, sol_number, heuristic, start_time, time_out):
        """
        a* algorithm
        :param sol_number: (int) number of solutions to search for
        :param heuristic: (int) which heuristic to use from 0 to 3
        :param start_time: (float) the timestamp that the algorithm is considered to have started at
        :param time_out: (float) how long until it stops running
        :return: (list(GameNode, float, int, int)) the list of solutions
        """
        sol = []
        queue = [self.start_nod]
        max_mem = 0
        total_w = 1
        while len(queue) > 0:
            time1 = time.time()
            if time1 - start_time >= time_out:
                sol.append(('Timeout', time1 - start_time, max_mem, total_w))
                return sol
            curr = queue.pop(0)
            if self.is_final_nod(curr):
                sol.append((curr, time1 - start_time, max_mem, total_w))
                sol_number = sol_number - 1
                if sol_number <= 0:
                    return sol
                continue
            children = curr.give_children(self.game_map, heuristic)
            total_w = total_w + len(children)
            for nod in children:
                a_star_list_insert(queue, nod)
            max_mem = max(max_mem, len(queue))
        if len(sol) == 0:
            sol.append(('No solution', time.time() - start_time, max_mem, total_w))
        return sol

    def a_star_optimal(self, heuristic, start_time, time_out):
        """
        a* the optimal algorithm
        :param heuristic: (int) which heuristic to use from 0 to 3
        :param start_time: (float) the timestamp that the algorithm is considered to have started at
        :param time_out: (float) how long until it stops running
        :return: (list(GameNode, float, int, int)) the list of solutions
        """
        opened = [self.start_nod]
        closed = []
        max_mem = 0
        total_w = 1
        while len(opened) > 0:
            time1 = time.time()
            if time1 - start_time >= time_out:
                return 'Timeout', time1 - start_time, max_mem, total_w

            curr = opened.pop(0)
            closed.append(curr)
            if self.is_final_nod(curr):
                return curr, time1 - start_time, max_mem, total_w

            children = curr.give_children(self.game_map, heuristic)
            total_w = total_w + len(children)

            for nod in children:
                nod_open = node_with_same_info(opened, nod)
                if nod_open is not None:
                    if nod_open.estimate > nod.estimate:
                        opened.remove(nod_open)
                        a_star_list_insert(opened, nod)
                    continue
                nod_close = node_with_same_info(closed, nod)
                if nod_close is not None:
                    if nod_close.estimate > nod.estimate:
                        closed.remove(nod_close)
                        a_star_list_insert(closed, nod)
                    continue
                a_star_list_insert(opened, nod)
            max_mem = max(max_mem, len(opened) + len(closed))
        return None, time.time() - start_time, max_mem, total_w

    def ida_star(self, heuristic, start_time, time_out):
        """
        ida* algorithm
        :param heuristic: (int) which heuristic to use from 0 to 3
        :param start_time: (float) the timestamp that the algorithm is considered to have started at
        :param time_out: (float) how long until it stops running
        :return: (list(GameNode, float, int, int)) the list of solutions
        """
        depth = self.start_nod.cost
        next_depth = float('inf')
        max_mem = 0
        total_w = 0
        while True:

            opened = [self.start_nod]
            closed = []

            total_w = total_w + 1

            while len(opened) > 0:
                time1 = time.time()
                if time1 - start_time >= time_out:
                    return 'Timeout', time1 - start_time, max_mem, total_w

                curr = opened.pop(0)
                closed.append(curr)
                if self.is_final_nod(curr):
                    return curr, time1 - start_time, max_mem, total_w

                children = curr.give_children(self.game_map, heuristic)
                total_w = total_w + len(children)

                for nod in children:

                    if nod.estimate > depth:
                        next_depth = min(nod.estimate, next_depth)
                        continue

                    nod_open = node_with_same_info(opened, nod)
                    if nod_open is not None:
                        if nod_open.estimate > nod.estimate:
                            opened.remove(nod_open)
                            a_star_list_insert(opened, nod)
                        continue
                    nod_close = node_with_same_info(closed, nod)
                    if nod_close is not None:
                        if nod_close.estimate > nod.estimate:
                            closed.remove(nod_close)
                            a_star_list_insert(closed, nod)
                        continue
                    a_star_list_insert(opened, nod)
                max_mem = max(max_mem, len(opened) + len(closed))
            if next_depth == float('inf'):
                break
            depth = next_depth
            next_depth = float('inf')
        return None, time.time() - start_time, max_mem, total_w


def node_with_same_info(node_list, node):
    """
    checks if in the list there is a node with the same information
    :param node_list: (list(GameNode))
    :param node: (GameNode)
    :return: (Bool)
    """
    for nod in node_list:
        if nod.info == node.info:
            return nod
    return None


def a_star_list_insert(node_list, node):
    """
    inserts into the list a node according to what the a* algorithm requires
    :param node_list: (list(GameNode))
    :param node: (GameNode)
    :return: None
    """
    poz = 0
    while poz < len(node_list) and (node.estimate > node_list[poz].estimate or
                                    node.estimate == node_list[poz].estimate and node.cost > node_list[poz].cost):
        poz += 1
    node_list.insert(poz, node)
