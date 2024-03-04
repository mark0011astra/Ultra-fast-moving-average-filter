# 移動平均フィルタの性能比較

異なる条件下での移動平均フィルタの実装方法による性能比較を行います。検証実験では、以下の3種類の実装方法を比較しました：

- 移動平均フィルタ（Pythonのみ使用）
- Numpyの`convolve`関数を使用した移動平均フィルタ
- Numpyの`cumsum`関数を使用した移動平均フィルタ

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

