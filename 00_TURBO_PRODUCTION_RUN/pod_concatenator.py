import os

# CONFIGURATION
INPUT_DIR = r"c:\iiwii_db\y-it_agents\00_TURBO_PRODUCTION_RUN\synthetic_cases"
OUTPUT_DIR = r"c:\iiwii_db\y-it_agents\00_TURBO_PRODUCTION_RUN\mega_pillars"
SOURCES_PER_PILLAR = 500

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    case_files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".md")])
    total_cases = len(case_files)
    
    print(f"Aggregating {total_cases} cases into Mega-Pillars...")
    
    pillar_index = 1
    for i in range(0, total_cases, SOURCES_PER_PILLAR):
        batch = case_files[i:i + SOURCES_PER_PILLAR]
        pillar_filename = os.path.join(OUTPUT_DIR, f"POD_TURBO_MEGA_PILLAR_{pillar_index:02d}.md")
        
        with open(pillar_filename, "w", encoding="utf-8") as outfile:
            outfile.write(f"# POD INDUSTRIAL MEGA-PILLAR {pillar_index:02d}\n\n")
            outfile.write(f"Contains cases {i+1} to {min(i+SOURCES_PER_PILLAR, total_cases)}\n\n")
            
            for case_file in batch:
                with open(os.path.join(INPUT_DIR, case_file), "r", encoding="utf-8") as infile:
                    outfile.write(infile.read())
                    outfile.write("\n\n---\n\n")
        
        print(f"Created: {pillar_filename}")
        pillar_index += 1

if __name__ == "__main__":
    main()
