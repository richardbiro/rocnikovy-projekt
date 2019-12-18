import math
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import random
import cProfile
from mpl_toolkits.mplot3d import Axes3D

solutions = dict()
correct_solutions = []
relatively_prime = []
labels = []
six_squares = []
seven_squares = []

def gcd_array(array):
    if len(array) < 2: return None
    d = math.gcd(array[0],array[1])
    for i in range(2,len(array)): d = math.gcd(d,array[i])
    return d


def is_square(n):
    if n < 0: return False
    return (int(math.sqrt(n))**2 == n)


def get_solutions():
    return solutions


def add_correct_solution(array,u1,v1,u2,v2):
    if [array,u1,v1,u2,v2] not in correct_solutions:
        correct_solutions.append([array,u1,v1,u2,v2])
        

def add_solution(array,u1,v1,u2,v2):
    different = len(set(array))

    if different == 9:
        squares = 0
        for i in array:
            if is_square(i): squares += 1

        if squares > 5:
            corners = [array[0],array[2],array[6],array[8]]
            corners.sort()
            corner1 = corners[0]
            corner2 = corners[1]
            center = array[4]
            
            index = ' '.join(str(s) for s in [corner1,corner2,center])
            largest = max(u1,v1,u2,v2)

            if index not in solutions or list(map(int,solutions[index].split(' ')))[0] > largest:
                solutions[index] = ' '.join(str(s) for s in [largest,squares])
                center = int(math.sqrt(center))

                if squares == 6: six_squares[largest] += 1
                        
                else:
                    seven_squares[largest] += 1
                    add_correct_solution(array,u1,v1,u2,v2)


def evaluate_rows(array):
    for i in range(3):
        for j in range(3):
            if array[3*i+j%3] != None and array[3*i+(j+1)%3] != None and array[3*i+(j+2)%3] == None:
                    array[3*i+(j+2)%3] = 3*array[4] - array[3*i+j%3] - array[3*i+(j+1)%3]


def evaluate_columns(array):
    for i in range(3):
        for j in range(3):
            if array[i+3*(j%3)] != None and array[i+3*((j+1)%3)] != None and array[i+3*((j+2)%3)] == None:
                array[i+3*((j+2)%3)] = 3*array[4] - array[i+3*(j%3)] - array[i+3*((j+1)%3)]



def evaluate_two_edges(array):
    for i in range(2):
        for j in range(2):
            if array[1+6*i] != None and array[3+2*j] != None:
                array[8-6*i-2*j] = (array[1+6*i] + array[3+2*j])//2


def evaluate_square(array):
    evaluate_rows(array)
    evaluate_columns(array)
    evaluate_two_edges(array)

    if None in array: return None
    return array



def normalize(array,divisor):
    for i in range(len(array)): array[i] = (array[i]//divisor)**2



def run_configuration(u1,v1,u2,v2):
    constants = [abs((u1**2 + v1**2)*(u2**2 + v2**2)),
                 abs((u1**2 + v1**2)*(u2**2 + 2*u2*v2 - v2**2)),
                 abs((u1**2 + v1**2)*(- u2**2 + 2*u2*v2 + v2**2)),
                 abs((u1**2 + 2*u1*v1 - v1**2)*(u2**2 + v2**2)),
                 abs((- u1**2 + 2*u1*v1 + v1**2)*(u2**2 + v2**2))]
    
    divisor = gcd_array(constants)
    normalize(constants,divisor)

    center = constants[0]
    x1 = constants[1]
    x2 = constants[2]
    y1 = constants[3]
    y2 = constants[4]
    squares = []

    squares.append(evaluate_square([x1,   y1,     None,
                                    None, center, None,
                                    None, y2,     x2]))

    squares.append(evaluate_square([x1,   y2,     None,
                                    None, center, None,
                                    None, y1,     x2]))

    squares.append(evaluate_square([x1,   None,   y1,
                                    None, center, None,
                                    y2,   None,   x2]))

    squares.append(evaluate_square([None, x1,     None,
                                    y1,   center, y2,
                                    None, x2,     None]))
    
    for i in squares:
        if i != None: add_solution(i,u1,v1,u2,v2)




def add_all_labels(upper_bound):
    for i in range(upper_bound+1):
        labels.append(i)
        six_squares.append(0)
        seven_squares.append(0)


def create_progress_bar():
    print("START |",str(datetime.now()))
    print("END |",str(datetime.now()),"\n")

    

def get_pairs():
    return relatively_prime


def add_all_pairs(upper_bound):
    add_all_labels(upper_bound)
    
    for i in range(1,upper_bound+1):
        for j in range(1,upper_bound+1):
            if math.gcd(i,j) == 1:
                relatively_prime.append([i,j])

    relatively_prime.sort()


def align(data,length):
    return (length - len(str(data)))*" " + str(data)



def seconds_to_time(sec):
    answer = str(sec//3600) + "h "
    answer += str((sec%3600)//60) + "m "
    answer += str((sec%3600)%60) + "s"
    return answer



def run_all_pairs():
    progress = 0
    
    n = len(relatively_prime)
    allsteps = n*(n-1)//2
    step = 0
    
    print("\nSTART |",str(datetime.now()))

    for i1 in range(n):
        u1 = relatively_prime[i1][0]
        v1 = relatively_prime[i1][1]
        for i2 in range(i1+1,n):
            u2 = relatively_prime[i2][0]
            v2 = relatively_prime[i2][1]
            run_configuration(u1,v1,u2,v2)
            step += 1
            if step/allsteps * 100 > progress:
                print(align(progress,3),"% |",align(step,len(str(allsteps))),"out of",allsteps,
                      "| estimated remaining time:",
                      align(seconds_to_time((allsteps-step)//9300),12))
                progress += 5
                
    print("END |",str(datetime.now()),"\n")
                



def show_graph():
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, six_squares, width, label='exactly 6 entries are squares')
    rects2 = ax.bar(x + width/2, seven_squares, width, label='at least 7 entries are squares')

    ax.set_xlabel('Maximum from u1, v1, u2, v2')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    fig.tight_layout()
    plt.show()




def random_relatively_prime(upper_bound):
    a = random.randint(1,upper_bound-1)
    b = random.randint(1,upper_bound-1)
    d = math.gcd(a,b)
    return [a//d,b//d]




def fixed_search(upper_bound):
    add_all_pairs(upper_bound)
    cProfile.run('run_all_pairs()')
    show_graph()



def random_search(upper_bound,k):
    add_all_labels(upper_bound)
    for _ in range(k):
        first_pair = random_relatively_prime(upper_bound)
        second_pair = random_relatively_prime(upper_bound)
        run_configuration(first_pair[0],first_pair[1],second_pair[0],second_pair[1])
        

    

def get_input(text,answers,error):
    while True:
        print(text)
        answer = input()
        if answer in answers: return answer
        print(error)
        



def get_int_input(text,error):
    while True:
        print(text)
        try:
            upper_bound = int(input())
            return upper_bound
        except ValueError: print(error)
        



def main():
    search_fixed = False
    search = get_input("Type 'bruteforce' to search all solutions.\n" +
                       "Type 'random' to search random solutions.\n" +
                       "Type 'advanced' to search solutions using simulated annealing.\n",
                       ["bruteforce","random","advanced"],"Invalid command.\n")

    upper_bound = get_int_input("\nChoose a positive integer - upper bound for solutions:\n" +
                                "Tip: bruteforce search for upper bound above 100 may run for a very long time.\n" +
                                "Tip: bruteforce search for upper bound above 200 is currently out of reach.",
                                "Invalid positive integer.\n")     

    if search == "bruteforce": fixed_search(upper_bound)

    elif search == "random": random_search(upper_bound,
        get_int_input("\nChoose a positive integer - number of iterations:","Invalid positive integer.\n"))
    

    print("")
    print(len(solutions) - len(correct_solutions),"solutions with six squares.")
    print(len(correct_solutions),"solutions with at least seven squares:")
    for i in correct_solutions:
        print(" ".join(map(str,i[0])))
        print("where u1 = " + str(i[1]) + ", v1 = " + str(i[2]) + ", u2 = " + str(i[3]) + ", v2 = " + str(i[4]))
    input("\nPress any key to end.")



if __name__ == '__main__':
    main()




