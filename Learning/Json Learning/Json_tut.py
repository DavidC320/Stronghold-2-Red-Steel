
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

data = json.loads(data_set)

print(data['allies'])