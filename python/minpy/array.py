#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Base type for arrays."""
from __future__ import absolute_import

from .utils import log
from .utils import common
#import typing
import minpy.numpy
import mxnet
import numpy

_logger = log.get_logger(__name__)

class Node(object):
    """Node representing data with gradient information."""
    __slots__ = ['_partial_derivatives', '_partial_derivative_cache']

    _partial_derivatives = []
    _partial_derivative_cache = []

    def __init__(self):
        """Initialize."""
        pass

    def __str__(self):
        """Get string representation.

        Return:
            A string representation.
        """
        return 'Node({})'.format(self)

    def add_partial_derivative(self, func, res):
        """ Add partial derivative information

        :param function func: the function to calculate derivative with respect to res
        :param Node res: variable that represent the target of derivative
        """
        _logger.info('Adding partial derivative to {}: {}'.format(id(self),
                                                                  self))
        assert(isinstance(res, Node))
        self._partial_derivatives.append((func, res))

    def partial_derivative(self, target):
        """ Add partial derivative information

        :param Node target: target variable to compute partial derivative
        """
        assert(isinstance(target, Node))
        if target in self._partial_derivative_cache:
            return self._partial_derivative_cache[target]
        else:
            if self is target:  # Partial derivative of self is one.
                return 1.0
            else:
                res = functools.reduce(operator.add, map(
                    lambda x: x[0](x[1].partial_derivative(target)),
                    self._partial_derivatives), 0.0)
                self._partial_derivative_cache[target] = res
                #_logger.info('Partial derivative id: {}, shape: {}, value: {}'.
                             #format(id(self), self.val.shape, res))
                return res

class ArrayTypeMissingError(ValueError):
    pass

class UnknownArrayTypeError(ValueError):
    pass

class Array(object):
    """Base array type.

    It provides convenient methods for arithmetic operations. The Array class
    is used for:
    1. Redirect all special member functions to corresponding pure function.
    2. Redirect normal member functions to correct member functions of
    underlying array object.
    """
    __slots__ = ['_node', '_data']

    _node = Node()
    _data = {}

    @staticmethod
    #def to_array_type(arr: typing.Union[numpy.ndarray, mxnet.narray.NArray]
                      #) -> ArrayType:
    def to_array_type(arr):
        t = type(arr)
        if t == numpy.ndarray:
            return minpy.numpy.ArrayType.NUMPY
        elif t == mxnet.nd.NArray:
            return minpy.numpy.ArrayType.MXNET
        else:
            raise UnknownArrayTypeError(
                'Array data of type {} unknown.'.format(t))

    @staticmethod
    #def to_real_type(arr: ArrayType) -> type:
    def to_real_type(arr):
        if arr == minpy.numpy.ArrayType.NUMPY:
            return numpy.ndarray
        elif arr == minpy.numpy.ArrayType.MXNET:
            return mxnet.nd.NArray
        else:
            raise UnknownArrayTypeError(
                'Array data of type {} unknown.'.format(arr))

    @property
    def node(self):
        """ get node which contains derivative information from this array """
        return self._node

    def __init__(self, data):
        t = Array.to_array_type(data)
        self._data[t] = data

    def has_type(self, t):
        """Return whether array data of given type exists in the underlying storage.
        """
        return t in self._data.keys()

    def get_data(self, t):
        """Get array data of given type. Raise exception if the type is missing.
        """
        if t not in self._data:
            raise ArrayTypeMissingError(
                'Array data of type {} not found.'.format(t))
        return self._data[t]

    #def create_data(self, t: ArrayType):
    def create_data(self, t):
        """Create data of given type."""
        if t not in self._data:
            if t == minpy.numpy.ArrayType.NUMPY:
                mxarray = self.get_data(minpy.numpy.ArrayType.MXNET)
                self._data[minpy.numpy.ArrayType.NUMPY] = mxarray.asnumpy()
            elif t == minpy.numpy.ArrayType.MXNET:
                nparray = self.get_data(minpy.numpy.ArrayType.NUMPY)
                self._data[minpy.numpy.ArrayType.MXNET] = mxnet.nd.array(nparray)
            else:
                raise UnknownArrayTypeError(
                    'Array data of type {} unknown.'.format(t))

    @property
    def shape(self):
        return self._data.values()[0].shape

    # TODO special function redirection and __getattr__ redirection
    def __getattr__(self, name):
        # TODO la magie
        pass

    def __cmp__(self, other):
        pass

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

    def __lt__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __le__(self, other):
        pass

    def __ge__(self, other):
        pass

    def __pos__(self):
        pass

    def __neg__(self):
        return minpy.numpy.negate(self)

    def __abs__(self):
        pass

    def __invert__(self):
        pass

    def __round__(self, n):
        pass

    def __floor__(self):
        pass

    def __ceil__(self):
        pass

    def __trunc__(self):
        pass

    def __add__(self, other):
        return minpy.numpy.add(self, other)

    def __sub__(self, other):
        return minpy.numpy.subtract(self, other)

    def __mul__(self, other):
        return minpy.numpy.multiply(self, other)

    def __floordiv__(self, other):
        pass

    def __div__(self, other):
        return minpy.numpy.divide(self, other)

    def __truediv__(self, other):
        return minpy.numpy.true_divide(self, other)

    def __mod__(self, other):
        return minpy.numpy.mod(self, other)

    def __divmod__(self, other):
        pass

    def __pow__(self, other):
        return minpy.numpy.power(self, other)

    def __lshift__(self, other):
        pass

    def __rshift__(self, other):
        pass

    def __and__(self, other):
        pass

    def __or__(self, other):
        pass

    def __xor__(self, other):
        pass

    def __radd__(self, other):
        return minpy.numpy.add(other, self)

    def __rsub__(self, other):
        return minpy.numpy.subtract(other, self)

    def __rmul__(self, other):
        return minpy.numpy.multiply(other, self)

    def __rfloordiv__(self, other):
        pass

    def __rdiv__(self, other):
        return minpy.numpy.divide(other, self)

    def __rtruediv__(self, other):
        return minpy.numpy.true_divide(other, self)

    def __rmod__(self, other):
        return minpy.numpy.mod(other, self)

    def __rdivmod__(self, other):
        return minpy.numpy.mod(other, self)

    def __rpow__(self, other):
        return minpy.numpy.power(other, self)

    def __rlshift__(self, other):
        pass

    def __rrshift__(self, other):
        pass

    def __rand__(self, other):
        pass

    def __ror__(self, other):
        pass

    def __rxor__(self, other):
        pass

    def __iadd__(self, other):
        return minpy.numpy.add(other, self)

    def __isub__(self, other):
        return minpy.numpy.subtract(other, self)

    def __imul__(self, other):
        return minpy.numpy.multiply(other, self)

    def __ifloordiv__(self, other):
        pass

    def __idiv__(self, other):
        return minpy.numpy.divide(other, self)

    def __itruediv__(self, other):
        return minpy.numpy.true_divide(other, self)

    def __imod__(self, other):
        return minpy.numpy.mod(other, self)

    def __ipow__(self, other):
        return minpy.numpy.power(other, self)

    def __ilshift__(self, other):
        pass

    def __irshift__(self, other):
        pass

    def __iand__(self, other):
        pass

    def __ior__(self, other):
        pass

    def __ixor__(self, other):
        pass

class Primitive(object):
    """Primitive computation."""
    __slots__ = ['_func', '_grad_func', '_grad_func_kw', '_type']

    def __init__(self, func, ty):
        """Initialize.
        Args:
            func: A function that performs the action.
        """
        self._func = func
        self._grad_func = {}
        self._grad_func_kw = {}
        self._type = ty

    @property
    def type(self):
        return self._type;

    def __call__(self, *args, **kwargs):
        """Call wrapped function.
        Args:
            *args:
                Arguments for the wrapped function.
            **kwargs:
                Arguments for the wrapped function.

        Returns:
            An `array.Array` representing the result.

        Raises:
            IndexError:
                No corresponding gradient function.
            KeyError:
                No corresponding gradient function.
        """
        _logger.info('Calling {}'.format(self._func))

        def get_val(x):
            return x.get_data(self._type) if isinstance(x, array.Array) else x
        # Get underlying data.
        arg_values = tuple(map(get_val, args))
        kwargs_values = {x: get_val(kwargs[x]) for x in kwargs}
        # Call the real function with raw value.
        result_value = self._func(*arg_values, **kwargs_values)
        # Wrap the result raw value with wrapper and node.
        result = array.Array(result_value)
        # Record partial derivative paths, only for `array.Array` type values.
        for i, arg in enumerate(args):
            if isinstance(arg, array.Array):
                arg.node.add_partial_derivative(
                        self._grad_func[i](result_value, *arg_values, **kwargs_values),
                        result.node)
        for x in kwargs:
            if isinstance(arg, array.Array):
                arg.node.add_partial_derivative(
                        self._grad_func_kw[x](result_value, *arg_values, **kwargs_values),
                        result.node)
        return result

    def def_grad(self, func, argnum=0):
        """Define gradient function.
        Args:
            func:
                Gradient function.
            argnum:
                Index of the argument.

        Return:
            self instance for multiple def_grad in one statement
        """
        self._grad_func[argnum] = func
        return self

    def def_grad_kw(self, func, key):
        """Define gradient function.
        Args:
            func:
                Gradient function.
            key:
                Key name of the argument.
        """
        self._grad_func[key] = func

    def def_grad_zero(self, argnum=0):
        self._grad_func[argnum] = lambda *args, **kwargs: lambda g: 0.0
