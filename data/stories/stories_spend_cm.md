
## category spend | later supplier category manager
* request_spend{"category_name": "arp", "market_area": "mana"}
    - slot{"category_name": "arp"}
    - slot{"market_area": "mana"}
    - action_request_spend
    - followup{"name": "category_lookup"}
    - category_lookup
    - slot{"category_name": "ARP"}
    - followup{"name": "category_spend_form"}
    - category_spend_form
    - form{"name": "category_spend_form"}
    - slot{"category_name": "ARP"}
    - slot{"market_area": "mana"}
    - slot{"requested_slot": "date"}
* form: date{"date": "last year"}
    - slot{"date": "last year"}
    - category_spend_form
    - slot{"date": "last year"}
    - form: followup{"name": "action_category_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup
* request_category_manager{"supplier_name": "american express", "market_area": "mela"}
    - slot{"market_area": "mela"}
    - slot{"supplier_name": "american express"}
    - action_request_category_manager
    - followup{"name": "supplier_lookup_for_category_manager"}
    - supplier_lookup_for_category_manager
* inform{"supplier_name": "AMERICAN EXPRESS"}
    - slot{"supplier_name": "AMERICAN EXPRESS"}
    - supplier_category_manager_form
    - form{"name": "supplier_category_manager_form"}
    - slot{"supplier_name": "AMERICAN EXPRESS"}
    - slot{"market_area": "mela"}
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
    - slot{"category_name": null}
    - followup{"name": "supplier_lookup"}
    - supplier_lookup
    - slot{"supplier_name": "AMATEL INC"}
    - followup{"name": "supplier_spend_form"}
    - supplier_spend_form
    - form{"name": "supplier_spend_form"}
    - slot{"supplier_name": "AMATEL INC"}
    - slot{"market_area": "mana"}
    - slot{"requested_slot": "date"}
* form: date{"date": "last year"}
    - slot{"date": "last year"}
    - supplier_spend_form
    - slot{"date": "last year"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup
* request_another_supplier{"category_name": "arp"}
    - slot{"category_name": "arp"}
    - action_request_spend
    - slot{"supplier_name": null}
    - followup{"name": "category_lookup"}
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
* request_another_date{"date": "last year"}
    - slot{"date": "last year"}
    - action_supplier_spend_lookup
* request_category_manager
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
* request_another_supplier{"supplier_name": "amatel", "market_area": "mela"}
    - slot{"market_area": "mela"}
    - slot{"supplier_name": "amatel"}
    - action_request_category_manager
    - slot{"category_name": null}
    - followup{"name": "supplier_lookup_for_category_manager"}
    - supplier_lookup_for_category_manager
    - slot{"supplier_name": "AMATEL INC"}
    - followup{"name": "supplier_category_manager_form"}
    - supplier_category_manager_form
    - form{"name": "supplier_category_manager_form"}
    - slot{"supplier_name": "AMATEL INC"}
    - slot{"market_area": "mela"}
    - form: followup{"name": "action_supplier_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_category_manager_lookup


## supplier category manager | later supplier spend | later another marker with date

* request_category_manager{"supplier_name": "american express", "market_area": "mela"}
    - slot{"market_area": "mela"}
    - slot{"supplier_name": "american express"}
    - action_request_category_manager
    - followup{"name": "supplier_lookup_for_category_manager"}
    - supplier_lookup_for_category_manager
* inform{"supplier_name": "AMERICAN EXPRESS"}
    - slot{"supplier_name": "AMERICAN EXPRESS"}
    - supplier_category_manager_form
    - form{"name": "supplier_category_manager_form"}
    - slot{"supplier_name": "AMERICAN EXPRESS"}
    - slot{"market_area": "mela"}
    - slot{"supplier_name": "AMERICAN EXPRESS"}
    - form: followup{"name": "action_supplier_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_category_manager_lookup
* request_spend
    - action_request_spend
    - followup{"name": "supplier_spend_form"}
    - supplier_spend_form
    - form{"name": "supplier_spend_form"}
    - slot{"requested_slot": "date"}
* form: date{"date": "last year"}
    - slot{"date": "last year"}
    - supplier_spend_form
    - slot{"date": "last year"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup
* form: request_another_date{"date": "last year", "market_area": "mana"}
    - slot{"date": "last year"}
    - slot{"market_area": "mana"}
    - action_supplier_spend_lookup
* askgraph_by_month
    - action_supplier_spend_graph_by_month


## category category manager | later category spend | later another marker with date

* request_category_manager{"category_name": "server", "market_area": "mela"}
    - slot{"market_area": "mela"}
    - slot{"category_name": "server"}
    - action_request_category_manager
    - followup{"name": "category_lookup_for_category_manager"}
    - category_lookup_for_category_manager
* inform{"category_name": "Server & Storage"}
    - slot{"category_name": "Server & Storage"}
    - category_category_manager_form
    - form{"name": "category_category_manager_form"}
    - slot{"category_name": "Server & Storage"}
    - slot{"market_area": "mela"}
    - slot{"category_name": "Server & Storage"}
    - form: followup{"name": "action_category_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_category_manager_lookup
* request_spend
    - action_request_spend
    - followup{"name": "category_spend_form"}
    - category_spend_form
    - form{"name": "category_spend_form"}
    - slot{"requested_slot": "date"}
* form: date{"date": "last year"}
    - slot{"date": "last year"}
    - category_spend_form
    - slot{"date": "last year"}
    - form: followup{"name": "action_category_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup
* form: request_another_date{"date": "last year", "market_area": "mana"}
    - slot{"date": "last year"}
    - slot{"market_area": "mana"}
    - action_category_spend_lookup
* askgraph_by_month
    - action_category_spend_graph_by_month

## category category manager | later supplier spend | later another marker with date

* request_category_manager{"category_name": "server", "market_area": "mela"}
    - slot{"market_area": "mela"}
    - slot{"category_name": "server"}
    - action_request_category_manager
    - followup{"name": "category_lookup_for_category_manager"}
    - category_lookup_for_category_manager
* inform{"category_name": "Server & Storage"}
    - slot{"category_name": "Server & Storage"}
    - category_category_manager_form
    - form{"name": "category_category_manager_form"}
    - slot{"category_name": "Server & Storage"}
    - slot{"market_area": "mela"}
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
    - supplier_existing_form
    - form{"name": "supplier_existing_form"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"requested_slot": "market_area"}
* market_area{"market_area": "mana"}
    - slot{"market_area": "mana"}
    - supplier_spend_form
    - form{"name": "supplier_spend_form"}
    - action_listen
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"market_area": "mana"}
    - slot{"market_area": "mana"}
    - slot{"requested_slot": "date"}
* form: date{"date": "last year"}
    - slot{"date": "last year"}
    - supplier_spend_form
    - slot{"date": "last year"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup
* askgraph_by_customer
    - action_supplier_spend_graph_by_month