import zlib
import base64
import json
import urllib.parse

def generate_mermaid_url(file_path):
    with open(file_path, 'r') as f:
        mermaid_code = f.read()
    
    state = {
        "code": mermaid_code,
        "mermaid": {
            "theme": "default"
        },
        "autoSync": True,
        "updateDiagram": True
    }
    
    json_str = json.dumps(state)
    # pako.deflate equivalent in python is zlib.compress but we drop the first 2 bytes (header) and last 4 bytes (checksum)?
    # Actually mermaid.live might use raw deflate.
    # Let's try standard standard base64 encoding of the code first, sometimes that works for simpler tools.
    # But mermaid.live specifically uses the pako method.
    
    # Let's attempt the standard pako deflate simulation
    # Javascript: pako.deflate(data, { level: 9 })
    # Python: zlib.compress(data, 9)
    
    compressed = zlib.compress(json_str.encode('utf-8'), 9)
    
    # Detailed check on mermaid.live encoding:
    # It constructs the URL as `https://mermaid.live/edit#pako:<base64_of_compressed>`
    # The base64 should be URL safe.
    
    # Standard zlib.compress produces a header. Pako might or might not. 
    # Let's try using the full compressed buffer.
    
    url_safe_b64 = base64.urlsafe_b64encode(compressed).decode('utf-8')
    
    url = f"https://mermaid.live/edit#pako:{url_safe_b64}"
    print(f"URL: {url}")

if __name__ == "__main__":
    generate_mermaid_url(r"c:\iiwii_db\y-it_agents\execution\source_vetting_workflow.mmd")
