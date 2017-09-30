from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions(Page):
    pass


#Timelimit appears in both treatments s.t. decisions are not biased through different experiment conditions
#If a player has a timeout the otree default submits 0`s for all the dice.
#Note: If a player submits e. g. only 3 dice and then has a timout, the player will get no payoff and will not be regarded in the histogramm.
#The dice inputs will be unchanged though and the other noninputted dice will be filled with 0 (This cannot be changed with a forced submission).
#This player can be sorted out in the analysis by the timeout bool. Additionally, in the database we have all information possible.
class CustomForm(Page):
    form_model = models.Player
    form_fields = ['dice1', 'dice2', 'dice3', 'dice4', 'dice5', 'dice6']
    timeout_seconds = Constants.timeoutseconds
    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout = True
            self.player.payoff = 0
        else:
            self.player.payoff = self.player.return_sum() / 2


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
            return ('Please click the nonstudent box if you are not a student. If you are a student please enter your field of studies.')
        if values['studies'] != '' and values['nonstudent'] == True:
            return('You entered a field of study and you clicked the nonstudent box also. Please leave the studies field blank if you are not a student.')


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









