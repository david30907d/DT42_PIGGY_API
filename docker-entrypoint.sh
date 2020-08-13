#!/bin/sh -e
#!/busybox/sh -e

case "$1" in
  "server") nginx && gunicorn -b 127.0.0.1:9000 project.app ;;
  *) exec "$@" ;;
esac