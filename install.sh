#!/usr/bin/env bash
set -e

RESET="\033[0m"
BOLD="\033[1m"
CYAN="\033[36m"
GREEN="\033[32m"
YELLOW="\033[33m"
MAGENTA="\033[35m"
RED="\033[31m"

header()  { printf "\n${BOLD}${CYAN}  ╭─ %s ───────────────────────────────╮${RESET}\n" "$1"; }
ok()      { printf "${GREEN}  │  ✓ %s${RESET}\n" "$1"; }
warn()    { printf "${YELLOW}  │  ⚠ %s${RESET}\n" "$1"; }
fail()    { printf "${RED}  │  ✗ %s${RESET}\n" "$1"; exit 1; }
footer()  { printf "  ╰%s╯${RESET}\n" "$(printf '─%.0s' $(seq 1 43))"; }

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

export PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1

clear
printf "\n${BOLD}${MAGENTA}"
printf "   ╔═══════════════════════════════════════════════╗\n"
printf "   ║               S T O R Y W E A V E R           ║\n"
printf "   ║        Novel → Video  Pipeline  Installer     ║\n"
printf "   ╚═══════════════════════════════════════════════╝${RESET}\n"

# ── 1. System ────────────────────────────────────────────────
header "1  Checking System"

if command -v python3 &>/dev/null; then
    ok "Python found: $(python3 --version 2>&1)"
else
    fail "Python 3 is required: sudo apt install python3 python3-venv"
fi

if command -v ffmpeg &>/dev/null; then
    ok "ffmpeg found: $(ffmpeg -version 2>&1 | head -1)"
else
    warn "ffmpeg not found — video export unavailable"
    if [ "$(id -u)" = "0" ]; then
        apt-get update -qq && apt-get install -y -qq ffmpeg 2>/dev/null && ok "ffmpeg installed" || warn "Could not install ffmpeg automatically"
    else
        warn "Install: sudo apt install ffmpeg"
    fi
fi

footer

# ── 2. Virtual Environment ───────────────────────────────────
header "2  Virtual Environment"

if [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
    ok "Virtual environment exists (reusing)"
else
    rm -rf .venv
    python3 -m venv .venv
    ok "Virtual environment created"
fi

source .venv/bin/activate
ok "Activated: $(which python)"

footer

# ── 3. Dependencies ──────────────────────────────────────────
header "3  Installing Dependencies"

PYTHON_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")

if [ "$PYTHON_VER" = "3.14" ]; then
    warn "Python 3.14 detected — using compatibility mode (PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1)"
fi

pip install --quiet --upgrade pip setuptools wheel 2>/dev/null || true

pip install --quiet -r backend/requirements.txt 2>&1 | while IFS= read -r line; do
    if echo "$line" | grep -qiE "error|failed|warning"; then
        printf "  │  ${YELLOW}%s${RESET}\n" "$line"
    fi
done

python3 -c "import fastapi, pydantic, moviepy, PIL; print('  │  ✓ fastapi pydantic moviepy Pillow')" 2>/dev/null || \
warn "Some packages may have issues with Python $PYTHON_VER"

ok "Dependencies installed"

footer

# ── 4. Configuration ─────────────────────────────────────────
header "4  Configuration"

ENV_FILE="backend/.env"
if [ ! -f "$ENV_FILE" ]; then
    cat > "$ENV_FILE" <<- EOF
GEMINI_API_KEY=
STABILITY_API_KEY=
ELEVENLABS_API_KEY=
PROJECTS_DIR=./projects
EOF
    ok "Created backend/.env"
fi

if grep -q "GEMINI_API_KEY=\"\?$\"" "$ENV_FILE" 2>/dev/null; then
    warn "GEMINI_API_KEY is empty — AI features (extraction, images, TTS) won't work"
    warn "Edit backend/.env and add your key"
else
    ok "GEMINI_API_KEY is set"
fi

mkdir -p backend/projects backend/voices backend/static
ok "Asset directories ready"

footer

# ── 5. Launch ────────────────────────────────────────────────
header "5  Launching Server"

port="${PORT:-8000}"
printf "  │  ${BOLD}Starting on http://localhost:%s${RESET}\n" "$port"

nohup .venv/bin/python -m uvicorn app.main:app \
    --app-dir backend --host 0.0.0.0 --port "$port" \
    --log-level warning > /tmp/storyweaver.log 2>&1 &
SERVER_PID=$!

for i in $(seq 1 15); do
    if curl -sf "http://localhost:$port/api/health" > /dev/null 2>&1; then
        ok "Server is running (PID: ${SERVER_PID})"
        break
    fi
    sleep 1
done

if ! kill -0 "$SERVER_PID" 2>/dev/null; then
    fail "Server failed to start.\n  │  └─ Check /tmp/storyweaver.log"
fi

footer

# ── 6. Verify ────────────────────────────────────────────────
header "6  Verification"

for check in \
    "API Health|curl -sf http://localhost:$port/api/health > /dev/null 2>&1" \
    "Dashboard  |curl -sf http://localhost:$port/static/index.html > /dev/null 2>&1" \
    "Projects   |curl -sf http://localhost:$port/api/projects > /dev/null 2>&1"; do

    label="${check%%|*}"
    cmd="${check##*|}"
    printf "  │  ${BOLD}%-12s${RESET}" "$label:"
    if eval "$cmd"; then
        printf "${GREEN}OK${RESET}\n"
    else
        printf "${RED}FAIL${RESET}\n"
    fi
done

voices=$(curl -s "http://localhost:$port/api/voices" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "0")
printf "  │  ${BOLD}%-12s${RESET}" "Voices:"
printf "${GREEN}%s available${RESET}\n" "$voices"

footer

# ── Done ─────────────────────────────────────────────────────
printf "\n${BOLD}${GREEN}"
printf "   ╔═══════════════════════════════════════════════╗\n"
printf "   ║          Installation Complete 🎬             ║\n"
printf "   ║                                               ║\n"
printf "   ║    ${CYAN}http://localhost:%-4s${GREEN}               ║\n" "$port"
printf "   ║                                               ║\n"
printf "   ║    ${YELLOW}Dashboard${GREEN}  /static/index.html          ║\n"
printf "   ║    ${YELLOW}API Docs${GREEN}    /docs                      ║\n"
printf "   ║                                               ║\n"
printf "   ║    ${MAGENTA}Stop${GREEN}:  kill %-5s                     ║\n" "$SERVER_PID"
printf "   ║    ${MAGENTA}Logs${GREEN}:   cat /tmp/storyweaver.log      ║\n"
printf "   ╚═══════════════════════════════════════════════╝\n${RESET}\n"
