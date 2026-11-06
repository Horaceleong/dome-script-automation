# 從地心到日心 — 流動球幕 Augmented Lesson

用 Digitalis（Digitarium / Nightshade G3）系統重演「地心說 → 日心說」的演變過程。
一鍵自動播放全場，也可分段播放。純播放約 8 分鐘，含講解約 15 分鐘。

## 安裝

把整個 `lessons/zhuoyue/geocentric-to-heliocentric/` 目錄放進主媒體碟的
`lessons/zhuoyue/` 下，同步到 Digitarium 主機後，在 Universal Console 的
**Lessons** 分頁開啟「從地心到日心」。

```
lessons/zhuoyue/geocentric-to-heliocentric/
├── index.html          ← 課程主檔（旁白 + 按鈕）
├── README.md
├── scripts/            ← StratoScript（G3 24.4）
│   ├── 00_reset.sts               重置場景（收拾殘局也用它）
│   ├── 01_celestial-sphere.sts    天球旋轉
│   ├── 02_retrograde.sts          火星逆行（恆星日步進）
│   ├── 03_ptolemy.sts             托勒密本輪（示意圖疊加）
│   ├── 04_copernicus.sts          飛出太陽系 + 逆行幾何
│   ├── 05_kepler.sts              橢圓與等面積
│   ├── 06_galileo.sts             木星衛星 + 金星相位 + 時間線
│   ├── 07_epilogue.sts            尾聲
│   └── show_all.sts               ← 一鍵全場（由分段腳本自動合成）
├── media/              ← 9 張示意圖（1920×1080 16:9 透明 PNG，dome 母版）
└── thumbs/             ← 縮圖（320×180）
```

## 分幕設計（教學邏輯）

| 幕 | 內容 | 模擬技術 |
|---|---|---|
| 1 | 天球：星空像殼一樣轉，地心說的感官基礎 | `timerate rate 900` 快轉 |
| 2 | 火星逆行（2027-02-19 衝） | 以 `date sidereal 2` 步進，星空凍結、只看行星 |
| 3 | 托勒密本輪 + 完整地心宇宙（天球殼） | `image` 疊加示意圖 |
| 4 | 兩模型對照、日心翻轉：俯瞰軌道、地球超車、逆行幾何、恒星視差 | `moveto object Sun lat 82 alt 4AU` + `timerate rate 400000` |
| 5 | 開普勒：橢圓、等面積 | 水星偏心率 0.206，快轉看近日點加速 |
| 6 | 伽利略：木星衛星、金星相位、時間線 | `zoom auto in` 看衛星系統 |
| 7 | 尾聲：太陽也不是中心 | 回地球夜空看銀河 |

## 開演前要調整的參數

| 參數 | 位置 | 說明 |
|---|---|---|
| 觀測地點 | 各腳本 `lat 22.30 lon 114.17` | 預設香港，改成你的城市 |
| 示意圖方位 | `altitude 42 azimuth 180` | dome 坐標以焦點方向為準；投影機焦點不同就調 azimuth |
| 逆行窗口 | `02_retrograde.sts` 的 `date utc 2026-12-05...` 與步數 | 火星下次衝：2029-03-25，屆時改日期與步數 |
| 快轉倍率 | 各 `timerate rate` | 播放卡頓就調低一個量級 |
| 開場日期 | `00_reset.sts` `date utc` | 任意晚上皆可，第 2 幕會自己跳到逆行窗口 |

## 已知限制（請在現場驗證）

- 腳本依 G3 24.4 手冊撰寫，**未在實機上跑過**；`moveto object Sun lat 82`
  的俯視角度、`zoom auto in` 的衛星系統視角，可能需要微調。
- 本腳本刻意不用 G3 的分類學 `set planetary...` 指令，NG 21.7 亦可播放；
  但 `configuration action load name default` 會重置到操作者的預設配置。
- 火星逆行的可視性取決於 `zoom fov 32` 與步進節奏（2 恒星日/步），
  想慢一點把 `wait duration 0.35` 調到 0.5–0.8。
- 示意圖為示意（非等比例）；`03-retrograde-geometry.png` 是按真實
  週期關係計算繪制的，`09-parallax.png` 的視差角大幅誇大（實際 < 1 角秒），
  其餘為概念圖。
- 媒體清理原則：每一幕結尾 `image action drop` 自己載入的圖；
  中途手動跳幕留下殘影時，播一次 `00_reset.sts` 即可清乾淨。

## 維護

改了任何分段腳本後，重新合成全場檔：

```
python build/build_show_all.py    # 重新產生 scripts/show_all.sts
python build/lint_sts.py          # 語法與媒體引用檢查
python build/make_images.py       # 重新產生示意圖（可選）
```

## 授權

腳本與示意圖：CC BY 4.0。StratoScript、Nightshade、Digitarium 是
Digitalis Education Solutions, Inc. 的商標。
