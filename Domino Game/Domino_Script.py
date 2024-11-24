from Domino_Func import *

scores = [0]          #initial value to enter the while loop
w = 0                 #initial value for player index in start_game function
N = get_correct_N()     #number of players
player,  data = Efile(N)          #get playing players in dict_player and the data base in dict_data from file 'update_scores'
while max(scores) <= 10:              #starting new game till one player exceeds 100 point
    cards = generate_domino_cards()
    player = distribute_cards(cards, player)
    ground, k = start_game(N,player, scores, w)           #in first game it searches for |6,6| |5,5|...etc then add it to the ground and get player index who played that card  in other games last winner starts with any card
    k = next_player(k, N)                                 #gets index of next player
    while k < N+1:                                        #moves players' rounds along the game
            R_edge = ground[-2]                                #defines the two sides of ground for each round
            L_edge = ground[1]

            if L_edge not in ''.join(player[k]['cards']) and R_edge not in ''.join(player[k]['cards']):              #if player doesn't have card to play he withdraws till he found one or cards finish
                if len(cards) > 0:
                    print(f"{player[k]['name']} withdraws {cards[0]}")
                    player[k]['cards'].append(cards[0])
                    del cards[0]
                    continue
                else:
                    print(f"{player[k]['name']} passed")
                    k = next_player(k, N)
                    continue

            rc_index = input(f"\n{player[k]['name']} round\nground --> {ground}\nyour cards are {list(enumerate(player[k]['cards'], 1))}\nchoose the card you want to play by it\'s number: ")
            if  rc_index.isdigit() == False:
                print('please play an appropriate card')                #get index of card that chosen and check if it is correct
                continue
            else:
                rc_index =  int(rc_index)
                if rc_index <= len(player[k]['cards']):
                    rc = player[k]['cards'][rc_index - 1]
                else:
                    print('please play an appropriate card')
                    continue


            if (L_edge not in rc and R_edge not in rc) or rc not in player[k]['cards'] :              #check if the chosen card can be played by that player or not
                print('please play an appropriate card')
            else:
                player[k]['cards'].remove(rc)
                ground = update_ground(ground, rc)
                end_conditions, w, game_score, msg = if_endgame(player, ground, k, N)        #check if any player wins by this round
                if end_conditions == True :
                    break

                k = next_player(k, N)
    if end_conditions == True:                      #add the score to the winner and print the message for him
        player[w]['score'] = player[w]['score'] + game_score
        print(msg)

    for s in player.keys(): #add the score to the list of scores to stop the while loop if one player exceeds 100 points
        scores.append(player[s]['score'])


champions = [z for z in player.keys() if player[z]['score'] == max(scores)]
champion = player[champions[0]]['id']                 #get id of the winner to update his data
print(data)
data[champion]['wins'] += 1
data[champion]['total score'] += max(scores)
Update_file(data)                                 #update the data base in file 'update_scores'
