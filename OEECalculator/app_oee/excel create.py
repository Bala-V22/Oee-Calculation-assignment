import pandas as pd
from datetime import datetime, timedelta
import random

cycle_numbers = ['CN001', 'CN002', 'CN003']
unique_ids = [f'ID{i}' for i in range(1, 16)] 
material_names = ['Material 1', 'Material 2', 'Material 3']

production_logs = []
for _ in range(15):
    cycle_no = random.choice(cycle_numbers)
    unique_id = random.choice(unique_ids)
    material_name = random.choice(material_names)
    start_time = datetime.now() - timedelta(days=random.randint(1, 30))
    end_time = start_time + timedelta(hours=random.randint(1, 8))
    duration = (end_time - start_time).total_seconds() / 3600
    production_logs.append({
        'cycle_no': cycle_no,
        'unique_id': unique_id,
        'material_name': material_name,
        'start_time': start_time,
        'end_time': end_time,
        'duration': duration
    })


df = pd.DataFrame(production_logs)


file_path = 'production_logs.csv'
df.to_csv(file_path, index=False)

print("CSV file generated successfully:", file_path)
