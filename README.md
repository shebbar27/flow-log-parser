# Flow Log Parser

A Python program to parse the AWS flow log files (version 2), match the destination port (dstport) and protocol to a tag from a lookup table, and then generate two output files: one for the tag counts and the other for the destination port/protocol combination counts.

### How to run the script:
User must provide path to the input files - lookup table file, protocol mappings file, flow log file, as well as output files - tag counts file and port protocol counts file in the commandline.

##### Sample commandline intput:
```
python src/main.py --lookup-table-file res/lookup_table.txt --protocol-mappings-file res/protocol_mappings.txt --flow-log-file res/flow_log.txt --tag-count-file out/tag_counts.txt --port-protocol-count-file out/port_protocol_counts.txt
```

The program will overwrite the output file if already present.

### Assumptions made:
- Flow log file is a flow log version 2 file in Default format as described here https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html.
- The protocol numbers used in flow log file are assumed to be one among the standard protocols defined in https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml, if not then it is considered as Unknown protocol.
- For combinations of port numbers and protocols not present in the lookup table file are considered as untagged.

### Testing done:
- Flow logs containing multiple instances of port and protocol combinations are counted correctly, tag counts and port protocol counts are accurate.
- Multiple port protocol combinations linked to same tag are counted correctly in the tag counts and port protocol counts output file.
- Verified that the untagged counts are accurate.
- Verified that sum of all port protocol counts and sum of all tag counts are equal and it matches the number of lines in the flow log file.