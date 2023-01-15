# need to update scaling augments
# augments are stored as single elements of 2d arrays
# the comments tell what the values associated with the augments do in the order listed
silver_augments = {
    'afk':                  20,         # the amount of gold you get
    'band_of_thieves':      1,          # the number of thieves gloves it gives
    'battlemage':           [15, 15],   # AP given, armor given
    'big_friend':           [1600, 0.07],   # neighboring health cutoff, damage reduction
    'celestial_blessing':   [0.1, 200], # % lifesteal given, max shielding
    'consistency':          2,          # the streak multiplier
    'cybernetic_implants':  [80, 10],   # health given, AD given
    'cybernetic_shell':     [80, 20],   # health given, armor given
    'cybernetic_uplink':    [80, 2],    # health given, mana per second given
    'electrocharge':        60,         # damage dealt
    'exiles':               0.25,       # % health shielded at the start of combat
    'featherweights':       1.2,        # the number AS and MS is multiplied by
    'first_aid_kit':        0.25,       # % healing is increased by
    'future_sight':         1,          # the number of zephyrs given (since radiant items not yet implimented)
    'item_grab_bag':        1,          # the number of items given
    'knifes_edge':          25,         # AD given
    'lategame_specialist':  40,         # gold given at level 9
    'ludens_echo':          60,         # damage dealt
    'makeshift_armor':      30,         # armor and MR given
    'pandoras_bench':       0,          # unused
    'pandoras_items':       0,          # unused
    'preparation':          [4, 25, 3], # max stacks, health per stack, AD and SP per stack
    'recombobulator':       0,          # unused
    'second_wind':          0.4,        # % of missing health restored
    'stand_united':         [1.5, 2],   # AD given per trait, SP given per trait
    'thrill_of_the_hunt':   350,        # health healed on kill
    'tiny_titans':          30,         # amount health is increased by
    'tri_force':            [75, 10, 1.1]   # health given, mana given, AS multiplier
}

gold_augments = {
    'ancient_archives':     1,          # number of tome of traits given
    'ascension':            1.5,        # ascension damage multiplier
    'axiom_arc':            30,         # amount of mana given on kill
    'battlemage':           [25, 25],   # AP given, armor given
    'big_friend':           [1600, 0.12],   # neighboring health cutoff, damage reduction
    'blue_battery':         [20, 10],   # AP given, the number mana is set to after spell cast
    'built_different':      [250, 1.55],    # health given, AS given
    'calculated_loss':      2,          # gold given per loss
    'celestial_blessing':   [0.15, 300],    # % lifesteal given, max shielding
    'clear_mind':           3,          # xp gained per turn
    'cluttered_mind':       3,          # xp gained per turn
    'combat_training':      [1, 8],     # the amount of AD given per kill, AD given by augment
    'component_grab_bag':   3,          # the number of components given
    'cybernetic_implants':  [120, 20],  # health given, AD given
    'cybernetic_shell':     [120, 30],  # health given, armor given
    'cybernetic_uplink':    [120, 3],   # health given, mana per second given
    'double_trouble':       30,         # AD, SP, armor and MR given
    'electrocharge':        80,         # damage dealt
    'exiles':               0.35,       # % health shielded at the start of combat
    'featherweights':       1.3,        # the number AS and MS is multiplied by
    'first_aid_kit':        0.35,       # % healing is increased by
    'hustler':              3,          # amount of gold given instead of interest
    'jeweled_lotus':        0.2,        # amount added to crit chance
    'knifes_edge':          35,         # AD given
    'last_stand':           [180, 18, 0.18],    # health given, armor and MR given, omnivamp given
    'ludens_echo':          80,         # damage dealt
    'makeshift_armor':      45,         # armor and MR given
    'metabolic_accelerator':2,          # health gained per turn
    'phony_frontline':      2,          # the number of target dummies given
    'portable_forge':       0,          # unused
    'preparation':          [4, 35, 4], # max stacks, health per stack, AD and SP per stack
    'rich_get_richer':      [7, 12],    # the max interest, gold given
    'salvage_bin':          0,          # unused
    'scoped_weapons':       [2, 1.1],   # range added, AS multiplier
    'second_wind':          0.6,        # % of missing health restored
    'stand_united':         [2.5, 3],   # AD given per trait, SP given per trait
    'sunfire_board':        0,          # unused
    'threes_company':       3,          # of three cost champions given
    'thrill_of_the_hunt':   550,        # health healed on kill
    'tri_force':            [125, 15, 1.15],    # health given, mana given, AS multiplier
    'true_twos':            [1, 2]      # cost values of the two 2* champions given
}

prismatic_augments = {
    'ancient_archives':     2,          # number of tome of traits given
    'band_of_thieves':      2,          # of thieves gloves given
    'battlemage':           [35, 35],   # AP given, armor given
    'binary_airdrop':       0,          # unused
    'birthday_present':     0,          # unused
    'built_different':      [350, 1.65],    # health given, AS given
    'celestial_blessing':   [0.25, 400],    # % lifesteal given, max shielding
    'cruel_pact':           [6, 3],     # health cost to buy exp, health gained per turn
    'cursed_crown':         2,          # the number of extra units on board
    'cybernetic_implants':  [200, 30],  # health given, AD given
    'cybernetic_shell':     [200, 40],  # health given, armor given
    'cybernetic_uplink':    [200, 3],   # health given, mana per second given
    'double_trouble':       40,         # AD, SP, armor and MR given
    'electrocharge':        140,        # damage dealt
    'featherweights':       1.5,        # the number AS and MS is multiplied by
    'future_sight':         2,          # the number of zephyrs given (radiant items not yet implimented)
    'golden_ticket':        50,         # % chance for a free refresh
    'high_end_shopping':    0,          # unused
    'high_roller':          3,          # the number of champion duplicators given (loaded dice not yet implimented)
    'item_grab_bag':        2,          # the number of items given
    'knifes_edge':          45,         # AD given
    'level_up':             7,          # exp given whenever xp is bought
    'living_forge':         [4, 14, 24],    # rounds an item is given on
    # 'lucky_gloves':         0,
    'ludens_echo':          130,        # damage dealt
    'march_of_progress':    5,          # amount of bonus xp per round
    'new_recruit':          0,          # unused
    'preparation':          [4, 50, 7], # max stacks, health per stack, AD and SP per stack
    'radiant_relics':       0,          # unused
    'stand_united':         [3.5, 4],   # AD given per trait, SP given per trait
    # 'the_golden_egg':       0,
    'think_fast':           100,        # the amount of free refreshes given
    'tri_force':            [200, 25, 1.25],    # health given, mana given, AS multiplier
    'urfs_grab_bag':        4,          # number of items given (including spatula)
    'verdant_veil':         [20, 1.15], # of seconds of cc immunity, AS multiplier
    'windfall':             [25, 35, 45],   # amount of gold given at each respective augment round
    'wise_spending':        2,          # exp per shop refresh
    'woodland_charm':       1           # clone health multiplier
}
