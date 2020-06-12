## supplier_spend_story_1
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

## supplier_spend_story_2
* request_spend{"supplier_name": "fusion", "market_area": "mana"}
    - slot{"market_area": "mana"}
    - slot{"supplier_name": "fusion"}
    - action_request_spend
* inform{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - supplier_spend_form
    - form{"name": "supplier_spend_form"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"market_area": "mana"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"requested_slot": "date"}
* form: date{"date": "last year"}
    - slot{"date": "last year"}
    - form: supplier_spend_form
    - slot{"date": "last year"}
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
    - supplier_spend_form
    - form{"name": "supplier_spend_form"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"date": "last year"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"requested_slot": "market_area"}
* form: market_area{"market_area": "mana"}
    - slot{"market_area": "mana"}
    - form: supplier_spend_form
    - slot{"market_area": "mana"}
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
    - form{"name": "supplier_spend_form"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - slot{"market_area": "mana"}
    - slot{"date": "last year"}
    - slot{"supplier_name": "FUSION TECHNICAL SOLUTIONS LLC"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_supplier_spend_lookup