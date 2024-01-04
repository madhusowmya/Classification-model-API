#!/bin/bash

# Set the endpoint URL
API_ENDPOINT="http://localhost:1313/predict"  # Update the port or path as needed

# Set the path to the JSON file
JSON_FILE="lib/data/test.json"  # Replace with the actual path

# Set the number of requests (n)
NUM_REQUESTS=10

# Create a log file for storing results
LOG_FILE="stress_test_results.log"

# Get the total number of rows in the JSON file
TOTAL_ROWS=$(jq length "$JSON_FILE")
echo "Total Rows: $TOTAL_ROWS"

# Loop for stress testing
for ((i=1; i<=$NUM_REQUESTS; i++)); do
    # Generate a random index to select a row
    RANDOM_INDEX=$((RANDOM % TOTAL_ROWS))
    echo "Request #$i - Selected Indices: $RANDOM_INDEX" 

    # Extract the selected JSON row using jq and surround it with square brackets
    JSON_DATA=$(jq --argjson INDEX "$RANDOM_INDEX" '[.[$INDEX]]' "$JSON_FILE")

    # Make the API call using curl and save the response to the log file
    RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d "$JSON_DATA" "$API_ENDPOINT")

    # Check if the API call was successful (HTTP status code 2xx)
    HTTP_STATUS=$(echo "$RESPONSE" | grep -Fi "HTTP" | awk '{print $2}')

    if [ "$STATUS_CODE" == "200" ]; then
    echo "Request #$i - Failed Response (Status Code: "$STATUS_CODE"): $RESPONSE" >> "$LOG_FILE"
    else
    echo "Request #$i - Successful Response (Status Code: "$STATUS_CODE"): $RESPONSE" >> "$LOG_FILE"
    fi  

    # Optional: Add sleep if needed to control the request rate
    # sleep 0.1  # Adjust the sleep duration as necessary
done
