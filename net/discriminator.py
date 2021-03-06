import torch.nn as nn
import torch.nn.functional as F


class Discriminator(nn.Module):

    def __init__(self, nfilter=64, nChannels=4, isLSGAN=True):

        """
        :param nfilter: filter size of Convolution layer
        :param nChannels: input dimension
        """

        super(Discriminator, self).__init__()
        self.isLSGAN = isLSGAN

        # input : nChannels * 128 * 128
        # output : nfilter * 64 * 64
        self.layer1 = nn.Sequential(
            nn.Conv2d(
                in_channels=nChannels,
                out_channels=nfilter,
                kernel_size=4,
                stride=2,
                padding=1,
                bias=False
            ),
            nn.BatchNorm2d(nfilter),
            nn.LeakyReLU(0.2, inplace=True)
        )

        # input : nfilter * 64 * 64
        # output : nfilter * 32 * 32
        self.layer2 = nn.Sequential(
            nn.Conv2d(
                in_channels=nfilter,
                out_channels=nfilter*2,
                kernel_size=4,
                stride=2,
                padding=1,
                bias=False
            ),
            nn.BatchNorm2d(nfilter*2),
            nn.LeakyReLU(0.2, inplace=True)
        )

        # input : nfilter * 32 * 32
        # output : nfilter * 16 * 16
        self.layer3 = nn.Sequential(
            nn.Conv2d(
                in_channels=nfilter*2,
                out_channels=nfilter*4,
                kernel_size=4,
                stride=2,
                padding=1,
                bias=False
            ),
            nn.BatchNorm2d(nfilter*4),
            nn.LeakyReLU(0.2, inplace=True)
        )

        # input : nfilter * 16 * 16
        # output : nfilter * 8 * 8
        self.layer4 = nn.Sequential(
            nn.Conv2d(
                in_channels=nfilter*4,
                out_channels=nfilter*8,
                kernel_size=4,
                stride=2,
                padding=1,
                bias=False
            ),
            nn.BatchNorm2d(nfilter*8),
            nn.LeakyReLU(0.2, inplace=True)
        )

        # input : nfilter * 8 * 8
        # output : nfilter * 4 * 4
        self.layer5 = nn.Sequential(
            nn.Conv2d(
                in_channels=nfilter * 8,
                out_channels=nfilter * 16,
                kernel_size=4,
                stride=2,
                padding=1,
                bias=False
            ),
            nn.BatchNorm2d(nfilter * 16),
            nn.LeakyReLU(0.2, inplace=True)
        )

        # input : nfilter * 4 * 4
        # output : result of judge Real or Fake
        self.layer6 = nn.Sequential(
            nn.Conv2d(
                in_channels=nfilter*16,
                out_channels=1,
                kernel_size=4,
                stride=1,
                padding=0,
                bias=False
            ),
            # nn.Sigmoid()
        )

    def forward(self, input):

        out = self.layer1(input)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = self.layer5(out)
        out = self.layer6(out)

        if not self.isLSGAN:
            out = F.sigmoid(out)

        return out.view(-1, 1).squeeze(1)
