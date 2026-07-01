from __future__ import annotations
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


class SongInformation:
    def __init__(self, Name: str, Artist: str, Album: AlbumInformation):
        self.Name = Name
        self.Artist = Artist
        self.Album = Album


class AlbumInformation:
    def __init__(self, Name: str, Artist: str, SongRoster: list[SongInformation] = []):
        self.Name = Name
        self.Artist = Artist
        self.SongRoster = SongRoster

    def CreateSuffledCopy(self) -> AlbumInformation:
        duplicate = AlbumInformation(Name=self.Name, Artist=self.Artist)

        roster = self.SongRoster
        random.shuffle(roster)

        duplicate.SongRoster = roster

        return duplicate


# Elements
