import os, sys
import xmltodict
from zipfile import ZipFile

# you need install xmltodict (e.g  "pip install xmltodict")

def usage():
  print("#usage:  python3 getBasicInfo2.py in_dir out_dir out_fn_base")
  print("#   example: python3 getBasicInfo2.py ./tmp ./out 12chiba")

##root_path = '/home/ubuntu/work/kuwanauchi12chiba/xml'
##root_path = '/home/ubuntu/work/kuwanauchi12chiba/tmp'
#root_path = './tmp'
#output_path = '/home/ubuntu/work/kuwanauchi12chiba/out'
#output_fn_base = '12chiba'

args = sys.argv
if (len(args)<3):
  usage()
  exit()

root_path = args[1]
output_path = args[2]
output_fn_base = args[3]

def getEle(dict, ele):
  return dict.get(ele, "")

def getZkk(zukaku):
  zkkdict = {}
  # TODO:すべて getEleに置き換える
  zkkdict["map_no"]= getEle(zukaku, '地図番号')
  zkkdict["scale"]= getEle(zukaku, '縮尺分母')
  zkkdict["unknown_direct_flg"] = getEle(zukaku, '方位不明フラグ')
  
  zkkdict["leftbottom_x"] = zukaku['左下座標']['zmn:X']
  zkkdict["leftbottom_y"] = zukaku['左下座標']['zmn:Y']
  zkkdict["lefttop_x"] = zukaku['左上座標']['zmn:X']
  zkkdict["lefttop_y"] = zukaku['左上座標']['zmn:Y']
  zkkdict["rightbottom_x"] = zukaku['右下座標']['zmn:X']
  zkkdict["rightbottom_y"] = zukaku['右下座標']['zmn:Y']
  zkkdict["righttop_x"]  = zukaku['右上座標']['zmn:X']
  zkkdict["righttop_y"]  = zukaku['右上座標']['zmn:Y']
  zkkdict["maptype"]     = getEle(zukaku, '地図種類')
  zkkdict["mapcategory"] = getEle(zukaku, '地図分類')
  zkkdict["mapmaterial"] = getEle(zukaku, '地図材質')

  zkk_ymd           = getEle(zukaku, '備付地図年月日')
  if zkk_ymd!="":
    zkkdict["sonae_ymd_y"] = getEle(zkk_ymd, '年')
    zkkdict["sonae_ymd_m"] = getEle(zkk_ymd, '月')
    zkkdict["sonae_ymd_d"] = getEle(zkk_ymd, '日')

  zkk_map_ymd           = getEle(zukaku, '地図作成年月日')
  if zkk_map_ymd != "":
    zkkdict["map_ymd_y"] = getEle(zkk_map_ymd, '年')
    zkkdict["map_ymd_m"] = getEle(zkk_map_ymd, '月')
    zkkdict["map_ymd_d"] = getEle(zkk_map_ymd, '日')

  return zkkdict
def csv_output(lst):
  return ",".join(map(str,lst))
def mainfile_output(ofh, lst):
  outstr = csv_output(lst)
  ofh.write(outstr+'\n')

def zukakufile_output(ofh, lst):
  outstr = csv_output(lst)
  ofh.write(outstr+'\n')

def write_header_main(ofh):
  headers=['filename','city_name','city_code','map_name','coordinate', 
          'version', 'sokuti_hanbetu','conv_pgm', 'conv_pgm_version', 'conv_pgm_param_version', 'numbers_of_zukaku']
  ofh.write(",".join(headers)+'\n')

def write_header_zkk(ofh):
  headers=['filename', 'map_no','scale','unknown_direct_flg','leftbottom_x','leftbottom_y','lefttop_x','lefttop_y','rightbottom_x','rightbottom_y','righttop_x','righttop_y','maptype','mapcategory','mapmaterial','sonae_ymd_y','sonae_ymd_m','sonae_ymd_d','map_ymd_y','map_ymd_m','map_ymd_d']
  ofh.write(",".join(headers)+'\n')

def main():
  files = os.listdir(root_path)
  outfilename_base=output_path+"/"+output_fn_base
  fout_main = open(outfilename_base+"_summary.csv", 'w')
  fout_zkk = open(outfilename_base+"_zukaku.csv", 'w')

  write_header_main(fout_main)
  write_header_zkk(fout_zkk)

  n=0
  for fn in files:
    n+=1
    base, ext = os.path.splitext(fn)
    if ext!='.zip':
      continue
    print("[%d]start: %s"%(n,fn))
    with ZipFile(root_path+"/"+fn) as zf:
      with zf.open(zf.namelist()[0]) as fd:
          doc = xmltodict.parse(fd.read())

          root = doc['地図'] ##
          ver = root['version']
          map_name = root['地図名']
          city_code = root['市区町村コード']
          city_name = root['市区町村名']
          coord = root['座標系']

          soku_han = getEle(root, '測地系判別')
          conv_pgm = getEle(root, '変換プログラム')
          conv_pgm_ver = getEle(root, '変換プログラムバージョン')
          conv_pgm_param = getEle(root, '変換パラメータバージョン')

          #zukakuは複数の場合もあり→ゼロの場合もあった！
          #print("ZKK type2: %s"% type(root['図郭'])) #list か dict が返る
          nof_zkk = 1
          if (not '図郭' in root):
            nof_zkk = 0
          else:
            if(type(root['図郭']) is list):
              zukaku = root['図郭']
              nof_zkk = len(root['図郭'])
            else:
              zukaku = [root['図郭']]

          #print(fn, city_name, city_code, map_name, coord, ver, nof_zkk)
          mainfile_output(fout_main, [fn, city_name, city_code, map_name, coord, 
                                 ver, soku_han, conv_pgm, conv_pgm_ver, conv_pgm_param, nof_zkk])
          if nof_zkk>0:
            for zukakuone in zukaku:
              zkk = getZkk(zukakuone)
              zukakufile_output(fout_zkk,[fn,
                getEle(zkk, 'map_no') ,getEle(zkk, 'scale')  ,getEle(zkk, 'unknown_direct_flg'),
                getEle(zkk, 'leftbottom_x') ,getEle(zkk, 'leftbottom_y') ,getEle(zkk, 'lefttop_x')  ,getEle(zkk, 'lefttop_y'), 
                getEle(zkk, 'rightbottom_x') ,getEle(zkk, 'rightbottom_y') ,getEle(zkk, 'righttop_x') ,getEle(zkk, 'righttop_y'),
                getEle(zkk, 'maptype'), getEle(zkk, 'mapcategory'), getEle(zkk, 'mapmaterial'), 
                getEle(zkk, 'sonae_ymd_y') ,getEle(zkk, 'sonae_ymd_m') ,getEle(zkk, 'sonae_ymd_d'),
                getEle(zkk, 'map_ymd_y')  ,getEle(zkk, 'map_ymd_m')  ,getEle(zkk, 'map_ymd_d') 
              ])
            #print(zkk)
      zf.close()

main()
