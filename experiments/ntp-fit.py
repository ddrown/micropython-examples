def simple_linear_regression(x, y):
    x_mean = sum(x) / float(len(x))
    y_mean = sum(y) / float(len(y))
    x_var = 0
    y_var = 0
    for i in range(0, len(x)):
        x_diff = x[i] - x_mean
        x_var += x_diff ** 2
        y_var += (x_diff) * (y[i] - y_mean)
    beta = y_var / x_var
    alpha = y_mean - beta * x_mean
    return (beta, alpha)

def timestamps_regression(timestamps):
    x = []
    y = []
    for i in range(0, len(timestamps)):
        s = timestamps[i][0] - timestamps[0][0]
        # micropython floats have around 6 digits of precision?
        n = s * 1000 + int(timestamps[i][1] - timestamps[0][1])
        x.append(n)
        d = n - timestamps[i][3] + timestamps[0][3]
        y.append(d)
    return simple_linear_regression(x, y)

def print_timestamps(timestamps):
    fit = timestamps_regression(timestamps)
    print(fit)

    for i in range(1, len(timestamps)):
        s = timestamps[i][0] - timestamps[0][0]
        ntp_change = s * 1000 + int(timestamps[i][1] - timestamps[0][1])
        local_change = timestamps[i][3] - timestamps[0][3]
        rtt = timestamps[i][3] - timestamps[i][2]
        d = ntp_change - local_change
        var = ntp_change * fit[0] + fit[1]
        d_var = var - d
        print(f"d {d} r {rtt} n {ntp_change} l {local_change} v {d_var}")

timestamps = [
    (1732244562, 649.931, 17675235, 17675253),
    (1732245004, 929.3588, 18117514, 18117531),
    (1732245273, 119.2846, 18385709, 18385720),
    (1732245346, 705.8622, 18459299, 18459305),
    (1732245602, 737.3245, 18715320, 18715337),
    (1732245858, 765.5577, 18971355, 18971363),
    (1732246114, 794.2702, 19227383, 19227390),
    (1732246370, 822.7165, 19483410, 19483418),
    (1732246626, 851.5998, 19739434, 19739445),
    (1732246882, 880.5934, 19995462, 19995473),
    (1732247138, 907.5654, 20251488, 20251499),
    (1732247394, 936.7784, 20507516, 20507528),
    (1732247650, 964.273, 20763545, 20763553),
    (1732247906, 990.0089, 21019569, 21019578),
    (1732248163, 14.01193, 21275593, 21275601),
    (1732248419, 39.16728, 21531616, 21531625),
    (1732248675, 65.89685, 21787644, 21787650),
    (1732248931, 92.86702, 22043667, 22043676),
    (1732249187, 116.4418, 22299691, 22299698),
    (1732249443, 145.4836, 22555719, 22555728),
    (1732249699, 174.8461, 22811745, 22811755),
    (1732249955, 198.7575, 23067770, 23067777),
    (1732250211, 222.3273, 23323792, 23323800),
    (1732250467, 247.8019, 23579816, 23579832),
    (1732250723, 277.9221, 23835846, 23835853),
    (1732250979, 305.5539, 24091870, 24091879),
    (1732251235, 332.0592, 24347895, 24347905),
    (1732251491, 357.7855, 24603921, 24603929),
    (1732251747, 384.3183, 24859946, 24859954),
    (1732252003, 407.5433, 25115970, 25115977),
    (1732252259, 432.3918, 25371991, 25372000),
    (1732252515, 462.2187, 25628017, 25628029),
    (1732252771, 488.2994, 25884046, 25884054),
]
print_timestamps(timestamps)