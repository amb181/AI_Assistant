
## category spend | later supplier category manager
* request_spend{"category_name": "arp", "market_area": "mana"}
    - slot{"category_name": "arp"}
    - slot{"market_area": "mana"}
    - action_request_spend
* inform{"category_name": "ARP"}
    - slot{"category_name": "ARP"}
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
* request_category_manager{"supplier_name": "american express", "market_area": "mela"}
    - slot{"market_area": "mela"}
    - slot{"supplier_name": "american express"}
    - action_request_category_manager
* inform{"supplier_name": "AMERICAN EXPRESS"}
    - slot{"supplier_name": "AMERICAN EXPRESS"}
    - form: followup{"name": "action_supplier_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_category_manager_lookup

## supplier spend | later category spend | later another date | its category manager | later supplier category manager
* request_spend{"supplier_name": "amatel", "market_area": "mana"}
    - slot{"market_area": "mana"}
    - slot{"supplier_name": "amatel"}
    - action_request_spend
* inform{"supplier_name": "AMATEL INC"}
    - slot{"supplier_name": "AMATEL INC"}
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
* request_another{"category_name": "arp"}
    - slot{"category_name": "arp"}
    - action_request_another
* request_another{"date": "last year"}
    - slot{"date": "last year"}
    - action_request_another
* request_category_manager
    - action_request_category_manager
    - form: followup{"name": "action_category_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_category_manager_lookup
* request_another{"supplier_name": "amatel", "market_area": "mela"}
    - slot{"market_area": "mela"}
    - slot{"supplier_name": "amatel"}
    - action_request_another


## supplier category manager | later supplier spend | later another marker with date

* request_category_manager{"supplier_name": "american express", "market_area": "mela"}
    - slot{"market_area": "mela"}
    - slot{"supplier_name": "american express"}
    - action_request_category_manager
* inform{"supplier_name": "AMERICAN EXPRESS"}
    - slot{"supplier_name": "AMERICAN EXPRESS"}
    - form: followup{"name": "action_supplier_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_category_manager_lookup
* request_spend
    - action_request_spend
    - slot{"requested_slot": "date"}
* form: date{"date": "last year"}
    - slot{"date": "last year"}
    - supplier_spend_form
    - slot{"date": "last year"}
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
* form: request_another{"date": "last year", "market_area": "mana"}
    - slot{"date": "last year"}
    - slot{"market_area": "mana"}
    - action_request_another
* askgraph_by_month
    - action_supplier_spend_graph_by_month


## category category manager | later category spend | later another marker with date

* request_category_manager{"category_name": "server", "market_area": "mela"}
    - slot{"market_area": "mela"}
    - slot{"category_name": "server"}
    - action_request_category_manager
* inform{"category_name": "Server & Storage"}
    - slot{"category_name": "Server & Storage"}
    - form: followup{"name": "action_category_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_category_manager_lookup
* request_spend
    - action_request_spend
    - slot{"requested_slot": "date"}
* form: date{"date": "last year"}
    - slot{"date": "last year"}
    - category_spend_form
    - slot{"date": "last year"}
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
* form: request_another{"date": "last year", "market_area": "mana"}
    - slot{"date": "last year"}
    - slot{"market_area": "mana"}
    - action_request_another
* askgraph_by_month
    - action_category_spend_graph_by_month

## category category manager | later supplier spend

* request_category_manager{"category_name": "server", "market_area": "mela"}
    - slot{"market_area": "mela"}
    - slot{"category_name": "server"}
    - action_request_category_manager
* inform{"category_name": "Server & Storage"}
    - slot{"category_name": "Server & Storage"}
    - form: followup{"name": "action_category_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_category_manager_lookup
* request_spend{"supplier_name": "fusion"}
    - slot{"supplier_name": "fusion"}
    - action_request_spend
* inform{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"requested_slot": "market_area"}
* form: market_area{"market_area": "mana"}
    - slot{"market_area": "mana"}
    - slot{"requested_slot": "date"}
* form: date{"date": "last year"}
    - slot{"date": "last year"}
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
* askgraph_by_customer
    - action_supplier_spend_graph_by_month