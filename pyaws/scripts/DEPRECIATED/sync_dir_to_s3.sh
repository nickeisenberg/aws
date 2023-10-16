#!/bin/bash

# Define a function to sync files to an S3 bucket
_sync_dir_to_s3() {
  local source_dir=""
  local bucket_name=""
  local notify_after=0
  local profile=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --source-dir)
        source_dir="$2"
        shift 2
        ;;
      --bucket-name)
        bucket_name="$2"
        shift 2
        ;;
      --notify-after)
        notify_after="$2"
        shift 2
        ;;
      --profile)
        profile="$2"
        shift 2
        ;;
      *)
        echo "Invalid argument: $1"
        exit 1
        ;;
    esac
  done

  if [[ -z "$source_dir" || -z "$bucket_name" ]]; then
    echo "Usage: sync_to_s3 --source-dir <source_dir> --bucket-name <bucket_name> [--notify-after <notify_after>] [--profile <profile>]"
    exit 1
  fi
 
  # Initialize a counter for the number of files synced
  file_sync_count=0
  running_count=0

  # Function to update the progress message
  update_progress() {
    echo "Synced $running_count files to S3."
  }

  # Use the AWS CLI to sync the source directory with the S3 bucket using the specified profile
  aws s3 sync "$source_dir" "s3://$bucket_name/" $([[ -n "$profile" ]] && echo "--profile $profile") | while read -r line; do
    # Increment the file_sync_count
    ((file_sync_count++))
    ((running_count++))

    # Check if it's time to update the progress message
    if [ "$file_sync_count" -ge "$notify_after" ]; then
      update_progress
      # Reset the file_sync_count
      file_sync_count=0
    fi
  done

  # Update the progress message for any remaining files
  if [ "$file_sync_count" -gt 0 ]; then
    update_progress
  fi

  echo "Sync completed successfully."
}

_sync_dir_to_s3 "$@"
