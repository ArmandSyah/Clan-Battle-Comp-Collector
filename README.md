# Priconne Clan Battle Comp Collector (CBCC)

**Live Demo Site:** https://blooming-hollows-51011.herokuapp.com/clanBattle 

## Information
This website is meant to be a repository for Clan Battle team compositions for the game Princess Connect Re:dive. Clan Battles are often a strict affair, requiring specific characters and builds in order to fight effectively. Rather than try to look up team compositions on youtube or other websites, it would be nice to have a website that has all that info in one palce. 

CBCC allows people to add new team compositions with detailed notes, specific character stats, ect.

This project is split into 3 different projects, each fulfilling a specific purpose (also I named each of them after my favourite characters in the game)

- `cbcc-data-extractor (Muimi)`: Handles seeding the database with character, boss and clan battle schedule info from the game. Only useful if you wish to do development on this project, otherwise not useful for anyone else.
- `cbcc-rest-api (Tsumugi)`: The backend API for this project. Allows access (mainly to the UI portion) to character and boss information. It also provides endpoints to add and store team comps  
- `cbcc-ui (Kokkoro)`: The UI for this project, allowing users to view, create, update and delete team compositions

### Things to do/Features to be added
- [ ] Realtime updates of the main page upon team comps being added, editted or deleted
- [ ] Additional comment section for the view team comp page
- [ ] Authentication and permissions for team comp crud operations
- [ ] Experiment with different fonts to find something more visually appealing
- [ ] Put some strict limits on the inputs of various places
- [ ] Add help tooltips
- [ ] DRY up code

## Requirements

- Python 3.8+
    - Do note that for the `CBCC-Data-Extractor`, the version of python used for that must be at 3.8, otherwise there'll be issues with trying to install its dependencies (in particular, the Decrunch package can't install properly on higher versions of python)
- Node.js
- Docker
- Docker-Compose
- virtualenv  

## Development

If you are interested in running this locally and doing some development for it, here's some instructions. For now, setup and local development of `CBCC` must be done through Docker

1. Clone this repo and then switch to the repo folder
   ```
   git clone https://github.com/ArmandSyah/pcrd-cbcc.git
   cd pcrd-cbcc
   ```
2. Add the following environment variable to ensure that the UI can communicate with the backend
   ```
   ## unix
   export REACT_APP_API_SERVICE_URL=http://localhost:5004

   ## windows
   SET REACT_APP_API_SERVICE_URL=http://localhost:5004
   ```
3. In the root of the project, run the following docker compose commands to build the services and then run their respective containers
   ```
   docker-compose build
   docker-compose up -d
   ```
   Once the containers are up and running, you can open `http://localhost:3007/` in the browser and interact with the UI.

   However, when you first open the page, you will see an error message on screen. That's because the in-game data for bosses, characters and clan battle schedule has not been seeded into the database. For that, you'll need the `cbcc-data-extractor`. Follow the instructions within the readme of that part of the project