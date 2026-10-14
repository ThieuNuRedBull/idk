N = 208
ROUNDS = 32


def transform(bits):
    for _ in range(ROUNDS):
        nxt = [0] * N

        for i in range(N):
            nxt[i] = (
                bits[(i - 1) % N] ^
                bits[(i + 1) % N]
            )

        bits = nxt

    return bits


def bytes_to_bits(data):
    bits = []

    for b in data:
        for j in range(7, -1, -1):
            bits.append((b >> j) & 1)

    return bits


def bits_to_bytes(bits):
    ans = bytearray()

    for i in range(0, N, 8):
        x = 0

        for j in range(8):
            x = (x << 1) | bits[i + j]

        ans.append(x)

    return bytes(ans)


# --------------------------------------------------
# Tạo ma trận của phép biến đổi 32 vòng
# --------------------------------------------------

# column[i] = kết quả khi input chỉ có bit i = 1
columns = []

for i in range(N):
    bits = [0] * N
    bits[i] = 1

    result = transform(bits)
    columns.append(result)


# --------------------------------------------------
# Gaussian elimination trên GF(2)
# --------------------------------------------------

def solve(target):
    # Mỗi hàng:
    #   208 bit đầu = hệ số
    #   bit 208     = vế phải
    #
    # equation:
    #   A*x = target

    equations = []

    for row in range(N):
        equation = 0

        for col in range(N):
            if columns[col][row]:
                equation ^= 1 << col

        if target[row]:
            equation |= 1 << N

        equations.append(equation)

    pivot_row = 0
    pivot_cols = []

    for col in range(N):

        # tìm pivot
        pivot = -1

        for r in range(pivot_row, N):
            if (equations[r] >> col) & 1:
                pivot = r
                break

        if pivot == -1:
            continue

        equations[pivot_row], equations[pivot] = \
            equations[pivot], equations[pivot_row]

        # eliminate tất cả hàng khác
        for r in range(N):
            if r != pivot_row and ((equations[r] >> col) & 1):
                equations[r] ^= equations[pivot_row]

        pivot_cols.append(col)
        pivot_row += 1

        if pivot_row == N:
            break

    # kiểm tra vô nghiệm
    for r in range(pivot_row, N):
        lhs = equations[r] & ((1 << N) - 1)
        rhs = (equations[r] >> N) & 1

        if lhs == 0 and rhs:
            return None

    # chọn các free variable = 0
    solution = 0

    for r, col in enumerate(pivot_cols):
        rhs = (equations[r] >> N) & 1

        if rhs:
            solution |= 1 << col

    bits = [
        (solution >> i) & 1
        for i in range(N)
    ]

    return bits


# --------------------------------------------------
# MAIN
# --------------------------------------------------

# Thay bằng 26 byte output mà binary yêu cầu
target = "652b481a7c203a240b244f045b365f090016050e58227d270b37"

//assert len(target) == 26

target_bits = bytes_to_bits(target)

input_bits = solve(target_bits)

if input_bits is None:
    print("Không tồn tại input!")
else:
    answer = bits_to_bytes(input_bits)

    print("INPUT:")
    print(answer)

    print("\nHEX:")
    print(answer.hex())

    print("\nCHECK:")
    print(bits_to_bytes(transform(input_bits)))