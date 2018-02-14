# Boardgame Tool

This tool uses data from the BoardGameGeek website, extracted by mrpantherson and located at https://www.kaggle.com/mrpantherson/board-game-data

The goal of this tool is to provide ways for users to interact with and explore this data for everyday purposes, such as:

* Picking the correct boardgame for a situation
* Getting suggestions on what boardgame to try next

Eventually I also have interest in producing an explorable ontology using similarities between games.

## Quickstart

1. Acquire Python - https://www.python.org/downloads/
2. Acquire Node.js - https://nodejs.org/en/download/
3. Acquire yarn - https://yarnpkg.com/en/
4. Run `git clone https://github.com/caesuric/boardgame-tool.git`
5. Navigate to the repo directory and run `yarn install`
6. Run `start webpack` and leave it running if you will be making changes to the code
7. To start the server, navigate to the 'server' directory and run `python boardgame-tool.py`
8. In a web browser, go to http://127.0.0.1:8080/

## Code Guide

/server/ - the Python backend server and processing features live here

/src/ - the frontend JavaScript lives here

/src/network/ - network communication logic

/src/views/ - the HTML templates, controllers, and styling for each screen of the application

/src/widgets/ - the HTML templates, controllers, and styling for visual components of the application

/web/ - this is where the compiled browser-ready JavaScript code is output
