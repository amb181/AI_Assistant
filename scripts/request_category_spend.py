from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction, UserUttered, ActionExecuted
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import requests ,re, pymysql, datetime, time, threading, logging
logger = logging.getLogger(__name__)


class CategorySpendForm(FormAction):
    def name(self):
        return 'category_spend_form'

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["category_name", "market_area", "date"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "category_name": self.from_entity(entity="category_name"),
            "market_area": self.from_entity(entity="market_area"),
            "date": self.from_entity(entity="date"),
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
        # run action category spend lookup
        # dispatcher.utter_message(template="utter_submit")
        # Need to add Stories that ask for category spend graph
        return [FollowupAction('action_category_spend_lookup')]


class Category_Lookup(Action):
    def name(self):
        return 'category_lookup'

    def run(self, dispatcher, tracker, domain):
        categoryname = tracker.get_slot('category_name')
        print(categoryname)
        if not categoryname:
            response = "I don't recognize this category name"
            dispatcher.utter_message(response)
        else:
            buttons = []
            message = ''
            db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
            cursor = db.cursor()
            sql = "SELECT DISTINCT VendorSpendCategory FROM `ab_hana_sami_spend` WHERE VendorSpendCategory LIKE '%s';" % (
                        '%' + categoryname + '%')
            print(sql)
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                if len(results) == 1:
                    for row in results:
                        # if a single supplier is found, set slot supplier_name_form and trigger spend form
                        categoryname = row[0]
                        message = ''
                        print(categoryname)
                        return SlotSet('category_name', categoryname), FollowupAction('category_spend_form')
                elif len(results) > 1:
                    for row in results:
                        # if a multiple suppliers are found, display buttons of all possible supplier matches back to user then trigger spend form
                        categoryname = row[0]
                        print(categoryname)
                        payload = "/inform{\"category_name\":\"" + categoryname + "\"}"
                        print(payload)
                        buttons.append({"title": "{}".format(categoryname.title()), "payload": payload})
                        message = "I found {} categories that also match that name, which one are you inquiring about?".format(len(buttons))
                else:
                    response = "I couldn't find any categories that match that name"
                    dispatcher.utter_message(response)
                dispatcher.utter_button_message(message, buttons)
                return []
            except (AttributeError, TypeError) as e:
                response = "I couldn't find any matches for that category name"
                # dispatcher.utter_message(e)
                dispatcher.utter_message(response)
                return None


class Category_SpendLookup(Action):
    def name(self):
        return 'action_category_spend_lookup'

    def run(self, dispatcher, tracker, domain):
        categorynamecnlookup = tracker.get_slot('category_name')
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
        print(categorynamecnlookup)
        spend = 0
        musid = 0
        db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
        cursor = db.cursor()
        cursor2 = db.cursor()
        print (categorynamecnlookup + " " + date_lookup_start + " " + date_lookup_end + " " + market_area_lookup)
        sql = "SELECT SUM(USD) AS Spend, VendorSpendCategory FROM `ab_hana_sami_spend` WHERE VendorSpendCategory = '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') AND MarketArea LIKE '%s' GROUP BY VendorSpendCategory;" % (
        categorynamecnlookup, str(date_lookup_start), str(date_lookup_end), '%' + market_area_lookup + '%')
        sql2 = "SELECT DISTINCT Company, SUM(USD) AS Spend FROM `ab_hana_sami_spend` WHERE VendorSpendCategory = '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') AND MarketArea LIKE '%s' GROUP BY Company;" % (
        categorynamecnlookup, str(date_lookup_start), str(date_lookup_end), '%' + market_area_lookup + '%')
        print(sql)
        print(sql2)
        try:
            cursor.execute(sql)
            cursor2.execute(sql2)
            results = cursor.fetchall()
            results2 = list(cursor2)
            for row in results:
                spend = row[0]
                categorynamecnlookup = row[1]
        except:
            print(results2)
            print("Error fetching data.")
        finally:
            db.close()
        # output sentence format
        print(spend)
        if spend == 0:
            response = """I couldn't find any spend for category {} for {} in {}.""".format("<b>"+categorynamecnlookup+"</b>",
                                                                                            "<b>"+date_lookup_name+"</b>",
                                                                                            "<b>"+market_area_lookup_name+"</b>")
        elif spend > 0:
            spend = "${:,.2f}".format(spend)
            spend = str(spend)
            # response = """The spend for supplier {} is ${:,.2f} for {}. This is based on MUSID {}.""".format(categorynamecnlookup, spend, date_lookup, musid)
            response = """The spend for category {} is {} for {} in {}.""".format("<b>"+categorynamecnlookup+"</b>", "<b>"+spend+"</b>",
                                                                                        "<b>"+date_lookup_name+"</b>",
                                                                                        "<b>"+market_area_lookup_name+"</b>")
        Category_SpendLookup.run.thisValue = results2
        dispatcher.utter_message(response), FollowupAction('action_supplier_dowjones_check')
        # return [AllSlotsReset()]
        # return[SlotSet("category_name", None)]


class Category_SpendGraph(Action):
    def name(self):
        return 'action_category_spend_graph'

    def run(self, dispatcher, tracker, domain, **kwargs):
        import requests
        import simplejson
        import numpy as np
        from decimal import Decimal

        malen = np.array(Category_SpendLookup.run.thisValue)
        Lflag = tracker.latest_message["text"]

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
            "title": ['Category spend'],
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


class Category_SpendGraph_ByMonth(Action):
    def name(self):
        return 'action_category_spend_graph_by_month'

    def run(self, dispatcher, tracker, domain, **kwargs):
        import requests
        import simplejson
        import numpy as np
        from decimal import Decimal

        monthNames = np.array(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
        monthlySpend = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        categorynamecnlookup = tracker.get_slot('category_name')
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
        print(categorynamecnlookup)
        spend = 0
        musid = 0
        db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
        cursor = db.cursor()
        #sql = "SELECT MONTH(InvoiceClearingDate) as Month, Round( SUM(USD),2) AS Spend FROM `ab_hana_sami_spend` WHERE VendorSpendCategory LIKE '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') AND MarketArea LIKE '%s' GROUP BY MONTH;" % (
        #categorynamecnlookup, str(date_lookup_start), str(date_lookup_end), '%' + market_area_lookup + '%')
        sql = "SELECT MONTH(InvoiceClearingDate) as Month, Round(SUM(USD), 2) AS Spend FROM `ab_hana_sami_spend` WHERE VendorSpendCategory = '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') AND MarketArea LIKE '%s' GROUP BY MONTH;" % (
            categorynamecnlookup, date_lookup_start, date_lookup_end, '%' + market_area_lookup + '%')
        print(sql)
        try:
            cursor.execute(sql)
            results = list(cursor)
            Category_SpendLookup.run.thisValue = results
        except:
            print("Error fetching data.")
        finally:
            db.close()

        malen = np.array(Category_SpendLookup.run.thisValue)
    
        #extract with numpy the columms from the matrix
        if str(now.year) == date_lookup:
            monthNames = monthNames[:now.month]
            monthlySpend = monthlySpend[:now.month]
        if malen.size != 0:
            Lflag = "line"
            coulum1 = malen[:,0]
            coulum2 = malen[:,1]
            for x in coulum1:
                pos = np.where(coulum1 == x)                
                monthlySpend[int(x) - 1] = coulum2[pos]
            #convert the individual strings into list
            col1 = monthNames.tolist()
            col2 = monthlySpend.tolist()
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
                "title": ['Category Spend by Month'],
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
            return []
        else:
            print("{} / {} / {}".format(categorynamecnlookup,market_area_lookup,date_lookup_name))
            response = "No data available with category <b>" + categorynamecnlookup + "</b> in market area <b>" + market_area_lookup + "</b> to show graph by month during <b>" + date_lookup_name + "</b>"
            dispatcher.utter_message(response)
            return None


class Category_SpendGraph_BySupplier(Action):
    def name(self):
        return 'action_category_spend_graph_by_supplier'

    def run(self, dispatcher, tracker, domain, **kwargs):
        import requests
        import simplejson
        import numpy as np
        from decimal import Decimal

        categorynamecnlookup = tracker.get_slot('category_name')
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
        print(categorynamecnlookup)
        spend = 0
        musid = 0
        db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
        cursor = db.cursor()
        #sql = "SELECT DISTINCT Vendor as Supplier, Round( SUM(USD),2) AS Spend FROM `ab_hana_sami_spend` WHERE VendorSpendCategory LIKE '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') GROUP BY Supplier;" % (
        #'%' + categorynamecnlookup + '%', date_lookup_start, date_lookup_end)
        sql = "SELECT Vendor as Supplier, Round( SUM(USD),2) AS Spend FROM `ab_hana_sami_spend` WHERE VendorSpendCategory = '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') AND MarketArea LIKE '%s' GROUP BY Vendor;" % (
            categorynamecnlookup, date_lookup_start, date_lookup_end, '%' + market_area_lookup + '%')
        print(sql)
        try:
            cursor.execute(sql)
            results = list(cursor)
            Category_SpendLookup.run.thisValue = results
        except:
            print("Error fetching data.")
        finally:
            db.close()

        malen = np.array(Category_SpendLookup.run.thisValue)
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
            "title": ['Category Spend by Supplier'],
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


class Category_SpendGraph_ByCompany(Action):
    def name(self):
        return 'action_category_spend_graph_by_company'

    def run(self, dispatcher, tracker, domain, **kwargs):
        import requests
        import simplejson
        import numpy as np
        from decimal import Decimal

        categorynamecnlookup = tracker.get_slot('category_name')
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
        print(categorynamecnlookup)
        spend = 0
        musid = 0
        db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
        cursor = db.cursor()
        #sql = "SELECT DISTINCT Company as Company, Round( SUM(USD),2) AS Spend FROM `ab_hana_sami_spend` WHERE VendorSpendCategory LIKE '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') GROUP BY Supplier;" % (
        #'%' + categorynamecnlookup + '%', date_lookup_start, date_lookup_end)
        sql = "SELECT Company as Company, Round( SUM(USD),2) AS Spend FROM `ab_hana_sami_spend` WHERE VendorSpendCategory = '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') AND MarketArea LIKE '%s' GROUP BY Company;" % (
            categorynamecnlookup, date_lookup_start, date_lookup_end, '%' + market_area_lookup + '%')
        print(sql)
        try:
            cursor.execute(sql)
            results = list(cursor)
            Category_SpendLookup.run.thisValue = results
        except:
            print("Error fetching data.")
        finally:
            db.close()

        malen = np.array(Category_SpendLookup.run.thisValue)
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
            "title": ['Category Spend by Company'],
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


class Category_SpendGraph_ByCustomer(Action):
    def name(self):
        return 'action_category_spend_graph_by_customer'

    def run(self, dispatcher, tracker, domain, **kwargs):
        import requests
        import simplejson
        import numpy as np
        from decimal import Decimal

        categorynamecnlookup = tracker.get_slot('category_name')
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
        print(categorynamecnlookup)
        spend = 0
        musid = 0
        db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
        cursor = db.cursor()
        #sql = "SELECT DISTINCT CustomerUnitName as Customer, Round( SUM(USD),2) AS Spend FROM `ab_hana_sami_spend` WHERE VendorSpendCategory LIKE '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') GROUP BY Customer;" % (
        #'%' + categorynamecnlookup + '%', date_lookup_start, date_lookup_end)
        sql = "SELECT CustomerUnitName as Customer, Round( SUM(USD),2) AS Spend FROM `ab_hana_sami_spend` WHERE VendorSpendCategory = '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') AND MarketArea LIKE '%s' GROUP BY CustomerUnitName;" % (
            categorynamecnlookup, date_lookup_start, date_lookup_end, '%' + market_area_lookup + '%')
        print(sql)
        try:
            cursor.execute(sql)
            results = list(cursor)
            Category_SpendLookup.run.thisValue = results
        except:
            print("Error fetching data.")
        finally:
            db.close()

        malen = np.array(Category_SpendLookup.run.thisValue)
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
            "title": ['Category Spend by Customer'],
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


class Category_SpendGraph_ByBusinessUnit(Action):
    def name(self):
        return 'action_category_spend_graph_by_businessunit'

    def run(self, dispatcher, tracker, domain, **kwargs):
        import requests
        import simplejson
        import numpy as np
        from decimal import Decimal

        categorynamecnlookup = tracker.get_slot('category_name')
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
        print(categorynamecnlookup)
        spend = 0
        musid = 0
        db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
        cursor = db.cursor()
        #sql = "SELECT DISTINCT CustomerUnitName as Customer, Round( SUM(USD),2) AS Spend FROM `ab_hana_sami_spend` WHERE VendorSpendCategory LIKE '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') GROUP BY Customer;" % (
        #'%' + categorynamecnlookup + '%', date_lookup_start, date_lookup_end)
        sql = "SELECT BusinessUnitCode as BusinessUnit, Round( SUM(USD),2) AS Spend FROM `ab_hana_sami_spend` WHERE VendorSpendCategory = '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') AND MarketArea LIKE '%s' GROUP BY BusinessUnitCode;" % (
            categorynamecnlookup, date_lookup_start, date_lookup_end, '%' + market_area_lookup + '%')
        print(sql)
        try:
            cursor.execute(sql)
            results = list(cursor)
            Category_SpendLookup.run.thisValue = results
        except:
            print("Error fetching data.")
        finally:
            db.close()

        malen = np.array(Category_SpendLookup.run.thisValue)
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
            "title": ['Category Spend by Business Unit'],
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


class Category_SpendGraph_ByMarketArea(Action):
    def name(self):
        return 'action_category_spend_graph_by_marketarea'

    def run(self, dispatcher, tracker, domain, **kwargs):
        import requests
        import simplejson
        import numpy as np
        from decimal import Decimal

        categorynamecnlookup = tracker.get_slot('category_name')
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
        print(categorynamecnlookup)
        spend = 0
        musid = 0
        db = pymysql.connect('localhost', 'ebromic', 'Ericsson1', 'ai')
        cursor = db.cursor()
        #sql = "SELECT DISTINCT MarketArea as MarketArea, Round( SUM(USD),2) AS Spend FROM `ab_hana_sami_spend` WHERE VendorSpendCategory LIKE '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') GROUP BY MarketArea;" % (
        #'%' + categorynamecnlookup + '%', date_lookup_start, date_lookup_end)
        sql = "SELECT MarketArea as MarketArea, Round( SUM(USD),2) AS Spend FROM `ab_hana_sami_spend` WHERE VendorSpendCategory = '%s' AND (InvoiceClearingDate BETWEEN '%s' and '%s') AND MarketArea LIKE '%s' GROUP BY MarketArea;" % (
            categorynamecnlookup, date_lookup_start, date_lookup_end, '%' + market_area_lookup + '%')
        print(sql)
        try:
            cursor.execute(sql)
            results = list(cursor)
            Category_SpendLookup.run.thisValue = results
        except:
            print("Error fetching data.")
        finally:
            db.close()

        malen = np.array(Category_SpendLookup.run.thisValue)
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
            "title": ['Category Spend by Market Area'],
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
