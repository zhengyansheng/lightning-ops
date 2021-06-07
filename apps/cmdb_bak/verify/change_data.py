from dictdiffer import diff, patch, swap, revert
print(1111111)


d1 = {
    "hostname": "ops111",
    "ip": "1.1.1.11",
    "xx": "tt"
}

d2 = {
    "hostname": "ops3",
    "ip": "1.1.1.1",
    "app": "nginx"
}

res = diff(d1, d2)
print(res.__dict__)