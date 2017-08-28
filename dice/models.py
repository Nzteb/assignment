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

    histogram_data = 1

    def calculate_histogram_data(self):
        data = {6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0, 21:0, 22:0, 23:0, 24:0, 25:0, 26:0, 27:0, 28:0, 29:0, 30:0, 31:0, 32:0, 33:0, 34:0, 35:0, 36:0}
        for player in self.get_players():
            sum = player.return_sum()
            data[sum] += 1
        #TODO: So he arrives here, but anyhow the self.histrogram_data assignment goes into nowhere
        print('At least I was here')
        # TODO: Im not sure if this last declaration of histogram_data always has the same ordering. But the ordering of the frequency is crucial for the histogramm
        # TODO: check this and find a better solution
        self.histogram_data = list(data.keys())









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