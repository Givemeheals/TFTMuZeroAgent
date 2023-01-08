from Simulator.augment_stats import silver_augments, gold_augments, prismatic_augments
from Simulator import champion, field
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
    return [[option1, augment_tier.get(option1)], [option2, augment_tier.get(option2)],\
            [option3, augment_tier.get(option3)]]

def electrocharge(value, champion):
    for enemy in field.enemies_in_distance(champion, champion.y, champion.x, 1):
        champion.spell(enemy, value, 0, True)
    return True

def start_of_battle_augments(team):
    if team and len(team[0].augments) > 0:
        for x in range(len(team[0].augments) - 1):
            if team[0].augments[x][0] == 'battlemage':
                for champ in team:
                    champ.SP += champ.augments[x][1]
            elif team[0].augments[x][0] == 'big_friend':
                for champ in team:
                    for allies in field.allies_in_distance(champ, champ.y, champ.x, 1):
                        if allies.health >= champ.augments[x][1][0]:
                            champ.big_friend -= champ.augments[x][1][1]
            elif team[0].augments[x][0] == 'built_different':
                for champ in team:
                    for trait in champ.origin:
                        ...
                        #if trait in
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
                    champ.mana_per_second += champ.augments[x][1][1]
                    champ.mps_increased = True

