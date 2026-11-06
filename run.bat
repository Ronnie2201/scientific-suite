@echo off
setlocal

set MODE=%1
if "%MODE%"=="" set MODE=cli
shift

if "%MODE%"=="cli" (
    echo Starting CLI mode...
    docker-compose run --rm scientific-suite python -m interface.cli %*
) else if "%MODE%"=="gui" (
    echo Starting GUI mode...
    docker-compose run --rm scientific-suite python -m interface.gui
) else if "%MODE%"=="shell" (
    echo Opening shell...
    docker-compose run --rm scientific-suite bash
) else if "%MODE%"=="build" (
    echo Building...
    docker-compose build
) else if "%MODE%"=="test" (
    echo Running tests...
    docker-compose run --rm scientific-suite python -m pytest tests/
) else if "%MODE%"=="web" (
    echo Starting web app on http://localhost:5001 ...
    docker-compose up scientific-web
) else (
    echo Usage: run.bat {cli^|gui^|web^|shell^|build^|test}
)

endlocal