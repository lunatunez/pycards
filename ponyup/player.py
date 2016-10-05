import os
import pickle
import random
from ponyup import draw5_plyr
from ponyup import names
from ponyup import stud5_plyr

TYPES = ['FISH', 'JACKAL', 'MOUSE', 'LION']
DATADIR = 'data/'
HUMAN_BANK_BITS = 1000


class Player():
    def __init__(self, name, playertype=None):
        self.set_name(name)
        self.bank = 0

        if playertype is None:
            # Choose random player type
            rnd_type = random_type()
            self.playertype = rnd_type
        else:
            self.playertype = playertype

    def __str__(self):
        """
        Returns the player's name.
        """
        return '{}'.format(self.name)

    def data(self):
        _str = 'Data for player: {}'.format(self.name)

        return _str

    def __repr__(self):
        """
        Same as str, returns name.
        """
        return str(self)

    def set_name(self, name):
        """
        Checks the player name, and sets it if valid. Raises an exception if not valid.
        """
        if names.is_validname(name):
            self.name = name
        else:
            raise ValueError('Invalid username "{}" for object!'.format(name))

    def withdraw(self, amt):
        """
        Removes the amount given from the player's stack and returns it. If the amount is more
        than the player has, then the remaining amount in the player's stack is remoevd and
        returned.
        """
        if amt < 0:
            raise ValueError('Player cannot bet a negative amount!')
        if amt > self.bank:
            # Put the player all-in
            amt = self.bank
            self.bank = 0
            return amt
        else:
            self.bank -= amt
            return amt

    def deposit(self, amt):
        """
        Adds the specified amount of chips to the player's stack.
        """
        if amt < 0:
            raise Exception('Cannot add negative chips!')
        else:
            self.bank += amt

    def is_human(self):
        """
        Returns True if the player is a HUMAN type, False otherwise.
        """
        return self.playertype == 'HUMAN'


def random_type():
    return random.choice(TYPES)


def factory(name, game, playertype='random'):
    """
    Create a new Player, using the game strategy from the game specified.
    """
    p = Player(name, playertype)

    if playertype == 'random':
        playertype = random_type()

    if game == "FIVE CARD DRAW":
        p.strategies = draw5_plyr.strat[playertype]
    elif game == "FIVE CARD STUD":
        p.strategies = stud5_plyr.strat[playertype]
    elif game is None:
        p.strategies = None

    return p


def mk_filename(name):
    return DATADIR + name + '.dat'


def load_player(name):
    """
    Gets the username, checks for any previous player info and loads the player. If no player
    file it creates a new one. Returns a Player object.
    """
    userfile = mk_filename(name)
    try:
        with open(userfile, 'rb') as f:
            plyr = pickle.load(f)
            return plyr
    except IOError:
        return None


def player_exists(name):
    return os.path.isfile(mk_filename(name))


def del_player(name):
    if player_exists(name):
        print('Are you sure you want to delete player: {}?'.format(name))
        choice = input('[y/n] :> ')
        if choice.lower().startswith('y'):
            try:
                os.remove(mk_filename(name))
                return True
            except Exception:
                return False
    else:
        return False


def create_player(name):
    if player_exists(name):
        return None
    else:
        try:
            p = Player(name, playertype="HUMAN")
            p.deposit(HUMAN_BANK_BITS)
            save_player(p)
            return p
        except ValueError:
            return None


def save_player(plyr):
    """
    Saves the Player current stats to file.
    """
    userfile = mk_filename(plyr.name)

    try:
        with open(userfile, 'wb') as f:
            pickle.dump(plyr, f)
            return True
    except IOError:
        return False