## Category
## interactive_story_1
* help_with_spend_nlu
    - utter_help_with_spend
* options_spend{"options_spend": "category"}
    - slot{"options_spend": "category"}
    - utter_ask_name
* inform{"category_name": "Batteries"}
    - slot{"category_name": "Batteries"}
    - slot{"requested_slot": "market_area"}
* form: market_area{"market_area": "mana"}
    - slot{"market_area": "mana"}
    - category_spend_form
    - slot{"requested_slot": "date"}
* form: date{"date": "last year"}
    - slot{"date": "last year"}
    - category_spend_form
	- slot{"requested_slot": "month"}
* request_q_m
    - utter_ask_Q_M
* request_month_info
    - utter_ask_months
* form: request_spend{"month": "May"}
    - slot{"month": "May"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup

## interactive_story_2
* help_with_spend_nlu
    - utter_help_with_spend
* options_spend{"options_spend": "category"}
    - slot{"options_spend": "category"}
    - utter_ask_name
* request_spend{"category_name": "corporate insurance"}
    - slot{"category_name": "corporate insurance"}
* inform{"category_name": "Corporate Insurance"}
    - slot{"category_name": "Corporate Insurance"}
    - slot{"requested_slot": "market_area"}
* form: market_area{"market_area": "mxot"}
    - slot{"market_area": "mxot"}
    - category_spend_form
    - slot{"requested_slot": "date"}
* form: date{"date": "last year"}
    - slot{"date": "last year"}
    - category_spend_form
	- slot{"requested_slot": "month"}
* request_q_m
    - utter_ask_Q_M
* request_month_info
    - utter_ask_months
* form: request_spend{"month": "May"}
    - slot{"month": "May"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup

## interactive_story_3
* help_with_spend_nlu
    - utter_help_with_spend
* options_spend{"options_spend": "category"}
    - slot{"options_spend": "category"}
    - utter_ask_name
* request_spend{"category_name": "arp"}
    - slot{"category_name": "arp"}
    - action_request_spend
* inform{"category_name": "ARP"}
    - slot{"category_name": "ARP"}
    - slot{"requested_slot": "market_area"}
* form: market_area{"market_area": "mana"}
    - slot{"market_area": "mana"}
    - category_spend_form
    - slot{"requested_slot": "date"}
* form: date{"date": "last year"}
    - slot{"date": "last year"}
    - category_spend_form
	- slot{"requested_slot": "month"}
* request_q_m
    - utter_ask_Q_M
* request_month_info
    - utter_ask_months
* form: request_spend{"month": "May"}
    - slot{"month": "May"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup



## interactive_story_4
* help_with_spend_nlu
    - utter_help_with_spend
* options_spend{"options_spend": "category"}
    - slot{"options_spend": "category"}
    - utter_ask_name
* request_spend{"category_name": "fleet"}
    - slot{"category_name": "fleet"}
    - action_request_spend
* inform{"category_name": "Fleet"}
    - slot{"category_name": "Fleet"}
    - slot{"requested_slot": "market_area"}
* form: market_area{"market_area": "mela"}
    - slot{"market_area": "mela"}
    - category_spend_form
    - slot{"requested_slot": "date"}
* form: date{"date": "last year"}
    - slot{"date": "last year"}
    - category_spend_form
	- slot{"requested_slot": "month"}
* request_q_m
    - utter_ask_Q_M
* request_month_info
    - utter_ask_months
* form: request_spend{"month": "May"}
    - slot{"month": "May"}
    - form: followup{"name": "action_category_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup


## Supplier


## interactive_story_1
* help_with_spend_nlu
    - utter_help_with_spend
* options_spend{"options_spend": "supplier"}
    - slot{"options_spend": "supplier"}
    - utter_ask_name
* request_spend{"supplier_name": "one2many"}
    - slot{"supplier_name": "one2many"}
    - action_request_spend
* inform{"supplier_name": "ONE2MANY B.V."}
    - slot{"supplier_name": "ONE2MANY B.V."}
    - slot{"requested_slot": "market_area"}
* form: market_area{"market_area": "mana"}
    - slot{"market_area": "mana"}
    - supplier_spend_form
    - slot{"requested_slot": "date"}
* form: date{"date": "last year"}
    - slot{"date": "last year"}
    - supplier_spend_form
	- slot{"requested_slot": "month"}
* request_q_m
    - utter_ask_Q_M
* request_month_info
    - utter_ask_months
* form: request_spend{"month": "May"}
    - slot{"month": "May"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup

## interactive_story_2
* help_with_spend_nlu
    - utter_help_with_spend
* options_spend{"options_spend": "supplier"}
    - slot{"options_spend": "supplier"}
    - utter_ask_name
* request_spend{"supplier_name": "american express"}
    - slot{"supplier_name": "american express"}
    - action_request_spend
* inform{"supplier_name": "AMERICAN EXPRESS"}
    - slot{"supplier_name": "AMERICAN EXPRESS"}
    - slot{"requested_slot": "market_area"}
* form: market_area{"market_area": "all market areas"}
    - slot{"market_area": "all market areas"}
    - supplier_spend_form
    - slot{"requested_slot": "date"}
* form: date{"date": "this year"}
    - slot{"date": "this year"}
    - supplier_spend_form
	- slot{"requested_slot": "month"}
* request_q_m
    - utter_ask_Q_M
* request_month_info
    - utter_ask_months
* form: request_spend{"month": "May"}
    - slot{"month": "May"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup

## interactive_story_3
* help_with_spend_nlu
    - utter_help_with_spend
* options_spend{"options_spend": "supplier"}
    - slot{"options_spend": "supplier"}
    - utter_ask_name
* inform{"supplier_name": "wipro"}
    - slot{"supplier_name": "wipro"}
    - action_request_spend
* inform{"supplier_name": "Wipro Ltd"}
    - slot{"supplier_name": "Wipro Ltd"}
    - slot{"requested_slot": "market_area"}
* form: market_area{"market_area": "mxot"}
    - slot{"market_area": "mxot"}
    - supplier_spend_form
    - slot{"requested_slot": "date"}
* form: date{"date": "last year"}
    - slot{"date": "last year"}
    - supplier_spend_form
	- slot{"requested_slot": "month"}
* request_q_m
    - utter_ask_Q_M
* request_month_info
    - utter_ask_months
* form: request_spend{"month": "May"}
    - slot{"month": "May"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup

## interactive_story_4
* help_with_spend_nlu
    - utter_help_with_spend
* options_spend{"options_spend": "supplier"}
    - slot{"options_spend": "supplier"}
    - utter_ask_name
* request_spend{"supplier_name": "commscope"}
    - slot{"supplier_name": "commscope"}
    - action_request_spend
* inform{"supplier_name": "COMMSCOPE TECHNOLOGIES LLC"}
    - slot{"supplier_name": "COMMSCOPE TECHNOLOGIES LLC"}
    - slot{"requested_slot": "market_area"}
* form: market_area{"market_area": "mxot"}
    - slot{"market_area": "mxot"}
    - supplier_spend_form
    - slot{"requested_slot": "date"}
* form: date{"date": "all years"}
    - slot{"date": "all years"}
    - supplier_spend_form
	- slot{"requested_slot": "month"}
* request_q_m
    - utter_ask_Q_M
* request_month_info
    - utter_ask_months
* form: request_spend{"month": "May"}
    - slot{"month": "May"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup