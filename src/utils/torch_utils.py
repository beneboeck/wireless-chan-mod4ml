def calculate_dim_after_convBlock(h_in, w_in, n_conv, ch_in, stride=2, padding=1, kernel_size=3, ch_increase=4):
    """calculates the flattened dimension after a convolutional block"""
    h = h_in
    w = w_in
    for _ in range(n_conv):
        h = (h + 2 * padding - kernel_size) // stride + 1
        w = (w + 2 * padding - kernel_size) // stride + 1
    ch_out = ch_in * ch_increase**n_conv
    return h, w, ch_out