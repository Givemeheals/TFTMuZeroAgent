import config
from Simulator.item_stats import item_builds as full_items, basic_items, starting_items
from Simulator import champion, pool, pool_stats
import random

item_list = list(full_items.keys())

# TODO
# add better randomness to drops
# add check for champion existing in the pool before being removed
# add "abilities" for each class of minions (krugs gain 1200 hp when another krug dies, etc)
# this would probably be handled with an origin for each type of minion


# Objects representing board configs for each minion round
# These should function similar to player objects except simplified for minion combat
class Minion:
    def __init__(self):
        # array of champions, since order does not matter, can be unordered list
        self.bench = [None for _ in range(9)]
        # Champion array, this is a 7 by 4 array.
        self.board = [[None for _ in range(4)] for _ in range(7)]
        self.opponent = None
        self.round = 0
        self.augment_dict = {}


class FirstMinion(Minion):
    def __init__(self, round_num):
        self.round = round_num
        super().__init__()
        self.board[2][1] = champion.champion('meleeminion')
        self.board[5][1] = champion.champion('meleeminion')


class SecondMinion(Minion):
    def __init__(self, round_num):
        self.round = round_num
        super().__init__()
        self.board[4][2] = champion.champion('meleeminion')
        self.board[1][2] = champion.champion('meleeminion')
        self.board[5][1] = champion.champion('rangedminion')


class ThirdMinion(Minion):
    def __init__(self, round_num):
        self.round = round_num
        super().__init__()
        self.board[4][2] = champion.champion('meleeminion')
        self.board[1][2] = champion.champion('meleeminion')
        self.board[5][1] = champion.champion('rangedminion')
        self.board[1][1] = champion.champion('rangedminion')


class Krug(Minion):
    def __init__(self, round_num):
        self.round = round_num
        super().__init__()
        self.board[1][3] = champion.champion('krug')
        self.board[6][3] = champion.champion('krug')
        self.board[5][1] = champion.champion('krug')


class Wolf(Minion):
    def __init__(self, round_num):
        self.round = round_num
        super().__init__()
        self.board[1][0] = champion.champion('lesserwolf')
        self.board[2][0] = champion.champion('lesserwolf')
        self.board[4][0] = champion.champion('lesserwolf')
        self.board[5][0] = champion.champion('lesserwolf')
        self.board[3][2] = champion.champion('wolf')


class Raptor(Minion):
    def __init__(self, round_num):
        self.round = round_num
        super().__init__()
        self.board[3][0] = champion.champion('crimsonraptor')
        self.board[2][1] = champion.champion('raptor')
        self.board[1][2] = champion.champion('raptor')
        self.board[5][1] = champion.champion('raptor')
        self.board[5][2] = champion.champion('raptor')


class Nexus(Minion):
    def __init__(self, round_num):
        self.round = round_num
        super().__init__()
        self.board[3][1] = champion.champion('nexusminion')


class Herald(Minion):
    def __init__(self, round_num):
        self.round = round_num
        super().__init__()
        self.board[3][1] = champion.champion('riftherald')


def minion_round(player, round_num, others):
    # simulate minion round here
    # 2 melee minions - give 1 item component
    if round_num == 0:
        minion_combat(player, FirstMinion(round_num), round_num, others)

    # 2 melee and 1 ranged minion - give 1 item component and 1 3 cost champion
    elif round_num == 1:
        minion_combat(player, SecondMinion(round_num), round_num, others)

    # 2 melee minions and 2 ranged minions - give 3 gold and 1 item component
    elif round_num == 2:
        minion_combat(player, ThirdMinion(round_num), round_num, others)

    # 3 Krugs - give 3 gold and 3 item components
    elif round_num == 8:
        minion_combat(player, Krug(round_num), round_num, others)

    # 1 Greater Murk Wolf and 4 Murk Wolves - give 3 gold and 3 item components
    elif round_num == 14:
        minion_combat(player, Wolf(round_num), round_num, others)

    # 1 Crimson Raptor and 4 Raptors - give 6 gold and 4 item components
    elif round_num == 20:
        minion_combat(player, Raptor(round_num), round_num, others)

    # 1 Nexus Minion - give 6 gold and a full item
    elif round_num == 26:
        minion_combat(player, Nexus(round_num), round_num, others)

    # Rift Herald - give 6 gold and a full item
    elif round_num >= 33:
        minion_combat(player, Herald(round_num), round_num, others)

    # invalid round! Do nothing
    else:
        return


# modeled after combat_phase from game_round.py, except with a minion "player" versus the player
def minion_combat(player, enemy, round_num, others):
    ROUND_DAMAGE = [
            [3, 0],
            [9, 2],
            [15, 3],
            [21, 5],
            [27, 8],
            [10000, 15]
        ]
    config.WARLORD_WINS['blue'] = player.win_streak
    player.end_turn_actions()

    round_index = 0
    while round_num > ROUND_DAMAGE[round_index][0]:
        round_index += 1

    player.opponent = enemy
    enemy.opponent = player

    index_won, damage, _, _ = champion.run(champion.champion, player, enemy, ROUND_DAMAGE[round_index][1])
    # list of currently alive players at the conclusion of combat
    alive = []
    for o in others:
        if o:
            if o.health > 0 and o is not player:
                alive.append(o)
    # tie!
    if index_won == 0:
        player.loss_round(damage)
        for p in alive:
            p.won_round(damage/len(alive))
        player.health -= damage
    # player wins!
    if index_won == 1:
        lootDrop(player, round_num, player.pool_obj)
    # minions win! (yikes)
    if index_won == 2:
        player.loss_round(damage)
        if len(alive) > 0:
            for p in alive:
                p.won_round(damage/len(alive))
        player.health -= damage


# decide the loot the player is owed after winning combat against minions
def lootDrop(player, round_num, pool_obj):
    # 2 melee minions - give 1 item component
    if round_num == 0:
        player.add_to_item_bench(starting_items[random.randint(0, len(starting_items) - 1)])

    # 2 melee and 1 ranged minion - give 1 item component and 1 3 cost champion
    elif round_num == 1:
        player.add_to_item_bench(starting_items[random.randint(0, len(starting_items) - 1)])
        ran_cost_3 = list(pool_stats.COST_3.items())[random.randint(0, len(pool_stats.COST_3) - 1)][0]
        ran_cost_3 = champion.champion(ran_cost_3)
        pool_obj.update(ran_cost_3, -1)
        player.add_to_bench(ran_cost_3)

    # 2 melee minions and 2 ranged minions - give 3 gold and 1 item component
    elif round_num == 2:
        player.add_to_item_bench(starting_items[random.randint(0, len(starting_items) - 1)])
        player.gold += 3

    # 3 Krugs - give 3 gold and 3 item components
    elif round_num == 8:
        player.gold += 3
        for _ in range(0, 3):
            player.add_to_item_bench(starting_items[random.randint(0, len(starting_items) - 1)])

    # 1 Greater Murk Wolf and 4 Murk Wolves - give 3 gold and 3 item components
    elif round_num == 14:
        player.gold += 3
        for _ in range(0, 3):
            player.add_to_item_bench(starting_items[random.randint(0, len(starting_items) - 1)])

    # 1 Crimson Raptor and 4 Raptors - give 6 gold and 4 item components
    elif round_num == 20:
        player.gold += 6
        for _ in range(0, 4):
            player.add_to_item_bench(starting_items[random.randint(0, len(starting_items) - 1)])

    # 1 Nexus Minion - give 6 gold and a full item
    elif round_num == 26:
        player.gold += 6
        player.add_to_item_bench(item_list[random.randint(0, len(item_list) - 1)])

    # Rift Herald - give 6 gold and a full item
    elif round_num >= 33:
        player.gold += 6
        player.add_to_item_bench(item_list[random.randint(0, len(item_list) - 1)])

    # invalid round! Do nothing
    else:
        return

