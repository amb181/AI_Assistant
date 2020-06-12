
## interactive_story_1
* request_spend{"category_name": "batteries"}
    - slot{"category_name": "batteries"}
    - action_request_spend
    - slot{"category_name": "Batteries"}
    - followup{"name": "category_spend_form"}
    - category_spend_form
    - form{"name": "category_spend_form"}
    - slot{"category_name": "Batteries"}
    - slot{"requested_slot": "market_area"}
* form: market_area{"market_area": "mana"}
    - slot{"market_area": "mana"}
    - form: category_spend_form
    - slot{"market_area": "mana"}
    - slot{"requested_slot": "date"}
* form: date{"date": "last year"}
    - slot{"date": "last year"}
    - form: category_spend_form
    - slot{"date": "last year"}
    - form: followup{"name": "action_supplier_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup

## interactive_story_2
* request_spend{"category_name": "batteries", "market_area": "mana"}
    - slot{"category_name": "batteries"}
    - slot{"market_area": "mana"}
    - action_request_spend
    - slot{"category_name": "Batteries"}
    - followup{"name": "category_spend_form"}
    - category_spend_form
    - form{"name": "category_spend_form"}
    - slot{"category_name": "Batteries"}
    - slot{"market_area": "mana"}
    - slot{"requested_slot": "date"}
* form: date{"date": "last year"}
    - slot{"date": "last year"}
    - form: category_spend_form
    - slot{"date": "last year"}
    - form: followup{"name": "action_category_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup

## interactive_story_3
* request_spend{"category_name": "batteries", "date": "last year"}
    - slot{"category_name": "batteries"}
    - slot{"date": "last year"}
    - action_request_spend
    - slot{"category_name": "Batteries"}
    - followup{"name": "category_spend_form"}
    - category_spend_form
    - form{"name": "category_spend_form"}
    - slot{"category_name": "Batteries"}
    - slot{"date": "last year"}
    - slot{"requested_slot": "market_area"}
* form: market_area{"market_area": "mana"}
    - slot{"market_area": "mana"}
    - form: category_spend_form
    - slot{"market_area": "mana"}
    - form: followup{"name": "action_category_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup

## interactive_story_4
* request_spend{"category_name": "batteries", "market_area": "mana", "date": "last year"}
    - slot{"category_name": "batteries"}
    - slot{"date": "last year"}
    - slot{"market_area": "mana"}
    - action_request_spend
    - slot{"category_name": "Batteries"}
    - followup{"name": "category_spend_form"}
    - category_spend_form
    - form{"name": "category_spend_form"}
    - slot{"category_name": "Batteries"}
    - slot{"market_area": "mana"}
    - slot{"date": "last year"}
    - form: followup{"name": "action_category_spend_lookup"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_category_spend_lookup