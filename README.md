# GenericRestJDE
Generic REST server for JDEdwars.

## Architecture
```PlantUML
@startditaa
+---------+      +---------+      +---------+      +---------+
|         |      |         |      |         |  Y   |         |
| Request +----->|  Query  +----->| Success +----->|  Data   |
| {d}     |      |         |      | {c}     |      | {d}     |
+---------+      +---+-----+      +----+----+      +---------+
                     | ^               | 
                     : :               | N
                     V |               V
                 +-----+---+      +---------+
                 |   {s}   |      |         |
                 |   JDE   |      | Errors  |
                 |         |      | {d}     |
                 +---------+      +---------+
@endditaa
```

## JSON Data Structure

>
>### Request
>>```PlantUML
>>@startjson
>>{
>>  "object": "F4101",
>>  "filter": [
>>    {
>>      "operator": "=",
>>      "term1": "IMPRP1",
>>      "term2": "A01"
>>    },
>>    {
>>      "operator": "AND",
>>      "term1": null,
>>      "term2": null
>>    },
>>    {
>>      "operator": "=",
>>      "term1": "IMPRP2",
>>      "term2": "B01"
>>    }
>>  ],
>>  "order": [
>>    {
>>      "colunm": "IMITM",
>>      "sort": "A"
>>    }
>>  ],
>>  "data": [
>>    "IMITM",
>>    "IMDSC1",
>>    "IMDSC2"
>>  ]
>>}
>>@endjson
>>```
>>
>>```PlantUML
>>@startjson
>>{
>>  "object": "F4101",
>>  "filter": [
>>    {
>>      "connection": "(",
>>      "option":
>>        {
>>          "colunm": "IMPRP1",
>>          "operator": "=",
>>          "value": "A01"
>>        }
>>    },
>>    {
>>      "connection": "OR",
>>      "option":
>>        {
>>          "colunm": "IMPRP1",
>>          "operator": "=",
>>          "value": "A02"
>>        }
>>    },
>>    {
>>      "connection": ")",
>>      "option": null
>>    },
>>    {
>>      "connection": "AND",
>>      "option":
>>        {
>>          "colunm": "IMPRP2",
>>          "operator": "=",
>>          "value": "B01"
>>        }
>>    }
>>  ],
>>  "order": [
>>    {
>>      "colunm": "IMITM",
>>      "sort": "A"
>>    }
>>  ],
>>  "data": [
>>    "IMITM",
>>    "IMDSC1",
>>    "IMDSC2"
>>  ]
>>}
>>@endjson
>>```
>>
>> **Types of connections:**
>>| Option 	|       Description       	|
>>|--------	|:-----------------------:	|
>>| (      	|  Open a operation group 	|
>>| )      	| Close a operation group 	|
>>| AND    	|       AND operator      	|
>>| OR     	|       OR operator       	|
>>| NOT    	|       NOT operator      	|
>
>### Error
>>```PlantUML
>>@startjson
>>{
>>  "error": [
>>    {
>>      "number": 12,
>>      "text": "No values returned."
>>    },
>>    {
>>      "number": 99,
>>      "text": "Revise your request."
>>    }
>>  ]
>>}
>>@endjson
>>```
>
>### Data
>>```PlantUML
>>@startjson
>>{
>>  "statistic": {
>>    "TimeStamp": "2012-04-23T18:25:43.511Z",
>>    "TimeElapsed": 0.00112
>>  },
>>  "data": [
>>    {
>>      "IMITM": 123,
>>      "IMDSC1": "ITEM ONE",
>>      "IMDSC2": "First Item"
>>    },
>>    {
>>      "IMITM": 234,
>>      "IMDSC1": "ITEM TWO",
>>      "IMDSC2": "Second item"
>>    },
>>    {
>>      "IMITM": 345,
>>      "IMDSC1": "ITEM THREE",
>>      "IMDSC2": "Third item"
>>    }
>>  ]
>>}
>>@endjson
>>```
>