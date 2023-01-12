from Simulator.augment_stats import silver_augments, gold_augments, prismatic_augments
from Simulator.stats import COST
from Simulator import champion, field, origin_class
from Simulator.item_stats import trait_items, starting_items, thiefs_gloves_items
from Simulator.pool import pool
from Simulator.pool_stats import cost_star_values
import random


def augment_choice():
    r1 = random.randint(0, 2)
    if r1 == 0:
        augment_tier = silver_augments
    elif r1 == 1:
        augment_tier = gold_augments
    else:
        augment_tier = prismatic_augments
    r2 = random.randint(0, len(augment_tier) - 1)
    r3 = random.randint(0, len(augment_tier) - 1)
    while r3 == r2:
        r3 = random.randint(0, len(augment_tier) - 1)
    r4 = random.randint(0, len(augment_tier) - 1)
    while r4 == r2 or r4 == r3:
        r4 = random.randint(0, len(augment_tier) - 1)
    option1 = list(augment_tier.keys())[r2]
    option2 = list(augment_tier.keys())[r3]
    option3 = list(augment_tier.keys())[r4]
    return [[option1, augment_tier.get(option1)], [option2, augment_tier.get(option2)],
            [option3, augment_tier.get(option3)]]


def augment_functions(player):
    if player.augments[-1][0] == 'afk':
        player.afk = player.augments[-1][1]
    elif player.augments[-1][0] == 'ancient_archives':
        player.add_to_bench(champion.champion('tome_of_traits', tome_of_traits=True))
    elif player.augments[-1][0] == 'band_of_thieves':
        if not player.item_bench_full(player.augments[-1][1]):
            for i in range(player.augments[-1][1] - 1):
                player.item_bench[player.item_bench_vacancy()] = 'thiefs_gloves'
    elif player.augments[-1][0] == 'calculated_loss':
        player.calculated_loss = player.augments[-1][1]
    elif player.augments[-1][0] == 'clear_mind':
        player.clear_mind = player.augments[-1][1]
    elif player.augments[-1][0] == 'cluttered_mind':
        player.cluttered_mind = player.augments[-1][1]
    elif player.augments[-1][0] == 'component_grab_bag':
        if not player.item_bench_full(player.augments[-1][1]):
            for _ in range(player.augments[-1][1]):
                r = random.randint(0, len(starting_items) - 1)
                player.item_bench[player.item_bench_vacancy()] = starting_items[r]
    elif player.augments[-1][0] == 'consistency':
        player.consistency = 2
    elif player.augments[-1][0] == 'future_sight':
        player.future_sight = True
        if not player.item_bench_full(player.augments[-1][1]):
            for i in range(player.augments[-1][1] - 1):
                player.item_bench[player.item_bench_vacancy()] = 'zephyr'
    elif player.augments[-1][0] == 'hustler':
        player.hustler = player.augments[-1][1][0]
        player.hustler_cut_off = player.augments[-1][1][1]
    elif player.augments[-1][0] == 'item_grab_bag':
        if not player.item_bench_full(player.augments[-1][1]):
            for i in range(player.augments[-1][1] - 1):
                r = random.randint(0, len(thiefs_gloves_items) - 1)
                player.item_bench[player.item_bench_vacancy()] = thiefs_gloves_items[r]
    elif player.augments[-1][0] == 'lategame_specialist':
        player.lategame_specialist = player.augments[-1][1]
    elif player.augments[-1][0] == 'last_stand':
        player.last_stand = True
    elif player.augments[-1][0] == 'metabolic_accelerator':
        player.metabolic_accelerator = player.augments[-1][1]
    elif player.augments[-1][0] == 'pandoras_bench':
        player.pandoras_bench = True
    elif player.augments[-1][0] == 'pandoras_items':
        player.pandoras_items = True
    elif player.augments[-1][0] == 'phony_frontline':
        dummy_added = 0
        x = 6
        y = 3
        while dummy_added < 2:
            if not player.board[x][y]:
                player.board[x][y] = champion.champion('target_dummy', target_dummy=True, round_num=player.round)
                dummy_added += 1
            x -= 1
            if x == -1:
                x = 6
                y -= 1
    elif player.augments[-1][0] == 'preparation':
        player.preparation_power = player.augments[-1][1][0]
        player.preparation_health = player.augments[-1][1][1]
        player.preparation_limit = player.augments[-1][1][2]
    elif player.augments[-1][0] == 'recombobulator':
        recombobulate(player)
    elif player.augments[-1][0] == 'tiny_titans':
        player.max_health += player.augments[-1][1]
        player.health += player.augments[-1][1]


def start_of_battle_augments(team):
    if team and len(team[0].augments) > 0:
        for x in range(len(team[0].augments)):
            if team[0].augments[x][0] == 'ascension':
                team[0].add_que('execute_function', 15000, [ascension, {team[0]}])
            elif team[0].augments[x][0] == 'axiom_arc':
                for champ in team:
                    champ.axiom_arc = True
            elif team[0].augments[x][0] == 'battlemage':
                for champ in team:
                    if champ.y == 2 or champ.y == 3 or champ.y == 4 or champ.y == 5:
                        champ.SP += champ.augments[x][1]
            elif team[0].augments[x][0] == 'big_friend':
                for champ in team:
                    for allies in field.allies_in_distance(champ, champ.y, champ.x, 1):
                        if allies.health >= champ.augments[x][1][0]:
                            champ.big_friend -= champ.augments[x][1][1]
            elif team[0].augments[x][0] == 'blue_battery':
                for champ in team:
                    champ.SP = champ.augments[x][1][0]
                    champ.blue_battery = champ.augments[x][1][1]
            elif team[0].augments[x][0] == 'built_different':
                for champ in team:
                    built_dif = True
                    for trait in champ.origin:
                        if origin_class.get_origin_class_tier(champ.team, trait) != 0:
                            built_dif = False
                    if built_dif:
                        champ.health += champ.augments[x][1][0]
                        champ.AS += champ.augments[x][1][1]
            elif team[0].augments[x][0] == 'celestial_blessing':
                for champ in team:
                    champ.lifesteal += champ.augments[x][1]
                    champ.lifesteal_spells += champ.augments[x][1]
            elif team[0].augments[x][0] == 'combat_training':
                for champ in team:
                    champ.combat_training_iteration = champ.augments[x][1][0]
                    champ.AD += champ.combat_training + champ.augments[x][1][1]
            elif team[0].augments[x][0] == 'cybernetic_implants':
                for champ in team:
                    champ.health += champ.augments[x][1][0]
                    champ.AD += champ.augments[x][1][1]
            elif team[0].augments[x][0] == 'cybernetic_shell':
                for champ in team:
                    champ.health += champ.augments[x][1][0]
                    champ.armor += champ.augments[x][1][1]
            elif team[0].augments[x][0] == 'cybernetic_uplink':
                for champ in team:
                    champ.health += champ.augments[x][1][0]
                    champ.change_stat(champ, None, 1000, True, 'mana', champ.mana + champ.augments[x][1][1])
            elif team[0].augments[x][0] == 'double_trouble':
                for champ in team:
                    double_trouble = False
                    for ally in team:
                        if champ.name == ally.name:
                            double_trouble = True
                    if double_trouble:
                        champ.AD += champ.augments[x][1]
                        champ.SP += champ.augments[x][1]
                        champ.MR += champ.augments[x][1]
                        champ.armor += champ.augments[x][1]
            elif team[0].augments[x][0] == 'exiles':
                for champ in team:
                    if not field.allies_in_distance(champ, champ.y, champ.x, 1):
                        champion.shield(champ, champ.augments[x][1])
            elif team[0].augments[x][0] == 'featherweights':
                for champ in team:
                    if COST.get(champ.name) == 1 or COST.get(champ.name) == 2:
                        champ.AS *= champ.augments[x][1]
                        champ.movement_delay *= 1 / champ.augments[x][1]
            elif team[0].augments[x][0] == 'first_aid_kit':
                for champ in team:
                    champ.healing_strength += champ.augments[x][1]
            elif team[0].augments[x][0] == 'jeweled_lotus':
                for champ in team:
                    champ.crit_chance += champ.augments[x][1]
                    champ.jeweled_lotus = True
            elif team[0].augments[x][0] == 'knifes_edge':
                for champ in team:
                    if champ.y == 2 or champ.y == 3 or champ.y == 4 or champ.y == 5:
                        champ.AD += champ.augments[x][1]
            elif team[0].augments[x][0] == 'last_stand' and team[0].last_stand:
                for champ in team:
                    champ.health += champ.augments[x][1][0]
                    champ.armor += champ.augments[x][1][1]
                    champ.MR += champ.augments[x][1][1]
                    champ.lifesteal += champ.augments[x][1][2]
                    champ.lifesteal_spells += champ.augments[x][1][2]
            elif team[0].augments[x][0] == 'makeshift_armor':
                for champ in team:
                    if not champ.items:
                        champ.MR += champ.augments[x][1]
                        champ.armor += champ.augments[x][1]
            elif team[0].augments[x][0] == 'second_wind':
                team[0].add_que('execute_function', 15000, [second_wind, {team[0]}])
            elif team[0].augments[x][0] == 'stand_united':
                traits = {key: value for (key, value) in team[0].team_tiers.items() if value > 0}
                for champ in team:
                    champ.AD += team.augments[x][1] * len(list(traits.values()))
                    champ.SP += team.augments[x][1] * len(list(traits.values()))
            elif team[0].augments[x][0] == 'thrill_of_the_hunt':
                for champ in team:
                    champ.thrill_of_the_hunt = True
            elif team[0].augments[x][0] == 'tri_force':
                for champ in team:
                    if champ.cost == 3:
                        champ.health += champ.augments[x][1][0]
                        champ.mana += champ.augments[x][1][1]
                        champ.AS += champ.augments[x][1][2]


def start_of_round_augments(player):
    if player.health + player.metabolic_accelerator <= 100:
        player.health += player.metabolic_accelerator
    if player.pandoras_bench:
        pandoras_bench_funct(player)
    if player.pandoras_items:
        pandoras_items_funct(player)
    if player.preparation_limit != 0:
        preparation(player)
    if player.calculated_loss and player.loss_streak != 0:
        player.gold += 2
        player.free_refreshes += 1
    if player.afk != 0:
        player.afk_turn_count += 1
        if player.afk_turn_count == 3:
            player.gold += player.afk
            player.afk = 0
    if player.clear_mind != 0:
        clear_mind(player, player.clear_mind)
    if player.cluttered_mind != 0:
        cluttered_mind(player, player.cluttered_mind)


def ascension(a_champion):
    for augments in a_champion.augments:
        if augments[0] == 'ascension':
            ascension_value = augments[1]
    for champ in a_champion.team:
        champ.add_que('change_stat', -1, False, 'ascension_value', ascension_value)


def clear_mind(player, value):
    empty_slots = 0
    for slot in player.bench:
        if slot is None:
            empty_slots += 1
    if empty_slots == 9:
        player.exp += value


def cluttered_mind(player, value):
    empty_slots = 0
    for slot in player.bench:
        if slot is not None:
            empty_slots += 1
    if empty_slots == 9:
        player.exp += value


def electrocharge(value, champion):
    for enemy in field.enemies_in_distance(champion, champion.y, champion.x, 1):
        champion.spell(enemy, value, 0, True)
    return True


def pandoras_bench_funct(player):
    for slot in range(6, 8):
        if player.bench[slot]:
            temp_star = player.bench[slot].stars
            temp_cost = player.bench[slot].cost
            player.sell_from_bench(slot, golden=False)
            player.gold -= cost_star_values[temp_cost - 1][temp_star - 1]
            player.bench[slot] = pool.sample(player, 1, player.bench[slot].cost - 1)[0]
            player.bench[slot].stars = temp_star


def pandoras_items_funct(player):
    for item in range(len(player.item_bench)):
        if player.item_bench[item]:
            if player.item_bench[item] in thiefs_gloves_items:
                r = random.randint(0, len(thiefs_gloves_items))
                if r == len(thiefs_gloves_items):
                    player.item_bench[item] = 'thiefs_gloves'
                else:
                    player.item_bench[item] = thiefs_gloves_items[r]
            elif player.item_bench[item] in trait_items:
                r = random.randint(0, len(list(trait_items.values())) - 1)
                player.item_bench[item] = list(trait_items.values())[r]
            elif player.item_bench[item] in starting_items:
                r = random.randint(0, len(starting_items) - 1)
                player.item_bench[item] = starting_items[r]


def preparation(player):
    for slot in player.bench:
        if slot:
            slot.preparation_stacks += 1
            if slot.preparation_stacks <= player.preparation_limit:
                slot.AD += player.preparation_power
                slot.SP += player.preparation_power
                slot.health += player.preparation_health


def recombobulate(player):
    for x in range(6):
        for y in range(3):
            if player.board[x][y]:
                temp_star = player.board[x][y].stars
                temp_cost = player.board[x][y].cost
                player.sell_champion(player.board[x][y], False, False)
                player.gold -= cost_star_values[temp_cost - 1][temp_star - 1]
                player.board[x][y] = pool.sample(player, 1, player.board[x][y].cost)[0]
                player.board[x][y].stars = temp_star


def second_wind(a_champion):
    for augment in a_champion.augments:
        if augment[0] == 'second_wind':
            for champ in a_champion.team:
                champ.add_que('heal', -1, None, None, augment[1] * (a_champion.max_health - a_champion.health))
