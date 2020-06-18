## get started
* get_started
  - utter_getting_started

## ask_whatspossible
* ask_whatspossible
  - utter_ask_whatspossible

## bot challenge
* bot_challenge
  - utter_iamabot

## ask wolfram 1
* wolframalpha_whatis{"wfquery":"the distance to the moon"}
 - slot{"wfquery":"the distance to the moon"}
 - wolfram_alpha

## ask wolfram 2
* wolframalpha_whatis{"wfquery":"the distance to the sun"}
 - slot{"wfquery":"the distance to the sun"}
 - wolfram_alpha

## ask wolfram 3
* wolframalpha_whatis{"wolframalpha_query": "what is 747 x 76"}
    - wolfram_alpha
* smalltalk_appraisal_thank_you
    - utter_smalltalk_appraisal_thank_you

## ask wolfram 4
* wolframalpha_whatis{"wfquery":"weather in New York city"}
 - slot{"wfquery":"weather in New York city"}
 - wolfram_alpha
    
## ask chart type 1
* askgraph
    - utter_ask_to_graph
* chart_type{"chart_type":"pie"}
    - slot{"chart_type":"pie"}
    - action_supplier_spend_graph 

## ask chart type 2
* askgraph
    - utter_ask_to_graph
* chart_type{"chart_type":"radar"}
    - slot{"chart_type":"radar"}
    - action_category_spend_graph 

## ask chart type 3
* askgraph
    - utter_ask_to_graph
* chart_type{"chart_type":"line"}
    - slot{"chart_type":"line"}
    - action_supplier_spend_graph 

## ask chart type 4
* askgraph
    - utter_ask_to_graph
* chart_type{"chart_type":"bar"}
    - slot{"chart_type":"bar"}
    - action_category_spend_graph 

## ask chart type 5
* askgraph
    - utter_ask_to_graph
* chart_type{"chart_type":"bubble"}
    - slot{"chart_type":"bubble"}
    - action_supplier_spend_graph 

## ask chart type 6
* askgraph
    - utter_ask_to_graph
* chart_type{"chart_type":"polarArea"}
    - slot{"chart_type":"polarArea"}
    - action_category_spend_graph 

## request_months_quarters_1
* request_q_m
    - utter_ask_Q_M
* request_month_info
    - utter_ask_month

## request_months_quarters_2
* request_q_m
    - utter_ask_Q_M
* request_quarter_info
    - utter_ask_quarter
