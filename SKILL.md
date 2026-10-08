---
name: handdrawn-lyric-mv
description: 把一首中文歌做成逐帧手绘的歌词 MV（简体或繁体）。歌词始终是同一套多彩拼贴打字（逐字打出，写在纸标签、黑缎带、招牌、对联、路牌、印章、夜空里，或砸拍大字）；画面每首歌都按歌词重新设计、重新画（角色、道具、地点、母题都从这首歌里来），粗墨线、平涂、线条抖动、一拍两张。可以做整首或高潮片段，Python 生成 SVG，HyperFrames 合成和渲染。用户说“手绘歌词 MV”“用《风吹新竹》那种风格给这首歌做 MV”“把这首歌做成手绘动画”时使用。只要卡点快剪、照片幻灯片或其他画风时，用 music-to-video。
---

# 逐帧手绘歌词 MV

一首歌 → 一支手绘歌词 MV。分两部分：
- **固定不变的**：歌词版式（多彩拼贴打字，`typo.py`）和画法（墨线、平涂、抖线、一拍两张）。
- **每首歌重新做的**：画面。读歌词，定这首歌的主角、道具、地点和母题，一件件新画出来，先出素材表确认，再拼成镜头。

节拍分析、合成、检查、渲染交给 HyperFrames（`music-to-video` 的 `analyze-beatgrid.py`，`hyperframes check / snapshot / render`）。

第一支作品是 hoy neo《风吹新竹》，全曲 3 分 26 秒、24 个镜头。完整工程不随技能发布，部分镜头脚本和画法收在 `examples/风吹新竹/`。它的人物和道具只作画法参考，不能搬进新歌。

## 依赖

- **基础工具**：Node（`npx hyperframes@0.8.123`）、Python 3、ffmpeg、`uv`（临时装 librosa、fontTools、OpenCC）。
- **另装的技能**：`music-to-video`（HyperFrames 系列），用它的 `scripts/analyze-beatgrid.py`。
- **中文字体**：按用字从 Google Fonts 取子集（需要联网），也可以用本地字体文件做子集。

`SKILL` 指本技能目录，`P` 指 MV 工程目录。工具都在 `$SKILL/scripts/tools/`。

## 流程

**0. 确认输入**
- **必需**：歌曲文件；歌词，最好是带时间的 LRC。
- **按需确认**：
  - 简体还是繁体：默认简体，繁体为台湾正体；
  - 做整首还是片段；
  - 主题一句话：用户没给就从歌词里提一版，请用户确认。
- 画面固定为横屏 1920×1080。

确认后都写进 `P/BRIEF.md`。

**1. 建工程**

```bash
python3 $SKILL/scripts/tools/new_project.py P 歌.mp3 --title 歌名 --artist 署名 --year 2026 --script zh-Hans   # 繁体用 zh-Hant
python3 $SKILL/scripts/tools/analyze.py P          # → assets/audiomap.json，打印小节线、能量段、强拍
python3 $SKILL/scripts/tools/lyrics.py P 歌词.lrc  # → assets/lyrics.json，打印每句时间和最近的小节线
```

**2. 读歌词，设计画面**：按 [歌词转画面](references/歌词转画面.md) 填 `P/设计/意象表.md`。
- **全片**：主题、谁在唱、母题、角色、地点、颜色节奏。
- **逐句**：画面里有什么（至少一样东西直接来自这句歌词），歌词放在哪个版式组件上，要新画哪些素材。

**3. 画素材**：这首歌的角色和道具，写成 `P/scripts/assets/*.py` 里的函数，写法照 `_example.py`。

```bash
python3 $SKILL/scripts/tools/asset_sheet.py P      # → 设计/素材表.png（一页 8 件），打开逐件看
```

- 画法用 `draw.py` 的基础件，规则见 [画风规范](references/画风规范.md)。
- 歌词点名的具体东西一律新画；地方特色先查资料，查不到确切样子的不画。

**4. 分镜**：按 [全曲规划](references/全曲规划.md) 把歌切成镜头。
- 用 `repeats.py` 找重复的副歌，能复用的画面就复用。
- 镜头表写进 `mv.json` 的 `scenes`，再整理成 `STORYBOARD.md`（时间、段落、歌词、画面、歌词放在哪）。
- **检查点 1：分镜 + 素材表一起请用户确认。** 用户要求改的素材先改好再往下做。

**5. 字体**：把歌名、署名、招牌和站名这类不在歌词里的字写进 `mv.json` 的 `extra_text`，然后运行：

```bash
python3 $SKILL/scripts/tools/fonts.py P fetch      # 取子集，写出 charset.txt；构建时缺字会直接报错
```

`mv.json` 的 `script` 决定全片简体还是繁体。生成镜头时，每个文字节点会统一转换：繁体用 OpenCC `s2tw`（台湾正体，能分清“裡面/公里”“著/着”），简体用 `t2s`。繁体片的大字自动换成 Chiron GoRound TC 900，因为站酷快乐体没有繁体字。

**6. 画镜头**：每个镜头一个脚本 `P/scripts/scenes/<id>.py`，从 `_template.py` 复制。
- **画面**：用 `scripts/assets/` 里这首歌自己的素材，配上 `draw.py` 的天气、植物等基础件。
- **歌词**：一律用 `typo.py` 的组件，规则见 [歌词版式](references/歌词版式.md)。
- **动作和镜头套路**：见 [动效与避坑](references/动效与避坑.md)、[镜头配方](references/镜头配方.md)。

```bash
python3 $SKILL/scripts/tools/build.py P <id>                     # 生成 compositions/scenes/<id>.html
python3 $SKILL/scripts/tools/preview.py P <id> --at t1,t2,t3     # 截图拼成一张图，打开逐张看
```

- **每个镜头都要截图看过再往下做。** 看什么见“动效与避坑”最后的检查清单。
- **检查点 2：先做 1–2 个代表镜头**，用 `preview.py P <id…> --video 样片.mp4` 出一段带音乐的样片，请用户确认画风和节奏，再铺开做全片。

**7. 拼接与检查**

```bash
python3 $SKILL/scripts/tools/assemble.py P --snap  # 镜头切点对齐到整帧（移动不超过 17 毫秒），分段渲染需要
python3 $SKILL/scripts/tools/build.py P            # 重建全部镜头
python3 $SKILL/scripts/tools/assemble.py P         # index.html：镜头首尾相接 + 整首歌
cd P && PRODUCER_PAGE_NAVIGATION_TIMEOUT_MS=90000 npx -y hyperframes@0.8.123 check .   # 必须 0 错误
```

**8. 渲染**：**检查点 3：渲染前告诉用户预计时长。**

```bash
python3 $SKILL/scripts/tools/render.py P --name 片名
```

- 默认每 4 个镜头渲一段，无损拼接后铺上整首歌。每段都裁到精确帧数，和整体渲染逐帧一致。
- 《风吹新竹》全片 24 个镜头，整体渲染用了 36 分钟，分段渲染 7.5 到 11.4 分钟，总帧数 6178 一帧不差。
- `--chunk 0` 改为整体渲染。一个工程出多个版本（比如简体、繁体各一版）时，每版一份配置文件，用 `--config` 指定。

输出：
- 原画质版；
- 1080p 分享版；
- 720p 手机版，30 MB 以内，能直接发到手机；
- 转场对照图 `-cuts.jpg`。

看完对照图再交付。

## 硬规则

1. **歌词版式不变，画面每首歌重画。** 歌词一律用 `typo.py`；画面里的角色、道具、地点从这首歌的歌词里来，新画在 `scripts/assets/`，不搬另一首歌的画。
2. **画面里至少有一样东西直接来自那句歌词。** 抽象词找能画的替身，不用一颗心、一个地球这类通用图。
3. **歌词在唱的时候必须完整可读。** 唱完之后才可以被吹走。全片只用简体或繁体中的一种，所有字都必须在字体子集里。
4. **全片一种画法。** 墨线、平涂、抖线，不用照片、渐变光效、KTV 逐字变色、底部字幕条。
5. **画出来的动作都量化到 12 fps。** 补间一律用 `q()`。
6. **遵守 GSAP 跳帧规则。**
   - 一个元素只用一个变换原点；
   - 大位移不配 `svgOrigin`：要么补间 `transform` 属性，要么拆成两层；
   - 时间轴里不能有 `Math.random()` 和 `Date.now()`。
7. **渲染必须加 `--experimental-fast-capture=false`。** `render.py` 和 `preview.py --video` 已经加好。
8. **确认后才往下做。** 素材表和分镜确认后才画镜头，样片确认后才铺满全片，渲染前告知耗时。

## 文件

- `scripts/kit/`：
  - `typo.py`：歌词版式，每支片子都一样；
  - `draw.py`：画新素材的基础件，包括参数化的人、天气、植物、通用建筑；
  - `hd_lib.py`：色板、文字、标签、缎带等底层组件；
  - `scene.py`：镜头编排层；
  - `frame_kit.py`：字体、滤镜、JS 小工具、写出镜头文件；
  - `music.py`：拍点和歌词时间；
  - `text.py`：简繁转换和缺字检查；
  - `project.py`：找到工程，读取 `mv.json`。
- `scripts/tools/`：`new_project`、`analyze`、`lyrics`、`repeats`、`asset_sheet`、`fonts`、`build`、`preview`、`assemble`、`render`。
- `templates/`：
  - `scene_template.py`：新镜头的起点；
  - `asset_example.py`：素材文件的写法；
  - `意象表.md`：歌词转画面的表格。
- `references/`：
  - 歌词转画面
  - 歌词版式
  - 画风规范
  - 镜头配方
  - 全曲规划
  - 动效与避坑
- `examples/风吹新竹/`：镜头脚本和 `drawings/`（当时的人物、道具、新竹地方道具），只作参考，不能直接运行，也不搬进新歌。
- `assets/fonts/`：两款拉丁字体（OFL 许可）。
