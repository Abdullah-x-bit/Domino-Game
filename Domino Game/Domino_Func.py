import random
def generate_domino_cards():
    cards = [f'|{i1},{i2}|' for i1 in range(7) for i2 in range(i1, 7)]
    random.shuffle(cards)
    return cards
def get_correct_N():
    N = int(input('N(2:4)= '))
    while N < 2 or N > 4 :
        print('Enter correct Number')
        N = int(input('N(2:4)= '))
    return N
def Efile(N):
    player = {}

    file1 = open("Update_scores.txt", "a+")
    file = open("Update_scores.txt", "r")
    l_p=[]
    data = {}
    for line in file:
        x = line.strip().split()
        if x[0] == 'Name':
            continue
        data.update({x[1]: {'name': x[0], 'wins': int(x[3]), 'total score':int(x[2])}})

    for i in range(N):
        pl_ID = input(f"Player {i + 1} ID:")

        while pl_ID in l_p:
            pl_ID = input(f"this player already joined enter another ID:")
        l_p.append(pl_ID)
        if pl_ID in data:
            print(f"player {data[pl_ID]['name']} joined ")
            pl_N = data[pl_ID]['name']

        else:
            pl_N = input(f"Player {i + 1} NAME:")
            file1.write(f"{pl_N}\t\t{pl_ID}\t\t{str(0)}\t\t{str(0)}\n")
            file1.close()
            file1=open("Update_scores.txt", "a+")
            # data = {}
            for line in file:
                x = line.strip().split()
                data.update({x[1]: {'name': x[0], 'wins': int(x[3]), 'total score':int(x[2])}})

        player.update({i: {'name': pl_N,'id': pl_ID ,'cards': [], 'weight': 0, 'score': 0}})

    return player, data
def distribute_cards(cards, player):
    for k in player.keys() :
        player[k]['cards'] = cards[:7]
        del cards[:7]
    return player

def next_player(k, N):
    k += 1
    if k == N:
        k = 0
    return k

def start_game(N, player, scores, w):
    k = w
    if max(scores) == 0:
        i = 6
        while i <= 6:
                if f'|{i},{i}|' in player[k]['cards']:
                    player[k]['cards'].remove(f'|{i},{i}|')
                    ground = f'|{i},{i}|'
                    break
                else:
                    if k == N-1:
                        i = i - 1
                    k = next_player(k, N)
    else:
        ground = ''
        rc_index = input(f"\n{player[k]['name']} round\nground --> {ground}\nyour cards are {list(enumerate(player[k]['cards'], 1))}\nchoose the card you want to play by it\'s number: ")
        while rc_index.isdigit() == False or int(rc_index) > len(player[k]['cards']):
            print('please play an appropriate card')
            rc_index = input(f"\n{player[k]['name']} round\nground --> {ground}\nyour cards are {list(enumerate(player[k]['cards'], 1))}\nchoose the card you want to play by it\'s number: ")
        rc_index = int(rc_index)
        rc = player[k]['cards'][rc_index - 1]
        ground = rc
        player[k]['cards'].remove(rc)
    return ground, k

def update_ground(ground, rc):
    R_edge = ground[-2]
    L_edge = ground[1]
    if L_edge in rc and R_edge in rc and L_edge != R_edge:  # card can be played on both sides
        side = input('which side(r/l)? ')
        while side != 'r' and side != 'l' :
            print('please choose a side r for right l for left')
            side = input('which side(r/l)? ')
        if side == 'l':
            if rc[1] == L_edge:
                ground = rc[::-1] + ground
            elif rc[-2] == L_edge:
                ground = rc + ground
        if side == 'r':
            if R_edge == rc[1]:
                ground = ground + rc
            elif R_edge == rc[-2]:
                ground = ground + rc[::-1]
    elif R_edge in rc:
        if rc[1] == R_edge:
            ground = ground + rc
        elif rc[-2] == R_edge:
            ground = ground + rc[::-1]
    elif L_edge in rc:
        if L_edge == rc[1]:
            ground = rc[::-1] + ground
        elif L_edge == rc[-2]:
            ground = rc + ground
    return ground

def calc_weights(N, player):
    weights = []
    for i in player.keys():
        s = ''.join(player[i]['cards'])
        #print(s)
        s = s.replace('||', '').replace('|','').replace(',', '')
        #print(s)
        player[i]['weight'] = sum([int(j) for j in s])
        weights.append(player[i]['weight'])
    return weights

def if_endgame(player, ground, k, N):
    R_edge = ground[-2]
    L_edge = ground[1]
    if len(player[k]['cards']) == 0:
        end_conditions = True
        w = k
        game_score = sum(calc_weights(N, player))
        msg = f"{player[w]['name']} wins with score {game_score}"
    elif R_edge == L_edge:
        G = ground.replace('|', '').replace(',', '').replace('||', '')
        count = 0
        for u in G:
            if u == R_edge:
                count = count + 1
        if count == 8:
            end_conditions = True
            winners = [z for z in player.keys() if player[z]['weight'] == min(calc_weights(N, player))]
            if len(winners) > 1:
                w = winners[0]
                game_score = 0
                msg = f"tie between players: {[player[x]['name'] for x in winners]}"
            else:
                w = winners[0]
                game_score = sum(calc_weights(N, player)) - min(calc_weights(N, player))
                msg = f"{player[w]['name']} wins with score {game_score}"
        else:
            end_conditions = False
            w = ''
            game_score = 0
            msg = ''
    else:
        end_conditions = False
        w = ''
        game_score = 0
        msg = ''
    return end_conditions, w, game_score, msg

def Update_file(data):
    file=open("Update_scores.txt", "w+")
    file.write(f"Name\t\tID\t\tScore\t\tWins\n")
    for key in data:
        file.write(f"{data[key]['name']}\t\t{key}\t\t{str(data[key]['total score'])}\t\t{str(data[key]['wins'])}\n")
