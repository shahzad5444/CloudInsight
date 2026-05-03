import boto3
import json
import os
from datetime import datetime
from scanners.s3_scanner import S3Scanner
from scanners.ec2_scanner import EC2Scanner

def run_audit():
    print("🚀 Starting Multi-Service Security Scan...")
    
    # We define the session INSIDE the python script
    # Change 'us-east-1' to whichever region your instances are in
    session = boto3.Session(region_name='us-east-1')
    
    all_findings = []

    # 1. Scan S3
    s3_scanner = S3Scanner(session)
    all_findings.extend(s3_scanner.scan())

    # 2. Scan EC2
    ec2_scanner = EC2Scanner(session)
    all_findings.extend(ec2_scanner.scan())

    if not all_findings:
        print("✅ No resources found in this region.")
        return

    for f in all_findings:
        print(f"[{f['severity']}] {f['resource']}: {f['issue']}")

    # Save to reports folder
    if not os.path.exists('reports'): os.makedirs('reports')
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_file = f"reports/full_audit_{timestamp}.json"
    
    with open(report_file, 'w') as f:
        json.dump(all_findings, f, indent=4)
        
    print(f"\n💾 Full Audit saved to: {report_file}")

if __name__ == "__main__":
    run_audit()
