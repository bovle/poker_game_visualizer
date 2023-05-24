from collections import Counter
import re
from poker_game_runner.state import Observation
from poker_game_runner.utils import Range, HandType

CALL = 1
CHECK_FOLD = 0

USE_FLUSH_DRAW = False

class Bot:
    def __init__(self) -> None:
        self.r25 = Range(
            "55+, A2s+, K5s+, Q8s+, J8s+, T9s, A8o+, K9o+, QTo+, JTo"
        )  # top 25%
        self.r20 = Range("55+, A3s+, K7s+, Q8s+, J9s+, T9s, A9o+, KTo+, QJo")  # top 20%
        self.r16 = Range("66+, A5s+, K9s+, Q9s+, JTs, ATo+, KJo+, QJo")  # 16%
        self.r10 = Range("77+, A9s+, KTs+, QJs, AJo+, KQo")  # 10%
        self.r6 = Range("88+, ATs+, KJs+, AKo")  # 6%

    def get_name(self):
        return "SpookyBot"

    def act(self, obs: Observation):
        if obs.current_round == 0:  # preflop
            return self.do_preflop(obs)
        else:
            return self.do_postflop(obs)

    def do_preflop(self, obs: Observation):
        r_raise = self.r6
        r_call = self.r25
        if r_raise.is_hand_in_range(obs.my_hand):
            return obs.get_fraction_pot_raise(1)  # raise 1 pot
        elif r_call.is_hand_in_range(obs.my_hand):
            return CALL
        else:
            # Fold
            return CHECK_FOLD

    def do_postflop(self, obs: Observation):
        my_hand_type = obs.get_my_hand_type()
        if my_hand_type >= HandType.FLUSH:
            return obs.get_max_raise()
        elif my_hand_type >= HandType.THREEOFAKIND:
            return obs.get_min_raise()
        elif my_hand_type >= HandType.PAIR:
            return CALL
        else:
            if USE_FLUSH_DRAW:
                if self.has_flush_draw(obs):
                    return CALL
            return CHECK_FOLD
    
    def has_flush_draw(self, obs: Observation):
        cards = obs.my_hand + obs.board_cards
        c = Counter([c[1] for c in cards])
        if (len(cards) == 5):
            return any(v >= 3 for k, v in c)
        
        return any(v >= 4 for k, v in c)

