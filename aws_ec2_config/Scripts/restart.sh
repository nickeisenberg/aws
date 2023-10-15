#! /bin/bash

aws ec2 reboot-instances \
        --region us-east-1 \
        --instance-ids i-03816f5ae6758ca00 \
        --profile nick
