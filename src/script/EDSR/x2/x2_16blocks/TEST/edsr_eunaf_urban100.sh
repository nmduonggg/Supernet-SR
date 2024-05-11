python test_eunaf_by_patches.py \
    --template EUNAF_EDSRx2_bl \
    --testset_tag Urban100 \
    --N 100 \
    --testset_dir ../../data/Urban100/ \
    --train_stage 2 \
    --n_resblocks 16 \
    --n_estimators 4 \
    --scale 2 \
    --eval_tag ssim \
    # --visualize