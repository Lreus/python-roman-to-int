"""
    >>> values = ['I', 'V', 'X', 'L', 'C', 'D', 'M']
    >>> [int(RomanNumber(roman)) for roman in values ]
    [1, 5, 10, 50, 100, 500, 1000]

    >>> values = ['IV', 'IX', 'XL', 'XC', 'CD', 'CM']
    >>> [int(RomanNumber(roman)) for roman in values ]
    [4, 9, 40, 90, 400, 900]

    >>> exp = RomanNumber('R')
    Traceback (most recent call last):
        ...
    KeyError: "Allowed roman digits are ['I', 'V', 'X', 'L', 'C', 'D', 'M']"

    >>> exp = RomanNumber('MMCCLXIII')
    >>> exp2 = RomanNumber('CCXLIV')
    >>> int(exp)
    2263
    >>> exp + exp2
    2507

    >>> exp = RomanNumber('XXXX')
    Traceback (most recent call last):
        ...
    ValueError: Roman digits other than 'M' cannot be used continuously more \
than three times

    >>> exp = RomanNumber('MMMM')
    Traceback (most recent call last):
        ...
    ValueError: RomanNumber class cannot handle numbers greater than 3999

    >>> exp = RomanNumber('MMMCMXCIX')
    >>> int(exp)
    3999
"""
import re


class RomanNumber:
    def __repr__(self):
        return "RomanNumber('{}')".format(self._value)

    def __init__(self, value: str):
        if not(RomanNumber._is_valid(value)):
            raise ValueError("Roman digits other than 'M' cannot be used "
                             "continuously more than three times")
        if not(RomanNumber._is_in_range(value)):
            raise ValueError("RomanNumber class cannot handle numbers greater " 
                             "than 3999")
        self._digits = RomanNumber._build_digits(value)
        self._value = value

    def __add__(self, other):
        if isinstance(other, int):
            return int(self) + other
        if type(other) != type(self):
            raise TypeError('RomanNumber does not allow sum with other objects')

        return int(self) + int(other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __radd__(self, other):
        return self.__add__(other)

    def __int__(self):
        return int(self._digits)

    @staticmethod
    def _build_digits(value):
        letters = list(reversed(value))
        digits = None
        while len(letters) > 0:
            digits = RomanDigitFactory.get_digit(letters.pop(0), digits)
        return digits

    @staticmethod
    def _is_valid(value):
        limited_digits = [digit for digit in RomanDigitFactory.map.keys() if digit != 'M']
        separated_pattern = ['[{}]{}'.format(digit, '{4}') for digit in limited_digits]
        pattern = re.compile('|'.join(separated_pattern))
        match = pattern.search(value)
        if match is None:
            return True
        return False

    @staticmethod
    def _is_in_range(value):
        pattern = re.compile('[M]{4}')
        if pattern.search(value) is None:
            return True
        return False


class RomanDigit:
    map = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }

    def __init__(self, value: str, next_digit=None):
        if len(value) > 1:
            raise TypeError('Roman digit expects one char as parameter, use '
                            'RomanNumber for longer strings'
            )
        if value not in RomanDigit.map.keys():
            raise KeyError(
                'Allowed roman digits are {}'.format(
                    list(RomanDigit.map.keys())
                )
            )
        self._value = value

        if next_digit is not None and not(isinstance(next_digit, RomanDigit)):
            raise TypeError('Only RomanDigit instances can be used for next value')
        self._next = next_digit

    def __int__(self):
        next_value = 0
        if self.next() is not None:
            next_value = int(self.next())
        return self.self_int() + next_value
    
    def self_int(self) -> int:
        return self.get_int_value(tuple())

    def get_int_value(self, class_tuple=tuple()):
        if not isinstance(class_tuple, (tuple)):
            raise TypeError('A tuple of class is required to calculate '
                            'RomanDigits against their following digit'
                            )
        base_value = RomanDigit.map[self._value]
        if isinstance(self.next(), class_tuple):
            return -1 * base_value
        return base_value

    def value(self):
        return self._value

    def next(self):
        return self._next


class RomanDigitOne(RomanDigit):
    def self_int(self):
        return super().get_int_value((RomanDigitFive, RomanDigitTen))


class RomanDigitFive(RomanDigit):
    pass


class RomanDigitTen(RomanDigit):
    def self_int(self):
        return super().get_int_value ((RomanDigitFifty, RomanDigitHundred))


class RomanDigitFifty(RomanDigit):
    pass


class RomanDigitHundred(RomanDigit):
    def self_int(self):
        return super().get_int_value((RomanDigitFiveHundred, RomanDigitThousand))


class RomanDigitFiveHundred(RomanDigit):
    pass


class RomanDigitThousand(RomanDigit):
    pass


class RomanDigitFactory:

    map = {
        'I': RomanDigitOne,
        'V': RomanDigitFive,
        'X': RomanDigitTen,
        'L': RomanDigitFifty,
        'C': RomanDigitHundred,
        'D': RomanDigitFiveHundred,
        'M': RomanDigitThousand
    }

    @staticmethod
    def get_digit(value: str, next_digit=None) -> RomanDigit:
        if value not in RomanDigitFactory.map.keys():
            raise KeyError(
                'Allowed roman digits are {}'.format(
                    list(RomanDigit.map.keys())
                )
            )
        else:
            return RomanDigitFactory.map[value](value, next_digit)
