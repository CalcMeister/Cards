import cards
import random

'''
The outcome of this game is not affected by the initial deck.
'''

name='Pure-Skill'
players=2
decks_per_game=0

def simulate(starting_decks):
	return {'winner':f'p{random.randrange(players)}'}

if __name__ == '__main__': # Simulate the game once if run directly
	print(simulate([cards.Deck().shuffled() for _ in range(decks_per_game)]))