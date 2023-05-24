from poker_game_runner.game import play_tournament_table, BlindScheduleElement
from poker_game_runner.bots import randombot
import mybot

play_tournament_table([mybot, randombot, randombot, randombot], 1000, (BlindScheduleElement(10, 5,10,0), BlindScheduleElement(-1, 10,20,0)))