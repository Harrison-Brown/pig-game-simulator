import random
from pig_logger import logger


class PigPlayer:
    def __init__(self, **kwargs) -> None:
        self.score = 0
        self.__dict__.update(kwargs)

    def keep_rolling(self) -> bool:
        if sum(self.turn_rolls) > 21:
            return False

    def roll(self):
        logger.info(f"{self} is rolling")

        self.turn_rolls = [random.randint(1, 6)]
        logger.info(f"{self} rolled a {self.turn_rolls[0]}")

        if self.turn_rolls[0] in self.game.excluded_numbers:
            logger.info(f"{self} rolled an excluded number")
            return 0
        
        while self.keep_rolling():
            logger.info(f"{self} is rolling again")
            self.turn_rolls.append(random.randint(1, 6))
            if self.turn_rolls[-1] in self.game.excluded_numbers:
                return 0
        return sum(self.turn_rolls)
    
    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items() if k not in ('score', 'turn_rolls', 'game'))
        return f"{self.__class__.__name__}({attrs})"



class PigGame:
    def __init__(self, player1: PigPlayer, player2: PigPlayer, excluded_numbers: list) -> None:
        player1.game = self
        player2.game = self
        self.players = [player1, player2]
    
        self.current_player = random.choice(self.players)
        self.excluded_numbers = excluded_numbers

    @property
    def other_player(self) -> PigPlayer:
        return self.players[0] if self.players[1] == self.current_player else self.players[1]
    
    def swap_players(self) -> None:
        self.current_player, self.other_player = self.other_player, self.current_player    


class RollNTimesPlayer(PigPlayer):
    def __init__(self, n_rolls: int) -> None:
        super().__init__(n_rolls = n_rolls)
        # self.n_rolls = n_rolls

    def keep_rolling(self) -> bool:
        super().keep_rolling()
        return len(self.turn_rolls) < self.n_rolls

    
class HoldAtNPlayer(PigPlayer):
    def __init__(self, hold_at: int) -> None:
        super().__init__()
        self.hold_at = hold_at

    def keep_rolling(self) -> bool:
        super().keep_rolling()
        return sum(self.turn_rolls) < self.hold_at
    
class RandomPlayer(PigPlayer):
    def keep_rolling(self) -> bool:
        super().keep_rolling()
        return random.choice([True, False])
    
class NBehindPlayer(PigPlayer):
    def __init__(self, behind_by: int) -> None:
        super().__init__(behind_by = behind_by)

    def keep_rolling(self) -> bool:
        super().keep_rolling()
        return sum(self.turn_rolls) + self.score > self.game.other_player.score + self.behind_by
    