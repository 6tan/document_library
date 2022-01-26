# Document Management

## pre requisite
#### Docker Compose (if want to run in docker)

If not installed please follow https://docs.docker.com/compose/install/

## setting up the system
clone the Repository using below command

`git clone https://github.com/6tan/document_library.git`

## How To Run in docker compose
1. go to directory **document_library**
    
    `cd document_library`
2.  Run following command
    
    `docker-compose up`

    This runs our webapp service at `local_IP:9876`

## How to Run without docker
1. go to directory **document_library**

    `cd document_library`
2.  Run following command
    
    `python src/app/main.py`

## API's
Please find the swagger Api doc here


### Response Status Code

    - Success: 200 OK
    - Invalid Request: 400 BAD REQUEST
    - Invalid URL: 404 NOT FOUND
    - Any Exception: 500 INTENAL SERVER ERROR