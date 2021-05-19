#!/usr/bin/env bash

if [ $# != 2 ]; then
	echo "Usage: "
	echo "sh ./scripts/coverage/coverage.sh <target_branch_name> <source_branch_name>"
	exit 0
fi

# git checkout
git fetch origin $1
git fetch origin $2

# run raw test coverage
go test ./internal/... -coverprofile=cover.out.tmp
cat cover.out.tmp | grep -v "gen.go" >cover.out
go tool cover -func cover.out -o cover.tsv

# formatted coverage
python ./scripts/coverage/coverage_stats.py $(git diff HEAD origin/$2 --name-only) --source_branch origin/$2
python ./scripts/coverage/coverage_details.py $(git diff HEAD origin/$2 --name-only) --source_branch origin/$2

rm -f ./cover.out.tmp
rm -f ./cover.out
rm -f ./cover.tsv
