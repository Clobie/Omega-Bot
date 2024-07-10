def format_emojis_file(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as infile, \
         open(output_filename, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            # Remove newline character
            line = line.strip()
            
            # Add double quotes and comma
            formatted_line = f'"{line}",\n'
            
            # Write formatted line to output file
            outfile.write(formatted_line)

# Example usage:
input_filename = 'emojis.txt'
output_filename = 'formatted_emojis.txt'
format_emojis_file(input_filename, output_filename)
