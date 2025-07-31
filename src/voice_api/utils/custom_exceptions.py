class VoiceAPIException(Exception):
    """Base exception class for the Voice API."""
    pass

class OTPGenerationError(VoiceAPIException):
    """Raised when OTP generation fails."""
    pass

class OTPStorageError(VoiceAPIException):
    """Raised when there is an error storing or retrieving an OTP."""
    pass

class VoiceSynthesisError(VoiceAPIException):
    """Raised when text-to-speech synthesis fails."""
    pass