import numpy as np
import pcl


def best_fit_transform(A, B):
    '''
    Calculates the least-squares best-fit transform between corresponding 3D points A->B
    Input:
      A: Nx3 numpy array of corresponding 3D points
      B: Nx3 numpy array of corresponding 3D points
    Returns:
      T: 4x4 homogeneous transformation matrix
      R: 3x3 rotation matrix
      t: 3x1 column vector
    '''

    assert len(A) == len(B)

    # translate points to their centroids
    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)
    AA = A - centroid_A
    BB = B - centroid_B

    # rotation matrix
    W = np.dot(BB.T, AA)
    U, s, VT = np.linalg.svd(W)
    R = np.dot(U, VT)

    # special reflection case
    if np.linalg.det(R) < 0:
        VT[2, :] *= -1
        R = np.dot(U, VT)

    # translation
    t = centroid_B.T - np.dot(R, centroid_A.T)

    # homogeneous transformation
    T = np.identity(4)
    T[0:3, 0:3] = R
    T[0:3, 3] = t

    return T, R, t


def nearest_neighbor(src, dst):
    '''
    Find the nearest (Euclidean) neighbor in dst for each point in src
    Input:
        src: Nx3 array of points
        dst: Nx3 array of points
    Output:
        distances: Euclidean distances (errors) of the nearest neighbor
        indecies: dst indecies of the nearest neighbor
    '''

    indecies = np.zeros(src.shape[0], dtype=np.int)
    distances = np.zeros(src.shape[0])
    for i, s in enumerate(src):
        min_dist = np.inf
        for j, d in enumerate(dst):
            dist = np.linalg.norm(s - d)
            if dist < min_dist:
                min_dist = dist
                indecies[i] = j
                distances[i] = dist
    return distances, indecies


def icp(A, B, init_pose=None, max_iterations=50, tolerance=0.001):
    '''
    The Iterative Closest Point method
    Input:
        A: Nx3 numpy array of source 3D points
        B: Nx3 numpy array of destination 3D point
        init_pose: 4x4 homogeneous transformation
        max_iterations: exit algorithm after max_iterations
        tolerance: convergence criteria
    Output:
        T: final homogeneous transformation
        distances: Euclidean distances (errors) of the nearest neighbor
    '''

    # make points homogeneous, copy them so as to maintain the originals
    src = np.ones((4, A.shape[0]))
    dst = np.ones((4, B.shape[0]))
    src[0:3, :] = np.copy(A.T)
    dst[0:3, :] = np.copy(B.T)

    # apply the initial pose estimation
    if init_pose is not None:
        src = np.dot(init_pose, src)

    prev_error = 0

    for i in range(max_iterations):
        # find the nearest neighbours between the current source and destination points
        distances, indices = nearest_neighbor(src[0:3, :].T, dst[0:3, :].T)

        # compute the transformation between the current source and nearest destination points
        T, _, _ = best_fit_transform(src[0:3, :].T, dst[0:3, indices].T)

        # update the current source
        # refer to "Introduction to Robotics" Chapter2 P28. Spatial description and transformations
        src = np.dot(T, src)

        # check error
        mean_error = np.sum(distances) / distances.size
        if abs(prev_error - mean_error) < tolerance:
            break
        prev_error = mean_error

    # calculcate final tranformation
    T, _, _ = best_fit_transform(A, src[0:3, :].T)

    return T, distances


if __name__ == "__main__":
    C = pcl.load('/home/fred/Documents/task00/shanghai/pcd/20181007.pcd')
    shapeC = (C.size, 3)
    row = 0
    pointsC = np.zeros(shapeC, dtype=np.float32)
    for i in range(0, C.size):
        x = C[i][0]
        y = C[i][1]
        z = C[i][2]

        pointsC[row][0] = x
        pointsC[row][1] = y
        pointsC[row][2] = z
        row += 1

    print(pointsC)

    D = pcl.load('/home/fred/Documents/task00/shanghai/pcd/2018100800.pcd')
    shapeD = (D.size, 3)
    row = 0
    pointsD = np.zeros(shapeD, dtype=np.float32)
    for i in range(0, D.size):
        x = D[i][0]
        y = D[i][1]
        z = D[i][2]

        pointsD[row][0] = x
        pointsD[row][1] = y
        pointsD[row][2] = z
        row += 1

    print(pointsD)

    T, distances = icp(pointsC, pointsD)

    np.set_printoptions(precision=3, suppress=True)
    print T
