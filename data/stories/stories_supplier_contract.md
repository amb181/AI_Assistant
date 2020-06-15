## contract_story_1
* request_supplier_contract{"supplier_name": "fusion"}
    - slot{"supplier_name": "fusion"}
    - supplier_lookup_for_contract
* inform{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"requested_slot": "market_area"}
* form: market_area{"market_area": "mana"}
    - slot{"market_area": "mana"}
    - form: followup{"name": "action_supplier_contract_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_contract_lookup

## contract_story_2
* request_supplier_contract{"supplier_name": "fusion", "market_area": "mana"}
    - slot{"market_area": "mana"}
    - slot{"supplier_name": "fusion"}
    - supplier_lookup_for_contract
* inform{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - form: followup{"name": "action_supplier_contract_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_contract_lookup

## contract_story_3
* request_supplier_contract{"supplier_name": "amatel"}
    - slot{"supplier_name": "amatel"}
    - supplier_lookup_for_contract
* inform{"supplier_name": "AMATEL INC"}
    - slot{"supplier_name": "AMATEL INC"}
    - slot{"requested_slot": "market_area"}
* form: market_area{"market_area": "mana"}
    - slot{"market_area": "mana"}
    - form: followup{"name": "action_supplier_contract_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_contract_lookup

## contract_story_4
* request_supplier_contract{"supplier_name": "amatel", "market_area": "mana"}
    - slot{"market_area": "mana"}
    - slot{"supplier_name": "amatel"}
    - supplier_lookup_for_contract
* inform{"supplier_name": "AMATEL INC"}
    - slot{"supplier_name": "AMATEL INC"}
    - slot{"supplier_name": "AMATEL INC"}
    - form: followup{"name": "action_supplier_contract_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_contract_lookup
