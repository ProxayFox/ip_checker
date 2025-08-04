{
  description = "A Nix-flake-based Python development environment";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs =
    { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};

      python = pkgs.python313;
      venvDir = ".venv";
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          (python.withPackages (
            ps: with ps; [
              venvShellHook
              pip

              # Coding Stuff
              python-lsp-server
              black
              pylint
              ruff
              jedi
              mypy
            ]
          ))

          nix-ld
          yaml-language-server
          markdown-oxide
        ];

        inputsFrom = with pkgs; [
          bat
        ];

        shellHook = ''
          nix-ld /home/proxay/.local/share/zed/languages/package-version-server/package-version-server-v0.0.7 "$@"

          if [ -d "${venvDir}" ]; then
            echo "Skipping venv creation, '${venvDir}' already exists"
          else
            echo "Creating new venv environment in path: '${venvDir}'"
            # Note that the module venv was only introduced in python 3, so for 2.7
            # this needs to be replaced with a call to virtualenv
            python -m venv "${venvDir}"
            # unescape to attempt use
            # \$\{pythonPackages.python.interpreter\} -m venv "${venvDir}"
          fi

          # activate our virtual env.
          source "${venvDir}/bin/activate"
        '';
      };
    };
}
