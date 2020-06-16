
## interactive_story_1
* request_spend{"supplier_name": "american express", "market_area": "mana", "date": "2019"}
    - slot{"date": "2019"}
    - slot{"market_area": "mana"}
    - slot{"supplier_name": "american express"}
    - action_request_spend
* inform{"supplier_name": "AMERICAN EXPRESS"}
    - slot{"supplier_name": "AMERICAN EXPRESS"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup
* request_another{"supplier_name": "amatel"}
    - slot{"supplier_name": "amatel"}
    - action_request_another
* request_category_manager
    - action_request_category_manager
    - form: followup{"name": "action_supplier_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_category_manager_lookup
* request_another{"market_area": "mela"}
    - slot{"market_area": "mela"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_request_another
* request_another{"date": "this year", "market_area": "mana"}
    - slot{"date": "this year"}
    - slot{"market_area": "mana"}
    - action_request_another
* request_another{"category_name": "batteries"}
    - slot{"category_name": "batteries"}
    - action_request_another
* inform{"category_name": "Batteries"}
    - slot{"category_name": "Batteries"}
    - form: followup{"name": "action_category_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup
* request_category_manager
    - action_request_category_manager
    - slot{"category_name": "Batteries"}
    - form: followup{"name": "action_category_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_category_manager_lookup
* request_another{"category_name": "base station", "market_area": "mela"}
    - slot{"category_name": "base station"}
    - slot{"market_area": "mela"}
    - action_request_another
* inform{"category_name": "Base Station Antennas"}
    - slot{"category_name": "Base Station Antennas"}
    - form: followup{"name": "action_category_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_category_manager_lookup
* request_another{"market_area": "moai"}
    - slot{"market_area": "moai"}
    - action_request_another
* request_spend
    - action_request_spend
* inform{"category_name": "Base Station Antennas"}
    - slot{"category_name": "Base Station Antennas"}
    - form: followup{"name": "action_category_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup
* request_another{"supplier_name": "amatel", "market_area": "mana"}
    - slot{"market_area": "mana"}
    - slot{"supplier_name": "amatel"}
    - action_request_another
* inform{"supplier_name": "AMATEL INC"}
    - slot{"supplier_name": "AMATEL INC"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup
* request_another{"date": "last year"}
    - slot{"date": "this year"}
    - action_request_another

## interactive_story_2
* request_spend{"supplier_name": "iweb", "market_area": "mela", "date": "this year"}
    - slot{"date": "this year"}
    - slot{"market_area": "mela"}
    - slot{"supplier_name": "iweb"}
    - action_request_spend
* inform{"supplier_name": "IWEB TECHNOLOGIES INC"}
    - slot{"supplier_name": "IWEB TECHNOLOGIES INC"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup
* request_another{"market_area": "mana"}
    - slot{"market_area": "mana"}
    - form: followup{"name": "action_request_another"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_request_another
* request_another{"supplier_name": "qualcomm"}
    - slot{"supplier_name": "qualcomm"}
    - action_request_another
* request_another{"date": "last year"}
    - slot{"date": "last year"}
    - action_request_another
* request_category_manager
    - action_request_category_manager
    - form: followup{"name": "action_supplier_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_category_manager_lookup
* request_another{"category_name": "arp"}
    - slot{"category_name": "arp"}
    - action_request_another
* request_spend{"date": "last year"}
    - slot{"date": "last year"}
    - action_category_spend_lookup
* request_another{"date": "last year"}
    - slot{"date": "last year"}
    - action_request_another
* request_another{"category_name": "memories"}
    - slot{"category_name": "memories"}
    - action_request_another
* request_another{"date": "this year"}
    - slot{"date": "this year"}
    - action_request_another
* request_another{"supplier_name": "fusion", "date": "last year"}
    - slot{"date": "last year"}
    - slot{"supplier_name": "fusion"}
    - action_request_another

## interactive_story_3
* request_spend{"category_name": "civil work", "market_area": "mela", "date": "2019"}
    - slot{"category_name": "civil work"}
    - slot{"date": "2019"}
    - slot{"market_area": "mela"}
    - action_request_spend
* inform{"category_name": "Civil Work Services"}
    - slot{"category_name": "Civil Work Services"}
    - form: followup{"name": "action_category_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
* request_another{"supplier_name": "fusion", "market_area": "mana"}
    - slot{"market_area": "mana"}
    - slot{"supplier_name": "fusion"}
    - action_request_another
* inform{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup
* askgraph_by_month
    - action_supplier_spend_graph_by_month
