
## cm_category_story_1
* request_category_manager{"category_name": "batteries", "market_area": "mela"}
    - slot{"category_name": "batteries"}
    - slot{"market_area": "mela"}
    - action_request_category_manager
    - followup{"name": "category_lookup_for_category_manager"}
    - category_lookup_for_category_manager
    - slot{"category_name": "Batteries"}
    - followup{"name": "category_category_manager_form"}
    - category_category_manager_form
    - form{"name": "category_category_manager_form"}
    - slot{"category_name": "Batteries"}
    - slot{"market_area": "mela"}
    - form: followup{"name": "action_category_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_category_manager_lookup

## cm_category_story_2
* request_category_manager{"category_name": "batteries"}
    - slot{"category_name": "batteries"}
    - action_request_category_manager
    - followup{"name": "category_lookup_for_category_manager"}
    - category_lookup_for_category_manager
    - slot{"category_name": "Batteries"}
    - followup{"name": "category_category_manager_form"}
    - category_category_manager_form
    - form{"name": "category_category_manager_form"}
    - slot{"category_name": "Batteries"}
    - slot{"requested_slot": "market_area"}
* form: market_area{"market_area": "mela"}
    - slot{"market_area": "mela"}
    - form: category_category_manager_form
    - slot{"market_area": "mela"}
    - form: followup{"name": "action_category_category_manager_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_category_manager_lookup


<!-- REQUEST ANOTHER FOR CATEGORY -->
## cm_category_story_3
* request_another_supplier{"category_name": "arp"}
    - slot{"category_name": "arp"}
    - action_request_category_manager
    - followup{"name": "category_lookup_for_category_manager"}
    - category_lookup_for_category_manager
    - slot{"category_name": "ARP"}
    - followup{"name": "category_category_manager_form"}
    - category_category_manager_form
    - form{"name": "category_category_manager_form"}
    - slot{"category_name": "ARP"}
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
    - followup{"name": "category_lookup"}