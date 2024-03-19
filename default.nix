{ pkgs ? import <nixpkgs> { } }:
let
  my-python = pkgs.python310; 
  python-with-my-packages =
    my-python.withPackages (p: with p; [ tox ]);
in

pkgs.mkShell {
  NIX_SHELL = "tap-meshstack";
  buildInputs = [
    pkgs.jq
    pkgs.poetry
    python-with-my-packages
  ];
  shellHook = ''
    PYTHONPATH=${python-with-my-packages}/${python-with-my-packages.sitePackages}
  '';
}
