from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction, UserUttered, ActionExecuted
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import requests ,re, pymysql, datetime, time, threading, logging
logger = logging.getLogger(__name__)


class RequestAnother(Action):
    def name(self):
        return 'action_request_another'
   
    def run(self, dispatcher, tracker, domain):
        last_intent = str(tracker.latest_message['intent']['name'])
        print("/_______{}________/".format(last_intent))
        last_working_with = str(tracker.latest_message['entities'][0]['entity'])
        print("/{}/".format(last_working_with))
        
        for e in reversed(tracker.events):
            if e['event'] == "action":
                print (e['name'])
                if 'spend' in e['name']:
                    return [FollowupAction('action_request_spend')]
                    break
                elif 'category_manager' in e['name']:
                    return [FollowupAction('action_request_category_manager')]
                    break
                elif 'contract' in e['name']:
                    if 'supplier_name' in last_working_with:
                        return [FollowupAction('supplier_lookup_for_contract')]
                    else:
                        return [FollowupAction('supplier_contract_form')]
                    break
                elif 'existing' in e['name']:
                    if 'supplier_name' in last_working_with:
                        return [FollowupAction('supplier_lookup_for_existing_supplier')]
                    else:
                        return [FollowupAction('supplier_existing_form')]
                    break
            # else:
            #     return [FollowupAction('wolfram_alpha')]
            #     break