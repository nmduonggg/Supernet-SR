python test_eunaf_by_patches.py \
    --template EUNAF_EDSRx3_bl \
    --testset_tag Set5RGB \
    --N 5 \
    --testset_dir ../../data/ \
    --train_stage 2 \
    --n_resblocks 16 \
    --n_estimators 4 \
    --scale 3 \
    --eval_tag psnr \
    # --visualize