import os, sys
import xml.etree.ElementTree as ET
from zipfile import ZipFile

XMLNS="http://www.moj.go.jp/MINJI/tizuxml"
XMLNS_ZMN="http://www.moj.go.jp/MINJI/tizuzumen"

PRM_NS=0
PRM_NS_ZMN=1
OUT_DELIMITER="\t"

#tree = ET.parse('tmp/12222-0424-201.xml')
#filename = 'tmp/12222-0424-200.xml'

def usage():
  print("#usage:  python3 getBasicInfo3.py in_dir out_dir out_fn_base")
  print("#   example: python3 getBasicInfo3.py ./tmp ./out 12chiba")

#strings with namespace
def swns(s):
    #return "{"+ XMLNS +"}"+s
    return "".join(["{", XMLNS ,"}",s])
#string with namespace_zmn
def swns_zmn(s):
    #return "{"+ XMLNS_ZMN +"}"+s
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


def printBasicInfoHeader(ofh):
    headerary = ["filename","city_name","city_code","map_name","coordinate","version","sokuti_hanbetu","conv_pgm","conv_pgm_version","conv_pgm_param_version","numbers_of_zukaku"]
    ofh.write(OUT_DELIMITER.join(map(str,headerary))+"\n")

def extractBasicInfo(root, filename, ofh, cnt_zkk):
    ver = getText(root,"version")
    map_name = getText(root,"地図名")
    city_code = getText(root,"市区町村コード")
    city_name = getText(root,"市区町村名")
    coord = getText(root, "座標系")

    soku_han = getText(root, '測地系判別')
    conv_pgm = getText(root, '変換プログラム')
    conv_pgm_ver = getText(root, '変換プログラムバージョン')
    conv_pgm_param = getText(root, '変換パラメータバージョン')

    outary = [filename, city_name, city_code, map_name, coord, ver, soku_han, conv_pgm, conv_pgm_ver, conv_pgm_param, cnt_zkk]
    array_write(ofh, outary)

def printZkkFudeHeader(ofh):
    headerary = ["filename","map_no","fude_ref"]
    ofh.write(OUT_DELIMITER.join(map(str,headerary))+"\n")

def printZkkFude(filename, map_no, idref, ofh):
    outary = [filename, map_no, idref]
    array_write(ofh, outary)

def printZkkHeader(ofh):
    headerary = ["filename","map_no","scale","unknown_direct_flg","leftbottom_x","leftbottom_y","lefttop_x","lefttop_y","rightbottom_x","rightbottom_y","righttop_x","righttop_y","maptype","mapcategory","mapmaterial","sonae_ymd_y","sonae_ymd_m","sonae_ymd_d","map_ymd_y","map_ymd_m","map_ymd_d"]
    ofh.write(OUT_DELIMITER.join(map(str,headerary))+"\n")

def extractZkk(zkkarray, filename, ofh, ofh_zkkfude):
    cnt = 0
    for zkk in zkkarray:
        map_no = getText(zkk, "地図番号")
        scale = getText(zkk, "縮尺分母")
        unknown_direct_flg = getText(zkk, "方位不明フラグ")

        (xLB,yLB) = getXY(zkk, "左下座標")
        (xRB,yRB) = getXY(zkk, "右下座標")
        (xLT,yLT) = getXY(zkk, "左上座標")
        (xRT,yRT) = getXY(zkk, "右上座標")

        maptype= getText(zkk, "地図種類")
        mapcategory = getText(zkk, "地図分類")
        map_material = getText(zkk, "地図材質")

        (ySET,mSET,dSET) = getYMD(zkk, "備付地図年月日")
        (yMAP,mMAP,dMAP) = getYMD(zkk, "地図作成年月日")
        

        outary = [filename, map_no,scale, unknown_direct_flg, xLB,yLB,xLT,yLT,xRB,yRB,xRT,yRT,
                  maptype,mapcategory,map_material, ySET,mSET,dSET, yMAP,mMAP,dMAP]
        array_write(ofh, outary)

        cnt += 1

        fuderef=zkk.findall(swns("筆参照"))
        lines = []    
        for fr in fuderef:
            outary = [filename, map_no, fr.attrib["idref"]]
            lines.append(make_linestr_for_write(outary))
                #printZkkFude(filename, map_no, fr.attrib["idref"], ofh_zkkfude)
        lines_write(ofh_zkkfude, lines)

    return cnt
        
def printPointHeader(ofh):
    headerary = ["filename","point_id", "x", "y"]
    ofh.write(OUT_DELIMITER.join(map(str,headerary))+"\n")

def extractPoint(areaarray, filename, ofh):
    area_point = areaarray.findall(swns_zmn("GM_Point"))
    lines = []    
    for points in area_point:
        point_id = points.attrib["id"]
        dp=points.find(swns_zmn("GM_Point.position"))
        (x,y)= getXY(dp, "DirectPosition", PRM_NS_ZMN)
        outary = [filename, point_id, x, y]
        lines.append(make_linestr_for_write(outary))
        # array_write(ofh, outary)
    lines_write(ofh, lines)

def printCurveHeader(ofh):
    headerary = ["filename","curve_id", "x", "y", "idref"]
    ofh.write(OUT_DELIMITER.join(map(str,headerary))+"\n")

def extractCurve(areaarray, filename, ofh):
    area_curve = areaarray.findall(swns_zmn("GM_Curve"))
    lines = []    
    for curve in area_curve:
        curve_id = curve.attrib["id"]
        cv1=curve.find(swns_zmn("GM_Curve.segment"))
        cv2=cv1.find(swns_zmn("GM_LineString"))
        cv3=cv2.find(swns_zmn("GM_LineString.controlPoint"))
        #cv4=cv3.find(swns_zmn("GM_PointArray.column"))
        for cv in cv3:
            #directAddress
            (x,y) = getXY(cv, "GM_Position.direct", PRM_NS_ZMN)
            #indireectAddress
            cv5 = cv.find(swns_zmn("GM_Position.indirect"))
            idref = ""
            if (not cv5 is None):
                idref=cv5.find(swns_zmn("GM_PointRef.point")).attrib["idref"]
            outary = [filename, curve_id, x, y, idref]
            lines.append(make_linestr_for_write(outary))
            #array_write(ofh, outary)
    lines_write(ofh, lines)


def printSurfaceHeader(ofh):
    headerary = ["filename","surface_id", "idref"]
    ofh.write(OUT_DELIMITER.join(map(str,headerary))+"\n")

def extractSurface(areaarray, filename, ofh):
    area_surface = areaarray.findall(swns_zmn("GM_Surface"))
    lines = []    
    for surface in area_surface:
        surface_id = surface.attrib["id"]
        sf1 = surface.find(swns_zmn("GM_Surface.patch"))
        sf2 = sf1.find(swns_zmn("GM_Polygon"))
        sf3 = sf2.find(swns_zmn("GM_Polygon.boundary"))
        sf4 = sf3.find(swns_zmn("GM_SurfaceBoundary"))
        sf5 = sf4.find(swns_zmn("GM_SurfaceBoundary.exterior"))
        sf6 = sf5.find(swns_zmn("GM_Ring"))

        for sf in sf6:
            idref="-"
            idref = sf.attrib["idref"]
            outary = [filename, surface_id, idref]
            lines.append(make_linestr_for_write(outary))
            #array_write(ofh, outary)
    lines_write(ofh, lines)

def make_linestr_for_write(outary):
    return OUT_DELIMITER.join(map(str,outary))

def lines_write(ofh, lines):
    if len(lines) > 0:
        ofh.write("\n".join(lines)+"\n")

def array_write(ofh, outary):
    outstr = make_linestr_for_write(outary)
    ofh.write(outstr+"\n")


def printSyudaiHeader(ofh):
    headerary = ["filename","syudai_name", "shape", "point_no/kijun_id", "line_type/kijun_type", "kijun_kbn",
                 "ooaza", "chome", "koaza", "yobi", "ooaza_name", "chome_name", "chiban", "zahyo_type"]
    ofh.write(OUT_DELIMITER.join(map(str,headerary))+"\n")

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
        outary = [filename, "筆界線",shape, "", line_type,"","","","","","","","",""]
        lines.append(make_linestr_for_write(outary))
        #array_write(ofh, [filename, "筆界線",shape, "", line_type,"","","","","","","","",""])
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
    if (len(args)<3):
        usage()
        exit()

    root_path = args[1]
    output_path = args[2]
    output_fn_base = args[3]

    files = os.listdir(root_path)
    outfilename_base=output_path+"/"+output_fn_base
    fout_main = open(outfilename_base+"_summary.csv", 'w')
    fout_zkk = open(outfilename_base+"_zukaku.csv", 'w')
    fout_zkk_fude = open(outfilename_base+"_zukaku_fude.csv", 'w')
    fout_pt = open(outfilename_base+"_point.csv", 'w')
    fout_curve = open(outfilename_base+"_curve.csv", 'w')
    fout_surface = open(outfilename_base+"_surface.csv", 'w')
    fout_syudai = open(outfilename_base+"_syudai.csv", 'w')
    
    printBasicInfoHeader(fout_main)
    printZkkHeader(fout_zkk)
    printZkkFudeHeader(fout_zkk_fude)
    printPointHeader(fout_pt)
    printCurveHeader(fout_curve)
    printSurfaceHeader(fout_surface)
    printSyudaiHeader(fout_syudai)

    #print header for point　追加する

    n=0
    for fn in files:
        n+=1
        base, ext = os.path.splitext(fn)
        if ext!='.zip':
            continue
        print("[%d]start: %s"%(n,fn))
        with ZipFile(root_path+"/"+fn) as zf:
          with zf.open(zf.namelist()[0]) as fd:
            tree = ET.parse(fd)
            root = tree.getroot()

            zkkarray = root.findall(swns("図郭"))
            areaarray = root.find(swns("空間属性"))

            cnt_zkk = extractZkk(zkkarray, fn, fout_zkk, fout_zkk_fude)
            extractPoint(areaarray, fn, fout_pt)
            extractCurve(areaarray, fn, fout_curve)
            extractSurface(areaarray, fn, fout_surface)
            extractSyudai(root, fn, fout_syudai)
            extractBasicInfo(root, fn, fout_main, cnt_zkk)


main()