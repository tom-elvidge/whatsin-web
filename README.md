# whatsin

'Whats In?' allows you to quickly find out what ingredients are commonly included in a recipe so you don't have to trawl through recipe websites for ingredient ideas and suggestions.

## Development Environment

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

### Build and start local API

From the project root directory build the backend code and then run the API locally.

```bash
whatsin$ sam build --use-container
whatsin$ sam local start-api --docker-network whatsin
```

### Start the React app in development mode

Change directory to the frontend (web), install the project requirements, and start the development server.

```bash
whatsin$ cd web
whatsin/web$ npm install
whatsin/web$ npm start
```

This runs the app in the development mode. Open [http://localhost:3001](http://localhost:3001) to view it in the browser.

## Deployment

Create an MySQL server instance anywhere you like (AWS RDS, on site, etc).

### Deploy backend using SAM

Update the `api/GetIngredientsFunction/credentials.csv` file with the production credentials.

From the project root directory build the backend code and then deploy with SAM.

```bash
whatsin$ sam build --use-container
whatsin$ sam deploy
```

### Deploy the frontend to S3

Create an AWS S3 Bucket for the build files using these instructions.

Configure the AWS CLI.

```bash
whatsin-web$ aws configure
```

Build the application to the build folder.

```bash
whatsin-web$ npm run build
```

Deploy the application to the S3 Bucket you created.

```bash
whatsin-web$ aws s3 sync build/ s3://whatsin-web
```