from cx_Freeze import setup, Executable

exe = Executable(
    script="summas.py",
    base="Win32GUI",
)

setup(
    name = "wxSampleApp",
    version = "0.1",
    description = "summas",
    executables = [exe]
)
