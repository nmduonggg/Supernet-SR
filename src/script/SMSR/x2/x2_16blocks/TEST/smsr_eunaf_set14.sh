python test_eunaf_by_patches.py \
    --template EUNAF_SMSRxN \
    --testset_tag Set14RGB \
    --N 14 \
    --testset_dir ../../data/ \
    --train_stage 2 \
    --n_resblocks 16 \
    --n_estimators 4 \
    --scale 2 \
    --eval_tag ssim \
    --weight './checkpoints/EUNAF_EDSRx2_bl_x2_nb16_nf64_st1/_best.t7' \
    # --visualize \