import csv
import argparse

# Function to load the lookup table file
def load_lookup_table(lookup_file):
    lookup_table = {}
    with open(lookup_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # print(row)
            dst_port = int(row['dstport'].strip())
            protocol = row['protocol'].strip().lower()
            tag = row['tag'].strip().lower()
            lookup_table[(dst_port, protocol)] = tag
    return lookup_table

# Load protocol to numbers mappings from file
def load_protocol_mapping(protocol_file):
    protocol_mapping = {}
    with open(protocol_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            protocol_number = row['Decimal'].strip().lower()
            protocol_name = row['Keyword'].strip().lower()
            protocol_mapping[protocol_number] = protocol_name
    return protocol_mapping

# Process the flow log file and generate the tag count and port/protocol count files.
def process_flow_log(lookup_table, protocol_mappings, flow_log_file, tag_count_file, port_protocol_count_file):
    tag_counts = {}
    port_protocol_counts = {}

    with open(flow_log_file, 'r') as log_file:
        for line in log_file:
            fields = line.split()
            dst_port = int(fields[6].strip())               # 7th field (0-based index 6) is the dst port number
            protocol_number = fields[7].strip().lower()     # 8th field (0-based index 7) is the protocol number
            # Transalte the protocol number to the protocol keyword
            protocol_name = protocol_mappings.get(protocol_number, f"Unknown Protocol {protocol_number}")
            
            # Find tag from lookup table and update tag counts
            tag = lookup_table.get((dst_port, protocol_name), "Untagged").lower()
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
            # Update the protocol/port counts
            protocol_port_key = (dst_port, protocol_name)
            port_protocol_counts[protocol_port_key] = port_protocol_counts.get(protocol_port_key, 0) + 1

    # Write the results to the output files
    write_tag_counts(tag_count_file, tag_counts)
    write_port_protocol_counts(port_protocol_count_file, port_protocol_counts)

# Write the tag counts to a plain text file.
def write_tag_counts(tag_count_file, tag_counts):
    with open(tag_count_file, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['Tag', 'Count'])
        for tag, count in tag_counts.items():
            writer.writerow([tag, count])
        print(f"Output file {tag_count_file} generated sucessfully")

# Write the port/protocol counts to a plain text file.
def write_port_protocol_counts(port_protocol_count_file, port_protocol_counts):
    with open(port_protocol_count_file, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['Port','Protocol', 'Count'])
        for (dst_port, protocol), count in port_protocol_counts.items():
            writer.writerow([dst_port, protocol, count])
        print(f"Output file {port_protocol_count_file} generated sucessfully")

# driver program
def main():
    print("Script execution started")

    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Process flow logs and generate tag and port/protocol counts.")
    parser.add_argument('--lookup-table-file', required=True, help="Path to the lookup table file")
    parser.add_argument('--protocol-mappings-file', required=True, help="Path to the protocol mappings file")
    parser.add_argument('--flow-log-file', required=True, help="Path to the flow log file")
    parser.add_argument('--tag-count-file', required=True, help="Path to the output tag count file")
    parser.add_argument('--port-protocol-count-file', required=True, help="Path to the output port/protocol count file")
    
    args = parser.parse_args()
    print("Parsed required arguments for processing flow logs")

    # Read lookup_file and protocol_mappings_file
    lookup_table = load_lookup_table(args.lookup_table_file)
    protocol_mappings = load_protocol_mapping(args.protocol_mappings_file)
    print("Reading lookup table and protocol mappings file completed")

    # Process the flow log and generate the output files
    process_flow_log(lookup_table, protocol_mappings, args.flow_log_file, args.tag_count_file, args.port_protocol_count_file)
    print("Processing flow log files completed. Exiting the script!")

if __name__ == "__main__":
    main()