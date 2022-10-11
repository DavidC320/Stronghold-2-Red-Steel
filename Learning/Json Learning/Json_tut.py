
# David Cruz
# 9/12/2022
import json

data_set = """
    {
        "allies" : [
            {
                "name" : "Anexttest",
                "race" : "human",
                "gender" : null,
                "dead" : false
            },
            {
                "name" : "23sf",
                "race" : "mech",
                "gender" : null,
                "dead" : false
            },
            {
                "name" : "YVJHB",
                "race" : "?",
                "gender" : null,
                "dead" : true
            }
        ]
    }"""

player_jason_data = {
    "data versions" : {
        "sql" : 10,
        "json" : 1
    },

    "player info" : {
        "money" : 0,
        "difficulty" : None
    }
}

# dumps converts pthon objects to json string
# loads converts json string into a python objects
data = json.dumps(player_jason_data, indent=2, sort_keys=True)
data = json.loads(data)

print(data)