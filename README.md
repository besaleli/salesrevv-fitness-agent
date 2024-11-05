# salesrevv-fitness-agent

## Setup
First, run `cp .env.example .env` and fill out all empty fields for API keys etc.

Then, run `docker compose up`.

Once *all* services are running and ready (the model service takes a second since it's downloading weights – could be optimized later), run `make backfill`. This will get all documents into the vector database.

The app will be running on `http://localhost:8501`.
