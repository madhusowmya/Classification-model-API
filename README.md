Classification Model deployment for production

The main objective of this project is to Prepare the model deployment for production and to wrap the modelcode inside an API, The model must be available via API call (port 1313). The call should pass 1 to N rows of data in JSON format, and expects a N responses each with a predicted class and probability belonging to the predicted clas.

That means for example, the below curl command with 1 to N rows the API should be able to handle either case with minimal impact to performance.The data passed in the below curl command must be able to process the same irrespective of the data size.

curl --request POST --url http://localhost:8080/predict --header 'content-type: application/json' --data '{"x0": "-1.018506", "x1": "-4.180869", "x2": "5.70305872366547", "x3": "-0.522021597308617", ...,"x99": "2.55535888"}'

Each of the 10,000 rows in the test dataset will be passed through an API call. This test can be individually made by passing the data(one row or two rows in data) in the curl command itself or the entire data of 10,000 rows passed through JSON file @data. The call could be a single batch call w/ all 10,000 rows, or 10,000 individual calls.


The results observed in one of the tests are as below,

curl --request POST --url http://localhost:1313/predict --header 'content-type: application/json' --data '[{"x0":0.042317,"x1":-3.344721,"x2":4.6351242122,"x3":-0.5983959993,"x4":-0.6477715046,"x5":"monday","x6":0.184902,"x7":46.690015,"x8":3.034132,"x9":0.364704,"x10":14.260733,"x11":-1.559332,"x12":"$5,547.78","x13":0.520324,"x14":31.212255,"x15":4.891671,"x16":0.357763,"x17":14.766366,"x18":-17.467243,"x19":0.224628,"x20":0.096752,"x21":1.305564,"x22":0.353632,"x23":3.909028,"x24":-91.273052,"x25":1.396952,"x26":4.401593,"x27":0.443086,"x28":14.048787,"x29":-0.932243,"x30":5.255472,"x31":"germany","x32":0.54199153,"x33":2.98948039,"x34":-1.78334189,"x35":0.80127315,"x36":-2.60231221,"x37":3.39682926,"x38":-1.22322646,"x39":-2.20977636,"x40":-68.69,"x41":522.25,"x42":-428.69,"x43":381.37,"x44":0.0197503,"x45":0.75116479,"x46":0.8630479008,"x47":-1.0383166613,"x48":-0.2726187635,"x49":-0.3430207259,"x50":0.3109008666,"x51":-0.797841974,"x52":-2.0390175153,"x53":0.87182889,"x54":0.14373012,"x55":-1.15212514,"x56":-2.1703139704,"x57":-0.267842962,"x58":0.212110633,"x59":1.6926559407,"x60":-0.9522767913,"x61":-0.8625864974,"x62":0.0748487158,"x63":"36.29%","x64":3.47125327,"x65":-3.16656509,"x66":0.65446814,"x67":14.60067029,"x68":-20.57521013,"x69":0.71083785,"x70":0.16983767,"x71":0.55082127,"x72":0.62814576,"x73":3.38608078,"x74":-112.45263714,"x75":1.48370808,"x76":1.77035368,"x77":0.75702363,"x78":"14.75731742","x79":-0.62550355,"x80":null,"x81":"October","x82":"Female","x83":-0.7116680715,"x84":-0.2653559892,"x85":0.5175495907,"x86":-1.0881027092,"x87":-1.8188638198,"x88":-1.3584469527,"x89":-0.654995195,"x90":-0.4933042262,"x91":0.373853,"x92":0.94143481,"x93":3.54679834,"x94":-99.8574882,"x95":0.403926,"x96":1.65378726,"x97":0.00771459,"x98":-32.02164582,"x99":-60.3127828}]'

[{"probability_positiveclass":0.3496745319,"selected_features":["x53","x44","x81","x12","x31","x58","x5","x62","x91","x56"],"predicted_class":0}]

The API is wrapped inside a docker image by following the docker commands which will create a docker image and run the image to deploy,A simple docker file Dockerfile created that contains a set of instructions for building a Docker image. It specifies the steps to create a containerized environment for running an application. 

root/
|--lib/
|   |-- model_components/
|   |  |-- imputer.pkl
|   |  |-- scaler.pkl
|   |  |-- model.pkl
|   |-- data/
|   |  |   |   |    |-- test.json
|-- flaskapp.py
|-- prerocess_input_json.py
|-- requirements.txt
|-- commands.txt
|-- docker-compose.yaml
|-- Dockerfile
|--run_api.sh
|-- setup.sh
|--stress_test.sh
|-- README.md


## Installation and Testing the application

To set up the project, follow these steps:

1. Clone the repository to your local machine:

    ```bash
    git clone
    ```

2. Navigate to the project directory:

    ```bash
    cd MLapplication
    ```

3. Create virtual env with the following bash command

    ```bash
    python -m venv venv 
    source venv/bin/activate
    ```
4. Activate virtual environment 

    ```bash
    source venv/bin/activate
    ```
5. Run the custom setup script to install dependencies and set up the environment:

    ```bash
    ./setup.sh
    ```
6. Make sure you have the required dependencies installed. You can install them using:

    ```bash
    pip install -r requirements.txt
    ```
7. Start the application with the following command

    ```bash
    python flaskapp.py
    ```
8. Test the functionaly of the data producing results in another terminal with foolowing curl command or by running shell script. 
    Three techniques to test the functionality and data adaptability of the application hosted with flask to predict the class and get the probbaility of positive class and the fetaures.

        1. Directly hit the curl command with data in batch call as in commands.txt
        2. Test with stress_test.sh with simple commands and save the results in log file (10,000 individual api calls)

            ```bash
            chmod +x stress_test.sh
            ./stress_test.sh 
            ``` 
        3. Curl command with including all 10,000 rows in a json file

            ```bash
            curl --request POST --url http://localhost:1313/predict --header 'content-type: application'/json --data @'lib/data/test.json'
            ./stress_test.sh 
            ```     
Running the stress_test_random.sh scrpt randomly selects individual data points for class prediction from test.json file
Running the stress_test_random_batchcall.sh scrpt randomly selects individual batches of data points for class prediction from test.json
Results stored in specified log file in the sh scripts.

9. Build the docker image (name:class-prediction) with Dockerfile and Deploy the application in docker container with run_api.sh

    ```bash
    docker build -t class-prediction
    docker run -p 1313:1313 class-prediction
    ```

10. Start the defined services in the docker-compose.yml like scaling up and down based on the cpu resource usage 

    ```bash
    docker-compose up
    docker-compose down
    ```
Running the stress_test_random.sh scrpt randomly selects individual data points for class prediction from test.json file
Running the stress_test_random_batchcall.sh scrpt randomly selects individual batches of data points for class prediction from test.json

