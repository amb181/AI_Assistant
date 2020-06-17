
## interactive_story_1
* request_category_manager{"category_name": "antennas"}
    - slot{"category_name": "antennas"}
    - action_request_category_manager
    - slot{"supplier_name": null}
    - followup{"name": "category_lookup_for_category_manager"}
    - category_lookup_for_category_manager
* inform{"category_name": "Base Station Antennas"}
    - slot{"category_name": "Base Station Antennas"}
    - category_category_manager_form
    - form{"name": "category_category_manager_form"}
    - slot{"category_name": "Base Station Antennas"}
    - slot{"category_name": "Base Station Antennas"}
    - slot{"requested_slot": "market_area"}
* form: inform{"market_area": "mela"}
    - slot{"market_area": "mela"}
    - form: category_category_manager_form
    - slot{"market_area": "mela"}
    - form: followup{"name": "action_category_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_category_manager_lookup
* request_another{"category_name": "batteries"}
    - slot{"category_name": "batteries"}
    - action_request_another
* request_another{"category_name": "memories"}
    - slot{"category_name": "memories"}
    - action_request_another
* request_another{"category_name": "arp"}
    - slot{"category_name": "arp"}
    - action_request_another

## interactive_story_2
* request_category_manager{"supplier_name": "american express"}
    - slot{"supplier_name": "american express"}
    - action_request_category_manager
    - slot{"category_name": null}
    - followup{"name": "supplier_lookup_for_category_manager"}
    - supplier_lookup_for_category_manager
* inform{"supplier_name": "AMERICAN EXPRESS"}
    - slot{"supplier_name": "AMERICAN EXPRESS"}
    - supplier_category_manager_form
    - form{"name": "supplier_category_manager_form"}
    - slot{"supplier_name": "AMERICAN EXPRESS"}
    - slot{"supplier_name": "AMERICAN EXPRESS"}
    - slot{"requested_slot": "market_area"}
* form: inform{"market_area": "mana"}
    - slot{"market_area": "mana"}
    - form: supplier_category_manager_form
    - slot{"market_area": "mana"}
    - form: followup{"name": "action_supplier_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_category_manager_lookup
* request_another{"supplier_name": "amatel"}
    - slot{"supplier_name": "amatel"}
    - action_request_another
* request_another{"supplier_name": "iweb"}
    - slot{"supplier_name": "iweb"}
    - action_request_another
* request_another{"supplier_name": "fusion"}
    - slot{"supplier_name": "fusion"}
    - action_request_another

## interactive_story_3
* request_supplier_existing{"supplier_name": "american express"}
    - slot{"supplier_name": "american express"}
    - supplier_lookup_for_existing_supplier
* inform{"supplier_name": "AMERICAN EXPRESS"}
    - slot{"supplier_name": "AMERICAN EXPRESS"}
    - supplier_existing_form
    - form{"name": "supplier_existing_form"}
    - slot{"supplier_name": "AMERICAN EXPRESS"}
    - slot{"supplier_name": "AMERICAN EXPRESS"}
    - slot{"requested_slot": "market_area"}
* form: inform{"market_area": "mana"}
    - slot{"market_area": "mana"}
    - form: supplier_existing_form
    - slot{"market_area": "mana"}
    - form: followup{"name": "action_existing_supplier_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_existing_supplier_lookup
* request_another{"supplier_name": "amatel"}
    - slot{"supplier_name": "amatel"}
    - action_request_another
* request_another{"supplier_name": "iweb"}
    - slot{"supplier_name": "iweb"}
    - action_request_another
* request_another{"supplier_name": "fusion"}
    - slot{"supplier_name": "fusion"}
    - action_request_another

## interactive_story_4
* request_supplier_contract{"supplier_name": "american express"}
    - slot{"supplier_name": "american express"}
    - supplier_lookup_for_contract
* inform{"supplier_name": "AMERICAN EXPRESS"}
    - slot{"supplier_name": "AMERICAN EXPRESS"}
    - supplier_contract_form
    - form{"name": "supplier_contract_form"}
    - slot{"supplier_name": "AMERICAN EXPRESS"}
    - slot{"supplier_name": "AMERICAN EXPRESS"}
    - slot{"requested_slot": "market_area"}
* form: inform{"market_area": "mana"}
    - slot{"market_area": "mana"}
    - form: supplier_contract_form
    - slot{"market_area": "mana"}
    - form: followup{"name": "action_supplier_contract_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_contract_lookup
* request_another{"supplier_name": "amatel"}
    - slot{"supplier_name": "amatel"}
    - action_request_another
* request_another{"supplier_name": "iweb"}
    - slot{"supplier_name": "iweb"}
    - action_request_another
* request_another{"supplier_name": "fusion"}
    - slot{"supplier_name": "fusion"}
    - action_request_another
