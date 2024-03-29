# PROJECT-BIRDNEST

A rare and endangered Monadikuikka has been spotted nesting at a local lake.
Unfortunately some enthusiasts have been a little too curious about this elusive bird species, flying their drones very close to the nest for rare photos and bothering the birds in the process.
To preserve the nesting peace, authorities have declared the area within 100 meters of the nest a no drone zone (NDZ), but suspect some pilots may still be violating this rule.
The authorities have set up drone monitoring equipment to capture the identifying information broadcasted by the drones in the area, and have given you access to a national drone pilot registry. They now need your help in tracking violations and getting in touch with the offenders.

### Updates
Added data generator because Reactor Api no longer works.

### More details
https://assignments.reaktor.com/birdnest/

The Reactor API is no longer working

### Demo

http://109.204.232.228:8080

The Reactor API is no longer working

### Requirements

- Persist the pilot information for 10 minutes since their drone was last seen by the equipment
- Display the closest confirmed distance to the nest
- Contain the pilot name, email address and phone number
- Immediately show the information from the last 10 minutes to anyone opening the application
- Not require the user to manually refresh the view to see up-to-date information

<b>Drone positions</b>

GET assignments.reaktor.com/birdnest/drones

<b>Pilot information</b>

GET assignments.reaktor.com/birdnest/pilots/:serialNumber

### Stack

- Django
- Python
- SQLite
- Canvasjs
- FastAPI (added for data generator if reactor host not works)
- Pydantyc


### TODO
1. Refactor main code
2. Run own data generator, because Reactor API is no longer working
3. Tests


