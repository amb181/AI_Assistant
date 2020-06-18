from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction, UserUttered, ActionExecuted
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import requests ,re, pymysql, datetime, time, threading, logging
logger = logging.getLogger(__name__)


class Supplier_DowJonesCheck(Action):
    def name(self):
        return 'action_supplier_dowjones_check'
    
    def run(self, dispatcher, tracker, domain):
        suppliernamedjcheck = tracker.get_slot('supplier_name')
        print(suppliernamedjcheck)
        alert = 0
        alertdate = 0
        suppliername = 0
        db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
        cursor = db.cursor()
        sql = "SELECT supplier_name, description_of_alert, alert_date, summary_of_article FROM `dow_jones_alerts` WHERE supplier_name = '%s';" % ('%' + suppliernamedjcheck + '%')
        print(sql)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                suppliername = row[0]            
                alert = row[1]
                alertdate = row[2]
                alertsummary = row[3]  
        except:
            print("Error fetching data.")
        finally:
            db.close()
        #output sentence format
        print(alert)
        if alert == 0:
            return []
        elif alert != '':
            response = """Also, I found a potential flag for supplier {}. I found this alert '{}' that was reported on {}.""".format("<b>"+suppliername+"</b>", "<b>"+alert+"</b>", "<b>"+alertdate+"</b>")
        #time.sleep(1)
        dispatcher.utter_message(response)
        
        
class Supplier_DowJonesCheck_Details(Action):
    def name(self):
        return 'action_supplier_dowjones_check_details'
    
    def run(self, dispatcher, tracker, domain):
        suppliernamedjcheck = tracker.get_slot('supplier_name')
        print(suppliernamedjcheck)        
        db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
        cursor = db.cursor()
        sql = "SELECT supplier_name, summary_of_article FROM `dow_jones_alerts` WHERE supplier_name LIKE '%s';" % ('%' + suppliernamedjcheck + '%')
        print(sql)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                suppliername = row[0]            
                alertsummary = row[1]  
        except:
            print("Error fetching data.")
        finally:
            db.close()
        #output sentence format
        if alertsummary == '':
            return []
        elif alertsummary != '':
            response = """Sure, here are the details for supplier {}. \n\n{}""".format("<b>"+suppliername+"</b>", "<b>"+alertsummary+"</b>")
        dispatcher.utter_message(response)
