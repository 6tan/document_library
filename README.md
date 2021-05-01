# Audio File Server

## pre requisite
#### Docker Compose 
If not installed please follow https://docs.docker.com/compose/install/

## setting up the system
clone the Repository using below command

`git clone https://github.com/6tan/SampleFlaskApp.git`

## How To Run
1. go to directory **SampleFlaskApp**
    
    `cd SampleFlaskApp`
2.  Run following command
    
    `sudo docker-compose up`

This will create postgres service and database with all necessary tables,
    Database schema can be found in **init.sql** file.
This also run our webapp service at `localhost:9876`

## API's

1. **CREATE**
    ```buildoutcfg
    url = /api/v1/audioFile/create
    method = POST
    content-type = application/json
    ```

    - **song**
        
        Request Body
        ```
        {
            "audioFileType":"song",
            "audioFileMetadata":{
                "duration_time": 12,
                "name":"sample"
                }
            }
        ```
    - **podcast**
        
        Request Body
        ```
        {
            "audioFileType":"podcast",
            "audioFileMetadata":{
                "duration_time":250,
                "name":"sample",
                "host":"sample-host",
                "participents":["sample1","sample2"]
            }
        }
        ```
    - **audiobook**
        
        Request Body
        ```
        {
            "audioFileType":"audiobook",
            "audioFileMetadata":{
                "duration_time": 223,
                "title":"sample",
                "author":"sampe author",
                "narrator":"sample narrator"
            }
        }
        ```
2. **UPDATE**

    ```buildoutcfg
    url = /api/v1/audioFile/<audioFileType>/<audioFileID> 
    method = PUT
    content-type = application/json
    ```
    Need to pass only metadata in json request which is going to be updated for given `<audioFileType>` and `<audioFileID>` 
    - **song**
        - url = /api/v1/audioFile/song/1
        - Request Body
        ```
        {
            "duration_time": 12,
            "name":"sample"
        }
        ```
    - **podcast**
        
        - url = /api/v1/audioFile/podcast/1
        - Request Body
        ```
        {
            "duration_time":250,
            "name":"sample",
            "host":"sample-host",
            "participents":["sample1","sample2"]
        }
        ```
    - **audiobook**
        
        - url = /api/v1/audioFile/audiobook/1
        - Request Body
        ```
        {
            "duration_time": 223,
            "title":"sample",
            "author":"sampe author",
            "narrator":"sample narrator"
        }
        ```
    
3. **DELETE**
    ```buildoutcfg
    url = /api/v1/audioFile/<audioFileType>/<audioFileID>
    method = DELETE
   ```
    
- **song**
    - url: `/api/v1/audioFile/song/1` - deletes song data with id 1
- **podcast**
    - url: `/api/v1/audioFile/podcast/1` - deletes podcast data with id 1
- **audiobook**
    - url : `/api/v1/audioFile/audiobook/1` - deletes audiobook data with id 1

4. GET
   ```buildoutcfg
   url = /api/v1/audioFile/<audioFileType> 
    - will return the specific audio file
   
   url = /api/v1/audioFile/<audioFileType>/<audioFileID> 
    - will return all the audio files of that type
   
   method = GET
   ```
   
    - song 
        - url = `/api/v1/audioFile/song` - return all song data
        - url = `/api/v1/audioFile/song/1` - return the specific song data with id 1       
           
    - podcast
        - url1 = `/api/v1/audioFile/podcast` - return all podcast data
        - url2 = `/api/v1/audioFile/podcast/1` - return the specific podcast data with id 1  
       
    - audiobook
        - url1 = `/api/v1/audioFile/audiobook` - return all audiobook data
        - url2 = `/api/v1/audioFile/audiobook/1` - return the specific audiobook data with id 1
    

### Response Status Code

    - Success: 200 OK
    - Success: 204 NO CONTENT (for get request when there is no data)
    - Invalid Request: 400 BAD REQUEST
    - Invalid URL: 404 NOT FOUND
    - Any Exception: 500 INTENAL SERVER ERROR