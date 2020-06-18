
## interactive_story_1
* request_spend{"supplier_name": "wipro"}
    - slot{"supplier_name": "wipro"}
    - action_request_spend
    - slot{"category_name": null}
    - followup{"name": "supplier_lookup"}
    - supplier_lookup
* inform{"supplier_name": "Wipro Ltd"}
    - slot{"supplier_name": "Wipro Ltd"}
    - supplier_spend_form
    - form{"name": "supplier_spend_form"}
    - slot{"supplier_name": "Wipro Ltd"}
    - slot{"supplier_name": "Wipro Ltd"}
    - slot{"requested_slot": "market_area"}
* form: market_area{"market_area": "mana"}
    - slot{"market_area": "mana"}
    - form: supplier_spend_form
    - slot{"market_area": "mana"}
    - slot{"requested_slot": "date"}
* form: date{"date": "all years"}
    - slot{"date": "all years"}
    - form: supplier_spend_form
    - slot{"date": "all years"}
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
* askgraph_by_category
    - action_supplier_spend_graph_by_category

## ask graph for category
* askgraph_by_category
    - action_supplier_spend_graph_by_category
