from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions(Page):
    pass


class CustomForm(Page):

    form_model = models.Player
    form_fields = ['dice1', 'dice2', 'dice3', 'dice4', 'dice5', 'dice6']
    #Timout appears in both treatments s.t. decisions are not biased through different experiment conditions
    timeout_seconds = 10
    timeout_submission = {'dice1':1, 'dice2':1, 'dice3':1, 'dice4':1, 'dice5':1, 'dice6':1}
    def before_next_page(self):
        self.player.payoff = self.player.return_sum()/2
        if self.timeout_happened:
            self.player.timeout = True


#Wait page in the distribution treatment s.t. the histogramm will be calculated with data of all players
class ResultsWaitPage(WaitPage):
    def is_displayed(self):
        return self.player.treatment == 'distribution'
    #Calculate histogramm data and store
    def after_all_players_arrive(self):
        self.session.vars['hist_data'] = self.subsession.create_histogramm_data()


class Results(Page):

    def vars_for_template(self):
        if self.player.treatment == 'distribution':
            #Instead of calculating on his own, each player just looks at the stored hist data
            data = self.session.vars['hist_data']
            return {'sum':self.player.return_sum(), 'histogramm_data': [{'name':'Frequency','data':data}]}
        elif self.player.treatment == 'private':
            return {'sum': self.player.return_sum()}


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









