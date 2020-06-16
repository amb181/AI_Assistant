## existing_story_1
* request_supplier_existing{"supplier_name": "fusion"}
    - slot{"supplier_name": "fusion"}
    - supplier_lookup_for_existing_supplier
* inform{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - supplier_existing_form
    - form{"name": "supplier_existing_form"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"requested_slot": "market_area"}
* form: market_area{"market_area": "mana"}
    - slot{"market_area": "mana"}
    - form: supplier_existing_form
    - slot{"market_area": "mana"}
    - form: followup{"name": "action_existing_supplier_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_existing_supplier_lookup


## existing_story_2
* request_supplier_existing{"supplier_name": "amatel"}
    - slot{"supplier_name": "amatel"}
    - supplier_lookup_for_existing_supplier
    - slot{"supplier_name": "AMATEL INC"}
    - followup{"name": "supplier_existing_form"}
    - supplier_existing_form
    - form{"name": "supplier_existing_form"}
    - slot{"supplier_name": "AMATEL INC"}
    - slot{"requested_slot": "market_area"}
* form: market_area{"market_area": "mana"}
    - slot{"market_area": "mana"}
    - form: supplier_existing_form
    - slot{"market_area": "mana"}
    - form: followup{"name": "action_existing_supplier_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_existing_supplier_lookup

## existing_story_3
* request_supplier_existing{"supplier_name": "amatel", "market_area": "mela"}
    - slot{"market_area": "mela"}
    - slot{"supplier_name": "amatel"}
    - supplier_lookup_for_existing_supplier
    - slot{"supplier_name": "AMATEL INC"}
    - followup{"name": "supplier_existing_form"}
    - supplier_existing_form
    - form{"name": "supplier_existing_form"}
    - slot{"supplier_name": "AMATEL INC"}
    - slot{"market_area": "mela"}
    - form: followup{"name": "action_existing_supplier_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_existing_supplier_lookup
* request_another{"supplier_name": "fusion"}
    - slot{"supplier_name": "fusion"}
    - action_request_another