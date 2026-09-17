from dataclasses import dataclass


@dataclass
class MediaState:
    playing: bool = False
    title: str = ""
    artist: str = ""


@dataclass
class MessageState:
    active: bool = False
    sender: str = ""
    text: str = ""


@dataclass
class CallState:
    active: bool = False
    caller_name: str = ""
    caller_number: str = ""


@dataclass
class PhoneState:
    connected: bool = False

    media: MediaState = None
    message: MessageState = None
    call: CallState = None

    def __post_init__(self):
        if self.media is None:
            self.media = MediaState()

        if self.message is None:
            self.message = MessageState()

        if self.call is None:
            self.call = CallState()