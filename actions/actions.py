# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

#Nicht getestet
class get_train_id(Location):
    plan = requests.get("https://api.deutschebahn.com/freeplan/v1/location/" + Location)
    plan = plan.json()
    return plan[0]["id"]

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []
