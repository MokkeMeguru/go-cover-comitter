#!/usr/bin/env python3
from pathlib import Path
import re
from itertools import groupby
import statistics
import argparse

coverage_output_file = "coverage_d.md"
coverage_out_fname = "cover.out"
repo_name = "go-cover-commenter"


def main(coverage_out_fname, repo_name, branch_name, diffs):
    coverage_out = Path(coverage_out_fname)
    coverage_output = Path(coverage_output_file)
    coverage_infos = []

    with coverage_out.open(mode="r", encoding="utf-8") as fr:
        for line in fr:
            if line.startswith("mode:"):
                continue
            base = line.split(repo_name)[-1][
                1:
            ]  # internal/domain/size.go:16.2,16.19 1 0
            t = base.split(":")
            fname, info = t[0], t[1]  # internal/domain/size.go // 16.2,16.19 1 0
            if int(base.split(" ")[-1]) > 0:
                continue
            occurline = float(info.split(",")[0])  # 16.2
            coverage_infos.append((occurline, fname))

    with coverage_output.open("w", encoding="utf-8") as fw:
        for key, file_group in groupby(coverage_infos, key=lambda x: x[1]):
            file_group = list(file_group)
            file_group = sorted(file_group, key=lambda x: x[0])
            for f in file_group:
                fw.write("{}:{}: no coverage \n".format(f[1], f[0]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="go coverage stats helper")
    parser.add_argument(
        "--source_branch", type=str, default="develop", help="source branch name"
    )
    parser.add_argument("target_files", metavar="N", type=str, nargs="+", help="")
    args = parser.parse_args()
    print(args.target_files)
    main(coverage_out_fname, repo_name, args.source_branch, args.target_files)
