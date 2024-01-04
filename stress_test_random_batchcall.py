#!/bin/bash

# Set the endpoint URL
API_ENDPOINT="http://localhost:1313/predict"  # Update the port or path as needed

# Set the path to the JSON file
JSON_FILE="lib/data/test.json"  # Replace with the actual path

# Set the maximum number of data points for an API call
MAX_DATA_POINTS=10  # Adjust as needed

# Set the number of requests (n)
NUM_REQUESTS=10

# Create a log file for storing results
LOG_FILE="stress_test_results_batchcall.log"

# Get the total number of rows in the JSON file
TOTAL_ROWS=$(jq length "$JSON_FILE")
echo "Total Rows: $TOTAL_ROWS"

# Loop for stress testing
for ((i=1; i<=$NUM_REQUESTS; i++)); do
    # Generate a random number between 1 and MAX_DATA_POINTS
    NUM_DATA_POINTS=$((1 + RANDOM % MAX_DATA_POINTS))

    # Generate an array of random indices to select rows
    SELECTED_INDICES=($(shuf -i 0-$((TOTAL_ROWS-1)) -n "$NUM_DATA_POINTS"))

    # Construct a comma-separated list of indices
    INDICES_LIST=$(IFS=,; echo "${SELECTED_INDICES[*]}")

    # Extract the selected JSON rows using jq and format it as an array of objects
    JSON_DATA=$(jq --arg INDICES "$INDICES_LIST" '[.[$INDICES | split(",")[] | tonumber]]' "$JSON_FILE")

    echo "Request #$i - Selected Indices: $INDICES_LIST" 

    # Make the API call using curl and save the response to the log file
    RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d "$JSON_DATA" "$API_ENDPOINT")

    # Check if the API call was successful (HTTP status code 2xx)
    HTTP_STATUS=$(echo "$RESPONSE" | grep -Fi "HTTP" | awk '{print $2}')

    if [ "$HTTP_STATUS" != "200" ]; then
        echo "Request #$i - Successful Response (Status Code: $HTTP_STATUS): $RESPONSE" >> "$LOG_FILE"
    else
        echo "Request #$i - Failed Response (Status Code: $HTTP_STATUS): $RESPONSE" >> "$LOG_FILE"
    fi

    # Optional: Add sleep if needed to control the request rate
    # sleep 0.1  # Adjust the sleep duration as necessary
done
