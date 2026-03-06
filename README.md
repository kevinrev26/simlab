# SimLab

This is a simulation orchestration tool for running ai specs and docker in mutiprocess environments to generate results for every run.

## Architecture

These are the components:

- **API:** A simple fastapi endpoints to control the simulations and retrieve results.

- **Job Queue:** A rabbit mq classic job queue and process workers.

- **Worker pods:** The pods that runs the simulation.

- **Postgres:** Database to store the results and analyzing.