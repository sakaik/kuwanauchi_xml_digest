## 出力ファイル（CSVフォーマット）について
- 基本情報サマリファイル(*_summary.csv)と図各情報ファイル(*_zukaku.csv)ファイルの2つがあります
- ひとつの基本サマリファイルに対して 0..* 個の図郭情報が紐付きます。
- 基本サマリと図郭情報の紐付けはファイル名（今回は XMLではなくZIPファイル名）としています
- 後続処理を考慮し、各ファイルのヘッダに記載の項目名は、アルファベット文字を基準とした名前にしています。日本語名との対応は後述します


## 基本情報サマリファイル(*_summary.csv)
- 各ファイルに1つだけ存在します（filename列でユニーク）
- この情報に紐付く図郭情報の数を numbers_of_zukaku列に掲載しています
- ヘッダ文字列およびその日本語対応は以下のとおりです

filename,city_name,city_code,map_name,coordinate,version,sokuti_hanbetu,conv_pgm,conv_pgm_version,conv_pgm_param_version,numbers_of_zukaku
ZIPファイル名,市区町村名,市区町村コード,地図名,座標系,version,測地系判別,変換プログラム,変換プログラムバージョン,変換パラメータバージョン,図郭数



## 図郭情報ファイル
- (再掲)ひとつのファイルに対して1つまたは複数の図郭が存在します。存在しない場合もあります。
- ヘッダ文字列およびその日本語対応は以下のとおりです

filename,map_no,scale,unknown_direct_flg,leftbottom_x,leftbottom_y,lefttop_x,lefttop_y,rightbottom_x,rightbottom_y,righttop_x,righttop_y,maptype,mapcategory,mapmaterial,sonae_ymd_y,sonae_ymd_m,sonae_ymd_d,map_ymd_y,map_ymd_m,map_ymd_d
ZIPファイル名,地図番号,縮尺分母,方位不明フラグ,左下座標X,左下座標Y,左上座標X,左上座標Y,右下座標X,右下座標Y,右上座標X,右上座標Y,地図種類,地図分類,地図材質,備付地図年月日_年,備付地図年月日_月,備付地図年月日_日,地図作成年月日_年,地図作成年月日_月,地図作成年月日_日
