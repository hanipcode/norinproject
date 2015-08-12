from distutils.core import setup
import py2exe 

setup( 
  options = {         
    'py2exe' : {
        'compressed': 2,
        'optimize': 2,
        'bundle_files': 3, #Options 1 & 2 do not work on a 64bit system
        'dist_dir': 'dist',  # Put .exe in dist/
        'xref': False,
        'skip_archive': False,
        'ascii': True,
        }
        },
  windows = [{
		"script":"main_int.py",
		"icon_resources": [(1, "norin.ico")],
		"dest_base":"main_int"
  }]
)