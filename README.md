# API WEATHER

API Weather  connects to OpenWeather API, and teh request result is stored in 
a json file wich name is an identification entered by the user.

## Build the docker image
To buid the docker image, you must have docker installed.
In the root directory of the project run:

```bash
docker build -t api-weather-image .
```

## Run container
To run and create the container , you have to execute:
```
docker run -it --name api-weather-container  -e API_KEY=<your_api_key>  -p 8585:8585 api-weather-image 
```
Then open the browser in 0.0.0.0:8585, and you will see a welcome message.

## Usage
To execute each endpoint maybe you have Postman installed, you can excecute:
### To get the weather and store its information in a json file.
with POST method: 
http://127.0.0.1:8585/weather/ 
 
the body :
{
    "user_id": "<any_unique_identification>"
}

or with curl:

```
curl --location --request POST 'http://127.0.0.1:8585/weather/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "user_id": "<any_unique_identification>"
}'
```

### To get the download progress :
with GET method:
http://127.0.0.1:8585/download/progress/<any_unique_request_identification>

for example, if you have a request called "lucia"
http://127.0.0.1:8585/download/progress/lucia

## Comments
In this case I decided to store the list of the cities ids in a json file,
but it can be passed in  the body as a new field like:
"list_city_id" : [city_id_1, city_id_2, ...]