import json
import os
import glob

def generate_summary():
    # Find the most recent report
    list_of_files = glob.glob('reports/full_audit_*.json')
    if not list_of_files:
        print("No reports found.")
        return
        
    latest_file = max(list_of_files, key=os.path.getctime)
    
    with open(latest_file, 'r') as f:
        findings = json.load(f)
        
    total = len(findings)
    high_risk = sum(1 for f in findings if f['severity'] == 'HIGH')
    secure = sum(1 for f in findings if f['severity'] == 'SECURE')
    
    print("\n" + "="*30)
    print(f"      SECURITY SUMMARY")
    print("="*30)
    print(f"Report: {os.path.basename(latest_file)}")
    print(f"Total Resources Audited: {total}")
    print(f"🔴 HIGH RISKS FOUND:    {high_risk}")
    print(f"🟢 SECURE RESOURCES:    {secure}")
    print("="*30)

if __name__ == "__main__":
    generate_summary()
