from typing import Dict

import splatan.Vertex as Vertex
from splatan.enums.Settlements import Settlements


class Vertices:
    def __init__(self) -> None:
        self.name_to_vertex: Dict[str, Vertex.Vertex] = {}

    def __contains__(self, item):
        return str(item) in self.name_to_vertex

    def build_settlement(self, name: str, settlement: Settlements) -> Vertex.Vertex:
        # TODO: check if it can build there
        settlement = Vertex.Vertex(name, settlement=settlement)
        self.name_to_vertex[name] = settlement
        return settlement

    def build_road(self, start: str, end: str) -> None:
        # at least once vertex has been initialized
        if not self.vertex_exists(start) and not self.vertex_exists(end):
            raise ValueError("Error: attempting to build on nothing")

        # initialize / get vertices
        start_vertex, end_vertex = self.get_or_create_vertex(start), self.get_or_create_vertex(end)

        # if not self.can_build_road(player, start_vertex, end_vertex):
        #     raise ValueError("Error: Can only build on empty or occupied territory.")

        # build road
        start_vertex.build_road(end_vertex)
        end_vertex.build_road(start_vertex)

    def get_or_create_vertex(self, location: str) -> Vertex.Vertex:
        """
        Returns existing vertex or creates new one if doesn't exist
        :param location: str representation of the location on the board
        :return: existing or created vertex
        """
        return self.get_vertex(location) if self.vertex_exists(location) else self.create_new_vertex(location)

    def vertex_exists(self, vertex: str) -> bool:
        return vertex in self.name_to_vertex

    def get_vertex(self, location: str) -> Vertex.Vertex:
        return self.name_to_vertex[location]

    def create_new_vertex(self, location: str) -> Vertex.Vertex:
        vertex = Vertex.Vertex(location)
        self.name_to_vertex[location] = vertex
        return vertex

    # def can_build_road(self, player: Player.Player, start: Vertex.Vertex, end: Vertex.Vertex) -> bool:
    #     """
    #     Vertices have to be beside each other and both start and end have to be either unoccupied
    #     or owned by the player
    #     :param player:
    #     :param start:
    #     :param end:
    #     :return:
    #     """
    #
    #     return start.is_beside(end) \
    #            and self.owns_or_unoccupied_vertex(player, start) \
    #            and self.owns_or_unoccupied_vertex(player, end)
    #
    # def owns_or_unoccupied_vertex(self, player: Player.Player, vertex: Vertex.Vertex) -> bool:
    #     return vertex.player == player or vertex.player is None
