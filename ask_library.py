from social_interaction_cloud.action import ActionRunner
from social_interaction_cloud.basic_connector import BasicSICConnector

user_model = {}
recognition_manager = {'attempt_success': False, 'attempt_number': 0}
sic = None
action_runner=None

def initiate(server_ip: str, dialogflow_key_file: str, dialogflow_agent_id: str):
    sic = BasicSICConnector(server_ip, 'en-US', dialogflow_key_file, dialogflow_agent_id)
    action_runner = ActionRunner(sic)

def ask_name():
    while not recognition_manager['attempt_success'] and recognition_manager['attempt_number'] < 2:
        action_runner.run_waiting_action('say', 'Hi I am Nao. What is your name?')
        action_runner.run_waiting_action('speech_recognition', 'answer_name', 3,
                                                additional_callback=on_intent_name)
    reset_recognition_management()

    if 'name' in user_model:
        action_runner.run_waiting_action('say', 'Nice to meet you ' + user_model['name'])
    else:
        action_runner.run_waiting_action('say', 'Nice to meet you')


def ask_age():
    while not recognition_manager['attempt_success'] and recognition_manager['attempt_number'] < 2:
        action_runner.run_waiting_action('say', 'how old are you' + user_model['name']+'?')
        action_runner.run_waiting_action('speech_recognition', 'answer_age', 5,
                                                additional_callback=on_intent_age)
    reset_recognition_management()

    if 'age' in user_model:
        action_runner.run_waiting_action('say', str(int(user_model['age']))+'wow, you are getting old ' + user_model['name'])
    else:
        action_runner.run_waiting_action('say', 'you are getting old bro')

def ask_height():
    while not recognition_manager['attempt_success'] and recognition_manager['attempt_number'] < 2:
        action_runner.run_waiting_action('say', 'how tall you bro' + user_model['height']+'?')
        action_runner.run_waiting_action('speech_recognition', 'answer_height', 5,
                                                additional_callback=on_intent_height)
    reset_recognition_management()

    if 'age' in user_model:
        action_runner.run_waiting_action('say', str(int(user_model['age']))+'wow, you are getting old ' + user_model['name'])
    else:
        action_runner.run_waiting_action('say', 'you are getting old bro')

def on_intent_name(detection_result: dict) -> None:
    print("name - detection_result",detection_result)
    if detection_result and 'intent' in detection_result and detection_result['intent'] == 'answer_name' \
            and 'parameters' in detection_result and 'name' in detection_result['parameters']:
        user_model['name'] = detection_result['parameters']['name'][0]['name']
        recognition_manager['attempt_success'] = True
    else:
        recognition_manager['attempt_number'] += 1



def on_intent_age(detection_result: dict) -> None:
    print("age-detection_result",detection_result)

    if detection_result and 'parameters' in detection_result and 'age' in detection_result['parameters']:
        user_model['age'] = detection_result['parameters']['age'][0]['amount']
        recognition_manager['attempt_success'] = True
    else:
        recognition_manager['attempt_number'] += 1

def stop():
    action_runner.run_waiting_action('rest')
    sic.stop()
    
def reset_recognition_management() -> None:
    recognition_manager.update({'attempt_success': False, 'attempt_number': 0})
