{
  description = "Devbox environment with urllib3 2.5.0 override";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/ee09932cedcef15aaf476f9343d1dea2cb77e261";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        overlay = (final: prev: {
          python313Packages = prev.python313Packages // {
            urllib3 = prev.python313Packages.urllib3;
            ansible = prev.python313Packages.ansible;
            molecule = prev.python313Packages.molecule;
            molecule-plugins = prev.python313Packages.molecule-plugins;
            kubernetes = prev.python313Packages.kubernetes.overridePythonAttrs (oldAttrs: {
              propagatedBuildInputs =
                let
                  urllib3_2_5_0 = prev.python313Packages.urllib3;
                  buildInputs = oldAttrs.propagatedBuildInputs or [];
                in
                builtins.map (dep:
                  if dep.pname or "" == "urllib3" then urllib3_2_5_0 else dep
                ) buildInputs;
            });
          };
        });

        pkgs = import nixpkgs {
          inherit system;
          overlays = [ overlay ];
        };

      in {
        # Export modified Python packages
        packages = {
          ansible-doctor = pkgs.ansible-doctor;
          ansible-lint = pkgs.ansible-lint;
          ansible = pkgs.python313Packages.ansible;
          kubernetes = pkgs.python313Packages.kubernetes;
          molecule = pkgs.python313Packages.molecule;
          molecule-plugins = pkgs.python313Packages.molecule-plugins;
          urllib3 = pkgs.python313Packages.urllib3;
        };
      });
}
