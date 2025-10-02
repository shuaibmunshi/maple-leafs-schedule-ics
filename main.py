import json
from ics import Calendar, Event
from datetime import datetime
from pytz import timezone

def create_ics_from_json(input_filename="sched_2025_2026.json", output_filename="toronto_maple_leafs_2025_2026.ics"):
  # Load JSON data from the file
  with open(input_filename, "r") as file:
    data = json.load(file)

  club_timezone = timezone(data["clubTimezone"])
  calendar = Calendar()
  
  for game in data["games"]:
    event = Event()
    event.name = f"{game['awayTeam']['placeName']['default']} ({game['awayTeam']['abbrev']}) vs. {game['homeTeam']['placeName']['default']} ({game['homeTeam']['abbrev']})"
    event.begin = datetime.fromisoformat(game["startTimeUTC"].replace("Z", "+00:00")).astimezone(club_timezone)
    event.location = game["venue"]["default"]
    event.description = f"Game at {game['venue']['default']}. Broadcast on {', '.join(b['network'] for b in game['tvBroadcasts'])}."
    event.uid = str(game["id"])  # Unique ID for the event
    event.duration = {'hours': 3}
    
    calendar.events.add(event)
  
  # Write to .ics file
  with open(output_filename, "w") as f:
    f.writelines(calendar.serialize_iter())

  print(f"ICS calendar file created: {output_filename}")

# Call the function to create the ICS file
create_ics_from_json()