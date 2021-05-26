#!/usr/bin/env python3
from pathlib import Path
import re
from itertools import groupby
import statistics
import argparse


base_coverage_shields = {
    "md": " ![](https://img.shields.io/static/v1?label=coverage&message={}%&color={}&style=flat-square) ",
    "html": ' <img src="https://img.shields.io/static/v1?label=coverage&message={}%&color={}&style=flat-square"> ',
}


def coverage_shields(percept, doc_type="md"):
    if percept >= 80.0:
        return base_coverage_shields[doc_type].format(percept, "success")
    if percept >= 70.0:
        return base_coverage_shields[doc_type].format(percept, "green")
    if percept >= 60.0:
        return base_coverage_shields[doc_type].format(percept, "important")
    return base_coverage_shields[doc_type].format(percept, "critical")


def main(coverage_tsv, coverage_output, owner, repo_name, commit_hash, diffs):
    coverage_funcs = []

    with coverage_tsv.open(mode="r", encoding="utf-8") as fr:
        for line in fr:
            # line: github.com/MokkeMeguru/go-coverage-commenter/internal/domain/size.go:3:	Size		33.3%
            title, func, percept = re.sub(r"\s+", "\t", line).strip().split("\t")
            # title: github.com/MokkeMeguru/go-coverage-commenter/internal/domain/size.go:3:
            # func : Size
            # percept: 33.3%
            if title == "total:":
                continue
            base = title.split(repo_name)[-1].split(":")
            file_path, line = base[0][1:], base[1]
            # iname :  internal/domain/size.go
            # line : 3
            if file_path not in diffs:
                continue
            # url : "https://github.com/MokkeMeguru/go-coverage-commenter/blob/cas2424gds/internal/domain/size.go#L3"
            url = "https://github.com/{}/{}/blob/{}/{}#L{}".format(
                owner, repo_name, commit_hash, file_path, line
            )
            title_link = "[{}]({})".format(file_path, url)
            coverage_funcs.append((file_path, title_link, func, percept))

    with coverage_output.open("w", encoding="utf-8") as fw:
        fw.write("## Coverage Report\n")

        for key, file_group in groupby(coverage_funcs, key=lambda x: x[0]):
            file_group = list(file_group)
            mean_percept = statistics.mean(
                [float(percept[:-1]) for (_, _, _, percept) in file_group]
            )
            fw.write("<details>\n")
            fw.write(
                "<summary>{}</summary> (average coverage: {})\n".format(
                    key, coverage_shields(mean_percept, "html")
                )
            )
            fw.write(
                " | {} | \n".format(" | ".join(["line", "function name", "coverage"]))
            )
            fw.write(" | {} | \n".format(" | ".join(["---", "---", "---"])))
            for (iname, title, func, percept) in file_group:
                fw.write(
                    " | {} | \n".format(
                        " | ".join([title, func, coverage_shields(float(percept[:-1]))])
                    )
                )
            fw.write("</details>\n")
        fw.write("\n")


if __name__ == "__main__":
    coverage_output_file = "coverage.md"
    coverage_tsv_fname = "cover.tsv"

    parser = argparse.ArgumentParser(description="go coverage stats helper")
    parser.add_argument("target_files", metavar="N", type=str, nargs="+", help="")
    parser.add_argument("--repo", type=str)
    parser.add_argument("--commit_hash", type=str)
    args = parser.parse_args()

    owner, repo_name = args.repo.split("/")
    main(
        Path(coverage_tsv_fname),
        Path(coverage_output_file),
        owner,
        repo_name,
        args.commit_hash,
        args.target_files,
    )
