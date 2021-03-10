# GenericRestJDE
Generic REST server for JDE

## JSON structure

>### Request
>>```PlantUML
>>@startjson
>>{
>>  "object": "F4101",
>>  "filter": [
>>    {
>>      "connection": null,
>>      "colunm": "IMPRP1",
>>      "operator": "=",
>>      "value": "A01"
>>    },
>>    {
>>      "connection": "AND",
>>      "colunm": "IMPRP2",
>>      "operator": "=",
>>      "value": "B01"
>>    }
>>  ],
>>  "order": [
>>    {
>>      "colunm": "IMITM",
>>      "sort": "A"
>>    }
>>  ],
>>  "return": [
>>    "IMITM",
>>    "IMDSC1",
>>    "IMDSC2"
>>  ]
>>}
>>@endjson
>>```
>---
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
>---
>### Return
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