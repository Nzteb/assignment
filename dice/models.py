from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random

from django_countries.fields import CountryField



author = 'Patrick Betz'

doc = """
A dice experiment
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

    #returns a list with the relative frequency values of the histogramm
    def create_histogramm_data(self):
        data = {6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0,
                17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0, 26: 0,
                27: 0, 28: 0, 29: 0, 30: 0, 31: 0, 32: 0, 33: 0, 34: 0, 35: 0, 36: 0}
        for player in self.get_players():
            sum = player.return_sum()
            data[sum] += 1
        return [value / self.session.config['num_demo_participants'] for value in list(data.values())]


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    treatment = models.CharField(
        doc='Defines the treatment of the player. The treatment is the same for all players in one session and can either be "Private" or "Distribution".',
        choices=['private', 'distribution'])

    #All dice inputs shall appear in the database
    dice1 = models.IntegerField(
        doc='The input for the 1st dice roll of the player', min=1, max=6)
    dice2 = models.IntegerField(
        doc='The input for the 2nd dice roll of the player', min=1, max=6)
    dice3 = models.IntegerField(
        doc='The input for the 3rd dice roll of the player', min=1, max=6)
    dice4 = models.IntegerField(
        doc='The input for the fourth dice roll of the player', min=1, max=6)
    dice5 = models.IntegerField(
        doc='The input for the fift dice roll of the player', min=1, max=6)
    dice6 = models.IntegerField(
        doc='The input for the sixt dice roll of the player', min=1, max=6)

    age = models.IntegerField(
        doc='The age of the participant',
        min=14,
        max=110,
        verbose_name='Please enter your age.')

    gender = models.CharField(
        doc='The gender of the participant',
        choices=['Male', 'Female'],
        widget=widgets.RadioSelect(),
        verbose_name='What is your gender?')

    nonstudent = models.BooleanField(
        doc='1 if the participant is not a student',
        widget=widgets.CheckboxInput(),
        verbose_name='Click if you are not a student.')

    studies = models.CharField(
        doc='Field of study, if the participant is a student',
        blank='True',
        verbose_name='Enter your field of study if you are a student. Leave blank if you are not a student')

    risk = models.CharField(
        doc='Risk attitude of the participant. (7 points Likert scale)',
        choices=['Agree Very Strongly',
                 'Agree Strongly',
                 'Agree',
                 'Disagree',
                 'Disagree Strongly',
                 'Disagree Very Strongly'],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name='How strong do you agree/disagree with the following statement: "I like taking risks."?')

    #note: if you implement a 'doc' parameter this will throw an exception
    country = CountryField(
        blank=False,
        verbose_name='What is the country of your origin?')

    #Note: payoff is calculated in views by using this function
    def return_sum(self):
        return sum ([self.dice1, self.dice2, self.dice3, self.dice4, self.dice5, self.dice6])