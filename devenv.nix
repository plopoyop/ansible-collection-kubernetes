{ pkgs, lib, config, inputs, ... }:

{
  env.LOCALE_ARCHIVE="${pkgs.glibcLocales}/lib/locale/locale-archive";
  env.LANG="en_US.UTF8";

  packages = [
    pkgs.ansible
    pkgs.ansible-doctor
    pkgs.ansible-lint
    pkgs.git
    pkgs.glibcLocales
    pkgs.go-task
    pkgs.jq
    pkgs.kind
    pkgs.pre-commit
    pkgs.python312Packages.kubernetes
    pkgs.python312Packages.boto3
    pkgs.python312Packages.flake8
    pkgs.python312Packages.molecule
    pkgs.python312Packages.molecule-plugins
    pkgs.python312Packages.moto
    pkgs.python312Packages.pytest-ansible
    pkgs.yamllint
  ];

  languages.ansible.enable = true;

  scripts.install-kind-cloud.exec = ''
    OSTYPE="$(uname -s | tr -d '0-9.' | tr '[:upper:]' '[:lower:]')"
    CPUTYPE="$(uname -m)"
    BIN_DEST=$DEVENV_DOTFILE/bin/
    BIN_NAME="cloud-provider-kind"

    if [[ -f $BIN_DEST/$BIN_NAME ]]; then
      echo "already installed"
      exit 0;
    fi

    case "$CPUTYPE" in
      aarch64|arm64)
        GH_CPUTYPE="arm64";;
      x86_64)
        GH_CPUTYPE="amd64" ;;
      *)
        echo '??' ;;
    esac

    KIND_CLOUD_SRC=$(curl -s https://api.github.com/repos/kubernetes-sigs/cloud-provider-kind/releases/latest  |  jq -r '.assets[] | select(.name | contains ("'$OSTYPE'")) | select(.name | contains ("'$GH_CPUTYPE'"))  | .browser_download_url')
    echo $KIND_CLOUD_SRC

    mkdir -p $BIN_DEST
    curl -L $KIND_CLOUD_SRC | tar -xz -C $BIN_DEST $BIN_NAME
  '';


  enterShell = ''
    export ANSIBLE_ROLES_PATH=$PWD/.devenv/ansible/roles;
    export ANSIBLE_COLLECTIONS_PATH=$PWD/.devenv/ansible/collections;

    mkdir -p $ANSIBLE_ROLES_PATH
    mkdir -p $ANSIBLE_COLLECTIONS_PATH
  '';
}
