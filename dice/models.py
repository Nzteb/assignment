from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random

from django_countries.fields import CountryField



author = 'Patrick Betz'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'dice'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):

    #will only be called in creating_session if treatment is wrongly entered or not entered
    def assign_treatment_random(self):
        treatment = random.choice(['private', 'distribution'])
        for player in self.get_players():
            player.treatment = treatment

    def creating_session(self):
        if 'treatment' in self.session.config:
            #Check if a valid treatment was entered in settings.py otherwise assign treatment randomly
            treatment_input = self.session.config['treatment']
            if treatment_input  == 'private' or treatment_input == 'distribution':
                for player in self.get_players():
                    player.treatment = treatment_input
            else: #nonvalid treatment was entered in settings.py
                self.assign_treatment_random()
        else: #no treatment was entered in settings.py
            self.assign_treatment_random()


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    treatment = models.CharField(doc='Defines the treatment of the player. The treatment is the same for all players in one session and can either be "Private" or "Distribution".',
                                 choices=['private', 'distribution'])

    #All dice inputs shall appear in the database
    dice1 = models.IntegerField(doc='The input for the 1st dice roll of the player', min=1, max=6)
    dice2 = models.IntegerField(doc='The input for the 2nd dice roll of the player', min=1, max=6)
    dice3 = models.IntegerField(doc='The input for the 3rd dice roll of the player', min=1, max=6)
    dice4 = models.IntegerField(doc='The input for the fourth dice roll of the player', min=1, max=6)
    dice5 = models.IntegerField(doc='The input for the fift dice roll of the player', min=1, max=6)
    dice6 = models.IntegerField(doc='The input for the sixt dice roll of the player', min=1, max=6)

    age = models.IntegerField(doc='The age of the participant',
                              min=14,
                              max=110)
    gender = models.CharField(doc='The gender of the participant',
                              choices=['male', 'female'])
    nonstudent = models.BooleanField(doc='1 if the participant is not a student',
                                     widget=widgets.CheckboxInput(),
                                     verbose_name='I am not a student')
    studies = models.CharField(doc='Field of study, if the participant is a student',
                               blank='True')
    risk = models.CharField(doc='Risk attitude of the participant. (7 points Likert scale)',
                            choices=['Agree Very Strongly',
                                     'Agree Strongly',
                                     'Agree',
                                     'Disagree',
                                     'Disagree Strongly',
                                     'Disagree Very Strongly'],
                            widget=widgets.RadioSelectHorizontal(),
                            verbose_name='"I like taking risks."')
    country = CountryField(blank='Select your country of origin.')
    #Note: payoff is calculated in views by using this function
    def return_sum(self):
        return sum ([self.dice1, self.dice2, self.dice3, self.dice4, self.dice5, self.dice6])