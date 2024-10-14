# OPNSense - Generate ISC DHCP Static IP Config Generator


This script is designed to generate DHCP static IP reservation into an OPNSense-compatible XML format to be used with ISC DHCP available in OPNsense. This script only handles ipv4 currently. 

**Key Features**
1. Input CSV Handling:

  * Reads a CSV file that contains fields for hostname, MAC address, IP address, and optional fields like description, WINS server, DNS server, and NTP server.

2. Data Validation:

  * Hostname Validation: Ensures hostnames are DHCP compliant (alphanumeric, hyphens allowed, no underscores, and starts with a letter).

  * MAC Address Validation: Validates MAC addresses against standard formats, allowing both colon (:) and hyphen (-) delimiters.

  * IP Address Validation: Checks if the IP addresses are valid IPv4 addresses and validates WINS server, DNS server, and NTP server against RFC 1918 private IP address ranges.

3. Hostname Normalization:

  * Converts hostnames to lowercase.
  * Replaces spaces and underscores with hyphens to ensure compliance with DHCP requirements.

4. XML Generation:

  * Creates a structured XML document that adheres to OPNSense's configuration format.
  * Generates XML tags for all specified fields, including empty tags for any missing values, ensuring a complete XML structure.

5. XML Beautification:

  * The output XML is formatted and indented for better readability using the minidom library, making it easier to inspect and troubleshoot.

6. Command-Line Interface:

  * Utilizes the argparse library to accept input and output file paths as command-line arguments, allowing for flexible use without modifying the script.

7. Error Handling:

  * The script does not currently include detailed error handling for CSV reading or XML writing errors but can be extended to handle such scenarios gracefully.

8. Flexible CSV Structure:

  * Supports optional fields, allowing users to include only the data they need, while still generating complete XML entries.

9. Modular Design:

  * The script is modular, with functions dedicated to specific tasks (validation, XML generation, etc.), making it easy to extend or modify specific features.


## Dependencies
Here are the dependencies required to run the provided Python script, along with the compatible Python versions:

### Python Version
Python 3.6 or later is required to ensure compatibility with features such as f-strings and the ipaddress module.

### Required Libraries
The script uses built-in libraries, so you don't need to install any external packages. Here are the libraries used in the script:

1. csv: For reading the CSV file.
2. re: For regular expression matching.
3. ipaddress: For validating IP addresses.
4. xml.etree.ElementTree: For creating and manipulating XML data.
5. argparse: For parsing command-line arguments.
6. xml.dom.minidom: For prettifying the XML output.


## Usage

```
python dhcp-static-opnsense.py input_data.csv opnsense_output.xml
```
_OR_
```
python3 dhcp-static-opnsense.py input_data.csv opnsense_output.xml

```

## Sample CSV Input

```
hostname,mac_address,ip_address,descr,winsserver,dnsserver,ntpserver
Unifi Usw Home Main Switch,ac:8b:a9:bf:5f:7e,192.168.248.2,Main Switch,,8.8.8.8,129.6.15.28
Test_Switch_1,ac:8b:a9:bf:5f:7f,192.168.248.4,Test Switch,192.168.248.5,8.8.4.4,
```

## Sample XML Output

```
<?xml version="1.0" ?>
<opnsense>
    <dhcpd>
        <lan>
            <staticmap>
                <mac>ac:8b:a9:bf:5f:7e</mac>
                <ipaddr>192.168.248.2</ipaddr>
                <hostname>unifi-usw-home-main-switch</hostname>
                <descr>Main Switch</descr>
                <winsserver></winsserver>
                <dnsserver>8.8.8.8</dnsserver>
                <ntpserver>129.6.15.28</ntpserver>
            </staticmap>
            <staticmap>
                <mac>ac:8b:a9:bf:5f:7f</mac>
                <ipaddr>192.168.248.4</ipaddr>
                <hostname>test-switch-1</hostname>
                <descr>Test Switch</descr>
                <winsserver>192.168.248.5</winsserver>
                <dnsserver>8.8.4.4</dnsserver>
                <ntpserver></ntpserver>
            </staticmap>
        </lan>
    </dhcpd>
</opnsense>
```
