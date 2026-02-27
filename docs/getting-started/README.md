# Getting Started Docs

For first-time setup and quick orientation.

## Start Path

1. Main overview and quick start: [../../README.md](../../README.md)
2. One-click setup and dual bootstrap mode: [../one-click-bootstrap.md](../one-click-bootstrap.md)
3. Update or uninstall on macOS: [macos-update-uninstall.md](macos-update-uninstall.md)
4. Find commands by tasks: [../commands-reference.md](../commands-reference.md)

## Choose Your Path

| Scenario | Command |
|----------|---------|
| I have an API key, want fastest setup | `zeroclaw onboard --api-key sk-... --provider openrouter` |
| I want guided prompts | `zeroclaw onboard --interactive` |
| Config exists, just fix channels | `zeroclaw onboard --channels-only` |
| Config exists, I intentionally want full overwrite | `zeroclaw onboard --force` |
| Using subscription auth | See [Subscription Auth](../../README.md#subscription-auth-openai-codex--claude-code) |

## Onboarding and Validation

- Quick onboarding: `zeroclaw onboard --api-key "sk-..." --provider openrouter`
- Interactive onboarding: `zeroclaw onboard --interactive`
- Existing config protection: reruns require explicit confirmation (or `--force` in non-interactive flows)
- Ollama cloud models (`:cloud`) require a remote `api_url` and API key (for example `api_url = "https://ollama.com"`).
- Validate environment: `zeroclaw status` + `zeroclaw doctor`

## Next

- Runtime operations: [../operations/README.md](../operations/README.md)
- Reference catalogs: [../reference/README.md](../reference/README.md)
- macOS lifecycle tasks: [macos-update-uninstall.md](macos-update-uninstall.md)

---

## ⚖️ OpenClaw vs. ZeroClaw (User Perspective)

If you are coming from **OpenClaw** or choosing between them, here is how **ZeroClaw** differs from a daily user's viewpoint:

### 1. Speed and Footprint

- **OpenClaw** relies on heavy Node.js runtimes. Startup can take longer, and it consumes hundreds of megabytes of RAM.
- **ZeroClaw** is a tiny, single compiled Rust binary. It uses under 5MB of RAM and starts in under 10ms. You can leave it running 24/7 on a background server (like a Mac mini or a $10 edge device) without noticing it.

### 2. Conversation Flow & Memory

- **OpenClaw** often treats memory in chunks or relies on your UI for context.
- **ZeroClaw** uses a built-in hybrid vector database for long-term memory. It isolates conversations automatically by channel, sender, and thread.
  - **Pro-Tip for ZeroClaw:** When using Slack, **always reply in thread** to maintain a continuous conversation.

### 3. Tool Usage & Autonomy

- **OpenClaw** focuses heavily on structured web interaction and complex sandboxed code execution, sometimes relying on thick UI configurations.
- **ZeroClaw** focuses on CLI-first, fully autonomous background execution (`zeroclaw daemon`). It gives you terminal-level control over its autonomy (`supervised` vs `full` mode) and integrates tightly with local tools (shell, git, workspace access).

### 4. Effective Usage with Tailscale + Quotio Setup

To use ZeroClaw effectively with your current Tailscale and Quotio proxy setup:
1. **Background Daemon:** Keep the daemon running (`zeroclaw daemon` or via system service).
2. **Channel Interaction:** Instead of using a web UI, interface with ZeroClaw entirely through Slack. The daemon routes messages through the Tailscale tunnel to your local Mac Quotio endpoint, and responds directly in chat.
3. **Threading:** Use threads in Slack for multi-turn tasks.
4. **Web Search:** Ensure `[web_search] enabled = true` in your `~/.zeroclaw/config.toml` so the agent can browse the internet.

---

## 🔧 Conversation History Debugging & Walkthrough

If the agent appears to "forget" context or fail to answer follow-up questions, check the following:

1. **Slack Thread Isolation:**
   ZeroClaw isolates conversation history using a composite key: `{channel}_{sender}_{thread_ts}`.
   - If you send a new top-level message directly into the channel, it begins a new context.
   - **Crucially:** If you want an isolated, continuous multi-turn conversation without interference, you must **Reply in Thread** to the bot's messages.
   - *(Note: A recent patch allows top-level responses to share a common user-level memory context when no explicit `thread_ts` exists, but using explicit threads is highly recommended).*

2. **The Quotio API Key / Connectivity:**
   If your API key is missing or the connection to your local Quotio proxy fails, the LLM request immediately drops.
   When an LLM request fails, ZeroClaw intentionally wraps up that specific user turn and inserts a synthetic "failed task" message to close the turn prematurely. This prevents broken, unanswered user turns from polluting the context window. However, because the tool loop aborted, the LLM "forgets" that turn.
   - **Fix:** Ensure your Quotio proxy API key (`sk-...`) is correctly set in `config.toml` and that your Tailscale tunnel connection is fully active between the execution host and your Mac.
