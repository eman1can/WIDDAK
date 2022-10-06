import numpy as np
import open3d as o3d

file_name = 'output.ply'

vis = o3d.visualization.Visualizer()
vis.create_window()
vis.add_geometry(o3d.io.read_triangle_mesh(file_name))
vis.get_render_option().background_color = np.asarray([0, 0, 0])
vis.get_view_control().rotate(120, 60)
vis.run()
vis.destroy_window()
