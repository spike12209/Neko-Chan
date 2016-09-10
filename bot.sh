until python3 bot.py; do
    echo "Bot crashed with exit code $?.  Respawning.." >&2
    sleep 3
done
