Data Types
==========

.. _`backend setting`: https://github.com/unifyai/ivy/blob/ee0da7d142ba690a317a4fe00a4dd43cf8634642/ivy/framework_handler.py#L205
.. _`_function_w_arrays_dtype_n_dev_handled`: https://github.com/unifyai/ivy/blob/fdaea62380c9892e679eba37f26c14a7333013fe/ivy/func_wrapper.py#L242
.. _`NON_WRAPPED_FUNCTIONS`: https://github.com/unifyai/ivy/blob/fdaea62380c9892e679eba37f26c14a7333013fe/ivy/func_wrapper.py#L9
.. _`NON_DTYPE_WRAPPED_FUNCTIONS`: https://github.com/unifyai/ivy/blob/fdaea62380c9892e679eba37f26c14a7333013fe/ivy/func_wrapper.py#L103
.. _`import time`: https://github.com/unifyai/ivy/blob/9c2eb725387152d721040d8638c8f898541a9da4/ivy/__init__.py#L225
.. _`ivy.Dtype`: https://github.com/unifyai/ivy/blob/9c2eb725387152d721040d8638c8f898541a9da4/ivy/__init__.py#L51
.. _`empty class`: https://github.com/unifyai/ivy/blob/9c2eb725387152d721040d8638c8f898541a9da4/ivy/__init__.py#L38
.. _`also specified`: https://github.com/unifyai/ivy/blob/9c2eb725387152d721040d8638c8f898541a9da4/ivy/__init__.py#L241
.. _`tuples`: https://github.com/unifyai/ivy/blob/9c2eb725387152d721040d8638c8f898541a9da4/ivy/__init__.py#L256
.. _`valid tuples`: https://github.com/unifyai/ivy/blob/9c2eb725387152d721040d8638c8f898541a9da4/ivy/__init__.py#L303
.. _`invalid tuples`: https://github.com/unifyai/ivy/blob/9c2eb725387152d721040d8638c8f898541a9da4/ivy/__init__.py#L309
.. _`data type class`: https://github.com/unifyai/ivy/blob/a594075390532d2796a6b649785b93532aee5c9a/ivy/functional/backends/torch/__init__.py#L14
.. _`true native data types`: https://github.com/unifyai/ivy/blob/a594075390532d2796a6b649785b93532aee5c9a/ivy/functional/backends/torch/__init__.py#L16
.. _`valid data types`: https://github.com/unifyai/ivy/blob/a594075390532d2796a6b649785b93532aee5c9a/ivy/functional/backends/torch/__init__.py#L29
.. _`invalid data types`: https://github.com/unifyai/ivy/blob/a594075390532d2796a6b649785b93532aee5c9a/ivy/functional/backends/torch/__init__.py#L56
.. _`original definition`: https://github.com/unifyai/ivy/blob/a594075390532d2796a6b649785b93532aee5c9a/ivy/__init__.py#L225
.. _`new definition`: https://github.com/unifyai/ivy/blob/a594075390532d2796a6b649785b93532aee5c9a/ivy/functional/backends/torch/__init__.py#L16
.. _`handled`: https://github.com/unifyai/ivy/blob/a594075390532d2796a6b649785b93532aee5c9a/ivy/backend_handler.py#L194
.. _`data_type.py`: https://github.com/unifyai/ivy/blob/30b7ca4f8a50a52f51884738fe7323883ce891bd/ivy/functional/ivy/data_type.py
.. _`ivy.can_cast`: https://github.com/unifyai/ivy/blob/f18df2e19d6a5a56463fa1a15760c555a30cb2b2/ivy/functional/ivy/data_type.py#L22
.. _`ivy.default_dtype`: https://github.com/unifyai/ivy/blob/f18df2e19d6a5a56463fa1a15760c555a30cb2b2/ivy/functional/ivy/data_type.py#L484
.. _`ivy.set_default_dtype`: https://github.com/unifyai/ivy/blob/30b7ca4f8a50a52f51884738fe7323883ce891bd/ivy/functional/ivy/data_type.py#L536


The data types supported by Ivy are as follows:

* int8
* int16
* int32
* int64
* uint8
* uint16
* uint32
* uint64
* bfloat16
* float16
* float32
* float64
* bool

These are all defined at `import time`_, with each of these set as an `ivy.Dtype`_ instance.
All data types can be queried as attributes of the :code:`ivy` namespace, such as :code:`ivy.float32` etc.

In addition, *native* data types are `also specified`_ at import time.
Likewise, these are all initially set as `ivy.Dtype`_ instances.

There is also an :code:`ivy.NativeDtype` class defined, but this is initially set as an `empty class`_.

The following `tuples`_ are also defined: :code:`all_dtypes`, :code:`all_numeric_dtypes`, :code:`all_int_dtypes`,
:code:`all_float_dtypes`. These each contain all possible data types which fall into the corresponding category.
Each of these tuples is also replicated in a new set of four `valid tuples`_
and a set of four `invalid tuples`_.
When no backend is set, all data types are assumed to be valid, and so the :code:`invalid` tuples are all empty,
and the :code:`valid` tuples are set as equal to the original four tuples.

However, when a backend is set, then some of these are updated.
Firstly, the :code:`ivy.NativeDtype` is replaced with the backend-specific `data type class`_.
Secondly, each of the native data types are replaced with the `true native data types`_.
Thirdly, the `valid data types`_ are updated.
Finally, the `invalid data types`_ are updated.

This leaves each of the data types unmodified,
for example :code:`ivy.float32` will still reference the  `original definition`_ in :code:`ivy/ivy/__init__.py`,
whereas :code:`ivy.native_float32` will now reference the `new definition`_ in
:code:`/ivy/functional/backends/backend/__init__.py`.

The tuples :code:`all_dtypes`, :code:`all_numeric_dtypes`, :code:`all_int_dtypes` and :code:`all_float_dtypes`
are also left unmodified.
Importantly, we must ensure that unsupported data types are removed from the :code:`ivy` namespace.
For example, torch supports :code:`uint8`, but does not support :code:`uint16`, :code:`uint32` or :code:`uint64`.
Therefore, after setting a torch backend via :code:`ivy.set_backend('torch')`,
we should not longer be able to access :code:`ivy.uint16`.
This is `handled`_ in :code:`ivy.set_backend`.

Data Type Module
----------------

The `data_type.py`_ module provides a variety of functions for working with data types.
A few examples include
:code:`astype` which copies an array to a specified data type,
:code:`broadcast_to` which broadcasts an array to a specified shape,
and :code:`result_type` which returns the dtype that results from applying the type promotion rules to the arguments.

Many functions are *convenience* functions, which means that they do not directly modify arrays,
as explained in the :ref:`Function Types` section.

For example,
`ivy.can_cast`_ which determines if one data type can be cast to another data type according to type-promotion rules,
`ivy.dtype`_ which gets the data type for the input array,
`ivy.set_default_dtype`_ which sets the global default data dtype,
and `ivy.default_dtype`_ which returns the correct data type to use,
are all convenience functions.

`ivy.default_dtype`_ is arguably the most important function.
Any function in the functional API that receives a :code:`dtype` argument will make use of this,
as explained below.

Arguments in other Functions
----------------------------

All :code:`dtype` arguments are keyword-only.
All creation functions include the :code:`dtype` argument, for specifying the data type of the created array.
Some other non-creation functions also support the :code:`dtype` argument,
such as :code:`ivy.prod` and :code:`ivy.sum`, but most functions do not include it.
The non-creation functions which do support it are generally functions that involve a compounding reduction across the
array, which could result in overflows, and so an explicit :code:`dtype` argument is useful to handling such cases.

The :code:`dtype` argument is handled in `_function_w_arrays_dtype_n_dev_handled`_ for all functions except those
appearing in `NON_WRAPPED_FUNCTIONS`_ or `NON_DTYPE_WRAPPED_FUNCTIONS`_.
This function calls `ivy.default_dtype`_ in order to determine the correct data type.
As discussed in the :ref:`Function Wrapping` section,
this is applied to all applicable function dynamically during `backend setting`_.

Overall, `ivy.default_dtype`_ infers the data type as follows:

#. if the :code:`dtype` argument is provided, use this directly
#. otherwise, if an array is present in the arguments, set :code:`arr` to this array. \
   This will then be used to infer the data type by calling :code:`ivy.dtype` on the array
#. otherwise, if a *relevant* scalar is present in the arguments, set :code:`arr` to this scalar \
   and derive the data type from this by calling either :code:`ivy.default_int_dtype` or \
   :code:`ivy.default_float_dtype` depending on whether the scalar is an :code:`int` or :code:`float`. \
   This will either return the globally set default :code:`int` or globally set default :code:`float` \
   (settable via :code:`ivy.set_default_int_dtype` and :code:`ivy.set_default_float_dtype` respectively). \
   An example of a *relevant* scalar is :code:`start` in the function :code:`ivy.arange`, \
   which is used to set the starting value of the returned array.\
   Examples of *irrelevant* scalars which should **not** be used for determining the data type are :code:`axis`, \
   :code:`axes`, :code:`dims` etc. which must be integers, and control other configurations of the function \
   being called, with no bearing at all on the data types used by that function.
#. otherwise, if no arrays or relevant scalars are present in the arguments, \
   then use the global default data type, which can either be an :code:`int` or :code:`float` data type. \
   This is settable via :code:`ivy.set_default_dtype`.

For the majority of functions which defer to `_function_w_arrays_dtype_n_dev_handled`_ for handling the data type,
these steps will have been followed and the :code:`dtype` argument will be populated with the correct value
before the backend-specific implementation is even enterred into. Therefore, whereas the :code:`dtype` argument is
listed as optional in the ivy API at :code:`ivy/functional/ivy/category_name.py`,
the argument is listed as required in the backend-specific implementations at
:code:`ivy/functional/backends/backend_name/category_name.py`.

Let's take a look at the function :code:`ivy.prod` as an example.

The implementation in :code:`ivy/functional/ivy/statistical.py` has the following signature:

.. code-block:: python

    def prod(
        x: Union[ivy.Array, ivy.NativeArray],
        axis: Optional[Union[int, Tuple[int]]] = None,
        keepdims: bool = False,
        *,
        dtype: Optional[Union[ivy.Dtype, ivy.NativeDtype]] = None,
        out: Optional[Union[ivy.Array, ivy.NativeArray]] = None,
    ) -> ivy.Array:

Whereas the backend-specific implementations in :code:`ivy/functional/backends/backend_name/statistical.py`
all list :code:`dtype` as required.

Jax:

.. code-block:: python

    def prod(
        x: JaxArray,
        axis: Optional[Union[int, Tuple[int]]] = None,
        keepdims: bool = False,
        *,
        dtype: jnp.dtype,
        out: Optional[JaxArray] = None,
    ) -> JaxArray:

MXNet:

.. code-block:: python

    def prod(
        x: mx.nd.NDArray,
        axis: Optional[Union[int, Tuple[int]]] = None,
        keepdims: bool = False,
        *,
        dtype: type,
        out: Optional[mx.nd.NDArray] = None,
    ) -> mx.nd.NDArray:

NumPy:

.. code-block:: python

    def prod(
        x: np.ndarray,
        axis: Optional[Union[int, Tuple[int]]] = None,
        keepdims: bool = False,
        *,
        dtype: np.dtype,
        out: Optional[np.ndarray] = None,
    ) -> np.ndarray:

TensorFlow:

.. code-block:: python

    def prod(
        x: Tensor,
        axis: Optional[Union[int, Tuple[int]]] = None,
        keepdims: bool = False,
        *,
        dtype: tf.DType,
        out: Optional[Tensor] = None,
    ) -> Tensor:

PyTorch:

.. code-block:: python

    def prod(
        x: torch.Tensor,
        axis: Optional[Union[int, Tuple[int]]] = None,
        keepdims: bool = False,
        *,
        dtype: torch.dtype,
        out: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:

This makes it clear that these backend-specific functions are only enterred into once the correct :code:`dtype`
has been determined.

However, the :code:`dtype` argument for functions listed in `NON_WRAPPED_FUNCTIONS`_ or `NON_DTYPE_WRAPPED_FUNCTIONS`_
are **not** handled by `_function_w_arrays_dtype_n_dev_handled`_,
and so these defaults must be handled by the backend-specific implementations themselves.

One reason for adding a function to `NON_DTYPE_WRAPPED_FUNCTIONS`_ is because it includes *relevant* scalar arguments
for inferring the data type from. `_function_w_arrays_dtype_n_dev_handled`_ is not able to correctly handle such cases,
and so such functions are added to `NON_DTYPE_WRAPPED_FUNCTIONS`_ and the dtype handling is delegated to the
backend-specific implementations.

For example :code:`ivy.full` is listed in `NON_DTYPE_WRAPPED_FUNCTIONS`_ because of the *relevant* :code:`fill_value`
which cannot be correctly handled by `_function_w_arrays_dtype_n_dev_handled`_.

The PyTorch-specific implementation is as follows:

.. code-block:: python

    def full(
        shape: Union[int, Tuple[int]],
        fill_value: Union[int, float],
        *,
        dtype: Optional[Union[ivy.Dtype, torch.dtype]] = None,
        device: torch.device,
    ) -> Tensor:
        return torch.full(
            shape_to_tuple(shape),
            fill_value,
            dtype=ivy.default_dtype(dtype, item=fill_value, as_native=True),
            device=device,
        )

The implementations for all other backends follow a similar pattern to this PyTorch implementation,
where the :code:`dtype` argument is optional and :code:`ivy.default_dtype` is called inside the
backend-specific implementation.
