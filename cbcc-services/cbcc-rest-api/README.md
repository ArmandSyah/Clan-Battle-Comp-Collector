# I will call this service, Tsumugi

Will be your typical REST Api, providing access to the db info provided by Muimi (the data extractor) to clients (like the UI for this app, Kokkoro). It will also handle user authentication as well

This will be built with Python, the Flask-RestX library, with the data stored/retrieved in a Postgres database. Might even add Redis and Flask-Cache for caching certain things