class TTSConfig:
    # Voice options: alloy, echo, fable, onyx, nova, shimmer
    VOICE = "echo"
    MODEL = "tts-1"
    MAX_CHARS = 4000

    # Audio settings
    AUDIO_FORMAT = "mp3"

    # Retry settings
    MAX_RETRIES = 3
    RETRY_MIN_WAIT = 4
    RETRY_MAX_WAIT = 10
    RETRY_MULTIPLIER = 1
