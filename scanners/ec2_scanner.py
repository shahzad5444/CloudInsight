from .base_scanner import BaseScanner

class EC2Scanner(BaseScanner):
    def scan(self):
        # Adding a manual log to prove this part of the code is reached
        print("🔍 Checking EC2 Instances...") 
        ec2 = self.session.client('ec2')
        try:
            instances = ec2.describe_instances()
            # If no instances exist, this loop just finishes silently
            for reservation in instances['Reservations']:
                for instance in reservation['Instances']:
                    self.add_finding("INFO", instance['InstanceId'], "Found an instance")
        except Exception as e:
            print(f"Error scanning EC2: {e}")
        return self.findings
