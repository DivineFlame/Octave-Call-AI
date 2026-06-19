#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="${OCTAVE_CALL_AI_INIT_WORKSPACE_DIR:-/workspace}"
OUTPUT_ROOT="${OCTAVE_CALL_AI_INIT_OUTPUT_ROOT:-/generated}"
NGINX_OUTPUT_DIR="$OUTPUT_ROOT/nginx"
COTURN_OUTPUT_DIR="$OUTPUT_ROOT/coturn"
CERTS_DIR="${OCTAVE_CALL_AI_INIT_CERTS_DIR:-/certs}"

# shellcheck disable=SC1091
. "$SCRIPT_DIR/lib/setup_common.sh"

OCTAVE_CALL_AI_DEPLOY_PROJECT_DIR="$WORKSPACE_DIR"

mkdir -p "$NGINX_OUTPUT_DIR" "$COTURN_OUTPUT_DIR"

if [[ "${ENVIRONMENT:-local}" == "production" ]]; then
    octave_call_ai_validate_remote_runtime_env
    [[ -f "$CERTS_DIR/local.crt" ]] || octave_call_ai_fail "certs/local.crt not found"
    [[ -f "$CERTS_DIR/local.key" ]] || octave_call_ai_fail "certs/local.key not found"

    export TURN_EXTERNAL_IP="$SERVER_IP"
    octave_call_ai_render_remote_nginx_conf "$WORKSPACE_DIR" "$NGINX_OUTPUT_DIR/default.conf"
    octave_call_ai_render_remote_turn_conf "$WORKSPACE_DIR" "$COTURN_OUTPUT_DIR/turnserver.conf"
    octave_call_ai_success "✓ octave-call-ai-init rendered remote nginx and coturn config"
    exit 0
fi

if [[ -n "${TURN_SECRET:-}" && -n "${TURN_HOST:-}" ]]; then
    export TURN_EXTERNAL_IP="$TURN_HOST"
    octave_call_ai_render_remote_turn_conf "$WORKSPACE_DIR" "$COTURN_OUTPUT_DIR/turnserver.conf"
    octave_call_ai_success "✓ octave-call-ai-init rendered local TURN config"
    exit 0
fi

octave_call_ai_success "✓ octave-call-ai-init no-op for current profile"
