{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    nixpkgs-python.url = "github:cachix/nixpkgs-python";
  };

  outputs = { self, nixpkgs, nixpkgs-python }:
  let
    pkgs = nixpkgs.legacyPackages.x86_64-linux;
    pkg-py = nixpkgs-python.packages.x86_64-linux;
  in
  {

    # packages.x86_64-linux.hello = pkgs.hello;

    # packages.x86_64-linux.default = pkgs.hello;

    devShells.x86_64-linux.default = pkgs.mkShell {

      NIX_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
        pkgs.stdenv.cc.cc
        pkgs.zlib
        # pkgs.libGL
        # pkgs.glib
      ];
      NIX_LD = pkgs.lib.fileContents "${pkgs.stdenv.cc}/nix-support/dynamic-linker";
      buildInputs = [
        pkg-py."3.13"
      ];
      shellHook = ''
        export LD_LIBRARY_PATH=$NIX_LD_LIBRARY_PATH

        folder_path="venv"  # The name of the folder relative to the current path
        # current_path="$PWD"
        # folder_path="$current_path/$folder_name"

        if [ ! -d "$folder_path" ]; then
          echo "Creating vertual env: $folder_path"
          python -m venv venv
        else
          echo "vertual env '$folder_path' already exists."
        fi

        source venv/bin/activate
      '';
    };

  };
}
