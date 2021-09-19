@ECHO OFF
TITLE sandbox.bat - TICK Sandbox

SET interactive=1
SET COMPOSE_CONVERT_WINDOWS_PATHS=1

SET TYPE=latest
SET TELEGRAF_TAG=latest
SET INFLUXDB_TAG=latest

ECHO %cmdcmdline% | FIND /i "/c"
IF %ERRORLEVEL% == 0 SET interactive=0

IF "%1"=="up" (
    ECHO Spinning up latest, stable Docker Images...
    ECHO If this is your first time starting system this might take a minute...
    docker-compose up -d --build
    ECHO Opening tabs in browser...
    timeout /t 3 /nobreak > NUL
    START "" http://localhost:8086
    START "" http://localhost:9000
    GOTO End

)

IF "%1"=="upswarm" (
    ECHO Spinning up latest, stable Docker Images...
    ECHO If this is your first time starting system this might take a minute...
    docker swarm init
    docker stack deploy --compose-file docker-compose-swarm.yml delpred
    ECHO Opening tabs in browser...
    timeout /t 3 /nobreak > NUL
    START "" http://localhost:9000
    START "" http://localhost:8086
    GOTO End
    
)

IF "%1"=="down" (
    ECHO Stopping and removing running system containers...
    docker-compose down
    GOTO End
)

IF "%1"=="downswarm" (
    ECHO Stopping and removing swarm containers with swarm mode...
    docker stack rm delpred
    docker swarm leave --force
    GOTO End
)

IF "%1"=="restart" (
    ECHO Stopping all sandbox processes...
    docker-compose down >NUL 2>NUL
    ECHO Starting all sandbox processes...
    docker-compose up -d --build >NUL 2>NUL
    ECHO Services available!
    GOTO End
)

IF "%1"=="delete-data" (
    ECHO Deleting all influxdb, kapacitor and chronograf data...
    rmdir /S /Q kapacitor\data influxdb\data chronograf\data
    GOTO End
)

IF "%1"=="docker-clean" (
    ECHO Stopping all running sandbox containers...
    docker-compose down
    echo Removing TICK images...
    docker-compose down --rmi=all
    GOTO End
)


IF "%1"=="help" (
ECHO sandbox commands:
ECHO   up           -^> spin up the system environment in compose.
ECHO   down         -^> tear down the system environment from compose.
ECHO   upswarm      -^> Initialize a swarm cluster, deploy system stack.
ECHO   downswarm    -^> Tear down system stack, and leave swarm cluster.
ECHO   restart      -^> restart the system environment (just in compose)
ECHO.
ECHO   enter ^(influxdb^|^|kapacitor^|^|chronograf^|^|telegraf^|^|generator^|^|predictor^) -^> enter the specified container
ECHO.
ECHO   delete-data  -^> delete all data created by in production
ECHO   docker-clean -^> stop and remove all running docker containers and images
)

:End
IF "%interactive%"=="0" PAUSE
EXIT /B 0
