from .base_scanner import BaseScanner
from botocore.exceptions import ClientError

class S3Scanner(BaseScanner):
    def scan(self):
        s3 = self.session.client('s3')
        try:
            buckets = s3.list_buckets()['Buckets']
            for bucket in buckets:
                name = bucket['Name']
                self.audit_public_access(s3, name)
        except Exception as e:
            print(f"Error scanning S3: {e}")
        return self.findings

    def audit_public_access(self, client, bucket_name):
        try:
            # Check Public Access Block configuration
            response = client.get_public_access_block(Bucket=bucket_name)
            config = response['PublicAccessBlockConfiguration']
            
            # If any of these are False, the bucket might be risky
            if not all(config.values()):
                self.add_finding("HIGH", bucket_name, "Public Access Block is NOT fully enabled")
            else:
                self.add_finding("SECURE", bucket_name, "Public Access is correctly blocked")
                
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
                self.add_finding("CRITICAL", bucket_name, "No Public Access Block configuration found!")
            else:
                self.add_finding("INFO", bucket_name, f"Could not audit: {e}")
