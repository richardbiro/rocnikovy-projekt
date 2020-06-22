#Program spustite cez prikazovy riadok / terminal prikazom:
#python rocnikovy_projekt.py [typ vyhladavania] [dolna hranica] [horna hranica]
#Typ vyhladavania moze byt "bruteforce" (uplne) alebo "random" (nahodne)
#Ak si zvolite nahodne vyhladavanie, mozete si zvolit aj pocet opakovani (defaultne je to 10^7):
#python rocnikovy_projekt.py random [dolna hranica] [horna hranica] --iterations [pocet opakovani]

from argparse import ArgumentParser
from cProfile import runctx
from datetime import datetime
from math import gcd, isqrt
import matplotlib.pyplot as plt
from numpy import arange
from random import randint
from multiprocessing import cpu_count, Pool

#Meno suboru, do ktoreho zapisujeme magicke stvorce s 6 a viac stvorcami
file = str(datetime.now())
file = file[:file.index(".")]
file = file.replace(":", "-")
file = file + ".txt"

#Meno suboru, do ktoreho zapisujeme magicke stvorce s 7 a viac stvorcami
file_correct = str(datetime.now())
file_correct = file_correct[:file_correct.index(".")]
file_correct = file_correct.replace(":", "-")
file_correct = file_correct + " correct.txt"

solutions = dict()
correct_solutions = dict()
relatively_prime = []
labels = []
six_squares = []
seven_squares = []
cpu_used = cpu_count()

#Funkcia vezme pole cisel a vrati ich najmensieho spolocneho delitela
def gcd_array(array):
    if len(array) < 2:
        return None
    d = gcd(array[0], array[1])
    for i in range(2, len(array)): d = gcd(d, array[i])
    return d

#Funkcia overi, ci je dane cislo stvorec
def is_square(n):
    if n < 0:
        return False
    return isqrt(n)**2 == n

def get_pairs():
    return relatively_prime

#Funkcia inicializuje vsetky polia, do ktorych sa budu ukladat data urcene pre vysledny graf
def add_all_labels(upper_bound):
    for i in range(upper_bound+1):
        labels.append(i)
        six_squares.append(0)
        seven_squares.append(0)

#Funkcia hodi do pola vsetky dvojice nesudelitelnych cisel a utriedi podla maxima - vid cast 6
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

#Funkcia vrati jednoznacny retazec (identifikator) magickeho stvorca - vid cast 6 a vetu 6.1
def get_index(array):
    corners = [array[0], array[2], array[6], array[8]]
    corners.sort()
    corner1 = corners[0]
    corner2 = corners[1]
    center = array[4]
    return ' '.join(str(s) for s in [corner1, corner2, center])

#Funkcia prida a zapise dany magicky stvorec (ak este nebol najdeny) - vid cast 6
def add_solution(array, uv):
    u1 = uv[0]
    v1 = uv[1]
    u2 = uv[2]
    v2 = uv[3]
    squares = array[0]
    square = array[1]
    index = get_index(square)
    largest = max(u1, v1, u2, v2)

    if index not in solutions:
        with open(file, 'a') as f:
            f.write(str(str(squares) + " squares | u1 = " + str(u1) +
                        " | v1 = " + str(v1) + " | u2 = " + str(u2) +
                        " | v2 = " + str(v2) + " | " + str(square) + "\n"))
        solutions[index] = ' '.join(str(s) for s in [largest, squares])

        if squares == 6:
            six_squares[largest] += 1
        else:
            seven_squares[largest] += 1
            if index not in correct_solutions:
                correct_solutions[index] = [array, u1, v1, u2, v2]
                with open(file_correct, 'a') as f:
                    f.write(str(str(squares) + " squares | u1 = " + str(u1) +
                                " | v1 = " + str(v1) + " | u2 = " + str(u2) +
                                " | v2 = " + str(v2) + " | " + str(square) + "\n"))

#Funkcia da stvorec do normalneho tvaru (vykrati cleny a umocni ich na druhu) - vid cast 6
def normalize(array, divisor):
    for i in range(len(array)):
        array[i] = (array[i]//divisor)**2

#Funkcia vygeneruje vsetky stvorce pre dane u1,v1,u2,v2 a zapamata si vyhovujuce - vid cast 6
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

#Funkcia zarovna text na zadanu dlzku
def align(data, length):
    return (length - len(str(data)))*" " + str(data)

#Funkcia prevedie cas zo sekund na format hodiny:minuty:sekundy
def seconds_to_time(sec):
    answer = str(sec//3600) + "h "
    answer += str((sec%3600)//60) + "m "
    answer += str((sec%3600)%60) + "s"
    return answer

#Funkcia prejde paralelne vsetky konfiguracie v execute-liste
def execute_parallel(execute_list):
    global cpu_used
    start = datetime.now()
    p = Pool(cpu_used)
    results = p.map(run_configuration, execute_list)
    for i in range(len(results)):
        for S in results[i][0]:
            if S is not None:
                add_solution(S, results[i][1])
    p.close()
    p.join()
    end = datetime.now()
    return end - start

#Funkcia vypise priebeznu spravu (progress bar)
def update(completed, block, allsteps, diff):
    current = min(allsteps,completed*block)
    print(align(int(100*current/allsteps), 3), "% |", align(current, len(str(allsteps))),
          "out of", allsteps, "| estimated remaining time:",
          align(seconds_to_time(int(diff.seconds*(allsteps - current)/block)), 12)) 

#Funkcia prejde cez vsetky pary dvojic (u1,v1) a (u2,v2) - vid cast 6
def run_all_pairs(lower_bound):
    n = len(relatively_prime)
    low = 0
    while max(relatively_prime[low]) < lower_bound:
        low += 1
        
    allsteps = n*(n-1)//2 - low*(low-1)//2
    completed = 0
    execute_list = []
    block = 10**6
    
    print("START |", str(datetime.now()))
    for i1 in range(n):
        u1 = relatively_prime[i1][0]
        v1 = relatively_prime[i1][1]
        for i2 in range(max(low, i1+1), n):
            u2 = relatively_prime[i2][0]
            v2 = relatively_prime[i2][1]
            execute_list.append([u1, v1, u2, v2])
            if len(execute_list) > block or (i1 == n-2 and i2 == n-1):
                diff = execute_parallel(execute_list)
                execute_list = []
                completed += 1
                update(completed, block, allsteps, diff)          
    print("END |", str(datetime.now()), "\n")

#Funkcia prejde k-krat cez nahodne pary dvojic (u1,v1) a (u2,v2) - vid cast 6
def run_random_pairs(lower_bound, upper_bound, k):
    allsteps = k
    completed = 0
    execute_list = []
    block = 10**6
    
    print("\nSTART |", str(datetime.now()))
    for i in range(k):
        u1 = randint(1, upper_bound-1)
        v1 = randint(u1+1, upper_bound)
        u2 = randint(1, upper_bound-1)
        v2 = randint(max(max(v1, u2+1), lower_bound), upper_bound)
        execute_list.append([u1, v1, u2, v2])
        if len(execute_list) > block or i == k-1:
            diff = execute_parallel(execute_list)
            execute_list = []
            completed += 1
            update(completed, block, allsteps, diff)      
    print("END |", str(datetime.now()), "\n")

#Funkcia ukaze vysledny graf pocetnosti magickych stvorcov
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

#Funkcia spusti bruteforce vyhladavanie od lower_bound po upper_bound
def fixed_search(lower_bound, upper_bound):
    add_all_pairs(upper_bound)
    runctx('r(l)', {'r': run_all_pairs}, {'l': lower_bound})

#Funkcia spusti nahodne vyhladavanie od lower_bound po upper_bound s k opakovaniami
def random_search(lower_bound, upper_bound, k):
    runctx('r(l, u, k)', {'r': run_random_pairs}, {'l': lower_bound, 'u': upper_bound, 'k': k})           

def main():
    global cpu_used
    parser = ArgumentParser(description="search for a magic square within given bounds " +
                            "(maximum of u1,v1,u2,v2)")
    parser.add_argument("search", help="type of search (bruteforce or random)")
    parser.add_argument("lower_bound", help="lower bound for solutions", type=int)
    parser.add_argument("upper_bound", help="upper bound for solutions", type=int)
    parser.add_argument("--cpu", default = cpu_count(), help="number of cpu cores used (" +
                        str(cpu_count()) + " by default)", type=int)
    parser.add_argument("--iterations", default = 10**7, help="number of iterations in random " +
                        "search (10^7 by default)", type=int)
    
    args = parser.parse_args()
    args.lower_bound = abs(args.lower_bound)
    args.upper_bound = abs(args.upper_bound)
    
    if args.cpu < 1:
        args.cpu = 1
    elif args.cpu > cpu_count():
        args.cpu = cpu_count()

    cpu_used = args.cpu
    print("Search will use " + str(cpu_used) + " cpu cores (" + str(cpu_count()) + " available)\n")
    
    if args.lower_bound > args.upper_bound:
        print("Lower bound is higher than upper bound, so they will be swapped.\n")
        args.lower_bound, args.upper_bound = args.upper_bound, args.lower_bound

    add_all_labels(args.upper_bound)

    with open(file, 'w') as f:
        f.write("")

    with open(file_correct, 'w') as f:
        f.write("")

    if args.search == "bruteforce":
        fixed_search(args.lower_bound, args.upper_bound)
    elif args.search == "random":
        random_search(args.lower_bound, args.upper_bound, args.iterations)
    else:
        print("\nInvalid command: " + args.search + ".\n")
        return
    
    show_graph(args.lower_bound)

    print("\n" + str(len(solutions) - len(correct_solutions)), "solutions with six squares.\n")
    print(len(correct_solutions), "solutions with at least seven squares.")
    for i,j in correct_solutions.items():
        print(" ".join(map(str, j[0][1])))
        print("| u1 =", j[1],
              "| v1 =", j[2],
              "| u2 =", j[3],
              "| v2 =", j[4], "|\n")
    input("\nPress any key to end.")

if __name__ == '__main__':
    main()
