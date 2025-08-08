# Cards
A simple module and simulation program for simulating large numbers of randomly-played card games from a set of initial states.

Use `game_template.py` as a template for programming the logic for additional card games. `your_game.simulate` should be a function that takes a list of card decks (`cards.Deck`) and returns a `dict` containing the results of your simulation, something like `{'round':28, 'winner':'p1'}`.

Use `simulate_games.py` to run many parallel simulations of games whose odds you would like to analyze. Results will be aggregated per-starting-deck as jsons in `./Results/`

War, Go Fish, Croup, Luck-Test, and Skill-Test are included for testing purposes.
