## supplier_spend_story_1
* request_spend{"supplier_name": "fusion"}
    - slot{"supplier_name": "fusion"}
    - action_request_spend
* inform{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"requested_slot": "market_area"}
* form: market_area{"market_area": "mana"}
    - slot{"market_area": "mana"}
    - supplier_spend_form
    - slot{"requested_slot": "date"}
* form: date{"date": "last year"}
    - slot{"date": "last year"}
    - supplier_spend_form
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup

## supplier_spend_story_2
* request_spend{"supplier_name": "fusion", "market_area": "mana"}
    - slot{"market_area": "mana"}
    - slot{"supplier_name": "fusion"}
    - action_request_spend
* inform{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"requested_slot": "date"}
* form: date{"date": "last year"}
    - slot{"date": "last year"}
    - supplier_spend_form
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup

## supplier_spend_story_3
* request_spend{"supplier_name": "fusion", "date": "last year"}
    - slot{"date": "last year"}
    - slot{"supplier_name": "fusion"}
    - action_request_spend
* inform{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"requested_slot": "market_area"}
* form: market_area{"market_area": "mana"}
    - slot{"market_area": "mana"}
    - supplier_spend_form
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup

## supplier_spend_story_4
* request_spend{"supplier_name": "fusion", "market_area": "mana", "date": "last year"}
    - slot{"date": "last year"}
    - slot{"market_area": "mana"}
    - slot{"supplier_name": "fusion"}
    - action_request_spend
* inform{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - supplier_spend_form
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup
* request_another{"supplier_name": "american express"}
    - slot{"supplier_name": "american express"}
    - action_request_another
* request_another{"supplier_name": "iweb"}
    - slot{"supplier_name": "iweb"}
    - action_request_another
* request_another{"supplier_name": "oracle"}
    - slot{"supplier_name": "oracle"}
    - action_request_another


## ask graph by month
* request_spend{"supplier_name": "infinite", "market_area": "mela", "date": "this year"}
    - slot{"date": "this year"}
    - slot{"market_area": "mela"}
    - slot{"supplier_name": "infinite"}
    - action_request_spend
* inform{"supplier_name": "INFINITE ELECTRONICS INTERNATIONAL"}
    - slot{"supplier_name": "INFINITE ELECTRONICS INTERNATIONAL"}
    - supplier_spend_form
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup
* askgraph_by_month
    - action_supplier_spend_graph_by_month

## ask graph by customer
* request_spend{"supplier_name": "pasternack", "market_area": "moai", "date": "2019"}
    - slot{"date": "2019"}
    - slot{"market_area": "moai"}
    - slot{"supplier_name": "pasternack"}
    - action_request_spend
* inform{"supplier_name": "PASTERNACK ENTERPRISES LLC"}
    - slot{"supplier_name": "PASTERNACK ENTERPRISES LLC"}
    - supplier_spend_form
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup
* askgraph_by_customer
    - action_supplier_spend_graph_by_customer

## ask graph by company
* request_spend{"supplier_name": "visualon", "market_area": "mmea", "date": "2020"}
    - slot{"date": "2020"}
    - slot{"market_area": "mmea"}
    - slot{"supplier_name": "visualon"}
    - action_request_spend
* inform{"supplier_name": "VISUALON INC"}
    - slot{"supplier_name": "VISUALON INC"}
    - supplier_spend_form
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup
* askgraph_by_company
    - action_supplier_spend_graph_by_company

## ask graph by market
* request_spend{"supplier_name": "elster", "market_area": "mnea", "date": "last year"}
    - slot{"date": "last year"}
    - slot{"market_area": "mnea"}
    - slot{"supplier_name": "elster"}
    - action_request_spend
* inform{"supplier_name": "ELSTER SOLUTIONS LLC"}
    - slot{"supplier_name": "ELSTER SOLUTIONS LLC"}
    - supplier_spend_form
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup
* askgraph_by_marketarea
    - action_supplier_spend_graph_by_marketarea

## ask graph by businessunit
* request_spend{"supplier_name": "datasafe", "market_area": "mmea", "date": "last year"}
    - slot{"date": "last year"}
    - slot{"market_area": "mmea"}
    - slot{"supplier_name": "datasafe"}
    - action_request_spend
* inform{"supplier_name": "DATASAFE INC"}
    - slot{"supplier_name": "DATASAFE INC"}
    - supplier_spend_form
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup
* askgraph_by_businessunit
    - action_supplier_spend_graph_by_businessunit