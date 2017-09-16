from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions(Page):
    pass


class CustomForm(Page):
    form_model = models.Player
    form_fields = ['dice1', 'dice2', 'dice3', 'dice4', 'dice5', 'dice6']
    timeout_seconds = 300
    timeout_submission = {'dice1':1, 'dice2':1, 'dice3':1, 'dice4':1, 'dice5':1, 'dice6':1}
    def before_next_page(self):
        self.player.payoff = self.player.return_sum()/2


#Wait page is needed in the distribution treatment, so that the histogramm will be calculated with data of all players
class ResultsWaitPage(WaitPage):
    def is_displayed(self):
        return self.player.treatment == 'distribution'


class Results(Page):
    def vars_for_template(self):
        #note: we need the empty data dictionaire in private treatment, otherwise exception will be thrown
        data = {}
        #calculate histogramm data in distribution treatment
        if self.player.treatment == 'distribution':
            data = self.subsession.create_histogramm_data()
        return {'sum':self.player.return_sum(), 'histogramm_data': [{'name':'Frequency','data':data}]}


class Demographics(Page):
    form_model = models.Player
    form_fields = ['nonstudent', 'gender', 'age', 'risk', 'country','studies']
    def error_message(self, values):
        if values['studies'] == '' and values['nonstudent'] == False:
            return ('Please click the box below if you are not a student. If you are a student please enter your field of studies.')
        if values['studies'] != '' and values['nonstudent'] == True:
            return('You entered a field of study and that you are not a student. Please leave the studies field blank if you are not a student.')




class LastPage(Page):
    pass


page_sequence = [
    Instructions,
    CustomForm,
    ResultsWaitPage,
    Results,
    Demographics,
    LastPage
]









