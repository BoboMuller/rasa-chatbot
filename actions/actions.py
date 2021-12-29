# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests


def get_train_id(Location):
    plan = requests.get("https://api.deutschebahn.com/freeplan/v1/location/" + Location)
    # print(plan)
    plan = plan.json()
    return plan[0]["id"]


def build_journey_url(start, end, time_from_now=0, results=1):
        start = get_train_id(start)
        if end == "Deggendorf":
            end = 8001397
        else:
            end = get_train_id(end)
        return f'https://v5.db.transport.rest/journeys?from={start}&to={end}&results={results}'


def formulate_answer(extracted_stepovers):
        journey, middle = extracted_stepovers
        ans = f'Um von {journey[0]["origin"]["name"]} nach {journey[-1]["destination"]["name"]} zu kommen musst du um {journey[0]["departure"][11:16]} zum Gleis Nummer {journey[0]["departurePlatform"]} gehen.' + middle
        return(ans)

class Action_fav_route(Action):
    def name(self):
        return "action_fav_route"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        fav = tracker.get_slot('stadtname')
        SlotSet('fav',fav)
        msg = f'{fav} wurde als Favorit hinterlegt.'
        dispatcher.utter_message(msg)
        pass
        
class Utter_price(Action):
    def name(self):
        return "utter_price"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        strt="Passau"
        dstn = tracker.get_slot('stadtname')
        a = build_journey_url(strt, dstn)
        price = a[journeys[0]["price"]]
        msg = f"Du musst um von {strt} nach {stadtname} zu kommen {price}€ Zahlen"
        dispatcher.utter_message(msg)
        pass
    
class Action_train_to_destination(Action):
    def name(self):
        return "action_train_to_destination"
        

    def extract_stopovers(self, journey_url):
        halts = []
        middle = ""
        formulierung = " Umstiege sind bei "
        # Deggendorf ID 8001397
        # departure inklusive verspätung falls vorhanden
        # departuredelay in sekunden
        # departurePlatform: Gleis bei Abfahrt
        # arrivalPlatform: Gleis bei Ankunft
        # Array in legs bestehend aus Arrays mit den verschiedenen Einzelfahrten von a nach b
        stops = requests.get(journey_url).json()
        journey = stops["journeys"][0]["legs"]
        if len(journey) > 1:
            for umstieg in journey[:-1]:
                halts.append(umstieg["destination"]["name"])
            for stop in halts[:-1]:
                if middle != "":
                    middle = middle + ", " + stop
                else:
                    middle = stop
            if middle == "":
                middle = formulierung + middle + halts[-1] + " erforderlich."
            else:
                middle = formulierung + middle + " und " + halts[-1] + " erforderlich."
        return journey, middle

    
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        a = build_journey_url("Passau", tracker.get_slot('stadtname'))
        b = self.extract_stopovers(a)
        c = formulate_answer(b)
        dispatcher.utter_message(c)
        
        return []
           
class Action_ask_time(Action):
    
    def name(self):
        return "action_train_arrival_time"
        
    def extract_time(self, journey_url):
            pass
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        journey_url = build_journey_url("Passau", tracker.get_slot('stadtname'))
        b = journey_url["journeys"][0]["legs"][-1]["arrival"][11:16]
        
        dispatcher.utter_message(b)
        
        return []
    

# class ActionHelloWorld(Action):

    # def name(self) -> Text:
        # return "action_details"

    # def run(self, dispatcher: CollectingDispatcher,
            # tracker: Tracker,
            # domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # dispatcher.utter_message(text="Hello World!")

        # return []
