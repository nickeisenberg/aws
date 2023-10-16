#!/bin/bash

# Function to copy files from a local directory to an S3 bucket
_copy_dir_to_s3() {

  # local SOURCE_DIR="/home/nicholas/Datasets/CelebA/img_64_10"
  # local S3_BUCKET_NAME="celeba-demo-bucket"
  # local PROFILE="nick"
  # local NOTIFY_AFTER=2

  local SOURCE_DIR=""
  local S3_BUCKET_NAME=""
  local PROFILE=""
  local NOTIFY_AFTER=0

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --source-dir)
        SOURCE_DIR="$2"
        shift 2
        ;;
      --bucket-name)
        S3_BUCKET_NAME="$2"
        shift 2
        ;;
      --profile)
        PROFILE="$2"
        shift 2
        ;;
      --notify-after)
        NOTIFY_AFTER="$2"
        shift 2
        ;;
      *)
        echo "Usage: $0 --source-dir <source-directory> --bucket-name <bucket-name> [--notify-after <notify-after>]"
        exit 1
        ;;
    esac
  done

  if [ -z "$SOURCE_DIR" ] || [ -z "$S3_BUCKET_NAME" ]; then
    echo "Both --source-dir and --bucket-name are required."
    exit 1
  fi

  file_count=0
  running_count=0

  # Use the `aws s3 cp` command to copy files to the S3 bucket
  if [ "$NOTIFY_AFTER" -eq 0 ]; then
    # Redirect all output to /dev/null to make it silent
    aws s3 cp "$SOURCE_DIR" "s3://$S3_BUCKET_NAME" \
      --recursive \
      --profile $PROFILE > /dev/null 2>&1
  else
    aws s3 cp "$SOURCE_DIR" "s3://$S3_BUCKET_NAME" \
      --recursive \
      --profile $PROFILE | while IFS= read -r line; do
      ((file_count++))
      ((running_count++))
      if [ "$file_count" -eq "$NOTIFY_AFTER" ]; then
        # echo "Copied $NOTIFY_AFTER files."
        echo "Copied $running_count files."
        file_count=0
      fi
    done
  fi

  # Check the exit status of the `aws s3 cp` command
  if [ $? -eq 0 ]; then
    echo "All files copied successfully to S3."
  else
    echo "Failed to copy files to S3."
  fi
}

# Call the function with provided parameters
_copy_dir_to_s3 "$@"


