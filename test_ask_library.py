from utils.ask_library import AskLibrary
from social_interaction_cloud.basic_connector import BasicSICConnector
sir = BasicSICConnector('127.0.0.1',
                        'testagent-nava-6ec5f3b4299a.json',
                        'testagent-nava')
                        


sir.start()
ask_library = AskLibrary(sir)

def main():
    ask_library.ask_name()
    ask_library.ask_age()
    ask_library.ask_height()
    ask_library.ask_weight()
    ask_library.ask_confirmation()
    ask_library.stop()


if __name__ == '__main__':
    main()
