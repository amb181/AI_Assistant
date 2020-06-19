from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, FollowupAction, UserUttered, ActionExecuted, EventType, UserUtteranceReverted, ConversationPaused
from rasa_sdk.executor import CollectingDispatcher 
from scripts import request_wolframalpha, request_category_spend, request_supplier_spend, request_classifier_spend, request_another
from scripts import request_category_cm, request_supplier_cm, request_supplier_contract 
from scripts import request_supplier_onboarding, request_wigslookup, request_supplier_existing, request_dowjones, request_classifier_cm

import requests ,re, pymysql, datetime, time, threading, logging
logger = logging.getLogger(__name__)



########## Two stage fallback payload #########


class ActionDefaultAskAffirmation(Action):
    """Asks for an affirmation of the intent if NLU threshold is not met."""

    def name(self) -> Text:
        return "action_default_ask_affirmation"

    def __init__(self) -> None:
        import csv

        self.intent_mappings = {}
        with open('intent_mapping.csv',
                  newline='',
                  encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                self.intent_mappings[row[0]] = row[1]

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List['Event']:

        intent_ranking = tracker.latest_message.get('intent_ranking', [])
        if len(intent_ranking) > 1:
            diff_intent_confidence = (intent_ranking[0].get("confidence") -
                                      intent_ranking[1].get("confidence"))
            if diff_intent_confidence < 0.2:
                intent_ranking = intent_ranking[:2]
            else:
                intent_ranking = intent_ranking[:1]
        first_intent_names = [intent.get('name', '')
                              for intent in intent_ranking
                              if intent.get('name', '') != 'out_of_scope']

        message_title = "Sure, to be clear did you mean... "

        mapped_intents = [(name, self.intent_mappings.get(name, name))
                          for name in first_intent_names]

        entities = tracker.latest_message.get("entities", [])
        entities_json, entities_text = get_formatted_entities(entities)
        message = tracker.latest_message.get('text')

        buttons = []
        for intent in mapped_intents:
            # buttons.append({'title': intent[1] + entities_text,
            buttons.append({'title': intent[1],
                            'payload': '/{}{}'.format(intent[0],
                                                      entities_json)})

        buttons.append({'title': 'Ask Wolfram',
                        'payload': "/wolframalpha_whatis{\"wfquery\":\"" +
                                   message + "\"}"})

        # buttons.append({'title': 'I feel lucky',
        #                   'payload': '/wolframalpha_whatis'})

        # buttons.append({'title': 'Something else',
        #                 'payload': '/utter_default'})

        dispatcher.utter_button_message(message_title, buttons=buttons)

        return [SlotSet("wfquery", message)]


def get_formatted_entities(entities: List[Dict[str, Any]]) -> (Text, Text):
    import json
    key_value_entities = {}
    for e in entities:
        key_value_entities[e.get("entity")] = e.get("value")
    entities_json = ""
    entities_text = ""
    if len(entities) > 0:
        entities_json = json.dumps(key_value_entities)
        entities_text = ["for {}".format(key_value_entities[k])
                         for k in key_value_entities]
        entities_text = ", ".join(entities_text)
        entities_text = " {}".format(entities_text)

    return entities_json, entities_text


class ActionDefaultFallback(Action):

    def name(self) -> Text:
        return "action_default_fallback"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List['Event']:
        # Fallback caused by TwoStageFallbackPolicy
        if (len(tracker.events) >= 4 and
                tracker.events[-4].get('name') ==
                # 'action_default_ask_affirmation'):
                'utter_out_of_scope'):
            dispatcher.utter_message('utter_restart_with_button')
            return []

            # return [#SlotSet('feedback_value', 'negative'),
            #       ConversationPaused()]

        # Fallback caused by Core
    # else:
    #     dispatcher.utter_template('utter_default', tracker)
    #     return [UserUtteranceReverted()]
