# I will call this service, Muimi

Basically, it will read all the required data from the current latest priconne database info, in order to retrieve characters and clan battle boss info. It will populate a database table with that info. That's where the REST API, Tsumugi, will take care of providing that db data to clients through http

This service is created with standard Python (nothing fancy for now), will probably put the cleaned data into a Postgresql database