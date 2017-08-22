from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random
author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'dice'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):

    #
    def assign_treatment_random(self):
        treatment = random.choice(['private', 'distribution'])
        for player in self.get_players():
            player.treatment = treatment

    def creating_session(self):
        #TODO: not tested yet
        if 'treatment' in self.session.config:
            #Check if a valid treatment was entered in settings.py otherwise assign treatment randomly
            if self.session.config['treatment'] == ('private' or 'distribution'):
                for player in self.get_players():
                    player.treatment = self.session.config['treatment']
            else: #nonvalid treatment was entered in settings.py
                self.assign_treatment_random()
        else: #no treatment was entered in settings.py
            self.assign_treatment_random()






class Group(BaseGroup):
    pass


class Player(BasePlayer):

    treatment = models.CharField(doc='Defines the treatment of the player. The treatment is the same for all players in one session and can either be "Private" or "Distribution".',
                                 choices=['private', 'distribution'])
    #TODO: Ok, for sure we want every single dice input saved in the datebase.
    #TODO: But can't implement this nicer? E.g. create the variables on the fly instead of in advance?

    #TODO: you dont neeed min max here, because the custom form is not entering these parameters. Instead it is done in the html itself
    dice1 = models.IntegerField(doc='The input for the x\'th dice roll of the player',
                                min=1, max=6)
    dice2 = models.IntegerField(doc='The input for the x\'th dice roll of the player',
                                min=1, max=6)
    dice3 = models.IntegerField(doc='The input for the x\'th dice roll of the player',
                                min=1, max=6)
    dice4 = models.IntegerField(doc='The input for the x\'th dice roll of the player',
                                min=1, max=6)
    dice5 = models.IntegerField(doc='The input for the x\'th dice roll of the player',
                                min=1, max=6)
    dice6 = models.IntegerField(doc='The input for the x\'th dice roll of the player',
                                min=1, max=6)

    age = models.IntegerField(doc='The participants\' age')
    gender = models.CharField(doc='The participants\'s gender', choices=['male', 'female'])
    student = models.BooleanField(doc = '1 if the participant is not a student', verbose_name='I am a student.')
    studies = models.CharField(doc = 'Field of study, if the participant is a student')

    def calc_payoff(self):
        self.payoff = sum([self.dice1, self.dice2, self.dice3, self.dice4, self.dice5, self.dice6]) / 2


    def return_sum(self):
        return sum ([self.dice1, self.dice2, self.dice3, self.dice4, self.dice5, self.dice6])