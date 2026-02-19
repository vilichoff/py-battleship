from typing import List, Tuple, Optional, Dict


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int],
        is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks: List[Deck] = []

        row_start, row_end = min(start[0], end[0]), max(start[0], end[0])
        col_start, col_end = min(start[1], end[1]), max(start[1], end[1])

        for r in range(row_start, row_end + 1):
            for c in range(col_start, col_end + 1):
                self.decks.append(Deck(r, c))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        target_deck = self.get_deck(row, column)
        if target_deck is not None:
            target_deck.is_alive = False
            self.is_drowned = all(not deck.is_alive for deck in self.decks)


class Battleship:
    def __init__(self, ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> None:
        self.field: Dict[Tuple[int, int], Ship] = {}

        for start, end in ships:
            new_ship = Ship(start, end)
            for deck in new_ship.decks:
                self.field[(deck.row, deck.column)] = new_ship

    def fire(self, location: Tuple[int, int]) -> str:
        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        ship.fire(location[0], location[1])

        if ship.is_drowned:
            return "Sunk!"

        return "Hit!"
