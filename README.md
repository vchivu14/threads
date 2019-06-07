# Project Item Catalog

## Project Overview:

This project is part of the [Udacity's Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)
We will build an application that will provide user authentication with Google Oauth. This application should include the following features to their users:
Create, Read, Update and Delete data. This application will have it's own database and will run a dynamic website.

## Project Description

This application we're building will allow authenticated users to post a cause they believe needs attention from the public and then let users come and respond with possible solutions. Users will be the only ones in charge of their content with the possibility to update and delete their posts. The website is open for reading to anyone but you must login to at least post an idea or respond to one.
In this project we will use:
Python, Flask, HTML, CSS, SQL database and Git.

## Setting up the project

1. Download and install the latest version of [Python](https://www.python.org/downloads/).
2. Download and install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/).
3. Download and install [Git](https://git-scm.com/) - an open source version control system.
4. Navigate in your bash interface and cd to this folder and run the following commands:

- `vagrant up` to start the VirtualMachine
- `vagrant ssh` to log into the VirtualMachine
- `cd /vagrant` to change to your directory

5. Run the application with:

- `python threadsPlainFinal.py`

6. Go to: (http://localhost:5000/threads) to navigate the website

## JSON Endpoints

http://localhost:5000/threads/JSON - will fetch all the Causes listed

{
"causes": [
{
"id": 4,
"name": "Single parents"
},
{
"id": 1,
"name": "The Environment problem"
},
{
"id": 3,
"name": "Unpaved roads"
},
{
"id": 2,
"name": "kids with no help"
}
]
}

http://localhost:5000/threads/1/answers/JSON/ - will fetch answers for each cause

{
"EffectAnswer": [
{
"area": "global",
"id": 1,
"importance": "high",
"name": "silly",
"solution": "drive less"
},
{
"area": "global",
"id": 2,
"importance": "high",
"name": "gauge",
"solution": "plant more trees"
},
{
"area": "local",
"id": 6,
"importance": "high",
"name": "jack",
"solution": "ggg"
}
]
}

http://localhost:5000/threads/1/answers/1/JSON/ - will fetch one answer at a time for each cause

{
"answer": {
"area": "global",
"id": 1,
"importance": "high",
"name": "silly",
"solution": "drive less"
},
"cause": {
"id": 1,
"name": "The Environment problem"
}
}

## Improvements needed for now:

- Style and layout for better allignment
- Add more features like Support and Admin for security
