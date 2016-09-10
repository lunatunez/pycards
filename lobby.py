from collections import namedtuple
import blinds

Game = namedtuple('Game', ['name', 'seats', 'level', 'game'])

"""
This lobby listing is a list of all the available cash tables a pony can play
at. Each has: Table name, seats, stakes level, game type.
"""

# 'CMC Clubhouse' in [n.name for n in l]


def sort_by_name(L):
    return sorted(L, key=lambda x: x.name)


def sort_by_level(L):
    return sorted(L, key=lambda x: x.level)


def get_games(L, game):
    return [x for x in L if x.game == game]


def stakes(gametuple):
    """
    Return the small bet and big bet sizes.
    """
    if gametuple.game == "FIVE CARD STUD":
        sb = blinds.ante[gametuple.level][0]
        return '${}/${}'.format(sb, sb*2)
    elif gametuple.game == "FIVE CARD DRAW":
        sb = blinds.no_ante[gametuple.level][0]
        return '${}/${}'.format(sb, sb*2)


def display_numbered_list(L):
    _str = ''
    fmt_str = '{:4}: {:25} {:9} {:6} {}\n'
    print(fmt_str.format('', 'Table Name', 'Stakes', 'Seats', 'Game'))
    for i, k in enumerate(L):

        _stakes = stakes(k)
        _str += (fmt_str.format(i, k.name, _stakes, k.seats, k.game))
    return _str


# TABLENAME | TABLE SIZE | STAKES | GAME
tables = (
    # Headsup
    #  Game('Twilight\'s Balloon', seats=2, level=2, game="FIVE CARD DRAW"),
    #  Game('Rainbow Dash\'s House', seats=2, level=3, game="FIVE CARD DRAW"),
    #  Game('Ponyville Tower', seats=2, level=5, game="FIVE CARD DRAW"),
    Game('Zecora\'s Hut', seats=2, level=8, game="FIVE CARD DRAW"),
    Game('Trixie\'s Wagon', seats=2, level=10, game="FIVE CARD DRAW"),

    # 3max
    #  Game('Twilight\'s Lab', seats=3, level=2, game="FIVE CARD DRAW"),
    #  Game('CMC Clubhouse', seats=3, level=3, game="FIVE CARD DRAW"),
    #  Game('Mr. Breezy\'s Fan shop', seats=3, level=5, game="FIVE CARD DRAW"),
    Game('Fluttershy\'s cottage', seats=3, level=8, game="FIVE CARD DRAW"),
    Game('Quills and Sofas', seats=3, level=10, game="FIVE CARD DRAW"),

    # 6max
    #  Game('Golden Oak Library', seats=6, level=2, game="FIVE CARD DRAW"),
    #  Game('Carousel Boutique', seats=6, level=3, game="FIVE CARD DRAW"),
    #  Game('Sugarcube Corner', seats=6, level=5, game="FIVE CARD DRAW"),
    Game('Pinkie\'s Party Cavet', seats=6, level=8, game="FIVE CARD DRAW"),
    Game('Cutie Map', seats=6, level=10, game="FIVE CARD DRAW"),

    # 8max
    #  Game('Apple Acres', seats=8, level=2, game="FIVE CARD DRAW"),
    #  Game('Ponyville Schoolhouse', seats=8, level=3, game="FIVE CARD DRAW"),
    #  Game('Wonderbolt Academy', seats=8, level=5, game="FIVE CARD DRAW"),
    Game('Rainbow Factory', seats=8, level=8, game="FIVE CARD DRAW"),
    Game('Mirror Pool', seats=8, level=10, game="FIVE CARD DRAW"),

    # ### 5-card stud
    # HU
    #  Game('Everfree Forest', seats=2, level=2, game="FIVE CARD STUD"),
    #  Game('White Tail Woods', seats=2, level=3, game="FIVE CARD STUD"),
    #  Game('Galloping Gorge', seats=2, level=5, game="FIVE CARD STUD"),
    Game('Froggy Bottom Bogg', seats=2, level=8, game="FIVE CARD STUD"),
    Game('Dragon Lands', seats=2, level=10, game="FIVE CARD STUD"),

    # 3max
    #  Game('Raket Range', seats=3, level=2, game="FIVE CARD STUD"),
    #  Game('Crystal Mountains', seats=3, level=3, game="FIVE CARD STUD"),
    #  Game('Friffish Islaes', seats=3, level=5, game="FIVE CARD STUD"),
    Game('Unicorn Range', seats=3, level=8, game="FIVE CARD STUD"),
    Game('Saddle Lake', seats=3, level=10, game="FIVE CARD STUD"),

    # 6max
    #  Game('Horseshoe Bay', seats=6, level=2, game="FIVE CARD STUD"),
    #  Game('San Palomino Desert', seats=6, level=3, game="FIVE CARD STUD"),
    #  Game('Dragon Lands', seats=6, level=5, game="FIVE CARD STUD"),
    Game('Winsome Falls', seats=6, level=8, game="FIVE CARD STUD"),
    Game('Tenochtitlan Basin', seats=6, level=8, game="FIVE CARD STUD"),

    # 8max
    #  Game('Mount Everhoof', seats=8, level=2, game="FIVE CARD STUD"),
    #  Game('Ghastly Gorge', seats=8, level=3, game="FIVE CARD STUD"),
    #  Game('Hollow Shades', seats=8, level=5, game="FIVE CARD STUD"),
    Game('Dodge Junction', seats=8, level=8, game="FIVE CARD STUD"),
    Game('Tartarus', seats=8, level=10, game="FIVE CARD STUD"),
)
