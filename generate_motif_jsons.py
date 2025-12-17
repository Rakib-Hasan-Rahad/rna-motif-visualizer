import csv
import json
import os
from collections import defaultdict

def parse_location(location_str):
    """Parse location string like '77-82/92-100' into residue ranges"""
    parts = location_str.split('/')
    ranges = []
    for part in parts:
        start, end = map(int, part.split('-'))
        ranges.append({'start': start, 'end': end})
    return ranges

def create_motif_entry(motif_name, ranking, chain, location, motif_id):
    """Create a motif entry dict for JSON output"""
    ranges = parse_location(location)
    
    # Extract all residues from the ranges
    residues = []
    for range_obj in ranges:
        residues.extend(list(range(range_obj['start'], range_obj['end'] + 1)))
    
    # Partner residues are from the second range
    partner_residues = []
    if len(ranges) > 1:
        partner_residues = list(range(ranges[1]['start'], ranges[1]['end'] + 1))
    
    entry = {
        "chain": str(chain),
        "residues": residues[:len(residues)//2] if len(ranges) > 1 else residues,
        "motif_id": motif_id,
        "description": f"{motif_name} rank {ranking}",
        "partner_residues": partner_residues,
        "ranking": ranking,
        "location": location
    }
    
    return entry

def main():
    csv_file = '/Users/rakibhasanrahad/plugin/rna-motif-visualizer/rna_motif_visualizer/motif_database/motifs.csv'
    db_dir = '/Users/rakibhasanrahad/plugin/rna-motif-visualizer/rna_motif_visualizer/motif_database'
    
    # Dictionary to group motifs by type
    motifs_by_type = defaultdict(lambda: defaultdict(list))
    
    # Read CSV and organize data
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            motif_type = row['Motif'].strip()
            ranking = int(row['Ranking'])
            chain = row['Chain'].strip()
            location = row['Location'].strip()
            
            entry = create_motif_entry(motif_type, ranking, chain, location, f"{motif_type.replace(' ', '_')}{ranking}")
            
            # Use a PDB ID placeholder (can be enhanced if needed)
            pdb_id = "RNA_STRUCTURE"  # Generic placeholder
            motifs_by_type[motif_type][pdb_id].append(entry)
    
    # Create JSON files for each motif type
    motif_file_mapping = {
        'Kink-turn': 'kink_turn.json',
        'C-loop': 'c_loop.json',
        'Sarcin-ricin': 'sarcin_ricin.json',
        'Reverse kink-turn': 'reverse_kink_turn.json',
        'E-loop': 'e_loop.json'
    }
    
    for motif_type, motif_file in motif_file_mapping.items():
        output_path = os.path.join(db_dir, motif_file)
        
        # Prepare data for this motif type
        motif_data = {}
        if motif_type in motifs_by_type:
            for pdb_id, entries in motifs_by_type[motif_type].items():
                motif_data[pdb_id] = entries
        
        # Write JSON file
        with open(output_path, 'w') as f:
            json.dump(motif_data, f, indent=2)
        
        print(f"✓ Created {motif_file} with {len(motifs_by_type.get(motif_type, {}).get('RNA_STRUCTURE', []))} entries")

if __name__ == '__main__':
    main()
