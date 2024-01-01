#!/bin/bash

# Function to log an error
log_error() {
    echo "Error: $1" >> error.log
}

# Run main.py in the background
python main.py &

# Capture the PID (process ID) of the main.py process
main_pid=$!

# Sleep for a few seconds to allow main.py to start
sleep 5

# Run your Aria2 script
sh your_aria2_script.sh &

# Capture the PID of the Aria2 process
aria2_pid=$!

# Wait for user input to stop the processes
read -p "Press enter to stop the processes..."

# Stop main.py
kill $main_pid
echo "main.py process stopped."

# Stop Aria2 script
kill $aria2_pid
echo "Aria2 script process stopped."

# Log any errors from main.py
if [ -s error.log ]; then
    echo "Errors detected. See error.log for details."
else
    echo "No errors detected."
fi
