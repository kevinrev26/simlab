# SimLab

This is a simulation orchestration tool for running ai specs and docker in mutiprocess environments to generate results for every run.

## Architecture

These are the components:

- **API:** A simple fastapi endpoints to control the simulations and retrieve results.

- **Job Queue:** A rabbit mq classic job queue and process workers.

- **Worker pods:** The pods that runs the simulation.

- **Postgres:** Database to store the results and analyzing.

## Schema v1
- **schema_version**: The version of the current contract schema for creating simulations.
- **uuid**: A uuid4 string generated from client side.
- **name**: A simple name for this simulation.
- **label (optional)**: A word drescribing what is this simulation, could be experiment1.1 or something meaningful for the dev.
- **priority**: If you are running a lot of simulations, which image should run first?
- **runtime.runs_per_container**: How many runs or iterations should a container run inside?
- **runtime.image_name**: What is the image that you build and want to run?
- **runtime.image_tag**: What is the tag of the image?
- **runtime.parameters.entrypoint_args (optional)**: How the image should run?
- **runtime.parameters.env_vars (optional)**: Are there any env variables to run the container?
- **resources.cpu_limit**: Is there any limit that you want to test?
- **resources.memory_limmit**: How many space do the simulation should take to run?
- **resources.max_containers**: The amount of containers that should run in parallel
- **reosources.max_duration_seconds:** How many seconds a simulation should finished?
- **behavior.seed**: For AI runs and reproducibility.
- **behavior.timeout_seconds**: Kill the container if this threshold is passed.
- **behavior.max_attempts**: How many retries the worker should attempt?
- **storage.volume_name**: To retrieve the results, the data is stored in this volume inside the container, what is the name of that volume?
- **storage.output_path**: The directory where the data is stored in the container.
- **observability.log_level**: Debug, info, warning or error.
- **observability.metrics_enabled**: To collect how many resources each run usage.
- **observability.webhook_url (optional)**: If tou need for some reason a notification when the sim is finished.

The above is passed to the `/api/simulation` endpoint as a POST request.