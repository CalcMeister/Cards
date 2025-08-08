import cards

'''
Generic two-player card game using a single standard card deck.
'''

name='Template'
players=2
decks_per_game=1

def simulate(starting_decks):
	return {'results':'return results as a dict'}

if __name__ == '__main__': # Simulate the game once if run directly
	print(simulate([cards.Deck().shuffled() for _ in range(decks_per_game)]))