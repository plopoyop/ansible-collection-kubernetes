{ pkgs, lib, config, inputs, ... }:

{
  env.ANSIBLE_ROLES_PATH=".devenv/ansible/roles";
  env.ANSIBLE_COLLECTIONS_PATH=".devenv/ansible/collections";
  env.LOCALE_ARCHIVE="${pkgs.glibcLocales}/lib/locale/locale-archive";
  env.LANG="en_US.UTF8";

  packages = [
    pkgs.ansible
    pkgs.ansible-lint
    pkgs.git
    pkgs.glibcLocales
    pkgs.go-task
    pkgs.pre-commit
    pkgs.python312Packages.kubernetes
    pkgs.python312Packages.boto3
    pkgs.python312Packages.molecule
    pkgs.python312Packages.molecule-plugins
    pkgs.yamllint
  ];

  languages.ansible.enable = true;

  enterShell = ''
    mkdir -p $ANSIBLE_ROLES_PATH
    mkdir -p $ANSIBLE_COLLECTIONS_PATH
  '';
}
