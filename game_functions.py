# Black Jack Game Functions

import random
import time


# Pause
# short pause for dealer's turn so player can keep up with actions
def pause():
    time.sleep(.9)


def pause_long():
    time.sleep(1.3)


# Save
# saves balance to txt file and exits
def save(balance, leave):
    with open('Save', 'w') as f:
        f.write(str(balance))
    if leave:
        exit()


# Load
# loads previous balance from txt file
def load():
    balance_save = open('Save', 'r')
    balance = balance_save.read()
    return balance  # returns saved balance


# Check for BJ
# checks input hand for BJ, returns True or False
def bj_check(hand, bj=False):
    if 'A' in hand:
        if '10' in hand or 'J' in hand or 'Q' in hand or 'K' in hand:
            bj = True
    return bj


# Hand Select
# randomly determines starting hands from deck, updates deck
def hand_select(deck):
    hand = random.sample(deck, 2)
    hand_player = [f"{hand[0]}", f"{hand[1]}"]
    deck.remove(hand_player[0])
    deck.remove(hand_player[1])
    return hand_player


# Card Select
# randomly determines next drawn card and adds it to hand
def draw_card(hand, deck):
    drawn = random.choice(deck)
    hand.append(drawn)
    deck.remove(drawn)
    return hand, drawn, deck


# Convert Ace
# converts aces to 11's or 1's depending on hand value, returns hand value and hand
def conv_ace(hand, hand_int):
    hand_no_ace = []
    for i in range(len(hand)):
        if hand[i] != 'A':
            hand_no_ace.append(int(hand_int[i]))

    tot = sum(hand_no_ace)  # value of hand without any
    ind = []

    if hand.count('A') == 1:  # if one Ace held
        if tot <= 10:
            for i in range(len(hand)):
                if hand[i] == 'A':
                    hand_int[i] = 11
        else:
            for i in range(len(hand)):
                if hand[i] == 'A':
                    hand_int[i] = 1  # Assign Ace to 1
    elif hand.count('A') == 2:  # if two Aces held
        if tot <= 9:
            ind.clear()
            for i in range(len(hand)):
                if hand[i] == 'A':
                    ind.append(i)  # create list of indices where Aces are
            hand_int[ind[0]] = 11  # Assign first Ace to 11
            hand_int[ind[1]] = 1  # Assign second Ace to 1
        else:
            for i in range(len(hand)):
                if hand[i] == 'A':
                    hand_int[i] = 1  # Assign both Aces to 1
    elif hand.count('A') == 3:  # if three Aces held
        if tot <= 8:
            ind.clear()
            for i in range(len(hand)):
                if hand[i] == 'A':
                    ind.append(i)
            hand_int[ind[0]] = 11
            hand_int[ind[1]] = 1
            hand_int[ind[2]] = 1
        else:
            for i in range(len(hand)):
                if hand[i] == 'A':
                    hand_int[i] = 1  # Assign all Aces to 1
    return hand, hand_int


# Bet / Pause
# asks player for bet ($) and displays it
def betting(balance):
    while True:
        initial = input('\nPlace Your Bet ($) (0 to pause): ')
        if not initial.isdigit() or int(initial) < 0:
            print('\n*** Invalid Bet, Try Again ***')
            continue
        elif int(initial) > balance:
            print("\n*** Bet Exceeds Balance ***\n")
            continue
        elif int(initial) == 0:
            while True:
                pause = input('\nPause? Y/N: ')
                if str(pause) == 'Y' or str(pause) == 'y':  # if choose pause
                    while True:
                        confirm = input('\nSave Balance (Overwrites Previous)? Y/N: ')
                        if confirm == 'Y' or confirm == 'y':  # if save balance
                            save(balance, True)  # save balance and terminate
                        elif confirm == 'N' or confirm == 'n':  # if not save Balance
                            exit()  # terminate
                        else:  # invalid input
                            print('*** Select Yes or No ***')
                            continue
                if str(pause) == 'N' or str(pause) == 'n':
                    break
                else:
                    print('*** Select Yes or No ***')
                    continue
        else:
            return initial


# Hit
# gives player new card
def hit(hand, deck):
    # draw card (and show)
    hand, drawn, deck = draw_card(hand, deck)
    # print("Card Drawn:   ", drawn)
    # pause()
    print("Current Hand: ", " ".join(hand))

    # calculate hand
    bust, value = calculate(hand)
    print(f'            :  [{value}]')  # show hand's current value
    pause()

    return hand, deck


# Calculate
# calculate's individual hand for a bust or BJ
def calculate(hand):
    # convert hand to integer array
    hand_int = [0 for i in range(len(hand))]

    # sum
    for i in range(len(hand)):
        if hand[i] == 'J' or hand[i] == 'Q' or hand[i] == 'K':
            hand_int[i] = 10
        elif hand[i] != 'A':
            hand_int[i] = int(hand[i])

        # consider player ace
    if 'A' in hand:
        hand, hand_int = conv_ace(hand, hand_int)  # convert aces based on

    # final value calc
    value = sum(hand_int)

    # if bust
    if value > 21:
        return 1, value  # returns bust & value

    # if 21
    elif value == 21:
        return -1, value  # returns bust & value

    # if nothing
    else:
        return -1, value  # returns bust & value


# Compare
# compares dealer and player's hand at end of turn (assumes no bust, no blackjack)
def compare(player_val, dealer_val):
    # display value comparison
    print('\n..............')
    print(f'Player: [{player_val[1]}] ')
    print(f'Dealer: [{dealer_val[1]}] ')
    print('..............')
    pause_long()

    if player_val > dealer_val:
        win = 1  # if player win
    elif player_val < dealer_val:
        win = -1  # if player lose
    else:
        win = 0  # if push
    return win


# Cashout
# takes input bet and balance, then calculates appropriate return balance
def cashout(balance, bet, bj, win):
    print('---------------------------------\n')
    # if bj
    if bj:
        balance += 2 * bet
    # if win
    elif win > 0:
        balance += bet
        print('\n  === You Win ===\n')
        print(f'\n---------------------------------\n  +${bet} Won')
    # if lose
    elif win < 0:
        balance -= bet
        print('\n === Dealer Wins ===\n')
        print(f'\n---------------------------------\n  -${bet} Lost')
    else:
        print('\n--- Push ---\n')
        print(f'\n---------------------------------\n')
    print('Balance: $', balance, '\n---------------------------------')
    return balance
