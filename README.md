# 移動平均フィルタの性能比較

異なる条件下での移動平均フィルタの実装方法による性能比較を行います。検証実験では、以下の3種類の実装方法を比較しました：

- 移動平均フィルタ（Pythonのみ使用）
- Numpyの`convolve`関数を使用した移動平均フィルタ
- Numpyの`cumsum`関数を使用した移動平均フィルタ

## `convolve`関数

`convolve`関数は、二つの配列の畳み込みを計算します。この関数は、信号処理でフィルタリングを行う場合などに有用です。移動平均フィルタを計算する際には、データ配列と、移動平均のウィンドウサイズに対応する重み配列を畳み込むことで使用されます。

### 使用方法

```python
import numpy as np

data = np.array([1, 2, 3, 4, 5])  # 処理するデータ
window_size = 3  # 移動平均のウィンドウサイズ

# ウィンドウサイズに対応する重み配列を作成
weights = np.ones(window_size) / window_size

# 畳み込みを使用して移動平均を計算
moving_average = np.convolve(data, weights, 'valid')
```

### `convolve`関数の特徴

- `valid`モードでは、出力サイズは入力サイズよりも小さくなります。これは、畳み込みが完全に重なる部分のみを計算するためです。
- 計算速度が非常に速く、特にNumpyの内部最適化により大規模なデータセットに対して効率的です。

## `cumsum`関数

`cumsum`関数は、配列の累積和を計算します。移動平均フィルタにおいては、累積和を利用して効率的に平均値を計算することができます。

### 使用方法

```python
import numpy as np

data = np.array([1, 2, 3, 4, 5])  # 処理するデータ
window_size = 3  # 移動平均のウィンドウサイズ

# データの累積和を計算
cumulative_sum = np.cumsum(np.insert(data, 0, 0))

# 累積和を使用して移動平均を計算
moving_average = (cumulative_sum[window_size:] - cumulative_sum[:-window_size]) / window_size
```

### `cumsum`関数の特徴

- 大規模なデータセットや大きなウィンドウサイズでの計算に非常に効率的です。
- `cumsum`を使用することで、計算の複雑さを大幅に削減し、計算速度を向上させることができます。
- 累積和を利用することで、連続するデータポイント間の平均値を繰り返し計算する必要がなくなります。

## 移動平均フィルタの実装

### 移動平均フィルタ（Pythonのみ使用）

```python
def simple_moving_average(data, window_size):
    result = []
    for i in range(len(data) - window_size + 1):
        window = data[i:i + window_size]
        window_average = sum(window) / window_size
        result.append(window_average)
    return result
```

### Numpyの`convolve`関数を使用した移動平均フィルタ

```python
import numpy as np

def moving_average_filter(data, window_size):
    weights = np.ones(window_size) / window_size
    return np.convolve(data, weights, 'valid')
```

### Numpyの`cumsum`関数を使用した移動平均フィルタ

```python
def fast_moving_average_filter(data, window_size):
    cumsum = np.cumsum(np.insert(data, 0, 0)) 
    return (cumsum[window_size:] - cumsum[:-window_size]) / float(window_size)
```


## 実験結果

以下の表に、各条件下での実装方法ごとの実行時間（秒）と、性能差（倍速）を示します。

| 条件 | 実装方法 | 実行時間（秒） | 性能差（倍速） |
| --- | --- | ---: | ---: |
| 小規模データセット（1,000点）, 小窓（5点） | 移動平均 | 0.0107 | - |
|  | Numpy `convolve` | 0.0003 | 40.85倍高速 |
|  | Numpy `cumsum` | 0.0002 | 53.69倍高速 |
| 小規模データセット（1,000点）, 大窓（50点） | 移動平均 | 0.0713 | - |
|  | Numpy `convolve` | 0.0003 | 229.72倍高速 |
|  | Numpy `cumsum` | 0.0003 | 263.22倍高速 |
| 大規模データセット（100,000点）, 小窓（5点） | 移動平均 | 2.5931 | - |
|  | Numpy `convolve` | 0.0010 | 2530.90倍高速 |
|  | Numpy `cumsum` | 0.0093 | 277.87倍高速 |
| 大規模データセット（100,000点）, 大窓（100点） | 移動平均 | 12.1863 | - |
|  | Numpy `convolve` | 0.0225 | 542.14倍高速 |
|  | Numpy `cumsum` | 0.0053 | 2306.86倍高速 |


## `cumsum`関数を使用すると、Python上での移動平均フィルタ処理が数千倍高速になる場合があることが示されました。

