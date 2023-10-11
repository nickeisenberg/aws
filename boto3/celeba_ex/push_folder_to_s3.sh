#! /bin/bash

start=$(date +%s)
aws s3 sync \
    /home/nicholas/Datasets/CelebA/img_transformed_100 \
    s3://celeba-for-tut/celeba_imgs \
    --profile nick
end=$(date +%s)
echo "Elapsed Time: $(($end-$start)) seconds"
