import cards
import random
from collections import Counter

'''
Go fish!
'''

name='Go Fish'
players=2
decks_per_game=1

CARDS_PER_HAND = 7

def simulate(starting_decks):
	deck = starting_decks[0]
	hands = deck.deal(2, number_of_cards=CARDS_PER_HAND*2) # Deal cards
	books = [cards.Deck(empty=True) for _ in range(players)] # Initialize completed books
	turn_count = 0

	while min(map(len, hands)) > 0:
		for turn in range(players):
			turn_count += 1
			# print('Hands:')
			# for hand in hands:
			# 	print(hand)
			# print(f'Player {turn}\'s turn.')

			rank_request = random.choice(hands[turn].ranks()) # Rank to ask from another player
			player_to_request = random.choice([i for i in range(players) if i != turn]) # Player to ask
			# print(f'\'Does Player {player_to_request} have any {cards.RANK_NAMES[rank_request]}s?\'')

			if rank_request in hands[player_to_request].ranks(): # If that player has cards of that rank
				hands[turn] += hands[player_to_request].draw_selection([c for c in hands[player_to_request] if c.rank == rank_request]) # Give player all of that rank
				# print(f'Player {turn} gains Player {player_to_request}\'s {cards.RANK_NAMES[rank_request]}s.', hands[turn], sep='\n')
			else:
				hands[player_to_request] += deck.draw() # Go fish!
				# print(f'Player {player_to_request} goes fish!', hands[player_to_request], sep='\n')

			for p in range(players):
				ranks = Counter([c.rank for c in hands[p]])
				completed_ranks = [r for r in ranks if ranks[r] == 4] # List of completed ranks
				books[p] += hands[p].draw_selection([c for c in hands[p] if c.rank in completed_ranks]) # Remove completed ranks
				# for r in completed_ranks:
				# 	print(f'Player {p} completes a book of {cards.RANK_NAMES[rank_request]}s.')

			if min(map(len, hands)) == 0:
				break

		winners = [i[0] for i in enumerate(hands) if len(i[1]) == 0]
		if len(winners) == 1:
			winner = f'p{winners[0]}'
		else:
			winner = 'tie'

	return {'turns':turn_count, 'winner':winner}



if __name__ == '__main__': # Simulate the game once if run directly
	print(simulate([cards.Deck().shuffled() for _ in range(decks_per_game)]))