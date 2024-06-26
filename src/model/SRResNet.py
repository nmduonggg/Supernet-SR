import functools
import torch.nn as nn
import torch.nn.functional as F
from model import common

import numpy as np



def make_layer(block, n_layers):
    layers = []
    for _ in range(n_layers):
        layers.append(block())
    return nn.ModuleList(layers)


class ResidualBlock_noBN(nn.Module):
    '''Residual block w/o BN
    ---Conv-ReLU-Conv-+-
     |________________|
    '''

    def __init__(self, nf=64):
        super(ResidualBlock_noBN, self).__init__()
        self.conv1 = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)
        self.conv2 = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)

        # initialization
        common.initialize_weights([self.conv1, self.conv2], 0.1)

    def forward(self, x):
        identity = x
        out = F.relu(self.conv1(x), inplace=True)
        out = self.conv2(out)
        return identity + out


class MSRResNet(nn.Module):
    ''' modified SRResNet'''

    def __init__(self, args, conv=common.default_conv):
        super(MSRResNet, self).__init__()
        
        self.in_nc = in_nc = args.input_channel
        self.out_nc = out_nc = args.input_channel 
        self.nf = nf = args.n_feats 
        self.upscale = scale = args.scale[0] if type(args.scale)==tuple else args.scale    # [HxW] or [HxH]
        self.nb = nb = args.n_resblocks
        self.n_estimators = n_estimators = args.n_estimators
        self.kernel_size = kernel_size = 3

        self.conv_first = nn.Conv2d(in_nc, nf, 3, 1, 1, bias=True)
        basic_block = functools.partial(ResidualBlock_noBN, nf=nf)
        self.recon_trunk = make_layer(basic_block, nb)

        # upsampling
        if self.upscale == 2:
            self.upconv1 = nn.Conv2d(nf, nf * 4, 3, 1, 1, bias=True)
            self.pixel_shuffle = nn.PixelShuffle(2)
        elif self.upscale == 3:
            self.upconv1 = nn.Conv2d(nf, nf * 9, 3, 1, 1, bias=True)
            self.pixel_shuffle = nn.PixelShuffle(3)
        elif self.upscale == 4:
            self.upconv1 = nn.Conv2d(nf, nf * 4, 3, 1, 1, bias=True)
            self.upconv2 = nn.Conv2d(nf, nf * 4, 3, 1, 1, bias=True)
            self.pixel_shuffle = nn.PixelShuffle(2)

        self.HRconv = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)
        self.conv_last = nn.Conv2d(nf, out_nc, 3, 1, 1, bias=True)

        # activation function
        self.lrelu = nn.LeakyReLU(negative_slope=0.1, inplace=True)

        # initialization
        common.initialize_weights([self.conv_first, self.upconv1, self.HRconv, self.conv_last], 0.1)
        if self.upscale == 4:
            common.initialize_weights(self.upconv2, 0.1)

    def forward(self, x):
        fea = self.lrelu(self.conv_first(x))
        for i in range(self.nb):
            out = self.recon_trunk(fea)

        if self.upscale == 4:
            out = self.lrelu(self.pixel_shuffle(self.upconv1(out)))
            out = self.lrelu(self.pixel_shuffle(self.upconv2(out)))
        elif self.upscale == 3 or self.upscale == 2:
            out = self.lrelu(self.pixel_shuffle(self.upconv1(out)))

        out = self.conv_last(self.lrelu(self.HRconv(out)))
        base = F.interpolate(x, scale_factor=self.upscale, mode='bilinear', align_corners=False)
        out += base
        return out
    
class EUNAF_MSRResNet(MSRResNet):
    def __init__(self, args, conv=common.default_conv):
        super(EUNAF_MSRResNet, self).__init__(args, conv=conv) 
        self.n_estimators = min(args.n_estimators, self.nb // 2)
        self.gap = (self.nb-4) // (self.n_estimators-1)
        # print("Locate EE at location: ", self.gap_range.tolist())
        
        self.predictors = self.init_intermediate_out(self.n_estimators-1, conv, out_channels=args.input_channel, last_act=False)
        self.estimators = self.init_intermediate_out(self.n_estimators, conv, out_channels=args.input_channel,is_estimator=True, last_act=False)
            
    def get_n_estimators(self):
        return self.n_estimators
        
    def init_intermediate_out(self, num_blocks, conv,
                              out_channels=1, is_estimator=False, 
                              last_act=False):
        
        interm_predictors = nn.ModuleList()
        
        for i in range(num_blocks):
            if is_estimator:
                m_tail = [
                    conv(self.nf, 16, 3), nn.LeakyReLU(0.1),
                    conv(16, out_channels*self.upscale*self.upscale, 3),
                    nn.PixelShuffle(self.upscale), nn.LeakyReLU(0.1),
                    conv(out_channels, out_channels, 1)
                ]
            else:
                
                if i==num_blocks-1:
                    m_tail = [
                        conv(self.nf, self.nf*4, 3),
                        nn.PixelShuffle(2), nn.LeakyReLU(0.1),
                        conv(self.nf, self.nf, 3),
                        nn.PixelShuffle(2), nn.LeakyReLU(0.1),
                        conv(self.nf//4, out_channels, 3)
                    ] 
                else:
                    m_tail = [
                        conv(self.nf, self.nf*2, self.kernel_size),
                        nn.PixelShuffle(2), nn.LeakyReLU(0.1),
                        conv(self.nf//2, out_channels*4, 3),
                        nn.PixelShuffle(2), nn.LeakyReLU(0.1),
                        conv(out_channels, out_channels, 1)
                    ]
            common.initialize_weights(m_tail, 0.1)
            if last_act: m_tail.append(nn.ELU())
            interm_predictors.append(nn.Sequential(*m_tail))
            
        return interm_predictors
    
    def freeze_backbone(self):
        for n, p in self.named_parameters():
            if 'estimators' not in n:
                p.requires_grad = False
                # for i in range(self.nb):
                #     if i > (self.nb - self.n_estimators)-1 and 'recon_trunk' in n and str(i) in n:
                #         p.requires_grad=True
            if p.requires_grad:
                print(n, end=' ')
    
    def enable_estimators_only(self):
        for n, p in self.named_parameters():
            if 'estimators' not in n:
                p.requires_grad = False
            if p.requires_grad:
                print(n, end=' ')
    
    def forward(self, x):
        
        outs, masks = list(), list()
        base = F.interpolate(x, scale_factor=self.upscale, mode='bilinear', align_corners=False)
        
        
        fea = self.lrelu(self.conv_first(x))
        # gap_range = np.arange(2, self.nb, self.gap)
        # tmp_gap_range = self.gap_range[:-1] if len(gap_range)==self.n_estimators else self.gap_range
        tmp_gap_range = [self.nb-1, self.nb-1]
        
        cnt = 0
        for i in range(self.nb):
            fea = self.recon_trunk[i](fea)
            
            if i == self.nb-1:
                
                for j in range(self.n_estimators-1):
                    tmp_out = self.predictors[j](fea)
                    outs.append(tmp_out+base)
                
                
                for j in range(self.n_estimators):
                    mask = self.estimators[j](fea)
                    masks.append(mask)
                        
        if self.upscale == 4:
            fea = self.lrelu(self.pixel_shuffle(self.upconv1(fea)))
            out = self.lrelu(self.pixel_shuffle(self.upconv2(fea)))
        elif self.upscale == 3 or self.upscale == 2:
            out = self.lrelu(self.pixel_shuffle(self.upconv1(fea)))
        out = self.conv_last(self.lrelu(self.HRconv(out)))  
        
        out += base
        
        outs.append(out)
                        
        return outs, masks
    
    def eunaf_forward(self, x):
        
        outs, masks = list(), list()
        base = F.interpolate(x, scale_factor=self.upscale, mode='bilinear', align_corners=False)
        
        
        fea = self.lrelu(self.conv_first(x))
        # gap_range = np.arange(2, self.nb, self.gap)
        # tmp_gap_range = self.gap_range[:-1] if len(gap_range)==self.n_estimators else self.gap_range
        tmp_gap_range = [self.nb-1, self.nb-1]
        
        cnt = 0
        for i in range(self.nb):
            fea = self.recon_trunk[i](fea)
            
            if i == self.nb-1:
                
                for j in range(self.n_estimators-1):
                    tmp_out = self.predictors[j](fea)
                    outs.append(tmp_out+base)
                
                
                for j in range(self.n_estimators):
                    mask = self.estimators[j](fea)
                    masks.append(mask)
                        
        if self.upscale == 4:
            fea = self.lrelu(self.pixel_shuffle(self.upconv1(fea)))
            out = self.lrelu(self.pixel_shuffle(self.upconv2(fea)))
        elif self.upscale == 3 or self.upscale == 2:
            out = self.lrelu(self.pixel_shuffle(self.upconv1(fea)))
        out = self.conv_last(self.lrelu(self.HRconv(out)))  
        
        out += base
        
        outs.append(out)
                        
        return outs, masks