from player import *
from dealer import *
from polynomial import *

def delta(i, Xs, q):
    d = 1
    for j in Xs:
        if j != i:
            d = (d * (-j) * pow((i - j) % q, -1, q)) % q
    return int(d)

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
    
    with open('result.txt', 'w') as result:
        for n_players in range(1, n + 1):
            reconstructedSecret = ""
            for cipher in dealer.secret:
                print(f"Q = {dealer.q}, P = {dealer.p}, G = {dealer.g}")
                f = Polynomial(cipher, dealer.q, dealer.threshold)
                f.printPolynomial()

                curr_players = players[0:n_players]
                dealer.distributeShares(curr_players, f)
                dealer.distributeCommits(curr_players)

                for i in range(len(curr_players)):
                    curr_players[i].verify(dealer.g, dealer.p, dealer.threshold, f.coefficients)
                    print(f"Dealer = {dealer.commitments[i]}, Player{i + 1} = {curr_players[i].verification}")
                    if curr_players[i].verification == dealer.commitments[i]:
                        print(f"Player{i + 1} share is verified")
                reconstructedSecret += chr(reconstruct(curr_players, dealer.q))
            result.write(f"Reconstructed secret with {n_players} shares = {reconstructedSecret}\n")

if __name__ == "__main__":
    main()