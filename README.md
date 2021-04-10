# threads

## Project Overview:

This project is part of the [Udacity's Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).
We will build an application that will provide user authentication with Google Oauth. This application should include the following features to their users:
Create, Read, Update and Delete posts. This application will have it's own database and will run a dynamic website.

## Project Description

This application we're building will allow authenticated users to post a CAUSE they believe needs attention from the public authorities and then let users come and respond with possible SOLUTIONS. Users will be the only ones in charge of their content with the possibility to update and delete their posts. The website is open for reading to anyone but you must login to post a cause or respond to one.
In this project we will use:
<ol>
  <li>Python</li>
  <li>Flask framework</li>
  <li>HTML, CSS, JavaScript</li>
  <li>sqlite database</li>
  <li>VirtualBox to hold our server application</li>
  <li>Other tools: Git, Vagrant</li>
 </ol>

## Setting up the project

1. Download and install the latest version of [Python](https://www.python.org/downloads/).
2. Download and install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/).
3. Download and install [Git](https://git-scm.com/) - an open source version control system.
4. Clone this repo and navigate in your bash interface and cd to this folder and run the following commands:

- `git clone https://github.com/vchivu14/threads.git`
- `vagrant up` to start the VirtualMachine
- `vagrant ssh` to log into the VirtualMachine
- `cd /vagrant`

5. Run the application with:

- `python threadsPlainFinal.py`

6. Go to: (http://localhost:5000/threads) to navigate the website

## JSON Endpoints

http://localhost:5000/threads/JSON - will fetch all the posts listed

http://localhost:5000/threads/1/answers/JSON/ - will fetch all the answers for a given post

http://localhost:5000/threads/1/answers/1/JSON/ - will fetch one answer at a time for each post

## Improvements needed:
- Style and layout for views
- Add more features like Support and Admin for security
