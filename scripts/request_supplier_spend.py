from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction, UserUttered, ActionExecuted
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import requests ,re, pymysql, datetime, time, threading, logging
logger = logging.getLogger(__name__)


class SupplierSpendForm(FormAction):
    def name(self):
        return 'supplier_spend_form'
    
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["supplier_name", "market_area", "date", "month"]
    
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
            
        return {
            "supplier_name": self.from_entity(entity="supplier_name"),
            "market_area": self.from_entity(entity="market_area"),
            "date": self.from_entity(entity="date"),
            "month": self.from_entity(entity="month"),
        }
    
    @staticmethod
    def market_area_db() -> List[Text]:
        """Database of supported Market Areas"""    
        return [
            "MANA",
            "MELA",
            "ALL",
        ]

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form should do after all required slots are filled"""
        # run action supplier spend lookup
        # dispatcher.utter_message(template="utter_submit")
        # Need to add Stories that ask for supplier spend graph
        return [FollowupAction('action_supplier_spend_lookup')]
    
            


class Supplier_Lookup(Action):
    def name(self):
        return 'supplier_lookup'
    
    def run(self, dispatcher, tracker, domain):
        suppliername = tracker.get_slot('supplier_name')
        print(suppliername)
        if not suppliername:
            response = "I don't recognize this supplier name"
            dispatcher.utter_message(response)
        else:
            buttons = []
            message = ''
            db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
            cursor = db.cursor()
            sql = "SELECT DISTINCT Vendor FROM `ab_hana_sami_spend` WHERE Vendor LIKE '%s';" % ('%' + suppliername + '%')
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
                        return SlotSet('supplier_name', suppliername),FollowupAction('supplier_spend_form')
                elif len(results) > 1 and len(results) < 15:
                    for row in results:
                        # if multiple suppliers are found, display buttons of all possible supplier matches back to user then trigger spend form
                        suppliername = row[0]
                        print(suppliername)
                        payload = "/inform{\"supplier_name\":\"" + suppliername + "\"}"
                        print(payload)
                        buttons.append(
                            {"title": "{}".format(suppliername.title()), "payload": payload})
                        message = "I found {} suppliers that also match that name, which one are you inquiring about?".format(len(buttons))
                elif len(results) > 14:
                    response = "There are too many suppliers that match that name, please be more specific"
                    dispatcher.utter_message(response)                
                else:
                    response = "I couldn't find any suppliers that match that name"
                    dispatcher.utter_message(response)
                dispatcher.utter_button_message(message, buttons)
                return []
            except (AttributeError, TypeError) as e:
                response = "I couldn't find any matches for that supplier name"
                #dispatcher.utter_message(e)
                dispatcher.utter_message(response)
                return None


class Supplier_SpendLookup(Action):
    def name(self):
        return 'action_supplier_spend_lookup'

    def run(self, dispatcher, tracker, domain):
        import math
        monthNumber = {
            "january": "01",
            "february": "02",
            "march": "03",
            "april": "04",
            "may": "05",
            "june": "06",
            "july": "07",
            "august": "08",
            "september": "09",
            "october": "10",
            "november": "11",
            "december": "12"
        }
        suppliernamesplookup = tracker.get_slot('supplier_name')
        market_area_lookup = tracker.get_slot('market_area')
        market_area_lookup_name = 0
        if market_area_lookup == "all market areas" or market_area_lookup == "ALL Market Areas":
            market_area_lookup = ""
            market_area_lookup_name = "All Market Areas"
        else:
            market_area_lookup = market_area_lookup
            market_area_lookup_name = market_area_lookup.upper()
        date_lookup = tracker.get_slot('date')
        date_lookup_name = 0
        now = datetime.datetime.now()
        last_year = now.year -1
        if date_lookup.lower() == "this year":
            date_lookup_start = str(now.year)
            date_lookup_end = str(now.year)
            date_lookup_name = str(now.year)
        elif date_lookup.lower() == "last year":
            date_lookup_start = str(last_year)
            date_lookup_end = str(last_year)
            date_lookup_name = str(last_year)
        elif date_lookup.lower() == "all years":
            date_lookup_start = "1900"
            date_lookup_end = str(now.year)
            date_lookup_name = "All Years"
        elif int(date_lookup) > now.year:
            response = "We cannot lookup for data in the future... yet, it's only possible to provide data up to " + str(now.month) + " " + str(now.year)
            dispatcher.utter_message(response)
            return None
        else:
            date_lookup_start = str(date_lookup)
            date_lookup_end = str(date_lookup)
            date_lookup_name = str(date_lookup)
        #Check about month/querter info
        month_quarter = tracker.get_slot('month')
        if not month_quarter or str(month_quarter).lower() == "none" or date_lookup_name == "All Years":
            month_start = "01"
            month_end = "12"
        else:
            if str(date_lookup_name) == "":
                date_lookup_name = str(month_quarter).capitalize()
            else:
                date_lookup_name = str(month_quarter).capitalize() + '</b> in <b>' + date_lookup_name
            if "q" in str(month_quarter).lower():
                quarter = math.ceil((now.month) / 3)
                if "1" in str(month_quarter):
                    month_start = "01"
                    month_end = "03"
                    quarter_requested = 1
                elif "2" in str(month_quarter):
                    month_start = "04"
                    month_end = "06"
                    quarter_requested = 2
                elif "3" in str(month_quarter):
                    month_start = "07"
                    month_end = "09"
                    quarter_requested = 3
                elif "4" in str(month_quarter):
                    month_start = "10"
                    month_end = "12"
                    quarter_requested = 4
                elif "last" in str(month_quarter):
                    quarter_requested = quarter - 1
                    print(quarter_requested)
                    if (quarter_requested) == 0:
                        date_lookup_start = str(last_year)
                        date_lookup_end = str(last_year)
                        month_start = "10"
                        month_end = "12"
                    else: 
                        month_start = str(((quarter_requested - 1) * 3) + 1)
                        month_end = str(quarter_requested * 3)
                elif "this" in str(month_quarter):
                    print(quarter)
                    month_start = str(((quarter - 1) * 3) + 1)
                    month_end = str(quarter * 3)
                    quarter_requested = quarter
                if quarter_requested > quarter and int(date_lookup_start) == now.year:
                    response = "We cannot lookup for data in the future... yet, it's only possible to provide data up to Q" + str(quarter) + " " + str(now.year)
                    dispatcher.utter_message(response)
                    return None 
            else:
                month_start = monthNumber[str(month_quarter).lower()]
                month_end = month_start
                if int(month_start) > now.month and int(date_lookup_start) == now.year:
                    response = "We cannot lookup for data in the future... yet, it's only possible to provide data up to " + str(now.month) + " " + str(now.year)
                    dispatcher.utter_message(response)
                    return None
                if month_start == "Invalid month":
                    month_start = "01"
                    month_end = "12"
                elif "last" in str(month_quarter).lower():
                    month_start = now.month - 1
                    month_end = now.month - 1
                elif "this" in str(month_quarter).lower():
                    month_start = now.month
                    month_end = now.month
        date_lookup_start = date_lookup_start + "-" + month_start + "-01"
        date_lookup_end = date_lookup_end + "-" + month_end + "-31"
        print(suppliernamesplookup)
        spend = 0
        musid = 0
        db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
        cursor = db.cursor()
        cursor2 = db.cursor()
        sql = "SELECT SUM(USD) AS Spend, Vendor FROM `ab_hana_sami_spend` WHERE Vendor = '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') AND MarketArea LIKE '%s' GROUP BY Vendor;" % (suppliernamesplookup, date_lookup_start, date_lookup_end, '%' + market_area_lookup + '%')
        sql2 = "SELECT DISTINCT Company, SUM(USD) AS Spend FROM `ab_hana_sami_spend` WHERE Vendor = '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') AND MarketArea LIKE '%s' GROUP BY Company;" % (suppliernamesplookup, date_lookup_start, date_lookup_end, '%' + market_area_lookup + '%')
        print(sql)
        print(sql2)
        try:
            cursor.execute(sql)
            cursor2.execute(sql2)
            results = cursor.fetchall()
            results2 = list(cursor2)
            for row in results:
                spend = row[0]
                suppliernamesplookup = row[1]
        except:
            print(results2)            
            print("Error fetching data.")
        finally:
            db.close()
        #output sentence format
        print(spend)
        if spend == 0:
            response = """I couldn't find any spend for supplier {} for {} in {}.""".format("<b>"+suppliernamesplookup+"</b>", "<b>"+date_lookup_name+"</b>", "<b>"+market_area_lookup_name+"</b>")
        elif spend > 0:
            spend = "${:,.2f}".format(spend)
            spend = str(spend)
            #response = """The spend for supplier {} is ${:,.2f} for {}. This is based on MUSID {}.""".format(suppliernamesplookup, spend, date_lookup, musid)
            response = """The spend for supplier {} is {} for {} in {}.""".format("<b>"+suppliernamesplookup+"</b>", "<b>"+spend+"</b>", "<b>"+date_lookup_name+"</b>", "<b>"+market_area_lookup_name+"</b>")
        Supplier_SpendLookup.run.thisValue = results2
        dispatcher.utter_message(response), FollowupAction('action_supplier_dowjones_check')
        #return [AllSlotsReset()]
        #return[SlotSet("supplier_name", None)]


class Supplier_SpendGraph(Action):
    def name(self):
        return 'action_supplier_spend_graph'
    
    def run(self, dispatcher, tracker, domain, **kwargs):
        import requests
        import simplejson
        import numpy as np
        from decimal import Decimal
        
        malen = np.array(Supplier_SpendLookup.run.thisValue)
        Lflag = tracker.latest_message["text"]
    
        #extract with numpy the columms from the matrix 
        coulum1 = malen[:,0]
        coulum2 = malen[:,1]
        #convert the individual strings into list
        col1 = coulum1.tolist()
        col2 = coulum2.tolist()
        #prepare to convert into  json readable strings
        result1 = simplejson.dumps(col1)
        result2 = simplejson.dumps(col2)
        #Convert file into Json readeable string        
        rescol1 = simplejson.loads(result1)
        rescol2 = simplejson.loads(result2)
        print (result1)
        print (result2)
        print (Lflag)
    
        data = {
            "title": ['Supplier spend'],
            # These labels appear in the legend and in the tooltips when hovering different arcs
            "labels": rescol1,
            "backgroundColor": [
                '#36a2eb',
                '#ffcd56',
                '#ff6384',
                '#009688',
                '#c45850',
                '#F0F8FF',
                '#FAEBD7',
                '#7FFFD4',
                '#8A2BE2',
                '#D2691E',
                '#36a2eb',
                '#ffcd56'
            ],
            "chartsData": rescol2,
            "chartType": Lflag,
            "displayLegend": ['true']
        }
        dispatcher.utter_custom_json({"payload": "chart", "data": data})
        return []


class Supplier_SpendGraph_ByMonth(Action):
    def name(self):
        return 'action_supplier_spend_graph_by_month'
    
    def run(self, dispatcher, tracker, domain, **kwargs):
        import requests
        import simplejson
        import numpy as np
        from decimal import Decimal
        import math
        monthNumber = {
            "january": "01",
            "february": "02",
            "march": "03",
            "april": "04",
            "may": "05",
            "june": "06",
            "july": "07",
            "august": "08",
            "september": "09",
            "october": "10",
            "november": "11",
            "december": "12"
        }
        monthNames = np.array(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
        monthlySpend = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        suppliernamesplookup = tracker.get_slot('supplier_name')
        market_area_lookup = tracker.get_slot('market_area')
        if market_area_lookup == "all market areas" or market_area_lookup == "ALL Market Areas":
            market_area_lookup = ""
        else:
            market_area_lookup = market_area_lookup
        date_lookup = tracker.get_slot('date')
        now = datetime.datetime.now()
        last_year = now.year -1
        if date_lookup.lower() == "this year":
            date_lookup_start = str(now.year)
            date_lookup_end = str(now.year)
            date_lookup_name = str(now.year)
        elif date_lookup.lower() == "last year":
            date_lookup_start = str(last_year)
            date_lookup_end = str(last_year)
            date_lookup_name = str(last_year)
        elif date_lookup.lower() == "all years":
            date_lookup_start = "1900"
            date_lookup_end = str(now.year)
            date_lookup_name = "All Years"
        elif int(date_lookup) > now.year:
            response = "We cannot lookup for data in the future... yet, it's only possible to provide data up to " + str(now.month) + " " + str(now.year)
            dispatcher.utter_message(response)
            return None
        else:
            date_lookup_start = str(date_lookup)
            date_lookup_end = str(date_lookup)
            date_lookup_name = str(date_lookup)
        #Check about month/querter info
        month_quarter = tracker.get_slot('month')
        if not month_quarter or str(month_quarter).lower() == "none" or date_lookup_name == "All Years":
            month_start = "01"
            month_end = "12"
        else:
            if str(date_lookup_name) == "":
                date_lookup_name = str(month_quarter).capitalize()
            else:
                date_lookup_name = str(month_quarter).capitalize() + '</b> in <b>' + date_lookup_name
            if "q" in str(month_quarter).lower():
                quarter = math.ceil((now.month) / 3)
                if "1" in str(month_quarter):
                    month_start = "01"
                    month_end = "03"
                    quarter_requested = 1
                elif "2" in str(month_quarter):
                    month_start = "04"
                    month_end = "06"
                    quarter_requested = 2
                elif "3" in str(month_quarter):
                    month_start = "07"
                    month_end = "09"
                    quarter_requested = 3
                elif "4" in str(month_quarter):
                    month_start = "10"
                    month_end = "12"
                    quarter_requested = 4
                elif "last" in str(month_quarter):
                    quarter_requested = quarter - 1
                    print(quarter_requested)
                    if (quarter_requested) == 0:
                        date_lookup_start = str(last_year)
                        date_lookup_end = str(last_year)
                        month_start = "10"
                        month_end = "12"
                    else: 
                        month_start = str(((quarter_requested - 1) * 3) + 1)
                        month_end = str(quarter_requested * 3)
                elif "this" in str(month_quarter):
                    print(quarter)
                    month_start = str(((quarter - 1) * 3) + 1)
                    month_end = str(quarter * 3)
                    quarter_requested = quarter
                if quarter_requested > quarter and int(date_lookup_start) == now.year:
                    response = "We cannot lookup for data in the future... yet, it's only possible to provide data up to Q" + str(quarter) + " " + str(now.year)
                    dispatcher.utter_message(response)
                    return None 
            else:
                month_start = monthNumber[str(month_quarter).lower()]
                month_end = month_start
                if int(month_start) > now.month and int(date_lookup_start) == now.year:
                    response = "We cannot lookup for data in the future... yet, it's only possible to provide data up to " + str(now.month) + " " + str(now.year)
                    dispatcher.utter_message(response)
                    return None
                if month_start == "Invalid month":
                    month_start = "01"
                    month_end = "12"
                elif "last" in str(month_quarter).lower():
                    month_start = now.month - 1
                    month_end = now.month - 1
                elif "this" in str(month_quarter).lower():
                    month_start = now.month
                    month_end = now.month
        date_lookup_start = date_lookup_start + "-" + month_start + "-01"
        date_lookup_end = date_lookup_end + "-" + month_end + "-31"
        print(suppliernamesplookup)
        spend = 0
        musid = 0
        db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
        cursor = db.cursor()
        sql = "SELECT MONTH(InvoiceClearingDate) as Month, Round( SUM(USD),2) AS Spend FROM `ab_hana_sami_spend` WHERE Vendor LIKE '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') AND MarketArea LIKE '%s' GROUP BY MONTH;" % (suppliernamesplookup, date_lookup_start, date_lookup_end, '%' + market_area_lookup + '%')
        #sql = "SELECT DISTINCT MONTH(InvoiceClearingDate) as Month, SUM(USD) AS Spend FROM `ab_hana_sami_spend` WHERE Vendor = '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') AND MarketArea LIKE '%s' GROUP BY MONTH(InvoiceClearingDate);" % (suppliernamesplookup, date_lookup_start, date_lookup_end, '%' + market_area_lookup + '%')
        print(sql)
        try:
            cursor.execute(sql)
            results = list(cursor)
            Supplier_SpendLookup.run.thisValue = results
        except:
            print("Error fetching data.")
        finally:
            db.close()
        
        malen = np.array(Supplier_SpendLookup.run.thisValue)
    
        #extract with numpy the columms from the matrix
        #if str(now.year) == date_lookup:
        #    monthNames = monthNames[:now.month]
        #    monthlySpend = monthlySpend[:now.month]
        if malen.size != 0:
            Lflag = "bar"
            coulum1 = malen[:,0]
            coulum2 = malen[:,1]
            for x in coulum1:
                pos = np.where(coulum1 == x)
                monthlySpend[int(x) - 1] = coulum2[pos]
            
            monthNames = monthNames[int(month_start) - 1:int(month_end)]
            monthlySpend = monthlySpend[int(month_start) - 1:int(month_end)]
            #convert the individual strings into list
								
            col1 = monthNames.tolist()
            col2 = monthlySpend.tolist()
						
						
            #prepare to convert into  json readable strings
            result1 = simplejson.dumps(col1)
            result2 = simplejson.dumps(col2)
						   
						   
            #Convert file into Json readeable string        
            rescol1 = simplejson.loads(result1)
            rescol2 = simplejson.loads(result2)    
            data = {
                "title": ['Supplier Spend by Month'],
                # These labels appear in the legend and in the tooltips when hovering different arcs
                "labels": rescol1,
                "backgroundColor": [
                    '#36a2eb',
                    '#ffcd56',
                    '#ff6384',
                    '#009688',
                    '#c45850',
                    '#345385',
                    '#FAEBD7',
                    '#7FFFD4',
                    '#8A2BE2',
                    '#D2691E',
                    '#36a2eb',
                    '#ffcd56'
                ],
                "chartsData": rescol2,
                "chartType": Lflag,
                "displayLegend": ['true']
            }
            dispatcher.utter_message(json_message={"payload": "chart", "data": data})
            ##dispatcher.utter_custom_json({"payload": "chart", "data": data})
            return []
        else:
            response = "No data available with supplier <b>" + suppliernamesplookup + "</b> in market area <b>" + market_area_lookup + "</b> to show graph by month during <b>" + date_lookup_name +"</b>"
            dispatcher.utter_message(response)
            return None


class Supplier_SpendGraph_ByQuarter(Action):
    def name(self):
        return 'action_supplier_spend_graph_by_quarter'
    
    def run(self, dispatcher, tracker, domain, **kwargs):
        import requests
        import simplejson
        import numpy as np
        from decimal import Decimal
        import math
        monthNumber = {
            "january": "01",
            "february": "02",
            "march": "03",
            "april": "04",
            "may": "05",
            "june": "06",
            "july": "07",
            "august": "08",
            "september": "09",
            "october": "10",
            "november": "11",
            "december": "12"
        }
        monthlySpend = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        quarterName = np.array(['Q1', 'Q2', 'Q3', 'Q4'])
        quarterSpend = np.array([0, 0, 0, 0])
        suppliernamesplookup = tracker.get_slot('supplier_name')
        market_area_lookup = tracker.get_slot('market_area')
        if market_area_lookup == "all market areas" or market_area_lookup == "ALL Market Areas":
            market_area_lookup = ""
        else:
            market_area_lookup = market_area_lookup
        date_lookup = tracker.get_slot('date')
        now = datetime.datetime.now()
        last_year = now.year -1
        if date_lookup.lower() == "this year":
            date_lookup_start = str(now.year)
            date_lookup_end = str(now.year)
            date_lookup_name = str(now.year)
        elif date_lookup.lower() == "last year":
            date_lookup_start = str(last_year)
            date_lookup_end = str(last_year)
            date_lookup_name = str(last_year)
        elif date_lookup.lower() == "all years":
            date_lookup_start = "1900"
            date_lookup_end = str(now.year)
            date_lookup_name = "All Years"
        elif int(date_lookup) > now.year:
            response = "We cannot lookup for data in the future... yet, it's only possible to provide data up to " + str(now.month) + " " + str(now.year)
            dispatcher.utter_message(response)
            return None
        else:
            date_lookup_start = str(date_lookup)
            date_lookup_end = str(date_lookup)
            date_lookup_name = str(date_lookup)
        #Check about month/querter info
        month_quarter = tracker.get_slot('month')
        if not month_quarter or str(month_quarter).lower() == "none" or date_lookup_name == "All Years":
            month_start = "01"
            month_end = "12"
        else:
            if str(date_lookup_name) == "":
                date_lookup_name = str(month_quarter).capitalize()
            else:
                date_lookup_name = str(month_quarter).capitalize() + '</b> in <b>' + date_lookup_name
            if "q" in str(month_quarter).lower():
                quarter = math.ceil((now.month) / 3)
                if "1" in str(month_quarter):
                    month_start = "01"
                    month_end = "03"
                    quarter_requested = 1
                elif "2" in str(month_quarter):
                    month_start = "04"
                    month_end = "06"
                    quarter_requested = 2
                elif "3" in str(month_quarter):
                    month_start = "07"
                    month_end = "09"
                    quarter_requested = 3
                elif "4" in str(month_quarter):
                    month_start = "10"
                    month_end = "12"
                    quarter_requested = 4
                elif "last" in str(month_quarter):
                    quarter_requested = quarter - 1
                    print(quarter_requested)
                    if (quarter_requested) == 0:
                        date_lookup_start = str(last_year)
                        date_lookup_end = str(last_year)
                        month_start = "10"
                        month_end = "12"
                    else: 
                        month_start = str(((quarter_requested - 1) * 3) + 1)
                        month_end = str(quarter_requested * 3)
                elif "this" in str(month_quarter):
                    print(quarter)
                    month_start = str(((quarter - 1) * 3) + 1)
                    month_end = str(quarter * 3)
                    quarter_requested = quarter
                if quarter_requested > quarter and int(date_lookup_start) == now.year:
                    response = "We cannot lookup for data in the future... yet, it's only possible to provide data up to Q" + str(quarter) + " " + str(now.year)
                    dispatcher.utter_message(response)
                    return None 
            else:
                month_start = monthNumber[str(month_quarter).lower()]
                month_end = month_start
                if int(month_start) > now.month and int(date_lookup_start) == now.year:
                    response = "We cannot lookup for data in the future... yet, it's only possible to provide data up to " + str(now.month) + " " + str(now.year)
                    dispatcher.utter_message(response)
                    return None
                if month_start == "Invalid month":
                    month_start = "01"
                    month_end = "12"
                elif "last" in str(month_quarter).lower():
                    month_start = now.month - 1
                    month_end = now.month - 1
                elif "this" in str(month_quarter).lower():
                    month_start = now.month
                    month_end = now.month
        date_lookup_start = date_lookup_start + "-" + month_start + "-01"
        date_lookup_end = date_lookup_end + "-" + month_end + "-31"
        print(suppliernamesplookup)
        spend = 0
        musid = 0
        db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
        cursor = db.cursor()
        sql = "SELECT MONTH(InvoiceClearingDate) as Month, Round( SUM(USD),2) AS Spend FROM `ab_hana_sami_spend` WHERE Vendor LIKE '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') AND MarketArea LIKE '%s' GROUP BY MONTH;" % (suppliernamesplookup, date_lookup_start, date_lookup_end, '%' + market_area_lookup + '%')
        #sql = "SELECT DISTINCT MONTH(InvoiceClearingDate) as Month, SUM(USD) AS Spend FROM `ab_hana_sami_spend` WHERE Vendor = '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') AND MarketArea LIKE '%s' GROUP BY MONTH(InvoiceClearingDate);" % (suppliernamesplookup, date_lookup_start, date_lookup_end, '%' + market_area_lookup + '%')
																																																																								  
        print(sql)
        try:
            cursor.execute(sql)
            results = list(cursor)
            Supplier_SpendLookup.run.thisValue = results
        except:
            print("Error fetching data.")
        finally:
            db.close()
        
        malen = np.array(Supplier_SpendLookup.run.thisValue)
    

        #extract with numpy the columms from the matrix
        #if str(now.year) == date_lookup:
        #    monthNames = monthNames[:now.month]l
        #    monthlySpend = monthlySpend[:now.month]
        if malen.size != 0:
            Lflag = "bar"
            coulum1 = malen[:,0]
            coulum2 = malen[:,1]
            for x in coulum1:
                pos = np.where(coulum1 == x)
                monthlySpend[int(x) - 1] = coulum2[pos]

            quarterSpend[0] = monthlySpend[0] + monthlySpend[1] + monthlySpend[2]
            quarterSpend[1] = monthlySpend[3] + monthlySpend[4] + monthlySpend[5]
            quarterSpend[2] = monthlySpend[6] + monthlySpend[7] + monthlySpend[8]
            quarterSpend[3] = monthlySpend[9] + monthlySpend[10] + monthlySpend[11]
            quarterName = quarterName[int(math.ceil(int(month_start) / 3)) - 1:int(math.ceil(int(month_end) / 3))]
            quarterSpend = quarterSpend[int(math.ceil(int(month_start) / 3)) - 1:int(math.ceil(int(month_end) / 3))]
            #convert the individual strings into list
								
            col1 = quarterName.tolist()
            col2 = quarterSpend.tolist()					
						
            #prepare to convert into  json readable strings
            result1 = simplejson.dumps(col1)
            result2 = simplejson.dumps(col2)
						   
						   
            #Convert file into Json readeable string        
            rescol1 = simplejson.loads(result1)
            rescol2 = simplejson.loads(result2)    
            data = {
                "title": ['Supplier Spend by Quarter'],
                # These labels appear in the legend and in the tooltips when hovering different arcs
                "labels": rescol1,
                "backgroundColor": [
                    '#36a2eb',
                    '#ffcd56',
                    '#ff6384',
                    '#009688',
                    '#c45850',
                    '#345385',
                    '#FAEBD7',
                    '#7FFFD4',
                    '#8A2BE2',
                    '#D2691E',
                    '#36a2eb',
                    '#ffcd56'
                ],
                "chartsData": rescol2,
                "chartType": Lflag,
                "displayLegend": ['true']
            }
            dispatcher.utter_message(json_message={"payload": "chart", "data": data})
            ##dispatcher.utter_custom_json({"payload": "chart", "data": data})
            return []
        else:
            response = "No data available with supplier <b>" + suppliernamesplookup + "</b> in market area <b>" + market_area_lookup + "</b> to show graph by quarter during <b>" + date_lookup_name +"</b>"
            dispatcher.utter_message(response)
            return None


class Supplier_SpendGraph_ByCompany(Action):
    def name(self):
        return 'action_supplier_spend_graph_by_company'

    def run(self, dispatcher, tracker, domain, **kwargs):
        import requests
        import simplejson
        import numpy as np
        from decimal import Decimal
        import math
        monthNumber = {
            "january": "01",
            "february": "02",
            "march": "03",
            "april": "04",
            "may": "05",
            "june": "06",
            "july": "07",
            "august": "08",
            "september": "09",
            "october": "10",
            "november": "11",
            "december": "12"
        }

        suppliernamesplookup = tracker.get_slot('supplier_name')
        market_area_lookup = tracker.get_slot('market_area')
        if market_area_lookup == "all market areas" or market_area_lookup == "ALL Market Areas":
            market_area_lookup = ""
        else:
            market_area_lookup = market_area_lookup
        date_lookup = tracker.get_slot('date')
        now = datetime.datetime.now()
        last_year = now.year - 1
        if date_lookup.lower() == "this year":
            date_lookup_start = str(now.year)
            date_lookup_end = str(now.year)
            date_lookup_name = str(now.year)
        elif date_lookup.lower() == "last year":
            date_lookup_start = str(last_year)
            date_lookup_end = str(last_year)
            date_lookup_name = str(last_year)
        elif date_lookup.lower() == "all years":
            date_lookup_start = "1900"
            date_lookup_end = str(now.year)
            date_lookup_name = "All Years"
        elif int(date_lookup) > now.year:
            response = "We cannot lookup for data in the future... yet, it's only possible to provide data up to " + str(now.month) + " " + str(now.year)
            dispatcher.utter_message(response)
            return None
        else:
            date_lookup_start = str(date_lookup)
            date_lookup_end = str(date_lookup)
            date_lookup_name = str(date_lookup)
        #Check about month/querter info
        month_quarter = tracker.get_slot('month')
        if not month_quarter or str(month_quarter).lower() == "none" or date_lookup_name == "All Years":
            month_start = "01"
            month_end = "12"
        else:
            if str(date_lookup_name) == "":
                date_lookup_name = str(month_quarter).capitalize()
            else:
                date_lookup_name = str(month_quarter).capitalize() + '</b> in <b>' + date_lookup_name
            if "q" in str(month_quarter).lower():
                quarter = math.ceil((now.month) / 3)
                if "1" in str(month_quarter):
                    month_start = "01"
                    month_end = "03"
                    quarter_requested = 1
                elif "2" in str(month_quarter):
                    month_start = "04"
                    month_end = "06"
                    quarter_requested = 2
                elif "3" in str(month_quarter):
                    month_start = "07"
                    month_end = "09"
                    quarter_requested = 3
                elif "4" in str(month_quarter):
                    month_start = "10"
                    month_end = "12"
                    quarter_requested = 4
                elif "last" in str(month_quarter):
                    quarter_requested = quarter - 1
                    print(quarter_requested)
                    if (quarter_requested) == 0:
                        date_lookup_start = str(last_year)
                        date_lookup_end = str(last_year)
                        month_start = "10"
                        month_end = "12"
                    else: 
                        month_start = str(((quarter_requested - 1) * 3) + 1)
                        month_end = str(quarter_requested * 3)
                elif "this" in str(month_quarter):
                    print(quarter)
                    month_start = str(((quarter - 1) * 3) + 1)
                    month_end = str(quarter * 3)
                    quarter_requested = quarter
                if quarter_requested > quarter and int(date_lookup_start) == now.year:
                    response = "We cannot lookup for data in the future... yet, it's only possible to provide data up to Q" + str(quarter) + " " + str(now.year)
                    dispatcher.utter_message(response)
                    return None 
            else:
                month_start = monthNumber[str(month_quarter).lower()]
                month_end = month_start
                if int(month_start) > now.month and int(date_lookup_start) == now.year:
                    response = "We cannot lookup for data in the future... yet, it's only possible to provide data up to " + str(now.month) + " " + str(now.year)
                    dispatcher.utter_message(response)
                    return None
                if month_start == "Invalid month":
                    month_start = "01"
                    month_end = "12"
                elif "last" in str(month_quarter).lower():
                    month_start = now.month - 1
                    month_end = now.month - 1
                elif "this" in str(month_quarter).lower():
                    month_start = now.month
                    month_end = now.month
        date_lookup_start = date_lookup_start + "-" + month_start + "-01"
        date_lookup_end = date_lookup_end + "-" + month_end + "-31"
        print(suppliernamesplookup)
        spend = 0
        musid = 0
        db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
        cursor = db.cursor()
        #sql = "SELECT DISTINCT Company as Company, Round( SUM(USD),2) AS Spend FROM `ab_hana_sami_spend` WHERE Vendor LIKE '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') GROUP BY Company;" % (
        #'%' + suppliernamesplookup + '%', date_lookup_start, date_lookup_end)
        sql = "SELECT Company as Company, SUM(USD) AS Spend FROM `ab_hana_sami_spend` WHERE Vendor = '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') AND MarketArea LIKE '%s' GROUP BY Company;" % (suppliernamesplookup, date_lookup_start, date_lookup_end, '%' + market_area_lookup + '%')
        print(sql)
        try:
            cursor.execute(sql)
            results = list(cursor)
            Supplier_SpendLookup.run.thisValue = results
        except:
            print("Error fetching data.")
        finally:
            db.close()

        malen = np.array(Supplier_SpendLookup.run.thisValue)
        Lflag = "bar"

        # extract with numpy the columms from the matrix
        coulum1 = malen[:, 0]
        coulum2 = malen[:, 1]
        # convert the individual strings into list
        col1 = coulum1.tolist()
        col2 = coulum2.tolist()
        # prepare to convert into  json readable strings
        result1 = simplejson.dumps(col1)
        result2 = simplejson.dumps(col2)
        # Convert file into Json readeable string
        rescol1 = simplejson.loads(result1)
        rescol2 = simplejson.loads(result2)
        print (result1)
        print (result2)
        print (Lflag)

        data = {
            "title": ['Supplier Spend by Company'],
            # These labels appear in the legend and in the tooltips when hovering different arcs
            "labels": rescol1,
            "backgroundColor": [
                '#36a2eb',
                '#ffcd56',
                '#ff6384',
                '#009688',
                '#c45850',
                '#F0F8FF',
                '#FAEBD7',
                '#7FFFD4',
                '#8A2BE2',
                '#D2691E',
                '#36a2eb',
                '#ffcd56'
            ],
            "chartsData": rescol2,
            "chartType": Lflag,
            "displayLegend": ['true']
        }
        dispatcher.utter_custom_json({"payload": "chart", "data": data})
        return []


class Supplier_SpendGraph_ByCustomer(Action):
    def name(self):
        return 'action_supplier_spend_graph_by_customer'

    def run(self, dispatcher, tracker, domain, **kwargs):
        import requests
        import simplejson
        import numpy as np
        from decimal import Decimal
        import math
        monthNumber = {
            "january": "01",
            "february": "02",
            "march": "03",
            "april": "04",
            "may": "05",
            "june": "06",
            "july": "07",
            "august": "08",
            "september": "09",
            "october": "10",
            "november": "11",
            "december": "12"
        }

        suppliernamesplookup = tracker.get_slot('supplier_name')
        market_area_lookup = tracker.get_slot('market_area')
        if market_area_lookup == "all market areas" or market_area_lookup == "ALL Market Areas":
            market_area_lookup = ""
        else:
            market_area_lookup = market_area_lookup
        date_lookup = tracker.get_slot('date')
        now = datetime.datetime.now()
        last_year = now.year - 1
        if date_lookup.lower() == "this year":
            date_lookup_start = str(now.year)
            date_lookup_end = str(now.year)
            date_lookup_name = str(now.year)
        elif date_lookup.lower() == "last year":
            date_lookup_start = str(last_year)
            date_lookup_end = str(last_year)
            date_lookup_name = str(last_year)
        elif date_lookup.lower() == "all years":
            date_lookup_start = "1900"
            date_lookup_end = str(now.year)
            date_lookup_name = "All Years"
        elif int(date_lookup) > now.year:
            response = "We cannot lookup for data in the future... yet, it's only possible to provide data up to " + str(now.month) + " " + str(now.year)
            dispatcher.utter_message(response)
            return None
        else:
            date_lookup_start = str(date_lookup)
            date_lookup_end = str(date_lookup)
            date_lookup_name = str(date_lookup)
        #Check about month/querter info
        month_quarter = tracker.get_slot('month')
        if not month_quarter or str(month_quarter).lower() == "none" or date_lookup_name == "All Years":
            month_start = "01"
            month_end = "12"
        else:
            if str(date_lookup_name) == "":
                date_lookup_name = str(month_quarter).capitalize()
            else:
                date_lookup_name = str(month_quarter).capitalize() + '</b> in <b>' + date_lookup_name
            if "q" in str(month_quarter).lower():
                quarter = math.ceil((now.month) / 3)
                if "1" in str(month_quarter):
                    month_start = "01"
                    month_end = "03"
                    quarter_requested = 1
                elif "2" in str(month_quarter):
                    month_start = "04"
                    month_end = "06"
                    quarter_requested = 2
                elif "3" in str(month_quarter):
                    month_start = "07"
                    month_end = "09"
                    quarter_requested = 3
                elif "4" in str(month_quarter):
                    month_start = "10"
                    month_end = "12"
                    quarter_requested = 4
                elif "last" in str(month_quarter):
                    quarter_requested = quarter - 1
                    print(quarter_requested)
                    if (quarter_requested) == 0:
                        date_lookup_start = str(last_year)
                        date_lookup_end = str(last_year)
                        month_start = "10"
                        month_end = "12"
                    else: 
                        month_start = str(((quarter_requested - 1) * 3) + 1)
                        month_end = str(quarter_requested * 3)
                elif "this" in str(month_quarter):
                    print(quarter)
                    month_start = str(((quarter - 1) * 3) + 1)
                    month_end = str(quarter * 3)
                    quarter_requested = quarter
                if quarter_requested > quarter and int(date_lookup_start) == now.year:
                    response = "We cannot lookup for data in the future... yet, it's only possible to provide data up to Q" + str(quarter) + " " + str(now.year)
                    dispatcher.utter_message(response)
                    return None 
            else:
                month_start = monthNumber[str(month_quarter).lower()]
                month_end = month_start
                if int(month_start) > now.month and int(date_lookup_start) == now.year:
                    response = "We cannot lookup for data in the future... yet, it's only possible to provide data up to " + str(now.month) + " " + str(now.year)
                    dispatcher.utter_message(response)
                    return None
                if month_start == "Invalid month":
                    month_start = "01"
                    month_end = "12"
                elif "last" in str(month_quarter).lower():
                    month_start = now.month - 1
                    month_end = now.month - 1
                elif "this" in str(month_quarter).lower():
                    month_start = now.month
                    month_end = now.month
        date_lookup_start = date_lookup_start + "-" + month_start + "-01"
        date_lookup_end = date_lookup_end + "-" + month_end + "-31"
        print(suppliernamesplookup)
        spend = 0
        musid = 0
        db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
        cursor = db.cursor()
        #sql = "SELECT DISTINCT CustomerUnitName as Customer, Round( SUM(USD),2) AS Spend FROM `ab_hana_sami_spend` WHERE Vendor LIKE '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') GROUP BY CustomerUnitName;" % (
        #'%' + suppliernamesplookup + '%', date_lookup_start, date_lookup_end)
        sql = "SELECT CustomerUnitName as Customer, SUM(USD) AS Spend FROM `ab_hana_sami_spend` WHERE Vendor = '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') AND MarketArea LIKE '%s' GROUP BY CustomerUnitName;" % (suppliernamesplookup, date_lookup_start, date_lookup_end, '%' + market_area_lookup + '%')
        print(sql)
        try:
            cursor.execute(sql)
            results = list(cursor)
            Supplier_SpendLookup.run.thisValue = results
        except:
            print("Error fetching data.")
        finally:
            db.close()

        malen = np.array(Supplier_SpendLookup.run.thisValue)
        Lflag = "bar"

        # extract with numpy the columms from the matrix
        coulum1 = malen[:, 0]
        coulum2 = malen[:, 1]
        # convert the individual strings into list
        col1 = coulum1.tolist()
        col2 = coulum2.tolist()
        # prepare to convert into  json readable strings
        result1 = simplejson.dumps(col1)
        result2 = simplejson.dumps(col2)
        # Convert file into Json readeable string
        rescol1 = simplejson.loads(result1)
        rescol2 = simplejson.loads(result2)
        print (result1)
        print (result2)
        print (Lflag)

        data = {
            "title": ['Supplier Spend by Customer'],
            # These labels appear in the legend and in the tooltips when hovering different arcs
            "labels": rescol1,
            "backgroundColor": [
                '#36a2eb',
                '#ffcd56',
                '#ff6384',
                '#009688',
                '#c45850',
                '#F0F8FF',
                '#FAEBD7',
                '#7FFFD4',
                '#8A2BE2',
                '#D2691E',
                '#36a2eb',
                '#ffcd56'
            ],
            "chartsData": rescol2,
            "chartType": Lflag,
            "displayLegend": ['true']
        }
        dispatcher.utter_custom_json({"payload": "chart", "data": data})
        return []


class Supplier_SpendGraph_ByBusinessUnit(Action):
    def name(self):
        return 'action_supplier_spend_graph_by_businessunit'

    def run(self, dispatcher, tracker, domain, **kwargs):
        import requests
        import simplejson
        import numpy as np
        from decimal import Decimal
        import math
        monthNumber = {
            "january": "01",
            "february": "02",
            "march": "03",
            "april": "04",
            "may": "05",
            "june": "06",
            "july": "07",
            "august": "08",
            "september": "09",
            "october": "10",
            "november": "11",
            "december": "12"
        }

        suppliernamesplookup = tracker.get_slot('supplier_name')
        market_area_lookup = tracker.get_slot('market_area')
        if market_area_lookup == "all market areas" or market_area_lookup == "ALL Market Areas":
            market_area_lookup = ""
        else:
            market_area_lookup = market_area_lookup
        date_lookup = tracker.get_slot('date')
        now = datetime.datetime.now()
        last_year = now.year - 1
        if date_lookup.lower() == "this year":
            date_lookup_start = str(now.year)
            date_lookup_end = str(now.year)
            date_lookup_name = str(now.year)
        elif date_lookup.lower() == "last year":
            date_lookup_start = str(last_year)
            date_lookup_end = str(last_year)
            date_lookup_name = str(last_year)
        elif date_lookup.lower() == "all years":
            date_lookup_start = "1900"
            date_lookup_end = str(now.year)
            date_lookup_name = "All Years"
        elif int(date_lookup) > now.year:
            response = "We cannot lookup for data in the future... yet, it's only possible to provide data up to " + str(now.month) + " " + str(now.year)
            dispatcher.utter_message(response)
            return None
        else:
            date_lookup_start = str(date_lookup)
            date_lookup_end = str(date_lookup)
            date_lookup_name = str(date_lookup)
        #Check about month/querter info
        month_quarter = tracker.get_slot('month')
        if not month_quarter or str(month_quarter).lower() == "none" or date_lookup_name == "All Years":
            month_start = "01"
            month_end = "12"
        else:
            if str(date_lookup_name) == "":
                date_lookup_name = str(month_quarter).capitalize()
            else:
                date_lookup_name = str(month_quarter).capitalize() + '</b> in <b>' + date_lookup_name
            if "q" in str(month_quarter).lower():
                quarter = math.ceil((now.month) / 3)
                if "1" in str(month_quarter):
                    month_start = "01"
                    month_end = "03"
                    quarter_requested = 1
                elif "2" in str(month_quarter):
                    month_start = "04"
                    month_end = "06"
                    quarter_requested = 2
                elif "3" in str(month_quarter):
                    month_start = "07"
                    month_end = "09"
                    quarter_requested = 3
                elif "4" in str(month_quarter):
                    month_start = "10"
                    month_end = "12"
                    quarter_requested = 4
                elif "last" in str(month_quarter):
                    quarter_requested = quarter - 1
                    print(quarter_requested)
                    if (quarter_requested) == 0:
                        date_lookup_start = str(last_year)
                        date_lookup_end = str(last_year)
                        month_start = "10"
                        month_end = "12"
                    else: 
                        month_start = str(((quarter_requested - 1) * 3) + 1)
                        month_end = str(quarter_requested * 3)
                elif "this" in str(month_quarter):
                    print(quarter)
                    month_start = str(((quarter - 1) * 3) + 1)
                    month_end = str(quarter * 3)
                    quarter_requested = quarter
                if quarter_requested > quarter and int(date_lookup_start) == now.year:
                    response = "We cannot lookup for data in the future... yet, it's only possible to provide data up to Q" + str(quarter) + " " + str(now.year)
                    dispatcher.utter_message(response)
                    return None 
            else:
                month_start = monthNumber[str(month_quarter).lower()]
                month_end = month_start
                if int(month_start) > now.month and int(date_lookup_start) == now.year:
                    response = "We cannot lookup for data in the future... yet, it's only possible to provide data up to " + str(now.month) + " " + str(now.year)
                    dispatcher.utter_message(response)
                    return None
                if month_start == "Invalid month":
                    month_start = "01"
                    month_end = "12"
                elif "last" in str(month_quarter).lower():
                    month_start = now.month - 1
                    month_end = now.month - 1
                elif "this" in str(month_quarter).lower():
                    month_start = now.month
                    month_end = now.month
        date_lookup_start = date_lookup_start + "-" + month_start + "-01"
        date_lookup_end = date_lookup_end + "-" + month_end + "-31"
        print(suppliernamesplookup)
        spend = 0
        musid = 0
        db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
        cursor = db.cursor()
        #sql = "SELECT DISTINCT BusinessUnitCode as Business, Round( SUM(USD),2) AS Spend FROM `ab_hana_sami_spend` WHERE Vendor LIKE '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') GROUP BY BusinessUnitCode;" % (
        #'%' + suppliernamesplookup + '%', date_lookup_start, date_lookup_end)
        sql = "SELECT BusinessUnitCode as Business, SUM(USD) AS Spend FROM `ab_hana_sami_spend` WHERE Vendor = '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') AND MarketArea LIKE '%s' GROUP BY BusinessUnitCode;" % (suppliernamesplookup, date_lookup_start, date_lookup_end, '%' + market_area_lookup + '%')
        print(sql)
        try:
            cursor.execute(sql)
            results = list(cursor)
            Supplier_SpendLookup.run.thisValue = results
        except:
            print("Error fetching data.")
        finally:
            db.close()

        malen = np.array(Supplier_SpendLookup.run.thisValue)
        Lflag = "bar"

        # extract with numpy the columms from the matrix
        coulum1 = malen[:, 0]
        coulum2 = malen[:, 1]
        # convert the individual strings into list
        col1 = coulum1.tolist()
        col2 = coulum2.tolist()
        # prepare to convert into  json readable strings
        result1 = simplejson.dumps(col1)
        result2 = simplejson.dumps(col2)
        # Convert file into Json readeable string
        rescol1 = simplejson.loads(result1)
        rescol2 = simplejson.loads(result2)
        print (result1)
        print (result2)
        print (Lflag)

        data = {
            "title": ['Supplier Spend by Business'],
            # These labels appear in the legend and in the tooltips when hovering different arcs
            "labels": rescol1,
            "backgroundColor": [
                '#36a2eb',
                '#ffcd56',
                '#ff6384',
                '#009688',
                '#c45850',
                '#F0F8FF',
                '#FAEBD7',
                '#7FFFD4',
                '#8A2BE2',
                '#D2691E',
                '#36a2eb',
                '#ffcd56'
            ],
            "chartsData": rescol2,
            "chartType": Lflag,
            "displayLegend": ['true']
        }
        dispatcher.utter_custom_json({"payload": "chart", "data": data})
        return []


class Supplier_SpendGraph_ByMarketArea(Action):
    def name(self):
        return 'action_supplier_spend_graph_by_marketarea'

    def run(self, dispatcher, tracker, domain, **kwargs):
        import requests
        import simplejson
        import numpy as np
        from decimal import Decimal
        import math
        monthNumber = {
            "january": "01",
            "february": "02",
            "march": "03",
            "april": "04",
            "may": "05",
            "june": "06",
            "july": "07",
            "august": "08",
            "september": "09",
            "october": "10",
            "november": "11",
            "december": "12"
        }

        suppliernamesplookup = tracker.get_slot('supplier_name')
        market_area_lookup = tracker.get_slot('market_area')
        if market_area_lookup == "all market areas" or market_area_lookup == "ALL Market Areas":
            market_area_lookup = ""
        else:
            market_area_lookup = market_area_lookup
        date_lookup = tracker.get_slot('date')
        now = datetime.datetime.now()
        last_year = now.year - 1
        if date_lookup.lower() == "this year":
            date_lookup_start = str(now.year)
            date_lookup_end = str(now.year)
            date_lookup_name = str(now.year)
        elif date_lookup.lower() == "last year":
            date_lookup_start = str(last_year)
            date_lookup_end = str(last_year)
            date_lookup_name = str(last_year)
        elif date_lookup.lower() == "all years":
            date_lookup_start = "1900"
            date_lookup_end = str(now.year)
            date_lookup_name = "All Years"
        elif int(date_lookup) > now.year:
            response = "We cannot lookup for data in the future... yet, it's only possible to provide data up to " + str(now.month) + " " + str(now.year)
            dispatcher.utter_message(response)
            return None
        else:
            date_lookup_start = str(date_lookup)
            date_lookup_end = str(date_lookup)
            date_lookup_name = str(date_lookup)
        #Check about month/querter info
        month_quarter = tracker.get_slot('month')
        if not month_quarter or str(month_quarter).lower() == "none" or date_lookup_name == "All Years":
            month_start = "01"
            month_end = "12"
        else:
            if str(date_lookup_name) == "":
                date_lookup_name = str(month_quarter).capitalize()
            else:
                date_lookup_name = str(month_quarter).capitalize() + '</b> in <b>' + date_lookup_name
            if "q" in str(month_quarter).lower():
                quarter = math.ceil((now.month) / 3)
                if "1" in str(month_quarter):
                    month_start = "01"
                    month_end = "03"
                    quarter_requested = 1
                elif "2" in str(month_quarter):
                    month_start = "04"
                    month_end = "06"
                    quarter_requested = 2
                elif "3" in str(month_quarter):
                    month_start = "07"
                    month_end = "09"
                    quarter_requested = 3
                elif "4" in str(month_quarter):
                    month_start = "10"
                    month_end = "12"
                    quarter_requested = 4
                elif "last" in str(month_quarter):
                    quarter_requested = quarter - 1
                    print(quarter_requested)
                    if (quarter_requested) == 0:
                        date_lookup_start = str(last_year)
                        date_lookup_end = str(last_year)
                        month_start = "10"
                        month_end = "12"
                    else: 
                        month_start = str(((quarter_requested - 1) * 3) + 1)
                        month_end = str(quarter_requested * 3)
                elif "this" in str(month_quarter):
                    print(quarter)
                    month_start = str(((quarter - 1) * 3) + 1)
                    month_end = str(quarter * 3)
                    quarter_requested = quarter
                if quarter_requested > quarter and int(date_lookup_start) == now.year:
                    response = "We cannot lookup for data in the future... yet, it's only possible to provide data up to Q" + str(quarter) + " " + str(now.year)
                    dispatcher.utter_message(response)
                    return None 
            else:
                month_start = monthNumber[str(month_quarter).lower()]
                month_end = month_start
                if int(month_start) > now.month and int(date_lookup_start) == now.year:
                    response = "We cannot lookup for data in the future... yet, it's only possible to provide data up to " + str(now.month) + " " + str(now.year)
                    dispatcher.utter_message(response)
                    return None
                if month_start == "Invalid month":
                    month_start = "01"
                    month_end = "12"
                elif "last" in str(month_quarter).lower():
                    month_start = now.month - 1
                    month_end = now.month - 1
                elif "this" in str(month_quarter).lower():
                    month_start = now.month
                    month_end = now.month
        date_lookup_start = date_lookup_start + "-" + month_start + "-01"
        date_lookup_end = date_lookup_end + "-" + month_end + "-31"
        print(suppliernamesplookup)
        spend = 0
        musid = 0
        db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
        cursor = db.cursor()
        #sql = "SELECT DISTINCT MarketArea as MarketArea, Round( SUM(USD),2) AS Spend FROM `ab_hana_sami_spend` WHERE Vendor LIKE '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') GROUP BY MarketArea;" % (
        #'%' + suppliernamesplookup + '%', date_lookup_start, date_lookup_end)
        sql = "SELECT MarketArea as MarketArea, SUM(USD) AS Spend FROM `ab_hana_sami_spend` WHERE Vendor = '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') AND MarketArea LIKE '%s' GROUP BY MarketArea;" % (suppliernamesplookup, date_lookup_start, date_lookup_end, '%' + market_area_lookup + '%')
        print(sql)
        try:
            cursor.execute(sql)
            results = list(cursor)
            Supplier_SpendLookup.run.thisValue = results
        except:
            print("Error fetching data.")
        finally:
            db.close()

        malen = np.array(Supplier_SpendLookup.run.thisValue)
        Lflag = "bar"

        # extract with numpy the columms from the matrix
        coulum1 = malen[:, 0]
        coulum2 = malen[:, 1]
        # convert the individual strings into list
        col1 = coulum1.tolist()
        col2 = coulum2.tolist()
        # prepare to convert into  json readable strings
        result1 = simplejson.dumps(col1)
        result2 = simplejson.dumps(col2)
        # Convert file into Json readeable string
        rescol1 = simplejson.loads(result1)
        rescol2 = simplejson.loads(result2)
        print (result1)
        print (result2)
        print (Lflag)

        data = {
            "title": ['Supplier Spend by Market Area'],
            # These labels appear in the legend and in the tooltips when hovering different arcs
            "labels": rescol1,
            "backgroundColor": [
                '#36a2eb',
                '#ffcd56',
                '#ff6384',
                '#009688',
                '#c45850',
                '#F0F8FF',
                '#FAEBD7',
                '#7FFFD4',
                '#8A2BE2',
                '#D2691E',
                '#36a2eb',
                '#ffcd56'
            ],
            "chartsData": rescol2,
            "chartType": Lflag,
            "displayLegend": ['true']
        }
        dispatcher.utter_custom_json({"payload": "chart", "data": data})
        return []

class Supplier_SpendGraph_ByCategory(Action):
    def name(self):
        return 'action_supplier_spend_graph_by_category'

    def run(self, dispatcher, tracker, domain, **kwargs):
        import requests
        import simplejson
        import numpy as np
        from decimal import Decimal

        suppliernamesplookup = tracker.get_slot('supplier_name')
        market_area_lookup = tracker.get_slot('market_area')
        if market_area_lookup == "all market areas" or market_area_lookup == "ALL Market Areas":
            market_area_lookup = ""
        else:
            market_area_lookup = market_area_lookup
        date_lookup = tracker.get_slot('date')
        now = datetime.datetime.now()
        last_year = now.year - 1
        if date_lookup.lower() == "this year":
            date_lookup_start = str(now.year) + "-01-01"
            date_lookup_end = str(now.year) + "-12-31"
            date_lookup_name = str(now.year)
        elif date_lookup.lower() == "last year":
            date_lookup_start = str(last_year) + "-01-01"
            date_lookup_end = str(last_year) + "-12-31"
            date_lookup_name = str(last_year)
        elif date_lookup.lower() == "all years":
            date_lookup_start = "1900-01-01"
            date_lookup_end = str(now.year) + "-12-31"
            date_lookup_name = "All Years"
        elif int(date_lookup) > now.year:
            response = "We cannot lookup for data in the future... yet, it's only possible to provide data up to " + str(now.year)
            dispatcher.utter_message(response)
            return None
        else:
            date_lookup_start = str(date_lookup) + "-01-01"
            date_lookup_end = str(date_lookup) + "-12-31"
            date_lookup_name = str(date_lookup)
        print(suppliernamesplookup)
        spend = 0
        musid = 0
        db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
        cursor = db.cursor()
        #sql = "SELECT DISTINCT MarketArea as MarketArea, Round( SUM(USD),2) AS Spend FROM `ab_hana_sami_spend` WHERE Vendor LIKE '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') GROUP BY MarketArea;" % (
        #'%' + suppliernamesplookup + '%', date_lookup_start, date_lookup_end)
        sql = "SELECT VendorSpendCategory, SUM(USD) AS Spend FROM `ab_hana_sami_spend` WHERE Vendor = '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') AND MarketArea LIKE '%s' GROUP BY VendorSpendCategory;" % (suppliernamesplookup, date_lookup_start, date_lookup_end, '%' + market_area_lookup + '%')
        print(sql)
        try:
            cursor.execute(sql)
            results = list(cursor)
            Supplier_SpendLookup.run.thisValue = results
        except:
            print("Error fetching data.")
        finally:
            db.close()

        malen = np.array(Supplier_SpendLookup.run.thisValue)
        Lflag = "bar"

        # extract with numpy the columms from the matrix
        coulum1 = malen[:, 0]
        coulum2 = malen[:, 1]
        # convert the individual strings into list
        col1 = coulum1.tolist()
        col2 = coulum2.tolist()
        # prepare to convert into  json readable strings
        result1 = simplejson.dumps(col1)
        result2 = simplejson.dumps(col2)
        # Convert file into Json readeable string
        rescol1 = simplejson.loads(result1)
        rescol2 = simplejson.loads(result2)
        print (result1)
        print (result2)
        print (Lflag)

        data = {
            "title": ['Supplier Spend by Category'],
            # These labels appear in the legend and in the tooltips when hovering different arcs
            "labels": rescol1,
            "backgroundColor": [
                '#36a2eb',
                '#ffcd56',
                '#ff6384',
                '#009688',
                '#c45850',
                '#F0F8FF',
                '#FAEBD7',
                '#7FFFD4',
                '#8A2BE2',
                '#D2691E',
                '#36a2eb',
                '#ffcd56'
            ],
            "chartsData": rescol2,
            "chartType": Lflag,
            "displayLegend": ['true']
        }
        dispatcher.utter_custom_json({"payload": "chart", "data": data})
        return []