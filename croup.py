import cards
import random

'''
The three-player trick-taking game that my dad always wins.
'''

name='Croup'
players=3
decks_per_game=12

class Mode:
	def __init__(self, name, ordering_function, scoring_function):
		self.name = name
		self.order = ordering_function
		self.score = scoring_function

def order(card, lead_suit, trump_suit=None):
	suit = card.suit
	bonus = 0
	if suit == lead_suit:
		bonus += 13
	if trump_suit is not None and suit == trump_suit:
		bonus += 26

	return card.rank + bonus

def score_no_trump(tricks_taken:int, chooser:bool):
	if chooser:
		return tricks_taken - 8
	else:
		return tricks_taken - 4

def score_low(tricks_taken:int, chooser:bool):
	if chooser:
		return 4 - tricks_taken
	else:
		return 6 - tricks_taken

def legal_plays(hand, lead_suit):
	# In Croup, lead must be followed unless you are out of the led suit.
	if max(c.suit==lead_suit for c in hand): # If they still have cards of the suit
		return cards.Deck([c for c in hand if c.suit==lead_suit]) # All cards of the lead suit
	else:
		return hand


no_trump = Mode('No trump', order, score_no_trump)
pick_a_trump = Mode('Pick-a-trump', order, score_no_trump)
spades = Mode('Spades', order, score_no_trump)
low = Mode('Low', order, score_low)

def simulate(starting_decks):
	remaining_modes = [[no_trump, pick_a_trump, spades, low] for i in range(players)]
	score = [0 for _ in range(players)]

	for cycle in range(4):
		for chooser in range(players):
			deck = starting_decks.pop()
			hands = deck.deal(players, number_of_cards=48) # Deal hands

			#for hand in hands:
				#print(hand)

			croup = deck.draw(4) # Deal croup
			#print(croup)
			mode = remaining_modes[chooser].pop(random.randrange(len(remaining_modes[chooser]))) # Select game mode
			#print(f'Player {chooser} chooses {mode.name}')


			trump = None
			if mode is pick_a_trump: # If it's pick a trump... pick a trump
				trump = random.randrange(4)
			elif mode is spades:
				trump = 0

			taken_tricks = [0 for _ in range(players)]

			hands[chooser] = (hands[chooser]+croup).draw_random(16) # Choose and discard croup

			#print(f'Player {chooser} has chosen their hand.')
			#print(hands[chooser])
			#print(f'Player {chooser} leads.')

			lead = chooser
			for trick in range(16):
				table = cards.Deck(empty=True)
				player_order = [(i+lead)%3 for i in [0,1,2]] # 'Clockwise' from lead
				table.append(hands[player_order[0]].draw_random()) # Leader leads
				table.append(hands[player_order[1]].draw_random(from_subdeck=legal_plays(hands[player_order[1]],table[0].suit))) # second player follows
				table.append(hands[player_order[2]].draw_random(from_subdeck=legal_plays(hands[player_order[2]],table[0].suit))) # then third

				ordering_key = lambda card: order(card, table[0].suit, trump)
				#print(table)

				winning_card = max(table, key=ordering_key) # Determine winning card
				winning_player = player_order[table.index(winning_card)] # Determine trick winner
				taken_tricks[winning_player] += 1 # Tally trick

				# print(f'Player {winning_player} wins trick with {winning_card}', end='')
				# if trick == 15:
				# 	print('.')
				# else:
				# 	print(' and leads.')

				lead = winning_player # Winner leads next trick

			for player in range(players):
				score[player] += mode.score(taken_tricks[player], chooser==player)

			# print(f'New score: {score}')

	return {f'p{p+1}':score[p] for p in range(players)} | {'winner':f'p{score.index(max(score))}'}



if __name__ == '__main__': # Simulate the game once if run directly
	print(simulate([cards.Deck().shuffled() for _ in range(decks_per_game)]))