# open3Dによるメッシュ化

詳細: [Open3Dによるメッシュ化 - デバイス実証課 Wiki](https://wiki.m-dev.denso.co.jp/user/SHUNJI%20NISHIGAKI/%E3%83%A1%E3%83%83%E3%82%B7%E3%83%A5%E5%8C%96/Open3D%E3%81%AB%E3%82%88%E3%82%8B%E3%83%A1%E3%83%83%E3%82%B7%E3%83%A5%E5%8C%96)

## スクリプトの説明

- `main.py` : LiDsEYE✕SLAMデータに対して前処理→法線付与→メッシュ化という一連の処理を行う。メッシュ化の流れを掴むために
- `meshing_sample.py` : 綺麗な点群のサンプル([The Stanford 3D Scanning Repository](http://graphics.stanford.edu/data/3Dscanrep/))をメッシュ化
- `meshing_rectangular_by_container.py` : SORC(立方体)のメッシュ化。法線付与を自力で行っているので、法線ベクトルへの理解を深めるために
- `meshing_CDRmap.py` : CDRの部屋をメッシュ化したい・・・

## モジュールの説明

```sh
$ tree ./src -L 2

./src
├── common                      # 共通処理
            FIXME: 名前が良くない
│   ├── converter.py              # Open3D⇔Numpy, 点群結合, ROS座標系からの変換
│   ├── display.py                # オブジェクトの表示, 外れ値の表示
│   ├── file_io.py                # I/O
│   ├── getter.py                 # 値の取得 points, xyz, 点間最短距離の平均値など
│   └── rgb.py                    # RGB
├── filter                      # フィルタリング関連 
│   ├── crop.py                   # 点群やメッシュなどを切り出す処理
│   ├── distance.py               # 距離によるフィルタリング
│   ├── down_sample.py            # ダウンサンプリング
│   ├── outlier.py                # 外れ値
            FIXME 場所が適切でない
│   ├── plane_segmentation.py     # セグメンテーション(平面検出)
│   └── rgb_filter.py             # RGB値によるフィルタリング
└── mesh                        # メッシュ
    ├── meshing.py                 # メッシュ化アルゴリズムの呼び出し 
    ├── normal.py                  # 法線の付与
    └── smoother.py                # スムージング
```