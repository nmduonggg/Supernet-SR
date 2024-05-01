import os

def set_template(args):
    if args.template == 'SuperNet_udl':
        print('[INFO] Template found (UDL-like SR)')
        args.style='Y'
        args.rgb_range=1.0
        args.core='SuperNet_udl'
        args.weight = os.path.join(args.cv_dir, '_best.t7')
    elif args.template == 'SuperNet_udl_RGB':
        print('[INFO] Template found (UDL-like SR)')
        args.style='RGB'
        args.rgb_range=1.0
        args.input_channel=3
        args.core='SuperNet_udl'
        args.weight = os.path.join(args.cv_dir, '_best.t7')
    elif  args.template == 'SuperNet_separate':
        print('[INFO] Template found (Separate SR)')
        args.style='Y'
        args.rgb_range=1.0
        args.core='SuperNet_separate'
        args.weight = os.path.join(args.cv_dir, '_best.t7')
    elif  args.template == 'SuperNet_separate_RGB':
        print('[INFO] Template found (Separate SR)')
        args.style='RGB'
        args.rgb_range=1.0
        args.input_channel=3
        args.core='SuperNet_separate'
        args.weight = os.path.join(args.cv_dir, '_best.t7')
    elif  args.template == 'EUNAF_EDSRx2_bl':
        print('[INFO] Template found (Separate SR)')
        args.style='RGB'
        args.rgb_range=1.0
        args.input_channel=3
        args.core='EUNAF_EDSR'
        args.scale=2
        args.weight = "/mnt/disk1/nmduong/FusionNet/Supernet-SR/src/checkpoints/EUNAF_EDSRx2_bl_nblock1/_best.t7"
        print(vars(args))
    elif  args.template == 'EUNAF_EDSRx2':
        print('[INFO] Template found (Separate SR)')
        args.style='RGB'
        args.rgb_range=255.0
        args.input_channel=3
        args.core='EUNAF_EDSR'
        args.n_resblocks=32
        args.n_feats=256
        args.input_channel=3
        args.res_scale=0.1
        args.scale=2
        args.weight = "/mnt/disk1/nmduong/FusionNet/Supernet-SR/src/checkpoints/PRETRAINED/EDSR/edsr_x2-0edfb8a3.pt"
        print(vars(args))
    else:
        print('[ERRO] Template not found')
        assert(0)
