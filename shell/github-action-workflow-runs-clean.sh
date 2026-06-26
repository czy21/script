#!/bin/bash

export GH_TOKEN=

github_user=$1
github_repo=$2

count=1

while true; do
  echo "=== Batch $count: Fetching runs... ==="
  
  ids=$(gh api -X GET -F per_page=100 /repos/${github_user}/${github_repo}/actions/runs --jq '.workflow_runs[] | select(.status=="completed") | .id')
  
  if [ -z "$ids" ]; then
    echo "No more completed runs found. Finished!"
    break
  fi

  for t in $ids; do
    echo "Delete: $t"
    gh api -X DELETE /repos/${github_user}/${github_repo}/actions/runs/$t --silent
  done

  echo "=== Batch $count completed. ==="
  count=$((count + 1))
done