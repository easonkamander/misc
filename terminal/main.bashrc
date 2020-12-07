alias ls='ls --color=always --group-directories-first'
alias grep='grep --color=always'
alias ip='ip -color=always'
alias dmesg='dmesg --color=always'
alias diff='diff --color=always'

export PATH="$PATH:~/Code/terminal/"
alias co='calico' # Shorter name

PS1="\e[1m[\e[31m\u\e[33m@\e[32m\h \e[34m\W\e[37m]\e[35m$\e[m "

export LESS=-R
export LESS_TERMCAP_mb=$'\E[1;31m'
export LESS_TERMCAP_md=$'\E[1;36m'
export LESS_TERMCAP_me=$'\E[0m'
export LESS_TERMCAP_so=$'\E[01;44;33m'
export LESS_TERMCAP_se=$'\E[0m'
export LESS_TERMCAP_us=$'\E[1;32m'
export LESS_TERMCAP_ue=$'\E[0m'