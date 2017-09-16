from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants
from . import views
from otree.api import SubmissionMustFail


class PlayerBot(Bot):

    #Note:
    #Run 'otree test' to run both session_configs entries. This will test both treatments of the app.
    # the most templates are the same in both treatments so they are not tested seperately


    #choose test cases and insert in list: 'check_html' , 'calculations', 'formvalidationfails'
    # all cases will be run if lists contains all cases
    cases = ['check_html' , 'calculations', 'formvalidationfails']

    def play_round(self):
        #case1 'check_html': check if the templates are correctly displayed for the different treatments
        treatment = self.player.treatment
        if self.case == 'check_html':
            if treatment == 'private':
                #Has to be displayed
                assert ('No participant will have any information about what the other players input or earn.' in self.html)
                #Must not be displayed
                assert ('A Histogramm will be shown at the end of the game, where everyone can see what the other participants in the experiment inputted.' not in self.html)
                yield views.Instructions
                yield (views.CustomForm, {'dice1':2, 'dice2':2, 'dice3':2, 'dice4':2, 'dice5':2, 'dice6':2})
                #must not be displayed
                assert ('Below, you can see the distribution of the results of the other participants.' not  in self.html)
            elif treatment == 'distribution':
                #Has to be displayed
                assert ('A Histogramm will be shown at the end of the game, where everyone can see what the other participants in the experiment inputted.' in self.html)
                #Must not be displayed
                assert ('No participant will have any information about what the other players input or earn.' not in self.html)
                yield views.Instructions
                yield (views.CustomForm, {'dice1':2, 'dice2':2, 'dice3':2, 'dice4':2, 'dice5':2, 'dice6':2})
                #has to be displayed
                assert ('Below, you can see the distribution of the results of the other participants.' in self.html)
                yield views.Results
        #case2 'calculations': Check if payoffcalculation works, check if histogram data is calculated correctly
        elif self.case == 'calculations':
                yield views.Instructions
                yield (views.CustomForm, {'dice1': 1, 'dice2': 1, 'dice3': 1, 'dice4': 1, 'dice5': 1, 'dice6': 1})
                assert self.player.payoff == 3
                if treatment == 'distribution':
                    #check if the histogramm data is calculated correctly. Only 1's inputted so the value of the first element of the data list must be 1 (100 percent)
                    #TODO: There is no better way to check the data of the Histogramm, I asked Chris
                    assert ('[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]' in self.html)
        #case3 'formvalidationfails': check that only integers from 1-6 and no chars can be entered for the dices, check other forms
        elif self.case == 'formvalidationfails':
                yield views.Instructions
                #ensure for every single dice that no 7 or 0 or character can be inputted
                for i in range(6):
                    for wrong_input in [7,0,'a']:
                        sl = [1, 1, 1, 1, 1, 1]
                        sl[i] = wrong_input
                        yield SubmissionMustFail(views.CustomForm,{'dice1': sl[0], 'dice2': sl[1], 'dice3': sl[2], 'dice4': sl[3],'dice5': sl[4], 'dice6': sl[5]})

                yield(views.CustomForm, {'dice1': 1, 'dice2': 1, 'dice3': 1, 'dice4': 1, 'dice5': 1, 'dice6': 1} )
                yield(views.Results)
                #ensure that only correct age input is possible
                for wrong_age in [10000, 'whats up', '!!']:
                    yield SubmissionMustFail(views.Demographics,{'nonstudent':True, 'gender':'Male', 'age':wrong_age, 'risk':'Agree', 'country':'DE','studies':''})
                #ensure that country of origin cannot be blank
                yield SubmissionMustFail(views.Demographics,{'nonstudent': True, 'gender': 'Female', 'age': 27, 'risk': 'Agree','country': '', 'studies': ''})
                # -- test dynamic form field validation for the nonstudent checkbox --
                #ensure that if one clicks nonstudent he cannot enter something
                yield SubmissionMustFail(views.Demographics, {'nonstudent': True, 'gender': 'Female', 'age': 26, 'risk': 'Agree', 'country': 'DE', 'studies': 'Economics'})
                #ensure that if one does not click nonstudent (so he is a student) that he must enter something in field of studies
                yield SubmissionMustFail(views.Demographics,{'nonstudent': False, 'gender': 'Female', 'age': 26, 'risk': 'Agree', 'country': 'DE', 'studies': ''})


                #finish the experiment correctly
                yield (views.Demographics, {'nonstudent': False, 'gender': 'Female', 'age': 26, 'risk': 'Agree', 'country': 'DE', 'studies': 'Economics'})



