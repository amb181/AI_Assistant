
## cm_supplier_story_1
* request_category_manager{"supplier_name": "fusion"}
    - slot{"supplier_name": "fusion"}
    - action_request_category_manager
* inform{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - supplier_category_manager_form
    - form{"name": "supplier_category_manager_form"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"requested_slot": "market_area"}
* form: market_area{"market_area": "mana"}
    - slot{"market_area": "mana"}
    - form: supplier_category_manager_form
    - slot{"market_area": "mana"}
    - form: followup{"name": "action_supplier_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_category_manager_lookup

## cm_supplier_story_2
* request_category_manager{"supplier_name": "fusion", "market_area": "mela"}
    - slot{"market_area": "mela"}
    - slot{"supplier_name": "fusion"}
    - action_request_category_manager
* inform{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - supplier_category_manager_form
    - form{"name": "supplier_category_manager_form"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"market_area": "mela"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - form: followup{"name": "action_supplier_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_category_manager_lookup

## cm_supplier_story_3
* request_another{"supplier_name": "amatel"}
    - slot{"supplier_name": "amatel"}
    - action_request_another
    - slot{"requested_slot": "market_area"}
* form: market_area{"market_area": "mana"}
    - slot{"market_area": "mana"}
    - form: category_category_manager_form
    - slot{"market_area": "mana"}
    - form: followup{"name": "action_category_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_category_manager_lookup
* request_spend
    - action_request_spend