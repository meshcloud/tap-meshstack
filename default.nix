{ pkgs ? import <nixpkgs> { } }:
let
  unstable = import <nixpkgs-unstable> { }; # need it for now, there's probably a better/cleaner way to import it 
  my-python = pkgs.python38; # matches tractor dockerfile
  python-with-my-packages =
    my-python.withPackages (p: with p; [ pip virtualenv ]);

in
pkgs.mkShell {
  NIX_SHELL = "meshBarn";
  buildInputs = [
    python-with-my-packages

  ];
  shellHook = ''
    PYTHONPATH=${python-with-my-packages}/${python-with-my-packages.sitePackages}

    echo "Welcome to tap-meshstack"
  '';
}
