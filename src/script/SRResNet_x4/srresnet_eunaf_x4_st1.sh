python train_eunaf_no_freeze_srr.py \
    --template EUNAF_SRResNetxN \
    --N 14 \
    --scale 4 \
    --train_stage 1 \
    --max_epochs 600 \
    --lr 0.00005 \
    --testset_tag='Set14RGB' \
    --testset_dir='../../data/' \
    --trainset_preload 100 \
    --rgb_channel \
    --n_estimators 4 \
    --weight './checkpoints/EUNAF_SRResNetxN_x2_nb16_nf64_st0/_best.t7' \
    # --wandb \
    # --lr 0.00
    # --max_load 1000