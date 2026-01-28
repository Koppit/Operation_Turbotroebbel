#!/usr/bin/env python
"""Diagnostic: Check what's in the database vs. what should be there."""
import json
import glob
import os

print("=" * 60)
print("DIAGNOSTIC: JSON vs. Database Comparison")
print("=" * 60)

# 1. Scan JSON for studies with/without location
studies_with_loc = 0
studies_without_loc = 0
locations_from_json = {}

print("\nScanning JSON files...")
for fp in sorted(glob.glob('json_for_processing/*.json')):
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for prog in data.get('study_programs', []):
            loc = prog.get('study_location') or {}
            if isinstance(loc, dict) and len(loc) > 0:
                studies_with_loc += 1
                for loc_key, loc_name in loc.items():
                    try:
                        loc_id = int(loc_key)
                        if loc_id not in locations_from_json:
                            locations_from_json[loc_id] = loc_name
                    except (ValueError, TypeError):
                        print(f"  WARNING: Invalid location_id '{loc_key}' in {os.path.basename(fp)}")
            else:
                studies_without_loc += 1
    except Exception as e:
        print(f"  ERROR reading {fp}: {e}")

print(f"\nJSON Statistics:")
print(f"  Studies WITH location: {studies_with_loc}")
print(f"  Studies WITHOUT location: {studies_without_loc}")
print(f"  Unique locations in JSON: {len(locations_from_json)}")
print(f"\nLocations in JSON:")
for loc_id in sorted(locations_from_json.keys()):
    print(f"    {loc_id}: {locations_from_json[loc_id]}")

# 2. Check database
print("\n" + "=" * 60)
print("Checking database...")
try:
    import pymysql
    conn = pymysql.connect(host='127.0.0.1', user='turbotroebbel', password='turbotroebbel', database='fagskolen', autocommit=True)
    cur = conn.cursor()

    # Total counts
    cur.execute('SELECT COUNT(*) FROM study_programs')
    total_studies = cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM study_place')
    total_places = cur.fetchone()[0]

    print(f"\nDatabase Statistics:")
    print(f"  Total study_programs: {total_studies}")
    print(f"  Total study_place rows: {total_places}")

    # Location breakdown
    cur.execute('SELECT location_id, location_name FROM study_place ORDER BY location_id')
    db_locs = {row[0]: row[1] for row in cur.fetchall()}
    print(f"\nLocations in database:")
    for loc_id in sorted(db_locs.keys()):
        print(f"    {loc_id}: {db_locs[loc_id]}")

    # Count studies per location
    cur.execute('SELECT location_id, COUNT(*) FROM study_programs WHERE location_id IS NOT NULL GROUP BY location_id ORDER BY location_id')
    counts = {row[0]: row[1] for row in cur.fetchall()}
    print(f"\nStudies per location (from study_programs table):")
    for loc_id in sorted(counts.keys()):
        print(f"    {loc_id}: {counts[loc_id]} studies")

    cur.execute('SELECT COUNT(*) FROM study_programs WHERE location_id IS NULL')
    null_loc = cur.fetchone()[0]
    print(f"  Studies with NULL location_id: {null_loc}")

    # Comparison
    print("\n" + "=" * 60)
    print("COMPARISON:")
    missing = set(locations_from_json.keys()) - set(db_locs.keys())
    extra = set(db_locs.keys()) - set(locations_from_json.keys())

    if missing:
        print(f"\n⚠️  MISSING from database ({len(missing)}):")
        for loc_id in sorted(missing):
            print(f"    {loc_id}: {locations_from_json[loc_id]}")
    else:
        print(f"\n✓ All JSON locations are in the database")

    if extra:
        print(f"\n⚠️  EXTRA in database ({len(extra)}):")
        for loc_id in sorted(extra):
            print(f"    {loc_id}: {db_locs[loc_id]}")

    # Name mismatches
    mismatched = []
    for loc_id in sorted(set(locations_from_json.keys()) & set(db_locs.keys())):
        if locations_from_json[loc_id] != db_locs[loc_id]:
            mismatched.append((loc_id, locations_from_json[loc_id], db_locs[loc_id]))

    if mismatched:
        print(f"\n⚠️  NAME MISMATCHES ({len(mismatched)}):")
        for loc_id, json_name, db_name in mismatched:
            print(f"    {loc_id}:")
            print(f"      JSON: {json_name}")
            print(f"      DB:   {db_name}")
    else:
        print(f"\n✓ No location name mismatches")

    cur.close()
    conn.close()

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
