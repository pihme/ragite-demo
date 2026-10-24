{
  description = "ragite-demo: Chromium for the search-page screenshots";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.sqlite.url = "path:../sqlite";

  outputs = { self, nixpkgs, sqlite }:
    let
      systems = ["x86_64-linux" "aarch64-linux" "aarch64-darwin"];
      forAll = f: nixpkgs.lib.genAttrs systems (system:
        f system nixpkgs.legacyPackages.${system});
    in {
      devShells = forAll (system: pkgs: {
        default = pkgs.mkShell {
          packages = with pkgs; [ chromium ];
            inputsFrom = [ sqlite.devShells.${system}.default ];
            shellHook = ''

              export CHROME_PATH=${pkgs.chromium}/bin/chromium
              # pip wheels such as greenlet (Playwright) need libstdc++.
              export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib''${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}

            '';
        };
      });
    };
}
