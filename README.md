# GenericRestJDE
Agnostic REST server for database (ie JDEdwards).

## Architecture
```PlantUML
@startuml
ditaa(scale=1.5)

+------+
|      |
|      |
|      |
|   {o}|
+--+---+
   |
   |
   |
   V
+---------+          +---------+          +---------+          +---------+
|c008     |          |c0FF     |          |cFF0     |          |c080     |
|         |          |         |          |         |  Y       |         |
| Request +--------->|  Query  +--------->| Success +--------->|   Data  |
|         |          |         |          |         |          |         |
| {d}     |          |         |          | {c}     |          | {d}     |
+---------+          +---+-----+          +----+----+          +----+----+
                         | ^                   |                    |
                         | |                   | N                  |   
                         : :                   |                    |
                         V |                   V                    V
                     +-----+---+          +---------+            +------+
                     |cAAA     |          |cRED     |            |      |
                     |         |          |         |            |      |
                     | Oracle  |          | Errors  +----------->|      |
                     |         |          |         |            |   {o}|
                     |     {s} |          | {d}     |            +------+
                     +---------+          +---------+          
@enduml
```

## JSON Data Structure

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
>>      "column": "TAB.IMITM",
>>      "sort": "A"
>>    }
>>  ],
>>  "data":
>>    [
>>      {
>>        "column": "TAB.IMITM",
>>        "value": null
>>      },
>>      {
>>        "column": "TAB.IMDSC1",
>>        "value": null
>>      },
>>      {
>>        "column": "TAB.IMDSC2",
>>        "value": null
>>      }
>>    ]
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
>>    IMPRP1 = 'A01' AND
>>    IMPRP2 = 'B01'
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
>>      "column": "TAB.IMITM",
>>      "sort": "A"
>>    }
>>  ],
>>  "data":
>>    {
>>      "TAB.IMITM": null,
>>      "TAB.IMDSC1": null,
>>      "TAB.IMDSC2": null
>>    }
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
>>    (IMPRP1 = 'A01' OR
>>    IMPRP1 = 'A02') AND
>>    IMPRP2 = 'B01'
>>ORDER BY
>>    IMITM ASC
>>```
>>
>>```PlantUML
>>@startjson
>>{
>>  'object': 'F4111',
>>  'filter': [
>>    {
>>      'operator': '>',
>>      'term1': 'TAB.ILCRDJ',
>>      'term2': 118000
>>    },
>>    {
>>      'operator': 'AND',
>>      'term1': None,
>>      'term2': None
>>    },
>>    {
>>      'operator': '<',
>>      'term1': 'TAB.ILCRDJ',
>>      'term2': 119000
>>    }
>>  ],
>>  'order': None,
>>  'data': [
>>    {
>>       'column': 'TAB.ILITM',
>>       'value': None
>>    },
>>    {
>>       'column': 'TAB.ILLITM',
>>       'value': None
>>    },
>>    {
>>       'column': 'TAB.ILMCU',
>>       'value': None
>>    },
>>    {
>>       'column': 'TAB.ILCRDJ',
>>       'value': None
>>    }
>>  ]
>>}
>>@endjson
>>```
>>
>>```SQLdotnetcli
>>SELECT
>>    ILITM,
>>    ILLITM,
>>    ILMCU,
>>    ILCRDJ,
>>    rownum
>>FROM
>>    F4111
>>WHERE
>>    ILCRDJ > 118000 AND
>>    ILCRDJ < 119000
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
>>      "column": "TAB.IMITM",
>>      "sort": "A"
>>    }
>>  ],
>>  "data":
>>    {
>>      "TAB.IMDSC1": "TAB.IMDSC2",
>>      "TAB.IMDSC2": "TAB.IMDSC1"
>>    }
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
>>    (IMPRP1 = 'A01' OR
>>    IMPRP1 = 'A02') AND
>>    IMPRP2 = 'B01'
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
>>  "data":
>>    {
>>      "TAB.IMITM": 123,
>>      "TAB.IMDSC1": "ITEM ONE",
>>      "TAB.IMDSC2": "First Item"
>>    }
>>}
>>@endjson
>>```
>>
>>```SQLdotnetcli
>>INSERT INTO
>>    F4101
>>    (IMITM,IMPRP1,IMPRP2)
>>VALUES
>>    (123,'ITEM ONE','First Item')
>>```
>### Request DELETE
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
>>  "order": null,
>>  "data": null
>>}
>>@endjson
>>```
>>
>>```SQLdotnetcli
>>DELETE FROM
>>    F4101
>>WHERE
>>    (IMPRP1 = 'A01' OR
>>    IMPRP1 = 'A02') AND
>>    IMPRP2 = 'B01'
>>```
>### Types of operator
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
>### Terms nomenclature
>>| Type                         	| Meaning           	|
>>|-------------------------------	|---------------------	|
>>| 9,999,999.999                  	| Numeric            	|
>>| "xxxxxxxxxxxxxxxxxxxxx"      	| String constant    	|
>>| "TAB.xxxxxxxxxx"             	| Table column       	|
>>| "YYYY-MM-DD"                	| Date              	|
>>| "HH:mm:SS"                  	| Time              	|
>>| "YYYY-MM-DDTHH:mm:SS.CCCZ"   	| Datetime           	|
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