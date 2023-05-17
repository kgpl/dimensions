from typing import Any, List, Union, Tuple
from collections import namedtuple
import utility as util
import warnings

Number = Union[int, float]

class Measurement():
    def __init__(self, number=0, unit=None,
                 lower_limit=None, upper_limit=None,
                 dtype= None, conversion_class=None):
        self._number = number
        self._unit = unit
        self._ulim = upper_limit
        self._llim = lower_limit
        self._conv = conversion_class
        self._measure = namedtuple("Measure", ["magnitude", "unit"])

    def __repr__(self):
        return str(self._measure(self.magnitude,self.unit))
    
    def __str__(self):
        return f"{self.magnitude} {self.unit}"
    
    @property
    def magnitude(self) -> Number:
        """Current Magnitude of Measurement

        Returns:
            Number: Magnitude of measured quantity
        """
        return self._number
    
    @magnitude.setter
    def magnitude(self, number: Number) -> None:
        """Change the current Magnitude for measurement

        Input value should be within limits if defined, 
        else they will be capped at limits with warning.

        Args:
            number (Number): input magnitude value.
        """
        self._number = util.lim_cap(number, self._llim, self._ulim)
    
    @property
    def unit(self) -> str:
        """returns current unit of measurement

        Returns:
            str: current unit of measurement
        """
        if self._unit is None:
            return ""
        return self._unit
    
    @unit.setter
    def unit(self, unit_str: str) -> None:
        """updates the measurement unit

        Args:
            unit_str (str): Measurement unit 
        """
        try:
            self._llim = self._conv.unit_conversion(self._llim, self.unit, unit_str)
            self._ulim= self._conv.unit_conversion(self._ulim, self.unit, unit_str)
            self._number = self._conv.unit_conversion(self.magnitude, self.unit, unit_str)
        except ValueError:
            warnings.warn("Conversion is not supported.")
        else:
            self._unit = unit_str

    @property
    def limit(self) -> Tuple:
        """returns current set limits.

        Returns:
            Tuple: returns the lower and upper limit possible for measurement
        """
        return (self._llim, self._ulim)
    
    @limit.setter
    def limit(self, lim: Union[List[Number, None],Tuple]) -> None:
        """updates the limit

        Args:
            lim (Union[List[Number, None],Tuple]): limit to be set. e.g. [0,100] it includes both 0 and 100.

        Raises:
            TypeError: Limit should be a list or tuple of integer, float or None.
            ValueError: Only two valued list/tuple is allowed where first_value < second_value
        """
        util.check_limit_type(lim)        
        self._llim, self._ulim = lim

    def convert(self, unit):
        lo_lim = self._conv.unit_conversion(self._llim, self.unit, unit)
        up_lim = self._conv.unit_conversion(self._ulim, self.unit, unit)
        value = self._conv.unit_conversion(self.magnitude, self.unit, unit)
        return util.lim_cap(value, lo_lim, up_lim)

    def __add__(self, val):
        try:
            converted_val = val.convert(self.unit)
        except ValueError:
            raise ValueError("Measurement with two different unrelated units can't be added.")
        else:
            new_num = self.magnitude + converted_val
  
        return Measurement(number=new_num, unit=self.unit,
                            lower_limit=self._llim, upper_limit=self._ulim,
                            conversion_class=self._conv)

    def __sub__(self, val):
        try:
            converted_val = val.convert(self.unit)
        except ValueError:
            raise ValueError("Measurement with two different unrelated units can't be subtracted.")
        else:
            new_num = self.magnitude - converted_val

        return Measurement(number=new_num, unit=self.unit,
                            lower_limit=self._llim, upper_limit=self._ulim,
                            conversion_class=self._conv)

    def __mul__(self, other):
        pass

    def __truediv__(self, other):
        pass

    def __floordiv__(self, other):
        pass

    def __lt__(self, other):
        pass

    def __le__(self, other):
        pass

    def __ge__(self, other):
        pass

    def __eq__(self, val):
        try:
            converted_val = val.convert(self.unit)
        except ValueError:
            return False
        else:
            mag = self.magnitude == converted_val
            lmt = self.limit == val.limit
            cnv = self.conv == val.conv
        
        return mag and lmt and cnv
    
    def __ne__(self, other):
        pass

    def __round__(self, n):
        pass

    def __floor__(self):
        pass

    def __ceil__(self):
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self