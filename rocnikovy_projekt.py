from cProfile import runctx
from datetime import datetime
from math import gcd, isqrt
import matplotlib.pyplot as plt
from numpy import arange
from random import randint
from multiprocessing import Pool
from itertools import combinations

file = str(datetime.now())
file = file[:file.index(".")]
file = file.replace(":", "-")
file = file + ".txt"

solutions = dict()
correct_solutions = []
relatively_prime = []
labels = []
six_squares = []
seven_squares = []

def gcd_array(array):
    if len(array) < 2:
        return None
    d = gcd(array[0], array[1])
    for i in range(2, len(array)): d = gcd(d, array[i])
    return d

def is_square(n):
    if n < 0:
        return False
    return isqrt(n)**2 == n

def get_pairs():
    return relatively_prime

def add_all_labels(upper_bound):
    for i in range(upper_bound+1):
        labels.append(i)
        six_squares.append(0)
        seven_squares.append(0)
        
def add_all_pairs(upper_bound):
    for i in range(1, upper_bound+1):
        for j in range(i, upper_bound+1):
            if gcd(i, j) == 1:
                relatively_prime.append([max(i, j), i, j])
    relatively_prime.sort()
    for i in range(len(relatively_prime)):
        relatively_prime[i].pop(0)

def get_solutions():
    return solutions

def get_index(array):
    corners = [array[0], array[2], array[6], array[8]]
    corners.sort()
    corner1 = corners[0]
    corner2 = corners[1]
    center = array[4]
    return ' '.join(str(s) for s in [corner1, corner2, center])

def add_solution(array, uv):
    global buffer
    u1 = uv[0]
    v1 = uv[1]
    u2 = uv[2]
    v2 = uv[3]
    squares = array[0]
    square = array[1]
    index = get_index(square)
    largest = max(u1, v1, u2, v2)

    if (index not in solutions or
            list(map(int, solutions[index].split(' ')))[0] > largest):
        with open(file, 'a') as f:
            f.write(str(str(squares) + " squares | u1 = " + str(u1) +
                        " | v1 = " + str(v1) + " | u2 = " + str(u2) +
                        " | v2 = " + str(v2) + " | " + str(square) + "\n"))
        solutions[index] = ' '.join(str(s) for s in [largest, squares])

        if squares == 6:
            six_squares[largest] += 1
        else:
            seven_squares[largest] += 1
            if [array, u1, v1, u2, v2] not in correct_solutions:
                correct_solutions.append([array, u1, v1, u2, v2])

def normalize(array, divisor):
    for i in range(len(array)):
        array[i] = (array[i]//divisor)**2

def run_configuration(uv):
    u1 = uv[0]
    v1 = uv[1]
    u2 = uv[2]
    v2 = uv[3]
    constants = [abs((u1**2 + v1**2)*(u2**2 + v2**2)),
                 abs((u1**2 + v1**2)*(u2**2 + 2*u2*v2 - v2**2)),
                 abs((u1**2 + v1**2)*(- u2**2 + 2*u2*v2 + v2**2)),
                 abs((u1**2 + 2*u1*v1 - v1**2)*(u2**2 + v2**2)),
                 abs((- u1**2 + 2*u1*v1 + v1**2)*(u2**2 + v2**2))]
    divisor = gcd_array(constants)
    normalize(constants, divisor)

    center = constants[0]
    x1 = constants[1]
    x2 = constants[2]
    y1 = constants[3]
    y2 = constants[4]
    squares = []
    squares.append([x1, y1, 3*center - x1 - y1,
                    x2 + y2 - x1, center, x1 + y1 - x2,
                    3*center - x2 - y2, y2, x2])

    squares.append([x1, y2, 3*center - x1 - y2,
                    y1 + x2 - x1, center, x1 + y2 - x2,
                    3*center - y1 - x2, y1, x2])

    squares.append([x1, 3*center - x1 - y1, y1,
                    3*center - x1 - y2, center, 3*center - y1 - x2,
                    y2, 3*center - x2 - y2, x2])

    if x1%2 == y1%2 == x2%2 == y2%2:
        squares.append([(x2 + y2)//2, x1, (x2 + y1)//2,
                        y1, center, y2,
                        (x1 + y2)//2, x2, (x1 + y1)//2])
    else:
        squares.append([x2 + y2, 2*x1, x2 + y1,
                        2*y1, 2*center, 2*y2,
                        x1 + y2, 2*x2, x1 + y1])
    answers = []
    for S in squares:
        if len(set(S)) < 9:
            answers.append(None)
        else:
            counter = 0
            for i in S:
                if is_square(i):
                    counter += 1
            if counter <= 5:
                answers.append(None)
            else:
                answers.append([counter, S])
    return [answers, [u1, v1, u2, v2]]

def align(data, length):
    return (length - len(str(data)))*" " + str(data)

def seconds_to_time(sec):
    answer = str(sec//3600) + "h "
    answer += str((sec%3600)//60) + "m "
    answer += str((sec%3600)%60) + "s"
    return answer

def run_all_pairs(lower_bound):
    n = len(relatively_prime)
    low = 0
    while max(relatively_prime[low]) < lower_bound:
        low += 1
    allsteps = n*(n-1)//2 - low*(low-1)//2
    execute_list = []
    block = 10**6
    blocks = allsteps//block + 1
    completed = 0
    print("\nSTART |", str(datetime.now()))

    for i1 in range(n):
        u1 = relatively_prime[i1][0]
        v1 = relatively_prime[i1][1]
        for i2 in range(max(low, i1+1), n):
            u2 = relatively_prime[i2][0]
            v2 = relatively_prime[i2][1]
            execute_list.append([u1, v1, u2, v2])
            if len(execute_list) > block or (i1 == n-2 and i2 == n-1):
                start = datetime.now()
                p = Pool()
                results = p.map(run_configuration, execute_list)
                for i in range(len(results)):
                    for S in results[i][0]:
                        if S is not None:
                            add_solution(S, results[i][1])
                p.close()
                p.join()
                execute_list = []
                completed += 1
                end = datetime.now()
                diff = end - start
                print(align(int(100*(completed*block)/allsteps), 3), "% |",
                      align(completed*block, len(str(allsteps))), "out of", allsteps,
                      "| estimated remaining time:", align(seconds_to_time(
                          int(diff.seconds*(allsteps - completed*block)/block)), 12))    
    print("END |", str(datetime.now()), "\n")

def show_graph(lower_bound):
    x = arange(len(labels[lower_bound:]))
    width = 0.35

    fig, ax = plt.subplots()
    ax.bar(x - width/2, six_squares[lower_bound:], width, label='exactly 6 entries are squares')
    ax.bar(x + width/2, seven_squares[lower_bound:], width, label='at least 7 entries are squares')

    ax.set_xlabel('Maximum from u1, v1, u2, v2')
    ax.set_xticks(x)
    ax.set_xticklabels(labels[lower_bound:])
    ax.legend()

    fig.tight_layout()
    plt.show()

def random_relatively_prime(lower_bound, upper_bound):
    first = randint(lower_bound, upper_bound-1)
    second = randint(lower_bound, upper_bound-1)
    divisor = gcd(first, second)
    return [first//divisor, second//divisor]

def fixed_search(lower_bound, upper_bound):
    add_all_pairs(upper_bound)
    runctx('r(l)', {'r': run_all_pairs}, {'l': lower_bound})
    
def random_search(lower_bound, upper_bound, k):
    for _ in range(k):
        first_pair = random_relatively_prime(lower_bound, upper_bound)
        second_pair = random_relatively_prime(lower_bound, upper_bound)
        result = run_configuration(first_pair + second_pair)
        for S in result[0]:
            if S is not None:
                add_solution(S, result[1])

def get_input(text, answers, error):
    while True:
        print(text)
        answer = input()
        if answer in answers:
            return answer
        print(error)

def get_int_input(text, error):
    while True:
        print(text)
        try:
            value = int(input())
            return value
        except ValueError:
            print(error)

def main():
    search = get_input("Type 'bruteforce' to search all solutions.\n" +
                       "Type 'random' to search random solutions.\n",
                       ["bruteforce", "random"], "Invalid command.\n")

    lower_bound = get_int_input("\nChoose a positive integer - lower bound for solutions:",
                                "Invalid positive integer.\n")

    upper_bound = get_int_input("\nChoose a positive integer - upper bound for solutions:\n" +
                                "Tip: bruteforce search for upper bound > 300 may take long.\n" +
                                "Tip: bruteforce search for upper bound > 600 is out of reach.",
                                "Invalid positive integer.\n")

    if lower_bound > upper_bound:
        print("\nLower bound is higher than upper bound, so they will be swapped.\n")
        lower_bound, upper_bound = upper_bound, lower_bound

    add_all_labels(upper_bound)

    with open(file, 'w') as f:
        f.write("")

    if search == "bruteforce":
        fixed_search(lower_bound, upper_bound)
    elif search == "random":
        random_search(lower_bound, upper_bound,
                      get_int_input("\nChoose a positive integer - number of iterations:",
                                    "Invalid positive integer.\n"))
    show_graph(lower_bound)

    print("\n" + str(len(solutions) - len(correct_solutions)), "solutions with six squares.\n")
    print(len(correct_solutions), "solutions with at least seven squares.")
    for i in correct_solutions:
        print(" ".join(map(str, i[0][1])))
        print("| u1 =", i[1],
              "| v1 =", i[2],
              "| u2 =", i[3],
              "| v2 =", i[4], "|\n")
    input("\nPress any key to end.")

if __name__ == '__main__':
    main()




