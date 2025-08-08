import random
import colored
from functools import total_ordering

SUIT_NAMES = {
	0:'spade',
	1:'diamond',
	2:'club',
	3:'heart'
}

# ♠♥♦♣♤♡♢♧
SUIT_CHARS = {
	0:'♠',
	1:'♦',
	2:'♣',
	3:'♥'
}

SUIT_COLORS = {
	0:'BLACK',
	1:'RED',
	2:'BLACK',
	3:'RED'
}

COLOR_CHARS = {
	'BLACK':colored.Back.WHITE+colored.Fore.BLACK,
	'RED':colored.Back.WHITE+colored.Fore.RED,
	'BLUE':colored.Back.WHITE+colored.Fore.BLUE,
	'RESET':colored.Style.RESET
}

RANK_NAMES = {
	1:'ace',
	2:'two',
	3:'three',
	4:'four',
	5:'five',
	6:'six',
	7:'seven',
	8:'eight',
	9:'nine',
	10:'ten',
	11:'jack',
	12:'queen',
	13:'king',
	14:'ace'
}

RANK_CHARS = {
	1:'A',
	2:'2',
	3:'3',
	4:'4',
	5:'5',
	6:'6',
	7:'7',
	8:'8',
	9:'9',
	10:'0',
	11:'J',
	12:'Q',
	13:'K',
	14:'A'
}

@total_ordering
class Card:
	def __init__(self, suit:int, rank:int, **kwargs):
		self.suit = suit
		self.rank = rank
		self.color = kwargs.get('color', None)
		self.back_color = kwargs.get('color', 'BLUE')
		self.face_up = kwargs.get('face_up', True)

		if self.color is None:
			self.color = SUIT_COLORS.get(suit, None)

	def __str__(self):
		return f'{RANK_NAMES[self.rank].capitalize()} of {SUIT_NAMES[self.suit].capitalize()}s'

	def __lt__(self, other):
		if isinstance(other, Card):
			if self.suit == other.suit:
				return self.rank < other.rank
			else:
				return self.suit < other.suit
		else:
			return False

	def __eq__(self, other):
		return self.suit == other.suit and self.rank == other.rank

	def __add__(self, other):
		if isinstance(other, Card):
			return Deck([self, other])
		else:
			raise rankError('Card can only be added to another card.')

	def flip(self):
		self.face_up = not self.face_up

	def unicode(self):
		if not self.face_up:
			return COLOR_CHARS[self.back_color]+'\u2593\u2593'+COLOR_CHARS['RESET']
		else:
			return COLOR_CHARS[self.color]+RANK_CHARS[self.rank]+SUIT_CHARS[self.suit]+COLOR_CHARS['RESET']

class Deck:
	def __init__(self, cards:list=None, **kwargs):
		self.aces_high = kwargs.get('aces_high', True)
		if cards is not None:
			self.cards = cards
		elif kwargs.get('empty', False):
			self.cards = []
		else:
			suits = list(range(4))
			ranks = list(range(1+self.aces_high, 14+self.aces_high))
			self.cards = [Card(s, v) for s in suits for v in ranks]

	def __iter__(self):
		yield from self.cards

	def __getitem__(self, val):
		if isinstance(val, int):
			return self.cards[val]
		else:
			return Deck(self.cards[val])

	def __str__(self):
		return ' '.join(c.unicode() for c in self.cards)

	def __add__(self, other):
		if isinstance(other, Deck):
			return Deck(self.cards + other.cards)
		elif isinstance(other, Card):
			return Deck(self.cards + [other])
		else:
			raise rankError('Deck can only be added by another Deck or Card.')

	def __len__(self):
		return len(self.cards)

	def suits(self):
		return list(set(c.suit for c in self.cards))

	def ranks(self):
		return list(set(c.rank for c in self.cards))

	def copy(self):
		# return an identical copy
		return Deck(self.cards, aces_high=self.aces_high)

	def shuffle(self):
		random.shuffle(self.cards)

	def shuffled(self):
		# returns a copy of the deck with the deck shuffled
		new_deck = self.copy()
		new_deck.shuffle()
		return new_deck

	def sort(self):
		self.cards.sort()

	def draw(self, n:int=1):
		# If n > cards in deck, will draw all remaining cards.
		if n > len(self.cards):
			n = len(self.cards)
		drawn_cards = self[:n]
		self.cards = self.cards[n:]
		return drawn_cards

	def draw_all(self):
		drawn_cards = self[:]
		self.cards = []
		return drawn_cards

	def draw_random(self, n:int=1, **kwargs):
		from_subdeck = kwargs.get('from_subdeck', self) # will only draw cards from given subdeck
		drawn_cards = from_subdeck.shuffled()[:n]
		self.cards = [c for c in self.cards if c not in drawn_cards]
		return drawn_cards

	def draw_selection(self, selection:list):
		if not isinstance(selection, Deck):
			selection = Deck(selection)
		if not all(c in self.cards for c in selection):
			raise ValueError('Some cards in selection are not in the deck being drawn from.')
		self.cards = [c for c in self.cards if c not in selection]
		return selection

	def deal(self, number_of_hands, **kwargs):
		number_of_cards = kwargs.get('number_of_cards', len(self))
		collate = kwargs.get('collate', 1)
		if number_of_cards % collate:
			raise rankError('Number of cards dealt must be divisible by the collation number.')
		
		hands_dealt = [Deck(empty=True) for _ in range(number_of_hands)]

		for i in range(number_of_cards // collate):
			hands_dealt[i % number_of_hands] += self.draw(collate)

		return hands_dealt

	def append(self, other):
		if isinstance(other, Card):
			self.cards.append(other)
		elif isinstance(other, Deck):
			self.cards += other.cards
		else:
			raise TypeError('Only Cards and other Decks can be added to Decks.')

	def index(self, element):
		return self.cards.index(element)




