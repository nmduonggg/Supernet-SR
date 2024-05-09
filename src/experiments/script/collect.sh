python collect_psnr_unc.py \
    --template EUNAF_EDSRx2_bl \
    --testset_tag Set14RGB \
    --N 12492 \
    --testset_dir ../../data/PATCHES_RGB/8x8/ \
    --analyze_dir ./experiments/ANALYZE/ \
    --train_stage 2 \
    --n_resblocks 16 \
    --n_estimators 4 \
    --scale 2 \
    --eval_tag psnr \
    --weight './checkpoints/EUNAF_EDSRx2_bl_x2_nb16_nf64_st2/_best.t7' \