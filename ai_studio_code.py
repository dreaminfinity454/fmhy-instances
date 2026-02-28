import requests
import json
import time
from datetime import datetime, timezone

# List of FMHY instances to track
INSTANCES =[
    {"name": "Official", "url": "https://fmhy.net"},
    {"name": "Clone Pages", "url": "https://fmhyclone.pages.dev"},
    {"name": "Main Pages", "url": "https://fmhy.pages.dev"},
    {"name": "Fast Archive", "url": "https://ffmhy.pages.dev"},
]

def check_instance(instance):
    result = {
        "name": instance["name"],
        "url": instance["url"],
        "status": "Offline",
        "safe": False,
        "search_works": False,
        "response_time": 0
    }
    
    try:
        start_time = time.time()
        # 10 second timeout
        response = requests.get(instance["url"], timeout=10)
        result["response_time"] = round((time.time() - start_time) * 1000) # in ms
        
        if response.status_code == 200:
            result["status"] = "Online"
            
            # SAFETY CHECK: Verify it hasn't been hijacked by domain squatters
            # Check for standard FMHY text or specific HTML tags
            if "FreeMediaHeckYeah" in response.text or "FMHY" in response.text:
                result["safe"] = True
                
            # SERVICE CHECK: Check if the search index exists (for Docusaurus/static search)
            # You can customize this endpoint based on how FMHY handles search
            search_response = requests.get(f"{instance['url']}/search-index.json", timeout=5)
            if search_response.status_code == 200:
                result["search_works"] = True

    except requests.RequestException:
        pass # Stays marked as offline/unsafe
        
    return result

def main():
    results = []
    for instance in INSTANCES:
        print(f"Checking {instance['name']}...")
        results.append(check_instance(instance))
        
    output = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "instances": results
    }
    
    # Save to a JSON file
    with open("status.json", "w") as f:
        json.dump(output, f, indent=4)

if __name__ == "__main__":
    main()