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


def url_to_json(link):
    return requests.get(link).json()



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
        return []
        
        
        
class Action_price(Action):
    def name(self):
        return "action_price"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        strt="Passau"
        dstn = tracker.get_slot('stadtname')
        a = build_journey_url(strt, dstn)
        a = url_to_json(a)
        price = a["journeys"][0]["price"]
        print(price)
        if price is not None:
            price = price["amount"]
            msg = f"Du musst um von {strt} nach {dstn} zu kommen {price}€ zahlen."
            dispatcher.utter_message(msg)
        else: 
            msg = "Ein Preis kann leider nicht genannt werden"
            dispatcher.utter_message(msg)
        return []
    
    
    
class Action_train_to_destination(Action):
    def name(self):
        return "action_train_from_to_destination"
        
    def formulate_answer(self, extracted_stepovers):
        journey, middle = extracted_stepovers
        ans = f'Um von {journey[0]["origin"]["name"]} nach {journey[-1]["destination"]["name"]} zu kommen musst du um {journey[0]["departure"][11:16]} zum Gleis Nummer {journey[0]["departurePlatform"]} gehen.' + middle
        return(ans)

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
        stops = url_to_json(journey_url)
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
            
        startstadt = tracker.get_slot('startstadt')
        start = "Passau" if startstadt is None else startstadt
        a = build_journey_url(startstadt, tracker.get_slot('stadtname'))
        print(a)
        b = self.extract_stopovers(a)
        c = self.formulate_answer(b)
        dispatcher.utter_message(c)
        
        return []
           
           
           
class Action_ask_arrival_time(Action):
    
    def name(self):
        return "action_train_arrival_time"
        
    def extract_time(self, journey_url):
        json = url_to_json(journey_url)
        return json["journeys"][0]["legs"][-1]["arrival"][11:16]
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        journey_url = build_journey_url("Passau", tracker.get_slot('stadtname'))
        arrival_time = self.extract_time(journey_url)
        dispatcher.utter_message(f'Du bist um {arrival_time} Uhr da')
        return []
