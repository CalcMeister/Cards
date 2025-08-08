import cards

'''
Klondike solitaire.
UNFINISHED
'''

name='Solitaire'
players=1
decks_per_game=1

def simulate(starting_decks):
	deck = starting_decks[0]
	piles = [cards.Deck(empty=True) for _ in range(7)]
	for i in range(7):
		for p in range(7-i):
			piles[p] += deck.draw()

	for p in piles:
		print(p)

	# moves = [None]
	# while len(moves) > 0:
	# 	pass


	return {'results':'return results as a dict'}

if __name__ == '__main__': # Simulate the game once if run directly
	print(simulate([cards.Deck().shuffled() for _ in range(decks_per_game)]))