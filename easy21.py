#######################################################################
# Easy21 - Reinforcement Learning Assignment
# 
# The goal of this assignment is to apply reinforcement learning methods to a
# simple card game that we call Easy21. This exercise is similar to the Blackjack
# example in Sutton and Barto 5.3 – please note, however, that the rules of the
# card game are different and non-standard.
# --- The game is played with an infinite deck of cards (i.e. cards are sampled
#     with replacement)
#
# --- Each draw from the deck results in a value between 1 and 10 (uniformly
#     distributed) with a colour of red (probability 1/3) or black (probability
#     2/3).
#
# --- There are no aces or picture (face) cards in this game
#
# --- At the start of the game both the player and the dealer draw one black
#     card (fully observed)
#
# --- Each turn the player may either stick or hit
#
# --- If the player hits then she draws another card from the deck
#
# --- If the player sticks she receives no further cards
#
# --- The values of the player’s cards are added (black cards) or subtracted (red
#     cards)
#
# --- If the player’s sum exceeds 21, or becomes less than 1, then she “goes
#     bust” and loses the game (reward -1)
#
# --- If the player sticks then the dealer starts taking turns. The dealer always
#     sticks on any sum of 17 or greater, and hits otherwise. If the dealer goes
#     bust, then the player wins; otherwise, the outcome – win (reward +1),
#     lose (reward -1), or draw (reward 0) – is the player with the largest sum.
#
# Assignment from: David Silver's Reinforcement Learning Course (Youtube videos)
#
# Written by: ByronJayJee
#######################################################################

import random as rng
import numpy as np

# Set seed for debugging, gives reproducible random numbers 
# rng.seed(a=42)

red_prob = 1.0/3.0
game_outcome = -1 # -1 when in-progrss, 0 when draw, 1 when loss, 2 when win
reward = -99 #initialize to non-sense number, 0 when draw, -1 when loss, +1 when win

scount = np.zeros((10,21))
value_func = np.zeros((10,21))

player_history = []

def draw_card():
   card_num = rng.randint(1,10)
   card_color = rng.random()
   
   return [card_num, card_color]

def add_card(pnum,card_num,card_color, red_prob=red_prob):
   if(card_color<red_prob):
      pnum -= card_num
      tcolor = 'Red'
   else:
      pnum += card_num
      tcolor = 'Black'
   #print('Card drawn: ',tcolor,' ',card_num)
   return pnum

def evaluate_game(state, action, game_outcome, reward):
   dnum = state[0]
   pnum = state[1]
   if(pnum<=0) or (pnum>21):
      game_outcome = 1
      reward = -1
   
   if(dnum<=0) or (dnum>21):
      game_outcome = 2
      reward = 1

   if(action[0]==0):
      if (dnum > pnum):
         game_outcome = 1
         reward = -1
      if (dnum < pnum):
         game_outcome = 2
         reward = 1
      if (dnum == pnum):
         game_outcome = 0
         reward = 0

   return game_outcome, reward
   

def step(state, action):
   # player twist/draw when action==1
   # player stick when action==0
   # possibly throw error when action not equal to 0 or 1
   dnum = state[0]
   pnum = state[1]
   #print(dnum,pnum,action)
   
   if(action[1]==1):
      a,b = draw_card()
      pnum = add_card(pnum,a,b)
      #pnum = draw_card(pnum)
   
   if(action[0]==1) and (action[1]==0):
      a,b = draw_card()
      dnum = add_card(dnum,a,b)

   return [dnum, pnum]

def select_action(state,action):
   # assumes action is initialized to [1,1] at start of game
   dact=action[0]
   pact=action[1]
   if(pact==1) and (state[1]>=15):
      pact=0
   if(dact==1) and (pact==0):
       #if (state[0]>=17) or (state[0]>state[1]):
       if (state[0]>=17): #Dealer only sticks on sums 17 or greater
          dact=0

   return [dact, pact]

def update_value_func(player_history,reward):
   hlen = len(player_history)
   while hlen>0:
      temp_sa = player_history[-1]
      temp_s = temp_sa[0]
      temp_a = temp_sa[1]

      idx_d = player_history[0][0][0] - 1
      idx_p = temp_s[1]-1

      scount[idx_d,idx_p] += 1
      vfunc_old = value_func[idx_d,idx_p]
      vfunc_new = vfunc_old + ((reward - vfunc_old) / scount[idx_d,idx_p])
      value_func[idx_d,idx_p] = vfunc_new

      #print(scount[idx_d,idx_p])
      #print(temp_sa)
      del player_history[-1]
      hlen = len(player_history)


def play_easy21():
   player_history = []
   game_outcome = -1 # -1 when in-progrss, 0 when draw, 1 when loss, 2 when win
   reward = -99 #initialize to non-sense number, 0 when draw, -1 when loss, +1 when win
   pnum=0
   dnum=0
   ph_flag=0

   pact=1
   dact=1

   a,b = draw_card()
   pnum = add_card(pnum,a,1.0)

   a,b = draw_card()
   dnum = add_card(dnum,a,1.0)

   # Initialize state and action
   state=[dnum,pnum]
   action=[dact,pact]
   player_history.append([state,[-1,-1]])
   while game_outcome < 0:
      action = select_action(state,action)
      state = step(state,action)
      game_outcome, reward = evaluate_game(state, action, game_outcome, reward)
      #print('state: ',state)
      #print('action: ',action)
      #print('game_outcome: ',game_outcome)
      #print('reward: ',reward)
      #print('\n\n')
      if(ph_flag==0):
         player_history.append([state,action])
      if(action[1]==0):
         ph_flag=1

   print(player_history)
   if(action[1]==1):
      print(player_history)
      del player_history[-1]
   return player_history, game_outcome, reward





#pnum=0
#a,b = draw_card()
#pnum = add_card(pnum,a,b)
#print(pnum)
#print(a,b)
#print(step([10, 17],[1,1]))
#print(step([10, 17],[1,0]))

#player_history, game_outcome, reward = play_easy21()
#print(player_history)
#print(len(player_history))
for x in range(0,1000):
   player_history, game_outcome, reward = play_easy21()
   update_value_func(player_history,reward)
print(scount)
print(value_func)
