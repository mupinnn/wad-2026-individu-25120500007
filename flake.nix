{
  description = "Node.js v24 and Python development environment";
  inputs = { nixpkgs.url = "github:NixOs/nixpkgs/release-25.11"; };
  outputs = { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in {
      devShells.${system}.default = pkgs.mkShell {
        venvDir = ".venv";
        packages = [
          pkgs.nodejs_24
          pkgs.python3
          pkgs.python3Packages.venvShellHook
        ];
      };
    };
}
