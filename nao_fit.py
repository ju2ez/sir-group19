import datetime
import time
from typing import Callable

from utils.ask_library import AskLibrary
from transitions import Machine

from social_interaction_cloud.action import ActionRunner
from social_interaction_cloud.basic_connector import BasicSICConnector

import pandas as pd


class NaoFit:
    """
    The NaoFit main class.
    Implements the whole flow of human-robot interaction using a state-machine scheme.
    Nao-Fit does a workout with the user, depending on your BMI and age.
    """

    states = ['asleep', 'wake_up', 'introduce', 'ask_workout', 'ask_name', 'ask_age', 'recognise', 'ask_weight',
              'ask_height', 'workout', 'finish_workout', 'logging_off', 'ask_again']

    def __init__(self, sic: BasicSICConnector):
        """
        Initializes the BasicConnector, AskLibrary and state-machine transitions
        """
        self.sic = sic
        self.action_runner = ActionRunner(self.sic)
        # self.name = namelist

        self.ask_nao = AskLibrary(sic)

        self.user_model = {}
        self.recognition_manager = {'attempt_success': False, 'attempt_number': 0}
        self.user_recognised = False
        self.file = pd.read_csv('data/user_data.csv')

        transitions = [
            {'trigger': 'start', 'source': 'asleep', 'dest': 'wake_up'},
            {'trigger': 'intro', 'source': 'wake_up', 'dest': 'introduce'},
            {'trigger': 'work', 'source': 'introduce', 'dest': 'ask_workout'},
            {'trigger': 'name', 'source': 'ask_workout', 'dest': 'ask_name'},
            {'trigger': 'age', 'source': 'ask_name', 'dest': 'ask_age'},
            {'trigger': 'rec', 'source': 'ask_age', 'dest': 'recognise'},
            {'trigger': 'start_workout', 'source': 'recognise', 'dest': 'workout'},
            {'trigger': 'height', 'source': 'recognise', 'dest': 'ask_height'},
            {'trigger': 'weight', 'source': 'ask_height', 'dest': 'ask_weight'},
            {'trigger': 'start_workout', 'source': 'ask_weight', 'dest': 'workout'},
            {'trigger': 'workout_done', 'source': 'workout', 'dest': 'finish_workout'},
            {'trigger': 'workout_done', 'source': 'ask_workout', 'dest': 'finish_workout'},
            {'trigger': 'say_goodbye', 'source': 'finish_workout', 'dest': 'logging_off'}]

        self.machine = Machine(model=self, states=NaoFit.states, transitions=transitions, initial='asleep')

        # In the following, state transitions are defined
        if self.state == 'asleep':
            print(self.state)
            self.start()

        if self.state == 'wake_up':
            print(self.state)
            self.intro()

        if self.state == 'introduce':
            print(self.state)
            self.handle_introduction()
            self.work()

        if self.state == 'ask_workout':
            print(self.state)
            ready = self.handle_ask_workout()
            if ready == 'Yes' or ready == 'YES' or ready == 'yes':
                self.name()
            # assume answer is no and end
            else:
                # print('The answer was:', ready)
                # print('Ending the workout..')
                self.workout_done()

        if self.state == 'ask_name':
            print(self.state)
            # print(name)

            name = self.handle_ask_name()
            if name is False:
                self.handle_ask_again()
            else:
                # set the name and switch to next state
                self.name = name
                self.age()

        if self.state == 'ask_age':
            print(self.state)
            age = self.handle_ask_age()
            if age is False:
                self.handle_ask_again()
            else:
                # set the age for later database usage

                # TODO: add the possiblity to call parents if age is too low
                self.age = int(age)
                if self.age <= 8:
                    self.action_runner.run_waiting_action('say', 'Great, please ask your parents to come here.')
                    self.action_runner.run_waiting_action('say', 'I will wait until your parents are here')
                    time.sleep(5) 

                self.rec()

        if self.state == 'recognise':
            print(self.state)
            # Todo Fix recognition
            recognise = self.handle_recognise()
            if recognise is False:
                self.height()
            else:
                self.start_workout()

        if self.state == 'ask_height':
            print(self.state)
            # save height for later
            self.height = self.handle_ask_height()
            # print('height:', self.height)
            self.weight()

        if self.state == 'ask_weight':
            print(self.state)
            # save weight for later
            self.weight = self.handle_ask_weight()
            # print('weight:', self.weight)
            self.start_workout()

        if self.state == 'workout':
            print(self.state)
            self.handle_workout()
            self.workout_done()

        if self.state == 'finish_workout':
            print(self.state)
            self.handle_finish()
            self.say_goodbye()

        if self.state == 'logging_off':
            print(self.state)
            self.handle_saying_goodbye()
            self.sic.stop()
            exit()

        if self.state == 'ask_again':
            # for now this state is not needed and unreachable!
            # However self.handle_ask_again() is used!
            print(self.state)

    # Now from here on are the functions that handle the interactions:
    # Like asking questions and dealing with the replies.

    def ask_until_answer(self, question_func: Callable):
        """
        This function asks a question until it gets a valid answer.
        It expects a function from the ask_library class as :str
        """
        var = False
        while var is False:
            var = question_func()
            if var is False:
                self.handle_ask_again()
        return var

    def handle_wake_up(self) -> None:
        """
        Handles the necessary tasks when nao wakes up
        """
        self.action_runner.load_waiting_action('set_language', 'en-US')
        self.action_runner.load_waiting_action('wake_up')
        print("\n\n state: awake \n\n")
        self.action_runner.run_loaded_actions()

    def handle_introduction(self) -> None:
        """
        Initiates an introduction
        """
        self.action_runner.run_waiting_action('say_animated',
                                              'Hi I am Nao-Fit. Your personal trainer. Let\'s be workout buddies!')
        return None

    def handle_ask_workout(self):
        """
        Asks if the user is ready to work out
        """
        self.action_runner.run_waiting_action('say', 'Are you ready for the workout?')
        confirm = self.ask_until_answer(self.ask_nao.ask_confirmation)
        return confirm

    def handle_ask_name(self):
        """
        Asks for the name of the user
        """

        self.action_runner.run_waiting_action('say_animated', 'Could you please tell me your name?')
        name = self.ask_until_answer(self.ask_nao.ask_name)
        return name

    def handle_ask_again(self):
        """
        Asks if the user could repeat the answer
        """
        self.action_runner.run_waiting_action('say_animated', 'I did not understand that. Could you repeat that?')
        return

    def handle_ask_age(self):
        """
        Asks for the age of the user
        """
        self.action_runner.run_waiting_action('say_animated', 'Awesome. And how old are you?')
        age = self.ask_until_answer(self.ask_nao.ask_age)
        return age

    def handle_recognise(self):
        """
        Checks if the user is already in the databse
        """
        df_dummy_database = self.file
        if self.name in df_dummy_database.loc[df_dummy_database['age'] == self.age].values:
            self.action_runner.run_waiting_action('say_animated', f'Welcome Back {self.name}!')
            return True
        else:
            return False
        # name_list = ['max', 'julian', 'enrico']
        # if name in namelist:
        #     self.recognise()

    def handle_ask_height(self):
        """
        Asks for the height of the user
        """
        self.action_runner.run_waiting_action('say_animated', 'Thank you! Now please tell me your height?')
        height = self.ask_until_answer(self.ask_nao.ask_height)
        return height

    def handle_ask_weight(self):
        """
        Asks for the weight of the user
        """
        self.action_runner.run_waiting_action('say_animated', f'Incredibble {self.name}! Lastly I would like to know'
                                                              'how much you weight? ')
        weight = self.ask_until_answer(self.ask_nao.ask_weight)
        return weight

    def reset_recognition_management(self) -> None:
        """
        Resets the recognition manager
        """
        self.recognition_manager.update({'attempt_success': False, 'attempt_number': 0})

    def handle_saying_goodbye(self) -> None:
        """
       Says goodbye to the user
        """
        print("\n\n NAO: \"Well this was fun.\"\n\"I will see you around.\" \n\n")
        self.action_runner.run_waiting_action('say_animated', 'I will see you around.')
        self.action_runner.run_waiting_action('rest')
        return

    def handle_workout(self) -> None:
        """
        Calculates the BMI based on the values that are given by the user.
        Initiates a workout based on the BMI.
        """
        self.action_runner.run_waiting_action('say',
                                              'That is so nice. We are gonna work out together!')

        user_bmi = int(float(self.weight) / (float(self.height) * float(self.height)))
        if user_bmi < 26:
            self.action_runner.run_waiting_action('do_gesture', "workout1/behavior_1")
        else:
            self.action_runner.run_waiting_action('do_gesture', 'workout1/behavior_1')

        # try:
            
        #     if user_bmi > 50:
        #         self.action_runner.run_waiting_action('do_gesture', "workout1/behavior_1")
        #     else:
        #         # TODO: create and add gestures for workout2
        #         self.action_runner.run_waiting_action('do_gesture', 'workout1/behavior_1')
        # except:
        #     self.action_runner.run_waiting_action('do_gesture', "workout1/behavior_1")

        # ToDO: wait here until the gesture is completly finished!


        # workout explanation starts
        # start workout sequence
        # Nao first says name of exxercise. Then demonstrates exercise. Counts down. 

    def handle_finish(self) -> None:
        """
        Finishes the whole flow and stores information into the dataframe
        """
        self.action_runner.run_waiting_action('say', ' This was so much fun!')

        # now write everything into the database
        df_user_info = pd.DataFrame({'name': self.name, 'age': self.age, 'height': self.height, 'weight:': self.weight,
                                     'date': datetime.date.today()})
        df_dummy_db = self.file.append(df_user_info)
        df_dummy_db.to_csv('data/user_data.csv')
        return None


class StateMachineInit(object):
    """
    A simple class that initiates the Nao-Fit when this file is executed from the console
    """
    def __init__(self, server_ip: str, dialogflow_key_file: str, dialogflow_agent_id: str):
        self.sic = BasicSICConnector(server_ip, 'en-US', dialogflow_key_file, dialogflow_agent_id)

    def run(self) -> None:
        """
        Starts the whole procedure and stops it when finished.
        """
        self.sic.start()
        self.robot = NaoFit(self.sic)
        print('byeee')
        self.sic.stop()


simple_nao_fit = StateMachineInit('127.0.0.1',
                                  'testagent-nava-6ec5f3b4299a.json',
                                  'testagent-nava')
simple_nao_fit.run()
