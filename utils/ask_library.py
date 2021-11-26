from social_interaction_cloud.action import ActionRunner
from social_interaction_cloud.basic_connector import BasicSICConnector

class AskLibrary:
    """
    A Library that uses Dialogflow to extract intends from a human-interactor based on speech information.
    """

    def __init__(self, sic: BasicSICConnector):
        self.sic = sic
        self.action_runner = ActionRunner(self.sic)
        self.user_model = {}
        self.recognition_manager = {'attempt_success': False, 'attempt_number': 0}

    def ask_name(self):
        """
        Asks for the name of the human interactor using Dialogflow

        Returns:
            The name of the person as :str or False
        """
        while not self.recognition_manager['attempt_success'] and self.recognition_manager['attempt_number'] < 2:
            # self.action_runner.run_waiting_action('say', 'Hi I am Nao. What is your name?')
            self.action_runner.run_waiting_action('speech_recognition', 'answer_name', 3,
                                                  additional_callback=self.on_intent_name)
        self.reset_recognition_management()

        if 'name' in self.user_model:
            # self.action_runner.run_waiting_action('say', 'Nice to meet you ' + self.user_model['name'])
            return self.user_model['name']
        else:
            # self.action_runner.run_waiting_action('say', 'Nice to meet you')
            return False

    def ask_age(self):
        """
        Asks for the age of the human interactor using Dialogflow

        Returns:
        The age of the person as :str or False
        """
        while not self.recognition_manager['attempt_success'] and self.recognition_manager['attempt_number'] < 2:
            # self.action_runner.run_waiting_action('say', 'how old are you' + self.user_model['name']+'?')
            self.action_runner.run_waiting_action('speech_recognition', 'answer_age', 5,
                                                  additional_callback=self.on_intent_age)
        self.reset_recognition_management()

        if 'age' in self.user_model:
            # self.action_runner.run_waiting_action('say', self.user_model['age']+'wow, you are getting old ' +
            # self.user_model['name'])
            return self.user_model['age']
        else:
            # self.action_runner.run_waiting_action('say', 'you are getting old bro')
            return False

    def ask_height(self):
        """
        Asks for the height of the human interactor using Dialogflow

        Returns:
        The height of the person as :str or False
        """
        while not self.recognition_manager['attempt_success'] and self.recognition_manager['attempt_number'] < 2:
            self.action_runner.run_waiting_action('say', 'how tall are you, bro ?')
            self.action_runner.run_waiting_action('speech_recognition', 'answer_height', 5,
                                                  additional_callback=self.on_intent_height)
        self.reset_recognition_management()

        if 'height' in self.user_model:
            # self.action_runner.run_waiting_action('say', str(self.user_model['height'])+'wow, you are tall ')
            return self.user_model['height']
        else:
            # self.action_runner.run_waiting_action('say', 'I did not get it, bro')
            return False

    def ask_weight(self):
        """
        Asks for the weight of the human interactor using Dialogflow

        Returns:
        The weight of the person as :str or False
        """

        #TODO: fix this functioN!
        return 50.

        while not self.recognition_manager['attempt_success'] and self.recognition_manager['attempt_number'] < 5:
            self.action_runner.run_waiting_action('say', 'What is your weight, bro?')
            self.action_runner.run_waiting_action('speech_recognition', 'answer_weight', 5,
                                                  additional_callback=self.on_intent_weight)
        self.reset_recognition_management()
        if 'weight' in self.user_model:
            # self.action_runner.run_waiting_action('say', str(self.user_model['weight'])+'wow, you are fat as fuck,
            # my bro double cheese')
            return self.user_model['weight']
        else:
            # self.action_runner.run_waiting_action('say', 'I did not get it, bro')
            return False

    def ask_confirmation(self):
        """
        Asks the human interactor for a confirmation to start the workout and extracts the intent using Dialogflow.

        Returns:
        The result of the confirmation
        """

        while not self.recognition_manager['attempt_success'] and self.recognition_manager['attempt_number'] < 10:
            self.action_runner.run_waiting_action('speech_recognition', 'Yes_No_answer', 5,
                                                  additional_callback=self.on_intent_yes_no)
        self.reset_recognition_management()
        if 'Yes_No_answer' in self.user_model:
            return self.user_model['Yes_No_answer']
            # if self.user_model['Yes_No_answer']=='yes': self.action_runner.run_waiting_action('say', 'Your answer
            # was '+ self.user_model['Yes_No_answer']+'. good! workout will begin') if self.user_model[
            # 'Yes_No_answer']=='no': self.action_runner.run_waiting_action('say', 'Your answer was
            # '+self.user_model['Yes_No_answer']+'. wow, you are fat as fuck, and you will continue to be')
        else:
            # self.action_runner.run_waiting_action('say', 'I did not get it, bro')
            return False

    def on_intent_name(self, detection_result: dict) -> None:
        """
        Asks for the name of the human interactor using Dialogflow

        Returns:
        The name of the person as :str or False
        """
        # print("name - detection_result",detection_result)
        if detection_result and 'intent' in detection_result and detection_result['intent'] == 'answer_name' \
                and 'parameters' in detection_result and 'name' in detection_result['parameters'] and \
                detection_result['parameters']['name'] != []:
            self.user_model['name'] = detection_result['parameters']['name'][0]['name']
            self.recognition_manager['attempt_success'] = True
        else:
            self.recognition_manager['attempt_number'] += 1

    def on_intent_age(self, detection_result: dict) -> None:
        """
        Detects the intent age using Dialogflof

        Returns:
        Overrides the detection_results :dict by setting 'attempt_success' either to true or false and the
        'age' to the :float valued age.

        Returns:
        The age of the person as :str or False
        """
        # print("age-detection_result",detection_result)
        if detection_result and 'parameters' in detection_result and 'age' in detection_result['parameters'] and \
                detection_result['parameters']['age'] != []:
            self.user_model['age'] = str(int(detection_result['parameters']['age'][0]['amount']))
            self.recognition_manager['attempt_success'] = True
        else:
            self.recognition_manager['attempt_number'] += 1

    def on_intent_height(self, detection_result: dict) -> None:
        """
        Detects the intent height using Dialogflof

        Returns:
        Overrides the detection_results :dict by setting 'attempt_success' either to true or false and the
        'height' to the :float valued height.
        """
        # print("height-detection_result",detection_result)
        if detection_result and 'parameters' in detection_result and 'height' in detection_result['parameters'] and \
                detection_result['parameters']['height'] != []:
            self.user_model['height'] = str(detection_result['parameters']['height'][0])
            self.recognition_manager['attempt_success'] = True
        else:
            self.recognition_manager['attempt_number'] += 1

    def on_intent_weight(self, detection_result: dict) -> None:
        """
        Detects the intent weight using Dialogflof

        Returns:
        Overrides the detection_results :dict by setting 'attempt_success' either to true or false and the
        'weight' to the :float valued weight.
        """
        # print("weight-detection_result",detection_result)
        if detection_result and 'parameters' in detection_result and 'weight' in detection_result['parameters'] and \
                detection_result['parameters']['weight'] != []:
            self.user_model['weight'] = str(detection_result['parameters']['weight'][0])
            self.recognition_manager['attempt_success'] = True
        else:
            self.recognition_manager['attempt_number'] += 1

    def on_intent_yes_no(self, detection_result: dict) -> None:
        """
        Detects an intent (yes or no) using Dialogflow

        Returns:
        Overrides the detection_results :dict by setting 'attempt_success' either to true or false and the
        'Yes_No_Answer' either to Yes or No.
        """
        #print(detection_result)
        if detection_result and 'parameters' in detection_result and 'yes' in detection_result['parameters'] and 'no' in \
                detection_result['parameters']:
            #print("okay great")

            if detection_result['parameters']['yes'] == '' and detection_result['parameters']['no'] != '':
                self.user_model['Yes_No_answer'] = 'no'
                #print("NO")
                self.recognition_manager['attempt_success'] = True
            else:
                if detection_result['parameters']['no'] == '' and detection_result['parameters']['yes'] != '':
                    self.user_model['Yes_No_answer'] = 'yes'
                    #print("YES")
                    self.recognition_manager['attempt_success'] = True
                else:
                    if detection_result['parameters']['no'] != '' and detection_result['parameters']['yes'] != '':
                        if detection_result['parameters']['no'] in detection_result['text']:
                            self.user_model['Yes_No_answer'] = 'no'
                            #print("NO")
                            self.recognition_manager['attempt_success'] = True
                        if detection_result['parameters']['yes'] in detection_result['text']:
                            self.user_model['Yes_No_answer'] = 'yes'
                            #print("YES")
                            self.recognition_manager['attempt_success'] = True
        else:
            self.recognition_manager['attempt_number'] += 1

    def stop(self):
        """
        A function to stop the robot
        """
        self.action_runner.run_waiting_action('rest')
        self.sic.stop()

    def reset_recognition_management(self) -> None:
        """
        Resets the recognition manager when needed
        """
        self.recognition_manager.update({'attempt_success': False, 'attempt_number': 0})
