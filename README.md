# whatsin

'Whats In?' allows you to quickly find out what ingredients are commonly included in a recipe so you don't have to trawl through recipe websites for ingredient ideas and suggestions.

## Development Environment

### Start the React app in development mode

Change directory to the frontend (web), install the project requirements, and start the development server.

```bash
whatsin$ cd web
whatsin/web$ npm install
whatsin/web$ npm start
```

This runs the app in the development mode. Open [http://localhost:3001](http://localhost:3001) to view it in the browser.

### Start and initialise a local MySQL instance

Change directory into the database and start the local MySQL database.

```bash
whatsin$ cd database
whatsin/database$ docker-compose up
```

Run the `init.sql` script to set up the tables and some dummy data.

```bash
whatsin/database$ mysql -h 127.0.0.1 -u root -p WhatsIn
...
mysql> source init.sql;
...
mysql> quit
```

