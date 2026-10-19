from pathlib import Path
import re, html, unicodedata, json
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from pypdf import PdfReader

# Resolve all inputs and generated outputs inside this project folder.
BASE=Path(__file__).resolve().parents[2]
ROOT=BASE/'05_制作记录/构建中间文件'
OUT=BASE/'01_制作文档'
ROOT.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
SOURCE=OUT/'02_推光_180秒AI分镜提示词.md'
source=SOURCE.read_text()

# A category is a rule family; a numbered asset is a concrete image state or text rule.
states={1:'C01检查状态',2:'C01检查状态',3:'C01检查状态',4:'P01木胎',5:'P02裱布状态',
6:'P02灰胎',7:'P02灰胎',8:'P02已干固灰胎',9:'P03漆层',10:'P03漆层',11:'P03后续漆层',
12:'P04纹样局部',13:'P04纹样局部',14:'P04纹样完成',15:'P04至P05罩漆过程',
16:'P05A罩层静置',17:'P05A待精磨',18:'P05B精磨后',19:'镜18薄擦麻油后的状态，形成P05C',
20:'P05C掌推中',21:'P05C掌推中',23:'P05C掌推中',24:'P05C掌推中',25:'C02完成检查状态',
26:'C02完成检查状态',27:'C02完成状态'}
hands={2,3,4,5,6,8,9,11,12,13,15,17,18,19,20,21,23,24,25,26,27}

def refs(n):
    if n==22:return '资产调用：直接复用镜02/03；P/G/H/W/L均沿用入选素材，不重新生成。'
    if n in (28,29):return '资产调用：纯后期文字，P/G/H/W/L均不调用实体资产。'
    g='无纹样，不调用G01' if 4<=n<=11 else ('G01定位，按P04局部进度' if n in (12,13) else 'G01，继承状态图内的纹样')
    h='H01' if n in hands else '无人物'
    l='L01，柜内弱环境光' if n in (7,10,16) else 'L01'
    return f'资产调用：P={states[n]}；G={g}；H={h}；W=继承W01；L={l}。'

lines=[]
for line in source.splitlines():
    m=re.match(r'^\| (\d{2}) / ',line)
    if m:
        n=int(m[1]);cells=[c.strip() for c in line.strip().strip('|').split('|')]
        assert len(cells)==3
        if not cells[1].startswith('资产调用：'):
            cells[1]=refs(n)+' '+cells[1]
        line='| '+' | '.join(cells)+' |'
    lines.append(line)
source='\n'.join(lines)+'\n'
# Keep the authoritative Markdown unchanged while rendering PDFs.

sections={m[1]:m[2].strip() for m in re.finditer(r'^## ([^\n]+)\n(.*?)(?=^## |\Z)',source,re.M|re.S)}
metadata=source.split('\n\n',2)[1]
assets='# 《推光》第一部分：资产\n\n'+metadata+'\n\n'
assets+='修订说明：补齐P/G/H/W/L与具体编号的对应关系；G01是金梅布局模板，L01是文字光线规范，图像参考不等于已经生成。逐镜调用见第二部分。\n\n'
for title in ['使用方式','总创作要求：可直接复制','资产与画面一致性','先生成的参考资产']:
    assets+=f'## {title}\n\n{sections[title]}\n\n'
assets+='## 生成时的通用约束\n\n'+sections['每镜通用约束']+'\n'

mapping=sections['资产与画面一致性'].split('**P：漆板。**',1)[0].strip()
shots='# 《推光》第二部分：分镜\n\n'
shots+='资产编号对应关系修订版。完整29个时间段，成片180秒，包含12秒片尾；编号沿用第一部分资产。\n\n'
shots+='## 使用方式与编号对应\n\n'+sections['使用方式']+'\n\n'+mapping+'\n\n'
shots+='本片为基于公开资料的纯AI工艺情境演绎，保持同一人、同一漆板与“检查、回溯、继续、再次检查、停手”的结构；先完成资产锁定，再逐镜生成。\n\n'
for title in ['180秒分镜表','旁白与声音','每镜通用约束','关键镜头的失败回退','后期与交付']:
    shots+=f'## {title}\n\n{sections[title]}\n\n'
assert all(v in assets+'\n'+shots for v in sections.values())

pdfmetrics.registerFont(TTFont('CN','/System/Library/Fonts/STHeiti Light.ttc',subfontIndex=0))
pdfmetrics.registerFont(TTFont('CNBold','/System/Library/Fonts/STHeiti Medium.ttc',subfontIndex=0))
pdfmetrics.registerFontFamily('CN',normal='CN',bold='CNBold',italic='CN',boldItalic='CNBold')
INK=colors.HexColor('#20252B');MUTED=colors.HexColor('#657079');ACCENT=colors.HexColor('#95723B');RULE=colors.HexColor('#D5D9DC')
def inline(s):
    s=html.escape(s.replace('\u2011','-').replace('\u2013','-').replace('\u2014','-'))
    return re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',s)

def build(md,path,label,size):
    width,height=size;margin=39 if width<700 else 34
    doc=SimpleDocTemplate(str(path),pagesize=size,leftMargin=margin,rightMargin=margin,topMargin=55,bottomMargin=43,title=f'推光 - {label} - 编号对应修订版',author='')
    body=ParagraphStyle('Body',fontName='CN',fontSize=10.1,leading=15.4,textColor=INK,wordWrap='CJK',spaceAfter=8)
    h1=ParagraphStyle('H1',parent=body,fontName='CNBold',fontSize=20,leading=27,spaceAfter=14,keepWithNext=True)
    h2=ParagraphStyle('H2',parent=body,fontName='CNBold',fontSize=12.5,leading=18,spaceBefore=11,spaceAfter=7,keepWithNext=True,textColor=ACCENT)
    quote=ParagraphStyle('Quote',parent=body,leftIndent=12,rightIndent=8,borderColor=RULE,borderWidth=.5,borderPadding=6,spaceBefore=3,spaceAfter=8)
    cell=ParagraphStyle('Cell',parent=body,fontSize=9.25,leading=13.2,spaceAfter=0,spaceBefore=0)
    th=ParagraphStyle('TH',parent=cell,fontName='CNBold',textColor=colors.white)
    def page(canvas,doc):
        canvas.saveState();canvas.setFont('CN',8);canvas.setFillColor(MUTED)
        canvas.drawString(margin,height-28,f'推光 / {label} / 编号对应修订版')
        canvas.setStrokeColor(RULE);canvas.setLineWidth(.5);canvas.line(margin,height-36,width-margin,height-36)
        canvas.drawString(margin,24,'180秒纯AI工艺情境短片');canvas.drawRightString(width-margin,24,str(doc.page));canvas.restoreState()
    flow=[];lines=md.splitlines();i=0
    while i<len(lines):
        ln=lines[i].strip()
        if not ln:i+=1;continue
        if ln.startswith('# '):flow.append(Paragraph(inline(ln[2:]),h1));i+=1
        elif ln.startswith('## '):
            if (label=='第一部分：资产' and ln[3:] in ['资产与画面一致性','先生成的参考资产']) or (label=='第二部分：分镜' and ln[3:]=='180秒分镜表'):
                flow.append(PageBreak())
            flow.append(Paragraph(inline(ln[3:]),h2));i+=1
        elif ln.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                row=[c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?',c) for c in row):rows.append(row)
                i+=1
            assert all(len(r)==3 for r in rows)
            is_shot='镜号' in rows[0][0];avail=width-2*margin
            is_map=rows[0][0]=='类别'
            ratios=[.13,.53,.34] if is_shot else ([.18,.34,.48] if is_map else [.12,.48,.40])
            data=[]
            for ri,row in enumerate(rows):
                cells=[]
                for ci,text in enumerate(row):
                    markup=inline(text)
                    if is_shot and ri>0 and ci==0:
                        m=re.fullmatch(r'(\d{2}) / ([\d:-]+) / (\d+秒)',text);assert m
                        markup=f'<b>镜{m[1]}</b><br/>{m[2]}<br/>{m[3]}'
                    if is_shot and ri>0 and ci==1:
                        # Put the explicit asset call on its own lines, then the original action.
                        a,sep,b=text.partition('。 ')
                        if sep:markup=f'<font color="#73572F">{inline(a+"。")}</font><br/>'+inline(b)
                    cells.append(Paragraph(markup,th if ri==0 else cell))
                data.append(cells)
            tab=Table(data,colWidths=[avail*r for r in ratios],repeatRows=1,hAlign='LEFT',splitByRow=1)
            tab.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),1,ACCENT),('LINEBELOW',(0,1),(-1,-1),.4,RULE),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F5F6F7')])]))
            flow.extend([tab,Spacer(1,10)])
        elif ln.startswith('>'):
            if ln[1:].strip():flow.append(Paragraph(inline(ln[1:].strip()),quote))
            i+=1
        else:
            p=[ln];i+=1
            while i<len(lines) and lines[i].strip() and not lines[i].lstrip().startswith(('#','|','>')):p.append(lines[i].strip());i+=1
            flow.append(Paragraph(inline(' '.join(p)),body))
    doc.build(flow,onFirstPage=page,onLaterPages=page)

for md,name,label,size in [(assets,'推光_第一部分_资产','第一部分：资产',A4),(shots,'推光_第二部分_分镜','第二部分：分镜',landscape(A4))]:
    out=OUT/f'{name}.pdf'
    (ROOT/f'{name}.md').write_text(md)
    build(md,out,label,size)
    r=PdfReader(out)
    print(out,len(r.pages),'pages',out.stat().st_size,'bytes')

# Keep exact timeline and the old actions; only reference declarations and indexing changed.
timeline=re.findall(r'^\| (\d{2}) / (\d{2}):(\d{2})-(\d{2}):(\d{2}) / (\d+)秒',source,re.M)
prev=0
for n,am,ass,bm,bs,d in timeline:
    a=int(am)*60+int(ass);b=int(bm)*60+int(bs)
    assert a==prev and b-a==int(d),(n,a,b,d,prev)
    prev=b
assert len(timeline)==29 and prev==180
for ln in source.splitlines():
    m=re.match(r'^\| (\d{2}) / ',ln)
    if not m:continue
    n=int(m[1]);assert '资产调用：' in ln
    if 4<=n<=11:assert 'G=无纹样，不调用G01' in ln
    if n in [12,13]:assert 'G=G01定位，按P04局部进度' in ln
    if n==22:assert '不重新生成' in ln
    if n in [28,29]:assert '纯后期文字' in ln
print('29条资产调用、类别对应、纹样阶段与180秒时码校验通过。')
