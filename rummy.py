import cards

'''
Generic game of Rummy.
UNFINISHED
'''

name='Rummy'
players=2
decks_per_game=1

def simulate(starting_decks):
	deck = starting_decks[0]
	hands = deck.deal(2, number_of_cards=CARDS_PER_HAND*2) # Deal cards
	discard = deck.draw() # Start discard pile





	return {'results':'return results as a dict'}

if __name__ == '__main__': # Simulate the game once if run directly
	print(simulate([cards.Deck().shuffled() for _ in range(decks_per_game)]))