"""Base class for deriving trainable modules"""

# local
from ivy.stateful.module import Module


class Sequential(Module):
    def __init__(self, *sub_modules, device=None, v=None):
        """
        A sequential container. Modules will be added to it in the order they are
        passed in the constructor.

        Parameters
        ----------
        submodules
            Submodules to chain together into a sequence.
        device
            device on which to create the layer's variables 'cuda:0', 'cuda:1', 'cpu'
            etc.
        v
            the variables for each submodule in the sequence, constructed internally by
            default.

        """
        if v is not None:
            for i, submod in enumerate(sub_modules):
                try:
                    submod.v = v["submodules"]["v" + str(i)]
                except KeyError:
                    if submod.v:
                        raise Exception(
                            "variables v passed to Sequential class must have key "
                            "chains in the form of "
                            '"submodules/v{}", where {} is an idx'
                        )
        self._submodules = list(sub_modules)
        Module.__init__(self, device, v)

    def _forward(self, inputs):
        """
        Perform forward pass of the Linear layer.

        Parameters
        ----------
        inputs
            Inputs to process.

        Returns
        -------
        ret
            The outputs following the linear operation and bias addition.

        """
        x = inputs
        for i, submod in enumerate(self._submodules):
            try:
                x = submod(x, v=self.v.submodules["v" + str(i)])
            except KeyError:
                if submod.v:
                    raise Exception(
                        "variables v passed to Sequential class must have key chains "
                        "in the form of "
                        '"submodules/v{}", where {} is an idx'
                    )
                x = submod(x)
        return x
