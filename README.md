# whatsin-web

This a repository for the web frontend of the applicationn 'What's In?' written in React. 'Whats In?' allows you to quickly find out what ingredients are commonly included in a recipe so you don't have to trawl through recipe websites for ingredient ideas and suggestions.

## Overview

This is a very simple React application which could be deployed in many places. For consistency with the other components of this application instructions here will be for AWS using Amplify.

## Development Environment

This will use the production backend by default but you can change it to use a local API endpoint if you have set up the backend development environment.

Install requirements.

```bash
whatsin-web$ npm install
```

Start the development server.

```bash
whatsin-web$ npm start
```

This runs the app in the development mode.

Open [http://localhost:3001](http://localhost:3001) to view it in the browser.

## Deployment

Create an AWS S3 Bucket for the build files using [these instructions](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/static-website-hosting.html).

Configure the AWS CLI.

```bash
whatsin-web$ aws configure
```

Build the application to the `build` folder.

```bash
whatsin-web$ npm run build
```

Deploy the application to the S3 Bucket you created.

```bash
whatsin-web$ aws s3 sync build/ s3://whatsin-web
```