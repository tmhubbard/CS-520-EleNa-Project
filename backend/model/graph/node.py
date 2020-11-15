class Node:
    """
    Node class represets a node in a Graph
    """
    def __init__(
            self, 
            id: int, 
            latitude: float = None, longitude: float = None, 
            elevation: float = None,
            neighbors: list = None):
        self._id = id
        self._latitude = latitude
        self._longitude = longitude
        self._elevation = elevation
        self._neighbors = neighbors # [(neighborID, distance), (,), ...]
    
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
    def elevation(self) -> float:
        return self._elevation
    
    @elevation.setter 
    def elevation(self, elevation: float):
        self._elevation = elevation

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
            "elevation": self._elevation
        }
    
    def get_content(self) -> dict:
        return {
            "id": self._id,
            "latitude": self._latitude,
            "longitude": self._longitude,
            "elevation": self._elevation,
            "neighbors": self._neighbors,
        }