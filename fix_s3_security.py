import boto3
import json
import os
import glob

def fix_s3_buckets():
    # 1. Find the latest report
    list_of_files = glob.glob('reports/full_audit_*.json')
    if not list_of_files:
        print("No reports found to fix.")
        return
    
    latest_file = max(list_of_files, key=os.path.getctime)
    with open(latest_file, 'r') as f:
        findings = json.load(f)

    s3 = boto3.client('s3')
    
    # 2. Look for HIGH risk S3 buckets
    for f in findings:
        if f['severity'] == 'HIGH' and 'Public Access Block' in f['issue']:
            bucket_name = f['resource']
            print(f"🛠️ Attempting to fix bucket: {bucket_name}...")
            
            try:
                # Apply the "Block All Public Access" configuration
                s3.put_public_access_block(
                    Bucket=bucket_name,
                    PublicAccessBlockConfiguration={
                        'BlockPublicAcls': True,
                        'IgnorePublicAcls': True,
                        'BlockPublicPolicy': True,
                        'RestrictPublicBuckets': True
                    }
                )
                print(f"✅ Successfully locked down {bucket_name}!")
            except Exception as e:
                print(f"❌ Failed to fix {bucket_name}: {e}")

if __name__ == "__main__":
    fix_s3_buckets()
