# open3Dによるメッシュ化

## スクリプトの説明

- `meshing_sample.py` : 綺麗な点群のサンプル([The Stanford 3D Scanning Repository](http://graphics.stanford.edu/data/3Dscanrep/))をメッシュ化
- `meshing_rectangular_by_container.py` : 立方体のメッシュ化。法線付与を自力で行っているので、法線ベクトルへの理解を深めるために

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
            FIXME 場所が微妙
│   ├── plane_segmentation.py     # セグメンテーション(平面検出)
│   └── rgb_filter.py             # RGB値によるフィルタリング
└── mesh                        # メッシュ
    ├── meshing.py                 # メッシュ化アルゴリズムの呼び出し
    ├── normal.py                  # 法線の付与
    └── smoother.py                # スムージング
```
