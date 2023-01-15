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
    return [{option1: augment_tier[option1]}, {option2: augment_tier[option2]},
            {option3: augment_tier[option3]}]


def augment_functions(player, augment):
    if 'ancient_archives' == augment.keys():
        for _ in range(augment.values()):
            player.add_to_bench(champion.champion('tome_of_traits', tome_of_traits=True))
    elif 'band_of_thieves' == augment.keys():
        if not player.item_bench_full(augment['band_of_thieves']):
            for i in range(augment['band_of_thieves']):
                player.item_bench[player.item_bench_vacancy()] = 'thiefs_gloves'
    elif 'consistency' == augment.keys():
        player.consistency = augment['consistency']
    elif 'component_grab_bag' == augment.keys():
        if not player.item_bench_full(augment['component_grab_bag']):
            for _ in range(augment['component_grab_bag']):
                r = random.randint(0, len(starting_items) - 1)
                player.item_bench[player.item_bench_vacancy()] = starting_items[r]
    elif 'cursed_crown' == augment.keys():
        player.damage_multiplier = 2
        player.max_units += augment['cursed_crown']
    elif 'future_sight' == augment.keys():
        player.future_sight = True
        if not player.item_bench_full(augment['future_sight']):
            for i in range(augment['future_sight'] - 1):
                player.item_bench[player.item_bench_vacancy()] = 'zephyr'
    elif 'high_roller' == augment.keys():
        for _ in range(augment.values()):
            if not player.item_bench_full(1):
                player.item_bench[player.item_bench_vacancy()] = 'champion_duplicator'
    elif 'item_grab_bag' == augment.keys():
        for _ in range(augment['item_grab_bag']):
            give_random_item(player)
    elif 'new_recruit' == augment.keys():
        player.max_units += 1
    elif 'phony_frontline' == augment.keys():
        dummy_added = 0
        x = 6
        y = 3
        while dummy_added < augment.values():
            if not player.board[x][y]:
                player.board[x][y] = champion.champion('target_dummy', target_dummy=True, round_num=player.round)
                dummy_added += 1
            x -= 1
            if x == -1:
                x = 6
                y -= 1
    elif 'portable_forge' == augment.keys():
        portable_forge(player)
    elif 'radiant_relics' == augment.keys():
        for _ in range(2):
            give_random_item(player)
    elif 'recombobulator' == augment.keys():
        recombobulate(player)
    elif 'rich_get_richer' == augment.keys():
        player.interest = augment['rich_get_richer'][0]
        player.gold += augment['rich_get_richer'][1]
    elif 'salvage_bin' == augment.keys():
        give_random_item(player)
    elif 'think_fast' == augment.keys():
        player.free_refreshes += augment.values()
    elif 'threes_company' == augment.keys():
        for _ in range(augment['threes_company']):
            if not player.bench_full():
                player.bench[player.bench_vacancy()] = pool.sample(player, 1, 2)[0]
    elif 'tiny_titans' == augment.keys():
        player.max_health += augment['tiny_titans']
        player.health += augment['tiny_titans']
    elif 'true_twos' == augment.keys():
        if not player.bench_full():
            temp_slot = player.bench_vacancy()
            player.bench[temp_slot] = pool.sample(player, 1, augment['true_twos'][0] - 1)[0]
            player.bench[temp_slot].stars = 2
        if not player.bench_full():
            temp_slot = player.bench_vacancy()
            player.bench[temp_slot] = pool.sample(player, 1, augment['true_twos'][1] - 1)[0]
            player.bench[temp_slot].stars = 2
    elif 'urfs_grab_bag' == augment.keys():
        for x in range(augment.values()):
            if not player.item_bench_full(1):
                if x == 0:
                    player.item_bench[player.item_bench_vacancy()] = 'spatula'
                else:
                    r = random.randint(0, len(starting_items) - 1)
                    player.item_bench[player.item_bench_vacancy()] = starting_items[r]
    elif 'windfall' == augment.keys():
        if player.round == 3:
            player.gold += augment['windfall'][0]
        if player.round == 10:
            player.gold += augment['windfall'][1]
        if player.round == 16:
            player.gold += augment['windfall'][2]


def give_random_item(player):
    if not player.item_bench_full(1):
        r = random.randint(0, len(thiefs_gloves_items) - 1)
        player.item_bench[player.item_bench_vacancy()] = thiefs_gloves_items[r]


def start_of_battle_augments(team, enemy):
    if team and len(team[0].augments) > 0:
        for x in range(len(team[0].augments)):
            if team[0].augments[x][0] == 'ascension':
                for champ in team:
                    champ.add_que('execute_function', 15000, [ascension, {team[0].augments[x][1]}])
            elif team[0].augments[x][0] == 'axiom_arc':
                for champ in team:
                    champ.axiom_arc = team[0].augments[x][1]
            elif team[0].augments[x][0] == 'battlemage':
                for champ in team:
                    if 2 <= champ.y <= 5:
                        champ.SP += team[0].augments[x][1][0]
                        champ.armor += team[0].augments[x][1][1]
            elif team[0].augments[x][0] == 'big_friend':
                for champ in team:
                    big_friend = False
                    for allies in field.allies_in_distance(champ, champ.y, champ.x, 1):
                        if allies.health >= team[0].augments[x][1][0] and not big_friend:
                            champ.big_friend -= team[0].augments[x][1][1]
                            big_friend = True
            elif team[0].augments[x][0] == 'binary_airdrop':
                for champ in team:
                    if len(champ.items) == 2:
                        r = random.randint(0, len(thiefs_gloves_items) - 1)
                        champ.items.append(thiefs_gloves_items[r])
            elif team[0].augments[x][0] == 'blue_battery':
                for champ in team:
                    champ.SP = team[0].augments[x][1][0]
                    champ.blue_battery = team[0].augments[x][1][1]
            elif team[0].augments[x][0] == 'built_different':
                for champ in team:
                    built_dif = True
                    for trait in champ.origin:
                        if origin_class.get_origin_class_tier(champ.team, trait) != 0:
                            built_dif = False
                    if built_dif:
                        champ.max_health += team[0].augments[x][1][0]
                        champ.health += team[0].augments[x][1][0]
                        champ.AS *= team[0].augments[x][1][1]
            elif team[0].augments[x][0] == 'celestial_blessing':
                for champ in team:
                    champ.lifesteal += team[0].augments[x][1][0]
                    champ.lifesteal_spells += team[0].augments[x][1][0]
                    champ.celestial_blessing += team[0].augments[x][1][1]
            elif team[0].augments[x][0] == 'combat_training':
                for champ in team:
                    champ.combat_training_iteration = team[0].augments[x][1][0]
                    champ.AD += champ.combat_training + team[0].augments[x][1][1]
            elif team[0].augments[x][0] == 'cybernetic_implants':
                for champ in team:
                    champ.max_health += team[0].augments[x][1][0]
                    champ.health += team[0].augments[x][1][0]
                    champ.AD += team[0].augments[x][1][1]
            elif team[0].augments[x][0] == 'cybernetic_shell':
                for champ in team:
                    champ.max_health += team[0].augments[x][1][0]
                    champ.health += team[0].augments[x][1][0]
                    champ.armor += team[0].augments[x][1][1]
            elif team[0].augments[x][0] == 'cybernetic_uplink':
                for champ in team:
                    champ.max_health += team[0].augments[x][1][0]
                    champ.health += team[0].augments[x][1][0]
                    champion.change_stat(champ, None, 1000, ['cybernetic_uplink', {}], 'mana',
                                         champ.mana + team[0].augments[x][1][1], {})
            elif team[0].augments[x][0] == 'double_trouble':
                for champ in team:
                    double_trouble = False
                    for ally in team:
                        if champ.name == ally.name:
                            double_trouble = True
                    if double_trouble:
                        champ.AD += team[0].augments[x][1]
                        champ.SP += team[0].augments[x][1]
                        champ.MR += team[0].augments[x][1]
                        champ.armor += team[0].augments[x][1]
            elif team[0].augments[x][0] == 'electrocharge':
                for champ in team:
                    champ.electrocharge = team[0].augments[x][1]
            elif team[0].augments[x][0] == 'exiles':
                for champ in team:
                    if not field.allies_in_distance(champ, champ.y, champ.x, 1):
                        champion.shield(champ, None, None, None, None, champ.health * team[0].augments[x][1], {})
            elif team[0].augments[x][0] == 'featherweights':
                for champ in team:
                    if COST.get(champ.name) == 1 or COST.get(champ.name) == 2:
                        champ.AS *= team[0].augments[x][1]
                        champ.movement_delay *= 1 / team[0].augments[x][1]
            elif team[0].augments[x][0] == 'first_aid_kit':
                for champ in team:
                    champ.healing_strength += team[0].augments[x][1]
            elif team[0].augments[x][0] == 'jeweled_lotus':
                for champ in team:
                    champ.crit_chance += team[0].augments[x][1]
                    champ.jeweled_lotus = True
            elif team[0].augments[x][0] == 'knifes_edge':
                for champ in team:
                    if 2 <= champ.y <= 5:
                        champ.AD += team[0].augments[x][1]
            elif team[0].augments[x][0] == 'last_stand' and team[0].last_stand:
                for champ in team:
                    champ.max_health += team[0].augments[x][1][0]
                    champ.health += team[0].augments[x][1][0]
                    champ.armor += team[0].augments[x][1][1]
                    champ.MR += team[0].augments[x][1][1]
                    champ.lifesteal += team[0].augments[x][1][2]
                    champ.lifesteal_spells += team[0].augments[x][1][2]
            elif team[0].augments[x][0] == 'ludens_echo':
                for champ in team:
                    champ.ludens_echo += team[0].augments[x][1]
            elif team[0].augments[x][0] == 'makeshift_armor':
                for champ in team:
                    if not champ.items:
                        champ.MR += team[0].augments[x][1]
                        champ.armor += team[0].augments[x][1]
            elif team[0].augments[x][0] == 'scoped_weapons':
                for champ in team:
                    if champ.y <= 1 or champ.y >= 6:
                        champ.range += team[0].augments[x][1][0]
                        champ.AS *= team[0].augments[x][1][1]
            elif team[0].augments[x][0] == 'second_wind':
                for champ in team:
                    champ.add_que('execute_function', 15000, [second_wind, {team[0].augments[x][1]}])
            elif team[0].augments[x][0] == 'stand_united':
                if team[0].team_tiers:
                    traits = {key: value for (key, value) in team[0].team_tiers.items() if value > 0}
                    for champ in team:
                        champ.AD += team.augments[x][1][0] * len(list(traits.values()))
                        champ.SP += team.augments[x][1][1] * len(list(traits.values()))
            elif team[0].augments[x][0] == 'sunfire_board':
                for champ in enemy:
                    champ.burn(champ)
            elif team[0].augments[x][0] == 'thrill_of_the_hunt':
                for champ in team:
                    champ.thrill_of_the_hunt = team[0].augments[x][1]
            elif team[0].augments[x][0] == 'tri_force':
                for champ in team:
                    if champ.cost == 3:
                        champ.max_health += team[0].augments[x][1][0]
                        champ.health += team[0].augments[x][1][0]
                        champ.mana += team[0].augments[x][1][1]
                        champ.AS *= team[0].augments[x][1][2]
            elif team[0].augments[x][0] == 'verdant_veil':
                for champ in team:
                    champ.verdant_veil = team[0].augments[x][1][0]
                    champ.AS *= team[0].augments[x][1][1]


def start_of_round_augments(player):
    if 'afk' in player.augment_dict:
        player.afk_turn_count += 1
        if player.afk_turn_count == 3:
            player.gold += player.augment_dict['afk']
            player.augment_dict.pop('afk')
    if player.loss_streak != 0 and 'calculated_loss' in player.augment_dict:
        player.gold += player.augment_dict['calculated_loss']
        player.free_refreshes += 1
    if 'clear_mind' in player.augment_dict:
        clear_mind(player, player.augment_dict['clear_mind'])
    if 'cluttered_mind' in player.augment_dict:
        cluttered_mind(player, player.augment_dict['cluttered_mind'])
    if 'cruel_pact' in player.augment_dict:
        if player.health + player.augment_dict['cruel_pact'][1] <= player.max_health:
            player.health += player.augment_dict['cruel_pact'][1]
    if 'living_forge' in player.augment_dict and player.round in player.augment_dict['living_forge']:
        if not player.item_bench_full(1):
            player.item_bench[player.item_bench_vacancy()] = 'infinity_force'
    if 'metabolic_accelerator' in player.augment_dict:
        if player.health + player.augment_dict['metabolic_accelerator'] <= player.max_health:
            player.health += player.augment_dict['metabolic_accelerator']
    if 'pandoras_bench' in player.augment_dict:
        pandoras_bench_funct(player)
    if 'pandoras_items' in player.augment_dict:
        pandoras_items_funct(player)
    if 'preparation' in player.augment_dict:
        preparation(player)


def ascension(a_champion, value):
    x = list(value)[0]
    a_champion.add_que('change_stat', -1, False, 'ascension_value', x)


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
        champion.spell(enemy, value, 0, False, False, True)
    return True


def pandoras_bench_funct(player):
    for slot in range(6, 8):
        if player.bench[slot]:
            temp_star = player.bench[slot].stars
            temp_cost = player.bench[slot].cost
            player.sell_from_bench(slot, golden=False)
            player.gold -= cost_star_values[temp_cost - 1][temp_star - 1]
            name = player.pool_obj.sample(player, 1, temp_cost - 1)[0]
            player.bench[slot] = champion.champion(name, itemlist=[], augments=player.augments,
                                    kayn_form=player.kayn_form, last_stand=player.last_stand_activated,
                                    round_num=player.round, stars=temp_star)
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


def portable_forge(player):
    if not player.item_bench_full(player):
        player.item_bench[player.item_bench_vacancy(player)] = 'infinity_force'


def preparation(player):
    for slot in player.bench:
        if slot:
            slot.preparation_stacks += 1
            if slot.preparation_stacks <= player.augment_dict['preparation'][0]:
                slot.max_health += player.augment_dict['preparation'][1]
                slot.health += player.augment_dict['preparation'][1]
                slot.AD += player.augment_dict['preparation'][2]
                slot.SP += player.augment_dict['preparation'][2]


def recombobulate(player):
    for x in range(7):
        for y in range(4):
            if player.board[x][y]:
                temp_star = player.board[x][y].stars
                temp_cost = player.board[x][y].cost
                player.sell_champion(player.board[x][y], False, False)
                player.gold -= cost_star_values[temp_cost - 1][temp_star - 1]
                player.board[x][y] = pool.sample(player, 1, player.board[x][y].cost)[0]
                player.board[x][y].stars = temp_star


def second_wind(a_champion, value):
    x = list(value)[0]
    a_champion.add_que('heal', -1, None, None, x * (a_champion.max_health - a_champion.health))


def woodland_charm(player, team):
    if 'woodland_charm' in player.augment_dict:
        most_health = 0
        biggest_champ = None
        for champ in team:
            if champ.health > most_health:
                most_health = champ.health
                biggest_champ = champ
        hexes = field.hexes_distance_away(biggest_champ.x, biggest_champ.y, 1, False)
        for x in range(len(hexes)):
            if hexes[x][0] <= 3:
                if not player.board[hexes[x][1]][hexes[x][0]]:
                    team.append(champion.champion(biggest_champ.name, biggest_champ.team, hexes[x][0], hexes[x][1],
                                                  biggest_champ.stars, None, False, None, False, biggest_champ.kayn_form
                                                  , biggest_champ.team_tiers, False, hexes[x][0], hexes[x][1],
                                                  biggest_champ.last_stand, biggest_champ.round_num,
                                                  biggest_champ.augments))
                    team[-1].health *= player.augment_dict['woodland_charm']
                    team[-1].max_health *= player.augment_dict['woodland_charm']
                    return True
