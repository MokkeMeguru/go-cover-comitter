#!/usr/bin/env python
from pathlib import Path
import re
from itertools import groupby
import statistics
import argparse

coverage_output_file = "coverage.md"
coverage_tsv_fname = "cover.tsv"
repo_name = "go-cover-commenter"
head_name = "https://github.com/MokkeMeguru"

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


def main(coverage_tsv_fname, repo_name, branch_name, diffs):
    coverage_tsv = Path(coverage_tsv_fname)
    coverage_funcs = []

    with coverage_tsv.open(mode="r", encoding="utf-8") as fr:
        for line in fr:
            title, func, percept = re.sub(r"\s+", "\t", line).strip().split("\t")
            if title == "total:":
                continue
            iname = title.split(repo_name)[-1].split(":")[0]
            # print(iname[1:] + "\n")
            if iname[1:] not in diffs:
                continue
            title = (repo_name + "/blob/" + branch_name + "").join(
                title.split(repo_name)
            )
            title, line = title.split(":")[:-1]
            url = "https://" + title + "#L" + line
            title = "[{}]({})".format(iname, url)
            # print(title + "\n")
            coverage_funcs.append((iname, title, func, percept))

    coverage_funcs = coverage_funcs
    coverage_output = Path(coverage_output_file)

    with coverage_output.open("w", encoding="utf-8") as fw:
        fw.write("### Coverage Report\n")
        # print(coverage_funcs)
        for key, file_group in groupby(coverage_funcs, key=lambda x: x[0]):
            file_group = list(file_group)
            mean_percept = statistics.mean(
                [float(percept[:-1]) for (_, _, _, percept) in file_group]
            )
            fw.write("<details>" + "\n")
            fw.write(
                "<summary>{}</summary>\n\n".format(
                    key
                    + "\t(average coverage: {} )".format(
                        coverage_shields(mean_percept, "html")
                    )
                )
            )
            fw.write(
                " | " + " | ".join(["line", "function name", "coverage"]) + " | " + "\n"
            )
            fw.write(" | " + " | ".join(["---", "---", "---"]) + " | " + "\n")
            for (iname, title, func, percept) in file_group:
                fw.write(
                    " | "
                    + " | ".join([title, func, coverage_shields(float(percept[:-1]))])
                    + " | "
                    + "\n"
                )
            fw.write("</details>" + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="go coverage stats helper")
    parser.add_argument(
        "--source_branch", type=str, default="develop", help="source branch name"
    )
    parser.add_argument("target_files", metavar="N", type=str, nargs="+", help="")
    args = parser.parse_args()
    # print(args.target_files)
    main(coverage_tsv_fname, repo_name, args.source_branch, args.target_files)
