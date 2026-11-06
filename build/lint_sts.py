# -*- coding: utf-8 -*-
"""輕量檢查 .sts：指令名、參數成對、無前導空白、媒體/路徑引用存在。"""
import os, sys, re

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "lessons", "zhuoyue", "geocentric-to-heliocentric")

COMMANDS = {
    "audio", "body", "clear", "color", "configuration", "cove_lights", "date",
    "deselect", "external_viewer", "flag", "flyto", "image", "landscape",
    "layer", "meteors", "moveto", "nebula", "point_cloud", "require",
    "script", "select", "set", "sky_culture", "soundscape", "text",
    "timerate", "video", "wait", "zoom",
}

FLAG_ARGS = {
    "atmosphere", "azimuthal_grid", "cardinal_points", "clouds", "circumpolar_circle",
    "constellation_art", "constellation_boundaries", "constellation_lines",
    "constellation_names", "constellation_pick", "ecliptic_line", "equator_line",
    "equatorial_grid", "force_land_heading", "galactic_grid", "galaxy_points",
    "j2000_grid", "landscape", "light_pollution", "light_travel_time", "manual_zoom",
    "media_captions", "meridian_line", "milky_way", "moon_scaled", "navigation_px_line",
    "navigation_zx_line", "nebula_names", "planet_names", "planet_orbits",
    "precession_circle", "script_gui_debug", "shadow_volumes", "show_framerate",
    "show_tui_datetime", "show_tui_short_obj_info", "star_names", "star_twinkle",
    "stars", "time_lapse", "track_object", "translate_constellation_names",
    "tropic_lines",
}

errors = []
files = sorted(f for f in os.listdir(os.path.join(BASE, "scripts")) if f.endswith(".sts"))
for fn in files:
    path = os.path.join(BASE, "scripts", fn)
    for n, raw in enumerate(open(path, encoding="utf-8").read().splitlines(), 1):
        if raw != raw.strip():
            errors.append(f"{fn}:{n} 前導/尾隨空白")
        line = raw.split("#")[0].strip()
        if not line:
            continue
        if line != raw.strip():
            errors.append(f"{fn}:{n} 註解外有 tab/連續空白？ -> {line[:40]}")
        toks = re.findall(r'"[^"]*"|\S+', line)
        cmd = toks[0].lower()
        if cmd not in COMMANDS:
            errors.append(f"{fn}:{n} 未知指令: {toks[0]}")
            continue
        if len(toks) % 2 != 1 and cmd not in {"deselect", "clear", "script"}:
            # 大多數指令需要偶數個參數（名/值成對）；deselect/clear 可裸用
            errors.append(f"{fn}:{n} 參數數量為奇數: {line[:60]}")
        if cmd == "flag" and len(toks) >= 2 and toks[1].lower() not in FLAG_ARGS:
            errors.append(f"{fn}:{n} flag 參數不在清單中: {toks[1]} (檢查手冊)")
        if cmd == "image" and "filename" in [t.lower() for t in toks]:
            i = [t.lower() for t in toks].index("filename")
            fnm = toks[i + 1].strip('"')
            p = os.path.normpath(os.path.join(BASE, "scripts", fnm))
            if not os.path.exists(p):
                errors.append(f"{fn}:{n} 找不到媒體檔: {fnm}")

if errors:
    print("== 發現問題 ==")
    for e in errors:
        print(" -", e)
else:
    print("OK：全部", len(files), "個腳本通過檢查")
