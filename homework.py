class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.traning_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.traning_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    MIN_IN_HOUR = 60
    LEN_STEP: float = 0.65
    workout_type: str = ''

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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.workout_type, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.workout_type = 'Running'

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        mean_speed = self.get_mean_speed()
        calories = ((coeff_calorie_1 * mean_speed - coeff_calorie_2)
                    * self.weight / self.M_IN_KM * self.duration
                    * self.MIN_IN_HOUR)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.workout_type = 'SportsWalking'

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 2
        coeff_calorie_3 = 0.029
        mean_speed = self.get_mean_speed()
        calories = ((coeff_calorie_1 * self.weight
                    + (mean_speed ** coeff_calorie_2 // self.height)
                    * coeff_calorie_3 * self.weight) * self.duration
                    * self.MIN_IN_HOUR)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.workout_type = 'Swimming'

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        mean_speed = self.get_mean_speed()
        return ((mean_speed + coeff_calorie_1) * coeff_calorie_2 * self.weight)

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    tranings = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return tranings[workout_type](*data)


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
