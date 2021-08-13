N = int(input())
A = [list(map(int, input().split())) for i in range(N)]
suma = 0
NM = []
for i in range(N):
    for j in range(N):
        NM.append(A[i][j])
        suma += A[i][j]
        LNM = len(NM)
        x = suma//LNM
for i in range(N):
    for j in range(N):
        if A[i][j] < x:
            A[i][j] = 0
        else:
            A[i][j] = 255
for i in range(len(A)):
    for j in range(len(A[i])):
        print(A[i][j], end = '')
    print()