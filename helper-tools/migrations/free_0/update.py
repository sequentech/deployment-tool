from sqlalchemy import *
import json

AGORA_ELECTIONS_PASSWORD = "<PASSWORD>"
AUTHAPI_PASSWORD = "<PASSWORD>"

db_string = "postgres://agora_elections:%s@localhost:5432/agora_elections" % AGORA_ELECTIONS_PASSWORD

db = create_engine(db_string)

# [(config, eid)]
all_elections = []
# [(admin_fields, eid)]
elections_with_admin_fields = []

# Create 
data = db.execute("select configuration, id from election;")

for line in data:
  all_elections.append(line)

for election in all_elections:
  config = election[0]
  eid = election[1]
  try:
    json_config = json.loads(config)
    if "extra_data" in json_config:
      extra_data = json.loads(json_config["extra_data"])
      
      if "admin_extra_fields" in extra_data and isinstance(extra_data["admin_extra_fields"], list):
        for field in extra_data["admin_extra_fields"]:
          if "name" in field and "type" in field and "value" in field \
            and "expected_census" == field["name"] and "int" == field["type"] \
            and isinstance(field["value"], int):
            payload = json.dumps([
              {
                "name": "expected_census",
                "label": "free.adminFields.expectedCensus.label",
                "description": "free.adminFields.expectedCensus.description",
                "type": "int",
                "min": 0,
                "step": 1,
                "value": field["value"],
                "required": True,
                "private": True
              }
            ])
            elections_with_admin_fields.append( (payload, eid) )
            break
  except:
    pass

db_string = "postgres://authapi:%s@localhost:5432/authapi" % AUTHAPI_PASSWORD

db = create_engine(db_string)

for election in elections_with_admin_fields:
  admin_fields = election[0]
  eid = election[1]
  db.execute("update api_authevent set admin_fields='%s' where id=%i;" % (admin_fields, eid))
