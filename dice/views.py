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
        pass


class PrivateResults(Page):
    def is_displayed(self):
        return self.player.treatment == 'private'

class DistributionResults(Page):
    def is_displayed(self):
        return self.player.treatment == 'distribution'


class Demographics(Page):
    form_model = models.Player
    form_fields = ['student']

    #TODO: This has no effect because after the participant marks the nonstudent checkbox the code is not reloaded:
    #TODO: possible workarounds:1.) let the field of studies field only appear if the checkbox is marked, with javascript
    #TODO: 2.) have the checkbox on the page before field of studies and then use the below function
    def studies_choices(self):
        if self.player.nonstudent == 1:
            return 'Non Student'

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
