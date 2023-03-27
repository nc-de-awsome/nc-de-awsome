class AwsomeError(Exception):
    pass

class DatabaseConnectionError(AwsomeError):
    pass

class IngestionError(AwsomeError):
    pass

class WriteError(AwsomeError):
    pass

class SelectQueryError(AwsomeError):
    pass