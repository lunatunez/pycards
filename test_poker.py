import unittest
import blinds
import card
import evaluator
import poker
import pokerhands
import table_factory
import testtools


class TestPoker(unittest.TestCase):
    """
    Setup a session and round, with a table filled with 6 players.
    """
    def setUp(self, level=2, players=6):
        # Make a 6 player table
        self.g = testtools.draw5_session(level, players)
        self.r = poker.Round(self.g)

    def setUp_stud(self, level=2, players=3):
        # Make a 6 player table
        self.g = testtools.stud5_session(level, players)
        self.r = poker.Round(self.g)
        #  self.r.post_bringin()

    def setup_allins(self, seats):
        self.g._table = table_factory.SteppedStackTable(seats)
        self.r = poker.Round(self.g)

        # For make_sidepots, get_allins need players to have cards.
        testtools.deal_random_cards(self.g._table, 2)

    def everybody_bet(self, bet):
        for s in self.r._table:
            self.r.pot += s.bet(bet)

    def givehand(self, seat, hand):
        self.r._table.seats[seat].hand.cards = pokerhands.make(hand)
        # Hide the 1st card
        self.r._table.seats[seat].hand.cards[0].hidden = True

    """
    Tests for __init__()
    """
    # Round __init__(): Pot = 0
    def test_newround_potis0(self):
        expected = 0
        result = self.r.pot
        self.assertEqual(expected, result)

    """
    Tests for __str__()
    """
    # None yet.

    """
    Tests for deal_cards(qty, faceup=False)
    """
    # 6 players, deal 1 - should be 6 cardholders
    def test_dealcards_deal1_6cardholders(self):
        self.r._table.move_button()
        self.r._table.set_blinds()
        self.r.deal_cards(1)
        expected = 6
        result = len(self.r._table.get_players(hascards=True))
        self.assertEqual(expected, result)

    # 6 players, deal 1 - decksize == 48
    def test_dealcards_deal1_decksize48(self):
        self.r.deal_cards(1)
        expected = 46
        result = len(self.r.d)
        self.assertEqual(expected, result)

    # 6 players, deal 1 (no keyword arg) - cards are hidden
    def test_dealcards_deal1_cardsarehidden(self):
        self.r.deal_cards(1)
        for s in self.r._table:
            expected = 0
            result = len(s.hand.get_upcards())
            self.assertEqual(expected, result)

    # 6 players, deal 1 (faceup=True) - cards are faceup
    def test_dealcards_deal1_faceup_cardsarenothidden(self):
        self.r.deal_cards(1, faceup=True)
        for s in self.r._table:
            self.assertFalse(s.hand.cards[0].hidden)

    # 5 players have cards, deal only to those that still have cards
    def test_dealcards_deal6deal5toands_deckis41cards(self):
        self.r.deal_cards(1)  # Deal 6 cards
        self.r._table.seats[0].fold()
        self.r.deal_cards(1, handreq=True)  # Deal 5 cards
        self.assertEqual(len(self.r.d), 41)

    """
    Tests show_cards()
    """
    # Deal cards to 2 players, should be able to see CPU cards

    """
    Tests for sortcards()
    """
    # deal highcards1():
    #  h = [('A', 'd'), ('4', 's'), ('Q', 's'), ('7', 's'), ('K', 'h')]
    def test_sortcards_humandealt_sorted(self):
        h = pokerhands.make('highcards')
        self.r._table.seats[0].hand.cards = h[:]
        expected = sorted(h)
        self.r.sortcards()
        result = self.r._table.seats[0].hand.cards
        self.assertEqual(expected, result)

    """
    Tests for muck_all_cards()
    """
    # 6 players, deal 1 - no cardholders after running
    def test_muckallcards_cardsmucked_nocardholders(self):
        self.r._table.move_button()
        self.r._table.set_blinds()
        self.r.deal_cards(1)
        self.r.muck_all_cards()
        expected = 0
        result = len(self.r._table.get_players(hascards=True))
        self.assertEqual(expected, result)

    # 6 players, deal 1 - verify_muck is True after running
    def test_muckallcards_cardsmucked_verifymuckreturnsTrue(self):
        self.r._table.move_button()
        self.r._table.set_blinds()
        self.r.deal_cards(1)
        self.r.muck_all_cards()
        expected = True
        result = self.r.check_integrity_post()
        self.assertEqual(expected, result)

    # 6 players, deal 1 - decksize == 0 after running
    def test_muckallcards_cardsmucked_decksize0(self):
        self.r.deal_cards(1)
        self.r.muck_all_cards()
        expected = 0
        result = len(self.r.d)
        self.assertEqual(expected, result)

    # 6 players, deal 1 - muck size == 52 after running
    def test_muckallcards_cardsmucked_mucksize52(self):
        self.r.deal_cards(1)
        self.r.muck_all_cards()
        expected = 52
        result = len(self.r.muck)
        self.assertEqual(expected, result)

    """
    Tests for post_antes()
    """
    # 6 players ante 1. Pot == 6.
    def test_postantes_6players_potequals60(self):
        self.r.blinds = blinds.BlindsAnte(level=4)
        self.r.post_antes()
        expected = 6
        result = self.r.pot
        self.assertEqual(expected, result)

    # Initial stacks=1000. Ante=1. After ante are 999.
    def test_postantes_6players_stacksequal999(self):
        self.r.blinds = blinds.BlindsAnte(level=4)
        self.r.post_antes()
        expected = 999
        for s in self.r._table:
            result = s.stack
            self.assertEqual(expected, result)

    """
    Tests for post_bringin():
    """
    # Initial stacks=1000. smallbet = 2. Bringin = 1
    # Seat 0
    def test_postbringin_seat5_has2chipsless(self):
        self.r.blinds = blinds.BlindsAnte(level=2)
        testtools.deal_stud5(self.r._table, matchingranks=0)
        player = self.r._table.seats[poker.bringin(self.r._table)]
        chips = player.stack
        self.r.post_bringin()
        expected = 1
        result = chips - player.stack
        self.assertEqual(expected, result)

    def test_postbringin_seat5_returnsString(self):
        self.r.blinds = blinds.BlindsAnte(level=2)
        testtools.deal_stud5(self.r._table, matchingranks=0)
        expected = 'bob5 brings it in for $1\n'
        result = self.r.post_bringin()
        self.assertEqual(expected, result)

    """
    Tests for post_blinds()
    """
    # If the button(and blinds haven't been set, raise an exception.)
    def test_postblinds_btnnotset_raiseException(self):
        self.r._table.TOKENS['D'] = -1
        self.assertEqual(self.r._table.TOKENS['D'], -1, 'Button should be -1!')
        self.assertRaises(Exception, self.r.post_blinds)

    # 2 players(spaced out). SB=1, BB=2, startingstacks=1000
    def test_postblinds_2players_pot3(self):
        for i in [1, 2, 4, 5]:
            self.r._table.pop(i)
        self.r._table.TOKENS['D'] = -1
        self.r._table.move_button()  # verify the button is 0
        self.r._table.set_blinds()
        self.assertEqual(self.r._table.TOKENS['D'], 0)
        self.r.post_blinds()
        self.assertEqual(self.r._table.seats[0].stack, 999)
        self.assertEqual(self.r._table.seats[3].stack, 998)
        self.assertEqual(self.r.pot, 3)

    # 3 players(spaced out). SB=1, BB=2, startingstacks=1000
    def test_postblinds_3players_pot3(self):
        for i in [1, 3, 5]:
            self.r._table.pop(i)

        self.r._table.TOKENS['D'] = -1
        self.r._table.move_button()  # verify the button is 0
        self.r._table.set_blinds()
        self.assertEqual(self.r._table.TOKENS['D'], 0)
        self.r.post_blinds()
        self.assertEqual(self.r._table.seats[2].stack, 999)
        self.assertEqual(self.r._table.seats[4].stack, 998)
        self.assertEqual(self.r.pot, 3)

    # 6 players(spaced out). SB=1, BB=2, startingstacks=1000
    def test_postblinds_6players_pot3(self):
        self.r._table.TOKENS['D'] = -1
        self.r._table.move_button()
        self.r._table.set_blinds()
        self.assertEqual(self.r._table.TOKENS['D'], 0)  # verify the button is 0
        self.r.post_blinds()
        self.assertEqual(self.r._table.seats[1].stack, 999)
        self.assertEqual(self.r._table.seats[2].stack, 998)
        self.assertEqual(self.r.pot, 3)

    # 6 players(spaced out). SB=1, BB=2, startingstacks=1000
    def test_postblinds_6players_returnsString(self):
        self.setUp(level=2)
        self.r._table.TOKENS['D'] = -1
        self.r._table.move_button()
        self.r._table.set_blinds()
        self.assertEqual(self.r._table.TOKENS['D'], 0)  # verify the button is 0
        expected = 'bob1 posts $1\nbob2 posts $2\n'
        result = self.r.post_blinds()
        self.assertEqual(expected, result)

    """
    Tests for invested(player)
    """
    # New table - player has invested nothing.
    def test_invested_nobets_returns0(self):
        expected = 0
        result = self.r.invested(self.r._table.seats[0])
        self.assertEqual(expected, result)

    # After betting 100 - player invested 100.
    def test_invested_bet100_returns100(self):
        expected = 100
        self.r._table.seats[0].bet(100)
        result = self.r.invested(self.r._table.seats[0])
        self.assertEqual(expected, result)

    """
    Tests for get_allin_stacks()
    """
    # No allins, returns empty list
    def test_getallins_none_returnsemptylist(self):
        self.r.deal_cards(2)
        expected = []
        result = self.r.get_allins()
        self.assertEqual(expected, result)

    # 1 allin, returns list with 1 stack size.
    def test_getallins_1allin_returns1stack(self):
        self.r.deal_cards(2)
        expected = [1000]
        self.r._table.seats[0].bet(1000)
        result = self.r.get_allins()
        self.assertEqual(expected, result)

    # 2 allins, returns list with 2 stack sizes.
    def test_getallins_2allin_returns2stacks(self):
        self.r.deal_cards(2)
        expected = [1000, 1000]
        self.r._table.seats[0].bet(1000)
        self.r._table.seats[1].bet(1000)
        result = self.r.get_allins()
        self.assertEqual(expected, result)

    """
    Tests for make_sidepots(self, _stacks):
    """
    # 2 players, 1 allin
    def test_makesidepots_2plyr_1allin_returns1sidepot(self):
        self.setup_allins(2)
        expected = {100: 200}
        self.everybody_bet(100)
        allins = self.r.get_allins()
        result = self.r.make_sidepots(allins)
        self.assertEqual(expected, result)

    # 3 players, 1 allin
    def test_makesidepots_3plyr_1allin_returns1sidepot(self):
        self.setup_allins(3)
        expected = {100: 300}
        self.everybody_bet(100)
        allins = self.r.get_allins()
        result = self.r.make_sidepots(allins)
        self.assertEqual(expected, result)

    # 3 players, 2 allins
    def test_makesidepots_3plyr_2allin_returns2sidepot(self):
        self.setup_allins(3)
        expected = {100: 300, 200: 200}
        self.everybody_bet(200)
        allins = self.r.get_allins()
        result = self.r.make_sidepots(allins)
        self.assertEqual(expected, result)

    # 4 players, 3 allins
    def test_makesidepots_4plyr_3allin_returns3sidepot(self):
        self.setup_allins(4)
        expected = {100: 400, 200: 300, 300: 200}
        self.everybody_bet(300)
        allins = self.r.get_allins()
        result = self.r.make_sidepots(allins)
        self.assertEqual(expected, result)

    # 5 players, 2 allins, challenge stack sizes.
    def test_makesidepots_4plyr_2allin_returns2sidepot(self):
        # Setup a problem situation
        self.g._table = table_factory.BobTable(4)
        stacks = [1000, 1000, 225, 100]
        for p in self.g._table:
            p.stack = stacks.pop(0)

        self.r = poker.Round(self.g)
        testtools.deal_random_cards(self.g._table)
        self.everybody_bet(300)

        expected = {100: 400, 225: 375}
        allins = self.r.get_allins()
        result = self.r.make_sidepots(allins)
        self.assertEqual(expected, result)

    """
    Tests for calc_sidepot(stacksize):
    """
    # 2 players, 1 allin
    def test_calcsidepot_2plyr_allinfor100_returns200(self):
        self.setup_allins(2)
        expected = 200
        self.everybody_bet(100)
        result = self.r.calc_sidepot(100)
        self.assertEqual(expected, result)

    # 3 players, 1 allin
    def test_calcsidepot_3plyr_allinfor100_returns300(self):
        self.setup_allins(3)
        expected = 300
        self.everybody_bet(100)
        result = self.r.calc_sidepot(100)
        self.assertEqual(expected, result)

    # 3 players, 2 allin
    def test_calcsidepot_3plyr_allinfor200_returns500(self):
        self.setup_allins(3)
        expected = 500
        self.everybody_bet(200)
        result = self.r.calc_sidepot(200)
        self.assertEqual(expected, result)

    """
    Tests for process_sidepots(sidepots)
    """
    # 2 players, 2 allins.
    def test_processsidepots_2players(self):
        self.setup_allins(2)
        testtools.deal_ranked_hands(self.r._table)
        self.everybody_bet(200)
        sidepots = self.r.make_sidepots(self.r.get_allins())

        expected = {200: [0], 100: [1]}
        result = self.r.process_sidepots(sidepots)
        self.assertEqual(expected, result)

    # 3 players, 3 allins.
    def test_processsidepots_3players(self):
        self.setup_allins(3)
        testtools.deal_ranked_hands(self.r._table)
        self.everybody_bet(300)
        # seat 0 gets strongest hand, 1 gets middle, 2 gets lowest.

        sidepots = self.r.make_sidepots(self.r.get_allins())

        expected = {300: [0], 200: [1], 100: [2]}
        result = self.r.process_sidepots(sidepots)
        self.assertEqual(expected, result)

    # If noone has cards, raise an exception.

    """
    Tests for eligible(self, stack_req):
    """
    def test_geteligible_3players_req100_returns3players(self):
        seats = 3
        self.setup_allins(seats)
        required_stack = 100
        expected = 3
        result = len(self.r.get_eligible(required_stack))
        self.assertEqual(expected, result)

    def test_geteligible_3players_req200_returns2players(self):
        seats = 3
        self.setup_allins(seats)
        required_stack = 200
        expected = 2
        result = len(self.r.get_eligible(required_stack))
        self.assertEqual(expected, result)

    def test_geteligible_3players_req300_returns1player(self):
        seats = 3
        self.setup_allins(seats)
        required_stack = 300
        expected = 1
        result = len(self.r.get_eligible(required_stack))
        self.assertEqual(expected, result)

    def test_geteligible_3players_req300_correctplayer(self):
        seats = 3
        self.setup_allins(seats)
        required_stack = 300
        expected = [self.r._table.seats[2]]
        result = self.r.get_eligible(required_stack)
        self.assertEqual(expected, result)

    """
    Tests for best_hand_val()
    # Note we'll use the table with the hand values reversed,
    # so that 0 has the lowest hand, 1 has better, 2 beats 1, etc.
    """

    # 2 players: should be pair_low
    def test_besthandval_2players_lowpair(self):
        self.setup_allins(2)
        testtools.deal_ranked_hands(self.r._table, _rev=True)
        players = self.r._table.get_players(hascards=True)

        expected = evaluator.get_value(pokerhands.make('pair_low'))
        result = self.r.best_hand_val(players)
        self.assertEqual(expected, result)

    # 3 players: should be pair_high
    def test_besthandval_3players_highpair(self):
        self.setup_allins(3)
        testtools.deal_ranked_hands(self.r._table, _rev=True)
        players = self.r._table.get_players(hascards=True)

        expected = evaluator.get_value(pokerhands.make('pair_high'))
        result = self.r.best_hand_val(players)
        self.assertEqual(expected, result)

    # 4 players: should be two pair
    def test_besthandval_4players_twopair(self):
        self.setup_allins(4)
        testtools.deal_ranked_hands(self.r._table, _rev=True)
        players = self.r._table.get_players(hascards=True)

        expected = evaluator.get_value(pokerhands.make('twopair_high'))
        result = self.r.best_hand_val(players)
        self.assertEqual(expected, result)

    # 5 players: should be trips
    def test_besthandval_5players_trips(self):
        self.setup_allins(5)
        testtools.deal_ranked_hands(self.r._table, _rev=True)
        players = self.r._table.get_players(hascards=True)

        expected = evaluator.get_value(pokerhands.make('trips_high'))
        result = self.r.best_hand_val(players)
        self.assertEqual(expected, result)

    # 5 players: should be straight
    def test_besthandval_6players_straight(self):
        self.setup_allins(6)
        testtools.deal_ranked_hands(self.r._table, _rev=True)
        players = self.r._table.get_players(hascards=True)

        expected = evaluator.get_value(pokerhands.make('straight_high'))
        result = self.r.best_hand_val(players)
        self.assertEqual(expected, result)

    """
    Tests for split_pot(winners, amt)
    """
    # Award 1 player 100 chips. Their stack goes up 100.
    # Award 2 players 100 chips. Each stack goes up 50
    # Award 2 players -100 chips. Raise exception.

    """
    Tests for showdown()
    """

    """
    Tests for award_pot(player, amt)
    """
    # Award 1 player 100 chips. Their stack goes up 100.
    # Try awarding -100. Should raise an exception.
    # Try awarding a player with no cards. Should raise an exception.

    """
    Tests for next_street()
    """
    def test_nextstreet_street0_streetIs1(self):
        self.r.next_street()
        expected = 1
        result = self.r.street
        self.assertEqual(expected, result)

    def test_nextstreet_draw5_street2_raisesException(self):
        self.r.next_street()
        self.r.next_street()
        self.assertRaises(Exception, self.r.next_street)

    """
    Tests for check_integrity_post(self):
    """
    # All cards mucked, but 1 card in deck, returns False
    def test_checkintegritypost_1cardindeck_returnsFalse(self):
        self.r.muck_all_cards()
        c = card.Card('A', 's')
        self.r.d.cards.append(c)
        expected = False
        result = self.r.check_integrity_post()
        self.assertEqual(expected, result)

    # All cards mucked, but 1 player w cards, returns False
    def test_checkintegritypost_1playerwithcards_returnsFalse(self):
        self.r._table.move_button()
        self.r._table.set_blinds()
        self.r.muck_all_cards()
        c = card.Card('A', 's')
        self.r._table.seats[0].hand.add(c)
        expected = False
        result = self.r.check_integrity_post()
        self.assertEqual(expected, result)

    # All cards mucked, but card in muck deleted, returns False
    def test_checkintegritypost_1poppedfrommuck_returnsFalse(self):
        self.r.muck_all_cards()
        self.r.muck.pop(0)
        expected = False
        result = self.r.check_integrity_post()
        self.assertEqual(expected, result)

    """
    Tests for clear_broke_players()
    """
    def test_clearbrokeplayers(self):
        p = self.r._table.seats[0]
        p.stack = 0
        expected = []
        self.r.clear_broke_players()
        result = self.r._table.get_broke_players()
        self.assertEqual(expected, result)

    """
    Tests for cleanup()
    """
    # After cleanup, there should be no broke players.
    """
    def test_cleanup(self):
        self.r.muck_all_cards()
        expected = False
        result = self.r.check_integrity_post()
        self.assertEqual(expected, result)
    """

    # After cleanup, no players should have cards
    def test_cleanup_noplayershavecards(self):
        self.r.muck_all_cards()
        expected = []
        result = self.r._table.get_players(hascards=True)
        self.assertEqual(expected, result)

    # After cleanup, there should be no cards in the deck
    def test_cleanup_deckisempty(self):
        self.r.muck_all_cards()
        expected = True
        result = self.r.d.is_empty()
        self.assertEqual(expected, result)

    # After cleanup, the muck size should equal the starting deck size
    def test_cleanup_muck_deck_sizesequal(self):
        self.r.muck_all_cards()
        expected = self.r.DECKSIZE
        result = len(self.r.muck)
        self.assertEqual(expected, result)

    """
    Tests for one_left()
    """
    def test_oneleft_allhavecards_returnsNone(self):
        self.setUp(players=2)
        self.r.deal_cards(1)
        expected = None
        result = self.r.one_left()
        self.assertEqual(expected, result)

    def test_oneleft_1withcards_returnsvictor(self):
        self.setUp(players=2)
        self.r.deal_cards(1)
        self.r._table.pop(0)
        victor = self.r._table.seats[1]
        expected = victor
        result = self.r.one_left()
        self.assertEqual(expected, result)

    """
    Tests for betting_over()
    """
    def test_bettingover_2hands1broke_returnsTrue(self):
        self.setUp(players=2)
        self.r.deal_cards(1)
        self.r._table.seats[0].stack = 0
        expected = True
        result = self.r.betting_over()
        self.assertEqual(expected, result)

    def test_bettingover_3hands1broke_returnsFalse(self):
        self.setUp(players=3)
        self.r.deal_cards(1)
        self.r._table.seats[0].stack = 0
        expected = False
        result = self.r.betting_over()
        self.assertEqual(expected, result)

    """
    Tests for bring(table, gametype):
    """
    # Stud5 deal: seat 5 has lowest card, 9
    def test_bringin_stud5_no_ties_returns5(self):
        t = table_factory.BobTable(6)
        testtools.deal_stud5(t, matchingranks=0)
        expected = 5
        result = poker.bringin(t)
        self.assertEqual(expected, result)

    # Stud5 deal: 2 Tied ranks
    def test_bringin_stud5_2tied_returns1(self):
        t = table_factory.BobTable(6)
        testtools.deal_stud5(t, matchingranks=2)
        expected = 1
        result = poker.bringin(t)
        self.assertEqual(expected, result)

    # Stud5 deal: 3 Tied ranks
    def test_bringin_stud5_3tied_returns1(self):
        t = table_factory.BobTable(6)
        testtools.deal_stud5(t, matchingranks=3)
        expected = 1
        result = poker.bringin(t)
        self.assertEqual(expected, result)

    # Stud5 deal: 4 Tied ranks
    def test_bringin_stud5_4tied_returns1(self):
        t = table_factory.BobTable(6)
        testtools.deal_stud5(t, matchingranks=4)
        expected = 1
        result = poker.bringin(t)
        self.assertEqual(expected, result)

    # Stud7 deal: seat 5 has lowest card, 9
    def test_bringin_stud7_no_ties_returns6(self):
        t = table_factory.BobTable(6)
        testtools.deal_stud5(t, matchingranks=0)
        expected = 5
        result = poker.bringin(t)
        self.assertEqual(expected, result)

    # Stud7 deal: 2 Tied ranks
    def test_bringin_stud7_2tied_returns1(self):
        t = table_factory.BobTable(6)
        testtools.deal_stud5(t, matchingranks=2)
        expected = 1
        result = poker.bringin(t)
        self.assertEqual(expected, result)

    # Stud7 deal: 3 Tied ranks
    def test_bringin_stud7_3tied_returns1(self):
        t = table_factory.BobTable(6)
        testtools.deal_stud5(t, matchingranks=3)
        expected = 1
        result = poker.bringin(t)
        self.assertEqual(expected, result)

    # Stud7 deal: 4 Tied ranks
    def test_bringin_stud7_4tied_returns1(self):
        t = table_factory.BobTable(6)
        testtools.deal_stud5(t, matchingranks=4)
        expected = 1
        result = poker.bringin(t)
        self.assertEqual(expected, result)

    """
    Tests for highhand(table)
    """
    # Throw in an empty seat for testing.
    # Throw in a player without cards for testing.

    # Stud5:
    def test_highhand_3cards_pairAces_return0(self):
        self.setUp_stud(players=3)
        self.givehand(0, '2AA_v1')
        self.givehand(1, '2KK')
        self.givehand(2, '2QQ')
        self.r._table.set_bringin(2)
        expected = 0
        result = poker.highhand(self.r._table, gametype="FIVE CARD STUD")
        self.assertEqual(expected, result)

    # Stud5:
    def test_highhand_4cards_AceHigh_return0(self):
        self.setUp_stud(players=4)
        self.givehand(0, 'QKA_v1')
        self.givehand(1, 'JTQ')
        self.givehand(2, '89J')
        self.givehand(3, '567')
        self.r._table.set_bringin(3)
        expected = 0
        result = poker.highhand(self.r._table, gametype="FIVE CARD STUD")
        self.assertEqual(expected, result)

    # Stud5:
    def test_highhand_3cards_2tied_return02(self):
        self.setUp_stud(players=3)
        self.givehand(0, '2AA_v1')
        self.givehand(1, '2KK')
        self.givehand(2, '2AA_v2')  # Ad is bringin; dealt first
        self.r._table.set_bringin(2)
        expected = 2
        result = poker.highhand(self.r._table, gametype="FIVE CARD STUD")
        self.assertEqual(expected, result)

    # Stud5:
    def test_highhand_4cards_2tied_return02(self):
        self.setUp_stud(players=4)
        self.givehand(0, 'QKA_v1')  # Dealt first on 4th street
        self.givehand(1, 'JTQ')
        self.givehand(2, 'QKA_v2')
        self.givehand(3, '567')     # Bringin
        self.r._table.set_bringin(3)
        expected = 0
        result = poker.highhand(self.r._table, gametype="FIVE CARD STUD")
        self.assertEqual(expected, result)

    # Stud5:
    def test_highhand_3cards_3tied_return023(self):
        self.setUp_stud(players=6)
        self.givehand(0, '3AK_v1')  # Dealt first on 4th street
        self.givehand(1, '3AK_v2')
        self.givehand(2, '3AK_v3')
        self.givehand(3, '345')
        self.givehand(4, '234')     # Bringin
        self.givehand(5, '245')
        self.r._table.set_bringin(4)
        expected = 0
        result = poker.highhand(self.r._table, gametype="FIVE CARD STUD")
        self.assertEqual(expected, result)
