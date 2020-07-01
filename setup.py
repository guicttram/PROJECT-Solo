import cx_Freeze

executables = [cx_Freeze.Executable(script='solo.py', icon='stars/solo.ico')]
cx_Freeze.setup(
    name = 'PROJECT: Solo',
    options = {'build_exe': {'packages':['pygame', 'functions'],
    'include_files': ['stars']
    } },
    executables = executables
)
