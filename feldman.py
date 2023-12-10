from player import *
from dealer import *
from polynomial import *

def delta(i, Xs, q):
    d = 1
    for j in Xs:
        if j != i:
            d *= -j / (i - j)
    return int(d % q)

def reconstruct(players, q):
    secretReconstructed = 0
    Xs = [player.x for player in players]
    for player in players:
        secretReconstructed += delta(player.x, Xs, q) * player.y
    return secretReconstructed % q

def main():
    threshold = int(input("Choose the threshold: "))
    dealer = Dealer(threshold)

    dealer.chooseSecret()
    dealer.chooseQ()
    dealer.chooseP()
    dealer.chooseGenerator()

    n = int(input("Choose the number of players: "))
    players = [Player(i) for i in range(1, n + 1)]
    reconstructedSecret = ""
    
    for cipher in dealer.secret:
        print(f"Q = {dealer.q}, P = {dealer.p}, G = {dealer.g}")
        f = Polynomial(cipher, dealer.q, dealer.threshold)
        f.printPolynomial()

        dealer.distributeShares(players, f)
        dealer.distributeCommits(players)

        for i in range(len(players)):
            players[i].verify(dealer.g, dealer.p, dealer.threshold, f.coefficients)
            print(f"Dealer = {dealer.commitments[i]}, Player{i + 1} = {players[i].verification}")
            if players[i].verification == dealer.commitments[i]:
                print(f"Player{i + 1} share is verified")
        reconstructedSecret += chr(reconstruct(players, dealer.q))
        
    print(f"Reconstructed secret = {reconstructedSecret}")

if __name__ == "__main__":
    main()