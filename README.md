# GenericRestJDE
Generic REST server for JDEdwars.

## Architecture
```PlantUML
@startditaa
+---------+      +---------+      +---------+      +---------+
|cBLU     |      | c1FF    |      |cYEL     |      |cGRE     |
|         |      |         |      |         |  Y   |         |
| Request +----->|  Query  +----->| Success +----->|  Data   |
|         |      |         |      |         |      |         |
| {d}     |      |         |      | {c}     |      | {d}     |
+---------+      +---+-----+      +----+----+      +---------+
                     | ^               | 
                     : :               | N
                     V |               V
                 +-----+---+      +---------+
                 |cAAA     |      |cRED     |
                 |         |      |         |
                 | Oracle  |      | Errors  |
                 |         |      |         |
                 |     {s} |      | {d}     |
                 +---------+      +---------+
@endditaa
```

## JSON Data Structure

>
>### Request GET
>>```PlantUML
>>@startjson
>>{
>>  "object": "F4101",
>>  "filter": [
>>    {
>>      "operator": "=",
>>      "term1": "TAB.IMPRP1",
>>      "term2": "A01"
>>    },
>>    {
>>      "operator": "AND",
>>      "term1": null,
>>      "term2": null
>>    },
>>    {
>>      "operator": "=",
>>      "term1": "TAB.IMPRP2",
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
>>```SQLdotnetcli
>>SELECT
>>    IMITM,
>>    IMDSC1,
>>    IMDSC2
>>FROM
>>    F4101
>>WHERE
>>    IMPRP1 = "A01" AND
>>    IMPRP2 = "B01"
>>ORDER BY
>>    IMITM ASC
>>```
>>
>>```PlantUML
>>@startjson
>>{
>>  "object": "F4101",
>>  "filter": [
>>    {
>>      "operator": "(",
>>      "term1": null,
>>      "term2": null
>>    },
>>    {
>>      "operator": "=",
>>      "term1": "TAB.IMPRP1",
>>      "term2": "A01"
>>    },
>>    {
>>      "operator": "OR",
>>      "term1": null,
>>      "term2": null
>>    },
>>    {
>>      "operator": "=",
>>      "term1": "TAB.IMPRP1",
>>      "term2": "A02"
>>    },
>>    {
>>      "operator": ")",
>>      "term1": null,
>>      "term2": null
>>    },
>>    {
>>      "operator": "AND",
>>      "term1": null,
>>      "term2": null
>>    },
>>    {
>>      "operator": "=",
>>      "term1": "TAB.IMPRP2",
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
>>```SQLdotnetcli
>>SELECT
>>    IMITM,
>>    IMDSC1,
>>    IMDSC2
>>FROM
>>    F4101
>>WHERE
>>    (IMPRP1 = "A01" OR
>>    IMPRP1 = "A02) AND
>>    IMPRP2 = "B01"
>>ORDER BY
>>    IMITM ASC
>>```
>>
>> **Types of operator:**
>>| Option 	|       Description       	|
>>|--------	|:-----------------------:	|
>>| (      	|  _Open a operation group_ 	|
>>| )      	| _Close a operation group_ 	|
>>| AND    	|       _AND operator_      	|
>>| OR     	|       _OR operator_       	|
>>| NOT    	|       _NOT operator_      	|
>>| =      	|           _equal_         	|
>>| !=     	|         _different_       	|
>>| <=     	|     _less or equal_       	|
>>| >=     	|    _great or equal_       	|
>>| >      	|          _great_          	|
>>| <      	|          _less_           	|
>>| IN     	|        _inbound_          	|
>>| NOT IN 	|        _outbound_         	|
>_
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