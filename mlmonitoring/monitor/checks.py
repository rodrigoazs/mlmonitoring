from typing import Callable, List, Tuple, Optional, Union
from functools import partial
import pandas as pd
import numpy as np


class _CheckBase:
    """Check base class.

    Args:
        check_fn (Callable): A check function.
        name (str, optional): Name of the check function.
        Defaults to None.
        error (Optional[str], optional): Error message of
        the check function. Defaults to None.
    """

    def __init__(
        self,
        check_fn: Callable,
        name: str = None,
        error: Optional[str] = None,
        **check_kwargs,
    ) -> None:
        self._check_fn = check_fn
        self._check_kwargs = check_kwargs
        self.error = error
        self.name = name

    def _prepare_series_input(
        self,
        samples: Union[pd.Series, np.ndarray, List],
    ) -> pd.Series:
        """Prepare input for checking.

        Args:
            samples (Union[pd.Series, np.ndarray, List]): Array
            with samples.

        Returns:
            pd.Series: Samples converted to pandas Series.
        """

        if isinstance(samples, pd.Series):
            return samples
        elif isinstance(samples, pd.DataFrame):
            return samples
        elif isinstance(samples, np.ndarray):
            return pd.Series(samples)
        elif isinstance(samples, list):
            return pd.Series(samples)
        raise TypeError("Type %s not a recognized argument.")

    def __call__(
        self,
        samples: Union[np.ndarray, pd.Series, pd.DataFrame, List],
    ) -> Tuple[bool, pd.Series]:
        """Validate samples given a check method.

        Arguments:
            samples (Union[np.ndarray, pd.Series, pd.DataFrame, List]):
            Array with samples from methods.

        Returns:
            Tuple[bool, pd.Series]: A tuple indicating if a warning has
            to be called for a given samples.
        """

        # prepare check object
        check_obj = self._prepare_series_input(samples)

        # apply check function to check object
        check_fn = partial(self._check_fn, **self._check_kwargs)

        # vectorized check function case
        check_output = check_obj.apply(check_fn)

        # warning cases only apply when the check function returns a boolean
        # series that matches the shape and index of the check_obj
        if (
            isinstance(check_obj, dict) or
            isinstance(check_output, bool) or
            not isinstance(check_output, (pd.Series, pd.DataFrame)) or
            check_obj.shape[0] != check_output.shape[0] or
            (check_obj.index != check_output.index).all()
        ):
            warning_cases = None
        elif isinstance(check_output, pd.Series):
            warning_cases = check_obj[check_output]
        else:
            raise TypeError(
                f"output type of check_fn not recognized: {type(check_output)}"
            )

        check_passed = (
            check_output.any()
            if isinstance(check_output, pd.Series)
            else check_output.any(axis=None)
        )

        return check_passed, warning_cases


class Check(_CheckBase):
    """Check given samples for certain properties."""

    @classmethod
    def equal_to(cls, value, **kwargs):
        """Ensure all elements equal a certain value."""

        def _equal(series: pd.Series) -> pd.Series:
            """Comparison function for check"""
            return series == value

        return cls(
            _equal,
            name=cls.equal_to.__name__,
            error=f"equal_to({value})",
            **kwargs,
        )

    eq = equal_to

    @classmethod
    def not_equal_to(cls, value, **kwargs):
        """Ensure no elements of a series equals a certain value."""

        def _not_equal(series: pd.Series) -> pd.Series:
            """Comparison function for check"""
            return series != value

        return cls(
            _not_equal,
            name=cls.not_equal_to.__name__,
            error=f"not_equal_to({value})",
            **kwargs,
        )

    ne = not_equal_to

    @classmethod
    def greater_than(cls, min_value, **kwargs):
        """Ensure values of a series are strictly greater than a minimum value."""
        if min_value is None:
            raise ValueError("min_value must not be None")

        def _greater_than(series: pd.Series) -> pd.Series:
            """Comparison function for check"""
            return series > min_value

        return cls(
            _greater_than,
            name=cls.greater_than.__name__,
            error=f"greater_than({min_value})",
            **kwargs,
        )

    gt = greater_than

    @classmethod
    def greater_than_or_equal_to(cls, min_value, **kwargs):
        """Ensure all values are greater or equal a certain value."""
        if min_value is None:
            raise ValueError("min_value must not be None")

        def _greater_or_equal(series: pd.Series) -> pd.Series:
            """Comparison function for check"""
            return series >= min_value

        return cls(
            _greater_or_equal,
            name=cls.greater_than_or_equal_to.__name__,
            error=f"greater_than_or_equal_to({min_value})",
            **kwargs,
        )

    ge = greater_than_or_equal_to

    @classmethod
    def less_than(cls, max_value, **kwargs):
        """Ensure values of a series are strictly below a maximum value."""
        if max_value is None:
            raise ValueError("max_value must not be None")

        def _less_than(series: pd.Series) -> pd.Series:
            """Comparison function for check"""
            return series < max_value

        return cls(
            _less_than,
            name=cls.less_than.__name__,
            error=f"less_than({max_value})",
            **kwargs,
        )

    lt = less_than

    @classmethod
    def less_than_or_equal_to(cls, max_value, **kwargs):
        """Ensure values are less than or equal to a maximum value."""
        if max_value is None:
            raise ValueError("max_value must not be None")

        def _less_or_equal(series: pd.Series) -> pd.Series:
            """Comparison function for check"""
            return series <= max_value

        return cls(
            _less_or_equal,
            name=cls.less_than_or_equal_to.__name__,
            error=f"less_than_or_equal_to({max_value})",
            **kwargs,
        )

    le = less_than_or_equal_to

    @classmethod
    def in_range(
        cls, min_value, max_value, include_min=True, include_max=True, **kwargs
    ):
        """Ensure all values of a series are within an interval. Including
        or not the boundaries."""
        if min_value is None:
            raise ValueError("min_value must not be None")
        if max_value is None:
            raise ValueError("max_value must not be None")
        if max_value < min_value or (
            min_value == max_value and (not include_min or not include_max)
        ):
            raise ValueError(
                "The combination of min_value = %s and max_value = %s "
                "defines an empty interval!" % (min_value, max_value)
            )

        def _lt(series: pd.Series) -> pd.Series:
            """Comparison function for check"""
            return series < max_value

        def _le(series: pd.Series) -> pd.Series:
            """Comparison function for check"""
            return series <= max_value
        
        def _gt(series: pd.Series) -> pd.Series:
            """Comparison function for check"""
            return series > min_value
        
        def _ge(series: pd.Series) -> pd.Series:
            """Comparison function for check"""
            return series >= min_value

        left_op = _le if include_max else _lt
        right_op = _ge if include_min else _gt

        def _in_range(series: pd.Series) -> pd.Series:
            """Comparison function for check"""
            return left_op(series) & right_op(series)

        return cls(
            _in_range,
            name=cls.in_range.__name__,
            error=f"in_range({min_value}, {max_value})",
            **kwargs,
        )
