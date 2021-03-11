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
>>      "colunm": "TAB.IMITM",
>>      "sort": "A"
>>    }
>>  ],
>>  "data": [
>>    {
>>      "TAB.IMITM": null,
>>      "TAB.IMDSC1": null,
>>      "TAB.IMDSC2": null
>>    }
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
>>      "colunm": "TAB.IMITM",
>>      "sort": "A"
>>    }
>>  ],
>>  "data": [
>>    {
>>      "TAB.IMITM": null,
>>      "TAB.IMDSC1": null,
>>      "TAB.IMDSC2": null
>>    }
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
>### Request POST (Update)
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
>>      "colunm": "TAB.IMITM",
>>      "sort": "A"
>>    }
>>  ],
>>  "data": [
>>    {
>>      "TAB.IMDSC1": "TAB.IMDSC2",
>>      "TAB.IMDSC2": "TAB.IMDSC1"
>>    }
>>  ]
>>}
>>@endjson
>>```
>>
>>```SQLdotnetcli
>>UPDATE
>>    F4101
>>SET
>>    IMPRP1 = IMPRP2
>>    IMPRP2 = IMPRP1
>>WHERE
>>    (IMPRP1 = "A01" OR
>>    IMPRP1 = "A02) AND
>>    IMPRP2 = "B01"
>>ORDER BY
>>    IMITM ASC
>>```
>### Request POST (Insert)
>>```PlantUML
>>@startjson
>>{
>>  "object": "F4101",
>>  "filter": null,
>>  "order": null,
>>  "data": [
>>    {
>>      "TAB.IMITM": 123,
>>      "TAB.IMDSC1": "ITEM ONE",
>>      "TAB.IMDSC2": "First Item"
>>    }
>>  ]
>>}
>>@endjson
>>```
>>
>>```SQLdotnetcli
>>INSERT INTO
>>    F4101
>>    (IMITM,IMPRP1,IMPRP2)
>>VALUES
>>    (123,"ITEM ONE","First Item")
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