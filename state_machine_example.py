from transitions import Machine

from social_interaction_cloud.action import ActionRunner
from social_interaction_cloud.basic_connector import BasicSICConnector
from social_interaction_cloud.detection_result_pb2 import DetectionResult

class ExampleRobot(object):
    """Example that shows how to implement a State Machine with pyTransitions. For more information go to
    https://socialrobotics.atlassian.net/wiki/spaces/CBSR/pages/616398873/Python+Examples#State-Machines-with-PyTransitions"""

    # states = ['asleep', 'awake', 'introduced', 'asked_name', 'got_acquainted']

    # states = ['asleep', 'awake', 'introduced', 'asked name', 'recognised', 'not recognised', 'asked age', 'wrong age', 'right age', 'explaining workout', 'select workout program', 
    # 'work out 1', 'work out 2', 'work out 3', 'finish workout', 'logging of']

    states = ['asleep', 'wake_up', 'introduced', 'name_asked', 'recognised', 'workout', 'finish_workout', 'logging_of']


    def __init__(self, sic: BasicSICConnector):
        self.sic = sic
        self.action_runner = ActionRunner(self.sic)
        # self.name = namelist

        self.user_model = {}
        self.recognition_manager = {'attempt_success': False, 'attempt_number': 0}

        transitions = [
            {'trigger':'start', 'source': 'asleep', 'dest': 'wake_up'},
            {'trigger': 'wake_up_2', 'source': 'wake_up', 'dest': 'introduced'},
            {'trigger': 'ask_name', 'source': 'introduced', 'dest': 'name_asked'},
            {'trigger': 'recognise', 'source': 'name_asked', 'dest': 'recognised'},
            {'trigger': 'start_workout', 'source': 'recognised', 'dest': 'workout'},
            {'trigger': 'timer', 'source': 'workout', 'dest': 'finish_workout'},
            {'trigger': 'say_goodbye', 'source': 'finish_workout', 'dest': 'logging_of'} ]

        self.machine = Machine(model=self, states=ExampleRobot.states, transitions=transitions, initial='asleep')
        if self.state == 'asleep':
            # print("test")
            print(self.state)
            self.start()

        
        if self.state == 'wake_up':
            # print("test2")
            self.wake_up_2()
            print(self.state)
            # print("test2")
        
        if self.state == 'introduced':
            self.ask_name()
            print(self.state)

        if self.state == 'name_asked':
            correct, name = self._ask_name()
            while self.state == 'name_asked':
                if correct == True:
                    # self.recognise(name)
                    self.recognise()
                else:
                    self.ask_name_again()
            print(self.state)

        if self.state == 'recognised':
            self.start_workout()
            print(self.state)

        if self.state == 'workout':
            self.timer()
            print(self.state)

        if self.state == 'finish_workout':
            self.say_goodbye()
            print(self.state)

        
        if self.state == 'logging_of':
            self.saying_goodbye()
            self.sic.stop()
            return None

            # self.say_goodbye()
            # print(self.state)






    

    def wake_up(self) -> None:
        self.action_runner.load_waiting_action('set_language', 'en-US')
        self.action_runner.load_waiting_action('wake_up')
        print("\n\n state: awake \n\n")
        self.action_runner.run_loaded_actions()

    def introduction(self) -> None:
        self.action_runner.run_waiting_action('say_animated', 'Hi I am Nao and I am a social robot. Let\'s be workout buddies!')


    def _ask_name(self) -> None:
        return True, ["name"]
        

        # while not self.recognition_manager['attempt_success'] and self.recognition_manager['attempt_number'] < 2:
        #     self.action_runner.run_waiting_action('say', 'What is your name?')
        #     self.action_runner.run_waiting_action('speech_recognition', 'answer_name', 3,
        #                                           additional_callback=self.on_intent)
        # self.reset_recognition_management()



    def ask_name_again(self):
        pass

    @property
    def recognised(self):
        # name_list = ['max', 'julian', 'enrico']
        # if name in namelist:
        #     self.recognise()

        print("\n\n state: Recognised \n\n")
        return True

    def on_intent(self, detection_result: DetectionResult) -> None:
        if detection_result and detection_result.intent == 'answer_name' and len(detection_result.parameters) > 0:
            self.user_model['name'] = detection_result.parameters['name'].struct_value['name']
            self.recognition_manager['attempt_success'] = True
        else:
            self.recognition_manager['attempt_number'] += 1

    def reset_recognition_management(self) -> None:
        self.recognition_manager.update({'attempt_success': False, 'attempt_number': 0})

    def has_name(self) -> bool:
        return 'name' in self.user_model

    def get_acquainted_with(self) -> None:
        self.action_runner.run_waiting_action('say_animated', 'Nice to meet you ' + self.user_model['name'])

    def get_acquainted_without(self) -> None:
        self.action_runner.run_waiting_action('say_animated', 'Nice to meet you')

    def saying_goodbye(self) -> None:
        print("\n\n NAO: \"Well this was fun.\"\n\"I will see you around.\" \n\n")
        # self.action_runner.run_waiting_action('say_animated', 'Well this was fun.')
        # self.action_runner.run_waiting_action('say_animated', 'I will see you around.')
        # self.action_runner.run_waiting_action('rest')

    def workout(self) -> None:
        self.action_runner.run_waiting_action('say', 'We are gonna work out together! We are going to do these movements.')
        # workout explanation starts
        # start workout sequence
        # Nao first says name of exxercise. Then demonstrates exercise. Counts down. 

    def finish(self) -> None:
        saying_goodbye(self)



class StateMachineExample(object):

    def __init__(self, server_ip: str, dialogflow_key_file: str, dialogflow_agent_id: str):
        self.sic = BasicSICConnector(server_ip, dialogflow_key_file, dialogflow_agent_id)
        self.sic.start()
        self.robot = ExampleRobot(self.sic)

    def run(self) -> None:

        # self.robot.start()
        self.sic.stop()

example = StateMachineExample('127.0.0.1',
                              '<dialogflow_key_file.json>',
                              '<dialogflow_agent_id>')
example.run()
