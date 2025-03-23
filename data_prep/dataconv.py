import pandas as pd
import json

def create_jsonl(input_file, output_file="output.jsonl"):

    try:
        with open(input_file, 'r') as infile:
            data = [json.loads(line) for line in infile]
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{input_file}'.")
        return

    with open(output_file, 'w') as outfile:
        for entry in data:
            if not isinstance(entry, dict):
                print(f"Warning: Skipping non-dictionary entry: {entry}")
                continue

            # --- Handle potential missing fields safely ----
            func = entry.get('func', '')
            cve_desc = entry.get('cve_desc', 'None')
            cve = entry.get('cve', 'None')
            cwe = entry.get('cwe', [])  # Default to empty list if 'cwe' is missing
            project = entry.get("project", "Unknown")

            conversation = [
                {
                    "content": f"Identify any vulnerabilities in the following code:\n\n```\n{func}\n```",
                    "role": "user"
                },
                {
                    "content": (
                        f"CVE Description: {cve_desc}\n"
                        f"CVE: {cve}\n"
                        f"CWE: {cwe}"
                    ),
                    "role": "assistant"
                }
            ]

            jsonl_line = {
                "conversations": conversation,
                "source": project,
               # "score": 0  #Default score
            }
            outfile.write(json.dumps(jsonl_line) + "\n")

    print(f"Successfully converted JSONL to JSONL and saved to {output_file}")


input_jsonl_file = './dataset/PrimeVul/primevul_valid.jsonl'
output_jsonl_file = 'valid.jsonl'
create_jsonl(input_jsonl_file, output_jsonl_file)