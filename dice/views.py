from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class PrivateInstructions(Page):
    def is_displayed(self):
        return self.player.treatment == 'private'

class DistributionInstructions(Page):
    def is_displayed(self):
        return self.player.treatment == 'distribution'


class CustomForm(Page):
    #TODO: the forms are not next to each other, instead on next lines look at picture of assignement description
    form_model = models.Player
    form_fields = ['dice1', 'dice2', 'dice3', 'dice4', 'dice5', 'dice6']
    def before_next_page(self):
        self.player.calc_payoff()


#TODO: as participants do not interact with each other, wait pages are not needed in principle
#TODO: but a waitpage is needed to calculate the histogramm
class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        #TODO calculation of histogram data is done in both treatments for now (only displayed in distribution treatment)
        self.subsession.calculate_histogram_data()


class PrivateResults(Page):
    def vars_for_template(self):
        sum = self.player.return_sum()
        return {'sum':sum}
    def is_displayed(self):
        return self.player.treatment == 'private'

class DistributionResults(Page):
    def vars_for_template(self):
        sum = self.player.return_sum()
        return {'sum':sum, 'histogramm_data': [{ 'name':'Distribution of Inputs of other Players', 'data': self.subsession.histogram_data}]}
    def is_displayed(self):
        return self.player.treatment == 'distribution'



class Demographics(Page):
    form_model = models.Player
    form_fields = ['student']


class FieldOfStudies(Page):
    form_model = models.Player
    form_fields = ['studies']
    def is_displayed(self):
        return  self.player.student


page_sequence = [
    PrivateInstructions,
    DistributionInstructions,
    CustomForm,
    ResultsWaitPage,
    PrivateResults,
    DistributionResults,
    Demographics,
    FieldOfStudies
]
