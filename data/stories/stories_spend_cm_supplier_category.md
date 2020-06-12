
## interactive_story_1
* request_spend{"supplier_name": "american express", "market_area": "mana", "date": "2019"}
    - slot{"date": "2019"}
    - slot{"market_area": "mana"}
    - slot{"supplier_name": "american express"}
    - action_request_spend
    - slot{"category_name": null}
    - followup{"name": "supplier_lookup"}
    - supplier_lookup
* inform{"supplier_name": "AMERICAN EXPRESS"}
    - slot{"supplier_name": "AMERICAN EXPRESS"}
    - supplier_spend_form
    - form{"name": "supplier_spend_form"}
    - slot{"supplier_name": "AMERICAN EXPRESS"}
    - slot{"market_area": "mana"}
    - slot{"date": "2019"}
    - slot{"supplier_name": "AMERICAN EXPRESS"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup
* request_another_supplier{"supplier_name": "amatel"}
    - slot{"supplier_name": "amatel"}
    - action_request_spend
    - slot{"category_name": null}
    - followup{"name": "supplier_lookup"}
    - supplier_lookup
    - slot{"supplier_name": "AMATEL INC"}
    - followup{"name": "supplier_spend_form"}
    - supplier_spend_form
    - form{"name": "supplier_spend_form"}
    - slot{"supplier_name": "AMATEL INC"}
    - slot{"market_area": "mana"}
    - slot{"date": "2019"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup
* request_category_manager
    - action_request_category_manager
    - slot{"category_name": null}
    - followup{"name": "supplier_lookup_for_category_manager"}
    - supplier_lookup_for_category_manager
    - slot{"supplier_name": "AMATEL INC"}
    - followup{"name": "supplier_category_manager_form"}
    - supplier_category_manager_form
    - form{"name": "supplier_category_manager_form"}
    - slot{"supplier_name": "AMATEL INC"}
    - slot{"market_area": "mana"}
    - form: followup{"name": "action_supplier_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_category_manager_lookup
* request_another_supplier{"market_area": "mela"}
    - slot{"market_area": "mela"}
    - action_request_spend
    - supplier_lookup
    - slot{"supplier_name": "AMATEL INC"}
    - followup{"name": "supplier_spend_form"}
    - supplier_spend_form
    - form{"name": "supplier_spend_form"}
    - slot{"supplier_name": "AMATEL INC"}
    - slot{"market_area": "mela"}
    - slot{"date": "2019"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup
* request_another_supplier{"date": "this year", "market_area": "mana"}
    - slot{"date": "this year"}
    - slot{"market_area": "mana"}
    - action_request_spend
    - supplier_lookup
    - slot{"supplier_name": "AMATEL INC"}
    - followup{"name": "supplier_spend_form"}
    - supplier_spend_form
    - form{"name": "supplier_spend_form"}
    - slot{"supplier_name": "AMATEL INC"}
    - slot{"market_area": "mana"}
    - slot{"date": "this year"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup
* request_another_supplier{"category_name": "batteries"}
    - slot{"category_name": "batteries"}
    - action_request_spend
    - slot{"supplier_name": null}
    - followup{"name": "category_lookup"}
    - category_lookup
    - slot{"category_name": "Batteries"}
    - followup{"name": "category_spend_form"}
    - category_spend_form
    - form{"name": "category_spend_form"}
    - slot{"category_name": "Batteries"}
    - slot{"market_area": "mana"}
    - slot{"date": "this year"}
    - form: followup{"name": "action_category_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup
* request_category_manager
    - action_request_category_manager
    - slot{"supplier_name": null}
    - followup{"name": "category_lookup_for_category_manager"}
    - category_lookup_for_category_manager
    - slot{"category_name": "Batteries"}
    - followup{"name": "category_category_manager_form"}
    - category_category_manager_form
    - form{"name": "category_category_manager_form"}
    - slot{"category_name": "Batteries"}
    - slot{"market_area": "mana"}
    - form: followup{"name": "action_category_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_category_manager_lookup
* request_another_supplier{"category_name": "base station", "market_area": "mela"}
    - slot{"category_name": "base station"}
    - slot{"market_area": "mela"}
    - action_request_category_manager
    - slot{"supplier_name": null}
    - followup{"name": "category_lookup_for_category_manager"}
    - category_lookup_for_category_manager
    - slot{"category_name": "Base Station Antennas"}
    - followup{"name": "category_category_manager_form"}
    - category_category_manager_form
    - form{"name": "category_category_manager_form"}
    - slot{"category_name": "Base Station Antennas"}
    - slot{"market_area": "mela"}
    - form: followup{"name": "action_category_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_category_manager_lookup
* request_another_supplier{"market_area": "moai"}
    - slot{"market_area": "moai"}
    - action_request_category_manager
    - category_lookup_for_category_manager
    - slot{"category_name": "Base Station Antennas"}
    - followup{"name": "category_category_manager_form"}
    - category_category_manager_form
    - form{"name": "category_category_manager_form"}
    - slot{"category_name": "Base Station Antennas"}
    - slot{"market_area": "moai"}
    - form: followup{"name": "action_category_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_category_manager_lookup
* request_spend
    - action_request_spend
    - slot{"supplier_name": null}
    - followup{"name": "category_lookup"}
    - category_lookup
    - slot{"category_name": "Base Station Antennas"}
    - followup{"name": "category_spend_form"}
    - category_spend_form
    - form{"name": "category_spend_form"}
    - slot{"category_name": "Base Station Antennas"}
    - slot{"market_area": "moai"}
    - slot{"date": "this year"}
    - form: followup{"name": "action_category_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup
* request_another_supplier{"supplier_name": "amatel", "market_area": "mana"}
    - slot{"market_area": "mana"}
    - slot{"supplier_name": "amatel"}
    - action_request_spend
    - slot{"category_name": null}
    - followup{"name": "supplier_lookup"}
    - supplier_lookup
    - slot{"supplier_name": "AMATEL INC"}
    - followup{"name": "supplier_spend_form"}
    - supplier_spend_form
    - form{"name": "supplier_spend_form"}
    - slot{"supplier_name": "AMATEL INC"}
    - slot{"market_area": "mana"}
    - slot{"date": "this year"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup
* request_another_date{"date": "last year"}
    - slot{"date": "this year"}
    - action_category_spend_lookup

## interactive_story_2
* request_spend{"supplier_name": "iweb", "market_area": "mela", "date": "this year"}
    - slot{"date": "this year"}
    - slot{"market_area": "mela"}
    - slot{"supplier_name": "iweb"}
    - action_request_spend
    - slot{"category_name": null}
    - followup{"name": "supplier_lookup"}
    - supplier_lookup
    - slot{"supplier_name": "IWEB TECHNOLOGIES INC"}
    - followup{"name": "supplier_spend_form"}
    - supplier_spend_form
    - form{"name": "supplier_spend_form"}
    - slot{"supplier_name": "IWEB TECHNOLOGIES INC"}
    - slot{"market_area": "mela"}
    - slot{"date": "this year"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup
* request_another_supplier{"market_area": "mana"}
    - slot{"market_area": "mana"}
    - action_request_spend
    - supplier_lookup
    - slot{"supplier_name": "IWEB TECHNOLOGIES INC"}
    - followup{"name": "supplier_spend_form"}
    - supplier_spend_form
    - form{"name": "supplier_spend_form"}
    - slot{"supplier_name": "IWEB TECHNOLOGIES INC"}
    - slot{"market_area": "mana"}
    - slot{"date": "this year"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup
* request_another_supplier{"supplier_name": "qualcomm"}
    - slot{"supplier_name": "qualcomm"}
    - action_request_spend
    - slot{"category_name": null}
    - followup{"name": "supplier_lookup"}
    - supplier_lookup
    - slot{"supplier_name": "QUALCOMM TECHNOLOGIES INC."}
    - followup{"name": "supplier_spend_form"}
    - supplier_spend_form
    - form{"name": "supplier_spend_form"}
    - slot{"supplier_name": "QUALCOMM TECHNOLOGIES INC."}
    - slot{"market_area": "mana"}
    - slot{"date": "this year"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup
* request_another_date{"date": "last year"}
    - slot{"date": "last year"}
    - action_supplier_spend_lookup
* request_category_manager
    - action_request_category_manager
    - slot{"category_name": null}
    - followup{"name": "supplier_lookup_for_category_manager"}
    - supplier_lookup_for_category_manager
    - slot{"supplier_name": "QUALCOMM TECHNOLOGIES INC."}
    - followup{"name": "supplier_category_manager_form"}
    - supplier_category_manager_form
    - form{"name": "supplier_category_manager_form"}
    - slot{"supplier_name": "QUALCOMM TECHNOLOGIES INC."}
    - slot{"market_area": "mana"}
    - form: followup{"name": "action_supplier_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_category_manager_lookup
* request_another_supplier{"category_name": "arp"}
    - slot{"category_name": "arp"}
    - action_request_category_manager
    - slot{"supplier_name": null}
    - followup{"name": "category_lookup_for_category_manager"}
    - category_lookup_for_category_manager
    - slot{"category_name": "ARP"}
    - followup{"name": "category_category_manager_form"}
    - category_category_manager_form
    - form{"name": "category_category_manager_form"}
    - slot{"category_name": "ARP"}
    - slot{"market_area": "mana"}
    - form: followup{"name": "action_category_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_category_manager_lookup
* request_spend{"date": "last year"}
    - slot{"date": "last year"}
    - action_request_spend
* request_spend{"date": "last year"}
    - slot{"date": "last year"}
    - action_request_spend
    - category_lookup
    - slot{"category_name": "ARP"}
    - followup{"name": "category_spend_form"}
    - category_spend_form
    - form{"name": "category_spend_form"}
    - slot{"category_name": "ARP"}
    - slot{"market_area": "mana"}
    - slot{"date": "last year"}
    - form: followup{"name": "action_category_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup
* request_another_supplier{"category_name": "memories"}
    - slot{"category_name": "memories"}
    - action_request_spend
    - slot{"supplier_name": null}
    - followup{"name": "category_lookup"}
    - category_lookup
    - slot{"category_name": "Memories"}
    - followup{"name": "category_spend_form"}
    - category_spend_form
    - form{"name": "category_spend_form"}
    - slot{"category_name": "Memories"}
    - slot{"market_area": "mana"}
    - slot{"date": "last year"}
    - form: followup{"name": "action_category_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup
* request_another_date{"date": "this year"}
    - slot{"date": "this year"}
    - action_category_spend_lookup
* request_another_supplier{"supplier_name": "fusion", "date": "last year"}
    - slot{"date": "last year"}
    - slot{"supplier_name": "fusion"}
    - action_request_spend
    - slot{"category_name": null}
    - followup{"name": "supplier_lookup"}
    - supplier_lookup
* inform{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - supplier_category_manager_form
    - form{"name": "supplier_category_manager_form"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"market_area": "mana"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - form: followup{"name": "action_supplier_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_category_manager_lookup

## interactive_story_3
* request_spend{"category_name": "civil work", "market_area": "mela", "date": "2019"}
    - slot{"category_name": "civil work"}
    - slot{"date": "2019"}
    - slot{"market_area": "mela"}
    - action_request_spend
    - slot{"supplier_name": null}
    - followup{"name": "category_lookup"}
    - category_lookup
    - slot{"category_name": "Civil Work Services"}
    - followup{"name": "category_spend_form"}
    - category_spend_form
    - form{"name": "category_spend_form"}
    - slot{"category_name": "Civil Work Services"}
    - slot{"market_area": "mela"}
    - slot{"date": "2019"}
    - form: followup{"name": "action_category_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup
* request_another_supplier{"supplier_name": "fusion", "market_area": "mana"}
    - slot{"market_area": "mana"}
    - slot{"supplier_name": "fusion"}
    - action_request_spend
    - slot{"category_name": null}
    - followup{"name": "supplier_lookup"}
    - supplier_lookup
* inform{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - supplier_spend_form
    - form{"name": "supplier_spend_form"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"market_area": "mana"}
    - slot{"date": "2019"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup
* askgraph_by_month
    - action_supplier_spend_graph_by_month