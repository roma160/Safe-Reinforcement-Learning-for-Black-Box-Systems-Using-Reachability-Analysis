# Install pip install imgui[full] on the PC before running

import os
import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer
import numpy as np
import time
import math
import threading
import socket
from common_state import DonkeyState


state = DonkeyState(0, 0, 0)

class Server():
	def __init__(self):
		self.running = False
		self.thread = threading.Thread(target=self._loop)

	def start(self):
		self.running = True
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.server_socket.bind(('', 12000))
		self.server_socket.settimeout(0.5)
		print("Starting server at:", self.server_socket.getsockname())
		self.thread.start()
	
	def join(self):
		self.running = False
		self.thread.join()

	def _loop(self):
		global state
		print("Server is running", self.running)
		while self.running:
			try:
				message, address = self.server_socket.recvfrom(1024)
			except socket.timeout:
				continue
			state = DonkeyState.load(message)

# https://github.com/pyimgui/pyimgui/blob/723022d87de8040d1c4a66f53288dcfd7d2274d3/doc/examples/plots.py#L67C1-L91C18
def impl_glfw_init():
	width, height = 1280, 720
	window_name = "minimal ImGui/GLFW3 example"

	if not glfw.init():
		print("Could not initialize OpenGL context")
		sys.exit(1)

	# OS X supports only forward-compatible core profiles from 3.2
	glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
	glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
	glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

	glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

	# Create a windowed mode window and its OpenGL context
	window = glfw.create_window(int(width), int(height), window_name, None, None)
	glfw.make_context_current(window)

	if not window:
		glfw.terminate()
		print("Could not initialize Window")
		sys.exit(1)

	return window

def main():
	window = impl_glfw_init()
	imgui.create_context()
	impl = GlfwRenderer(window)

	server = Server()
	server.start()

	while not glfw.window_should_close(window):
		glfw.poll_events()
		impl.process_inputs()

		imgui.new_frame()
		loop()

		gl.glClearColor(1.0, 1.0, 1.0, 1)
		gl.glClear(gl.GL_COLOR_BUFFER_BIT)

		imgui.render()
		impl.render(imgui.get_draw_data())
		glfw.swap_buffers(window)

	server.join()
	impl.shutdown()
	glfw.terminate()


folder_name = os.path.dirname(os.path.abspath(__file__))
map = np.loadtxt(os.path.join(folder_name, "car.csv"), delimiter=",", dtype=int)

def loop():
	imgui.set_next_window_size_constraints(
		(0, 0), (imgui.FLOAT_MAX, imgui.FLOAT_MAX),
		callback = lambda data: setattr(data, "desired_size", (max(data.desired_size.x, data.desired_size.y),) * 2)
	)
	imgui.begin("Data from the Donkey")
	imgui.set_window_size(500, 500)

	window_size = imgui.get_window_size()
	l_x, l_y = map.shape
	cx, cy = imgui.get_cursor_screen_pos()
	height = window_size.y - 40
	dx, dy = (window_size.x - 15) / l_x, (height) / l_y

	pixel_size = 0.5
	car_radius = 25

	draw_list = imgui.get_window_draw_list()
	for i in range(map.shape[0]):
		for j in range(map.shape[1]):
			if map[i][j] == 1:
				draw_list.add_rect_filled(
					cx + (i) * dx, cy + (l_y - j) * dy,
					cx + (i + 1) * dx, cy + (l_y - j - 1) * dy,
					imgui.get_color_u32_rgba(1.0, 1.0, 1.0, 1.0)
				)
	
	draw_list.add_circle(
		cx + (state.x) * dx / pixel_size, cy + height - (state.y) * dy / pixel_size,
		car_radius, imgui.get_color_u32_rgba(1.0, 0.0, 0.0, 1.0)
	)
	draw_list.add_line(
		cx + (state.x) * dx / pixel_size, cy + height - (state.y) * dy / pixel_size,
		cx + (state.x + 1.2 * car_radius * math.cos(state.angle)) * dx / pixel_size,
		cy + height - (state.y + 1.2 * car_radius * math.sin(state.angle)) * dy / pixel_size,
		imgui.get_color_u32_rgba(0.0, 1.0, 0.0, 1.0)
	)

	imgui.end()

	imgui.begin("State view")
	imgui.text(f"X: {state.x} Y: {state.y} Angle: {state.angle}")
	imgui.text(f"Render position: {cx + (state.x) * dx / pixel_size}, {cy + height - (state.y) * dy / pixel_size}")
	imgui.end()

if __name__ == "__main__":
	main()