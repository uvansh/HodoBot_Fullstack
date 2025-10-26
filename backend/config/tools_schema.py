from tools.weather import get_weather
from tools.currency import get_currency
from tools.timezone import get_timezone

available_functions = {"get_weather":get_weather,"get_currency":get_currency,"get_timezone":get_timezone}

tools = [
    {
        "type":"function",
        "function":{
            "name":"get_weather",
            "description":"Get current weather for a city",
            "parameters":{
                "type":"object",
                "properties":{
                    "city":{"type":"string","description":"City name"}
                },
                "required":["city"]
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"get_currency",
            "description":"Get the conversion from one currency rates to other.",
            "parameters":{
                "amount":{"type":"number","description":"Amount to convert"},
                "from_currency":{"type":"string","description":"Current currency code (USD,EUR,INR,etc.)"},
                "to_currency":{"type":"string","description":"Target currency code."},
            },
            "required":["amount","from_currency","to_currency"]
        }
    },
    {
        "type":"function",
        "function":{
            "name":"get_timezone",
            "description":"Get the current time of a city or country.",
            "parameters":{
                "type":"object",
                "properties":{
                    "city":{"type":"string","description":"Current time of a place."}
                },
                "required":["city"]
            }
        }
    }
]

print(f"Registered Tools: {list(available_functions.keys())}")