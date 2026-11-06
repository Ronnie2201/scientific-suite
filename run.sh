#!/bin/bash
# Convenience script to run the scientific suite

set -e

MODE=${1:-cli}
shift || true

case $MODE in
    cli)
        echo "Starting CLI mode..."
        docker-compose run --rm scientific-suite python -m interface.cli "$@"
        ;;
    gui)
        echo "Starting GUI mode..."
        # Enable X11 forwarding on Linux/Mac
        xhost +local:docker 2>/dev/null || true
        docker-compose run --rm \
            -e DISPLAY=$DISPLAY \
            -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
            scientific-suite python -m interface.gui
        ;;
    web)
        echo "Starting web interface..."
        docker-compose run --rm -p 5001:5001 scientific-suite python -m interface.web_app
        ;;
    shell)
        echo "Opening shell in container..."
        docker-compose run --rm scientific-suite bash
        ;;
    build)
        echo "Building image..."
        docker-compose build
        ;;
    test)
        echo "Running tests..."
        docker-compose run --rm scientific-suite python -m pytest tests/
        ;;
    *)
        echo "Usage: $0 {cli|gui|web|shell|build|test} [args]"
        exit 1
        ;;
esac