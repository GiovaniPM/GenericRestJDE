# GenericRestJDE
Generic REST server for JDE

## JSON structure

### Request
```PlantUML
@startjson
{
  "object": "F4101",
  "filter": [
    {
      "connection": null,
      "colunm": "IMPRP1",
      "operator": "=",
      "value": "A01"
    },
    {
      "connection": "AND",
      "colunm": "IMPRP2",
      "operator": "=",
      "value": "B01"
    }
  ],
  "order": [
    {
      "colunm": "IMITM",
      "sort": "A"
    }
  ],
  "return": [
    "IMITM",
    "IMDSC1",
    "IMDSC2"
  ]
}
@endjson
```

### Error
```PlantUML
@startjson
{
  "error": [
    {
      "number": 12,
      "text": "No values return."
    },
    {
      "number": 99,
      "text": "Revise your request."
    }
  ]
}
@endjson
```

### Return
@startjson
{
  "statistic": {
    "TimeStamp": "2012-04-23T18:25:43.511Z",
    "TimeElapsed": 0.00112
  },
  "data": [
    {
      "IMITM": 123,
      "IMDSC1": "ITEM UM",
      "IMDSC2": "Primeiro item"
    },
    {
      "IMITM": 234,
      "IMDSC1": "ITEM DOIS",
      "IMDSC2": "Segundo item"
    },
    {
      "IMITM": 345,
      "IMDSC1": "ITEM TRÊS",
      "IMDSC2": "Terceiro item"
    }
  ]
}
@endjson
```