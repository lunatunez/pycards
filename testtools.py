import blinds
import deck
import sessions
import names
import player
import pokerhands
import table

STARTINGCHIPS = 1000

HANDS = (pokerhands.make('royalflush'),
         pokerhands.make('straightflush_high'),
         pokerhands.make('fullhouse_high'),
         pokerhands.make('flush_high'),
         pokerhands.make('straight_high'),
         pokerhands.make('trips_high')
         )


def make(num, hero=None):
    # The hero variable lets someone pass in a Human player name
    # If they don't want any human players, just let it be None.

    t = table.Table(num)
    nameset = names.random_names(num)

    for i, s in enumerate(t.seats):
        # Always put hero in 0 seat.
        if i == 0 and hero is not None:
            t.add_player(0, player.Player(hero, 'HUMAN'))

        elif nameset[-1] is not None:
            t.add_player(i, "CPU")
        else:
            nameset.pop()
        t.seats[i].chips = STARTINGCHIPS
    return t


def test_table(seats, cards=False, CHIPS=STARTINGCHIPS):
    # Populate a Table of the specified # of seats with players.
    # This table doesn't have button or blinds set.
    t = table.Table(seats)

    for i in range(seats):
        t.add_player(i, player.Player('bob{}'.format(i), 'CPU'))
        t.seats[i].chips = STARTINGCHIPS

    if cards:
        deal_table_cards(t, 5)
    return t


def allin_table(seats, REVERSEHANDS=False):
    # Populates a table with different levels of stack sizes by 100's
    # ex: 100, 200, 300, 400, etc.
    DEFAULT_CHIPS = 100
    t = test_table(seats)

    for i, p in enumerate(t):
        p.chips = DEFAULT_CHIPS * (i + 1)

    if REVERSEHANDS is True:
        deal_hands_weakfirst(t)
    else:
        deal_hands_strongfirst(t)
    return t


def deal_table_cards(table, qty=5):
    d = deck.Deck()

    for p in table:
        for i in range(qty):
            p.add_card(d.deal())


def get_cards(quantity):
    d = deck.Deck()
    d.shuffle()
    for c in d.cards:
        c.hidden = False
    return [d.deal() for i in range(quantity)]


def deal_hands_strongfirst(table):
    # Deal out the hands: strongest first
    for i, s in enumerate(table.seats):
        s._hand.cards = HANDS[i]


def deal_hands_weakfirst(table):
    # Deal out the hands: strongest first
    reversed_hands = list(reversed(HANDS))
    for i, s in enumerate(table.seats):
        s._hand.cards = list(reversed_hands[i])


def deallist(table, cards, faceup=False):
    if faceup:
        for c in cards:
            c.hidden = False

    for p in table:
        p.add_card(cards.pop(0))


def deal_stud(table, qty, matchingranks=0):
    down = pokerhands.convert_to_cards(['As', 'Ks', 'Qs', 'Js', 'Ts', '9s',
                                        '2d', '3d', '4d', '2s', '3s', '4s'])
    if qty == 2:
        deallist(table, down)
    elif qty == 3:
        deallist(table, down)
        deallist(table, down)
    else:
        raise Exception('bad qty!')

    if matchingranks == 0:
        up = pokerhands.convert_to_cards(['Ah', 'Kh', 'Qh', 'Jh', 'Th', '9h'])
    elif matchingranks == 2:
        up = pokerhands.convert_to_cards(['5h', '5c', 'Qh', 'Jh', 'Th', '9h'])
    elif matchingranks == 3:
        up = pokerhands.convert_to_cards(['5s', '5c', 'Qh', 'Jh', '5d', '9h'])
    elif matchingranks == 4:
        up = pokerhands.convert_to_cards(['5s', '5c', 'Qh', 'Jh', '5d', '5h'])
    else:
        raise Exception('bad matchingranks #, 0, 2, 3, or 4!')

    deallist(table, up, faceup=True)


def make_game_table(num, gametype, playertype, heroname):
    # The hero variable lets someone pass in a Human player name
    # If they don't want any human players, just let it be None.

    t = table.Table(num)

    nameset = names.random_names(num)
    # Add the hero to seat 0
    t.add_player(0, player.Player(heroname, 'HUMAN'))

    for i, s in enumerate(t.seats):
        if s is None:
            if gametype == "FIVE CARD DRAW":
                t.add_player(i, player.Player5Card(nameset.pop(), playertype))
            elif gametype == "FIVE CARD STUD":
                t.add_player(i, player.Player5Stud(nameset.pop(), playertype))

        else:
            nameset.pop()
        t.seats[i].chips = STARTINGCHIPS
    return t


def get_draw5_sesh_1_2_blinds():
    STAKES = blinds.Blinds()
    table = test_table(6)
    return sessions.Draw5Session('FIVE CARD DRAW', table, STAKES)


def get_dealt_table(hands):
    t = test_table(len(hands))
    for k, v in hands.items():
        t.seats[k]._hand.cards = pokerhands.convert_to_cards(v)
    return t

"""
Table factory.
"""
STARTINGCHIPS = 1000
STEP = 100


class BobTable(table.Table):
    """
    Creates a table of bobs with the default chip stack.
    """
    def __init__(self, seats):
        super().__init__(seats)

        for i, s in enumerate(self.seats):
            self.add_player(i, player.Player('bob{}'.format(i), 'CPU'))
            self.seats[i].chips = STARTINGCHIPS
            #  s.chips = STARTINGCHIPS


class SteppedStackTable(table.Table):
    """
    Creates a table of bobs with stack sizes starting from 100 and increasing in 100's for
    each seat.
    """
    def __init__(self, seats):
        super().__init__(seats)

        for i, s in enumerate(self.seats):
            self.add_player(i, player.Player('bob{}'.format(i), 'CPU'))
            self.seats[i].chips = STEP * (i + 1)
