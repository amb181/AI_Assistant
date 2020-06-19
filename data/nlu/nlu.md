## intent:ask_whatspossible
- What are my options
- What are you able to do
- What can I ask you
- What can you do
- What can you do for me
- What can you do
- What can you tell me
- What do you do
- how can i use you
- how can you help me
- how can you help me
- how can you help
- how does this work
- how u can help me
- how you help me
- now what
- options
- show me the menu
- show me what's possible
- so now what
- so what can you do
- so what can you do
- so what can you help me with
- so what next
- um what now
- what are all the things you understand
- what can u do
- what can we talk about
- what can you answer
- what can you do
- what do you do
- what do you do
- what else can I do here
- what else can i do
- what else can i do
- What are your limiation

## intent:bot_challenge
- are you a human
- am I talking to a bot
- am I talking to a human

## intent:date
- [This year]{"entity": "date", "value": "this year"}
- [Last Year]{"entity": "date", "value": "last year"}
- [ALL Years]{"entity": "date", "value": "all years"}

## intent:month
- [January](month)
- [February](month)
- [March](month)
- [April](month)
- [May](month)
- [June](month)
- [July](month)
- [August](month)
- [September](month)
- [October](month)
- [November](month)
- [December](month)
- [Jan]{"entity": "month", "value": "january"}
- [Feb]{"entity": "month", "value": "february"}
- [Mar]{"entity": "month", "value": "march"}
- [Apr]{"entity": "month", "value": "april"}
- [Jun]{"entity": "month", "value": "june"}
- [Jul]{"entity": "month", "value": "july"}
- [Aug]{"entity": "month", "value": "august"}
- [Sep]{"entity": "month", "value": "september"}
- [Oct]{"entity": "month", "value": "october"}
- [Nov]{"entity": "month", "value": "november"}
- [Dec]{"entity": "month", "value": "december"}
- [last month](month)
- [this month](month)
- [1st quarter]{"entity": "month", "value": "q1"}
- [2nd quarter]{"entity": "month", "value": "q2"}
- [3rd quarter]{"entity": "month", "value": "q3"}
- [4th quarter]{"entity": "month", "value": "q4"}
- [Q1](month)
- [q2](month)
- [Q3](month)
- [q4](month)
- [this quarter](month)
- [last quarter](month)

## intent:askgraph
- show me the graph
- can i see a graph
- could you please create a graph
- show me the chart
- pie chart please

## intent:askgraph_by_month
- show me by month
- can i see by month
- can you show me by month
- per month

## intent:askgraph_by_quarter
- show me by quarter
- can i see by quarter
- can you show me by quarter
- per quarter

## intent:askgraph_by_supplier
- show me by supplier
- can i see by supplier
- can you show me by supplier
- per supplier

## intent:askgraph_by_company
- show me by company
- can i see by company
- can you show me by company
- per company

## intent:askgraph_by_customer
- show me by customer
- can i see by customer
- can you show me by customer
- per customer

## intent:askgraph_by_businessunit
- show me by business
- can i see by business unit
- can you show me by business
- per business unit

## intent:askgraph_by_marketarea
- show me by market
- show me by market area
- show me by MA
- can i see by market
- can i see it by MA
- can i see by market area
- can you show me by market area
- can you show me by MA
- per market
- per market area
- per MA

## intent:askgraph_by_category
- show me by category
- can i see by category
- can you show me by category

## intent:chart_type
- [pie](chart_type)
- [radar](chart_type)
- [line](chart_type)
- [bar](chart_type)
- [bubble](chart_type)
- [porlarArea](chart_type)

## lookup:supplier_name
data/lookup-tables/suppliers.txt

## regex:supplier_name
- [a-zA-Z]

## lookup:category_name
data/lookup-tables/categories.txt

## regex:category_name
- [a-zA-Z]

## intent:request_supplier_onboarding_status
- What is the onboarding status for [microsoft](supplier_name)
- What is the onboarding status for [apple](supplier_name)

## intent:inform
- [HP Inc](supplier_name)
- [Fusion Solutions Inc](supplier_name)
- [Amatel](supplier_name)
- [plano](weather_location)
- [dallas](weather_location)
- [ALL](market_area)

## intent:out_of_scope
- i can't deal with _your_ request
- i mean something else
- something else