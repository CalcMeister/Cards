import cards
import json, pprint
import numpy as np
import war, croup, go_fish, luck_test, skill_test # Games, reference game_template.py to add more
from multiprocessing import Pool
from collections import Counter


number_of_states = 100 # Number of deck shuffles to simulate
sims_per_state = 1000 # Number of games to simulate per shuffle
games_to_simulate = [luck_test, skill_test, war, croup] # List of games to simulate

def result_stats(ranks):
	t = type(ranks[0])
	n = len(ranks)
	if t in (int, float):
		mean = float(np.mean(ranks))
		median = float(np.median(ranks))
		std = float(np.std(ranks))
		n_range = (float(np.min(ranks)), float(np.max(ranks)))

		return {'mean':mean, 'median':median, 'std':std, 'range':n_range}

	elif t in (str, bool):
		counter = Counter(ranks)
		fractional_frequency = {k:v/n for k,v in counter.items()}

		return fractional_frequency

	elif t == dict:
		return combine_results(ranks)

	elif t == tuple:
		if len(ranks[0]) == 2:
			return (min(i[0] for i in ranks), max(i[1] for i in ranks))
		else:
			return f'Cannot combine: unknown tuple format'

	else:
		return f'Cannot combine type: {t}'

def combine_results(results):
	# take a look at r.get(key, 0) later
	return {key:result_stats([r.get(key, 0) for r in results]) for key in results[0]}

if __name__ == '__main__':
	for game in games_to_simulate:
		print(f'Simulating {sims_per_state} games of {game.name} per each of {number_of_states} initial states.')

		initial_states = [cards.Deck().shuffled() for _ in range(number_of_states)]
		result_averages = []


		for i in range(number_of_states):
			print(f'State {i}: ', end='')
			deck = initial_states[i].copy()

			with Pool() as p:
				decks = [[deck.copy() for _ in range(game.decks_per_game)] for _ in range(sims_per_state)]
				games = p.map(game.simulate, decks) # use mp.Pool() to execute a simulation on each deck simultaneously
		
				if not isinstance(games[0], dict):
					raise TypeError('Game simulation functions must return a dict of results.')

				result_average = combine_results(games) | {'simulations':sims_per_state}
				result_averages.append(result_average)
				print(result_average)

		results_filename = f'Results/{game.name.replace(' ', '_')}_results.json'
		with open(results_filename, 'w') as f:
			out = json.dumps(result_averages)
			f.write(out)

		print(f'{game.name} simulation results saved to ./{results_filename}')

		pprint.pp(combine_results(result_averages))








