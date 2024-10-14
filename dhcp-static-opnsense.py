import csv
import re
import ipaddress
import xml.etree.ElementTree as ET
import argparse
from xml.dom import minidom

# Validate hostname (DHCP compliant: alphanumeric, hyphens allowed, no underscores, starts with letter)
def validate_hostname(hostname):
    if len(hostname) > 63:
        return False
    return bool(re.match(r"^[a-zA-Z]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$", hostname))

# Fix hostname (replace spaces and underscores with hyphens, make it DHCP compliant)
def fix_hostname(hostname):
    # Replace spaces and underscores with hyphens
    hostname = re.sub(r'[ _]', '-', hostname)
    # Ensure that it starts with an alphabetic character and ends with alphanumeric characters
    # (trim to 63 characters max for hostname)
    hostname = re.sub(r'[^a-zA-Z0-9-]', '', hostname).strip('-')
    return hostname[:63]  # Ensure maximum length is 63 characters

# Validate MAC address (supporting both ':' and '-' delimiters, case insensitive)
def validate_mac(mac):
    return bool(re.match(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", mac))

# Validate IP address (RFC 1918 ranges for private IPs)
def validate_rfc1918_ip(ip):
    try:
        ip_obj = ipaddress.IPv4Address(ip)
        return ip_obj.is_private
    except ipaddress.AddressValueError:
        return False

# Validate IP address (general)
def validate_ip(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False

# Function to beautify the XML output
def prettify_xml(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")

# Convert to OPNSense format (XML output)
def generate_opnsense_xml(input_file, output_file):
    root = ET.Element("opnsense")
    dhcpd = ET.SubElement(root, "dhcpd")
    lan = ET.SubElement(dhcpd, "lan")

    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            hostname = row['hostname'].strip()
            mac_address = row['mac_address'].strip()
            ip_address = row['ip_address'].strip()
            descr = row.get('descr', '').strip()  # Optional
            winsserver = row.get('winsserver', '').strip()
            dnsserver = row.get('dnsserver', '').strip()
            ntpserver = row.get('ntpserver', '').strip()

            # Fix the hostname to make it DHCP compliant and convert to lowercase
            hostname = fix_hostname(hostname).lower()

            # Create XML entry for each valid row
            staticmap = ET.SubElement(lan, "staticmap")
            mac = ET.SubElement(staticmap, "mac")
            mac.text = mac_address if mac_address else ""
            ipaddr = ET.SubElement(staticmap, "ipaddr")
            ipaddr.text = ip_address if ip_address else ""
            hostname_xml = ET.SubElement(staticmap, "hostname")
            hostname_xml.text = hostname if hostname else ""

            descr_xml = ET.SubElement(staticmap, "descr")
            descr_xml.text = descr if descr else ""
            
            winsserver_xml = ET.SubElement(staticmap, "winsserver")
            winsserver_xml.text = winsserver if winsserver else ""
            
            dnsserver_xml = ET.SubElement(staticmap, "dnsserver")
            dnsserver_xml.text = dnsserver if dnsserver else ""
            
            ntpserver_xml = ET.SubElement(staticmap, "ntpserver")
            ntpserver_xml.text = ntpserver if ntpserver else ""

    # Beautify and write the XML output to a file
    pretty_xml_string = prettify_xml(root)

    with open(output_file, 'w') as xmlfile:
        xmlfile.write(pretty_xml_string)

    print("OPNSense XML output written to {}".format(output_file))

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Convert CSV to OPNSense DHCP static map XML")
    parser.add_argument('input_csv', help="Path to the input CSV file")
    parser.add_argument('output_xml', help="Path to the output XML file")
    
    args = parser.parse_args()
    
    generate_opnsense_xml(args.input_csv, args.output_xml)

if __name__ == "__main__":
    main()
