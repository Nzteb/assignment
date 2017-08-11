from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'dice'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):

    def creating_session(self):
        #TODO: IF a wrong treatment has been assigned, or no treatment has been assigned, the exceptions are not thrown.
        #TODO: Instead otree tries to open the the session without succes repeatedly
        #TODO: How can you throw your own exceptions in Otree?
        if 'treatment' in self.session.config:
            print('I believe treatment is defined in settings')
            #Check if correct treatment was entered in settings.py
            if self.session.config['treatment'] == ('private' or 'distribution'):
                for player in self.get_players():
                    player.treatment = self.session.config['treatment']
            else:
                raise Exception('The entered Treatment in "settings.py" does not exist. Please enter "private" or "distribution".')
        #I dont allow random assignment of Treatments if no treatment is defined in setttings.py, because it is more senseful if in one session all players have the same treatment.
        else:
            raise Exception ('No Treatment defined in "settings.py". Enter either "private" or "distribution" as treatment')

    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    treatment = models.CharField(doc='Defines the treatment of the player. The treatment is the same for all players in one session and can either be "Private" or "Distribution".',
                                 choices=['private', 'distribution'])
    #TODO: Ok, for sure we want every single dice input saved in the datebase.
    #TODO: But can't implement this nicer? E.g. create the variables on the fly instead of in advance?
    dice1 = models.IntegerField(doc='The input for the x\'th dice roll of the player',
                                choices=[1,2,3,4,5,6])
    dice2 = models.IntegerField(doc='The input for the x\'th dice roll of the player',
                                choices=[1,2,3,4,5,6])
    dice3 = models.IntegerField(doc='The input for the x\'th dice roll of the player',
                                choices=[1,2,3,4,5,6])
    dice4 = models.IntegerField(doc='The input for the x\'th dice roll of the player',
                                choices=[1,2,3,4,5,6])
    dice5 = models.IntegerField(doc='The input for the x\'th dice roll of the player',
                                choices=[1,2,3,4,5,6])
    dice6 = models.IntegerField(doc='The input for the x\'th dice roll of the player',
                                choices=[1,2,3,4,5,6])

    def calc_payoff(self):
        self.payoff = sum([self.dice1, self.dice2, self.dice3, self.dice4, self.dice5, self.dice6]) / 2