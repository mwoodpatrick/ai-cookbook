let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    (pkgs.python313.withPackages (python-pkgs: [
      python-pkgs.pandas
      python-pkgs.requests
      python-pkgs.jupyterlab
      python-pkgs.ipykernel
      python-pkgs.loguru
      python-pkgs.google-genai
    ]))
    pkgs.pandoc
    pkgs.ruff # A modern Python linter
  ];
  # Optional: Add any additional Python packages you need
  shellHook = ''
    echo "JupyterLab is ready to use. Run 'jupyter lab' to start."
  '';
}
