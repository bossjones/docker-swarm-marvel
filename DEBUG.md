# Example debug session w/ debugger modules

*source: https://stackoverflow.com/questions/21961693/how-to-print-all-variables-values-when-debugging-python-with-pdb-without-specif*


```
In [1]: import debug_nice
In [2]: len(debug_nice.debug_nice(locals()))
Out[2]: 5
In [3]: from pandas import *; from numpy import *
In [4]: len(locals())
Out[4]: 698
In [5]: len(debug_nice.debug_nice(locals()))
Out[5]: 151
In [6]: keys = ['typeNA', 'typeDict', 'sctypes', 'sctypeNA', 'typecodes', 'sctypeDict', 'typeCodes', 'ScalarType', 'nbytes', 'cast', 'In', 'Out', 'keys', 'get_ipython']
Out [6]:
In [7]: keys.extend( {k: v for k, v in locals().iteritems() if type(v) == type(sign)}.keys())
Out [7]:
In[8]:
In [9]: debug_nice.debug_nice(locals(), keys=keys)
Out[9]:
{'ALLOW_THREADS': 1,
 'BUFSIZE': 8192,
 'CLIP': 0,
 'ERR_CALL': 3,
 'ERR_DEFAULT': 0,
 'ERR_DEFAULT2': 521,
 'ERR_IGNORE': 0,
 'ERR_LOG': 5,
 'ERR_PRINT': 4,
 'ERR_RAISE': 2,
 'ERR_WARN': 1,
 'FLOATING_POINT_SUPPORT': 1,
 'FPE_DIVIDEBYZERO': 1,
 'FPE_INVALID': 8,
 'FPE_OVERFLOW': 2,
 'FPE_UNDERFLOW': 4,
 'False_': False,
 'Inf': inf,
 'Infinity': inf,
 'MAXDIMS': 32,
 'NAN': nan,
 'NINF': -inf,
 'NZERO': -0.0,
 'NaN': nan,
 'NaT': NaT,
 'PINF': inf,
 'PZERO': 0.0,
 'RAISE': 2,
 'SHIFT_DIVIDEBYZERO': 0,
 'SHIFT_INVALID': 9,
 'SHIFT_OVERFLOW': 3,
 'SHIFT_UNDERFLOW': 6,
 'True_': True,
 'UFUNC_BUFSIZE_DEFAULT': 8192,
 'UFUNC_PYVALS_NAME': 'UFUNC_PYVALS',
 'WRAP': 1,
 'c_': <numpy.lib.index_tricks.CClass at 0x102925390>,
 'describe_option': <pandas.core.config.CallableDynamicDoc at 0x102e232d0>,
 'e': 2.718281828459045,
 'exit': <IPython.core.autocall.ExitAutocall at 0x101e7d5d0>,
 'format_parser': numpy.core.records.format_parser,
 'get_option': <pandas.core.config.CallableDynamicDoc at 0x102e23210>,
 'help': Type help() for interactive help, or help(object) for help about object.,
 'index_exp': <numpy.lib.index_tricks.IndexExpression at 0x102925410>,
 'inf': inf,
 'infty': inf,
 'little_endian': True,
 'mgrid': <numpy.lib.index_tricks.nd_grid at 0x1029252d0>,
 'nan': nan,
 'newaxis': None,
 'ogrid': <numpy.lib.index_tricks.nd_grid at 0x102925310>,
 'options': <pandas.core.config.DictWrapper at 0x102e23310>,
 'pi': 3.141592653589793,
 'plot_params': {'xaxis.compat': False},
 'r_': <numpy.lib.index_tricks.RClass at 0x102925350>,
 'reset_option': <pandas.core.config.CallableDynamicDoc at 0x102e23290>,
 's_': <numpy.lib.index_tricks.IndexExpression at 0x102925490>,
 'set_option': <pandas.core.config.CallableDynamicDoc at 0x102e23250>}
```
