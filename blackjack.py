# Black Jack Game Logic
# Brandon 7/15/24

# import all
from game_functions import hand_select
from game_functions import hit
from game_functions import betting
from game_functions import calculate
from game_functions import bj_check
from game_functions import cashout
from game_functions import compare
from game_functions import pause
from game_functions import load
from game_functions import save
from game_functions import pause_long

# Initialize Start Conditions
print('|||||||| BLACKJACK ||||||||')

# Game Select or Erase
balance_init = int(500)
while True:
    print('\nNew Game:   (1) \nLoad Game:  (2)'  # Game Select Screen
          '\nErase Save: (3) \nExit:       (4)')
    game_choice = input('\nChoose a Game Option: ')
    if not game_choice.isdigit():
        print('Please Choose a Valid Option:\n')
        continue
    if int(game_choice) == 1:  # NEW
        balance = balance_init
        break
    elif int(game_choice) == 2:  # LOAD
        balance = int(load())
        break
    elif int(game_choice) == 3:  # ERASE
        print('Save Successfully Erased')
        save(balance_init, False)  # resets saved balance (equivalent to erase), don't leave
        balance = balance_init  # reset current balance
        pause()
        continue
    elif int(game_choice) == 4:
        exit()
    else:
        print('Please Choose a Valid Option:\n')
        continue

print('---------------------------------\n', 'Balance: $', balance, '\n---------------------------------')
win = False

# ===== Main Game Loop =====
while True:

    if balance <= 0:  # First Check Balance for Bankrupcy
        print("\n\nYou're Bankrupt :/ \n")
        pause_long()
        if int(game_choice) == 2:  # if Load Game was selected (reset save)
            print('Save File Balance was Reset')
            save(balance_init, False)  # reset saved balance, don't leave

        while True:
            restart = input("\nRestart? Y/N: ")
            if str(restart) == 'Y' or str(restart) == 'y':
                balance = balance_init
                break
            elif str(restart) == 'N' or str(restart) == 'n':
                balance = balance_init  # reset current balance
                print('Exiting...')
                pause()
                break
            else:
                print('Please Choose a Valid Option:\n')
                continue
        if str(restart) == 'N' or str(restart) == 'n':  # if not restarting
            break  # exit game loop
        print('---------------------------------\n', 'Balance: $', balance, '\n---------------------------------')
        win = False

    #

    # reshuffle deck
    deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4

    # ask player bet
    bet = int(betting(balance))

    # determine and display starting hands
    hand_player = hand_select(deck)  # player's hand
    hand_dealer = hand_select(deck)  # dealer's hand
    print('\nDealer Hand: ', hand_dealer[0], '*')
    print('Player Hand: ', hand_player[0], hand_player[1])
    pause()

    # initial player bj check for potential cashout
    bj = bj_check(hand_player)
    if bj:
        bj_dealer = bj_check(hand_dealer) # if dealer doesn't have BJ
        if not bj_dealer:
            print('\n--- BLACKJACK ---')
            pause()
            balance = cashout(balance, bet, bj, win)
            continue
        else:  # if dealer ALSO has blackjack
            print('\n--- BLACKJACK ---')
            pause()
            print('\n---Dealer also has BLACKJACK---')
            pause()
            print(f'\nDealer Hand: {hand_dealer[0]} {hand_dealer[1]}')
            pause()
            bj = False
            player_val = calculate(hand_player)
            dealer_val = calculate(hand_dealer)
            win = compare(player_val, dealer_val)

            balance = cashout(balance, bet, bj, win)
            pause()
            continue

    # Insurance case
    if hand_dealer[0] == 'A':
        side_bet = 0
        while True:
            insurance = input('Insurance? Y/N: ')
            if str(insurance) == 'Y' or str(insurance) == 'y':
                side_bet = int(bet)
                break
            if str(insurance) == 'N' or str(insurance) == 'n':
                break
            else:
                print('Invalid, Try Again')
                continue
            # initial bj check - nothing if no bj, lose if bj
        bj = bj_check(hand_dealer)
        if bj and (str(insurance) == 'Y' or str(insurance) == 'y'):
            print(f'\nDealer Hand: {hand_dealer[0]} {hand_dealer[1]}')
            pause()
            print('\n--- Dealer has BLACKJACK ---')
            pause()
            bj = False
            win = -1
            bet = 0
            balance = cashout(balance, bet, bj, win)
            continue
        if not bj and (str(insurance) == 'N' or str(insurance) == 'n'):
            print('\n--- Dealer does NOT have BLACKJACK ---')
            pause()
            print(f'     (${side_bet} of Insurance lost)')
            pause()
            balance -= side_bet

    # Regular Dealer BlackJack Check
    bj = bj_check(hand_dealer)
    if bj:
        print(f'\nDealer Hand: {hand_dealer[0]} {hand_dealer[1]}')
        pause()
        print('\n--- Dealer has BLACKJACK ---')
        bj = False
        win = -1
        balance = cashout(balance, bet, bj, win)
        continue

    # ==== Player's Turn ==== #
    # player decision
    while True:
        print("\n==== Player's Turn ====")
        decision = input('Hit (H), Double Down (D), or Stand (S): ')
        if str(decision) != 'H' and str(decision) != 'h' and str(decision) != 'D' and str(decision) != 'd' and str(
                decision) != 'S' and str(decision) != 's':
            print('Invalid choice, try again!')
            continue
        else:
            decision = str(decision)

            # consequence
            if decision == 'H' or decision == 'h':
                hand_player, deck = hit(hand_player, deck)
                bust, value_player = calculate(hand_player)
                if value_player == 21:
                    print('\n\\\\ TWENTY ONE ////')
                    break
                elif bust < 0:
                    continue
            elif decision == 'D' or decision == 'd':
                if len(hand_player) > 2:
                    print('\n*** Cannot Double Down After Initial Action ***')
                    continue
                if 2*bet > balance:
                    print('\n*** Not Enough Money ***')
                    continue
                else:
                    hand_player, deck = hit(hand_player, deck)
                    bust, value_player = calculate(hand_player)
                    bet *= 2
                    break
            elif decision == 'S' or decision == 's':
                bust = -1
                break
        # if bust
        if bust > 0:
            break
        elif value_player == 21:
            print('YOU HIT 21')
            break
        else:
            break

    if bust > 0:  # catch bust case
        win = -1
        print('   --- BUST ---')
        balance = cashout(balance, bet, bj, win)
        continue

    # else goes to dealer's turn

    # ==== Dealer's Turn ==== #
    print("\n==== Dealer's Turn ====")
    print("Dealer Hand: ", hand_dealer[0], hand_dealer[1])
    bust, value_dealer = calculate(hand_dealer)
    print(f'           : [{value_dealer}]')
    pause()

    while True:  # continue hit until > 17
        bust, value_dealer = calculate(hand_dealer)
        if value_dealer == 21:
            break  # break to cashout
        elif value_dealer < 17:
            print(':: Dealer Hits ::')
            pause_long()
            hand_dealer, deck = hit(hand_dealer, deck)  # hit
            continue
        elif value_dealer > 21:
            bust = 1
            break  # break to dealer bust
        else:  # stand
            print(':: Dealer Stands ::')
            pause()
            bust = -1
            break
    if bust > 0:  # catch bust case for dealer
        win = 1
        print('--- Dealer BUST ---')
        pause_long()
        balance = cashout(balance, bet, bj, win)
        continue

    # ==== Cashout ==== #
    pause()
    player_val = calculate(hand_player)
    dealer_val = calculate(hand_dealer)
    win = compare(player_val, dealer_val)

    balance = cashout(balance, bet, bj, win)
    pause()
