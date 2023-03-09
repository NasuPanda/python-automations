"""ファイル入出力"""

import open3d as o3d


def read_point_cloud(filepath: str) -> o3d.geometry.PointCloud:
    """点群読み込み"""
    return o3d.io.read_point_cloud(filepath)


def write_point_cloud(filepath: str, pcd):
    """点群書き込み"""
    o3d.io.write_point_cloud(filepath, pcd)
    print(f"Written file: {filepath}\tPointCloud: {pcd}")


def read_mesh(filepath: str):
    """メッシュ読み込み"""
    return o3d.io.read_triangle_mesh(filepath)


def write_mesh(filepath: str, mesh):
    """メッシュ書き込み"""
    o3d.io.write_triangle_mesh(filepath, mesh)
    print(f"Written file: {filepath}\nMesh: {mesh}")


def ply_to_stl(in_ply_path: str, out_stl_path: str) -> None:
    """ply => stl"""
    mesh = o3d.io.read_triangle_mesh(in_ply_path)
    # 三角形の法線を計算(STL出力の場合必須)
    mesh = o3d.geometry.TriangleMesh.compute_triangle_normals(mesh)
    print("Mesh:", mesh)
    o3d.io.write_triangle_mesh(out_stl_path, mesh)
    print(f"Save {out_stl_path} completed.")


def pcd_to_ply(in_pcd_path: str, out_ply_path: str) -> None:
    """pcd => ply"""
    pcd = o3d.io.read_point_cloud(in_pcd_path)
    o3d.io.write_point_cloud(out_ply_path, pcd)
