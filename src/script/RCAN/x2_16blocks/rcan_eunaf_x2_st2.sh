python train_eunaf.py \
    --template EUNAF_RCANx2 \
    --N 14 \
    --scale 2 \
    --train_stage 2 \
    --n_resblocks 2 \
    --n_resgroups 8 \
    --max_epochs 1000 \
    --lr 0.0001 \
    --testset_tag='Set14RGB' \
    --testset_dir='../../data/' \
    --trainset_preload 400 \
    --wandb \
    --weight '/mnt/disk1/nmduong/FusionNet/Supernet-SR/src/checkpoints/EUNAF_EDSRx2_bl_x2_nb4_nf64_st0/_best.t7' \
    # --lr 0.00
    # --max_load 1000