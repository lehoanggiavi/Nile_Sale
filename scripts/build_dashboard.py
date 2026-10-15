"""Phase 5B: build the three existing native report pages."""
import json
import hashlib
import sys
from pathlib import Path

SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json"
PAGE = Path("pbi/NileSales.Report/definition/pages/fba0ca66315c4cccbdf0")
VDIR = PAGE / "visuals"
MEAS = "Measure"
LIT = lambda v: {"expr": {"Literal": {"Value": v}}}
HEX = lambda v: {"solid": {"color": {"expr": {"Literal": {"Value": v}}}}}


def col(table, prop):
    return {"field": {"Column": {"Expression": {"SourceRef": {"Entity": table}},
                                 "Property": prop}},
            "queryRef": f"{table}.{prop}", "nativeQueryRef": prop}


def meas(prop):
    return {"field": {"Measure": {"Expression": {"SourceRef": {"Entity": MEAS}},
                                  "Property": prop}},
            "queryRef": f"{MEAS}.{prop}", "nativeQueryRef": prop}


def vco(title=None):
    o = {"background": [{"properties": {
        "show": LIT("true"), "color": HEX("'#FFFFFF'"),
        "transparency": LIT("0D")}}],
        "border": [{"properties": {
            "show": LIT("true"), "color": HEX("'#E6E8F0'"),
            "radius": LIT("8D")}}],
        "padding": [{"properties": {
            "top": LIT("5D"), "bottom": LIT("5D"),
            "left": LIT("5D"), "right": LIT("5D")}}]}
    if title:
        o["title"] = [{"properties": {
            "show": LIT("true"),
            "text": LIT(f"'{title}'"),
            "fontSize": LIT("12D"),
            "fontColor": HEX("'#1F1F1F'")}}]
    return o


def card(name, measure, label, x):
    return {"$schema": SCHEMA, "name": name,
            "position": {"x": x, "y": 156, "z": 1000, "height": 110,
                         "width": 270, "tabOrder": 1000},
            "visual": {
                "visualType": "cardVisual",
                "query": {"queryState": {"Data": {"projections": [meas(measure)]}}},
                "objects": {
                    "value": [{"properties": {
                        "fontSize": LIT("20D"),
                        "fontColor": HEX("'#1F1F1F'")},
                        "selector": {"id": "default"}}],
                    "label": [{"properties": {
                        "show": LIT("true"),
                        "text": LIT(f"'{label}'"),
                        "fontSize": LIT("12D")},
                        "selector": {"id": "default"}}],
                    "outline": [{"properties": {"show": LIT("false")},
                                 "selector": {"id": "default"}}],
                    "padding": [{"properties": {"paddingUniform": LIT("8L")},
                                 "selector": {"id": "default"}}],
                    "layout": [{"properties": {"paddingUniform": LIT("8L")},
                                "selector": {"id": "default"}}]},
                "visualContainerObjects": vco()}}


def chart(name, measure, title, x, color):
    return {"$schema": SCHEMA, "name": name,
            "position": {"x": x, "y": 274, "z": 1000, "height": 200,
                         "width": 560, "tabOrder": 1000},
            "visual": {
                "visualType": "clusteredColumnChart",
                "query": {"queryState": {
                    "Category": {"projections": [dict(col("DimDate", "YearMonth"),
                                                      active=True)]},
                    "Y": {"projections": [meas(measure)]}}},
                "objects": {
                    "dataPoint": [{"properties": {
                        "defaultColor": HEX(f"'{color}'")}}],
                    "labels": [{"properties": {"show": LIT("true")}}]},
                "visualContainerObjects": vco(title)}}


def table(name):
    return {"$schema": SCHEMA, "name": name,
            "position": {"x": 76, "y": 482, "z": 1000, "height": 222,
                         "width": 1128, "tabOrder": 1000},
            "visual": {
                "visualType": "tableEx",
                "query": {"queryState": {"Values": {"projections": [
                    col("DimDate", "YearMonth"),
                    meas("Giá trị dòng nguồn"),
                    meas("Giá trị nguồn tháng trước"),
                    meas("Thay đổi giá trị nguồn so tháng trước (%)")]}}},
                "objects": {"columnHeaders": [{"properties": {
                    "columnAdjustment": LIT("'growToFit'"),
                    "autoSizeColumnWidth": LIT("true")}}]},
                "visualContainerObjects": vco("Tháng | Giá trị | Tháng trước | %")}}


def slicer(name, table, prop, header, x, w):
    return {"$schema": SCHEMA, "name": name,
            "position": {"x": x, "y": 68, "z": 1000, "height": 80,
                         "width": w, "tabOrder": 1000},
            "visual": {
                "visualType": "slicer",
                "query": {"queryState": {"Values": {"projections": [
                    col(table, prop)]}}},
                "objects": {
                    "data": [{"properties": {
                        "mode": LIT("'Dropdown'")}}],
                    "header": [{"properties": {
                        "show": LIT("true"),
                        "text": LIT(f"'{header}'")}}]},
                "visualContainerObjects": {"padding": [{"properties": {
                    "top": LIT("8D"), "bottom": LIT("8D"),
                    "left": LIT("8D"), "right": LIT("8D")}}]}}}


def textbox(name, text, x, y, w, h, size):
    run = {"value": text,
           "textStyle": {"fontFamily": "Segoe UI Semibold",
                         "fontSize": f"{size}px", "color": "#1F1F1F"}}
    para = {"textRuns": [run], "horizontalTextAlignment": "left"}
    return {"$schema": SCHEMA, "name": name,
            "position": {"x": x, "y": y, "z": 1000, "height": h,
                         "width": w, "tabOrder": 1000},
            "visual": {
                "visualType": "textbox",
                "objects": {"general": [{"properties": {
                    "paragraphs": [para]}}]},
                "visualContainerObjects": {
                    "background": [{"properties": {"show": LIT("false")}}],
                    "border": [{"properties": {"show": LIT("false")}}],
                    "padding": [{"properties": {
                        "top": LIT("0D"), "bottom": LIT("0D"),
                        "left": LIT("0D"), "right": LIT("0D")}}]}}}


def nav(name):
    return {"$schema": SCHEMA, "name": name,
            "position": {"x": 0, "y": 0, "z": 1000, "height": 720,
                         "width": 64, "tabOrder": 1000},
            "visual": {"visualType": "pageNavigator"}}



# Stable IDs reuse the first page. Running again updates the same visual files.
OLD = {'rail':'cb9582687a4ff4d2377c','title':'24e296d33e4205fcb587','scope':'3a4add3af4b5372e32d6',
 'month':'f137d6d7bc7b064c4245','category':'e6752e27d773b6426775','place':'bc1f0169c07fc9a3ec85',
 'value':'ccd05c1636bb89c1ee8a','qty':'6abe32e9653c84d9d7b6','rows':'754affc5a46e543cdf12',
 'codes':'5c9c74bd1b51537e2344','trend':'fa8c06e4129f7fc8a5a5','qtychart':'9dc1cb120fcdff8a9972',
 'monthtable':'ea79fd31f78f85b53ac4'}
PAGES=['fba0ca66315c4cccbdf0','fb26ae9c412e83475001','fb26ae9c412e83475002']
ROOT=Path('pbi/NileSales.Report/definition')


def prop(**values):
    return [{'properties': {k: HEX("'"+v+"'") if isinstance(v,str) and v.startswith('#')
       else LIT('true' if v is True else 'false' if v is False else str(v)+'D' if isinstance(v,(int,float)) else "'"+v+"'")
       for k,v in values.items()}}]


def button(label, action=None, target=None, selected=False, dark=False):
    vc={'background':prop(show=True,color='#111111' if dark else '#FFFFFF',transparency=0),
        'border':prop(show=False),
        'title':prop(show=bool(label),text=label,fontSize=10,bold=True,fontColor='#FFFFFF' if dark else '#865EFF',alignment='center')}
    if action: vc['visualLink']=prop(show=True,type=action,**({'navigationSection':target} if target else {}))
    return {'visual':{'visualType':'basicShape','objects':{'fill':prop(show=True,transparency=100),'line':prop(transparency=100,weight=0)},'visualContainerObjects':vc}}


def refine_overview_chart(v, role):
    """Three chart variants; also used to update the saved report without rebuilding it."""
    visual = v['visual']
    qs = visual['query']['queryState']
    objects = visual['objects']
    if role == 'trend':
        visual['visualType'] = 'lineClusteredColumnComboChart'
        qs['Y']['projections'] = [dict(meas('Giá trị dòng nguồn'), displayName='Giá trị nguồn')]
        qs['Y2'] = {'projections': [dict(meas('Thay đổi giá trị nguồn so tháng trước (%)'), displayName='Thay đổi (%)')]}
        qs['Tooltips'] = {'projections': [meas('Giá trị nguồn tháng trước')]}
        objects['valueAxis'] = prop(show=True, start=0, sharedAxis=False, secShow=True, secStart=0,
            fontSize=9, secFontSize=9, labelDisplayUnits=1000000, labelPrecision=1,
            secLabelDisplayUnits=1, secLabelPrecision=0, showAxisTitle=False, secShowAxisTitle=False,
            gridlineColor='#ECEEF4', gridlineTransparency=35)
        objects['lineStyles'] = prop(strokeWidth=3, showMarker=True, markerSize=5)
        objects['dataPoint'] = [dict(prop(fill='#865EFF')[0], selector={'metadata': qs['Y']['projections'][0]['queryRef']}),
            dict(prop(fill='#6B007B')[0], selector={'metadata': qs['Y2']['projections'][0]['queryRef']})]
        objects['legend'] = prop(show=True, position='Bottom', fontSize=9)
        objects['labels'] = prop(show=False)
        caption = 'GIÁ TRỊ NGUỒN (triệu) · THAY ĐỔI THÁNG (%)'
    elif role in {'categorybar', 'placebar'}:
        visual['visualType'] = 'donutChart' if role == 'categorybar' else 'treemap'
        objects.pop('categoryAxis', None)
        objects.pop('valueAxis', None)
        objects.pop('dataPoint', None)
        if role == 'categorybar':
            objects['legend'] = prop(show=True, showTitle=False, position='Right', fontSize=9)
            objects['labels'] = prop(show=True, labelStyle='Percent of total', position='outside',
                fontSize=9, percentageLabelPrecision=1, color='#202124', background='off')
            caption = 'CƠ CẤU GIÁ TRỊ · 5 NHÓM SẢN PHẨM'
        else:
            qs['Group'] = qs.pop('Category')
            qs['Values'] = qs.pop('Y')
            objects['legend'] = prop(show=False)
            objects['categoryLabels'] = prop(show=True, fontSize=9, color='#FFFFFF')
            objects['labels'] = prop(show=False)
            caption = 'CƠ CẤU NƠI NHẬN · DIỆN TÍCH = GIÁ TRỊ'
    else:
        return v
    visual['visualContainerObjects']['title'][0]['properties']['text'] = LIT("'" + caption + "'")
    return v


def scatter(t, c, x_measure, y_measure, size_measure, caption, x_title, y_title):
    v = {'visual': {'visualType': 'scatterChart',
        'query': {'queryState': {
            'Category': {'projections': [dict(col(t, c), active=True)]},
            'X': {'projections': [meas(x_measure)]}, 'Y': {'projections': [meas(y_measure)]},
            'Size': {'projections': [meas(size_measure)]}}},
        'objects': {'dataPoint': prop(defaultColor='#865EFF'),
            'categoryAxis': prop(fontSize=9, showAxisTitle=True, titleText=x_title, titleFontSize=9, start=0),
            'valueAxis': prop(fontSize=9, showAxisTitle=True, titleText=y_title, titleFontSize=9, start=0),
            'bubbles': prop(bubbleSize=-10, preventOverflow=True),
            'categoryLabels': prop(show=False), 'legend': prop(show=False)},
        'visualContainerObjects': vco(caption)}}
    v['visual']['query']['queryState']['Series'] = {'projections': [dict(col('DimProduct', 'Category'), active=True)]}
    v['visual']['objects'].pop('dataPoint')
    v['visual']['objects']['legend'] = prop(show=True, showTitle=False, position='Right', fontSize=9)
    return v


def build(index):
    items=[]
    def identity(role):
        return (OLD.get(role) if index==0 else None) or hashlib.sha256(f'nile:{index}:{role}'.encode()).hexdigest()[:20]
    def put(role,item,box):
        x,y,w,h=box
        assert x>=16 and y>=16 and w>0 and h>0 and x+w<=1264 and y+h<=704
        item.update({'$schema':SCHEMA,'name':identity(role),'position':{'x':x,'y':y,'width':w,'height':h,'z':0 if role=='rail' else 1000,'tabOrder':len(items)}})
        items.append(item);return item
    def label(role,value,box,size=12,color='#FFFFFF'):
        v=textbox('',value,0,0,0,0,size)
        v['visual']['objects']['general'][0]['properties']['paragraphs'][0]['textRuns'][0]['textStyle']['color']=color
        return put(role,v,box)
    def select(role,t,c,caption,box,sync=False):
        v=slicer('',t,c,caption,0,0)
        v['visual']['objects']['header']=prop(show=True,text=caption,textSize=9,fontColor='#606472')
        v['visual']['objects']['items']=prop(textSize=10,fontColor='#202124')
        v['visual']['visualContainerObjects']=vco()
        v['visual']['visualContainerObjects']['padding']=prop(top=0,bottom=0,left=8,right=8)
        if sync:v['visual']['syncGroup']={'groupName':'nile_'+role,'fieldChanges':True,'filterChanges':True}
        return put(role,v,box)
    def number(role,m,caption,box,precision=0,fmt='#,0'):
        v=card('',m,caption,0)
        v['visual']['objects']['value']=prop(show=True,fontSize=27,bold=True,fontColor='#202124',horizontalAlignment='left',labelDisplayUnits=1,labelPrecision=precision,customFormatString=fmt)
        v['visual']['objects']['value'][0]['selector']={'id':'default'}
        v['visual']['objects']['label'][0]['properties']['fontSize']=LIT('11D')
        return put(role,v,box)
    def plot(role,t,c,measures,caption,box,horizontal=False,tooltip=None):
        v=chart('',measures[0],caption,0,'#865EFF')
        v['visual']['visualType']='clusteredBarChart' if horizontal else 'clusteredColumnChart'
        qs=v['visual']['query']['queryState']
        qs['Category']['projections']=[dict(col(t,c),active=True)]
        qs['Y']['projections']=[meas(m) for m in measures]
        if len(measures)>1:
            for pr,name in zip(qs['Y']['projections'],['Giá trị','Kỳ trước']):pr['displayName']=name
            v['visual']['objects'].pop('dataPoint',None)
            v['visual']['objects']['legend']=prop(show=True,position='Bottom',fontSize=9)
        else:v['visual']['objects']['dataPoint']=prop(defaultColor='#865EFF')
        v['visual']['objects']['categoryAxis']=prop(fontSize=9,showAxisTitle=False,preferredCategoryWidth=22 if horizontal else 38)
        v['visual']['objects']['valueAxis']=prop(fontSize=9,showAxisTitle=False,gridlineColor='#ECEEF4',gridlineTransparency=35)
        v['visual']['objects']['labels']=prop(show=True,fontSize=9,labelPrecision=1,color='#33343B')
        if len(measures)>1:v['visual']['objects']['labels']=prop(show=False)
        if tooltip:qs['Tooltips']={'projections':[meas(tooltip)]}
        v['visual']['query']['sortDefinition']={'sort':[{'field':meas(measures[0])['field'] if horizontal else col(t,c)['field'],'direction':'Descending' if horizontal else 'Ascending'}],'isDefaultSort':False}
        if index == 0:
            refine_overview_chart(v, role)
        return put(role,v,box)
    def grid(role,fields,aliases,caption,box,widths):
        v=table('');v['visual']['visualContainerObjects']=vco(caption);prs=[]
        for (t,c),name in zip(fields,aliases):
            f=meas(c) if t=='Measure' else col(t,c);f['displayName']=name;prs.append(f)
        v['visual']['query']['queryState']['Values']['projections']=prs
        v['visual']['objects']={'columnHeaders':prop(fontSize=9,bold=True,fontColor='#202124',backColor='#ECE6FF',autoSizeColumnWidth=False,wordWrap=False),
            'values':prop(fontSize=9,wordWrap=False,fontColor='#202124',backColorPrimary='#FFFFFF',backColorSecondary='#F8F7FD'),
            'grid':prop(rowPadding=0,gridHorizontal=False,gridVertical=False),'total':prop(fontSize=9,bold=True,fontColor='#202124'),
            'columnWidth':[{'properties':{'value':LIT(str(w)+'D')},'selector':{'metadata':pr['queryRef']}} for pr,w in zip(prs,widths)]}
        return put(role,v,box)

    titles=['Tổng quan theo tháng','Sản phẩm và nơi nhận','Cờ nguồn và hiệu ngày']
    put('rail',button('',dark=True),(16,16,1248,70))
    label('title','NILE SALES | '+titles[index],(32,22,660,36),21)
    label('scope','01–07/2025 · Theo ngày bán · Phạm vi theo bộ lọc',(32,58,650,20),10,'#C3C5CC')
    for i,(caption,x,w) in enumerate([('Tổng quan',720,130),('Sản phẩm / nơi nhận',850,220),('Cờ / hiệu ngày',1090,164)]):
        put('nav'+str(i),button(caption,'PageNavigation',PAGES[i],i==index,True),(x,34,w,36))
        if i==index:
            v=button('');v['visual']['visualContainerObjects']['background']=prop(show=True,color='#865EFF',transparency=0)
            put('active_tab',v,(x,76,w,3))
    select('month','DimDate','YearMonth','Tháng',(16,96,236,48),True)
    select('category','DimProduct','Category','Nhóm sản phẩm',(268,96,300,48),True)
    select('place','DimDestination','To_Location','Nơi nhận',(584,96,440,48),True)
    put('reset',button('Đặt lại','ClearAllSlicers'),(1040,96,224,48))
    summary=[('value','Giá trị dòng nguồn','Giá trị nguồn',0,'#,0'),('qty','Lượng bán nguồn','Lượng bán',0,'#,0'),('rows','Số dòng nguồn','Dòng nguồn',0,'#,0'),('codes','Số mã nhóm nguồn','Mã nhóm nguồn',0,'#,0')]
    if index==2:
        summary=[('flagcount','Số dòng có cờ hoàn','Dòng có cờ 1',0,'#,0'),('flagrate','Tỷ lệ dòng có cờ hoàn','Tỷ lệ trên mẫu cờ hợp lệ',2,'0.00%'),('median','Trung vị hiệu ngày nguồn','Trung vị hiệu ngày nguồn',1,'0.0'),('daysample','Số dòng đủ ngày','Mẫu ngày đủ',0,'#,0')]
    for x,(role,m,caption,precision,fmt) in zip([16,332,648,964],summary):number(role,m,caption,(x,156,300,102),precision,fmt)
    category_share='Tỷ trọng giá trị sản phẩm được chọn';place_share='Tỷ trọng giá trị nơi nhận được chọn'
    if index==0:
        plot('trend','DimDate','YearMonth',['Giá trị dòng nguồn','Giá trị nguồn tháng trước'],'GIÁ TRỊ THEO THÁNG · SO KỲ TRƯỚC',(16,274,776,184))
        plot('placebar','DimDestination','To_Location',['Giá trị dòng nguồn'],'ĐÓNG GÓP THEO NƠI NHẬN',(808,274,456,184),True,place_share)
        plot('qtychart','DimDate','YearMonth',['Lượng bán nguồn'],'LƯỢNG THEO THÁNG',(16,474,380,230))
        plot('categorybar','DimProduct','Category',['Giá trị dòng nguồn'],'ĐÓNG GÓP THEO NHÓM',(412,474,380,230),True,category_share)
        grid('monthtable',[('DimDate','YearMonth'),('Measure','Giá trị dòng nguồn'),('Measure','Giá trị nguồn tháng trước'),('Measure','Thay đổi giá trị nguồn so tháng trước (%)')],['Tháng','Giá trị','Kỳ trước','Thay đổi'],'SO VỚI THÁNG TRƯỚC',(808,474,456,230),[76,110,110,110])
    if index==1:
        select('sku','DimProduct','SKU_Code','Mã sản phẩm · chọn một tháng để so kỳ trước',(16,272,1248,48))
        put('skuscatter',scatter('DimProduct','SKU_Code','Lượng bán nguồn','Giá trị dòng nguồn','Số dòng nguồn',
            '50 SẢN PHẨM · LƯỢNG × GIÁ TRỊ · CỠ CHẤM = SỐ DÒNG','Lượng bán','Giá trị nguồn'),(16,336,792,176))
        sku=grid('skutable',[('DimProduct','SKU_Code'),('DimProduct','Category'),('Measure','Số dòng nguồn'),('Measure','Lượng bán nguồn'),('Measure','Giá trị dòng nguồn'),('Measure','Giá trị nguồn tháng trước'),('Measure','Thay đổi giá trị nguồn so tháng trước (%)')],['SKU','Nhóm','Dòng','Lượng','Giá trị','Kỳ trước','Thay đổi'],'CHI TIẾT 50 MÃ SẢN PHẨM',(16,528,792,176),[90,130,80,80,135,135,104])
        bars=[plot('categorybar','DimProduct','Category',['Giá trị dòng nguồn'],'ĐÓNG GÓP THEO NHÓM',(824,336,440,176),True,category_share),plot('placebar','DimDestination','To_Location',['Giá trị dòng nguồn'],'ĐÓNG GÓP THEO NƠI NHẬN',(824,528,440,176),True,place_share)]
    if index==2:
        select('from','FactSalesLine','From_Location','Nơi gửi',(16,272,860,48))
        select('flag','FactSalesLine','Is_Returned','Cờ nguồn (0/1)',(892,272,372,48))
        put('flagcategory',scatter('DimProduct','Category','Số dòng có cờ hợp lệ','Tỷ lệ dòng có cờ hoàn','Số dòng có cờ hoàn',
            'NHÓM SẢN PHẨM · MẪU × TỶ LỆ CỜ 1','Số dòng cờ hợp lệ','Tỷ lệ cờ 1'),(16,336,616,176))
        for role,t,c,caption,box in [('flagplace','DimDestination','To_Location','CỜ NGUỒN · THEO NƠI NHẬN',(16,528,616,176))]:
            grid(role,[(t,c),('Measure','Số dòng có cờ hoàn'),('Measure','Số dòng có cờ hợp lệ'),('Measure','Tỷ lệ dòng có cờ hoàn')],['Nhóm' if c=='Category' else 'Nơi nhận','Cờ 1','Mẫu cờ','Tỷ lệ'],caption,box,[240,95,110,120])
        monthly=plot('daychart','DimDate','YearMonth',['Tỷ lệ dòng có cờ hoàn'],'TỶ LỆ CỜ 1 THEO THÁNG · ĐỌC KÈM MẪU',(648,336,616,176),False,'Số dòng có cờ hợp lệ')
        monthly['visual']['visualType']='lineChart'
        monthly['visual']['objects']['lineStyles']=prop(strokeWidth=3,showMarker=True,markerSize=5)
        monthly['visual']['objects']['valueAxis']=prop(fontSize=9,showAxisTitle=False,start=0,labelDisplayUnits=1,labelPrecision=1,gridlineColor='#ECEEF4')
        grid('routes',[('FactSalesLine','From_Location'),('DimDestination','To_Location'),('Measure','Số dòng đủ ngày'),('Measure','Trung vị hiệu ngày nguồn')],['Nơi gửi','Nơi nhận','Mẫu ngày','Trung vị'],'TUYẾN GỬI → NHẬN · ĐỌC KÈM MẪU',(648,528,616,176),[190,190,110,100])

    folder=ROOT/'pages'/PAGES[index];folder.mkdir(parents=True,exist_ok=True)
    pagefile=folder/'page.json';page=json.loads(pagefile.read_text(encoding='utf-8-sig'))
    page.update(displayName=titles[index],width=1280,height=720,displayOption='FitToPage',objects={'background':prop(color='#F5F6FA',transparency=0)})
    page.pop('visualInteractions',None)
    if index==1:
        page['visualInteractions']=[{'source':b['name'],'target':v['name'],'type':'DataFilter' if v['name']==sku['name'] else 'NoFilter'} for b in bars for v in items if v['name']!=b['name']]
    pagefile.write_text(json.dumps(page,ensure_ascii=False,indent=2),encoding='utf-8')
    assert len({v['name'] for v in items})==len(items)
    current={v['name'] for v in items}
    roles=set(OLD)|{'brand','nav0','nav1','nav2','active_tab','reset','categorybar','placebar','sku','skutable','skuscatter','from','flag','flagcount','flagrate','median','daysample','flagcategory','flagplace','daychart','routes'}
    owned={identity(role) for role in roles}
    obsolete=[q for q in folder.glob('visuals/*/visual.json') if q.parent.name in owned-current]
    for q in obsolete:
        assert q.resolve().is_relative_to(ROOT.resolve()) and set(z.name for z in q.parent.iterdir())=={'visual.json'}
    for v in items:
        dest=folder/'visuals'/v['name']/'visual.json';dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
    for q in obsolete:q.unlink();q.parent.rmdir()
    print(titles[index],len(items),'containers; removed',len(obsolete),'owned obsolete containers')
    return items


if __name__=='__main__':
    if '--check-charts' in sys.argv:
        for index, role, dimension, x, y in [
            (1, 'skuscatter', 'SKU_Code', 'Lượng bán nguồn', 'Giá trị dòng nguồn'),
            (2, 'flagcategory', 'Category', 'Số dòng có cờ hợp lệ', 'Tỷ lệ dòng có cờ hoàn')]:
            identity = hashlib.sha256(f'nile:{index}:{role}'.encode()).hexdigest()[:20]
            v = json.loads((ROOT/'pages'/PAGES[index]/'visuals'/identity/'visual.json').read_text(encoding='utf-8-sig'))
            q = v['visual']['query']['queryState']
            assert v['visual']['visualType'] == 'scatterChart'
            assert q['Category']['projections'][0]['field']['Column']['Property'] == dimension, 'Lost point grouping'
            assert q['X']['projections'][0]['field']['Measure']['Property'] == x, 'Wrong x-axis unit'
            assert q['Y']['projections'][0]['field']['Measure']['Property'] == y, 'Wrong y-axis unit'
        print('Chart grouping and axis units passed; no report files written')
        sys.exit(0)
    for index in range(3):build(index)
    order=ROOT/'pages/pages.json';meta=json.loads(order.read_text(encoding='utf-8-sig'));meta.update(pageOrder=PAGES,activePageName=PAGES[0]);order.write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
    reportfile=ROOT/'report.json';report=json.loads(reportfile.read_text(encoding='utf-8-sig'))
    report['themeCollection']['customTheme']={'name':'NileExecutive.json','reportVersionAtImport':{'visual':'2.9.0','report':'3.3.0','page':'2.1.0'},'type':'RegisteredResources'}
    packages=report.setdefault('resourcePackages',[])
    rr=next((r for r in packages if r['name']=='RegisteredResources'),None)
    if rr is None:rr={'name':'RegisteredResources','type':'RegisteredResources','items':[]};packages.append(rr)
    rr['items']=[r for r in rr['items'] if r['name'] not in {'NileExecutive','NileExecutive.json'}]+[{'name':'NileExecutive.json','path':'NileExecutive.json','type':'CustomTheme'}]
    resource=ROOT.parent/'StaticResources/RegisteredResources/NileExecutive.json';resource.parent.mkdir(parents=True,exist_ok=True)
    theme=json.loads(Path('reports/phase5a/template_executive.json').read_text(encoding='utf-8-sig'))
    theme['name']='NileExecutive.json'
    resource.write_text(json.dumps(theme,ensure_ascii=False,indent=2),encoding='utf-8')
    reportfile.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
