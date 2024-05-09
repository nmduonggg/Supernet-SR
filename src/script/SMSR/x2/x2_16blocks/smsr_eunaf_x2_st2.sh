python train_eunaf.py \
    --template EUNAF_SMSRxN \
    --N 14 \
    --scale 2 \
    --train_stage 2 \
    --n_resblocks 16 \
    --n_estimators 4 \
    --max_epochs 1000 \
    --lr 0.00001 \
    --testset_tag='Set14RGB' \
    --testset_dir='../../data/' \
    --trainset_preload 400 \
    --weight './checkpoints/EUNAF_EDSRx2_bl_x2_nb16_nf64_st1/_best.t7' \
    # --wandb \
    # --lr 0.00
    # --max_load 1000