Sazabi
======

A discord bot with cats and imgur. Tested on Python 3.6.

```bash
python bin/sazabi -c config.yaml
```

## Plugins
* cat: Random cat picture
* imgur: Random imgur picture from configured galleries
* joke: Random joke from /r/oneliners
* text: Text macros
* twitch: Watches streams and notifies when they become online.
  (Requires postgres)
* weather: Weather for specified location

## Setup
1.  Create database and user for sazabi. Configure alembic.ini with database details
2.  `pip3 install alembic psycopg2`
3.  If you do not have postgres contrib libraries `yum install postgresql95-contrib`
4.  Connect to the database as the postgres user and enable the uuid_ossp extension
    `# CREATE EXTENSION 'uuid-ossp';`
5.  Create the tables `alembic upgrade head`

## Configuration

### Environment variables
* SAZABI_LOG: Path to log file

### Configuration file
Sample YAML configuration
```yaml
discord:
    client: "CLIENT ID"
    secret: "CLIENT SECRET"
    token: "AUTH TOKEN"
imgur:
    client_id: "CLIENT ID"
    client_token: "TOKEN"
twitch:
    client_id: "CLIENT ID"
    interval: 60
plugins:
    - "cat"
    - "imgur"
    - "joke"
    - "text"
    - "weather"

```