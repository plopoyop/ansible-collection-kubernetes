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
    pkgs.kind
    pkgs.pre-commit
    pkgs.python312Packages.kubernetes
    pkgs.python312Packages.boto3
    pkgs.python312Packages.molecule
    pkgs.python312Packages.molecule-plugins
    pkgs.yamllint
  ];

  languages.ansible.enable = true;

  enterShell = ''
    export ANSIBLE_ROLES_PATH=$PWD/.devenv/ansible/roles;
    export ANSIBLE_COLLECTIONS_PATH=$PWD/.devenv/ansible/collections;

    mkdir -p $ANSIBLE_ROLES_PATH
    mkdir -p $ANSIBLE_COLLECTIONS_PATH
  '';
}
