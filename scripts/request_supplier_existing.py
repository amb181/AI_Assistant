from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction, UserUttered, ActionExecuted
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import requests ,re, pymysql, datetime, time, threading, logging
logger = logging.getLogger(__name__)


class SupplierExistingForm(FormAction):
    def name(self):
        return 'supplier_existing_form'

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
        # return [FollowupAction('supplier_lookup_for_contract')]
        return [FollowupAction('action_existing_supplier_lookup')]


class Supplier_Lookup_for_Existing(Action):
    def name(self):
        return 'supplier_lookup_for_existing_supplier'

    def run(self, dispatcher, tracker, domain):
        suppliername = tracker.get_slot('supplier_name')

        if not suppliername:
            response = "I don't recognize this supplier name"
            dispatcher.utter_message(response)
        else:
            buttons = []
            message = ''
            db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
            cursor = db.cursor()
            sql = "SELECT DISTINCT Vendor FROM `ab_hana_sami_spend` WHERE Vendor LIKE '%s';" % (
                        '%' + suppliername + '%')
            print(sql)
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                if len(results) == 1:
                    for row in results:
                        # if a single supplier is found, set slot supplier_name_form and trigger spend form
                        suppliername = row[0]
                        message = ''
                        print(suppliername)
                        return SlotSet('supplier_name', suppliername), FollowupAction('supplier_existing_form')
                elif len(results) > 1:
                    for row in results:
                        # if a multiple suppliers are found, display buttons of all possible supplier matches back to user then trigger spend form
                        suppliername = row[0]
                        print(suppliername)
                        payload = "/inform{\"supplier_name\":\"" + suppliername + "\"}"
                        print(payload)
                        buttons.append(
                            {"title": "{}".format(suppliername.title()), "payload": payload})
                        message = "I found {} suppliers that also match that name, which one are you inquiring about?".format(len(buttons))
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


class Supplier_Lookup_Existing(Action):
    def name(self):
        return 'action_existing_supplier_lookup'

    def run(self, dispatcher, tracker, domain):
        suppliernameexisting = tracker.get_slot('supplier_name')
        if not suppliernameexisting:
            suppliernameexisting = tracker.latest_message['entities'][0]['value']
        else:
            suppliernameexisting = tracker.get_slot('supplier_name')
        market_area_lookup = tracker.get_slot('market_area')
        market_area_lookup = market_area_lookup.upper()
        if not market_area_lookup:
            response = "I didn't catch the market area"
            dispatcher.utter_message(response)
        else:
            market_area_lookup = market_area_lookup
        if market_area_lookup == "ALL MARKET AREAS":
            market_area_lookup = ""
        else:
            market_area_lookup = market_area_lookup
        print(suppliernameexisting)
        if not suppliernameexisting:
            response = "I don't recognize this supplier name"
            dispatcher.utter_message(response)
        else:
            musid = 0
            db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
            cursor = db.cursor()
            sql = "SELECT Vendor, MUS_ID, MarketArea FROM `ab_hana_sami_spend` WHERE Vendor = '%s' AND MarketArea LIKE '%s' ORDER BY InvoiceClearingDate DESC LIMIT 1;" % (
                        suppliernameexisting, '%' + market_area_lookup + '%')
            print(sql)
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                for row in results:
                    suppliernameexisting = row[0]
                    musid = row[1]
                    market = row[2]
            except:
                print("Error fetching data.")
            finally:
                db.close()
            print(musid)
            if not musid:
                response = """I could not find {} as an Ericsson Supplier in {}.""".format(
                    suppliernameexisting, market_area_lookup)
            else:
                response = "Yes, the supplier {} was found as an Ericsson Supplier, with MusID {} in {}.".format(
                    "<b>"+suppliernameexisting+"</b>", "<b>"+musid+"</b>", "<b>"+market+"</b>")
            dispatcher.utter_message(response)
