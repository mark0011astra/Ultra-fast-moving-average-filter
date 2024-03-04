import numpy as np
import timeit

# 移動平均フィルタ（Pythonのみ使用）
def simple_moving_average(data, window_size):
    result = []
    for i in range(len(data) - window_size + 1):
        window = data[i:i + window_size]
        window_average = sum(window) / window_size
        result.append(window_average)
    return result
  
# Numpyの`convolve`関数を使用した移動平均フィルタ
def moving_average_filter(data, window_size):
    weights = np.ones(window_size) / window_size
    return np.convolve(data, weights, 'valid')

# Numpyの`cumsum`関数を使用した移動平均フィルタ
def fast_moving_average_filter(data, window_size):
    cumsum = np.cumsum(np.insert(data, 0, 0)) 
    return (cumsum[window_size:] - cumsum[:-window_size]) / float(window_size)
def fast_moving_average_filter(data, window_size):
    cumsum = np.cumsum(np.insert(data, 0, 0)) 
    return (cumsum[window_size:] - cumsum[:-window_size]) / float(window_size)

# 実験条件の設定と実行
experiment_conditions = [
    {"data_size": 1000, "window_size": 5},
    {"data_size": 1000, "window_size": 50},
    {"data_size": 100000, "window_size": 5},
    {"data_size": 100000, "window_size": 100}
]

for condition in experiment_conditions:
    data = np.random.rand(condition["data_size"])
    window_size = condition["window_size"]
    
    # 普通の移動平均フィルタの実行時間測定
    simple_time = timeit.timeit(lambda: simple_moving_average(data, window_size), number=3)
    
    # Numpy convolveを使用した移動平均フィルタの実行時間測定
    numpy_convolve_time = timeit.timeit(lambda: moving_average_filter(data, window_size), number=3)
    
    # Numpy cumsumを使用した移動平均フィルタの実行時間測定
    numpy_cumsum_time = timeit.timeit(lambda: fast_moving_average_filter(data, window_size), number=3)
    
    # 結果の出力（この部分は実際のコードには含まれていませんが、結果の解釈に使用されました）
    print(f"データサイズ: {condition['data_size']}, ウィンドウサイズ: {window_size}")
    print(f"普通の移動平均: {simple_time:.4f}秒, Numpy convolve: {numpy_convolve_time:.4f}秒, Numpy cumsum: {numpy_cumsum_time:.4f}秒")
