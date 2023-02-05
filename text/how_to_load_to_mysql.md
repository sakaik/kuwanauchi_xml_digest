## MySQLへのデータロード方法

本リポジトリの csvデータを MySQL 8.0 にロードする方法を説明します。


### *_summary ファイル群の登録

- テーブルを作成
    - 列サイズは適当に大きめなので、気持ち悪い人は適切なサイズに変更して使ってください。

```
CREATE TABLE mojmap_summary (
    filename  varchar(100) PRIMARY KEY,
    city_name varchar(100) ,
    city_code char(5) ,
    map_name  varchar(100),
    coordinate varchar(100) ,
    version    varchar(10),
    sokuti_hanbetu  varchar(10),
    conv_pgm varchar(100),
    conv_pgm_version varchar(100),
    conv_pgm_param_version varchar(100),
    numbers_of_zukaku int
);
```

- csvデータをテーブルにロードする
    - MySQL 8.0ではセキュリティ強化のため、ファイルからのロードについての制約が加わっています。ロードのために少し手続き（指定）が必要です。
    - 手続き（指定）は、サーバ側の設定、そして、ロード処理を行うmysqlクライアントの接続時の指定の両側が必要です。
        - サーバ側設定
            - mysql>  `mysql> SET GLOBAL local_infile=on; `
        - クライアント接続時指定
            - $ `mysql -umyuser -p --local-infile=1`
    - ロード処理を行うSQL命令の例を以下に示します。`/home/ubuntu/csvdata/` の部分は、csvファイルを置いたフォルダに置換してください

```
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/01hokkaido_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/02aomori_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/03iwate_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/04miyagi_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/05akita_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/06yamagata_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/07fukushima_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/08ibaraki_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/09tochigi_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/10gumma_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/11saitama_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/12chiba2_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/13tokyo_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/14kanagawa_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/15niigata_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/16toyama_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/17ishikawa_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/18fukui_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/19yamanashi_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/20nagano_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/21gifu_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/22shizuoka_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/23aichi_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/24mie_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/25shiga_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/26kyoto_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/27osaka_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/28hyogo_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/29nara_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/30wakayama_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/31tottori_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/32shimane_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/33okayama_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/34hiroshima_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/35yamaguchi_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/36tokushima_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/37kagawa_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/38ehime_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/39kochi_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/40fukuoka_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/41saga_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/42nagasaki_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/43kumamoto_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/44oita_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/45miyazaki_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/46kagoshima_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/47okinawa_summary.csv' INTO TABLE mojmap_summary FIELDS TERMINATED BY ',' IGNORE 1 LINES;
```

- 一部データの修正
　本リポジトリのsummaryデータでは、データ中に含まれるコンマを、セパレータであるコンマと区別するために $ に置き換えています。
（本来は フィールドを "" でエンクローズするか、tsvを採用すべきでした。作業完了後に気づいたので、手作業で問題のあるデータを編集して公開しています）
そのため、オリジナルデータを忠実に再現するには、この置換文字を元に戻す必要があります。
    - まず念のため、置換される予定のデータを目視確認します。

```
mysql> SELECT map_name FROM mojmap_summary WHERE map_name LIKE '%$%';
+---------------------------------------------------+
| map_name                                          |
+---------------------------------------------------+
| 41135井吹台西町８丁目13$15                        |
| 41135井吹台西町21$23$12                           |
| 岡口1$2丁目他                                     |
| 最新野原西1$2$4                                   |
| 最新野原中3$4                                     |
| 五條市野原中1$2$5丁目                             |
| 改R2.2.7 13$14阿木名、勝浦                        |
| 改1R2.2.7 13$14瀬戸内町節子                       |
| 改R2.2.7-13$14大字古仁屋（乙2）修正後             |
| R1$3035大字小島修正後                             |
+---------------------------------------------------+
10 rows in set (0.19 sec)
```
    - 問題なければ、以下のクエリで $ を , に置換します。
```
UPDATE mojmap_summary SET map_name=replace(map_name,'$',',') WHERE map_name LIKE '%$%';
```





### *_zukaku ファイル群の登録
- テーブルを作成
  - 数字っぽい列(スケールや年月日)でも文字型を使っているのは LOAD DATA時のwarning抑止のためです

```
CREATE TABLE mojmap_zukaku (
    filename      varchar(100),
    map_no        varchar(50),
    scale         varchar(10),
    unknown_direct_flg  varchar(10),
    leftbottom_x  float,
    leftbottom_y  float,
    lefttop_x     float,
    lefttop_y     float,
    rightbottom_x float,
    rightbottom_y float,
    righttop_x    float,
    righttop_y    float,
    maptype       varchar(100),
    mapcategory   varchar(100),
    mapmaterial   varchar(100),
    sonae_ymd_y   varchar(4),
    sonae_ymd_m   varchar(2),
    sonae_ymd_d   varchar(2),
    map_ymd_y     varchar(4),
    map_ymd_m     varchar(2),
    map_ymd_d     varchar(2)
);
CREATE INDEX idx_zkk_fn ON mojmap_zukaku(filename);
```


- csvデータをテーブルにロードする
    - 詳細は上記 *_summary のロードの情報を参照ください
    - ロード処理を行うSQL命令の例を以下に示します。`/home/ubuntu/csvdata/` の部分は、csvファイルを置いたフォルダに置換してください


```
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/01hokkaido_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/02aomori_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/03iwate_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/04miyagi_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/05akita_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/06yamagata_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/07fukushima_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/08ibaraki_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/09tochigi_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/10gumma_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/11saitama_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/12chiba2_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/13tokyo_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/14kanagawa_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/15niigata_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/16toyama_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/17ishikawa_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/18fukui_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/19yamanashi_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/20nagano_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/21gifu_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/22shizuoka_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/23aichi_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/24mie_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/25shiga_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/26kyoto_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/27osaka_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/28hyogo_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/29nara_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/30wakayama_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/31tottori_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/32shimane_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/33okayama_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/34hiroshima_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/35yamaguchi_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/36tokushima_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/37kagawa_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/38ehime_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/39kochi_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/40fukuoka_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/41saga_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/42nagasaki_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/43kumamoto_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/44oita_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/45miyazaki_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/46kagoshima_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE '/home/ubuntu/csvdata/47okinawa_zukaku.csv' INTO TABLE mojmap_zukaku FIELDS TERMINATED BY ',' IGNORE 1 LINES;
```
