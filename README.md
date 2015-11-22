# Directory Listener

Checks for changes (new files) in a directory, to do some processing with.

## In a nutshell

1. Checks intermittently for new files in a given directory (default is `in` directory)
2. Moves the files temporarily to `processing` directory
3. Once processing has finished, moves them to `processed` directory

Logs everything to stdout and a log file.
