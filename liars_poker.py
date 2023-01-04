# liar's poker game - in simplest words: liar's dice but with cards and poker figures-------------------------------------------------


# imported methods---------------------------------------------------------------------------------------------------------------

# for random AI  decisions
import random

# to create a dictionary of poker figures in the game
from itertools import combinations
from itertools import permutations


# classes----------------------------------------------------------------------------------------------------------------------


# each card contains info about its value and suit
class Card:
	def __init__(self,value,suit):
		self.value=value
		self.suit=suit
	def __repr__(self):
		# print(type(f"{self.value}{self.suit}"))
		return f"{self.value}{self.suit}"

# deck default contains same cards as typical game deck without jokers
# deck can be defined with limitation of card's values which is essential in balancing this game
class Deck:
	
	# generates a list of card in deck
	def __init__(self,values=['2','3','4','5','6','7','8','9','10','J','Q','K','A']):
		self.values=values
		self.suits=['♥','♦','♣','♠']
		self.cards=[Card(value,suit) for value in values for suit in self.suits]

	def __repr__(self):
		return f'Deck of {self.count()} cards'

	def count(self):
		return len(self.cards)

	# removes specified number of cards from a deck and adds them to the list of cards on the table
	def _deal(self,num):
		amount=self.count()
		if amount == 0:
			raise ValueError ('All cards have been dealt')
		possible_num=min([num,amount])
		#print(f'going to remove {possible_num} cards')
		cards=self.cards[-possible_num:]
		self.cards=self.cards[:-possible_num]
		global cards_on_table
		cards_on_table+=[str(card) for card in cards]
		return cards

	# deals one card
	def deal_card(self):
		return self._deal(1)[0]
	
	# deals amount of card secified in player's variable 'hand_size'
	def deal_hand(self,hand_size):
		return self._deal(hand_size)

	# shuffles the deck
	def shuffle(self):
		random.shuffle(self.cards)
		print('deck shuffled')


# player has specified name and hand_size
class Player:
	
	# by default player has 1 card on hand
	# each player has a list of card on his hand
	def __init__(self,name,hand_size=1):
		self.name=name
		self.hand_size=hand_size
		self.cards_on_hand=[]

	def __repr__(self):
		return f'{self.name}'

	# each player can  bid a poker figure which is higher than global actual_bid variable
	# bidding is made by random choice of position in sliced list of possible figures
	def _bid(self):
		global actual_bid 
		actual_bid=random.choice(list(possible_figures.keys())[list(possible_figures.keys()).index(actual_bid)+1:])
		print(f'{self.name}: There are {actual_bid} ')

	# instead of bidding player can check if previous player's bid was True
	def _check(self):
		global check
		global checkin_player
		check=True
		checkin_player=players.index(self)
		print(f'{self.name}: Check')

	# each player decides if bid or check by random decision
	def _decide(self):
		global actual_bid
		decision=random.randint(0,1)
		#print(decision)
		if 'poker' in actual_bid or decision==1:
			#print('_check')
			return self._check()
		if decision==0 or actual_bid=='None':
			#print('_bid')
			return self._bid() 
			


"""
Creation of dictionary of possible poker figures in the game-------------------------------------------------------------------
will be moved to deck class
"""

def _hierarchy():

	# lists of possibles thai poker figures

	# auxiliary variable to define figures
	values_perm=[list(comb) for comb in (permutations(deck.values, 2))]
	#print(values_perm)

	high_cards_keys=[f'high card {value}' for value in deck.values]
	high_cards_values=[value for value in deck.values]

	pairs_keys=[f'pair of {value}' for value in deck.values]
	pairs_values=[value for value in deck.values]

	#sorted!!!

	# print(pairs_keys)
	rev_pair_keys=pairs_keys
	rev_pair_keys.reverse()
	# print(rev_pair_keys)

	# print(pairs_keys)
	rev_pair_values=pairs_values
	rev_pair_values.reverse()
	# print(rev_pair_values)

	two_pairs_keys =[' '.join(list(two)) for two in list(combinations(rev_pair_keys, 2))]
	two_pairs_keys.reverse()
	two_pairs_values=[(list(two)) for two in list(combinations(rev_pair_values, 2))]
	two_pairs_values.reverse()

	three_of_a_kind_keys=[f'three of {value}' for value in deck.values]
	three_of_a_kind_values=[value for value in deck.values]

	#sorted!!!

	# print(three_of_a_kind_keys)
	rev_three_key=three_of_a_kind_keys
	rev_three_key.reverse()
	# print(rev_three_key)

	# print(three_of_a_kind_values)
	rev_three_values=three_of_a_kind_values
	rev_three_values.reverse()
	# print(rev_three_values)

	double_three_of_a_kind_keys =[' '.join(list(three)) for three in list(combinations(rev_three_key, 2))]
	double_three_of_a_kind_keys.reverse()
	double_three_of_a_kind_values =[(list(three)) for three in list(combinations(rev_three_values, 2))]
	double_three_of_a_kind_values.reverse()

	full_house_keys=[f'three of {values_perm[i][0]} pair of {values_perm[i][1]}' for i in range(len(values_perm))]
	full_house_values=values_perm

	four_of_a_kind_keys=[f'four of {value}' for value in deck.values]
	four_of_a_kind_values=[value for value in deck.values]

	poker_keys=[f'poker of {suit}' for suit in deck.suits]
	poker_values=[[value+suit for value in ['9','10','J','Q','K','A']] for suit in deck.suits]
	#[suit for suit in deck.suits]

	#full list of possible thai poker figure names
	possible_figure_keys=['None']+high_cards_keys+pairs_keys+two_pairs_keys+three_of_a_kind_keys+full_house_keys+double_three_of_a_kind_keys+four_of_a_kind_keys+poker_keys
	possible_figure_values=['None']+high_cards_values+pairs_values+two_pairs_values+three_of_a_kind_values+full_house_values+double_three_of_a_kind_values+four_of_a_kind_values+poker_values
	return {possible_figure_keys[i]:possible_figure_values[i] for i in range(0,len(possible_figure_keys))}
	


	# auxiliary prints

	"""

	print(high_cards_keys)
	print(high_cards_values)
	print('  ')

	print(pairs_keys)
	print(pairs_values)
	print('  ')

	print(two_pairs_keys)
	print(two_pairs_values)
	print('  ')

	print(double_three_of_a_kind_keys)
	print(double_three_of_a_kind_values)
	print('  ')

	print(three_of_a_kind_keys)
	print(three_of_a_kind_keys)
	print('  ')

	print(full_house_keys)
	print(full_house_keys)
	print('  ')

	print(four_of_a_kind_keys)
	print(four_of_a_kind_values)
	print('  ')

	print(poker_keys)
	print(poker_values)
	print('  ')

	#print(possible_figure_keys)
	#print(possible_figure_values)

	"""

# wil be moved to Player class	
def checking():

	#print(''.join(cards_on_table))
	#print(''.join(cards_on_table).count(actual_bid.split()[2]))


	if 'high' in actual_bid:
		#print('high')
		if actual_bid.split()[2] in ''.join(cards_on_table):
			return True
		else:
			return False

	elif actual_bid.count('pair')==1 and actual_bid.count('three')==0 :
		#print('pair')
		if ''.join(cards_on_table).count(actual_bid.split()[2])>1:
			return True
		else:
			return False

	elif actual_bid.count('pair')==2 :
		#print('two pairs')
		if ''.join(cards_on_table).count(actual_bid.split()[2])>1 and ''.join(cards_on_table).count(actual_bid.split()[5])>1 :
			return True
		else:
			return False

	elif actual_bid.count('three')==0 and actual_bid.count('pair')==1 :
		#print('three')
		if ''.join(cards_on_table).count(actual_bid.split()[2])>2:
			return True
		else:
			return False

	elif actual_bid.count('three')==1 and actual_bid.count('pair')==1 :
		#print('full house')
		if ''.join(cards_on_table).count(actual_bid.split()[2])>2 and ''.join(cards_on_table).count(actual_bid.split()[5])>1:
			return True
		else:
			return False

	elif actual_bid.count('three')==2 :
		#print('two threes')
		if ''.join(cards_on_table).count(actual_bid.split()[2])>2 and ''.join(cards_on_table).count(actual_bid.split()[5])>2:
			return True
		else:
			return False


	elif actual_bid.count('four')==1 :
		#print('four')
		if ''.join(cards_on_table).count(actual_bid.split()[2])>3 :
			return True
		else:
			return False


	elif actual_bid.count('poker')==1 :
		#print('poker')
		#print(possible_figures.get(actual_bid))
		if   set(possible_figures.get(actual_bid)).issubset(set(cards_on_table)):
			return True
		else:
			return False



# Game begins---------------------------------------------------------------------------------------------------------------


# define players
players=[
Player('Paweł'),
Player('Adi'),
Player('Michał'),
Player('Daro')
]
players_names=[player.name for player in players]
print(players_names)

# main loop of the game
while len(players)>1:

	# declare a deck
	# for four players with one card on their hands it's common to limit deck values
	deck=Deck(['8','9','10','J','Q','K','A'])
	possible_figures=_hierarchy()
	#print(list(possible_figures.keys()))
	#print(deck)
	#print(deck.cards)

	# initial global conditions
	actual_bid='None'
	check=False
	checkin_player=None
	cards_on_table=[]

	# shuffle a deck
	deck.shuffle()
	for player in players:
		player.cards_on_hand+=deck.deal_hand(player.hand_size)
		print(f'{player.name} has {player.cards_on_hand} on hand')

	print(f'cards on  a table: {cards_on_table}')

	# a loop of players bidding ended by check
	while check==False:
		for player in players:
			player._decide()
			if check:
				break

	

	# result of check
	#print(f'checked bid: {actual_bid}')
	print(f'cards on  a table: {cards_on_table}')
	if checking():
		players[checkin_player].hand_size+=1
		print(f'{players[checkin_player].name} loses')
	else:
		players[checkin_player-1].hand_size+=1
		print(f'{players[checkin_player-1].name} loses')

	# new split
	for player in players:
		player.cards_on_hand=[]
	players=[player for player in players if player.hand_size<5]
	players_names=[player.name for player in players]
	print(players_names)

print(f'the winner is {players_names[0]} with {players[0].hand_size} cards on hand')



# auxiliary checking test

"""

for i in range(1,len(possible_figure_keys)):
	actual_bid=possible_figure_keys[i]
	print(actual_bid)
	print(actual_bid.split())
	if checking():
		print ('true')
	else:
		print ('false')

"""