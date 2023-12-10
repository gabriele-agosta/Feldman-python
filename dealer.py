import math
import random

class Dealer:

    def __init__(self, threshold):
        self.threshold = threshold
        self.secret = None
        self.q = None
        self.p = None
        self.r = None
        self.g = None
        self.commitments = None

    def chooseSecret(self):
        secret = int(input("Insert your secret: "))
        self.secret = secret

    def chooseQ(self):
        self.q = 127

    def chooseP(self):
        r = 1
        while True:
            p = r*self.q + 1
            if self._isPrime(p):
                break
            r = r + 1
        self.p, self.r = p, r
    
    def chooseGenerator(self):
        Z_p_star = []
        for i in range(0, self.p):
            if(math.gcd(i, self.p) == 1):
                Z_p_star.append(i)
        
        G = [] 
        for i in Z_p_star:
            G.append(i**self.r % self.p)

        G = list(set(G))
        G.sort()    

        g = random.choice(list(filter(lambda g: g != 1, G)))

        self.g = g
    
    def distributeShares(self, players, f):
        for player in players:
            player.y = f.computePolynomial(player.x, self.q)

    def distributeCommits(self, players):
        commitments = []
        for player in players:
            commitments.append((self.g ** player.y) % self.p)
        self.commitments = commitments

    def _isPrime(self, n):
        if n == 2:
            return True
        if n == 1 or n % 2 == 0:
            return False    
        i = 3    
        while i <= math.sqrt(n):
            if n % i == 0:
                return False
            i = i + 2        
        return True