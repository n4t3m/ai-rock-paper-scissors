# rps server

This server will exist someway somehow on gcp

## Installation Instructions

1. Switch to server directory.
2. Create virtual environment `python3 -m venv venv`
3. Activate virtual environment `venv/Scripts/activate`
4. Install dependencies `python -m pip install -r requirements.txt`

## Runtime Intructions

- If developing, run server with `python -m flask run`
- If deploying, run server in tmux session `tmux` with `python -m flask run --host 0.0.0.0`

## Docker Deployment Instructions

1.  Switch to server directory
2.  Build image: `docker build -t rps-server .`
3.  Run container: `docker run -d -p 5000:5000 rps-server`
4.  Use container id to retrieve account credentials `docker logs <container id>`
