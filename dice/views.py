from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions(Page):
    pass


class CustomForm(Page):
    form_model = models.Player
    form_fields = ['dice1', 'dice2', 'dice3', 'dice4', 'dice5', 'dice6']
    def before_next_page(self):
        self.player.payoff = self.player.return_sum()/2


#Wait page is needed in the distribution treatment, so that the histogramm will be calculated with data of all players
class ResultsWaitPage(WaitPage):
    def is_displayed(self):
        return self.player.treatment == 'distribution'


class Results(Page):
    def vars_for_template(self):
        # calculate data for the histogramm; data: 'inputted sum' : 'absolute frequency of players'
        # note: this could be done in both treatments but only be displayed in the distriution treatment
        # but then the waitpage must be used also in private treatment otherwise an error occurs when the (useless) calculation starts
        # before all players are finished with inputting their results
        #TODO: Substantial objection: the histogramm data is calculated by each player when he is on this page
        #TODO: it would be nicer if this is only done once. But if I write a function in models.Subsession and call this from here,
        #TODO than exactly the same thing happens because every player is calling this function then from here, right?
        data = {}
        if self.player.treatment == 'distribution':
            data = {6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15:0, 16: 0,
                    17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0, 26: 0,
                    27: 0, 28: 0, 29: 0, 30: 0, 31: 0, 32: 0, 33: 0, 34: 0, 35: 0, 36: 0}
            for player in self.subsession.get_players():
                sum = player.return_sum()
                data[sum] += 1
        #data holds absolute frequencies, in the dict value this is divided by the number of players
        #note: in private treatment the 'data dic' is empty and will not be used in the template
        return {'sum':self.player.return_sum(), 'histogramm_data': [{'name':'Frequency','data':[value/self.session.config['num_demo_participants'] for value in list(data.values())]}]}


class Demographics(Page):
    form_model = models.Player
    form_fields = ['student', 'gender', 'age', 'risk', 'country']


#Builds the last page for students, with instructions to remain seated
class FieldOfStudies(Page):
    form_model = models.Player
    form_fields = ['studies']
    def is_displayed(self):
        return  self.player.student


class LastPageNonstudent(Page):
    def is_displayed(self):
        return not self.player.student
    pass


page_sequence = [
    Instructions,
    CustomForm,
    ResultsWaitPage,
    Results,
    Demographics,
    FieldOfStudies,
    LastPageNonstudent
]
