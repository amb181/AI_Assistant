from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction, UserUttered, ActionExecuted
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import requests ,re, pymysql, datetime, time, threading, logging
logger = logging.getLogger(__name__)


class Supplier_OnboardingStatus(Action):
    def name(self):
        return 'action_supplier_onboarding_status'
    
    def run(self, dispatcher, tracker, domain):
        suppliernameoblookup = tracker.get_slot('supplier_name')
        #singlesuppliernamecmlookup = tracker.get_slot('supplier_spend_cm_lookup_name')
        print(suppliernameoblookup)
        #categorymanager = [0]
        #if singlesuppliernamecmlookup != '':
        #    #print("Lookup CM here")
        #    suppliernamecmlookup = singlesuppliernamecmlookup
        #else:
        #    suppliernamecmlookup = suppliernamecmlookup
        #db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
        #cursor = db.cursor()
        #sql = "SELECT VendorName, MANACategoryOwner FROM `supplier_cm_mapping` WHERE VendorName LIKE '%s';" % ('%' + suppliernamecmlookup + '%')
        #sql = "SELECT VendorName, MANACategoryOwner FROM 'supplier_cm_mapping' WHERE VendorName LIKE %s"
        #print(sql)
        #try:
            #suppliernamecmlookup = tracker.get_slot('supplier_name')
            #cursor.execute(sql, (suppliernamecmlookup))
            #cursor.execute(sql)
            #results = cursor.fetchall()
            #for row in results:
            #    suppliernamecmlookup = row[0]
            #    categorymanager = row[1]
        #except:
            #print("Error fetching data.")
        #finally:
            #db.close()
        #output sentence format
        #response = """The Category Manager responsible for supplier {} is {}.""".format(suppliernamecmlookup, categorymanager)
        #dispatcher.utter_message(response)
        #return [AllSlotsReset()]
        #return[SlotSet("supplier_name", None)]




