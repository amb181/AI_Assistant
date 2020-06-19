from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction, UserUttered, ActionExecuted
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import requests ,re, pymysql, datetime, time, threading, logging
logger = logging.getLogger(__name__)


class CategoryCategoryManagerForm(FormAction):
    def name(self):
        return 'category_category_manager_form'

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["category_name", "market_area"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "category_name": self.from_entity(entity="category_name"),
            "market_area": self.from_entity(entity="market_area"),
        }

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form should do after all required slots are filled"""
        # run action supplier category manager lookup
        # dispatcher.utter_message(template="utter_submit")
        return [FollowupAction('action_category_category_manager_lookup')]


class Category_Lookup_for_Category_Manager(Action):
    def name(self):
        return 'category_lookup_for_category_manager'

    def run(self, dispatcher, tracker, domain):
        categoryname = tracker.get_slot('category_name')
        market_area_lookup = tracker.get_slot('market_area')
        print(categoryname)
        if not categoryname:
            response = "Please enter a supplier or a category"
            #response = "I don't recognize this supplier name"
            dispatcher.utter_message(response)
            return [FollowupAction('supplier_lookup_for_category_manager')]
        else:  
            buttons = []
            message = ''
            db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
            cursor = db.cursor()
            if market_area_lookup == "MANA" or market_area_lookup == "mana":
                sql = "SELECT DISTINCT VendorSpendCategory FROM `ab_vendor_to_category_manager` WHERE VendorSpendCategory LIKE '%s';" % ('%' + categoryname + '%')
            else:
                sql = "SELECT DISTINCT VendorSpendCategory FROM `ab_vendor_to_category_manager_global` WHERE VendorSpendCategory LIKE '%s';" % ('%' + categoryname + '%')
            print(sql)
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                if len(results) == 1:
                    for row in results:
                        # if a single category is found, set slot category_name_form and trigger spend form
                        categorynamecmlookup = row[0]
                        message = ''
                        print(categorynamecmlookup)
                        return SlotSet('category_name', categorynamecmlookup), FollowupAction('category_category_manager_form')
                elif len(results) > 1 and len(results) < 15:
                    for row in results:
                        # if a multiple categories are found, display buttons of all possible category matches back to user then trigger spend form
                        categorynamecmlookup = row[0]
                        print(categorynamecmlookup)
                        payload = "/inform{\"category_name\":\"" + categorynamecmlookup + "\"}"
                        print(payload)
                        buttons.append({"title": "{}".format(categorynamecmlookup.title()), "payload": payload})
                        message = "I found {} categories that also match that name, which one are you inquiring about?".format(len(buttons))
                elif len(results) > 14:
                    response = "There are too many categories that match that name, please be more specific"
                    dispatcher.utter_message(response)  
                else:
                    response = "I couldn't find any categories that match that name"
                    dispatcher.utter_message(response)
                dispatcher.utter_button_message(message, buttons)
                return []
            except (AttributeError, TypeError) as e:
                response = "I couldn't find any matches for that category name"
                # dispatcher.utter_message(e)
                print(e)
                dispatcher.utter_message(response)
                return None

class Category_CategoryManagerLookup(Action):
    def name(self):
        return 'action_category_category_manager_lookup'

    def run(self, dispatcher, tracker, domain):
        categorynamecmlookup = tracker.get_slot('category_name')
        if not categorynamecmlookup:
            categorynamecmlookup = tracker.latest_message['entities'][0]['value']
        else:
            categorynamecmlookup = tracker.get_slot('category_name')
        market_area_lookup = tracker.get_slot('market_area')

        if market_area_lookup == "all market areas" or market_area_lookup == "ALL Market Areas":
            if not categorynamecmlookup:
                response = "I don't recognize this category name"
                dispatcher.utter_message(response)
            else:
                categorymanager = [0]
                categorymarketarea = [0]
                db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
                cursor = db.cursor()
                #Search for MANA
                sql = "SELECT DISTINCT VendorSpendCategory, MANACategoryOwner, ManagedGloballyorinMANA FROM `ab_vendor_to_category_manager` WHERE VendorSpendCategory = '%s' AND ManagedGloballyorinMANA LIKE 'MANA' AND CalendarYear >= YEAR(CURRENT_DATE())-5;" % (
                    categorynamecmlookup)
                try:
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    for row in results:
                        categorynamecmlookup = row[0]
                        categorymanager = row[1]
                        categorymarketarea = row[2]
                        response = """The Category Manager responsible for {} is {} in {}.""".format(
                            "<b>"+categorynamecmlookup+"</b>", "<b>"+categorymanager+"</b>", "<b>"+categorymarketarea+"</b>")
                        dispatcher.utter_message(response)
                except:
                    print("Error fetching data.")

                #Search for all markets but MANA
                sql = "SELECT DISTINCT VendorSpendCategory, CategoryApproverforSRT, MarketArea FROM `ab_vendor_to_category_manager_global` WHERE VendorSpendCategory = '%s' AND MarketArea <> 'MANA' AND CalendarYear >= YEAR(CURRENT_DATE())-5;" % (
                    categorynamecmlookup)
                print(sql)
                try:
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    for row in results:
                        categorynamecmlookup = row[0]
                        categorymanager = row[1]
                        categorymarketarea = row[2]
                        response = """The Category Manager responsible for {} is {} in {}.""".format(
                            "<b>"+categorynamecmlookup+"</b>", "<b>"+categorymanager+"</b>", "<b>"+categorymarketarea+"</b>")
                        dispatcher.utter_message(response)
                except:
                    print("Error fetching data.")
                finally:
                    db.close()
        else:
            market_area_lookup = market_area_lookup
            print(categorynamecmlookup)
            if not categorynamecmlookup:
                response = "I don't recognize this category name"
                dispatcher.utter_message(response)
            else:
                categorymanager = [0]
                categorymarketarea = [0]
                db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
                cursor = db.cursor()
                if market_area_lookup == "MANA" or market_area_lookup == "mana":
                    sql = "SELECT DISTINCT VendorSpendCategory, MANACategoryOwner, ManagedGloballyorinMANA FROM `ab_vendor_to_category_manager` WHERE VendorSpendCategory = '%s' AND ManagedGloballyorinMANA LIKE '%s' AND CalendarYear >= YEAR(CURRENT_DATE())-5;" % ( categorynamecmlookup, '%' + market_area_lookup + '%')
                else:
                    sql = "SELECT DISTINCT VendorSpendCategory, CategoryApproverforSRT, MarketArea FROM `ab_vendor_to_category_manager_global` WHERE VendorSpendCategory = '%s' AND MarketArea LIKE '%s' AND CalendarYear >= YEAR(CURRENT_DATE())-5;" % ( categorynamecmlookup, '%' + market_area_lookup + '%')
                print(sql)
                try:
                    cursor.execute(sql)
                    if cursor.rowcount == 0:
                        response = """I couldn't find a Category Manager for {} in {}.""".format(
                            "<b>"+categorynamecmlookup+"</b>", "<b>"+market_area_lookup+"</b>")
                    else:
                        results = cursor.fetchall()
                        for row in results:
                            categorynamecmlookup = row[0]
                            categorymanager = row[1]
                            categorymarketarea = row[2]
                        response = """The Category Manager responsible for {} is {} in {}.""".format(
                            "<b>"+categorynamecmlookup+"</b>", "<b>"+categorymanager+"</b>", "<b>"+categorymarketarea+"</b>")
                    dispatcher.utter_message(response)
                except:
                    print("Error fetching data.")
                finally:
                    db.close()
