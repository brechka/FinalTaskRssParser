# raise RuntimeError

class Error(Exception):
    """Base class for exceptions in this module"""
    pass

class InvalidURL(Error):
    """Exception raised for invalid URL"""
    pass

