from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction, UserUttered, ActionExecuted
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import requests ,re, pymysql, datetime, time, threading, logging
logger = logging.getLogger(__name__)


class SupplierCategoryManagerForm(FormAction):
    def name(self):
        return 'supplier_category_manager_form'
    
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["supplier_name", "market_area"]
    
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
            
        return {
            "supplier_name": self.from_entity(entity="supplier_name"),
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
        return [FollowupAction('action_supplier_category_manager_lookup')]



class Supplier_Lookup_for_Category_Manager(Action):
    def name(self):
        return 'supplier_lookup_for_category_manager'

    def run(self, dispatcher, tracker, domain):
        suppliername = tracker.get_slot('supplier_name')
        market_area_lookup = tracker.get_slot('market_area')
        print("SUPPLIER SPEND")
        print(suppliername)
        print(market_area_lookup)
        if not suppliername:
            response = "Please enter a supplier or a category"
            #response = "I don't recognize this supplier name"
            dispatcher.utter_message(response)
            return [FollowupAction('category_lookup_for_category_manager')]
        else:
            buttons = []
            message = ''
            db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
            cursor = db.cursor()
            if market_area_lookup == "MANA" or market_area_lookup == "mana":
                sql = "SELECT DISTINCT VendorName FROM `ab_vendor_to_category_manager`WHERE VendorName LIKE '%s';" % ('%' + suppliername + '%')
            else:
                sql = "SELECT DISTINCT VendorName FROM `ab_vendor_to_category_manager_global` WHERE VendorName LIKE '%s';" % ('%' + suppliername + '%')
            print(sql)
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                if len(results) == 1:
                    for row in results:
                        # if a single supplier is found, set slot supplier_name_form and trigger spend form
                        suppliernamecmlookup = row[0]
                        message = ''
                        print(suppliernamecmlookup)
                        return SlotSet('supplier_name', suppliernamecmlookup), FollowupAction('supplier_category_manager_form')
                elif len(results) > 1:
                    for row in results:
                        # if a multiple suppliers are found, display buttons of all possible supplier matches back to user then trigger spend form
                        suppliernamecmlookup = row[0]
                        print(suppliernamecmlookup)
                        payload = "/inform{\"supplier_name\":\"" + suppliernamecmlookup + "\"}"
                        print(payload)
                        buttons.append(
                            {"title": "{}".format(suppliernamecmlookup.title()), "payload": payload})
                        message = "I found {} suppliers that also match that name, which one are you inquiring about?".format(
len(buttons))
                else:
                    response = "I couldn't find any suppliers that match that name"
                    dispatcher.utter_message(response)
                dispatcher.utter_button_message(message, buttons)
                return []
            except (AttributeError, TypeError) as e:
                response = "I couldn't find any matches for that supplier name"
                # dispatcher.utter_message(e)
                print(e)
                dispatcher.utter_message(response)
                return None


class Supplier_CategoryManagerLookup(Action):
    def name(self):
        return 'action_supplier_category_manager_lookup'
    
    def run(self, dispatcher, tracker, domain):
        suppliernamecmlookup = tracker.get_slot('supplier_name')
        if not suppliernamecmlookup:
            suppliernamecmlookup = tracker.latest_message['entities'][0]['value']
            #return FollowupAction('supplier_lookup')
        else:
            suppliernamecmlookup = tracker.get_slot('supplier_name')
        market_area_lookup = tracker.get_slot('market_area')

        if market_area_lookup == "all market areas" or market_area_lookup == "ALL Market Areas":
            if not suppliernamecmlookup:
                response = "I don't recognize this supplier name"
                dispatcher.utter_message(response)
            else:
                categorymanager = [0]
                db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
                cursor = db.cursor()
                #Search for MANA
                sql = "SELECT DISTINCT VendorName, VendorSpendCategory, MANACategoryOwner, ManagedGloballyorinMANA FROM `ab_vendor_to_category_manager` WHERE VendorName LIKE '%s' AND ManagedGloballyorinMANA LIKE 'MANA' AND CalendarYear >= YEAR(CURRENT_DATE())-5 ORDER BY MANACategoryOwner;" % (
                    '%' + suppliernamecmlookup + '%')
                try:
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    for row in results:
                        suppliernamecmlookup = row[0]
                        category = row[1]
                        categorymanager = row[2]
                        categorymarketarea = row[3]
                        response = "The Category Manager responsible for category {} with {} is {} in {}.".format(
                            "<b>"+category+"</b>", "<b>"+suppliernamecmlookup+"</b>", "<b>"+categorymanager+"</b>", "<b>"+categorymarketarea+"</b>")
                        print(response)
                        dispatcher.utter_message(response)
                except:
                    print("Error fetching data.")

                #Search all markets but MANA
                sql = "SELECT DISTINCT VendorName, VendorSpendCategory, CategoryApproverforSRT, MarketArea FROM `ab_vendor_to_category_manager_global` WHERE VendorName LIKE '%s' AND MarketArea <> 'MANA' AND CalendarYear >= YEAR(CURRENT_DATE())-5 ORDER BY MarketArea;" % (
                    '%' + suppliernamecmlookup + '%')
                print(sql)
                try:
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    for row in results:
                        suppliernamecmlookup = row[0]
                        category = row[1]
                        categorymanager = row[2]
                        categorymarketarea = row[3]
                        response = "The Category Manager responsible for category {} with {} is {} in {}.".format(
                            "<b>"+category+"</b>", "<b>"+suppliernamecmlookup+"</b>", "<b>"+categorymanager+"</b>", "<b>"+categorymarketarea+"</b>")
                        print(response)
                        dispatcher.utter_message(response)
                except:
                    print("Error fetching data.")
                finally:
                    db.close()
        else:
            market_area_lookup = market_area_lookup
            print(suppliernamecmlookup)
            if not suppliernamecmlookup:
                response = "I don't recognize this supplier name"
                dispatcher.utter_message(response)
            else:
                categorymanager = [0]
                db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
                cursor = db.cursor()
                if market_area_lookup == "MANA" or market_area_lookup == "mana":
                    sql = "SELECT DISTINCT VendorName, VendorSpendCategory, MANACategoryOwner, ManagedGloballyorinMANA FROM `ab_vendor_to_category_manager` WHERE VendorName LIKE '%s' AND ManagedGloballyorinMANA LIKE '%s' AND CalendarYear >= YEAR(CURRENT_DATE())-5 ORDER BY MANACategoryOwner;" % (
                        '%' + suppliernamecmlookup + '%', '%' + market_area_lookup + '%')
                else:
                    sql = "SELECT DISTINCT VendorName, VendorSpendCategory, CategoryApproverforSRT, MarketArea FROM `ab_vendor_to_category_manager_global` WHERE VendorName LIKE '%s' AND MarketArea LIKE '%s' AND CalendarYear >= YEAR(CURRENT_DATE())-5 ORDER BY MarketArea;" % (
                        '%' + suppliernamecmlookup + '%', '%' + market_area_lookup + '%')
                print(sql)
                try:
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    for row in results:
                        suppliernamecmlookup = row[0]
                        category = row[1]
                        categorymanager = row[2]
                        categorymarketarea = row[3]
                        response = "The Category Manager responsible for category {} with {} is {} in {}.".format(
                            "<b>"+category+"</b>", "<b>"+suppliernamecmlookup+"</b>", "<b>"+categorymanager+"</b>", "<b>"+categorymarketarea+"</b>")
                        print(response)
                        dispatcher.utter_message(response)
                except:
                    print("Error fetching data.")
                finally:
                    db.close()
            #output sentence format
            #response = """The Category Manager responsible for supplier {} is {} in {}.""".format(suppliernamecmlookup, categorymanager, market_area_lookup)
            #dispatcher.utter_message(response)
            #return [AllSlotsReset()]
            #return[SlotSet("supplier_name", None)]
