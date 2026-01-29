class Action:
    pass


class MovePawn(Action):
    def __init__(self, x, y):
        """
        A pawn move to (x, y)

        Arguments:
            x: x coordinate, from 1 to 9 if the board is standard
            y: y coordinate, from 0 to 10 if the board is standard
        """
        self.x = x
        self.y = y


class PlaceFence(Action):
    def __init__(self, x, y, direction):
        """
        A fence placement at (x, y) along a direction

        Arguments:
            x: x fence coordinate, from 1 to 9 if the board is standard
            y: y fence coordinate, from 1 to 9 if the board is standard
            direction: True if horizontal, False if vertical
        """
        self.x = x
        self.y = y
        self.direction = direction
