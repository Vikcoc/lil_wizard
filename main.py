from game_map import GameMap
from game_logic import GameLogic
import time

inputPath = input("Input path: ")
outputPath = input("Output path: ")
no_of_sol = int(input("No of sol: "))
time_out = float(input("Timeout: "))

input_name = [inputPath + 'input1.txt', inputPath + 'input2.txt', inputPath + 'input3.txt', inputPath + 'input4.txt']


def write_to_file(filepath, root_filename, solutions):
    """
    prints each solution into a separate file at the given folder with the given base file name
    :param filepath: (str) the path of the folder
    :param root_filename: (str) the base name of the outputs
    :param solutions: (list(GameNode, float, int, int)) the list of solutions with the final node in the solution,
                                                        total number of nodes created, and the maximum number of nodes
                                                        handled at one point
    :return: None
    """
    for i in range(len(solutions)):
        with open(filepath + root_filename + str(i) + '.txt', "w+") as g:
            g.write(f'Solution: {i}\nTime: {solutions[i][1]}\nMax in memory: {solutions[i][2]}\nTotal: {solutions[i][3]}\n')
            if solutions[i][0] is not None and not isinstance(solutions[i][0], str):
                g.write(f'Cost: {solutions[i][0].cost}\n')
                g.write(str(solutions[i][0]) + 'A iesit din pestera.')
            else:
                g.write(str(solutions[i][0]))
        g.close()


def ex(i):
    """
    reads the input, then calls each algorithm with the timestamp and prints the results
    :param i: (int) the count of the input in the list
    :return: None
    """
    with open(input_name[i], "r") as f:
        gme = GameMap(f)
    f.close()
    logic = GameLogic(gme)
    time0 = time.time()
    res = logic.ucs(no_of_sol, time0, time_out)
    write_to_file(outputPath, 'input' + str(i) + '_ucs', res)

    time0 = time.time()
    res = logic.a_star(no_of_sol, 0, time0, time_out)
    write_to_file(outputPath, 'input' + str(i) + '_a_star_banal', res)
    time0 = time.time()
    res = logic.a_star(no_of_sol, 1, time0, time_out)
    write_to_file(outputPath, 'input' + str(i) + '_a_star_normal1', res)
    time0 = time.time()
    res = logic.a_star(no_of_sol, 2, time0, time_out)
    write_to_file(outputPath, 'input' + str(i) + '_a_star_normal2', res)
    time0 = time.time()
    res = logic.a_star(no_of_sol, 3, time0, time_out)
    write_to_file(outputPath, 'input' + str(i) + '_a_star_wrong', res)

    time0 = time.time()
    res = logic.a_star_optimal(0, time0, time_out)
    write_to_file(outputPath, 'input' + str(i) + '_a_star_optimal_banal', [res])
    time0 = time.time()
    res = logic.a_star_optimal(1, time0, time_out)
    write_to_file(outputPath, 'input' + str(i) + '_a_star_optimal_normal1', [res])
    time0 = time.time()
    res = logic.a_star_optimal(2, time0, time_out)
    write_to_file(outputPath, 'input' + str(i) + '_a_star_optimal_normal2', [res])
    time0 = time.time()
    res = logic.a_star_optimal(3, time0, time_out)
    write_to_file(outputPath, 'input' + str(i) + '_a_star_optimal_wrong', [res])

    time0 = time.time()
    res = logic.ida_star(0, time0, time_out)
    write_to_file(outputPath, 'input' + str(i) + '_ida_star_banal', [res])
    time0 = time.time()
    res = logic.ida_star(1, time0, time_out)
    write_to_file(outputPath, 'input' + str(i) + '_ida_star_normal1', [res])
    time0 = time.time()
    res = logic.ida_star(2, time0, time_out)
    write_to_file(outputPath, 'input' + str(i) + '_ida_star_normal2', [res])
    time0 = time.time()
    res = logic.ida_star(3, time0, time_out)
    write_to_file(outputPath, 'input' + str(i) + '_ida_star_wrong', [res])


ex(0)
# ex(1) not possible because start point has a symbol and stone has a different one, so they cannot overlap
ex(2)
ex(3)
