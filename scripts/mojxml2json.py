import os, sys
import xml.etree.ElementTree as ET
from zipfile import ZipFile
import json
import xy2do

XMLNS="http://www.moj.go.jp/MINJI/tizuxml"
XMLNS_ZMN="http://www.moj.go.jp/MINJI/tizuzumen"

PRM_NS=0
PRM_NS_ZMN=1
OUT_DELIMITER="\t"

def usage():
  print("#usage:  python3 mojxml2json.py in_data_dir out_dir")
  print("#   example: python3 getBasicInfo3.py ./kuwanauchi12chiba/xml ./out/12chiba")

#strings with namespace
def swns(s):
    return "".join(["{", XMLNS ,"}",s])

#string with namespace_zmn
def swns_zmn(s):
    return "".join(["{", XMLNS_ZMN ,"}", s])

def NoneToBlank(s):
    return "" if s is None else s

def getText(tree, name):
    if (tree is None):
        return ""
    return NoneToBlank(tree.findtext(swns(name)))

def getText_zmn(tree, name):
    if (tree is None):
        return ""
    return NoneToBlank(tree.findtext(swns_zmn(name)))

def getIdref(ele, name):
    return ele.find(swns(name)).attrib["idref"]


def getXY(tree, name, prm_zmn=PRM_NS):
    if prm_zmn==PRM_NS_ZMN:
        tmp = tree.find(swns_zmn(name))
    else:
        tmp = tree.find(swns(name))
    x = getText_zmn(tmp, "X")
    y = getText_zmn(tmp, "Y")
    return (x,y)

def getYMD(tree, name):
    tmp = tree.find(swns(name))
    y = getText(tmp, "年")
    m = getText(tmp, "月")
    d = getText(tmp, "日")
    return (y,m,d)


#done
def extractBasicInfo(root):
    binfo = {}
    binfo["version"] = getText(root,"version")
    binfo["map_name"] = getText(root,"地図名")
    binfo["city_code"] = getText(root,"市区町村コード")
    binfo["city_name"] = getText(root,"市区町村名")
    binfo["coord"] = getText(root, "座標系")
    binfo["soku_han"] = getText(root, '測地系判別')
    binfo["conv_pgm"] = getText(root, '変換プログラム')
    binfo["conv_pgm_ver"] = getText(root, '変換プログラムバージョン')
    binfo["conv_pgm_param"] = getText(root, '変換パラメータバージョン')
    return binfo


def printZkkFude(filename, map_no, idref, ofh):
    outary = [filename, map_no, idref]
    array_write(ofh, outary)

#done
def extractZkk(zkkarray):
    zkk_id = 0 #参照のために振る連番
    zkk_info={}
    fuderef_info={}
    for zkkone in zkkarray:
        zkk_id += 1
        zkk = {}
        zkk["map_no"] = getText(zkkone, "地図番号")
        zkk["scale"] = getText(zkkone, "縮尺分母")
        zkk["unknown_direct_flg"] = getText(zkkone, "方位不明フラグ")

        #未使用
        # (xLB,yLB) = getXY(zkkone, "左下座標")
        # (xRB,yRB) = getXY(zkkone, "右下座標")
        # (xLT,yLT) = getXY(zkkone, "左上座標")
        # (xRT,yRT) = getXY(zkkone, "右上座標")

        zkk["maptype"] = getText(zkkone, "地図種類")
        zkk["mapcategory"] = getText(zkkone, "地図分類")
        zkk["map_material"] = getText(zkkone, "地図材質")

        (zkk["ySET"],zkk["mSET"],zkk["dSET"]) = getYMD(zkkone, "備付地図年月日")
        (zkk["yMAP"],zkk["mMAP"],zkk["dMAP"]) = getYMD(zkkone, "地図作成年月日")
        # "tzu:分割図葉"
        zkk_info[zkk_id] = zkk

        # 筆参照IDリスト作成
        fuderef = zkkone.findall(swns("筆参照"))
        for fr in fuderef:
            fuderef_info[fr.attrib["idref"]] = zkk_id  ## zkk_info[fuderef_info[筆ID]] として図郭情報を利用可能

    return zkk_info, fuderef_info
        

#done
def extractPoint(areaarray):
    area_point = areaarray.findall(swns_zmn("GM_Point"))
    pinfo = {}
    for points in area_point:
        point_id = points.attrib["id"]
        dp = points.find(swns_zmn("GM_Point.position"))
        (x,y)= getXY(dp, "DirectPosition", PRM_NS_ZMN)
        pinfo[point_id] = (x,y)
    return pinfo

#done
def extractCurve(areaarray, point_info):
    area_curve = areaarray.findall(swns_zmn("GM_Curve"))
    cinfo = {}

    for curve in area_curve:
        curve_id = curve.attrib["id"]
        cv1=curve.find(swns_zmn("GM_Curve.segment"))
        cv2=cv1.find(swns_zmn("GM_LineString"))
        cv3=cv2.find(swns_zmn("GM_LineString.controlPoint"))
        #cv4=cv3.find(swns_zmn("GM_PointArray.column"))
        lineary = []
        for cv in cv3:
            #directAddress
            (x,y) = getXY(cv, "GM_Position.direct", PRM_NS_ZMN)
            #indireectAddress
            cv5 = cv.find(swns_zmn("GM_Position.indirect"))
            idref = ""
            if (not cv5 is None):
                idref = cv5.find(swns_zmn("GM_PointRef.point")).attrib["idref"]

                (x, y) = point_info[idref]
            lineary.append((x,y))
        cinfo[curve_id] = lineary
    return cinfo

def getLinesStartEndXYs(lineary):
    return (lineary[0][0], lineary[0][1], lineary[1][0], lineary[1][1])


#
def makePolygonPointsArray(c_idrefs, curve_info):
    sur_polygon=[]
    (x0, y0, xcur2, ycur2) = (0,0,0,0)
    cnt=0
    for sf in c_idrefs:
        cnt += 1
        c_idref = sf.attrib["idref"]
        lineary = curve_info[c_idref]

        if cnt==1:
            (x0, y0, xprev, yprev) = getLinesStartEndXYs(lineary)
            sur_polygon.append((x0,y0))
            sur_polygon.append((xprev, yprev))
        else:
            (xcur1, ycur1, xcur2, ycur2) = getLinesStartEndXYs(lineary)
            if (xcur1!=xprev or ycur1!=yprev):
                print("ERROR: Not Connected Lines") #TODO
            sur_polygon.append((xcur2,ycur2))
            (xprev, yprev) = (xcur2, ycur2)
    if (xcur2!=x0 or ycur2!=y0):
        print("ERROR: Not Connect for a ring.") #TODO
    return sur_polygon


#done
def extractSurface(areaarray, curve_info):
    area_surface = areaarray.findall(swns_zmn("GM_Surface"))
    sinfo = {}
    for surface in area_surface:
        surface_id = surface.attrib["id"]
        sf1 = surface.find(swns_zmn("GM_Surface.patch"))
        sf2 = sf1.find(swns_zmn("GM_Polygon"))
        sf3 = sf2.find(swns_zmn("GM_Polygon.boundary"))
        sf4 = sf3.find(swns_zmn("GM_SurfaceBoundary"))

        sf5ext = sf4.find(swns_zmn("GM_SurfaceBoundary.exterior"))

        one_surinfo=[]    
        sf6ext = sf5ext.find(swns_zmn("GM_Ring"))
        sur_ext = makePolygonPointsArray(sf6ext, curve_info)
        one_surinfo.append(sur_ext)

        sf5int = sf4.findall(swns_zmn("GM_SurfaceBoundary.interior"))
        if (not sf5int is None):
            for sur_int_one in sf5int:
                sf6int = sur_int_one.find(swns_zmn("GM_Ring"))
                sinfo_int = makePolygonPointsArray(sf6int, curve_info)
                one_surinfo.append(sinfo_int)
        else:
            one_surinfo.append([])
        sinfo[surface_id]=one_surinfo
    return sinfo

def make_linestr_for_write(outary):
    return OUT_DELIMITER.join(map(str,outary))

def lines_write(ofh, lines):
    if len(lines) > 0:
        ofh.write("\n".join(lines)+"\n")

def array_write(ofh, outary):
    outstr = make_linestr_for_write(outary)
    ofh.write(outstr+"\n")

def out_jsonheader(ofh):
    outstr = '{"type": "FeatureCollection", "features": ['
    ofh.write(outstr+"\n")
def out_jsonfooter(ofh):
    outstr = '], "crs": null}'
    ofh.write(outstr+"\n")

#done
def extractAndOutputSyudaiFude(syudaiarray, basic_info, surface_info, zkk_info, zkk_fude_info, ofh):
    fudearray = syudaiarray.findall(swns("筆"))

    out_jsonheader(ofh)
    fude_info = {}
    cnt=0
    for fudeone in fudearray: #筆
        fude={}
        fude_id = fudeone.attrib["id"]
        fude["fude_id"] = fude_id
        fude["oaza"] = getText(fudeone, "大字コード") 
        fude["chome"]= getText(fudeone, "丁目コード") 
        fude["koaza"]= getText(fudeone, "小字コード") 
        fude["yobi"] = getText(fudeone, "予備コード") 
        fude["oaza_name"] = getText(fudeone, "大字名") 
        fude["chome_name"] = getText(fudeone, "丁目名") 
        fude["koaza_name"] = getText(fudeone, "小字名") 
        fude["yobi_name"] = getText(fudeone, "予備名") 
        fude["chiban"] = getText(fudeone, "地番") 
        fude["seido"] = getText(fudeone, "精度区分")
        fude["zahyo_type"] = getText(fudeone, "座標値種別") 
        fude["shape"] = getIdref(fudeone, "形状")
        fude["mitei"] = getText(fudeone, "筆界未定構成筆")
        #
        try:                                          # memo:図郭がないものもあるので空dictを明示
            zkk = zkk_info[zkk_fude_info[fude_id]] 
        except KeyError:
            zkk = {}

        this_coord = makeCoordDict(surface_info[fude["shape"]], basic_info["coord"])

        one_fude_json_part = makeJson(fude, basic_info, this_coord, zkk)
        if (cnt!=0):
            ofh.write(",")
        ofh.write(one_fude_json_part+"\n")
        cnt+=1
    out_jsonfooter(ofh)


    return one_fude_json_part

def getCoordNumberByName(coord_str):
    #todo: ゼロもエラーにする
    coord_str_array = ["公共座標%d系"%x for x in range(0,20)]
    try:
        kei = coord_str_array.index(coord_str)
    except ValueError:
        kei = -1
    return kei


def makeCoordDict(surface_array, coord_str):
    kei = getCoordNumberByName(coord_str)
    resary = []
    for onesurface in surface_array:
        ary = []
        for xy in onesurface:
            if (kei>0):
                (lat, lon) = xy2do.xy2do(float(xy[0]), float(xy[1]), kei)
            else:
                (lat, lon) = (float(xy[0]), float(xy[1]))
            ary.append([lon, lat])  #GeoJSONはlon-lat！
        resary.append(ary)
    return resary

def makeJson(fude, basic_info, coord_part, zkk):
    one_fude_dict = {
        "type": "Feature",
        "geometry": {
            "type": "MultiPolygon",
            "coordinates": [coord_part],
        },
        "properties": {
            "筆ID": fude["fude_id"],
            "version": basic_info["version"],
            "座標系": basic_info["coord"],
            "測地系判別": basic_info["soku_han"],
            "地図名": basic_info["map_name"],
            "地図番号": zkk.get("map_no",""),
            "縮尺分母":zkk.get("scale",""),
            "市区町村コード":basic_info["city_code"],
            "市区町村名":basic_info["city_name"],
            "大字コード":fude["oaza"],
            "丁目コード":fude["chome"],
            "小字コード": fude["koaza"],
            "予備コード": fude["yobi"],
            "大字名": fude["oaza_name"],
            "丁目名": fude["chome_name"],
            "小字名": fude["koaza_name"],
            "予備名": fude["yobi_name"],
            "地番": fude["chiban"],
            "精度区分": fude["seido"],
            "座標値種別": fude["zahyo_type"],
            "筆界未定構成筆": fude["mitei"],
            #
            "地図種類": zkk.get("maptype",""),
            "地図分類": zkk.get("mapcategory",""),
            "地図材質": zkk.get("map_material",""),
            "方位不明フラグ": zkk.get("unknown_direct_flg",""),
        }
    }

    fude_json = json.dumps(one_fude_dict, ensure_ascii=False, indent=4)
    #fude_json = json.dumps(one_fude_dict, ensure_ascii=False) # for release file (Non linefeeded)
    return fude_json


#deprecated
def extractSyudai(root, filename, ofh):
    syudaiarray=root.find(swns("主題属性"))

    kijunpointarray=syudaiarray.findall(swns("基準点"))
    fudekaipointarray=syudaiarray.findall(swns("筆界点"))
    karigyouarray=syudaiarray.findall(swns("仮行政界線"))
    fudekailinearray=syudaiarray.findall(swns("筆界線"))
    fudearray=syudaiarray.findall(swns("筆"))
    cnt = 0
    lines = []    
    for syu in kijunpointarray: #基準点
        cnt += 1
        kijun_id = getText(syu, "名称")
        shape = getIdref(syu, "形状")
        kijun_type = getText(syu, "基準点種別")
        kijun_kbn = getText(syu, "埋標区分")

        outary = [filename, "基準点", shape, kijun_id,kijun_type, kijun_kbn,"","","","","","","",""]
        lines.append(make_linestr_for_write(outary))
        #array_write(ofh, [filename, "基準点", shape, kijun_id,kijun_type, kijun_kbn,"","","","","","","",""])
    lines_write(ofh, lines)

    lines = []    
    for syu in fudekaipointarray: #筆界点
        cnt += 1
        point_no = getText(syu, "点番名")
        shape = getIdref(syu, "形状")
        #print("筆界点", point_no, shape)
        outary = [filename, "筆界点", shape, point_no,"","","","","","","","","",""]
        lines.append(make_linestr_for_write(outary))
        #array_write(ofh, [filename, "筆界点", shape, point_no,"","","","","","","","","",""])
    lines_write(ofh, lines)
    
    lines = []    
    for syu in karigyouarray: #仮行政界線
        cnt += 1
        line_type = getText(syu, "線種別")
        shape = getIdref(syu, "形状")
        outary = [filename, "仮行政界線", shape, "", line_type,"","","","","","","","",""]
        lines.append(make_linestr_for_write(outary))
        #array_write(ofh, [filename, "仮行政界線", shape, "", line_type,"","","","","","","","",""])
    lines_write(ofh, lines)

    lines = []    
    for syu in fudekailinearray: #筆界線
        cnt += 1
        line_type = getText(syu, "線種別")
        shape = getIdref(syu, "形状")
        #print("筆界線", line_type, shape)
        lines.append(make_linestr_for_write(outary))
    lines_write(ofh, lines)
        
    lines = []    
    for syu in fudearray: #筆
        cnt += 1
        oaza = getText(syu, "大字コード") 
        chome= getText(syu, "丁目コード") 
        koaza= getText(syu, "小字コード") 
        yobi = getText(syu, "予備コード") 
        oaza_name = getText(syu, "大字名") 
        chome_name = getText(syu, "丁目名") 
        chiban = getText(syu, "地番") 
        zahyo_type = getText(syu, "座標値種別") 
        shape = getIdref(syu, "形状")
        
        outary = [filename, "筆",shape, "","","", oaza, chome, koaza, yobi, oaza_name, chome_name, chiban, zahyo_type]
        lines.append(make_linestr_for_write(outary))
    lines_write(ofh, lines)

    return cnt


def main():
    args = sys.argv
    if (len(args)<2):
        usage()
        exit()

    root_path = args[1]
    output_path = args[2]

    files = os.listdir(root_path)

    n=0
    for fn in files:
        n+=1
        base, ext = os.path.splitext(fn)
        if ext!='.zip':
            continue
        print("[%d]start: %s"%(n,fn))

        #
        fout = open(output_path+"/"+base+".geojson", 'w')
        with ZipFile(root_path+"/"+fn) as zf:
          with zf.open(zf.namelist()[0]) as fd:
            tree = ET.parse(fd)
            root = tree.getroot()

            #基本情報を変数に保持
            basic_info = extractBasicInfo(root)

            #PointをPID->x,y のdictに保持
            areaarray = root.find(swns("空間属性"))
            point_info = extractPoint(areaarray)

            # CURVEを CID->(x1,y1),(x2, y2)でdictに保持
            curve_info = extractCurve(areaarray, point_info)

            # surfaceを FID->(x1,y1)..(sn,yn),(x1,y1)で保持
            surface_info = extractSurface(areaarray, curve_info)

            # 図郭情報
            zkkarray = root.findall(swns("図郭"))
            (zkk_info, zkk_fude_info) = extractZkk(zkkarray)

            #主題の中から筆情報だけ抜き出し、上記情報を利用して1件のGeoJson情報を構築、出力
            syudaiarray = root.find(swns("主題属性"))
            fude_info_json = extractAndOutputSyudaiFude(syudaiarray, basic_info, surface_info, zkk_info, zkk_fude_info, fout)

        fout.close()


#TODO 未表示線は何らかの形で返したい。どう返すと利用できるのか要調査


main()