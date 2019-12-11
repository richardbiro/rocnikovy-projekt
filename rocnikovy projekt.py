import math
import numpy as np
import matplotlib.pyplot as plt

def gcd(a,b):
    if a*b*(a-b) == 0: return max(a,b)
    return gcd(max(a,b)%min(a,b),min(a,b))

def gcd_array(X):
    d = gcd(X[0],X[1])
    for i in range(2,len(X)): d = gcd(d,X[i])
    return d

def lcm(a,b): return a*b//gcd(a,b)

def lcm_array(X):
    m = lcm(X[0],X[1])
    for i in range(2,len(X)): m = lcm(m,X[i])
    return m

def isSquare(n):
    return (math.sqrt(n)**2 == n)



already_known = 1
want_to_know = 125
solutions_abcdeghi = dict()
solutions_xxexx = dict()
all_solutions_xxexx = []

relatively_prime = []
labels = []
six_squares = []
seven_squares = []

for i in range(already_known, want_to_know+1):
    labels.append(i-1)
    six_squares.append(0)
    seven_squares.append(0)
    if i < want_to_know:
        for j in range(already_known+1,want_to_know):
            if gcd(i,j) == 1:
                relatively_prime.append([i,j])

relatively_prime.sort()



def add_solution_xxexx(X,u1,v1,u2,v2):
    different = len(set(X))

    if different == 9:
        squares = 0
        for i in X:
            if isSquare(i): squares += 1

        if squares > 5:
            index = ' '.join(str(s) for s in [min(X[0],X[2],X[6],X[8]),min(X[1],X[3],X[5],X[7]),X[4]])

            if index not in solutions_xxexx or list(map(int,solutions_xxexx[index].split(' ')))[0] > max(u1,v1,u2,v2):
                solutions_xxexx[index] = ' '.join(str(s) for s in [max(u1,v1,u2,v2),squares])

                if squares == 6: six_squares[max(u1,v1,u2,v2)] += 1
                else: seven_squares[max(u1,v1,u2,v2)] += 1
                             
                    




def run_configuration_xxexx(u1,v1,u2,v2):
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
    add_solution_xxexx([A,B,C,D,E,F,G,H,I],u1,v1,u2,v2)



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
    add_solution_xxexx([A,B,C,D,E,F,G,H,I],u1,v1,u2,v2)




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
    add_solution_xxexx([A,B,C,D,E,F,G,H,I],u1,v1,u2,v2)

    
        
progress = 10
n = len(relatively_prime)

print("PROCESSING",n)

for i1 in range(n):
    print(i1,"out of",n)
    u1 = relatively_prime[i1][0]
    v1 = relatively_prime[i1][1]
    for i2 in range(i1+1,n):
        u2 = relatively_prime[i2][0]
        v2 = relatively_prime[i2][1]
        run_configuration_xxexx(u1,v1,u2,v2)
##        for i3 in range(i2+1,len(relatively_prime)):
##            u3 = relatively_prime[i3][0]
##            v3 = relatively_prime[i3][1]
##            run_configuration_abdefhi(u1,v1,u2,v2,u3,v3)



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




