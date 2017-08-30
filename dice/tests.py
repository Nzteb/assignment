from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        if self.player.treatment == 'distribution':

            yield (views.DistributionInstructions)
            #check payoff calculation
            yield (views.CustomForm, {'dice1':6, 'dice2':6,'dice3':6,'dice4':6,'dice5':6,'dice6':6})
            assert self.player.payoff == 18
            print('I was here')
        elif self.player.treatment == 'private':
            #check payoff calculation

            yield (views.PrivateInstructions)
            yield (views.CustomForm, {'dice1': 6, 'dice2': 6, 'dice3': 6, 'dice4': 6, 'dice5': 6, 'dice6': 6})
            assert self.player.payoff == 18




