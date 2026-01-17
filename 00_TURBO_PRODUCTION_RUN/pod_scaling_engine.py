import json
import requests
import random
import os

# CONFIGURATION
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"
OUTPUT_DIR = r"c:\iiwii_db\y-it_agents\00_TURBO_PRODUCTION_RUN\synthetic_cases"
TARGET_COUNT = 4900 # Reaching towards 5,000 total with existing sources

# POD FAILURE MODES
FAILURE_MODES = [
    "Ad-Spend Burn: Spending hundreds on ads for negligible profit.",
    "IP Sweep: Shop closure due to unintentional trademark/copyright infringement.",
    "The 1,200-Design Death March: Design saturation with zero organic sales.",
    "Quality Control Collapse: High return rates due to poor supplier quality.",
    "The Sample Gap: Not testing products before listing, leading to bad reviews.",
    "Platform Ban: VPN or payout policy violations.",
    "Niche Saturation: Entering a high-competition niche with low-quality designs."
]

NICHES = [
    "Sarcastic Developer", "Over-caffeinated Mom", "Boho Plant Parent", 
    "Retro Gaming", "Minimalist Hiking", "Specific Dog Breed Lovers",
    "Obscure Hobbyist", "Mid-Century Modern Decor", "Stoic Motivation"
]

PLATFORMS = ["Etsy", "Amazon Merch", "Shopify + FB Ads", "Redbubble", "Printful Direct"]

def generate_case(index):
    failure = random.choice(FAILURE_MODES)
    niche = random.choice(NICHES)
    platform = random.choice(PLATFORMS)
    
    prompt = f"""
    Generate a short, high-fidelity satirical POD failure case study.
    Niche: {niche}
    Platform: {platform}
    Core Failure: {failure}
    
    Format:
    ### Case POD-SHADOW-{index:04d}
    - **Niche**: {niche}
    - **Platform**: {platform}
    - **Metrics**: Loss: ${random.randint(500, 5000)}, Efficiency: {random.randint(-50, 5)}%
    - **Critical Failure**: [Specific satirical detail about the failure]
    
    Tag: SYNTH
    """
    
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        return response.json().get('response', '')
    except Exception as e:
        print(f"Error generating case {index}: {e}")
        return None

import argparse
from concurrent.futures import ThreadPoolExecutor

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--count", type=int, default=4900)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print(f"Starting Parallel Industrial Scaling for POD... Range: {args.start} to {args.start + args.count - 1} with {args.workers} workers.")
    
    def process_case(i):
        case_content = generate_case(i)
        if case_content:
            with open(os.path.join(OUTPUT_DIR, f"case_{i:04d}.md"), "w", encoding="utf-8") as f:
                f.write(case_content)
            return True
        return False

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        list(executor.map(process_case, range(args.start, args.start + args.count)))

    print("Generation complete.")

if __name__ == "__main__":
    main()
