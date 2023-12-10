class Player:
    def __init__(self, x):
        self.x = x
        self.y = None
        self.verification = None
    
    def verify(self, generator, p, threshold, coefficients):
        res = 1
        for i in range(threshold):
            res *= (generator ** coefficients[i]) ** (self.x ** i)
        self.verification = res % p
        
