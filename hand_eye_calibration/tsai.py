#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/07/12 21:34
# @Author  : ww
# @FileName: tsai.py
# @Software: PyCharm

import transforms3d as tfs
import numpy as np
import math

np.set_printoptions(suppress=True)


def get_matrix_eular_radu(x, y, z, rx, ry, rz):
    rmat = tfs.euler.euler2mat(math.radians(rx), math.radians(ry), math.radians(rz))
    rmat = tfs.affines.compose(np.squeeze(np.asarray((x, y, z))), rmat, [1, 1, 1])
    return rmat


def skew(v):
    return np.array([[0, -v[2], v[1]],
                     [v[2], 0, -v[0]],
                     [-v[1], v[0], 0]])


def rot2quat_minimal(m):
    quat = tfs.quaternions.mat2quat(m[0:3, 0:3])
    return quat[1:]


def quatMinimal2rot(q):
    p = np.dot(q.T, q)
    w = np.sqrt(np.subtract(1, p[0][0]))
    return tfs.quaternions.quat2mat([w, q[0], q[1], q[2]])


# 参数顺序：x,y,z,rx,ry,rz
# 注意单位：mm 和 °
# 下面例子是走了8个点位，有8组数据，hand 是示教器读取出来的，camera是相机解算出来的。


hand = [308.67, -457.69, -223.26, 176.69, -2.3, 152.07,
        231.46, -585.94, -226.36, 179.39, 0.43, -115.02,
        265.27, -598.9, -195.61, 162.4, -6.63, -115.57,
        142.01, -612.69, -191.12, -176.15, 11.9, -117.75,
        282.89, -514.64, -121.19, 161.36, -9.71, 152.56,
        358.97, -540.68, -118.64, 175.48, -18.38, 166.51,
        349.1, -536.98, -111.67, 161.09, 8.75, 161.47,
        166.3, -494.47, -150.81, 174.75, 17.11, 165.08]

camera = [-34.022015, -90.6645, 595.9659, 5.475858166007529, -2.2591752344658085, -5.693059793426721,
          12.908683, -0.91019094, 605.1342, 0.15830325279021293, -0.5779854796907787, 87.48088571334634,
          -6.920392, -101.960464, 596.4481, 0.21667154310131914, -19.97065667229419, 86.05302665557336,
          42.457134, -23.295813, 658.16644, 9.271483971640496, 8.45089107768745, 85.02331441590775,
          -74.774155, -177.04884, 641.47687, 21.736087930074234, -2.350569667168675, -6.798426951903581,
          -93.244095, -66.59615, 687.0854, 8.62280432820663, -19.164881824708623, 6.994208530984782,
          163.74376, -113.10099, 658.121, 16.92341045564796, 12.310612710890956, 7.273645561748227,
          19.60516, -33.712517, 700.6987, 1.8015999943187166, 17.03602643644007, 8.49126115511029]


def isRotationMatrix(R):
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype=R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6


def getPose_fromT(T):
    x = T[0, 3]
    y = T[1, 3]
    z = T[2, 3]

    R = T[:3, :3]
    assert (isRotationMatrix(R))

    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        rx = math.atan2(R[2, 1], R[2, 2])
        ry = math.atan2(-R[2, 0], sy)
        rz = math.atan2(R[1, 0], R[0, 0])
    else:
        rx = math.atan2(-R[1, 2], R[1, 1])
        ry = math.atan2(-R[2, 0], sy)
        rz = 0

    return x, y, z, rx, ry, rz


if __name__ == '__main__':
    Hgs, Hcs = [], []
    for i in range(0, len(hand), 6):
        Hgs.append(get_matrix_eular_radu(hand[i], hand[i + 1], hand[i + 2], hand[i + 3], hand[i + 4], hand[i + 5]))
        Hcs.append(
            get_matrix_eular_radu(camera[i], camera[i + 1], camera[i + 2], camera[i + 3], camera[i + 4], camera[i + 5]))

    Hgijs = []
    Hcijs = []
    A = []
    B = []
    size = 0
    for i in range(len(Hgs)):
        for j in range(i + 1, len(Hgs)):
            size += 1
            Hgij = np.dot(np.linalg.inv(Hgs[j]), Hgs[i])
            Hgijs.append(Hgij)
            Pgij = np.dot(2, rot2quat_minimal(Hgij))

            Hcij = np.dot(Hcs[j], np.linalg.inv(Hcs[i]))
            Hcijs.append(Hcij)
            Pcij = np.dot(2, rot2quat_minimal(Hcij))

            A.append(skew(np.add(Pgij, Pcij)))
            B.append(np.subtract(Pcij, Pgij))
    MA = np.asarray(A).reshape(size * 3, 3)
    MB = np.asarray(B).reshape(size * 3, 1)
    Pcg_ = np.dot(np.linalg.pinv(MA), MB)
    pcg_norm = np.dot(np.conjugate(Pcg_).T, Pcg_)
    Pcg = np.sqrt(np.add(1, np.dot(Pcg_.T, Pcg_)))
    Pcg = np.dot(np.dot(2, Pcg_), np.linalg.inv(Pcg))
    Rcg = quatMinimal2rot(np.divide(Pcg, 2)).reshape(3, 3)

    A = []
    B = []
    id = 0
    for i in range(len(Hgs)):
        for j in range(i + 1, len(Hgs)):
            Hgij = Hgijs[id]
            Hcij = Hcijs[id]
            A.append(np.subtract(Hgij[0:3, 0:3], np.eye(3, 3)))
            B.append(np.subtract(np.dot(Rcg, Hcij[0:3, 3:4]), Hgij[0:3, 3:4]))
            id += 1

    MA = np.asarray(A).reshape(size * 3, 3)
    MB = np.asarray(B).reshape(size * 3, 1)
    Tcg = np.dot(np.linalg.pinv(MA), MB).reshape(3, )

    result = tfs.affines.compose(Tcg, np.squeeze(Rcg), [1, 1, 1])
    print(result)

    x, y, z, rx, ry, rz = getPose_fromT(result)
    # print(result, type(result), result.shape)
    print(x, y, z, rx * 57.3, ry * 57.3, rz * 57.3)

    print(math.sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2)))
