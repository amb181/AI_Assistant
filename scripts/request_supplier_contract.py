from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction, UserUttered, ActionExecuted
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import requests ,re, pymysql, datetime, time, threading, logging
logger = logging.getLogger(__name__)


class SupplierContractForm(FormAction):
    def name(self):
        return 'supplier_contract_form'

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
        return [FollowupAction('action_supplier_contract_lookup')]


class Supplier_Lookup_For_Contract(Action):
    def name(self):
        return 'supplier_lookup_for_contract'

    def run(self, dispatcher, tracker, domain):
        suppliername = tracker.get_slot('supplier_name')
        market_area_lookup = tracker.get_slot('market_area')
        print(market_area_lookup)
        if not suppliername:
            response = "I don't recognize this supplier name"
            dispatcher.utter_message(response)
        else:
            buttons = []
            message = ''
            db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
            cursor = db.cursor()
            sql = "SELECT DISTINCT SupplierName FROM `global_clm_list` WHERE SupplierName LIKE '%s';" % (
                    '%' + suppliername + '%')
            print(sql)
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                if len(results) == 1:
                    for row in results:
                        # if a single supplier is found, set slot supplier_name_form and trigger spend form
                        suppliernamecontractlookup = row[0]
                        message = ''
                        print(suppliernamecontractlookup)
                        return SlotSet('supplier_name', suppliernamecontractlookup), SlotSet('category_name', None),FollowupAction(
                            'supplier_contract_form')
                elif len(results) > 1 and len(results) < 15:
                    for row in results:
                        # if multiple suppliers are found, display buttons of all possible supplier matches back to user then trigger spend form
                        suppliernamecontractlookup = row[0]
                        print(suppliernamecontractlookup)
                        payload = "/inform{\"supplier_name\":\"" + suppliernamecontractlookup + "\"}"
                        print(payload)
                        buttons.append({"title": "{}".format(suppliernamecontractlookup.title()), "payload": payload})
                        message = "I found {} suppliers that also match that name, which one are you inquiring about?".format(len(buttons))
                elif len(results) > 14:
                    response = "There are too many suppliers that match that name, please be more specific"
                    dispatcher.utter_message(response)
                else:
                    response = "I couldn't find any contract with {} in {}".format("<b>"+suppliername+"</b>", "<b>"+market_area_lookup+"</b>")
                    dispatcher.utter_message(response)
                dispatcher.utter_button_message(message, buttons)
                return []
            except (AttributeError, TypeError) as e:
                response = "I couldn't find any matches for that supplier name"
                print(e)
                dispatcher.utter_message(response)
                return None


class Supplier_ContractLookup(Action):
    def name(self):
        return 'action_supplier_contract_lookup'

    def run(self, dispatcher, tracker, domain):
        suppliernamecontractlookup = tracker.get_slot('supplier_name')
        if not suppliernamecontractlookup:
            suppliernamecontractlookup = tracker.latest_message['entities'][0]['value']
        else:
            suppliernamecontractlookup = tracker.get_slot('supplier_name')
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
        print(suppliernamecontractlookup)
        if not suppliernamecontractlookup:
            response = "I don't recognize this supplier name"
            dispatcher.utter_message(response)
        else:
            contractid = 0
            contractname = 0
            effectivedate = 0
            db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
            cursor = db.cursor()
            sql = "SELECT SupplierName, MasterAgreementID, MasterAgreementName, EffectiveDate, MarketArea FROM `global_clm_list` WHERE SupplierName = '%s' AND MarketArea LIKE '%s' AND Status = 'Valid' ORDER BY EffectiveDate;" % (
                suppliernamecontractlookup, '%' + market_area_lookup + '%')
            print(sql)
            try:
                cursor.execute(sql)
                if cursor.rowcount == 0:
                    response = """I couldn't find an agreement for supplier {} in {}.""".format(
                        "<b>"+suppliernamecontractlookup+"</b>", "<b>"+market_area_lookup+"</b>")
                else:    
                    results = cursor.fetchall()
                    for row in results:
                        suppliernamecontractlookup = row[0]
                        contractid = row[1]
                        contractname = row[2]
                        effectivedate = row[3]
                        marketarea = row[4]
                    effectivedate = str(effectivedate)
                    response = "I found an agreement with the name {} for supplier {} that has been in effect since {} in {}.".format(
                        "<b>"+contractname+"</b>", "<b>"+suppliernamecontractlookup+"</b>", "<b>"+effectivedate+"</b>", "<b>"+marketarea+"</b>")
                dispatcher.utter_message(response)
                return [SlotSet('category_name', None)]
                # return[SlotSet("supplier_name", None)]
            except:
                print("Error fetching data.")
            finally:
                db.close()
