python test_eunaf_by_patches.py \
    --template EUNAF_SMSRxN \
    --testset_tag BSD100 \
    --N 100 \
    --testset_dir ../../data/BSD100/ \
    --train_stage 2 \
    --n_resblocks 16 \
    --n_estimators 4 \
    --scale 2 \
    --eval_tag psnr \
    # --visualize