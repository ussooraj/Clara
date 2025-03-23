import pandas as pd
import numpy as np
import json

def handle_large_numbers(obj):
    """Converts large numbers to strings to avoid ValueError."""
    for key, value in obj.items():
        if isinstance(value, int) and value > 2**32:
            obj[key] = str(value)
    return obj

with open('./dataset/PrimeVul/primevul_valid.jsonl', 'r') as f:
    data = [json.loads(line, object_hook=handle_large_numbers) for line in f]

df = pd.DataFrame(data)
print(df)

col_remove = ['idx', 'nvd_url', 'commit_id', 'project_url', 'commit_url', 'commit_message', 'target', 'func_hash', 'file_name', 'file_hash']
df = df.drop(columns = col_remove)
print(df)

df.to_json('./dataset/PrimeVul/primevul_valid.jsonl', lines=True, orient='records')
