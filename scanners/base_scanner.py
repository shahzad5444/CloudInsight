class BaseScanner:
    def __init__(self, session):
        self.session = session
        self.findings = []

    def scan(self):
        raise NotImplementedError("Subclasses must implement scan()")

    def add_finding(self, severity, resource, issue):
        self.findings.append({
            'severity': severity,
            'resource': resource,
            'issue': issue
        })
