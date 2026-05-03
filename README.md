# CloudInsight

An automated DevSecOps framework designed for AWS security auditing.

## Features
* **S3 Scanning:** Identifies publicly accessible buckets.
* **IAM Analysis:** Detects overly permissive roles.
* **Automated Fixes:** Includes scripts like fix_s3_security.py to remediate issues.

## Setup
1. **Clone the repo:** `git clone https://github.com/shahzad5444/CloudInsight.git`
2. **Create venv:** `python3 -m venv venv`
3. **Install dependencies:** `pip install -r requirements.txt`

## Usage
**Run the main scanner:**
`python3 main.py`
