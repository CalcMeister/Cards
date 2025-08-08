import cards

'''
Two player game, the dumb one you played as an elementary schooler.
'''

name='War'
players=2
decks_per_game=1

def compare_war(card1, card2):
	'''
	In 'War', the highest card wins
	'''
	if card1.rank > card2.rank:
		return 1
	elif card1.rank < card2.rank:
		return 2
	else:
		return None

def simulate(starting_decks):
	# returns a dict with keys 'round' and 'winner'

	hands = starting_decks[0].deal(2)
	table = cards.Deck(empty=True)

	round_count = 0

	while min(map(len, hands)) > 0:
		# print('Hands:', hands[0], hands[1], sep='\n')
		round_count += 1
		# print(f'Round {round_count}')

		player_1_card = hands[0].draw()[0]
		player_2_card = hands[1].draw()[0]

		table += player_1_card + player_2_card

		# print(table)

		winner = compare_war(player_1_card, player_2_card)
		if winner is not None:
			# print(f'\tPlayer {winner} wins with {table[len(table)-3+winner]}')
			hands[winner-1] += table.draw_all().shuffled()

	if len(hands[0]) == 0:
		winner = 'p2'
	else:
		winner = 'p1'
	return {'round':round_count, 'winner':winner}

if __name__ == '__main__': # Simulate the game once if run directly
	print(simulate([cards.Deck().shuffled() for _ in range(decks_per_game)]))