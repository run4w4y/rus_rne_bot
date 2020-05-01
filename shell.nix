{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
    name = "rus_rne_bot";

    buildInputs = with pkgs; [
        git
        libffi
        (python3.withPackages ( p: 
            with p; [ pip ]
        ))
    ];

    shellHook = ''
        export TERM=xterm-256color
        alias pip="PIP_PREFIX='$(pwd)/_build/pip_packages' \pip"
        export PYTHONPATH="$(pwd)/_build/pip_packages/lib/python3.7/site-packages:$(pwd)/_build/pip_packages/bin:$PYTHONPATH"
        unset SOURCE_DATE_EPOCH
    '';
}