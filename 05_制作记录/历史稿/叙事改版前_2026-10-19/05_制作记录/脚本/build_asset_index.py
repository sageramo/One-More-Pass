"""Index generated originals and create a browsing contact sheet, without editing originals."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import csv
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / '02_视觉资产'
DOCS = ROOT / '01_制作文档'
RECORDS = ROOT / '05_制作记录'

# File, code, role, intended shots, important stage boundary.
SPECS = [
 ('W01_workshop.png', 'W01', '工坊空间母图', '01—27按需', '固定左窗、工作台、工作垫和后侧柜的空间关系；近景可以裁去环境。'),
 ('H01_hands_master.png', 'H01', '双手与灰袖口母图', '有手的镜头', '身份基准；左手在画面左侧、右手在画面右侧，均为手背视图。'),
 ('H01_right_hand.png', 'H01', '右手独立参考', '有右手的镜头', '用于锁定右手与袖口；不能镜像后当左手使用。'),
 ('H01_left_hand.png', 'H01', '左手独立参考', '有左手的镜头', '用于锁定左手与袖口；不能镜像后当右手使用。'),
 ('H01_below_shoulders.png', 'H01', '肩以下身体与工作服', '27及身体可见处', '人物匿名，无可识别正脸；不新增传承人身份。'),
 ('G01_plum_layout.png', 'G01', '三朵金梅布局参考', '01—03、12—27', '白底RGB布局参考，不是透明贴图；板上坐标及透视以P04完成图为准。'),
 ('P01_wood_top.png', 'P01', '裸木胎俯视', '04—05', '无黑漆、无金纹；保持板形与长宽比例。'),
 ('P01_wood_oblique.png', 'P01', '裸木胎斜俯视', '04—05', '同一木胎的斜俯视几何基准。'),
 ('P02_cloth.png', 'P02', '裱布状态', '05', '可见布纹，尚未覆盖灰层。'),
 ('P02_gray_wet.png', 'P02', '湿灰胎状态', '06—07', '细膏状灰料覆盖布纹，不是黑漆或水泥喷涂。'),
 ('P02_gray_cured.png', 'P02', '已干固灰胎', '08', '干固、平整，不自动变湿，不保留粗布编织纹。'),
 ('P03_black_cured.png', 'P03', '固化无纹黑漆底', '09—11', '用作器型与无纹黑底参考；髹涂时仅局部表现本镜新上的薄湿漆。'),
 ('P04_gold_partial_branch.png', 'P04', '描金局部：梅枝', '12', '从完成图减去花朵的局部进度，只补短段线条，不自动长出花。'),
 ('P04_gold_partial_flower.png', 'P04', '描金局部：花瓣收笔', '13', '同一纹样，仅一处花瓣留有待完成的小缺口。'),
 ('P04_gold_complete.png', 'P04', '三朵金梅完成母图', '14；后续纹样基准', '后续只继承这组三朵花及枝干，不增加金边、山水或第四朵花。'),
 ('P05_coat_structure.png', 'P05', '罩漆器型与纹样结构母图', '15；后续结构基准', '只继承器型、侧边、纹样与罩层关系，不当作所有工序的反光状态。'),
 ('P05A_coat_cured.png', 'P05A', '罩层已固化、待精磨', '16—17', '无油灰；柜内等待由剪辑表达，不在一镜内变干。'),
 ('P05B_finely_sanded.png', 'P05B', '精磨后、已清理', '18', '均匀柔和的表面，无油灰，开始薄擦麻油。'),
 ('P05B_oiled.png', 'P05B', '薄擦麻油后、尚未落灰', '19', '只有极薄油膜，不是油池、厚胶或已完成镜面。'),
 ('P05C_oil_ash.png', 'P05C', '薄油与少量细砖灰操作面', '20—21、23—24', '少量粉末贴在留黑工作区；不把它直接用作干净检查面。'),
 ('C01_mid_polish_check.png', 'C01', '掌推中途、整理后的检查面', '01—03、22', '同构图检查基准，左上局部窗反射边缘稍发散；镜22复用视频素材。'),
 ('C02_finished_check.png', 'C02', '完成检查面', '25—27', '从C01派生，窗反射边缘更清楚；不靠整体变亮、换灯或清灰制造对比。'),
]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path):
    try:
        return str(Path(path).relative_to(ROOT))
    except ValueError:
        return str(path)

def main():
    logs = [json.loads(line) for line in (RECORDS / 'imagegen_生成记录.jsonl').read_text().splitlines() if line.strip()]
    selected = {d['filename']: d for d in logs if d.get('status', '').startswith('accepted')}
    expected = {x[0] for x in SPECS}
    actual = {p.name for p in ASSETS.glob('*.png')}
    assert actual == expected, (expected - actual, actual - expected)
    rows = []
    for name, code, role, shots, note in SPECS:
        path = ASSETS / name
        with Image.open(path) as im:
            im.verify()
        with Image.open(path) as im:
            width, height, mode = im.width, im.height, im.mode
        record = selected[name]
        rows.append(dict(code=code, filename=name, role=role, shots=shots, note=note,
                         path=rel(path), width=width, height=height, mode=mode, sha256=digest(path),
                         generation_id=record['id'], generation_mode='built-in imagegen',
                         prompt=record['prompt'], references=[rel(p) for p in record.get('references', [])],
                         qa='静态视觉检查通过；视频连续性尚待验证'))
    manifest = dict(project='推光', scope='22张静态参考PNG及L01文字规范；不包含视频与音频成片',
                    image_count=len(rows), source_generation_count=len(logs),
                    asset_rows=rows, lighting_rule='03_光线规范/L01_lighting.md')
    (DOCS / '资产清单.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    keys = ['code', 'filename', 'role', 'shots', 'width', 'height', 'mode', 'sha256', 'note']
    with (DOCS / '资产清单.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer=csv.DictWriter(f, fieldnames=keys, extrasaction='ignore'); writer.writeheader();writer.writerows(rows)
    md = ['# 《推光》静态资产清单与调用说明', '',
          '本轮使用内置 imagegen 生成并筛选22张独立PNG：21张规定状态/视图，加1张H01双手身份母图。L01是文字规范，另存Markdown与TXT，不虚构成第23张图片。所有图片均已检查可读性、尺寸和SHA256；画面经过静态视觉核对，尚未验证视频生成后的连续性。', '',
          '[打开资产总览](资产总览.jpg) · [CSV清单](资产清单.csv) · [JSON清单与完整提示词](资产清单.json) · [最终提示词集](../05_制作记录/imagegen_最终提示词集.md)', '',
          '| 编号 | 文件 | 内容 | 对应镜头 | 像素 |', '|---|---|---|---|---|']
    for row in rows:
        md.append(f"| {row['code']} | [{row['filename']}](../{row['path']}) | {row['role']} | {row['shots']} | {row['width']}×{row['height']} |")
    md += ['', '## 使用顺序', '',
           '先选择本镜的P/C工序状态，再按需要附H01人物视图和W01空间图，并展开L01规则；不要一次上传所有阶段。P、G、H、W、L是类别，实际参考文件必须附图，模型不会仅凭编号理解。本轮将每个工序保存为独立图片，材质状态的切换仍发生在剪辑点。', '',
           'G01是白底RGB纹样定位参考，不是透明叠加层；它用于传递枝干与三朵花的设计，板上比例、坐标和透视以P04_gold_complete.png为正式基准。后续P05、P05A/B/C、C01/C02已包含该纹样，无需再叠加G01。早期透明候选出现光晕，已隔离在候选与退回目录。', '',
           'P05只锁定罩漆后的器型、金梅及薄红侧边，表面状态分别调用P05A、P05B、薄油后P05B_oiled与P05C。P05C含少量操作用灰，C01/C02则是经必要整理后的检查面；两者通过剪辑衔接，不能让灰粉在连续画面里自动消失。P05A与P05B的材质差别克制，具体水砂、擦油动作由各镜提示词补足。', '',
           'C01/C02经独立视觉复核：器型、纹样、桌垫和窗格未见明显漂移，C02窗格边缘更清楚并伴随局部对比变化，整体曝光基本一致。可用于匹配剪辑的静态参照，不作为真实工艺实验或专业质量验收结论。', '',
           '图片是生成视频的原始参考资产，实际尺寸如表；多数为1536×1024，空间及人物中景约16:9。没有将它们拉伸或冒称为1920×1080成片帧。后续在视频生成与剪辑阶段按目标画幅重构构图，保留板边和手部安全边距。镜28—29按脚本用后期文字排版，无需图像模型生成汉字。', '',
           '## 各状态的边界', '']
    md += [f"**{row['filename']}**：{row['note']}\n" for row in rows]
    (DOCS / '资产清单与调用说明.md').write_text('\n'.join(md)+'\n')
    prompt_lines = ['# 《推光》imagegen最终提示词集', '',
                    '模式：内置imagegen。以下按最终入选文件列出实际提示词与输入参考；完整候选及退回过程见同目录imagegen_生成记录.jsonl。图片均为AI生成的创作参考，不是工坊实拍。', '']
    for row in rows:
        prompt_lines += [f"## {row['filename']}", '', f"编号：{row['code']}；内容：{row['role']}；实际尺寸：{row['width']}×{row['height']}。", '',
                         '输入参考：'+('；'.join(row['references']) if row['references'] else '无，文字生成。'), '',
                         '```text', row['prompt'], '```', '']
    (RECORDS / 'imagegen_最终提示词集.md').write_text('\n'.join(prompt_lines)+'\n')

    # This contact sheet is a browsing/QA artifact, not a synthesized film asset.
    cols, cw, ch, pad = 4, 400, 316, 20
    nrows = (len(rows)+cols-1)//cols
    sheet=Image.new('RGB', (cols*cw+pad*2, nrows*ch+100+pad), '#eeeae2')
    draw=ImageDraw.Draw(sheet)
    font='/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
    title=ImageFont.truetype(font, 30); small=ImageFont.truetype(font, 19); body=ImageFont.truetype(font, 17)
    draw.text((pad, 20), '《推光》静态资产总览 · 22 PNG', font=title, fill='#222831')
    draw.text((pad, 62), '浏览索引；原始图片保持独立文件。L01为文字规范。', font=small, fill='#555555')
    for i,row in enumerate(rows):
        x=pad+(i%cols)*cw; y=100+(i//cols)*ch
        box=(cw-16, 240)
        with Image.open(ASSETS/row['filename']) as im:
            thumb=ImageOps.contain(im.convert('RGB'), box)
        draw.rectangle((x,y,x+box[0],y+box[1]),fill='#d9d5cf')
        sheet.paste(thumb,(x+(box[0]-thumb.width)//2,y+(box[1]-thumb.height)//2))
        draw.text((x,y+248),row['filename'],font=body,fill='#222831')
        draw.text((x,y+274),row['role'],font=small,fill='#66502f')
    sheet.save(DOCS/'资产总览.jpg',quality=92)
    print(json.dumps({'images':len(rows),'generation_records':len(logs),'sheet_size':sheet.size,'files_verified':True},ensure_ascii=False))

if __name__ == '__main__':
    main()
