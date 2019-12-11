import math
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import random
import cProfile



solutions = dict()
correct_solutions = []
relatively_prime = []
labels = []
six_squares = []
seven_squares = []

def gcd_array(X):
    if len(X) < 2: return None
    d = math.gcd(X[0],X[1])
    for i in range(2,len(X)): d = math.gcd(d,X[i])
    return d


def is_square(n):
    if n < 0: return False
    return (int(math.sqrt(n))**2 == n)


def get_solutions():
    return solutions


def add_correct_solution(X,u1,v1,u2,v2):
    if [X,u1,v1,u2,v2] not in correct_solutions:
        correct_solutions.append([X,u1,v1,u2,v2])
        

def add_solution(X,u1,v1,u2,v2):
    different = len(set(X))

    if different == 9:
        squares = 0
        for i in X:
            if is_square(i): squares += 1

        if squares > 5:
            corners = [X[0],X[2],X[6],X[8]]
            corners.sort()
            corner1 = corners[0]
            corner2 = corners[1]
            center = X[4]
            
            index = ' '.join(str(s) for s in [corner1,corner2,center])
            largest = max(u1,v1,u2,v2)

            if index not in solutions or list(map(int,solutions[index].split(' ')))[0] > largest:
                solutions[index] = ' '.join(str(s) for s in [max(u1,v1,u2,v2),squares])

                if squares == 6: six_squares[largest] += 1
                else:
                    seven_squares[largest] += 1
                    add_correct_solution(X,u1,v1,u2,v2)



def run_configuration(u1,v1,u2,v2):
    E = abs((u1**2 + v1**2)*(u2**2 + v2**2))
    A = abs((u1**2 + v1**2)*(u2**2 + 2*u2*v2 - v2**2))
    B = abs((u1**2 + 2*u1*v1 - v1**2)*(u2**2 + v2**2))
    H = abs((- u1**2 + 2*u1*v1 + v1**2)*(u2**2 + v2**2))
    I = abs((u1**2 + v1**2)*(- u2**2 + 2*u2*v2 + v2**2))

    divisor = gcd_array([A,B,E,H,I])
    E = (E//divisor)**2
    A = (A//divisor)**2
    B = (B//divisor)**2
    H = (H//divisor)**2
    I = (I//divisor)**2
    C = 3*E - A - B
    G = 3*E - H - I
    D = 3*E - A - G
    F = 3*E - C - I
    add_solution([A,B,C,D,E,F,G,H,I],u1,v1,u2,v2)



    E = abs((u1**2 + v1**2)*(u2**2 + v2**2))
    A = abs((u1**2 + v1**2)*(u2**2 + 2*u2*v2 - v2**2))
    H = abs((u1**2 + 2*u1*v1 - v1**2)*(u2**2 + v2**2))
    B = abs((- u1**2 + 2*u1*v1 + v1**2)*(u2**2 + v2**2))
    I = abs((u1**2 + v1**2)*(- u2**2 + 2*u2*v2 + v2**2))

    divisor = gcd_array([A,B,E,H,I])
    E = (E//divisor)**2
    A = (A//divisor)**2
    B = (B//divisor)**2
    H = (H//divisor)**2
    I = (I//divisor)**2
    C = 3*E - A - B
    G = 3*E - H - I
    D = 3*E - A - G
    F = 3*E - C - I
    add_solution([A,B,C,D,E,F,G,H,I],u1,v1,u2,v2)



    E = abs((u1**2 + v1**2)*(u2**2 + v2**2))
    A = abs((u1**2 + v1**2)*(u2**2 + 2*u2*v2 - v2**2))
    C = abs((u1**2 + 2*u1*v1 - v1**2)*(u2**2 + v2**2))
    G = abs((- u1**2 + 2*u1*v1 + v1**2)*(u2**2 + v2**2))
    I = abs((u1**2 + v1**2)*(- u2**2 + 2*u2*v2 + v2**2))

    divisor = gcd_array([A,C,E,G,I])
    E = (E//divisor)**2
    A = (A//divisor)**2
    C = (C//divisor)**2
    G = (G//divisor)**2
    I = (I//divisor)**2
    B = 3*E - A - C
    D = 3*E - A - G
    F = 3*E - C - I
    H = 3*E - G - I
    add_solution([A,B,C,D,E,F,G,H,I],u1,v1,u2,v2)




    E = abs((u1**2 + v1**2)*(u2**2 + v2**2))
    B = abs((u1**2 + v1**2)*(u2**2 + 2*u2*v2 - v2**2))
    D = abs((u1**2 + 2*u1*v1 - v1**2)*(u2**2 + v2**2))
    F = abs((- u1**2 + 2*u1*v1 + v1**2)*(u2**2 + v2**2))
    H = abs((u1**2 + v1**2)*(- u2**2 + 2*u2*v2 + v2**2))

    divisor = gcd_array([B,D,E,F,H])
    E = (E//divisor)**2
    B = (B//divisor)**2
    D = (D//divisor)**2
    F = (F//divisor)**2
    H = (H//divisor)**2
    A = (F + H)//2
    C = (D + H)//2
    G = (B + F)//2
    I = (B + D)//2
    add_solution([A,B,C,D,E,F,G,H,I],u1,v1,u2,v2)


def add_all_labels(upper_bound):
    for i in range(upper_bound+1):
        labels.append(i)
        six_squares.append(0)
        seven_squares.append(0)


def get_pairs():
    return relatively_prime


def add_all_pairs(upper_bound):
    add_all_labels(upper_bound)
    
    for i in range(1,upper_bound+1):
        for j in range(1,upper_bound+1):
            if math.gcd(i,j) == 1:
                relatively_prime.append([i,j])

    relatively_prime.sort()





def run_all_pairs():
    progress = 0
    
    n = len(relatively_prime)
    allsteps = n*(n-1)//2
    step = 0
    
    print("START |",str(datetime.now()))

    for i1 in range(n):
        u1 = relatively_prime[i1][0]
        v1 = relatively_prime[i1][1]
        for i2 in range(i1+1,n):
            u2 = relatively_prime[i2][0]
            v2 = relatively_prime[i2][1]
            run_configuration(u1,v1,u2,v2)
            step += 1
            if step/allsteps * 100 > progress:
                print(progress,"% |",step,"out of",allsteps)
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



def random_search(upper_bound,k):
    add_all_labels(upper_bound)
    for _ in range(k):
        first_pair = random_relatively_prime(upper_bound)
        second_pair = random_relatively_prime(upper_bound)
        run_configuration(first_pair[0],first_pair[1],second_pair[0],second_pair[1])
    


def main():
    
    while True:
        print("Type 'fixed' to search all solutions.")
        print("Type 'random' to search random solutions.")
        answer = input()
        if answer == "fixed":
            search_fixed = True
            break
        
        elif answer == "random":
            search_fixed = False
            break
        
        else: print("Invalid command:",answer,"\n")
            
    
    while True:
        try:
            print("\nChoose a positive integer - upper bound for solutions:")
            print("Tip: fixed search for upper bound above 70 may run for a very long time.")
            print("Tip: fixed search for upper bound above 200 is currently out of reach.")
                
            answer = input()
            upper_bound = int(answer)
            break
        
        except ValueError: print("Invalid positive integer",answer)
        

    if search_fixed:
        add_all_pairs(upper_bound)
        cProfile.run('run_all_pairs()')
        show_graph()

    else:
        while True:
            try:
                print("\nChoose a positive integer - number of iterations:")      
                answer = input()
                k = int(answer)
                break
        
            except ValueError: print("Invalid positive integer",answer)
     
        random_search(upper_bound,k)

    print("")
    print(len(solutions) - len(correct_solutions),"solutions with six squares were found.")
    print(len(correct_solutions),"solutions with at least seven squares were found.")
    for i in correct_solutions: print(i)




if __name__ == '__main__':
    main()




