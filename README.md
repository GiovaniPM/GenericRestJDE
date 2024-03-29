# GenericRestJDE
Agnostic REST server for database (example Oracle) to be used for internals request such others services.<br>
Based uppon Python 3.9 and Flask.

## Project Structure
📦 **GenericRestJDE**<br>
 ┣ 📂 **api**<br>
 ┃ ┣ 📂 **Archive**<br>
 ┃ ┃ ┗ 📜 _archived files ..._<br>
 ┃ ┗ 📜 api.py<br>
 ┣ 📂 **docker**<br>
 ┃ ┣ 📂 **Api**<br>
 ┃ ┃ ┣ 📜 build.bat<br>
 ┃ ┃ ┣ 📜 Dockerfile<br>
 ┃ ┃ ┣ 📜 requirements.txt<br>
 ┃ ┃ ┣ 📜 run.bat<br>
 ┃ ┃ ┣ 📜 start.bat<br>
 ┃ ┃ ┗ 📜 stop.bat<br>
 ┃ ┣ 📂 **Base**<br>
 ┃ ┃ ┣ 📜 build.bat<br>
 ┃ ┃ ┣ 📜 Dockerfile<br>
 ┃ ┃ ┗ 📜 push.bat<br>
 ┃ ┗ 📂 **Oldies**<br>
 ┃ ┃ ┗ 📜 _old files ..._<br>
 ┣ 📂 **Test**<br>
 ┃ ┗ 📜 _test files ..._<br>
 ┣ 📜 README.md<br>
 ┗ 📜 upload.per<br>

## Solution Design
```PlantUML
@startuml
ditaa(scale=0.8)
                           +-----+
                           |     |
                           |     |
                           |  {o}|
                           +--+--+
                              |
                              V
                         +---------+
                         |c008     |
                         |         |
                         | Request |
                         |         |
                         | {io}    |
                         +----+----+
                              |
                              V
+-------------------------------------------[Agnostic Rest]-+
|     +-----+                                               |
|     |cEEE |                                               |
|     |     |                                               |
|     |  {o}|                                               |
|     +--+--+                                               |
|        |                                                  |
|        V                                                  |
|   +---------+                                             |
|   |c0FF     |                                             |
|   |  Build  |                                             |
|   |         |                                             |
|   |  Query  |                                             |
|   |         |                                             |
|   +----+----+                                             |
|        |                                                  |
|        V                                                  |
|   +---------+                               +---------+   |
|   |cFF0     |                               |cF00     |   |
|   |         |               N               |         |   |
|   | Success +------------------------------>| Errors  |   |
|   |         |                               |         |   |
|   | {c}     |                               | {d}     |   |
|   +----+----+                               +----+----+   |
|      Y |                                         |        |
|        V                                         |        |
|   +---------+                                    |        |          +---------+
|   |c0FF     |                                    |        |          |c888     |
|   |         +-=----------------------------------|-=------|-=------->|         |
|   |  Query  |                                    |        |          | Oracle  |
|   |         |<-=---------------------------------|-=------|-=--------+         |
|   |         |                                    |        |          |     {s} |
|   +----+----+                                    |        |          +---------+
|        |                                         |        |
|        V                                         |        |
|   +---------+          +---------+               |        |
|   |cFF0     |          |cF00     |               |        |
|   |         |    N     |         |               |        |
|   | Success +--------->| Errors  |               |        |
|   |         |          |         |               |        |
|   | {c}     |          | {d}     |               |        |
|   +----+----+          +----+----+               |        |
|      Y |                    |                    |        |
|        V                    |                    |        |
|   +---------+               |                    |        |
|   |c0F0     |               |                    |        |
|   |         |               |                    |        |
|   |   Data  |               |                    |        |
|   |         |               |                    |        |
|   | {d}     |               |                    |        |
|   +----+----+               |                    |        |
|        |                    |                    |        |
|        V                    |                    |        |
|     +-----+                 |                    |        |
|     |cBBB |                 |                    |        |
|     |     |<----------------+--------------------+        |
|     |  {o}|                                               |
|     +-----+                                               |
+-----------------------------+-----------------------------+
                              |
                              V
                         +---------+
                         |c008     |
                         |         |
                         |  Send   |
                         |         |
                         | {io}    |
                         +----+----+
                              |
                              V
                           +-----+
                           |cBLK |
                           |     |
                           |  {o}|
                           +-----+
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
>>  "object": "F4111",
>>  "filter": [
>>    {
>>      "operator": ">",
>>      "term1": "TAB.ILCRDJ",
>>      "term2": 118000
>>    },
>>    {
>>      "operator": "AND",
>>      "term1": null,
>>      "term2": null
>>    },
>>    {
>>      "operator": "<",
>>      "term1": "TAB.ILCRDJ",
>>      "term2": 119000
>>    }
>>  ],
>>  "order": null,
>>  "data": [
>>    {
>>       "column": "TAB.ILITM",
>>       "value": null
>>    },
>>    {
>>       "column": "TAB.ILLITM",
>>       "value": null
>>    },
>>    {
>>       "column": "TAB.ILMCU",
>>       "value": null
>>    },
>>    {
>>       "column": "TAB.ILCRDJ",
>>       "value": null
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
>>```bash
>>curl -X GET -i -H "Content-Type: application/json" -d "{\"object\": \"F4111\", \"filter\": [{\"operator\": \"=\", \"term1\": \"TAB.ILLITM\", \"term2\": \"ME00004N                 \"}], \"order\": null, \"data\": [{\"column\": \"TAB.ILITM\", \"value\": null}, {\"column\": \"TAB.ILLITM\", \"value\": null}, {\"column\": \"TAB.ILMCU\", \"value\": null}, {\"column\": \"TAB.ILCRDJ\", \"value\": null}]}" http://127.0.0.1:8080/api/v1/oracle/select
>>```
>### Request PUT (Update)
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
>>  "data":
>>    [
>>      {
>>        "column": "TAB.IMDSC1",
>>        "value": "TAB.IMDSC2"
>>      },
>>      {
>>        "column": "TAB.IMDSC2",
>>        "value": "TAB.IMDSC1"
>>      }
>>    ]
>>}
>>@endjson
>>```
>>
>>```SQLdotnetcli
>>UPDATE
>>    F4101
>>SET
>>    IMPRP1 = IMPRP2,
>>    IMPRP2 = IMPRP1
>>WHERE
>>    (IMPRP1 = 'A01' OR
>>    IMPRP1 = 'A02') AND
>>    IMPRP2 = 'B01'
>>```
>>```bash
>>curl -X PUT -i -H "Content-Type: application/json" -d "{ \"object\": \"F4101\", \"filter\": [ { \"operator\": \"(\", \"term1\": null, \"term2\": null }, { \"operator\": \"=\", \"term1\": \"TAB.IMPRP1\", \"term2\": \"A01\" }, { \"operator\": \"OR\", \"term1\": null, \"term2\": null }, { \"operator\": \"=\", \"term1\": \"TAB.IMPRP1\", \"term2\": \"A02\" }, { \"operator\": \")\", \"term1\": null, \"term2\": null }, { \"operator\": \"AND\", \"term1\": null, \"term2\": null }, { \"operator\": \"=\", \"term1\": \"TAB.IMPRP2\", \"term2\": \"B01\" } ], \"order\": null, \"data\": [ { \"column\": \"TAB.IMDSC1\", \"value\": \"TAB.IMDSC2\" }, { \"column\": \"TAB.IMDSC2\", \"value\": \"TAB.IMDSC1\" } ] }" http://127.0.0.1:8080/api/v1/oracle/update
>>```
>### Request POST (Insert)
>>```PlantUML
>>@startjson
>>{
>>  "object": "F4101",
>>  "filter": null,
>>  "order": null,
>>  "data":
>>    [
>>      {
>>        "column": "TAB.IMITM",
>>        "value": 123
>>      },
>>      {
>>        "column": "TAB.IMDSC1",
>>        "value": "ITEM ONE"
>>      },
>>      {
>>        "column": "TAB.IMDSC2",
>>        "value": "First Item"
>>      }
>>    ]
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
>>```bash
>>curl -X POST -i -H "Content-Type: application/json" -d "{ \"object\": \"F4101\", \"filter\": null, \"order\": null, \"data\": [ { \"column\": \"TAB.IMITM\", \"value\": 123 }, { \"column\": \"TAB.IMDSC1\", \"value\": \"ITEM ONE\" }, { \"column\": \"TAB.IMDSC2\", \"value\": \"First Item\" } ] } " http://127.0.0.1:8080/api/v1/oracle/insert
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
>>```bash
>>curl -X DELETE -i -H "Content-Type: application/json" -d "{ \"object\": \"F4101\", \"filter\": [ { \"operator\": \"=\", \"term1\": \"TAB.IMITM\", \"term2\": 123 } ], \"order\": null, \"data\": null }" http://127.0.0.1:8080/api/v1/oracle/delete
>>```
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

## Types of operator
|Option	|Description	|
|:--------:	|:-----------------------:	|
|(	|_Open a operation group_	|
|)	|_Close a operation group_	|
|AND	|_AND operator_	|
|OR	|_OR operator_	|
|NOT	|_NOT operator_	|
|=	|_equal_	|
|!=	|_different_	|
|<=	|_less or equal_	|
|>=	|_great or equal_	|
|>	|_great_	|
|<	|_less_	|
|IN	|_inbound_	|
|NOT IN	|_outbound_	|

## Terms nomenclature
|Type	|Meaning	|Prefix    |Value    |
|-------------------------------	|---------------------	|---------------------	|---------------------	|
|9,999,999.999	|_Numeric_	|    |9,999,999.999    |
|xxxxxxxxxxxxxxxxxxxxx	|_String constant_	|    |xxxxxxxxxxxxxxxxxxxxx    |
|TAB.xxxxxxxxxx	|_Table column_	|TAB.    |xxxxxxxxxx    |
|DTA.YYYY-MM-DD	|_Date_	|DTA.    |YYYY-MM-DD    |
|TME.HH:mm:SS	|_Time_	|TME.    |HH:mm:SS    |
|CNJ.('XXXX','XXXX')	|_Set of values_	|CNJ.    |('XXXX','XXXX')|
<!--|"YYYY-MM-DDTHH:mm:SS.CCCZ"	|_Datetime_	|-->

## Status Code
|Status	|Description	|
|-----------	|:-----------------------:  	|
|200	|_Success_	|
|204	|_No data found_	|
|400	|_Bad Request_	|
|406	|_Error_	|
|500	|_Internal Error_	|

## Processing Errors
|Status	|Description	|
|-----------	|:-----------------------:	|
|500.01	|_Output column(s) are required!_	|
|500.02	|_Filter column(s) are required!_	|
|500.03	|_Insert column(s) are required!_	|
|500.04	|_Update column(s) are required!_	|
|500.05	|_Date must be YYYY-MM-DD format!_	|
|500.06	|_Time must be HH:mm:SS format!_	|
|500.07	|_JSON in BODY is required!_	|

## Next Act
- [ ] - Improve the errors to a array<br>
- [x] - Implement filter option IN/NOT IN<br>
- [x] - Tretament of datatypes: Date, Time and Datetime over filter conditions<br>