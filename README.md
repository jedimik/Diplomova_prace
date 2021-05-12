# Master theses project

Software architecture for real time data streaming and anomaly prediction.
### Prerequisites
#### Windows
Install and enable WSL2 for windows. Install Docker Desktop and Git for repository cloning
```bash
git clone https://github.com/jedimik/Diplomova_prace.git
```
#### Linux
```bash
apt-get install docker git python
git clone https://github.com/jedimik/Diplomova_prace.git
```
### How to run
```bash
$ ./sandbox
For windows use ./sandbox.bat <arg> 
For linux use ./sandbox <arg>
sandbox commands:
up                 -> spin up the sandbox environment (latest or nightlies specified in the companion file)
down               -> tear down the sandbox environment (latest or nightlies specified in the companion file)
upswarm     -> Initialize a swarm cluster, deploy system stack.
downswarm   -> Tear down system stack, and leave swarm cluster.
restart            -> restart the system environment (just in compose)
influxdb           -> attach to the influx cli
flux               -> attach to the flux REPL

enter (influxdb||kapacitor||chronograf||telegraf) -> enter the specified container
logs  (influxdb||kapacitor||chronograf||telegraf) -> stream logs for the specified container

delete-data  -> delete all data created by the TICK Stack
docker-clean -> stop and remove all running docker containers and images
 
```

To get started with compose type `./sandbox up`. You browser will open two tabs:
To get started docker swarm run `./sandbox upswarm`. You browser will open two tabs:
- `localhost:8888` - Chronograf's address. Management API Influx components
- `localhost:9000` - Portainer address.  Managment API for containers
