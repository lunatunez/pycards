from collections import namedtuple
import hand
import player
import pokerhands
import random

Ranges = namedtuple('Ranges', ['call1', 'call2', 'bet', 'raise1', 'raise2', 'bluff'])

FISH = {
    1: Ranges(
        call1=0,
        call2=pokerhands.PAIR_66,
        bet=0,
        raise1=pokerhands.PAIR_AA,
        raise2=pokerhands.PAIR_AA,
        bluff=0
    ),
    2: Ranges(
        call1=pokerhands.PAIR_22,
        call2=pokerhands.PAIR_JJ,
        bet=pokerhands.TWOPAIR_22,
        raise1=pokerhands.TWOPAIR_JJ,
        raise2=pokerhands.TRIPS,
        bluff=0
    ),
}

JACKAL = {
    1: Ranges(
        call1=pokerhands.HI_KT,
        call2=pokerhands.PAIR_66,
        bet=0,
        raise1=pokerhands.PAIR_66,
        raise2=pokerhands.PAIR_AA,
        bluff=0
    ),
    2: Ranges(
        call1=pokerhands.PAIR_JJ,
        call2=pokerhands.PAIR_AA,
        bet=pokerhands.PAIR_66,
        raise1=pokerhands.TWOPAIR_TT,
        raise2=pokerhands.TWOPAIR_KK,
        bluff=0
    ),
}

MOUSE = {
    1: Ranges(
        call1=pokerhands.TWOPAIR_KK,
        call2=pokerhands.TWOPAIR_TT,
        bet=0,
        raise1=pokerhands.TRIPS,
        raise2=pokerhands.STRAIGHT,
        bluff=0
    ),
    2: Ranges(
        call1=pokerhands.TWOPAIR_TT,
        call2=pokerhands.TRIPS,
        bet=pokerhands.TWOPAIR_TT,
        raise1=pokerhands.STRAIGHT,
        raise2=pokerhands.FLUSH,
        bluff=0
    ),
}

LION = {
    1: Ranges(
        call1=pokerhands.PAIR_88,
        call2=pokerhands.PAIR_KK,
        bet=0,
        raise1=pokerhands.PAIR_JJ,
        raise2=pokerhands.TRIPS,
        bluff=0
    ),
    2: Ranges(
        call1=pokerhands.TWOPAIR_TT,
        call2=pokerhands.TRIPS,
        bet=pokerhands.PAIR_KK,
        raise1=pokerhands.TRIPS,
        raise2=pokerhands.STRAIGHT,
        bluff=0
    ),
}

TYPES = {
    'FISH': FISH,
    'JACKAL': JACKAL,
    'MOUSE': MOUSE,
    'LION': LION,
}


class Player5Card(player.Player):
    def __init__(self, name, playertype=None):
        self.set_name(name)
        self._type = playertype
        self.strategies = {}
        if playertype is None:
            random_playertype = random.choice(list(TYPES.keys()))
            self.strategies = TYPES[random_playertype]
        elif playertype not in TYPES:
            raise ValueError('type argument is not valid.')
        else:
            self.strategies = TYPES[playertype]

        self.chips = 0
        self._hand = hand.Hand()
