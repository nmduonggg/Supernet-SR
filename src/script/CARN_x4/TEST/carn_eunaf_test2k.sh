python test_eunaf_by_patches.py \
    --template EUNAF_CARNxN \
    --testset_tag Test2K \
    --N 100 \
    --testset_dir ../../data/test2k/ \
    --train_stage 1 \
    --n_resblocks 16 \
    --n_estimators 4 \
    --scale 4 \
    --eval_tag ssim \
    --rgb_channel \
    # --visualize