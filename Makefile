.PHONY: list help

define ASCILOGO
___  ____ ____ _  _ ____ ____    ____ _ _ _ ____ ____ _  _    _  _ ____ ____ _  _ ____ _
|  \ |  | |    |_/  |___ |__/ __ [__  | | | |__| |__/ |\/| __ |\/| |__| |__/ |  | |___ |
|__/ |__| |___ | \_ |___ |  \    ___] |_|_| |  | |  \ |  |    |  | |  | |  \  \/  |___ |___

=======================================
endef

export ASCILOGO

# http://misc.flogisoft.com/bash/tip_colors_and_formatting

RED=\033[0;31m
GREEN=\033[0;32m
ORNG=\033[38;5;214m
BLUE=\033[38;5;81m
NC=\033[0m

export RED
export GREEN
export NC
export ORNG
export BLUE

PROXY_COMMAND=

ifdef use_proxy
PROXY_COMMAND=--ssh-extra-args='-o ProxyCommand="/usr/bin/nc -x localhost:1230 %h %p"'
endif

# verify that certain variables have been defined off the bat
check_defined = \
    $(foreach 1,$1,$(__check_defined))
__check_defined = \
    $(if $(value $1),, \
      $(error Undefined $1$(if $(value 2), ($(strip $2)))))

list_allowed_args := product ip command

help:
	@printf "\033[1m$$ASCILOGO $$NC\n"
	@printf "\033[21m\n\n"
	@printf "=======================================\n"
	@printf "\n"
	@printf "Setup Commands :\n"
	@printf "$$GREEN make download-roles$$NC                               Downloads roles listed in install_roles.txt from ansible-galaxy to local folder\n"
	@printf "$$GREEN make create-logs-dir$$NC                              Local logs folder used for pulling entire journald logs from multiple hosts\n"
	@printf "$$GREEN make bootstrap-coreos product=<PRODUCT>$$NC           Install ansible on coreos instances. Pass use_proxy=1 if you want to use your socks5 proxy for performance increase\n"
	@printf "\n"
	@printf "\033[21m\n\n"
	@printf "=======================================\n"
	@printf "\n"
	@printf "Role Commands :\n"
	@printf "$$GREEN make rolling-reboot-no-jump-server product=<PRODUCT>$$NC             Perform a rolling reboot on <PRODUCT> cluster. Pass use_proxy=1 if you want to use your socks5 proxy for performance increase\n"
	@printf "=======================================\n"
	@printf "\n"

create-logs-dir:
	@mkdir ./.ansible-logs

list:
	@$(MAKE) -qp | awk -F':' '/^[a-zA-Z0-9][^$#\/\t=]*:([^=]|$$)/ {split($$1,A,/ /);for(i in A)print A[i]}' | sort

download-roles:
	ansible-galaxy install -r install_roles.txt --roles-path ./roles/

bootstrap-coreos:
	$(call check_defined, product, Please set product)
	@ansible-playbook coreos_ansibleize.yml -i ./inventory-$(product)/ -f 10 ${PROXY_COMMAND}

who:
	$(call check_defined, product, Please set product)
	@ansible coreos -i inventory-$(product)/ ${PROXY_COMMAND} -m raw -a "who" -f 10

raw:
	$(call check_defined, product, Please set product)
	$(call check_defined, command, Please set command)
	@ansible coreos -i inventory-$(product)/ ${PROXY_COMMAND} -m raw -a "$(command)" -f 10

proxy-list:
	$(call check_defined, product, Please set product)
	$(call check_defined, command, Please set command)
	@ansible coreos_proxy -i inventory-$(product)/ ${PROXY_COMMAND} -m raw -a "$(command)" -f 10

# Hard to remember so many ad-hoc commands, lets make a make task that can help us remember them all
show-adhoc-examples:
	@printf "\n"
	@printf "\033[21m\n\n"
	@printf "=======================================\n"
	@printf "$$GREEN Get last 50 errors in journald logs$$NC\n"
	@printf "$$BLUE ansible coreos_workers -m raw -a 'bash -c \"journalctl -n 50 -p err --no-pager\"' -i ./inventory-marvel/ -f 10 -u ansible$$NC\n"
	@printf "\n"
	@printf "$$GREEN Get current disk space$$NC\n"
	@printf "$$BLUE ansible coreos_worker -m raw -a 'set -x;df -H' -i ./inventory-marvel/ -f 10 -u ansible$$NC\n"
	@printf "\n"

# Compile python modules against homebrew openssl. The homebrew version provides a modern alternative to the one that comes packaged with OS X by default.
# OS X's older openssl version will fail against certain python modules, namely "cryptography"
# Taken from this git issue pyca/cryptography#2692
install-virtualenv-osx:
	ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include" pip install --ignore-installed --pre "https://github.com/pradyunsg/pip/archive/hotfix/9.0.2.zip#egg=pip"
	ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include" pip install --upgrade setuptools==36.0.1 wheel==0.29.0
	ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include" pip install -r requirements.txt

install-virtualenv:
	pip install -r requirements.txt

serverspec-diff:
	cat serverspec_things_to_check_for.txt

serverspec:
	bundle exec rake

serverspec-install:
	bundle install --path .vendor

install-cidr-brew:
	pip install cidr-brewer

bootstrap-ansible-swarm:
	ansible latveria -i inventory-marvel/ -m raw -a "set -x; dnf install -y python2 ansible python2-dnf libselinux-python" -f 10

bootstrap-ansible-latveria:
	ansible latveria -i inventory-marvel/ -m raw -a "set -x; dnf install -y python2 ansible python2-dnf libselinux-python" -f 10

bootstrap-playbook:
	@ansible-playbook -vvv playbook.yml -i ./inventory-marvel-dyninv/ -f 10 -u pi

bootstrap-user-role:
	@ansible-playbook -vvv user-role.yml -i ./inventory-marvel-dyninv/ -f 10 -u root

create-droplets:
	@ansible-playbook -vvv create-droplets.yml -i do_dynamic --skip-tags "pause"

# RUN ORDER:
# 1. create-droplets
# 2. bootstrap-user-role
# 3. bootstrap-playbook
