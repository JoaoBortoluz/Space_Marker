import cx_Freeze
executables = [
    cx_Freeze.Executable(script="main.py", icon="icone.ico")
]
cx_Freeze.setup(
    name = "SPACE MARKER",
    options={
        "build_exe":{
            "packages":["pygame"],
            "include_files":["space.png",
                             "icone.png",
                             "musica_espaço.mp3"
                             ]
        }
    }, executables = executables
)
#rodar apenas pelo terminal
#py geraSetup.py build = pasta
#py geraSetup.py bdist_msi = microsoft installer