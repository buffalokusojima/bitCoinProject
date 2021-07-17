# bitCoinProject


## What the hell is this project

This project makes a chart for bitcoin, the data of which is from "BitStamp" API.
You can see from Browser

## How to srtart

`npm init` to get package installed

`cd web` and `npm start` to star web server

type `localhost:3000` to see like below

<img width="951" alt="Screen Shot 2021-07-17 at 14 58 07" src="https://user-images.githubusercontent.com/43209874/126027481-1d31a9b8-cbc0-4267-a6f6-03b98d1e2533.png">

## Hope you can make it But ...

Before these steps you need to create mysql DB with `trade.sql`
And need to create `dbInfo.json` like below
```json
{
    "host": "localhost",
    "user": "UserName",
    "password": "Password",
    "database": "DataBaseNae",
    "insecureAuth": true
}
```
Don't use this file as it is! You need modify it first. And place the file upon this root directory.
Might be troublesome a little, sorrt bro....
