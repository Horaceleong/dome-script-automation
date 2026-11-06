# -*- coding: utf-8 -*-
"""把分段腳本串成一支全自動的 show_all.sts（單一來源，避免內容分歧）。"""
import os, re

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "lessons", "zhuoyue", "geocentric-to-heliocentric", "scripts")
SEGMENTS = ["00_reset.sts", "01_celestial-sphere.sts", "02_retrograde.sts",
            "03_ptolemy.sts", "04_copernicus.sts", "05_kepler.sts",
            "06_galileo.sts", "07_epilogue.sts"]

out = ["require projection_type fisheye version 24.4.0 release professional", ""]
out.append("# ============================================================")
out.append("# 全自動播放：從地心說到日心說（約 15 分鐘）")
out.append("# 本檔由 build/build_show_all.py 產生，請改分段腳本後重新產生。")
out.append("# ============================================================")
out.append("")

for i, seg in enumerate(SEGMENTS):
    path = os.path.join(BASE, seg)
    lines = open(path, encoding="utf-8").read().splitlines()
    body = [ln for ln in lines if not ln.strip().startswith("require ")]
    title = next((ln.split("｜")[1].split("—")[0].strip() for ln in body
                  if ln.strip().startswith("# 第")), seg)
    out.append("")
    out.append("# " + "─" * 40)
    out.append("# >>> " + seg + "  " + title)
    out.append("# " + "─" * 40)
    out.extend(body)

dst = os.path.join(BASE, "show_all.sts")
open(dst, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("wrote", dst, len(out), "lines")
