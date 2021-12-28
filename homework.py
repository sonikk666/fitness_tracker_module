"""Модуль фитнес-трекера: рассчитывает и отображает результаты тренировки."""
from dataclasses import asdict, dataclass
from typing import Dict, List, Tuple, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Получить готовое сообщение о тренировке."""
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINUTES_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'Определить метод get_spent_calories в {self.__class__.__name__}'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    RATE_CALORIE: float = 18
    CORRECT_CALORIE: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        return (
            (self.RATE_CALORIE * self.get_mean_speed() - self.CORRECT_CALORIE)
            * self.weight / self.M_IN_KM * self.duration * self.MINUTES_IN_HOUR
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    RATE_WEIGHT: float = 0.035
    FACTOR_WALK: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при ходьбе."""
        return (
            (self.RATE_WEIGHT * self.weight + (self.get_mean_speed()**2
             // self.height) * self.FACTOR_WALK * self.weight) * self.duration
            * self.MINUTES_IN_HOUR
        )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CORRECT_SPEED: float = 1.1
    FACTOR_SPEED: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км при плавании."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения при плавании."""
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании."""
        return (
            (self.get_mean_speed() + self.CORRECT_SPEED)
            * self.FACTOR_SPEED * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков.
    Принимает на вход код тренировки и список её параметров.
    """
    type_training_name: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    try:
        return type_training_name[workout_type](*data)
    except (KeyError, TypeError):
        raise ValueError(
            f'Ошибка данных от датчиков <{workout_type}: {data}>'
        )


def main(training: Training) -> None:
    """Главная функция. Создаёт объект класса InfoMessage
    и выводит его на экран.
    """
    info = training.show_training_info()
    print(info.get_message())


"""Имитация получения данных от датчиков."""
if __name__ == '__main__':
    packages: List[Tuple[str, List[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
