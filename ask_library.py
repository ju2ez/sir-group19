from social_interaction_cloud.action import ActionRunner
from social_interaction_cloud.basic_connector import BasicSICConnector

class AskLibrary:

    def __init__(self, server_ip: str, dialogflow_key_file: str, dialogflow_agent_id: str):
        self.sic = BasicSICConnector(server_ip, 'en-US', dialogflow_key_file, dialogflow_agent_id)
        self.action_runner = ActionRunner(self.sic)
        self.user_model = {}
        self.recognition_manager = {'attempt_success': False, 'attempt_number': 0}

    def ask_name(self):
        while not self.recognition_manager['attempt_success'] and self.recognition_manager['attempt_number'] < 2:
            self.action_runner.run_waiting_action('say', 'Hi I am Nao. What is your name?')
            self.action_runner.run_waiting_action('speech_recognition', 'answer_name', 3,
                                                  additional_callback=self.on_intent_name)
        self.reset_recognition_management()

        if 'name' in self.user_model:
            self.action_runner.run_waiting_action('say', 'Nice to meet you ' + self.user_model['name'])
        else:
            self.action_runner.run_waiting_action('say', 'Nice to meet you')
        
    def ask_age(self):
        while not self.recognition_manager['attempt_success'] and self.recognition_manager['attempt_number'] < 2:
            self.action_runner.run_waiting_action('say', 'how old are you' + self.user_model['name']+'?')
            self.action_runner.run_waiting_action('speech_recognition', 'answer_age', 5,
                                                    additional_callback=self.on_intent_age)
        self.reset_recognition_management()

        if 'age' in self.user_model:
            self.action_runner.run_waiting_action('say', self.user_model['age']+'wow, you are getting old ' + self.user_model['name'])
        else:
            self.action_runner.run_waiting_action('say', 'you are getting old bro')

    def ask_height(self):
        while not self.recognition_manager['attempt_success'] and self.recognition_manager['attempt_number'] < 2:
            self.action_runner.run_waiting_action('say', 'how tall are you, bro ?')
            self.action_runner.run_waiting_action('speech_recognition', 'answer_height', 5,
                                                    additional_callback=self.on_intent_height)
        self.reset_recognition_management()

        if 'height' in self.user_model:
            self.action_runner.run_waiting_action('say', str(self.user_model['height'])+'wow, you are tall ')
        else:
            self.action_runner.run_waiting_action('say', 'I did not get it, bro')
    
    def ask_weight(self):
        while not self.recognition_manager['attempt_success'] and self.recognition_manager['attempt_number'] < 5:
            self.action_runner.run_waiting_action('say', 'What is your weight, bro?')
            self.action_runner.run_waiting_action('speech_recognition', 'answer_weight', 5,
                                                    additional_callback=self.on_intent_weight)
        self.reset_recognition_management()

        if 'weight' in self.user_model:
            self.action_runner.run_waiting_action('say', str(self.user_model['weight'])+'wow, you are fat as fuck, my bro double cheese')
        else:
            self.action_runner.run_waiting_action('say', 'I did not get it, bro')
    
    def ask_confirmation(self):
        while not self.recognition_manager['attempt_success'] and self.recognition_manager['attempt_number'] < 11:
            self.action_runner.run_waiting_action('say', 'Are you ready for the workout, bro?')
            self.action_runner.run_waiting_action('speech_recognition', 'Yes_No_answer', 7,
                                                    additional_callback=self.on_intent_Yes_No)
        self.reset_recognition_management()

        if 'Yes_No_answer' in self.user_model:
            if self.user_model['Yes_No_answer']=='yes':
                self.action_runner.run_waiting_action('say', 'Your answer was '+self.user_model['Yes_No_answer']+'. good! workout will begin')
            if self.user_model['Yes_No_answer']=='no':
                self.action_runner.run_waiting_action('say', 'Your answer was '+self.user_model['Yes_No_answer']+'. wow, you are fat as fuck, and you will continue to be')
        
        else:
            self.action_runner.run_waiting_action('say', 'I did not get it, bro')

    def on_intent_name(self, detection_result: dict) -> None:
        #print("name - detection_result",detection_result)
        if detection_result and 'intent' in detection_result and detection_result['intent'] == 'answer_name' \
                and 'parameters' in detection_result and 'name' in detection_result['parameters'] and detection_result['parameters']['name']!=[]:
            self.user_model['name'] = detection_result['parameters']['name'][0]['name']
            self.recognition_manager['attempt_success'] = True
        else:
            self.recognition_manager['attempt_number'] += 1

    def on_intent_age(self, detection_result: dict) -> None:
        #print("age-detection_result",detection_result)
        if detection_result and 'parameters' in detection_result and 'age' in detection_result['parameters'] and detection_result['parameters']['age']!=[]:
            self.user_model['age'] = str(int(detection_result['parameters']['age'][0]['amount']))
            self.recognition_manager['attempt_success'] = True
        else:
            self.recognition_manager['attempt_number'] += 1
    
    def on_intent_height(self, detection_result: dict) -> None:
        #print("height-detection_result",detection_result)
        if detection_result and 'parameters' in detection_result and 'height' in detection_result['parameters'] and detection_result['parameters']['height']!=[]:
            self.user_model['height'] = str(detection_result['parameters']['height'][0])
            self.recognition_manager['attempt_success'] = True
        else:
            self.recognition_manager['attempt_number'] += 1

    def on_intent_weight(self, detection_result: dict) -> None:
        #print("weight-detection_result",detection_result)
        if detection_result and 'parameters' in detection_result and 'weight' in detection_result['parameters'] and detection_result['parameters']['weight'] != []:
            self.user_model['weight'] = str(detection_result['parameters']['weight'][0])
            self.recognition_manager['attempt_success'] = True
        else:
            self.recognition_manager['attempt_number'] += 1
            
    def on_intent_Yes_No(self, detection_result: dict) -> None:
        #print("Yes_No_answer-detection_result",detection_result)
        if detection_result and 'parameters' in detection_result and 'yes' in detection_result['parameters'] and 'no' in detection_result['parameters']:
            print("okay great")

            if detection_result['parameters']['yes']=='' and detection_result['parameters']['no']!='': 
                self.user_model['Yes_No_answer'] = 'no'
                print("NO")
                self.recognition_manager['attempt_success'] = True
            else:
                if detection_result['parameters']['no']==''and detection_result['parameters']['yes']!='': 
                    self.user_model['Yes_No_answer'] = 'yes'  
                    print("YES")
                    self.recognition_manager['attempt_success'] = True
                else:
                    if detection_result['parameters']['no']!=''and detection_result['parameters']['yes']!='': 
                        if detection_result['parameters']['no'] in detection_result['text']:
                            self.user_model['Yes_No_answer'] = 'no'
                            print("NO")
                            self.recognition_manager['attempt_success'] = True
                        if detection_result['parameters']['yes'] in detection_result['text']:
                            self.user_model['Yes_No_answer'] = 'yes'
                            print("YES")
                            self.recognition_manager['attempt_success'] = True   
        else:
            self.recognition_manager['attempt_number'] += 1

    def stop(self):
        self.action_runner.run_waiting_action('rest')
        self.sic.stop()
         
    def reset_recognition_management(self) -> None:
        self.recognition_manager.update({'attempt_success': False, 'attempt_number': 0})



