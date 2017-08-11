from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class PrivateFirstPage(Page):
    #TODO: the forms are not next to each other, instead on next lines look at picture of assignement description
    form_model = models.Player
    form_fields = ['dice1', 'dice2', 'dice3', 'dice4', 'dice5', 'dice6']

    def is_displayed(self):
        return self.player.treatment == 'private'
    def before_next_page(self):
        self.player.calc_payoff()

class DistributionFirstPage(Page):
    # TODO: the forms are not next to each other, instead on next lines look at picture of assignement description
    form_model = models.Player
    form_fields = ['dice1', 'dice2', 'dice3', 'dice4', 'dice5', 'dice6']

    def is_displayed(self):
        return self.player.treatment == 'distribution'

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass

class PrivateResults(Page):
    pass

class DistributionResults(Page):
    pass

class Results(Page):
    pass


page_sequence = [
    PrivateFirstPage,
    DistributionFirstPage,
    ResultsWaitPage,
    PrivateResults,
    DistributionResults
]
