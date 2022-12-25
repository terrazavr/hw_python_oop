from dataclasses import dataclass, asdict
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    INFORMATION = ('Тип тренировки: {training_type}; '
                   + 'Длительность: {duration:.3f} ч.; '
                   + 'Дистанция: {distance:.3f} км; '
                   + 'Ср. скорость: {speed:.3f} км/ч; '
                   + 'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        '''Возвращает строку сообщения.'''
        return self.INFORMATION.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    H_IN_MIN: float = 1
    MIN_IN_H: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return ((self.action * self.LEN_STEP / self.M_IN_KM) / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise (NotImplementedError('Метод будет переопределен далее'))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        calories_of_run = (((self.CALORIES_MEAN_SPEED_MULTIPLIER
                             * self.action * self.LEN_STEP
                             / self.M_IN_KM / self.duration
                             + self.CALORIES_MEAN_SPEED_SHIFT)
                            * self.weight / self.M_IN_KM
                            * self.duration * self.MIN_IN_H))
        return calories_of_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: float = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        self.height = height / self.CM_IN_M
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        calories__of_sw = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                           + ((self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                              / self.height
                            * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                            * self.weight))
                           * self.duration * self.MIN_IN_H)
        return calories__of_sw


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SWIM_MULTIPLIER: float = 1.1
    CALORIES_MEAN_SWIM_SHIFT: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        self.length_pool = length_pool
        self.count_pool = count_pool
        super().__init__(action, duration, weight)

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        calories_of_swim = ((self.get_mean_speed()
                            + self.CALORIES_MEAN_SWIM_MULTIPLIER)
                            * self.CALORIES_MEAN_SWIM_SHIFT * self.weight
                            * self.duration)
        return calories_of_swim


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking}
    if workout_type not in training_type:
        raise ValueError('Отсутствует указанный тип тренировки.')
    return training_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
