class Node:
    def __init__(
            self, 
            id: int, 
            latitude: float, longitude: float, 
            neighbors: list = None):
        self._id = id
        self._latitude = latitude
        self._longitude = longitude
        self._neighbors = neighbors
    
    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, id: int):
        self._id = id
    
    @property
    def latitude(self) -> float:
        return self._latitude
    
    @latitude.setter 
    def latitude(self, latitude: float):
        self._latitude = latitude
    
    @property
    def longitude(self) -> float:
        return self._longitude
    
    @longitude.setter 
    def longitude(self, longitude: float):
        self._longitude = longitude

    @property
    def neighbors(self) -> list:
        return self._neighbors
    
    @neighbors.setter 
    def neighbors(self, neighbors: list):
        self._neighbors = neighbors
    
    def as_json(self) -> dict:
        return {
            "id": self._id,
            "latitude": self._latitude,
            "longitude": self._longitude,
            "neighbors": self._neighbors,
        }