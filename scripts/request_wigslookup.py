from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction, UserUttered, ActionExecuted
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import requests ,re, pymysql, datetime, time, threading, logging
logger = logging.getLogger(__name__)


class Sourcing_WigLookup(Action):
    def name(self):
        return 'action_sourcing_wigs'
    
    def run(self, dispatcher, tracker, domain):
        db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
        cursor = db.cursor()
        sql = "SELECT answer FROM `sourcing_faqs` WHERE question LIKE 'Where are the Sourcing WIGs Stored?';"
        print(sql)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                answer = row[0]
        except:
            print("Error fetching data.")
        finally:
            db.close()
        #output sentence format
        #print(answer)
        if answer == '':
            response = """I couldn't find an answer for your question"""
        elif answer != '':
            response_answer = """{}""".format(answer)
        dispatcher.utter_message(response_answer)
