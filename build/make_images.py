# -*- coding: utf-8 -*-
"""
生成《從地心到日心》球幕課程所需的示意圖。
輸出：透明背景 1920x1080（16:9 dome 母版）PNG（media/）+ 320x180 縮圖（thumbs/）
說明：投影到半球面由播放器做 dome warp；母版一律 16:9，內容置於中央安全區。
"""
import os, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Polygon, FancyArrowPatch, Ellipse, FancyBboxPatch
from matplotlib.font_manager import FontProperties

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "lessons", "zhuoyue", "geocentric-to-heliocentric")
MEDIA = os.path.join(BASE, "media")
THUMB = os.path.join(BASE, "thumbs")
os.makedirs(MEDIA, exist_ok=True)
os.makedirs(THUMB, exist_ok=True)

FONT_PATH = "C:/Windows/Fonts/msjh.ttc"
F = lambda s: FontProperties(fname=FONT_PATH, size=s)
FB = lambda s: FontProperties(fname=FONT_PATH, size=s, weight="bold")

# 球幕配色：深底 + 暖白文字，避免純白過曝
BG      = (0.020, 0.028, 0.055)
INK     = "#f4f1e8"
INK_DIM = "#9aa7bd"
GOLD    = "#f0b429"
EMBER   = "#e8724c"
BLUE    = "#5aa9e6"
TEAL    = "#59c3a6"
VIOLET  = "#a98bdb"


# 16:9 dome 母版：資料座標 y ±1.18，x 依比例放大；圓形內容居中於安全區
YMAX = 1.18
XMAX = YMAX * 16.0 / 9.0          # ≈ 2.098


def canvas(title=None, subtitle=None):
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-XMAX, XMAX)
    ax.set_ylim(-YMAX, YMAX)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_facecolor((0, 0, 0, 0))
    fig.patch.set_alpha(0.0)
    # 柔和暗底圓角面板：投影到半球時邊角會被 warp 自然吸收
    panel = FancyBboxPatch((-XMAX + 0.05, -YMAX + 0.05),
                           2 * XMAX - 0.10, 2 * YMAX - 0.10,
                           boxstyle="round,pad=0,rounding_size=0.16",
                           transform=ax.transData,
                           facecolor=BG, edgecolor="#2b3a55", lw=1.2,
                           alpha=0.80, zorder=0)
    ax.add_patch(panel)
    if title:
        ax.text(0, 1.055, title, fontproperties=FB(23), color=INK,
                ha="center", va="center", zorder=30)
    if subtitle:
        ax.text(0, 0.985, subtitle, fontproperties=F(13.5), color=INK_DIM,
                ha="center", va="center", zorder=30)
    return fig, ax


def save(fig, name):
    p = os.path.join(MEDIA, name)
    fig.savefig(p, dpi=100, transparent=True, facecolor="none")
    plt.close(fig)
    from PIL import Image
    im = Image.open(p).convert("RGBA")
    im.thumbnail((320, 180), Image.LANCZOS)
    im.save(os.path.join(THUMB, name))
    print("saved", name, im.size)


# ---------------------------------------------------------------- 1 托勒密本輪
def fig_ptolemy():
    fig, ax = canvas("地心說：本輪疊在均輪上",
                     "用「圓套圓」把行星的來回走動折疊出來  ·  Ptolemy, c. 150 AD")
    R, r, n = 0.62, 0.16, 5.0          # 均輪半徑／本輪半徑／本輪相對轉速
    t = np.linspace(0, 2 * np.pi, 3000)
    x = R * np.cos(t) + r * np.cos(-n * t)
    y = R * np.sin(t) + r * np.sin(-n * t)
    ax.plot(x, y, color=GOLD, lw=1.6, alpha=0.55, zorder=6)

    ax.add_patch(Circle((0, 0), R, fill=False, ec=BLUE, lw=1.6, alpha=0.85, zorder=5))
    ax.text(0, -R - 0.075, "均輪  deferent", fontproperties=F(13), color=BLUE,
            ha="center", va="center", zorder=20)

    # 地球
    ax.add_patch(Circle((0, 0), 0.052, color="#5aa9e6", zorder=12))
    ax.add_patch(Circle((0, 0), 0.075, fill=False, ec="#5aa9e6", lw=1.0, alpha=0.4, zorder=11))
    ax.text(0, -0.145, "地球", fontproperties=FB(15), color="#cfe6ff",
            ha="center", va="center", zorder=20)

    # 某一時刻的均輪／本輪連線
    t0 = 1.15
    cx, cy = R * np.cos(t0), R * np.sin(t0)
    px, py = cx + r * np.cos(-n * t0), cy + r * np.sin(-n * t0)
    ax.plot([0, cx], [0, cy], color=BLUE, lw=1.0, ls=(0, (4, 3)), alpha=0.55, zorder=8)
    ax.add_patch(Circle((cx, cy), r, fill=False, ec=VIOLET, lw=1.4, alpha=0.9, zorder=9))
    ax.text(cx + r * 0.72, cy + r * 1.42, "本輪  epicycle", fontproperties=F(12.5),
            color=VIOLET, ha="center", va="center", zorder=20)
    ax.plot([cx, px], [cy, py], color=VIOLET, lw=1.0, ls=(0, (3, 3)), alpha=0.7, zorder=9)
    ax.add_patch(Circle((px, py), 0.028, color=EMBER, zorder=13))

    # 標出逆行段
    ax.annotate("這裡倒退走\n＝逆行", xy=(-0.34, 0.47), xytext=(-0.55, 0.82),
                fontproperties=F(12.5), color=EMBER, ha="center", va="center", zorder=25,
                arrowprops=dict(arrowstyle="-|>", color=EMBER, lw=1.3,
                                connectionstyle="arc3,rad=0.25"))
    ax.text(0, -1.03,
            "均輪＋本輪能算出行星位置，誤差約 1–2°；這個模型用了 1400 年。",
            fontproperties=F(12.5), color=INK_DIM, ha="center", va="center", zorder=30)
    save(fig, "01-ptolemy.png")


# ---------------------------------------------------------------- 2 哥白尼日心
def fig_copernicus():
    fig, ax = canvas("日心說：把太陽放回中心",
                     "行星越遠、跑得越慢  ·  Copernicus, 1543")
    planets = [("水星", 0.26, TEAL), ("金星", 0.40, GOLD),
               ("地球", 0.56, BLUE), ("火星", 0.72, EMBER),
               ("木星", 0.88, "#d9a066")]
    for name, rad, col in planets:
        ax.add_patch(Circle((0, 0), rad, fill=False, ec=col, lw=1.3, alpha=0.55, zorder=5))
        ang = rad * 4.2 + 1.8
        ax.add_patch(Circle((rad * math.cos(ang), rad * math.sin(ang)), 0.030,
                            color=col, zorder=12))
        ax.text(rad * math.cos(ang + 0.30) * 1.06, rad * math.sin(ang + 0.30) * 1.06 + 0.045,
                name, fontproperties=F(12), color=col, ha="center", va="center", zorder=20)

    ax.add_patch(Circle((0, 0), 0.075, color=GOLD, zorder=14))
    gl = Circle((0, 0), 0.115, facecolor=GOLD, edgecolor="none", alpha=0.22, zorder=13)
    ax.add_patch(gl)
    ax.text(0, -0.175, "太陽", fontproperties=FB(14.5), color=GOLD,
            ha="center", va="center", zorder=20)

    ax.annotate("同一方向、內圈先跑完\n→ 從地球看，外行星就「倒退」",
                xy=(0.72, -0.50), xytext=(1.50, -0.82),
                fontproperties=F(12.5), color=INK_DIM, ha="center", va="center", zorder=25,
                arrowprops=dict(arrowstyle="-|>", color=INK_DIM, lw=1.0,
                                connectionstyle="arc3,rad=-0.2"))
    # 比例尺說明
    ax.text(0, -1.03, "圖為示意，非等比；軌道在哥白尼系統裡仍是正圓。",
            fontproperties=F(12), color=INK_DIM, ha="center", va="center", zorder=30)
    save(fig, "02-copernicus.png")


# ---------------------------------------------------------- 3 逆行幾何（算出來的）
def fig_retrograde():
    fig, ax = canvas("行星為什麼會倒退",
                     "地球在內圈超車時，視線方向跟著反轉")
    rE, rM = 0.50, 0.72                      # 地球／火星軌道半徑（示意比例）
    wE, wM = 1.0, 1.0 / 1.881                # 角速度 ∝ 1/週期
    ax.add_patch(Circle((0, 0), rE, fill=False, ec=BLUE, lw=1.2, alpha=0.5, zorder=4))
    ax.add_patch(Circle((0, 0), rM, fill=False, ec=EMBER, lw=1.2, alpha=0.5, zorder=4))

    # 對衝放在左上方 140°，讓視線指向圖內有空的區域
    PHI = math.radians(140)
    ts = np.linspace(-0.50, 0.50, 500)       # 年
    angE = PHI + wE * ts
    angM = PHI + wM * ts
    ex = rE * np.cos(angE); ey = rE * np.sin(angE)
    mx = rM * np.cos(angM); my = rM * np.sin(angM)
    dx = mx - ex; dy = my - ey
    sight_ang = np.arctan2(dy, dx)           # 從地球看火星的視線方向
    RP = 0.99                                 # 「星空」投影半徑
    px = RP * np.cos(sight_ang); py = RP * np.sin(sight_ang)
    d = np.diff(np.unwrap(sight_ang))
    retro = np.concatenate([[d[0]], d]) < 0   # 視線方向角在變小 ⇒ 逆行

    # 星空圓弧背景
    th = np.linspace(np.min(sight_ang) - 0.30, np.max(sight_ang) + 0.30, 200)
    ax.plot(RP * np.cos(th), RP * np.sin(th), color=INK, lw=1.4, alpha=0.20, zorder=3)
    ax.text(RP * math.cos(math.radians(196)), RP * math.sin(math.radians(196)) - 0.055,
            "星空（示意）", fontproperties=F(11), color=INK_DIM,
            ha="center", va="center", zorder=25)

    # 逆行段（金）與順行段（灰）
    segs, cur = [], [0]
    for i in range(1, len(ts)):
        if retro[i] == retro[i - 1]:
            cur.append(i)
        else:
            segs.append(cur); cur = [i]
    segs.append(cur)
    for s in segs:
        col = GOLD if retro[s[0]] else "#8fa2bd"
        lw = 2.8 if retro[s[0]] else 1.8
        al = 0.95 if retro[s[0]] else 0.65
        ax.plot(px[s], py[s], color=col, lw=lw, alpha=al, zorder=16,
                solid_capstyle="round")

    idx = [int(round(i)) for i in np.linspace(0, len(ts) - 1, 7)]
    for i in idx:
        ax.plot([ex[i], px[i]], [ey[i], py[i]], color=INK, lw=0.6, alpha=0.20, zorder=6)
        ax.add_patch(Circle((ex[i], ey[i]), 0.015, color=BLUE, zorder=11))
        ax.add_patch(Circle((mx[i], my[i]), 0.017, color=EMBER, zorder=11))

    ax.add_patch(Circle((0, 0), 0.052, color=GOLD, zorder=14))
    ax.text(0, -0.105, "太陽", fontproperties=F(12), color=GOLD,
            ha="center", va="center", zorder=20)
    i0 = idx[3]
    ax.text(ex[i0] + 0.075, ey[i0] - 0.075, "地球", fontproperties=F(11.5), color=BLUE,
            ha="center", va="center", zorder=20)
    ax.text(mx[i0] + 0.10, my[i0] + 0.02, "火星", fontproperties=F(11.5), color=EMBER,
            ha="center", va="center", zorder=20)
    ax.annotate("金色這段在星空上倒著走＝逆行；\n灰色兩段照常向前",
                xy=(px[int(len(ts) * 0.52)], py[int(len(ts) * 0.52)]),
                xytext=(0.85, 0.60),
                fontproperties=F(12.5), color=INK, ha="center", va="center", zorder=25,
                arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=1.2,
                                connectionstyle="arc3,rad=0.15"))
    ax.text(0, -1.03, "地球 365 天一圈、火星 687 天一圈；每 780 天左右超車一次。",
            fontproperties=F(12), color=INK_DIM, ha="center", va="center", zorder=30)
    save(fig, "03-retrograde-geometry.png")


# ---------------------------------------------------------------- 4 開普勒橢圓
def fig_kepler():
    """橢圓 + 等面積。兩塊扇形各佔 1/12 週期，面積由開普勒方程反解，確實相等。"""
    fig, ax = canvas("開普勒：圓不夠圓",
                     "橢圓、等面積、週期定律  ·  Kepler, 1609 / 1619")
    a, e = 0.80, 0.42
    b = a * math.sqrt(1 - e * e)
    c = a * e
    ax.add_patch(Ellipse((0, 0), 2 * a, 2 * b, fill=False, ec=BLUE, lw=1.7, alpha=0.9, zorder=6))

    DM = 2 * math.pi / 12.0          # 各佔 1/12 週期 ⇒ 掃過面積必然相同

    def solve_half(dm, near_perihelion):
        """給定 ΔM（= 掃過面積的 2/ab 倍），反解偏心近點角半寬 d。"""
        def f(d):
            return (2 * d - 2 * e * math.sin(d)) if near_perihelion \
                else (2 * d + 2 * e * math.sin(d))
        lo, hi = 0.0, math.pi
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if f(mid) < dm:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    d_peri = solve_half(DM, True)      # 近日點（E 以 0 為中心）
    d_aph = solve_half(DM, False)      # 遠日點（E 以 π 為中心）

    def sector(E0, E1, color):
        th = np.linspace(E0, E1, 600)
        pts = np.vstack([[(c, 0)], np.column_stack([a * np.cos(th), b * np.sin(th)])])
        poly = Polygon(pts, closed=True, facecolor=color, edgecolor="none",
                       alpha=0.32, zorder=4)
        ax.add_patch(poly)
        return poly

    sector(-d_peri, d_peri, EMBER)              # 近日點：寬而短
    sector(math.pi - d_aph, math.pi + d_aph, TEAL)   # 遠日點：窄而長

    ax.add_patch(Circle((c, 0), 0.055, color=GOLD, zorder=14))
    ax.text(c, -0.125, "太陽（焦點）", fontproperties=F(12), color=GOLD,
            ha="center", va="center", zorder=20)
    ax.plot([-c], [0], marker="+", color=INK_DIM, ms=12, mew=1.5, zorder=12)
    ax.text(-c, 0.095, "空焦點", fontproperties=F(11), color=INK_DIM,
            ha="center", va="center", zorder=20)

    ax.text(a + 0.045, 0.14, "近日點\n掃得快", fontproperties=F(11.5), color=EMBER,
            ha="left", va="center", zorder=20)
    ax.text(-a - 0.045, 0.145, "遠日點\n掃得慢", fontproperties=F(11.5), color=TEAL,
            ha="right", va="center", zorder=20)
    ax.annotate("同樣 1/12 個週期\n掃過的面積完全相同",
                xy=(0.14, 0.26), xytext=(0.05, 0.62),
                fontproperties=F(12.5), color=INK, ha="center", va="center", zorder=25,
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.0))
    ax.text(0, -1.03, "火星離心率 0.093、水星 0.206；差 8 角分就得換掉正圓。",
            fontproperties=F(12), color=INK_DIM, ha="center", va="center", zorder=30)
    save(fig, "04-kepler.png")


# ---------------------------------------------------------------- 5 金星相位
def fig_venus():
    fig, ax = canvas("金星的相位，誰說了算",
                     "地心說只能給出蛾眉相；實測卻看到完整的一輪")

    def draw_venus(cx, cy, rad, phase, col):
        """phase: 0 = 全暗（新月），0.5 = 半，1 = 全亮。
        亮面 = 右側邊緣弧 + 終止線（半橢圓，x 半軸 = -rad*k）圍成的區域。"""
        k = 2.0 * phase - 1.0
        ax.add_patch(Circle((cx, cy), rad, facecolor="#101827", edgecolor=col,
                            lw=1.0, alpha=1.0, zorder=8))
        t1 = np.linspace(-math.pi / 2, math.pi / 2, 90)          # 右側邊緣（下→上）
        limb_x = cx + rad * np.cos(t1)
        limb_y = cy + rad * np.sin(t1)
        t2 = np.linspace(math.pi / 2, -math.pi / 2, 90)          # 終止線（上→下）
        term_x = cx - rad * k * np.cos(t2)
        term_y = cy + rad * np.sin(t2)
        pts = np.vstack([np.column_stack([limb_x, limb_y]),
                         np.column_stack([term_x, term_y])])
        ax.add_patch(Polygon(pts, closed=True, facecolor=col, edgecolor="none",
                             alpha=0.92, zorder=9))
        ax.add_patch(Circle((cx, cy), rad, fill=False, edgecolor=col, lw=1.0,
                            alpha=0.75, zorder=10))

    # 上排：地心說預測（永遠是蛾眉）
    ax.text(-1.30, 0.80, "地心說預測", fontproperties=FB(15), color=EMBER,
            ha="left", va="center", zorder=25)
    for i, ph in enumerate([0.10, 0.16, 0.22]):
        draw_venus(-1.10 + i * 0.55, 0.52, 0.085, ph, EMBER)
    ax.text(0, 0.28, "金星永遠在太陽附近——只能是蛾眉狀，而且大小不變",
            fontproperties=F(12.5), color=INK_DIM, ha="center", va="center", zorder=25)

    ax.plot([-1.55, 1.55], [0.16, 0.16], color="#2b3a55", lw=1.2, alpha=0.8, zorder=6)

    # 下排：實測（完整相位，大小變化）
    ax.text(-1.30, 0.00, "伽利略 1610 年看到的", fontproperties=FB(15), color=TEAL,
            ha="left", va="center", zorder=25)
    for i, (ph, rad) in enumerate([(0.96, 0.052), (0.62, 0.085), (0.20, 0.125)]):
        draw_venus(-1.10 + i * 0.55, -0.30, rad, ph, TEAL)
    ax.text(0, -0.62, "相位從滿到細鉤都有，而且越細越大",
            fontproperties=F(12.5), color=INK_DIM, ha="center", va="center", zorder=25)
    ax.text(0, -0.72, "→ 金星繞的是太陽，不是地球",
            fontproperties=FB(13), color=TEAL, ha="center", va="center", zorder=25)

    ax.text(0, -1.03, "同一時期伽利略還看到四顆小星繞木星轉——不是所有東西都繞地球。",
            fontproperties=F(12), color=INK_DIM, ha="center", va="center", zorder=30)
    save(fig, "05-venus-phases.png")


# ---------------------------------------------------------------- 6 時間線
def fig_timeline():
    fig, ax = canvas("一千五百年，一場坐標系的搬遷")

    items = [
        ("c.150", "托勒密《天文學大成》", "本輪＋均輪，精度 1–2°", BLUE),
        ("1543", "哥白尼《天體運行論》", "太陽居中，仍用正圓", TEAL),
        ("1576", "第谷開始 20 年觀測", "裸眼精度 1–2 角分", "#9aa7bd"),
        ("1609", "開普勒《新天文學》", "火星軌道是橢圓", GOLD),
        ("1610", "伽利略《星際信使》", "木星衛星、金星相位", VIOLET),
        ("1687", "牛頓《原理》", "引力給出橢圓的成因", EMBER),
    ]
    LX = -1.05                              # 時間軸（寬幅下置於左側、整體置中）
    y = 0.72
    ax.plot([LX, LX], [0.74, -0.78], color="#2b3a55", lw=2.0, alpha=0.9, zorder=4)
    for yr, title, note, col in items:
        ax.add_patch(Circle((LX, y), 0.028, color=col, zorder=10))
        ax.text(LX + 0.07, y + 0.038, yr, fontproperties=FB(15), color=col,
                ha="left", va="center", zorder=20)
        ax.text(LX + 0.30, y + 0.038, title, fontproperties=F(14), color=INK,
                ha="left", va="center", zorder=20)
        ax.text(LX + 0.30, y - 0.038, note, fontproperties=F(11.5), color=INK_DIM,
                ha="left", va="center", zorder=20)
        y -= 0.245

    ax.text(0, -1.03, "注意：哥白尼沒有讓預報立刻變準；真正拉開差距的是開普勒的橢圓。",
            fontproperties=F(12), color=INK_DIM, ha="center", va="center", zorder=30)
    save(fig, "06-timeline.png")


# ---------------------------------------------------------- 7 地心宇宙殼層
def fig_geocosmos():
    fig, ax = canvas("地心宇宙：一層一層的天球殼")
    rings = [("月球天", 0.20, "#cfd8e3"), ("水星天", 0.305, TEAL),
             ("金星天", 0.41, GOLD), ("太陽天", 0.515, "#f5a623"),
             ("火星天", 0.62, EMBER), ("木星天", 0.73, "#d9a066"),
             ("土星天", 0.84, VIOLET), ("恒星期（不動）", 0.945, INK)]
    for name, rad, col in rings:
        ax.add_patch(Circle((0, 0), rad, fill=False, ec=col, lw=1.4,
                            alpha=0.75, zorder=5))
        ax.text(0, rad + 0.022, name, fontproperties=F(12.5), color=col,
                ha="center", va="center", zorder=20)

    ax.add_patch(Circle((0, 0), 0.052, color="#5aa9e6", zorder=12))
    ax.add_patch(Circle((0, 0), 0.075, fill=False, ec="#5aa9e6", lw=1.0,
                        alpha=0.4, zorder=11))
    ax.text(0.02, -0.115, "地球", fontproperties=FB(14), color="#cfe6ff",
            ha="center", va="center", zorder=20)

    ax.text(0, -1.02, "天球殼一天繞地球一圈；行星在殼之間向東漂，殼外是「原動力天」。",
            fontproperties=F(11.5), color=INK_DIM, ha="center", va="center", zorder=30)
    save(fig, "07-geocentric-cosmos.png")


# ---------------------------------------------------------- 8 兩種模型對照
def fig_two_models():
    fig, ax = canvas("同一片星空，兩套宇宙",
                     "差別只有一件事：中心放在哪裡")
    CX = {"L": -1.05, "R": 1.05}
    CY = 0.10

    # 左：地心說——本輪真的在倒退
    R, r, n = 0.18, 0.05, 5.0
    t = np.linspace(0, 2 * np.pi, 2200)
    x = CX["L"] + R * np.cos(t) + r * np.cos(-n * t)
    y = CY + R * np.sin(t) + r * np.sin(-n * t)
    ax.plot(x, y, color=GOLD, lw=1.5, alpha=0.7, zorder=6)
    ax.add_patch(Circle((CX["L"], CY), R, fill=False, ec=BLUE, lw=1.2,
                        alpha=0.7, zorder=5))
    ax.add_patch(Circle((CX["L"], CY), 0.035, color="#5aa9e6", zorder=12))
    ax.text(CX["L"], 0.62, "地心說", fontproperties=FB(16), color=BLUE,
            ha="center", va="center", zorder=25)
    ax.text(CX["L"], -0.42, "行星在本輪上真的走回頭路", fontproperties=F(12),
            color=INK, ha="center", va="center", zorder=25)
    ax.text(CX["L"], -0.51, "要用幾層圓才能算準", fontproperties=F(11.5),
            color=INK_DIM, ha="center", va="center", zorder=25)

    # 右：日心說——地球超車造成的錯覺
    rE, rM = 0.11, 0.175
    ax.add_patch(Circle((CX["R"], CY), rE, fill=False, ec=BLUE, lw=1.2,
                        alpha=0.7, zorder=5))
    ax.add_patch(Circle((CX["R"], CY), rM, fill=False, ec=EMBER, lw=1.2,
                        alpha=0.7, zorder=5))
    ax.add_patch(Circle((CX["R"], CY), 0.035, color=GOLD, zorder=12))
    # 地球兩個位置 + 視線反向
    for i, ang in enumerate([math.radians(200), math.radians(320)]):
        ex = CX["R"] + rE * math.cos(ang); ey = CY + rE * math.sin(ang)
        mx = CX["R"] + rM * math.cos(ang * 0.53); my = CY + rM * math.sin(ang * 0.53)
        ax.plot([ex, mx], [ey, my], color=INK, lw=0.7, alpha=0.25, zorder=6)
        ax.add_patch(Circle((ex, ey), 0.014, color=BLUE, zorder=11))
        ax.add_patch(Circle((mx, my), 0.016, color=EMBER, zorder=11))
    ax.text(CX["R"], 0.62, "日心說", fontproperties=FB(16), color=GOLD,
            ha="center", va="center", zorder=25)
    ax.text(CX["R"], -0.42, "地球在內圈超車，火星只是被「比過去」",
            fontproperties=F(12), color=INK, ha="center", va="center", zorder=25)
    ax.text(CX["R"], -0.51, "一套簡單的幾何就夠了", fontproperties=F(11.5),
            color=INK_DIM, ha="center", va="center", zorder=25)

    ax.plot([0, 0], [0.66, -0.55], color="#2b3a55", lw=1.2,
            alpha=0.9, zorder=4)
    ax.text(0, -1.03, "兩套都算得出行星位置——當年的勝負不在准，在簡潔與證據。",
            fontproperties=F(12), color=INK_DIM, ha="center", va="center", zorder=30)
    save(fig, "08-two-models.png")


# ---------------------------------------------------------- 9 恒星視差
def fig_parallax():
    fig, ax = canvas("日心說最大的難題：恒星視差",
                     "地球若在動，星空應該輕微搖晃——但當時看不到")

    # 遠方星空弧
    bx = np.linspace(-0.45, 0.55, 100)
    by = 0.62 + 0.010 * np.cos(np.linspace(0, np.pi, 100))
    ax.plot(bx, by, color="#5c6b82", lw=1.6, alpha=0.8, zorder=4)
    ax.text(-0.52, 0.665, "遠方星空", fontproperties=F(11.5), color="#5c6b82",
            ha="center", va="center", zorder=20)

    # 地球軌道（下方，誇大明顯）
    ax.add_patch(Circle((0, -0.72), 0.22, fill=False, ec=BLUE, lw=1.3,
                        ls=(0, (4, 3)), alpha=0.8, zorder=5))
    ex1, ey1 = -0.22, -0.72
    ex2, ey2 = 0.22, -0.72
    ax.add_patch(Circle((ex1, ey1), 0.026, color=BLUE, zorder=11))
    ax.add_patch(Circle((ex2, ey2), 0.026, color=BLUE, zorder=11))
    ax.text(ex1, ey1 - 0.065, "6 月", fontproperties=F(11.5), color=BLUE,
            ha="center", va="center", zorder=20)
    ax.text(ex2, ey2 - 0.065, "12 月", fontproperties=F(11.5), color=BLUE,
            ha="center", va="center", zorder=20)
    ax.text(0, -0.685, "太陽", fontproperties=F(11.5), color=GOLD,
            ha="center", va="center", zorder=20)
    ax.add_patch(Circle((0, -0.72), 0.048, color=GOLD, zorder=12))

    # 近星
    sx, sy = 0.10, 0.35
    ax.add_patch(Circle((sx, sy), 0.034, color="#fdf6e3", zorder=12))
    ax.add_patch(Circle((sx, sy), 0.055, fill=False, ec="#fdf6e3",
                        lw=0.8, alpha=0.5, zorder=11))
    ax.text(sx + 0.10, sy + 0.05, "近星", fontproperties=F(12), color="#fdf6e3",
            ha="center", va="center", zorder=20)

    # 兩條視線與延長線
    ARC_Y = 0.585
    for ex, ey, col in [(ex1, ey1, GOLD), (ex2, ey2, TEAL)]:
        dx, dy = sx - ex, sy - ey
        k = (ARC_Y - ey) / dy
        qx, qy = ex + dx * k, ARC_Y
        ax.plot([ex, sx], [ey, sy], color=col, lw=1.3, alpha=0.85, zorder=7)
        ax.plot([sx, qx], [sy, qy], color=col, lw=1.0, ls=(0, (3, 3)),
                alpha=0.65, zorder=7)
        ax.add_patch(Circle((qx, qy), 0.014, color=col, zorder=13))
        globals()[f"q_{col}"] = (qx, qy)
    qa = globals()["q_" + GOLD]; qb = globals()["q_" + TEAL]
    ax.annotate("", xy=qa, xytext=qb,
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.2), zorder=15)
    ax.text((qa[0] + qb[0]) / 2 + 0.05, (qa[1] + qb[1]) / 2 + 0.055, "視差角（圖中大幅誇大）",
            fontproperties=F(11.5), color=INK, ha="center", va="center", zorder=25)

    ax.text(0, -1.03, "哥白尼時代量不到視差，成了日心說最大的反駁；",
            fontproperties=F(12), color=INK_DIM, ha="center", va="center", zorder=30)
    ax.text(0, -1.095, "1838 年白塞耳才在天鵝座 61 量到 0.3 角秒——星星比我們想的遠得多。",
            fontproperties=F(12), color=INK_DIM, ha="center", va="center", zorder=30)
    save(fig, "09-parallax.png")


if __name__ == "__main__":
    fig_ptolemy()
    fig_copernicus()
    fig_retrograde()
    fig_kepler()
    fig_venus()
    fig_timeline()
    fig_geocosmos()
    fig_two_models()
    fig_parallax()
