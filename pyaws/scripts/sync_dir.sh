#!/bin/bash

# Define a function to sync files to an S3 bucket
_sync_dir() {
  local source_dir=""
  local save_dir=""
  local notify_after=0
  local profile=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --source-dir)
        source_dir="$2"
        shift 2
        ;;
      --save-dir)
        save_dir="$2"
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

  if [[ -z "$source_dir" || -z "$save_dir" ]]; then
    echo "Usage: sync_to_s3 --source-dir <source_dir> --save-dir <save_dir> [--notify-after <notify_after>] [--profile <profile>]"
    exit 1
  fi
  

  if [ "$notify_after" -eq 0 ]; then
    # If notify-after is 0, suppress stdout by redirecting to /dev/null
    aws s3 sync "$source_dir" "$save_dir" \
      --profile "$profile" > /dev/null
  else

    # Initialize a counter for the number of files synced
    file_sync_count=0
    running_count=0

    # Function to update the progress message
    update_progress() {
      echo "Synced $running_count files to S3."
    }

    # Use the AWS CLI to sync the source directory with the S3 bucket using the specified profile
    aws s3 sync "$source_dir" "$save_dir" \
      --profile "$profile" | while read -r line; do
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
  fi

  echo "Sync completed."
}

_sync_dir "$@"
