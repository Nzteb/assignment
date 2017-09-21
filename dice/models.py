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
    #Please enter the number of minutes you want to allow for rolling the dice
    timeoutminutes = 5
    timeoutseconds = 60*timeoutminutes


class Subsession(BaseSubsession):

    #Will only be called in creating_session if treatment is wrongly entered or not entered
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
            else: #Nonvalid treatment was entered in settings.py
                self.assign_treatment_random()
        else: #No treatment was entered in settings.py
            self.assign_treatment_random()

    #Returns a list with the relative frequency values of the histogramm
    #Only players who did not time out are regarded s.t. the histogramm is correct
    def create_histogramm_data(self):
        data = {6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0,
                17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0, 26: 0,
                27: 0, 28: 0, 29: 0, 30: 0, 31: 0, 32: 0, 33: 0, 34: 0, 35: 0, 36: 0}

        num_no_timout = 0
        for player in self.get_players():
            #only regard players with no timeout
            if player.timeout == False:
                sum = player.return_sum()
                data[sum] += 1
                #count players with no timeout
                num_no_timout += 1
        if num_no_timout != 0:
            # Divide absolute frequency of players with no timeout by number of players with no timeout to get relative frequency
            return [value / num_no_timout for value in list(data.values())]
        else: #all players had a timout. Display list with 0`s to not force an exception
            return[value for value in list(data.values())]


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
        choices=['Entirely Agree',
                 'Mostly Agree',
                 'Somewhat Agree',
                 'Neither Agree nor Disagree',
                 'Somewhat Disagree',
                 'Mostly Disagree',
                 'Entirely Disagree'],
        widget=widgets.RadioSelectHorizontal(),
        verbose_name='How strong do you agree/disagree with the following statement: "I like taking risks."?')

    timeout = models.BooleanField(
        default=False,
        doc="Equals True if the participant did not enter any results. She then gets a payoff of zero.")

    #Note: if you implement a 'doc' parameter this will throw an exception
    country = CountryField(
        #I decided to not permit not entering a country
        blank=False,
        verbose_name='What is the country of your origin?')

    #Note: payoff is calculated in views by using this function
    def return_sum(self):
        return sum ([self.dice1, self.dice2, self.dice3, self.dice4, self.dice5, self.dice6])


