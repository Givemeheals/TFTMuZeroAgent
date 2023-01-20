import numpy as np

PRINTMESSAGES = True
LOGMESSAGES = True
MANA_DAMAGE_GAIN = 0.06
MAX_MANA_FROM_DAMAGE = 42.5

MOVEMENTDELAY = 550
STARMULTIPLIER = 1.8

ATTACK_PASSIVES = ['vayne', 'jhin', 'kalista', 'warwick', 'zed']

MANA_PER_ATTACK = 10

BURN_SECONDS = 10
BURN_DMG_PER_SLICE = 0.025
BURN_HEALING_REDUCE = 0.5

MINION_ROUNDS = [0, 1, 2, 9, 17]
AUGMENT_ROUNDS = [3, 11, 19]

# unit name
CHOSEN = None

GALIO_MULTIPLIER = 0.14
GALIO_TEAM_HEALTH_PERCENTAGE = 0.50

WARLORD_WINS = {'blue': 0, 'red': 0}

LEAP_DELAY = 395  # assassins and shades

## AI RELATED VALUES START HERE

#### MODEL SET UP ####
BATCH_SIZE = 64
LSTM_SIZE = 256
HIDDEN_TENSOR_SIZE = 256
HIDDEN_STATE_SIZE = 512
HEAD_HIDDEN_SIZE = 1024
N_HEAD_HIDDEN_LAYERS = 1
ROOT_DIRICHLET_ALPHA = 0.03
ROOT_EXPLORATION_FRACTION = 0.25
MINIMUM_REWARD = -1.0
MAXIMUM_REWARD = 1.0
PB_C_BASE = 19652
PB_C_INIT = 1.25
DISCOUNT = 0.997
TRAINING_STEPS = 1e10
CORE_LSTM_LAYERS = 2
OBSERVATION_SIZE = 4665
OBSERVATION_TIME_STEPS = 5
OBSERVATION_TIME_STEP_INTERVAL = 4
INPUT_SHAPE = np.array([OBSERVATION_SIZE])
ACTION_CONCAT_SIZE = 10
# ACTION_DIM = [10, 5, 9, 10, 7, 4, 7, 4]
ACTION_DIM = 10
ENCODER_NUM_STEPS = 601

### TIME RELATED VALUES ###
NUM_SIMULATIONS = 25
NUM_PLAYERS = 8
SAMPLES_PER_PLAYER = 256
UNROLL_STEPS = 4
ACTIONS_PER_TURN = 25
CONCURRENT_GAMES = 16

#### TRAINING ####
INIT_LEARNING_RATE = 0.01
LEARNING_RATE_DECAY = int(350e3)
LR_DECAY_FUNCTION = 0.1
WEIGHT_DECAY = 1e-5
REWARD_LOSS_SCALING = 0
POLICY_LOSS_SCALING = 1
# Putting this here so that we don't scale the policy by a multiple of 5
# Because we calculate the loss for each of the 5 dimensions.
# I'll add a mathematical way of generating these numbers later.
DEBUG = True

#### TESTING ####
RUN_UNIT_TEST = True
RUN_PLAYER_TESTS = True
RUN_MINION_TESTS = False
LOG_COMBAT = False
