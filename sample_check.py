import json
import glob

# Quick scan without DB
locations = {}
studies_with = 0
studies_without = 0

for fp in sorted(glob.glob('json_for_processing/*.json'))[:5]:  # First 5 files
    with open(fp, 'r', encoding='utf-8') as f:
        data = json.load(f)
    filename = fp.split('\\')[-1]
    for prog in data.get('study_programs', []):
        loc = prog.get('study_location') or {}
        if isinstance(loc, dict) and len(loc) > 0:
            studies_with += 1
            for k, v in loc.items():
                try:
                    locations[int(k)] = v
                except:
                    pass
        else:
            studies_without += 1

print(f"Sample (first 5 files):")
print(f"  Studies with location: {studies_with}")
print(f"  Studies without location: {studies_without}")
print(f"  Unique locations: {locations}")
