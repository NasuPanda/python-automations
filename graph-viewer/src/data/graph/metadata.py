from dataclasses import dataclass


@dataclass
class Metadata:
    filename: str
    data: list
    header: str

    @property
    def label(self) -> str:
        return self.filename + "_" + self.header
