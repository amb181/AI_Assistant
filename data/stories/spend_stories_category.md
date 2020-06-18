## interactive_story_1
* request_spend{"category_name": "batteries"}
    - slot{"category_name": "batteries"}
    - action_request_spend
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
* request_spend{"category_name": "batteries", "market_area": "mana"}
    - slot{"category_name": "batteries"}
    - slot{"market_area": "mana"}
    - action_request_spend
* inform{"category_name": "Batteries"}
    - slot{"category_name": "Batteries"}
    - slot{"requested_slot": "date"}
* form: date{"date": "last year"}
    - slot{"date": "last year"}
    - category_spend_form
	- slot{"requested_slot": "month"}
* request_q_m
    - utter_ask_Q_M
* request_month_info
    - utter_ask_months
* form: request_spend{"month": "August"}
    - slot{"month": "August"}
    - form: followup{"name": "action_category_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup

## interactive_story_3
* request_spend{"category_name": "batteries", "date": "last year"}
    - slot{"category_name": "batteries"}
    - slot{"date": "last year"}
    - action_request_spend
* inform{"category_name": "Batteries"}
    - slot{"category_name": "Batteries"}
    - slot{"requested_slot": "market_area"}
* form: market_area{"market_area": "mana"}
    - slot{"market_area": "mana"}
    - category_spend_form
	- slot{"requested_slot": "month"}
* request_q_m
    - utter_ask_Q_M
* request_quarter_info
    - utter_ask_quarter
* form: request_spend{"month": "q3"}
    - slot{"month": "q3"}
    - form: followup{"name": "action_category_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup

## interactive_story_4
* request_spend{"category_name": "batteries", "market_area": "mana", "date": "last year"}
    - slot{"category_name": "batteries"}
    - slot{"date": "last year"}
    - slot{"market_area": "mana"}
    - action_request_spend
* inform{"category_name": "Batteries"}
    - slot{"category_name": "Batteries"}
    - category_spend_form
	- slot{"requested_slot": "month"}
* request_q_m
    - utter_ask_Q_M
* request_month_info
    - utter_ask_months
* form: request_spend{"month": "November"}
    - slot{"month": "November"}
    - form: followup{"name": "action_category_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup
* request_another{"category_name": "memories"}
    - slot{"category_name": "memories"}
    - action_request_another
* request_another{"category_name": "towers"}
    - slot{"category_name": "towers"}
    - action_request_another
* request_another{"category_name": "small cells"}
    - slot{"category_name": "small cells"}
    - action_request_another
* request_another{"category_name": "batteries"}
    - slot{"category_name": "batteries"}
    - action_request_another
* request_another{"category_name": "memories"}
    - slot{"category_name": "memories"}
    - action_request_another

## interactive_story_5
* request_spend{"category_name": "ARP", "market_area": "MOAI", "month": "May"}
    - slot{"category_name": "ARP"}
    - slot{"month": "May"}
    - slot{"market_area": "MOAI"}
    - action_request_spend
    - followup{"name": "category_lookup"}
    - category_lookup
    - slot{"category_name": "ARP"}
    - followup{"name": "category_spend_form"}
    - category_spend_form
    - form{"name": "category_spend_form"}
    - slot{"category_name": "ARP"}
    - slot{"market_area": "MOAI"}
    - slot{"month": "May"}
    - slot{"requested_slot": "date"}
* form: date{"date": "this yearr"}
    - slot{"date": "this year"}
    - form: category_spend_form
    - slot{"date": "this year"}
    - form: followup{"name": "action_category_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup
* askgraph_by_businessunit
    - action_category_spend_graph_by_businessunit

## ask graph by month
* request_spend{"category_name": "physical security", "market_area": "mana", "date": "last year", "month": "February"}
    - slot{"category_name": "physical security"}
    - slot{"date": "last year"}
    - slot{"market_area": "mana"}
    - slot{"month": "February"}
    - action_request_spend
* inform{"category_name": "Physical and Personal Security"}
    - slot{"category_name": "Physical and Personal Security"}
    - category_spend_form
    - form: followup{"name": "action_category_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup
* askgraph_by_month
    - action_category_spend_graph_by_month

## ask graph by supplier
* request_spend{"category_name": "personal security", "market_area": "mana", "date": "last year", "month": "3rd quarter"}
    - slot{"category_name": "personal security"}
    - slot{"date": "last year"}
    - slot{"market_area": "mana"}
    - slot{"month": "q3"}
    - action_request_spend
* inform{"category_name": "Physical and Personal Security"}
    - slot{"category_name": "Physical and Personal Security"}
    - category_spend_form
    - form: followup{"name": "action_category_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup
* askgraph_by_supplier
    - action_category_spend_graph_by_supplier

## ask graph by company
* request_spend{"category_name": "air travel", "market_area": "mxot", "date": "this year", "month": "May"}
    - slot{"category_name": "air travel"}
    - slot{"date": "this year"}
    - slot{"market_area": "mxot"}
    - slot{"month": "May"}
    - action_request_spend
* inform{"category_name": "Air Travel"}
    - slot{"category_name": "Air Travel"}
    - category_spend_form
    - form: followup{"name": "action_category_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup
* askgraph_by_company
    - action_category_spend_graph_by_company

## ask graph by customer
* request_spend{"category_name": "cable", "market_area": "mmea", "date": "2019", "month": "August"}
    - slot{"category_name": "cable"}
    - slot{"date": "2019"}
    - slot{"market_area": "mmea"}
    - slot{"month": "August"}
    - action_request_spend
* inform{"category_name": "Cable Assemblies"}
    - slot{"category_name": "Cable Assemblies"}
    - category_spend_form
    - form: followup{"name": "action_category_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup
* askgraph_by_customer
    - action_category_spend_graph_by_customer

## ask graph by bussinesunit
* request_spend{"category_name": "banking", "market_area": "mana", "date": "last year", "month": "2nd Quarter"}
    - slot{"category_name": "banking"}
    - slot{"date": "last year"}
    - slot{"market_area": "mana"}
    - slot{"month": "q2"}
    - action_request_spend
* inform{"category_name": "Banking"}
    - slot{"category_name": "Banking"}
    - category_spend_form
    - form: followup{"name": "action_category_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup
* askgraph_by_businessunit
    - action_category_spend_graph_by_businessunit

## ask graph by market
* request_spend{"category_name": "events", "market_area": "mana", "date": "last year", "month": "December"}
    - slot{"category_name": "events"}
    - slot{"date": "last year"}
    - slot{"market_area": "mana"}
    - slot{"month": "December"}
    - action_request_spend
* inform{"category_name": "Events & Exhibitions"}
    - slot{"category_name": "Events & Exhibitions"}
    - category_spend_form
    - form: followup{"name": "action_category_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup
* askgraph_by_marketarea
    - action_category_spend_graph_by_marketarea
