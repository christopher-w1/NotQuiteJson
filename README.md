# Not Quite JSON
**A simple and tolerant parser for data in JSON-Format and also for data that is similar, but ultimatively incompatible.**

## What does this parser do?
This parser will try to convert data that contains of key-value-pairs inside curly brackets seperated by ':' and ',' 
as well as list items in square brackets seperated by ',' as python data. It does not care about the kind of quotes being used for values 
or about keys being a certain data structure.
Alpha-Numeric characters will be interpreted as strings and in case they are values, automatically converted to integers, bools or None.

## What does this parser not do?
This parser won't be able to magically fix a clusterfuck of mismatched brackets. 


## Usage example

```py
data_string1 = "{'REID': 2, 'RNUM': 200, 'RESPONSE': 'OK', 'PAYL': { 'metrics': None }}"
data_string2 = "{REID: 2, 'RNUM': 200, 'RESPONSE': 'OK'}"
data_string3 = "{'DATA': {val1: a, val2: {}, val3: [10, 12, 13e]}, 'ONLINE': TrUe}"
ps = NotQuiteJson()
result = ps.parseIter(data_string1)
print("Result: ", result)

>>Result:  {'REID': 2, 'RNUM': 200, 'RESPONSE': 'OK', 'PAYL': {'metrics': None}}```


