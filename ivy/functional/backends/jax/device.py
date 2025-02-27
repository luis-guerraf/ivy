"""Collection of Jax device functions, wrapped to fit Ivy syntax and signature."""

# global
import os
import jax
from typing import Union
import jaxlib.xla_extension

# local
import ivy
from ivy.functional.backends.jax import JaxArray
from ivy.functional.ivy.device import Profiler as BaseProfiler


# Helpers #
# --------#


def _to_array(x):
    if isinstance(x, jax.interpreters.ad.JVPTracer):
        return _to_array(x.primal)
    elif isinstance(x, jax.interpreters.partial_eval.DynamicJaxprTracer):
        return _to_array(x.aval)
    return x


# API #
# ----#


def dev(
    x: JaxArray, as_native: bool = False
) -> Union[ivy.Device, jaxlib.xla_extension.Device]:
    if isinstance(x, jax.interpreters.partial_eval.DynamicJaxprTracer):
        return None
    try:
        dv = _to_array(x).device_buffer.device
        dv = dv()
    except Exception:
        dv = jax.devices()[0]
    if as_native:
        return dv
    return as_ivy_dev(dv)


_callable_dev = dev


def to_dev(x, *, device=None, out=None):
    if device is not None:
        cur_dev = as_ivy_dev(_callable_dev(x))
        if cur_dev != device:
            x = jax.device_put(x, as_native_dev(device))
    if ivy.exists(out):
        return ivy.inplace_update(out, x)
    return x


# this is a non-wrapped function used to place JAX arrays on respective devices,
# since if we use to_dev, it will return ivy.array which is not desirable
def _to_dev(x, device=None):
    if device is not None:
        cur_dev = as_ivy_dev(_callable_dev(x))
        if cur_dev != device:
            x = jax.device_put(x, as_native_dev(device))
    return x


def as_ivy_dev(device):
    if isinstance(device, str):
        return ivy.Device(device)
    if device is None:
        return None
    p, dev_id = (device.platform, device.id)
    if p == "cpu":
        return ivy.Device(p)
    return ivy.Device(p + ":" + str(dev_id))


def as_native_dev(device):
    if not isinstance(device, str):
        return device
    dev_split = ivy.Device(device).split(":")
    device = dev_split[0]
    if len(dev_split) > 1:
        idx = int(dev_split[1])
    else:
        idx = 0
    return jax.devices(device)[idx]


clear_mem_on_dev = lambda device: None


def _dev_is_available(base_dev):
    try:
        jax.devices(base_dev)
        return True
    except RuntimeError:
        return False


def gpu_is_available() -> bool:
    return _dev_is_available("gpu")


def num_gpus() -> int:
    try:
        return len(jax.devices("gpu"))
    except RuntimeError:
        return 0


def tpu_is_available() -> bool:
    return _dev_is_available("tpu")


# noinspection PyMethodMayBeStatic
class Profiler(BaseProfiler):
    def __init__(self, save_dir):
        super(Profiler, self).__init__(save_dir)
        self._save_dir = os.path.join(self._save_dir, "profile")

    def start(self):
        jax.profiler.start_trace(self._save_dir)

    def stop(self):
        jax.profiler.stop_trace()

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
