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
		status.cards_on_table+=[str(card) for card in cards]
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

	def _hierarchy(self):

		# lists of possibles poker figures

		# auxiliary variable to define figures
		values_perm=[list(comb) for comb in (permutations(self.values, 2))]

		high_cards_keys=[f'high card {value}' for value in self.values]

		pairs_keys=[f'pair of {value}' for value in self.values]

		pairs_keys.reverse()

		two_pairs_keys =[' '.join(list(two)) for two in list(combinations(pairs_keys, 2))]
		two_pairs_keys.reverse()
		pairs_keys.reverse()

		three_of_a_kind_keys=[f'three of {value}' for value in self.values]

		three_of_a_kind_keys.reverse()

		double_three_of_a_kind_keys =[' '.join(list(three)) for three in list(combinations(three_of_a_kind_keys, 2))]
		double_three_of_a_kind_keys.reverse()
		three_of_a_kind_keys.reverse()

		full_house_keys=[f'three of {values_perm[i][0]} pair of {values_perm[i][1]}' for i in range(len(values_perm))]

		four_of_a_kind_keys=[f'four of {value}' for value in self.values]	

		poker_keys=[f'poker of {suit}' for suit in self.suits]

		#full list of possible  poker figure names
		return ['None']+high_cards_keys+pairs_keys+two_pairs_keys+three_of_a_kind_keys+full_house_keys+double_three_of_a_kind_keys+four_of_a_kind_keys+poker_keys
		


# player has specified name and hand_size
class Player:
	
	# by default player has 1 card on hand
	# each player has a list of card on his hand
	def __init__(self,name,hand_size=1,strategy=None):
		self.name=name
		self.def_hand_size=hand_size
		self.hand_size=hand_size
		self.cards_on_hand=[]
		self.strategy=strategy
		self.possible_cards=[]

	def __repr__(self):
		return f'{self.name}'

	# each player can  bid a poker figure which is higher than global actual_bid variable
	# bidding is made by random choice of position in sliced list of possible figures
	def _bid(self): 
		print(status.actual_bid)
		print(str(self.cards_on_hand[0])[:-1])
		print(status.cards_declared)
		self.possible_cards=[str(card)[:-1] for card in self.cards_on_hand]
		print(self.possible_cards)
		self.possible_cards.extend(status.cards_declared)
		print(self.possible_cards)
		

		if status.actual_bid=='None':
			status.actual_bid=f'high card {str(random.choice(self.cards_on_hand))[:-1]}'
		else:
			i=0
			for possible_figure in list(status.possible_figures[list(status.possible_figures).index(status.actual_bid)+1:]):
				if len(possible_figure.split())==3:
					if self.possible_cards.count(possible_figure.split()[2])>1:
						status.actual_bid=possible_figure
						i=1
						break
				elif len(possible_figure.split())==6:
					if self.possible_cards.count(possible_figure.split()[2])>1 & self.possible_cards.count(possible_figure.split()[5])>1:
						status.actual_bid=possible_figure
						i=1
						break
			if i==0:
				status.actual_bid=random.choice(list(status.possible_figures[list(status.possible_figures).index(status.actual_bid)+1:list(status.possible_figures).index(status.actual_bid)+6]))



		if len(status.actual_bid.split())==3:
			status.cards_declared.append(status.actual_bid.split()[2])
		elif len(status.actual_bid.split())==6:
			status.cards_declared.extend([status.actual_bid.split()[2],status.actual_bid.split()[5]])
		print(status.cards_declared)
		print(f'{self.name}: There are {status.actual_bid} ')

	# instead of bidding player can check if previous player's bid was True
	def _check(self):
		status.check=True
		status.checkin_player=status.active_players.players_list.index(self)
		print(f'{self.name}: Check')

	# each player decides if bid or check by random decision
	def _default_strategy(self):
		decision=random.randint(0,1)
		#print(decision)
		if status.actual_bid!='None' and ('poker' in status.actual_bid or decision==1):
			#print('_check')
			return self._check()
		if decision==0  :
			#print('_bid')
			return self._bid() 

	# each player decides if bid or check by his strategy or by self._deafult_strategy()
	def _decide(self):
		if self.strategy:
			return self.strategy(self)
		return self._default_strategy()

	# function returns True if chcecked person was right
	def checking(self):
		if 'high' in status.actual_bid:
			if status.actual_bid.split()[2] in ''.join(status.cards_on_table):
				return True
			else:
				return False

		elif status.actual_bid.count('pair')==1 and status.actual_bid.count('three')==0 :
			if ''.join(status.cards_on_table).count(status.actual_bid.split()[2])>1:
				return True
			else:
				return False

		elif status.actual_bid.count('pair')==2 :
			if ''.join(status.cards_on_table).count(status.actual_bid.split()[2])>1 and ''.join(status.cards_on_table).count(status.actual_bid.split()[5])>1 :
				return True
			else:
				return False

		elif status.actual_bid.count('three')==0 and status.actual_bid.count('pair')==1 :
			if ''.join(status.cards_on_table).count(status.actual_bid.split()[2])>2:
				return True
			else:
				return False

		elif status.actual_bid.count('three')==1 and status.actual_bid.count('pair')==1 :
			if ''.join(status.cards_on_table).count(status.actual_bid.split()[2])>2 and ''.join(status.cards_on_table).count(status.actual_bid.split()[5])>1:
				return True
			else:
				return False

		elif status.actual_bid.count('three')==2 :
			if ''.join(status.cards_on_table).count(status.actual_bid.split()[2])>2 and ''.join(status.cards_on_table).count(status.actual_bid.split()[5])>2:
				return True
			else:
				return False


		elif status.actual_bid.count('four')==1 :
			if ''.join(status.cards_on_table).count(status.actual_bid.split()[2])>3 :
				return True
			else:
				return False


		elif status.actual_bid.count('poker')==1 :
			poker_values=[[value+suit for value in ['9','10','J','Q','K','A']] for suit in status.deck.suits]
			if  any([set(value).issubset(set(status.cards_on_table)) for value in poker_values]):
				return True
			else:
				return False	
	


class Players:
	def __init__(self,def_players):
		self.def_players=def_players
		self.players_list=def_players
		self.players_names=[player.name for player in self.players_list]
		self.players_stat={player.name:0 for player in self.def_players}
		
	def __repr__(self):
		return f"Players: {self.players_names}"

	def _refresh(self):
		self.players_list=self.def_players
		self.players_names=[player.name for player in self.players_list]
		for player in self.players_list:
			player.hand_size=player.def_hand_size
			player.cards_on_hand=[]

	def show_stats(self):
		for key,value in self.players_stat.items():
			print(key,value)



# stores variables used by other classes through the game
class Game_status:
	def __init__(self,def_players):
		# initial conditions
		self.active_players=def_players
		self.possible_figures=[]
		self.actual_bid='None'
		self.check=False
		self.checkin_player=None
		self.cards_on_table=[]
		self.deck=[]
		self.cards_declared=[]
	
	def _refresh(self):
		self.actual_bid='None'
		self.check=False
		self.checkin_player=None
		self.cards_on_table=[]
		self.deck=[]
		self.cards_declared=[]



# game contains of its number, initial conditions and run method which initialize gameplay
class Game:
	def __init__(self,number):
		self.number=number
		winner=None

	def __repr__(self):
		return f"Game no. {self.number}"

	def _run(self):
		print(self.__repr__())
		# main loop of the game
		while len(status.active_players.players_list)>1:

			# declare a deck
			# for four players with one card on their hands it's common to limit deck values
			status.deck=Deck(['8','9','10','J','Q','K','A'])
			status.possible_figures=status.deck._hierarchy()

			# shuffle a deck
			status.deck.shuffle()
			for player in status.active_players.players_list:
				player.cards_on_hand+=status.deck.deal_hand(player.hand_size)
				print(f'{player.name} has {player.cards_on_hand} on hand')

			print(f'cards on  a table: {status.cards_on_table}')

			# a loop of players bidding ended by check
			while status.check==False:
				for player in status.active_players.players_list:
					player._decide()
					if status.check:
						break

			# result of check
			print(f'cards on  a table: {status.cards_on_table}')
			if player.checking():
				status.active_players.players_list[status.checkin_player].hand_size+=1
				print(f'{status.active_players.players_list[status.checkin_player].name} loses')
			else:
				status.active_players.players_list[status.checkin_player-1].hand_size+=1
				print(f'{status.active_players.players_list[status.checkin_player-1].name} loses')

			# new split
			for player in status.active_players.players_list:
				player.cards_on_hand=[]
			status.active_players.players_list=[player for player in status.active_players.players_list if player.hand_size<6]
			status.active_players.players_names=[player.name for player in status.active_players.players_list]
			status._refresh()
			print(players.players_names)

		self.winner=status.active_players.players_list[0].name
		print(f'the winner is {status.active_players.players_names[0]} with {status.active_players.players_list[0].hand_size} cards on hand')
		players.players_stat[self.winner]+=1
		players._refresh()
		status.__init__(players)
		return 


# Strategies-----------------------------------------------------------------------------------------------------------------


# first strategy
def first_strategy(self):
		self.possible_cards.extend(status.cards_declared)
		if status.actual_bid=='None':
			# print(status.actual_bid)
			# print(self.cards_on_hand)
			# print(list(status.possible_figures[list(status.possible_figures).index(status.actual_bid)+1:]))
			# print(status.possible_figures[1:len(status.deck.values)])
			status.actual_bid=random.choice(list(status.possible_figures[1:len(status.deck.values)+1]))
			status.cards_declared.append(status.actual_bid.split()[2])
			# print(status.cards_declared)
			print(f'{self.name}: There are {status.actual_bid} ')
		elif len(status.actual_bid.split())==3:
			if self.possible_cards.count(status.actual_bid.split()[2])>1:
				return self._bid()
		elif len(status.actual_bid.split())==6:
			if self.possible_cards.count(status.actual_bid.split()[2])>1 & self.possible_cards.count(status.actual_bid.split()[5])>1:
				return self._bid()
		else:
			return self._check()


# Game begins---------------------------------------------------------------------------------------------------------------


# define players
players=Players([
Player('Paweł',1,first_strategy),
Player('Adi'),
Player('Michał'),
Player('Daro')
])

status=Game_status(players)

game_one=Game(1)
game_one._run()

game_two=Game(2)
game_two._run()	

players.show_stats()


for i in range(100):
	game_loop=Game(i)
	game_loop._run()
players.show_stats()

