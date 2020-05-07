Django channels based web chess application 

![](https://raw.githubusercontent.com/elkcarc/EBChess/master/sample%20image.png)

implements chessboard.js and chess.js

originally deployed to aws elastic beanstalk and elasticache for redis


to run:

start redis

navigate to /Scripts

activate the venv

go back up one level and run daphne -b 0.0.0.0 -p 8001 ebdjango.asgi:application
