class InvalidURL(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class VideoUnavailable(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class PlaylistUnavailable(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class NoResolutionDesired(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)