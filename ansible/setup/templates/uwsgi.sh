#!/bin/sh

# uwsgi - Use uwsgi to run python and wsgi web apps.
#
# chkconfig: - 85 15
# description: Use uwsgi to run python and wsgi web apps.
# processname: uwsgi

# Source function library.
. /etc/rc.d/init.d/functions

uwsgi="/usr/local/python/bin/uwsgi"
prog=$(basename $uwsgi)

lockfile="/var/run/${prog}/${prog}.lock"
pidfile="/var/run/${prog}/${prog}.pid"

DAEMON_OPTS="--emperor /etc/uwsgi/vassals --uid <username> --gid nginx --pidfile $pidfile --https2"

start() {
    [ -x $uwsgi ] || exit 5
    echo -n $"Starting $prog: "
    daemon $uwsgi $DAEMON_OPTS &
    retval=$?
    echo
    [ $retval -eq 0 ] && touch $lockfile
    return $retval
}

stop() {
    echo -n $"Stopping $prog: "
    killproc -p $pidfile $prog
    retval=$?
    echo
    [ $retval -eq 0 ] && rm -f $lockfile
    return $retval
}

restart() {
    stop
    start
}

refresh() {
    echo -n $"Reloading $prog: "
    touch /tmp/$prog.touch
    echo
}

reload (){
    echo -n $"Reloading $prog: "
    killproc -p $pidfile $prog -HUP
    echo
}

rh_status() {
    status $prog
}

rh_status_q() {
    rh_status >/dev/null 2>&1
}

case "$1" in
    start)
        rh_status_q && exit 0
        $1
        ;;
    stop)
        rh_status_q || exit 0
        $1
        ;;
    restart)
        $1
        ;;
    reload)
        rh_status_q || exit 7
        $1
        ;;
    status|status_q)
        rh_$1
        ;;
    *)
        echo $"Usage: $0 {start|stop|reload|status|restart}"
        exit 2
esac
