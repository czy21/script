
## conf
- /volume5/storage/docker-data/superset/conf/docker/.env
```text
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
COMPOSE_PROJECT_NAME=superset

# database configurations (do not modify)
DATABASE_DB=superset
DATABASE_HOST=db
DATABASE_PASSWORD=superset
DATABASE_USER=superset

# database engine specific environment variables
# change the below if you prefers another database engine
DATABASE_PORT=5432
DATABASE_DIALECT=postgresql
POSTGRES_DB=superset
POSTGRES_USER=superset
POSTGRES_PASSWORD=superset
#MYSQL_DATABASE=superset
#MYSQL_USER=superset
#MYSQL_PASSWORD=superset
#MYSQL_RANDOM_ROOT_PASSWORD=yes

# Add the mapped in /app/pythonpath_docker which allows devs to override stuff
PYTHONPATH=/app/pythonpath:/app/docker/pythonpath_dev
REDIS_HOST=redis
REDIS_PORT=6379

FLASK_ENV=development
SUPERSET_ENV=development
SUPERSET_LOAD_EXAMPLES=yes
CYPRESS_CONFIG=false
SUPERSET_PORT=8088
```
- /volume5/storage/docker-data/superset/conf/docker/.env-non-dev
```text
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
COMPOSE_PROJECT_NAME=superset

# database configurations (do not modify)
DATABASE_DB=superset
DATABASE_HOST=db
DATABASE_PASSWORD=superset
DATABASE_USER=superset

# database engine specific environment variables
# change the below if you prefers another database engine
DATABASE_PORT=5432
DATABASE_DIALECT=postgresql
POSTGRES_DB=superset
POSTGRES_USER=superset
POSTGRES_PASSWORD=superset
#MYSQL_DATABASE=superset
#MYSQL_USER=superset
#MYSQL_PASSWORD=superset
#MYSQL_RANDOM_ROOT_PASSWORD=yes

# Add the mapped in /app/pythonpath_docker which allows devs to override stuff
PYTHONPATH=/app/pythonpath:/app/docker/pythonpath_dev
REDIS_HOST=redis
REDIS_PORT=6379

FLASK_ENV=production
SUPERSET_ENV=production
SUPERSET_LOAD_EXAMPLES=yes
CYPRESS_CONFIG=false
SUPERSET_PORT=8088
```
- /volume5/storage/docker-data/superset/conf/docker/docker-bootstrap.sh
```bash
#!/usr/bin/env bash
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

set -eo pipefail

REQUIREMENTS_LOCAL="/app/docker/requirements-local.txt"
# If Cypress run – overwrite the password for admin and export env variables
if [ "$CYPRESS_CONFIG" == "true" ]; then
    export SUPERSET_CONFIG=tests.integration_tests.superset_test_config
    export SUPERSET_TESTENV=true
    export ENABLE_REACT_CRUD_VIEWS=true
    export SUPERSET__SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://superset:superset@db:5432/superset
fi
#
# Make sure we have dev requirements installed
#
if [ -f "${REQUIREMENTS_LOCAL}" ]; then
  echo "Installing local overrides at ${REQUIREMENTS_LOCAL}"
  pip install -r "${REQUIREMENTS_LOCAL}"
else
  echo "Skipping local overrides"
fi

if [[ "${1}" == "worker" ]]; then
  echo "Starting Celery worker..."
  celery --app=superset.tasks.celery_app:app worker -Ofair -l INFO
elif [[ "${1}" == "beat" ]]; then
  echo "Starting Celery beat..."
  celery --app=superset.tasks.celery_app:app beat --pidfile /tmp/celerybeat.pid -l INFO -s "${SUPERSET_HOME}"/celerybeat-schedule
elif [[ "${1}" == "app" ]]; then
  echo "Starting web app..."
  flask run -p 8088 --with-threads --reload --debugger --host=0.0.0.0
elif [[ "${1}" == "app-gunicorn" ]]; then
  echo "Starting web app..."
  /usr/bin/run-server.sh
fi
```
- /volume5/storage/docker-data/superset/conf/docker/docker-ci.sh
```bash
#!/usr/bin/env bash
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
/app/docker/docker-init.sh

# TODO: copy config overrides from ENV vars

# TODO: run celery in detached state
export SERVER_THREADS_AMOUNT=8
# start up the web server

/usr/bin/run-server.sh
```
- /volume5/storage/docker-data/superset/conf/docker/docker-frontend.sh
```bash
#!/usr/bin/env bash
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
set -e

cd /app/superset-frontend
npm install -g npm@7
npm install -f --no-optional --global webpack webpack-cli
npm install -f --no-optional

echo "Running frontend"
npm run dev
```
- /volume5/storage/docker-data/superset/conf/docker/docker-init.sh
```bash
#!/usr/bin/env bash
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
set -e

#
# Always install local overrides first
#
/app/docker/docker-bootstrap.sh

STEP_CNT=4

echo_step() {
cat <<EOF

######################################################################


Init Step ${1}/${STEP_CNT} [${2}] -- ${3}


######################################################################

EOF
}
ADMIN_PASSWORD="admin"
# If Cypress run – overwrite the password for admin and export env variables
if [ "$CYPRESS_CONFIG" == "true" ]; then
    ADMIN_PASSWORD="general"
    export SUPERSET_CONFIG=tests.superset_test_config
    export SUPERSET_TESTENV=true
    export ENABLE_REACT_CRUD_VIEWS=true
    export SUPERSET__SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://superset:superset@db:5432/superset
fi
# Initialize the database
echo_step "1" "Starting" "Applying DB migrations"
superset db upgrade
echo_step "1" "Complete" "Applying DB migrations"

# Create an admin user
echo_step "2" "Starting" "Setting up admin user ( admin / $ADMIN_PASSWORD )"
superset fab create-admin \
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email admin@superset.com \
              --password $ADMIN_PASSWORD
echo_step "2" "Complete" "Setting up admin user"
# Create default roles and permissions
echo_step "3" "Starting" "Setting up roles and perms"
superset init
echo_step "3" "Complete" "Setting up roles and perms"

if [ "$SUPERSET_LOAD_EXAMPLES" = "yes" ]; then
    # Load some data to play with
    echo_step "4" "Starting" "Loading examples"
    # If Cypress run which consumes superset_test_config – load required data for tests
    if [ "$CYPRESS_CONFIG" == "true" ]; then
        superset load_test_users
        superset load_examples --load-test-data
    else
        superset load_examples
    fi
    echo_step "4" "Complete" "Loading examples"
fi
```
- /volume5/storage/docker-data/superset/conf/docker/frontend-mem-nag.sh
```bash
#!/usr/bin/env bash
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

set -e

# We need at least 3GB of free mem...
MIN_MEM_FREE_GB=3
MIN_MEM_FREE_KB=$(($MIN_MEM_FREE_GB*1000000))

echo_mem_warn() {
  MEM_FREE_KB=$(awk '/MemFree/ { printf "%s \n", $2 }' /proc/meminfo)
  MEM_FREE_GB=$(awk '/MemFree/ { printf "%s \n", $2/1024/1024 }' /proc/meminfo)

  if [[ "${MEM_FREE_KB}" -lt "${MIN_MEM_FREE_KB}" ]]; then
    cat <<EOF
    ===============================================
    ========  Memory Insufficient Warning =========
    ===============================================

    It looks like you only have ${MEM_FREE_GB}GB of
    memory free. Please increase your Docker
    resources to at least ${MIN_MEM_FREE_GB}GB

    ===============================================
    ========  Memory Insufficient Warning =========
    ===============================================
EOF
  else
    echo "Memory check Ok [${MEM_FREE_GB}GB free]"
  fi
}

# Always nag if they're low on mem...
echo_mem_warn
```
- /volume5/storage/docker-data/superset/conf/docker/README.md
```text
<!--
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
-->

# Getting Started with Superset using Docker

Docker is an easy way to get started with Superset.

## Prerequisites

1. Docker! [link](https://www.docker.com/get-started)
2. Docker-compose [link](https://docs.docker.com/compose/install/)

## Configuration

The `/app/pythonpath` folder is mounted from [`./docker/pythonpath_dev`](./pythonpath_dev)
which contains a base configuration [`./docker/pythonpath_dev/superset_config.py`](./pythonpath_dev/superset_config.py)
intended for use with local development.

### Local overrides

In order to override configuration settings locally, simply make a copy of [`./docker/pythonpath_dev/superset_config_local.example`](./pythonpath_dev/superset_config_local.example)
into `./docker/pythonpath_dev/superset_config_docker.py` (git ignored) and fill in your overrides.

### Local packages

If you want to add Python packages in order to test things like databases locally, you can simply add a local requirements.txt (`./docker/requirements-local.txt`)
and rebuild your Docker stack.

Steps:

1. Create `./docker/requirements-local.txt`
2. Add your new packages
3. Rebuild docker-compose
    1. `docker-compose down -v`
    2. `docker-compose up`

## Initializing Database

The database will initialize itself upon startup via the init container ([`superset-init`](./docker-init.sh)). This may take a minute.

## Normal Operation

To run the container, simply run: `docker-compose up`

After waiting several minutes for Superset initialization to finish, you can open a browser and view [`http://localhost:8088`](http://localhost:8088)
to start your journey.

## Developing

While running, the container server will reload on modification of the Superset Python and JavaScript source code.
Don't forget to reload the page to take the new frontend into account though.

## Production

It is possible to run Superset in non-development mode by using [`docker-compose-non-dev.yml`](../docker-compose-non-dev.yml). This file excludes the volumes needed for development and uses [`./docker/.env-non-dev`](./.env-non-dev) which sets the variable `SUPERSET_ENV` to `production`.

## Resource Constraints

If you are attempting to build on macOS and it exits with 137 you need to increase your Docker resources. See instructions [here](https://docs.docker.com/docker-for-mac/#advanced) (search for memory)

```
- /volume5/storage/docker-data/superset/conf/docker/run-server.sh
```bash
#!/usr/bin/env bash
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
HYPHEN_SYMBOL='-'

gunicorn \
    --bind "${SUPERSET_BIND_ADDRESS:-0.0.0.0}:${SUPERSET_PORT:-8088}" \
    --access-logfile "${ACCESS_LOG_FILE:-$HYPHEN_SYMBOL}" \
    --error-logfile "${ERROR_LOG_FILE:-$HYPHEN_SYMBOL}" \
    --workers ${SERVER_WORKER_AMOUNT:-1} \
    --worker-class ${SERVER_WORKER_CLASS:-gthread} \
    --threads ${SERVER_THREADS_AMOUNT:-20} \
    --timeout ${GUNICORN_TIMEOUT:-60} \
    --limit-request-line ${SERVER_LIMIT_REQUEST_LINE:-0} \
    --limit-request-field_size ${SERVER_LIMIT_REQUEST_FIELD_SIZE:-0} \
    "${FLASK_APP}"
```
- /volume5/storage/docker-data/superset/conf/docker/pythonpath_dev/superset_config.py
```text
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# This file is included in the final Docker image and SHOULD be overridden when
# deploying the image to prod. Settings configured here are intended for use in local
# development environments. Also note that superset_config_docker.py is imported
# as a final step as a means to override "defaults" configured here
#
import logging
import os
from datetime import timedelta
from typing import Optional

from cachelib.file import FileSystemCache
from celery.schedules import crontab

logger = logging.getLogger()


def get_env_variable(var_name: str, default: Optional[str] = None) -> str:
    """Get the environment variable or raise exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = "The environment variable {} was missing, abort...".format(
                var_name
            )
            raise EnvironmentError(error_msg)


DATABASE_DIALECT = get_env_variable("DATABASE_DIALECT")
DATABASE_USER = get_env_variable("DATABASE_USER")
DATABASE_PASSWORD = get_env_variable("DATABASE_PASSWORD")
DATABASE_HOST = get_env_variable("DATABASE_HOST")
DATABASE_PORT = get_env_variable("DATABASE_PORT")
DATABASE_DB = get_env_variable("DATABASE_DB")

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = "%s://%s:%s@%s:%s/%s" % (
    DATABASE_DIALECT,
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_DB,
)

REDIS_HOST = get_env_variable("REDIS_HOST")
REDIS_PORT = get_env_variable("REDIS_PORT")
REDIS_CELERY_DB = get_env_variable("REDIS_CELERY_DB", "0")
REDIS_RESULTS_DB = get_env_variable("REDIS_RESULTS_DB", "1")

RESULTS_BACKEND = FileSystemCache("/app/superset_home/sqllab")


class CeleryConfig(object):
    BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    CELERY_IMPORTS = ("superset.sql_lab", "superset.tasks")
    CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    CELERYD_LOG_LEVEL = "DEBUG"
    CELERYD_PREFETCH_MULTIPLIER = 1
    CELERY_ACKS_LATE = False
    CELERYBEAT_SCHEDULE = {
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=10, hour=0),
        },
    }


CELERY_CONFIG = CeleryConfig

FEATURE_FLAGS = {"ALERT_REPORTS": True}
ALERT_REPORTS_NOTIFICATION_DRY_RUN = True
WEBDRIVER_BASEURL = "http://superset:8088/"
# The base URL for the email report hyperlinks.
WEBDRIVER_BASEURL_USER_FRIENDLY = WEBDRIVER_BASEURL

SQLLAB_CTAS_NO_LIMIT = True

#
# Optionally import superset_config_docker.py (which will have been included on
# the PYTHONPATH) in order to allow for local settings to be overridden
#
try:
    import superset_config_docker
    from superset_config_docker import *  # noqa

    logger.info(
        f"Loaded your Docker configuration at " f"[{superset_config_docker.__file__}]"
    )
except ImportError:
    logger.info("Using default Docker config...")
```
- /volume5/storage/docker-data/superset/conf/docker/pythonpath_dev/superset_config_local.example
```text
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# This is an example "local" configuration file. In order to set/override config
# options that ONLY apply to your local environment, simply copy/rename this file
# to docker/pythonpath/superset_config_docker.py
# It ends up being imported by docker/superset_config.py which is loaded by
# superset/config.py
#

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://pguser:pgpwd@some.host/superset"
SQLALCHEMY_ECHO = True
```
## docker-compose
```bash
docker-compose --project-name superset --file docker-compose.yaml up --detach --build --remove-orphans
```
```yaml
version: "3.9"
services:

  superset:
    image: apache/superset:latest-dev
    container_name: superset_app
    command: ["/app/docker/docker-bootstrap.sh", "app-gunicorn"]
    user: "root"
    restart: unless-stopped
    ports:
      - 8088:8088
    volumes: 
      - /volume5/storage/docker-data/superset/conf/docker/:/app/docker/
      - /volume5/storage/docker-data/superset/data/superset/:/app/superset_home
    environment:
      DATABASE_DB: superset
      DATABASE_HOST: <ip>
      DATABASE_PASSWORD: <password>
      DATABASE_USER: postgres
      DATABASE_PORT: 5432
      DATABASE_DIALECT: postgresql
      POSTGRES_DB: superset
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: <password>
      PYTHONPATH: /app/pythonpath:/app/docker/pythonpath_dev
      REDIS_HOST: <ip>
      REDIS_PORT: 6379
      FLASK_ENV: production
      SUPERSET_ENV: production
      SUPERSET_LOAD_EXAMPLES: "yes"
      CYPRESS_CONFIG: "false"
      SUPERSET_PORT: 8088

  superset-init:
    image: apache/superset:latest-dev
    container_name: superset_init
    command: ["/app/docker/docker-init.sh"]
    user: "root"
    volumes:
      - /volume5/storage/docker-data/superset/conf/docker/:/app/docker/
      - /volume5/storage/docker-data/superset/data/superset/:/app/superset_home
    environment:
      DATABASE_DB: superset
      DATABASE_HOST: <ip>
      DATABASE_PASSWORD: <password>
      DATABASE_USER: postgres
      DATABASE_PORT: 5432
      DATABASE_DIALECT: postgresql
      POSTGRES_DB: superset
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: <password>
      PYTHONPATH: /app/pythonpath:/app/docker/pythonpath_dev
      REDIS_HOST: <ip>
      REDIS_PORT: 6379
      FLASK_ENV: production
      SUPERSET_ENV: production
      SUPERSET_LOAD_EXAMPLES: "yes"
      CYPRESS_CONFIG: "false"
      SUPERSET_PORT: 8088

  superset-worker:
    image: apache/superset:latest-dev
    container_name: superset_worker
    command: ["/app/docker/docker-bootstrap.sh", "worker"]
    restart: unless-stopped
    user: "root"
    volumes:
      - /volume5/storage/docker-data/superset/conf/docker/:/app/docker/
      - /volume5/storage/docker-data/superset/data/superset/:/app/superset_home
    environment:
      DATABASE_DB: superset
      DATABASE_HOST: <ip>
      DATABASE_PASSWORD: <password>
      DATABASE_USER: postgres
      DATABASE_PORT: 5432
      DATABASE_DIALECT: postgresql
      POSTGRES_DB: superset
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: <password>
      PYTHONPATH: /app/pythonpath:/app/docker/pythonpath_dev
      REDIS_HOST: <ip>
      REDIS_PORT: 6379
      FLASK_ENV: production
      SUPERSET_ENV: production
      SUPERSET_LOAD_EXAMPLES: "yes"
      CYPRESS_CONFIG: "false"
      SUPERSET_PORT: 8088

  superset-worker-beat:
    image: apache/superset:latest-dev
    container_name: superset_worker_beat
    command: ["/app/docker/docker-bootstrap.sh", "beat"]
    restart: unless-stopped
    user: "root"
    volumes:
      - /volume5/storage/docker-data/superset/conf/docker/:/app/docker/
      - /volume5/storage/docker-data/superset/data/superset/:/app/superset_home
    environment:
      DATABASE_DB: superset
      DATABASE_HOST: <ip>
      DATABASE_PASSWORD: <password>
      DATABASE_USER: postgres
      DATABASE_PORT: 5432
      DATABASE_DIALECT: postgresql
      POSTGRES_DB: superset
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: <password>
      PYTHONPATH: /app/pythonpath:/app/docker/pythonpath_dev
      REDIS_HOST: <ip>
      REDIS_PORT: 6379
      FLASK_ENV: production
      SUPERSET_ENV: production
      SUPERSET_LOAD_EXAMPLES: "yes"
      CYPRESS_CONFIG: "false"
      SUPERSET_PORT: 8088


```