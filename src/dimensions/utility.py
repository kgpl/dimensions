import warnings

def lim_cap(number, lower_limit, upper_limit):
    if lower_limit is not None:
        if number < lower_limit:
            number = lower_limit
            warnings.warn(f"set value is lower than preset lower limit. Capping value at {lower_limit}")
    if upper_limit is not None:
        if number > upper_limit:
            number = upper_limit
            warnings.warn(f"set value is higher than preset upper limit. Capping value at {upper_limit}")
    return number

def check_limit_type(data):
    if not isinstance(data, list) or isinstance(data, tuple):
            raise TypeError("limit should be a list or tuple containing two values, [lower_lim, upper_lim]")
    if not len(data) == 2:
        raise ValueError("Only two valued list/tuple is allowed.")
    if not all([isinstance(data_itr, int) \
                or isinstance(data_itr, float) \
                or data_itr is None \
                for data_itr in data]):
        raise TypeError("Only list/tuple of integer,float or None is supported.")
    if all([data_itr is not None for data_itr in data]):
        if data[0] >= data[1]:
            raise ValueError("Upper limit should be higher than lower limit.")