import chainer
import typing


class FusionLayer(chainer.Chain):
    def __init__(self):
        super().__init__(
            conv=chainer.functions.Convolution2D(
                in_channels=None,
                out_channels=256,
                ksize=1,
            )
        )

    def __call__(
            self,
            h: chainer.Variable,
            one_dimension_feature_list: typing.List[chainer.Variable],
            test: bool = False,
    ):
        batchsize = h.data.shape[0]
        height = h.data.shape[2]
        width = h.data.shape[3]

        h_global = chainer.functions.concat(one_dimension_feature_list)

        channel = h_global.data.shape[1]
        h_global = chainer.functions.broadcast_to(h_global, (height, width, batchsize, channel))
        h_global = chainer.functions.transpose(h_global, (2, 3, 0, 1))
        h = chainer.functions.concat((h, h_global))

        h = chainer.functions.relu(self.conv(h))
        return h
