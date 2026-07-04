from __future__ import annotations
from contextlib import nullcontext
import curses
import random


# Custom Types
class Vector:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y

    def __add__(self, other) -> Vector:
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        elif isinstance(other, int):
            return Vector(self.x + other, self.y + other)
        else:
            raise ValueError("Type not supported for Vectors")

    def __sub__(self, other) -> Vector:
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        elif isinstance(other, int):
            return Vector(self.x - other, self.y - other)
        else:
            raise ValueError("Type not supported for Vectors")

    def __mul__(self, other) -> Vector:
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)
        elif isinstance(other, int):
            return Vector(self.x * other, self.y * other)
        else:
            raise ValueError("Type not supported for Vectors")

    def __truediv__(self, other) -> Vector:
        if isinstance(other, Vector):
            return Vector(int(self.x / other.x), int(self.y / other.y))
        elif isinstance(other, int):
            return Vector(int(self.x / other), int(self.y / other))
        else:
            raise ValueError("Type not supported for Vectors")

    def __pow__(self, other) -> Vector:
        if isinstance(other, Vector):
            return Vector(self.x**other.x, self.y**other.y)
        elif isinstance(other, int):
            return Vector(self.x**other, self.y**other)
        else:
            raise ValueError("Type not supported for Vectors")

    def __str__(self) -> str:
        return f"∟{self.x}, {self.y}"


class MusicalInformation:
    def __init__(self) -> None:
        self.Name: str
        self.Pin: bool = False
        self.Rating: int = 0

        self.Path: str = ""


class SongInformation(MusicalInformation):
    def __init__(self):
        self.Artist: AlbumInformation
        self.Album: AlbumInformation


class AlbumInformation(MusicalInformation):
    def __init__(self):
        self.Artist: AlbumInformation
        self.Roster: list = []

    def CreateSuffledCopy(self) -> AlbumInformation:
        duplicate = AlbumInformation()

        shuffledRoster = self.Roster
        random.shuffle(shuffledRoster)

        duplicate.Roster = shuffledRoster

        return duplicate


# Elements
