'''
本ファイルは以下の条件の下で、ご自身のアプリケーションに組み込むなど自由に利用ください。
- 本ヘッダ部分のコメントおよびコピーライト表示を削除しないこと。改変しないこと。
- コードの改造は自由に行って良い。改造物は再財布しても良い。
- 改造物の再配布の場合は、オリジナルとの区別のため、必ず追加のコピーライト表示をつけてください。
- 無保証です。原開発者は本関数を使用した結果について一切の責任を負いません。
- 本ファイルを利用したWebサービスには、本ファイルを使用した旨のクレジットを明記する必要はありません。が、謝意の表明は喜びます。
ver. 0.1.1
copyright @sakaik, 2023
'''
##おことわり:　上記利用規約は適宜変更していくことがあります

import math, sys

### xy to Degree function ###
# xy2do: args
#   平面直角座標系から緯度経度へ。
#   x, y: 平面直角座標系における X,Yの値
#   japaneseKei: 日本の平面直角座標系の系番号（1～19）
def xy2do(x, y, japaneseKei):
    # 楕円体長半径a、扁平率逆数F https://www.gsi.go.jp/sokuchikijun/datum-main.html
    a = 6378137.0
    F = 298.257222101

    #平面直角座標系のX軸縮尺係数
    m0 = 0.9999

    # 与えられた系の経度緯度をラジアンで返す。範囲外の値は与えられないものとする(手抜き)。ゼロが与えられた場合はゼロを原点として返す(意味はない)
    # 戻り rad単位で原点座標の(lat,lon)
    # https://www.gsi.go.jp/LAW/heimencho.html
    def getPhiLambFromKeiByRadian(kei):
        ary = [(0, 0), 
               (33.0, 129.5        ), (33.0, 131.0,       ), (36.0, 132+(10.0/60)), (33.0, 133.5        ), (36.0, 134+(20.0/60)),
               (36.0, 134+(20.0/60)), (36.0, 137+(10.0/60)), (36.0, 138.5        ), (36.0, 139+(50.0/60)), (36.0, 140+(50.0/60)),
               (44.0, 140+(15.0/60)), (44.0, 142+(15.0/60)), (44.0, 144+(15.0/60)), (26.0, 142.0        ), (26.0, 127.5        ),
               (26.0, 124.0        ), (26.0, 131.0,       ), (20.0, 136.0        ), (26.0, 154.0        )
               ]
        return (math.radians(ary[kei][0]), math.radians(ary[kei][1]))
    
    def makeAryA(n):
        A0 = 1 + (n**2)/4.0 + (n**4)/64.0
        A1 = -(3.0/2)*(n - (n**3)/8.0 - (n**5)/64.0)
        A2 = (15.0/16)*(n**2 - (n**4)/4.0)
        A3 = -(35.0/48)*(n**3 - (5.0/16)*(n**5))
        A4 = (315.0/512)*(n**4)
        A5 = -(693.0/1280)*(n**5)
        return [A0, A1, A2, A3, A4, A5]

    def makeAryBeta(n):
        beta1 = (1.0/2)*n - (2.0/3)*(n**2) + (37.0/96)*(n**3) - (1.0/360)*(n**4) - (81.0/512)*(n**5)
        beta2 = (1.0/48)*(n**2) + (1.0/15)*(n**3) - (437.0/1440)*(n**4) + (46.0/105)*(n**5)
        beta3 = (17.0/480)*(n**3) - (37.0/840)*(n**4) - (209.0/4480)*(n**5)
        beta4 = (4397.0/161280)*(n**4) - (11.0/504)*(n**5)
        beta5 = (4583.0/161280)*(n**5)
        return [math.nan, beta1, beta2, beta3, beta4, beta5]

    def makeAryDelta(n):
        delta1 = 2*n - (2.0/3)*(n**2) - 2*(n**3) + (116.0/45)*(n**4) + (26.0/45)*(n**5) - (2854.0/675)*(n**6)
        delta2 = (7.0/3)*(n**2) - (8.0/5)*(n**3) - (227.0/45)*(n**4) + (2704.0/315)*(n**5) + (2323.0/945)*(n**6)
        delta3 = (56.0/15)*(n**3) - (136.0/35)*(n**4) - (1262.0/105)*(n**5) + (73814.0/2835)*(n**6)
        delta4 = (4279.0/630)*(n**4) - (332.0/35)*(n**5) - (399572.0/14175)*(n**6)
        delta5 = (4174.0/315)*(n**5) - (144838.0/6237)*(n**6)
        delta6 = (601676.0/22275)*(n**6)
        return [math.nan, delta1, delta2, delta3, delta4, delta5, delta6]

    def calcPartOfSbar_phi0(aryA, phi0):
        res = 0.0
        for j in range(1, 5+1):
            res += aryA[j] * math.sin(2*j*phi0)
        return res

    def calcPartOfXidash(aryBeta, xi, eta):
        res = 0.0
        for j in range(1, 5+1):
            res += aryBeta[j]*math.sin(2*j*xi)*math.cosh(2*j*eta)
        return res

    def calcPartOfEtadash(aryBeta, xi, eta):
        res = 0.0
        for j in range(1, 5+1):
            res += aryBeta[j]*math.cos(2*j*xi)*math.sinh(2*j*eta)
        return res

    def calcPartOfPhi(aryDelta, chi):
        res = 0.0
        for j in range(1, 6+1):
            res += aryDelta[j]*math.sin(2*j*chi)
        return res


    # 平面直角座標系原点座標取得
    (phi0, lambda0) = getPhiLambFromKeiByRadian(japaneseKei)

    # Fからnを算出
    n = 1.0/(2*F - 1.0)

    # A, beta, delta の配列を用意
    aryA = makeAryA(n)
    aryBeta = makeAryBeta(n)
    aryDelta = makeAryDelta(n)

    # Sbar_phi0, Abar
    m0a_per_1pn = m0 * a / (1.0+n)
    Sbar_phi0 = m0a_per_1pn * (aryA[0]*phi0 + calcPartOfSbar_phi0(aryA, phi0))

    Abar = m0a_per_1pn * aryA[0]

    # ξ, η 
    xi = (x + Sbar_phi0)/Abar
    eta = (y / Abar)

    # ξ', η'
    xidash = xi - calcPartOfXidash(aryBeta, xi, eta)
    etadash = eta - calcPartOfEtadash(aryBeta, xi, eta)

    # χ
    chi = math.asin( math.sin(xidash)/math.cosh(etadash))

    # 経度緯度！ φ, λ
    phi = chi + calcPartOfPhi(aryDelta, chi)
    lambda_ = lambda0 + math.atan(math.sinh(etadash)/math.cos(xidash))

    latitude = math.degrees(phi)
    longitude = math.degrees(lambda_)

    return (latitude, longitude)


if __name__ == '__main__':
    #test
    '''
    例：我孫子市役所
    平面9系  (-15035.6705 ,17617.1597 ) ->  緯度経度 35.864320, 140.028410
      コマンド例: python3 xy2do.py -15035.6705 17617.1597 9
    '''
    if (len(sys.argv)<=3):
        print("usage: %s <X> <Y> <System(1-19)>."%sys.argv[0])
        sys.exit(-1)

    try:
        x = float(sys.argv[1])    
        y = float(sys.argv[2]) 
        kei = int(sys.argv[3])
    except ValueError:
        print("usage: %s <X> <Y>. X,Y is float number."%sys.argv[0])
        sys.exit(-1)

    # x = -15035.6705
    # y = 17617.1597
    #print(x, y, ' is ', 35.864320, 140.028410, "(Expect)")

    (lat, lon) = xy2do(x,y,9)
    #print(x, y,' to ',lat, lon, "Calced")
    print(lat, lon)
