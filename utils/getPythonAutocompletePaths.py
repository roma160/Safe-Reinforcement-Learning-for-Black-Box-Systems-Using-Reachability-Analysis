import os
import subprocess

def main():
	WORKSPACE_FOLDER = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
	DISTRO = os.path.join(WORKSPACE_FOLDER, "catkin_ws", "devel", "setup.bash")
	if not os.path.exists(DISTRO):
		print(f"Error: No '{DISTRO=}' file found in the catkin workspace")
		return
	
	# https://github.com/ajshort/vscode-ros/pull/11/files
	proc = subprocess.run(
		f"source {DISTRO} ; rospack list",
		executable="/bin/bash",
		shell=True, text=True,
		stdout=subprocess.PIPE
	)
	for line in proc.stdout.splitlines():
		pkg, path = line.split(" ", 1)
		
		"""
		const pkg_name = pkg.substring(pkg.lastIndexOf("/")+1);
        const pkg_path = path.join(pkg, "src");

        return pfs.exists( path.join(pkg_path, pkg_name, "__init__.py")).then(exists => {
            if (exists) {
                pathon_paths.push(pkg_path);
            }
        });
		"""
		pkg_name = os.path.basename(pkg)
		pkg_path = os.path.join(path, "src")
		if os.path.exists(os.path.join(pkg_path, pkg_name, "__init__.py")):
			print(pkg_path)

if __name__ == "__main__":
	main()
