import cards

'''
The outcome of this game is entirely determined by the initial deck.
'''

name='Pure-Luck'
players=2
decks_per_game=1

def simulate(starting_decks):
	winner = {True:'p1', False:'p2'}[starting_decks[0][0].suit in (0,1)]
	return {'winner':winner}

if __name__ == '__main__': # Simulate the game once if run directly
	print(simulate([cards.Deck().shuffled() for _ in range(decks_per_game)]))