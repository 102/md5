from hash import MD5

hex_bin_map = {'0': '0000', '1': '0001', '2': '0010', '3': '0011',
               '4': '0100', '5': '0101', '6': '0110', '7': '0111',
               '8': '1000', '9': '1001', 'a': '1010', 'b': '1011',
               'c': '1100', 'd': '1101', 'e': '1110', 'f': '1111'}

regimes = [['f', 'g', 'h', 'k'],
           ['g', 'h', 'f', 'k'],
           ['h', 'k', 'f', 'g'],
           ['k', 'f', 'g', 'h']]


strings = ['aaaaa', 'aaaab', 'aaaba', 'aabaa', 'abaaa', 'baaaa']


def hex_to_bin(a):
    return ''.join(hex_bin_map[c] for c in a)


def hamming_distance(a, b):
    return sum(1 if q != w else 0 for q, w in zip(hex_to_bin(a), hex_to_bin(b)))


for regime in regimes:
    hash_creator = MD5(order=regime)
    row = []
    for string in strings:
        row.append(hash_creator.md5(string))

    distances = []
    for i in row:
        r = []
        for j in row:
            if not i == j:
                r.append(hamming_distance(i, j))
        distances.append(r)

    mr = sum(j for j in (sum(i) for i in distances))/30

    r = []
    for i in distances:
        r.append(((mr - sum(i))**2)/30)
    r = sum(r) ** 0.5

    print(regime)
    for distance in distances:
        print(distance)
    print('mr={0}'.format(mr))
    print('r={0}'.format(r))
    print()
