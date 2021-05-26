#!/usr/bin/env python3
from pathlib import Path
import re
from itertools import groupby
import statistics
import argparse


def main(coverage_out, coverage_output, owner, repo_name, commit_hash, diffs):
    coverage_infos = []

    with coverage_out.open(mode="r", encoding="utf-8") as fr:
        for line in fr:
            if line.startswith("mode:"):
                continue
            base = line.split(repo_name)[-1][1:]
            # internal/domain/size.go:16.2,16.19 1 0
            t = base.split(":")
            fname, info = t[0], t[1]  # internal/domain/size.go // 16.2,16.19 1 0
            if fname not in diffs:
                continue
            if int(base.split(" ")[-1]) > 0:
                continue
            occurline = float(info.split(",")[0])  # 16.2
            coverage_infos.append((occurline, fname))

    with coverage_output.open("w", encoding="utf-8") as fw:
        fw.write("### Details (no coverage condition) \n")

        for key, file_group in groupby(coverage_infos, key=lambda x: x[1]):
            file_group = list(file_group)
            file_group = sorted(file_group, key=lambda x: x[0])

            fw.write("<details>\n")
            fw.write("<summary>{}</summary>\n\n".format(file_group[0][1]))
            for f in file_group:
                fw.write(
                    "https://github.com/{}/{}/blob/{}/{}#L{}-L{}\n\n".format(
                        owner, repo_name, commit_hash, f[1], int(f[0]), int(f[0]) + 4
                    )
                )
            fw.write("</details>\n")


if __name__ == "__main__":
    coverage_output_file = "coverage_d.md"
    coverage_out_fname = "cover.out"

    parser = argparse.ArgumentParser(description="go coverage stats helper")
    parser.add_argument("target_files", metavar="N", type=str, nargs="+", help="")
    parser.add_argument("--repo", type=str)
    parser.add_argument("--commit_hash", type=str)
    args = parser.parse_args()

    owner, repo_name = args.repo.split("/")
    main(
        Path(coverage_out_fname),
        Path(coverage_output_file),
        owner,
        repo_name,
        args.commit_hash,
        args.target_files,
    )
