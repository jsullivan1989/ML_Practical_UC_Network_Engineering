import getpass

# Input password using getpass 

pw = getpass.getpass()

# Use Case 1, determine number of BGP routes on <hostname> that is within normal.
# Optional: use the 'table' or 'logical-system' option if running in non-default RT or LS
# "show route summary table <route-table>.inet.0 | match BGP " will output a number
# What is the correct upper and lower threshold?
# But a suitable threshold will vary over time, so we need to implement 
# a way to identify the normal number
# Example output,
# username@<hostname> show route summary table <route-table>.inet.0 | match BGP
#               BGP:   2838 routes,   606 active


import paramiko
import sys
import os
import time
import re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import numpy as np
import csv
import io 

os.system("rm Current_BGP_Routes.csv")


hostname = '<hostname>'
password = pw
username = '<username>
# Use different port if using nonstandard SSH port
port = 22

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=hostname, port=port, username=username, password=password)
x = []
y = []
count = 0
# gather 10 outputs
while count < 10:
    time.sleep(1)
    command = "show route summary table <route-table>.inet.0 | match BGP"
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode()
    print(output)
    # Use the regex command to parse and find the Total and Active Routes
    # We are interested in the Total routes due to more volatility
    BGP_Routes = re.findall(r"[\d]+", output)
    print(BGP_Routes)
    Total_BGP_Routes = BGP_Routes[0]
    Active_BGP_Routes = BGP_Routes[1]
    # Convert to Integer for Plotting
    Total_BGP_Routes = int(Total_BGP_Routes)
    now = datetime.datetime.now()

    
    # Gather the date and time, the next several lines capture the output of the 
    # now variable so that a proper date and time can be stored in our CSV file
    # Redirect standard output to a StringIO object for the current date/time

    
    string_io = io.StringIO()
    sys.stdout = string_io

    # Gather current time as output
    print(now)

    # Restore standard output
    sys.stdout = sys.__stdout__

    # Get the captured output
    current_date_time_string = string_io.getvalue()

    # Print the captured output
    print(current_date_time_string)
    print(current_date_time_string)
    # Append the current date time to a list that will append to be used on the X Axis
    x.append(current_date_time_string)
    y.append(Total_BGP_Routes)
    count += 1
    # Increment the counter by 1 in order to capture 10 (x , y) outputs


# Rotate date labels for better readability
fig.autofmt_xdate()

fig, ax = plt.subplots()
ax.plot(x, y)


date_format = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
ax.xaxis.set_major_formatter(date_format)

# Instantiate a variable for your line graph, comma after line unpacks the list 

line, = ax.plot(x, y)
data = line.get_data()



# Export to CSV that maps the BGP routes at the time the command was run

with open('Current_BGP_Routes.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['date/time', 'Total BGP Routes'])  # Write header
    for i in range(len(data[0])):
        writer.writerow([data[0][i], data[1][i]])

client.close()
