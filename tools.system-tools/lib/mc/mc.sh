# Don't define aliases in plain Bourne shell
[ -n "${BASH_VERSION}${KSH_VERSION}${ZSH_VERSION}" ] || return 0
alias mc='. /storage/.kodi/addons/tools.system-tools/lib/mc/mc-wrapper.sh'
