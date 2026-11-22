class Converter:
    def convert(self, value, source, target):
        raise NotImplementedError


class LinearConverter(Converter):
    def __init__(self, factors):
        self._factors = factors.copy()

    def convert(self, value, source, target):
        return value * self._factors[source] / self._factors[target]


class TemperatureConverter(Converter):
    def convert(self, value, source, target):
        if source == target:
            return value
        if source == "°C":
            return value * 9 / 5 + 32
        return (value - 32) * 5 / 9

