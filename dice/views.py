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
        self.player.payoff = self.player.return_sum()/2


#Wait page is needed, so that the histogramm will be calculated with data of all players
#TODO: you could try something like "is displayed if treatment = distribution" does this work with wait pages
class ResultsWaitPage(WaitPage):
    pass


class PrivateResults(Page):
    def vars_for_template(self):
        return {'sum':self.player.return_sum()}
    def is_displayed(self):
        return self.player.treatment == 'private'

class DistributionResults(Page):
    def vars_for_template(self):
        #calculate data for the histogramm
        #data: 'inputted sum' : 'absolute frequency of players'
        data = {6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0,
                21: 0, 22: 0, 23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 0, 31: 0, 32: 0, 33: 0, 34: 0, 35: 0,
                36: 0}
        for player in self.subsession.get_players():
            _sum = player.return_sum()
            data[_sum] += 1
        # TODO: Im not sure if list(data.keys()) always has the same ordering. But the ordering of the frequency is crucial for the histogramm
        return {'sum':self.player.return_sum(), 'histogramm_data': [{'name':'Frequency','data':[value/self.session.config['num_demo_participants'] for value in  list(data.values())]}]}
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
