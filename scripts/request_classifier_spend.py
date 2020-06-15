from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction, UserUttered, ActionExecuted
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import requests ,re, pymysql, datetime, time, threading, logging
logger = logging.getLogger(__name__)


class RequestCategoryManager(Action):
    def name(self):
        return 'action_request_spend'
   
    def run(self, dispatcher, tracker, domain):
        with open('data/lookup-tables/categories.txt') as f:
            entity = tracker.get_slot('supplier_name')
            if entity in f:
                return [SlotSet("category_name", entity), SlotSet("supplier_name", None)]
                
        if not tracker.latest_message['entities']:
            for e in reversed(tracker.events):
                if e['event'] == "action":
                    print (e['name'])
                    if "supplier" in e['name']:
                        print("indetified last action as " + e['name'])
                        last_working_with = "supplier"
                        break
                    elif "category" in e['name'] and "manager" not in e['name']:
                        print("indetified last action as " + e['name'])
                        last_working_with = "category"
                        break
        else:
            last_working_with = str(tracker.latest_message['entities'][0]['entity'])
        print("/_______{}________/".format(last_working_with))
        if (re.search('supplier', last_working_with)):
            supplier = tracker.get_slot('supplier_name')
            print("{} is a supplier".format(supplier))
            return [SlotSet("category_name", None), FollowupAction('supplier_lookup')]
            
        elif (re.search('category', last_working_with)):
            category = tracker.get_slot('category_name')
            print("{} is a category".format(category))
            return [SlotSet("supplier_name", None), FollowupAction('category_lookup')]
        else:
            supplier = tracker.get_slot('supplier_name')
            category = tracker.get_slot('category_name')
            if (supplier != None):
                return [SlotSet("category_name", None), FollowupAction('supplier_lookup')]
            elif (category != None):
                return [SlotSet("supplier_name", None), FollowupAction('category_lookup')]
