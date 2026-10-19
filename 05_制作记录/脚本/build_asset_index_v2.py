"""Index generated originals; create browsing sheets without editing film assets."""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import json,csv,hashlib
ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/'01_制作文档';REC=ROOT/'05_制作记录';ASSET=ROOT/'02_视觉资产'
FONT='/System/Library/Fonts/Supplemental/Arial Unicode.ttf'

def sheet(rows,path,title,cols=4,cw=400,ch=316):
 pad=20;im=Image.new('RGB',(cols*cw+2*pad,100+((len(rows)+cols-1)//cols)*ch+pad),'#eeeae2');d=ImageDraw.Draw(im)
 d.text((pad,18),title,font=ImageFont.truetype(FONT,29),fill='#222831')
 d.text((pad,61),'静态参考索引；原图保持独立文件，L01为文字规范。',font=ImageFont.truetype(FONT,18),fill='#555555')
 for i,r in enumerate(rows):
  x=pad+(i%cols)*cw;y=100+(i//cols)*ch;box=(cw-16,240)
  with Image.open(ASSET/r['filename']) as src:t=ImageOps.contain(src.convert('RGB'),box)
  d.rectangle((x,y,x+box[0],y+box[1]),fill='#d9d5cf');im.paste(t,(x+(box[0]-t.width)//2,y+(box[1]-t.height)//2))
  d.text((x,y+248),r['filename'],font=ImageFont.truetype(FONT,17),fill='#222831')
  d.text((x,y+274),r['role'],font=ImageFont.truetype(FONT,18),fill='#66502f')
 im.save(path,quality=92)

def main():
 source=json.loads((DOC/'推光_叙事改版_v2.json').read_text())
 specs=source['existing_assets']+source['new_assets']
 logs=[json.loads(l) for l in (REC/'imagegen_生成记录.jsonl').read_text().splitlines() if l.strip()]
 selected={d['filename']:d for d in logs if d.get('status','').startswith('accepted')}
 assert {s['file'] for s in specs}=={p.name for p in ASSET.glob('*.png')}
 rows=[]
 for a in specs:
  p=ASSET/a['file']
  with Image.open(p) as im:im.verify()
  with Image.open(p) as im:w,h,mode=im.width,im.height,im.mode
  r=selected[a['file']];refs=[str(Path(x).relative_to(ROOT)) for x in r.get('references',[])]
  assert all((ROOT/x).exists() for x in refs)
  rows.append(dict(code=a['code'],filename=a['file'],role=a['label'],shots=a['use'],note=a['note'],path=str(p.relative_to(ROOT)),width=w,height=h,mode=mode,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),generation_id=r['id'],generation_mode='built-in imagegen',prompt=r['prompt'],references=refs,qa='静态检查；视频连续性及手机可辨性尚待样片验证'))
 manifest=dict(project='推光',version=source['version'],scope='29张静态PNG及L01文字规范；视频和音频尚未生成',image_count=len(rows),source_generation_count=len(logs),asset_rows=rows,lighting_rule='03_光线规范/L01_lighting.md')
 (DOC/'资产清单.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 with (DOC/'资产清单.csv').open('w',encoding='utf-8-sig',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=['code','filename','role','shots','width','height','mode','sha256','note'],extrasaction='ignore');writer.writeheader();writer.writerows(rows)
 md=['# 《推光》资产清单与调用说明 · v2','','原22图继续保留，本轮内置imagegen新增7图，合计29张PNG。L01是另存的文字光线规范。文件已校验存在、可读性、实际尺寸、来源参考与SHA256；静态资产不代表视频已完成。','','[全部资产总览](资产总览.jpg) · [本轮新增7图](新增资产总览_v2.jpg) · [CSV](资产清单.csv) · [JSON与提示词](资产清单.json) · [实际提示词集](../05_制作记录/imagegen_最终提示词集.md)','','| 编号 | 文件 | 内容 | 新版用途 | 像素 |','|---|---|---|---|---|']
 for r in rows:md.append(f"| {r['code']} | [{r['filename']}](../{r['path']}) | {r['role']} | {r['shots']} | {r['width']}×{r['height']} |")
 md+=['','## 调用规则','','当前执行时间线是32镜、180秒、三组插叙共40秒。资产库允许保留备用图，正片无需逐张展示。具体调用以新版分镜及上表为准，旧版29镜编号不再执行。','','每次只输入本镜视觉规则、对应工序/动作图和一个主要动作。K01已含掌推双手；K02是开场将棉团放回小碟而停住；K04是完成推光后仍持棉团的姿势；结尾仅用K04到K03生成归置动作，板面材质全程不变。不能用K02到K03连续生成，否则会让光泽在放棉团时变化。','','棉团操作期间临放于小碟下方工作垫右下留白处，取放可由切点省略；一直未完成的是放回小碟，而不是始终悬空拿着。继续处理时保留已部分推光的当下表面，不能退回P05B刚精磨初态。','','正式细节检查统一使用R01/R02/R03；红边及局部金纹为对焦参照，窗影从发散到局部改善再到较均匀清楚。三图保持同样整洁、同构图与曝光；K01/P05C含操作油灰，不加入这组比较。C01/C02保留作全板结构及材质来源。','','R系列的金梅自然裁切，不代表重新设计花朵。G01仍为白底RGB纹样参考，不是透明叠加层；以P04完成图锁定板上坐标。','','图片实际尺寸见表，未拉伸为成片帧。R系列3:2在16:9中统一等比置入或统一裁切；三次检查不分别改取景。镜31-32的文字后期排版，不由图像模型生成汉字。','','## 状态边界','']
 md += [f"**{r['filename']}**：{r['note']}\n" for r in rows]
 (DOC/'资产清单与调用说明.md').write_text('\n'.join(md)+'\n')
 prompts=['# 《推光》imagegen最终提示词集 · v2','','内置imagegen；29张入选图的实际提示词和引用图如下。全部35次生成及退回过程保留在imagegen_生成记录.jsonl；源图为AI创作参考，不是工坊实拍。','']
 for r in rows:
  prompts += [f"## {r['filename']}",'',f"编号：{r['code']}；{r['role']}；实际尺寸：{r['width']}×{r['height']}。",'','输入参考：'+('；'.join(r['references']) or '无，文字生成。'),'','```text',r['prompt'],'```','']
 (REC/'imagegen_最终提示词集.md').write_text('\n'.join(prompts)+'\n')
 newnames={a['file'] for a in source['new_assets']}
 sheet(rows,DOC/'资产总览.jpg','《推光》v2 · 全部29张静态资产')
 sheet([r for r in rows if r['filename'] in newnames],DOC/'新增资产总览_v2.jpg','《推光》v2 · 新增7张叙事资产',cols=2,cw=540)
 print(json.dumps({'images':len(rows),'new_images':len(newnames),'generation_records':len(logs),'readable':True},ensure_ascii=False))

if __name__=='__main__':main()
