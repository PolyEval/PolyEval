let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-23.11";
  pkgs = import nixpkgs { config = {}; overlays = []; };
  executionEnv = import ./execution-templates/shell.nix ;
in
pkgs.mkShell.override { stdenv = executionEnv.stdenv; } {
  packages = [
    pkgs.git
    pkgs.cacert
    pkgs.python3
    pkgs.pdm
  ] ++ executionEnv.buildInputs;
}