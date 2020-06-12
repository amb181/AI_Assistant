from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction, UserUttered, ActionExecuted
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import requests ,re, pymysql, datetime, time, threading, logging
logger = logging.getLogger(__name__)


class Wolfram(Action):
    def name(self):
        return 'wolfram_alpha'

    def run(self, dispatcher, tracker, domain):
        import wolframalpha
        app_id = "7PL9XG-9KT6V3G5H6"
        message = tracker.latest_message.get('text')
        msg = tracker.get_slot('wfquery')
        print(msg)
        print(message)

        try:
            if not msg:
                pass
                client = wolframalpha.Client(app_id)
                res = client.query(message)
                try:
                    answer = next(res.results).text
                    #for answer in itertools.isslice(res.results, 3):
                    response = answer
                    dispatcher.utter_message(response)
                except StopIteration:
                    answer = "I could not find any results"
                    response = answer
                    dispatcher.utter_message(response)
                return[SlotSet("wfquery", None)]
            else:
                client = wolframalpha.Client(app_id)
                res = client.query(msg)
                try:
                    answer = next(res.results).text
                    #for answer in itertools.isslice(res.results, 3):
                    response = answer
                    dispatcher.utter_message(response)
                except StopIteration:
                    answer = "I could not find any results"
                    response = answer
                    dispatcher.utter_message(response)
                return[SlotSet("wfquery", None)]

        except (AttributeError, TypeError) as e:
                print(e)
                return [FollowupAction('utter_wolfram_alpha_error')]

        return []
