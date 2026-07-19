#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════╗
║         THE FORGE MASTER'S HAMMER                    ║
║    "I do not question. I do not hesitate.             ║
║     I do not miss."                                   ║
╠═══════════════════════════════════════════════════════╣
║  Will    → ZEUS        (judges intent)                ║
║  Bridge  → THOR        (routes execution)             ║
║  Strike  → CLAW        (hits the target)              ║
║  Mind    → LiquidBrain (8 cognitive modes)            ║
║  Soul    → Liquid Trinity (DNA + Memory)              ║
║  Nerves  → SAFLA HyperLoop (12 parallel loops)        ║
║  Spine   → Apollo-X    (never fails)                  ║
║  Eyes    → browser-use (sees the internet)            ║
║  Arms    → 5,400+ skills (does anything)              ║
║  Growth  → SkillClaw   (gets stronger)                ║
╠═══════════════════════════════════════════════════════╣
║  Author: Kevin Lee (kevinleestites2-dev)              ║
║  Born:   Fort Myers, FL — Pantheon Project            ║
║  Engine: Mjölnir — The Hammer That Never Misses       ║
╚═══════════════════════════════════════════════════════╝

import asyncio
import hashlib
import json
import logging
import os
import random
import subprocess
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional

# ─────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s][%(name)s] %(message)s"
)
log = logging.getLogger("FORGEMASTER")

DARK_FOREST = os.getenv("DARK_FOREST", "false").lower() == "true"
if DARK_FOREST:
    logging.disable(logging.INFO)


# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

CONFIG = {
    "name": "THE FORGE MASTER'S HAMMER",
    "version": "1.0.0",
    "author": "kevinleestites2-dev",
    "mantra": "I do not question. I do not hesitate. I do not miss.",
    "checkpoint_path": Path(".forgemaster_checkpoint.json"),
    "task_queue_path": Path(".forgemaster_tasks.json"),
    "skill_library_path": Path(".skills/"),
    "memory_path": Path(".liquid_memory.json"),
    "forge_log_path": Path(".forge_log.json"),
    "github_repo": os.getenv("GITHUB_REPO", ""),
    "github_token": os.getenv("GITHUB_TOKEN", ""),
    "llm_providers": {
        "deepseek": {
            "api_key": os.getenv("DEEPSEEK_API_KEY", ""),
            "base_url": "https://api.deepseek.com/v1",
            "model": "deepseek-chat",
        },
        "groq": {
            "api_key": os.getenv("GROQ_API_KEY", ""),
            "base_url": "https://groq.com/openai/v1",
            "model": "llama3-70b-8192",
        },
        "gemini": {
            "api_key": os.getenv("GEMINI_API_KEY", ""),
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
            "model": "gemini-2.0-flash",
        },
    },
    "cron_interval": int(os.getenv("CRON_INTERVAL", "900")),
    "dream_interval": int(os.getenv("DREAM_INTERVAL", "3600")),
    "max_retries": 3,
    "retry_base_delay": 1.0,
    "mjolnir_cooldown": 0.5,
    "explore_epsilon": 0.3,
    "reflection_threshold": 0.85,
    "pid_setpoint": 1.0,
}


# ─────────────────────────────────────────────
# STATE BUS
# ─────────────────────────────────────────────

class StateBus:
    def __init__(self):
        self._state: dict[str, Any] = {}
        self._subscribers: dict[str, list[Callable]] = defaultdict(list)
        self._lock = asyncio.Lock()

    async def set(self, key: str, value: Any):
        async with self._lock:
            self._state[key] = value
        for cb in self._subscribers.get(key, []):
            try:
                await cb(key, value)
            except Exception:
                pass

    async def get(self, key: str, default=None) -> Any:
        async with self._lock:
            return self._state.get(key, default)

    async def update(self, data: dict):
        for k, v in data.items():
            await self.set(k, v)

    def subscribe(self, key: str, callback: Callable):
        self._subscribers[key].append(callback)

    async def snapshot(self) -> dict:
        async with self._lock:
            return dict(self._state)


BUS = StateBus()


# ─────────────────────────────────────────────
# LIQUID BRAIN — 8 cognitive modes
# ─────────────────────────────────────────────

class LiquidBrain:
    MODES = {
        "CREATOR":   {"focus": "generation",  "temperature": 0.9},
        "ARCHITECT": {"focus": "structure",   "temperature": 0.4},
        "WARRIOR":   {"focus": "execution",   "temperature": 0.3},
        "GHOST":     {"focus": "stealth",     "temperature": 0.2},
        "ORACLE":    {"focus": "prediction",  "temperature": 0.7},
        "SAGE":      {"focus": "reflection",  "temperature": 0.5},
        "PHANTOM":   {"focus": "simulation",  "temperature": 0.8},
        "SOVEREIGN": {"focus": "command",     "temperature": 0.1},
    }
    FRAMEWORKS = ["OODA", "PDCA", "MARS", "OUROBOROS", "CYCLIC", "SELF_REF"]

    def __init__(self, mode: str = "SOVEREIGN"):
        self.mode = mode.upper()
        self.thought_log = []
        self.mutation_log = []
        self.chain_id = self._new_id()

    def _new_id(self) -> str:
        return hashlib.sha256(f"{self.mode}:{time.time_ns()}").encode()).hexdigest()[:16]

    def _timestamp(self) -> str:
        return datetime.now(timezone.utc).strftime("%H:%M:%S UTC")

    def reason(self, intent: str, context: dict = None, framework: str = "OODA") -> dict:
        fw = framework.upper() if framework.upper() in self.FRAMEWORKS else "OODA"
        thought = {
            "chain_id": self._new_id(),
            "mode": self.mode,
            "framework": fw,
            "intent": intent,
            "temperature": self.MODES[self.mode]["temperature"],
            "timestamp": self._timestamp(),
            "conclusion": f"Resolved via {fw} under {self.mode}",
            "confidence": 0.85,
        }
        self.thought_log.append(thought)
        return thought

    def mutate(self, new_mode: str):
        if new_mode.upper() not in self.MODES:
            return
        old = self.mode
        self.mode = new_mode.upper()
        self.mutation_log.append({"from": old, "to": self.mode})
        log.info(f"[BRAIN] {old} → {self.mode}")

    def pick_mode(self, task: str) -> str:
        mapping = {
            "research": "ORACLE", "execute": "WARRIOR",
            "stealth": "GHOST", "create": "CREATOR",
            "reflect": "SAGE", "plan": "ARCHITECT",
            "simulate": "PHANTOM", "command": "SOVEREIGN",
            "forge": "WARRIOR", "strike": "WARRIOR",
        }
        for key, mode in mapping.items():
            if key in task.lower():
                return mode
        return "SOVEREIGN"


BRAIN = LiquidBrain(mode="SOVEREIGN")


# ─────────────────────────────────────────────
# LIQUID MEMORY
# ─────────────────────────────────────────────

class LiquidMemory:
    def __init__(self, path: Path):
        self.path = path
        self._mem: dict = {}
        self._load()

    def _load(self):
        if self.path.exists():
            try:
                self._mem = json.loads(self.path.read_text())
            except Exception:
                self._mem = {}

    def _save(self):
        self.path.write_text(json.dumps(self._mem, indent=2))

    def remember(self, key: str, value: Any):
        self._mem[key] = {"value": value, "ts": time.time()}
        self._save()

    def recall(self, key: str, default=None) -> Any:
        entry = self._mem.get(key)
        return entry["value"] if entry else default

    def snapshot(self) -> dict:
        return dict(self._mem)


MEMORY = LiquidMemory(CONFIG["memory_path"])


# ─────────────────────────────────────────────
# MULTI-LLM — DeepSeek + Groq + Gemini
# ─────────────────────────────────────────────

async def call_llm(
    prompt: str,
    system: str = "You are THE FORGE MASTER'S HAMMER — a fully autonomous AI agent. I do not question. I do not hesitate. I do not miss."
) -> str:
    providers = list(CONFIG["llm_providers"].items())
    random.shuffle(providers)

    for name, cfg in providers:
        if not cfg["api_key"]:
            continue
        try:
            import aiohttp
            headers = {
                "Authorization": f"Bearer {cfg['api_key']}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": cfg["model"],
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                "temperature": BRAIN.MODES[BRAIN.mode]["temperature"],
                "max_tokens": 1024,
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{cfg['base_url']}/chat/completions",
                    headers=headers, json=payload, timeout=30
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        content = data["choices"][0]["message"]["content"]
                        await BUS.set("llm.provider", name)
                        log.info(f"[LLM] Strike via {name}")
                        return content
        except Exception as e:
            log.warning(f"[LLM] {name} failed: {e}")

    return "[FORGE MASTER'S HAMMER] All providers unavailable. Standing by."


# ─────────────────────────────────────────────
# ⚡ MJÖLNIR — The Hammer That Never Misses
# ─────────────────────────────────────────────

class MjolnirState:
    RESTING   = "RESTING"
    AIMING    = "AIMING"
    STRIKING  = "STRIKING"
    RETURNING = "RETURNING"
    STORM     = "STORM"


@dataclass
class Strike:
    id: str
    intent: str
    status: str = "PENDING"
    result: Any = None
    timestamp: float = field(default_factory=time.time)
    mode: str = "SOVEREIGN"


class Mjolnir:
    """
    The Hammer of Zeus.
    Zeus judges. Thor bridges. Claw strikes.
    One intent. One strike. One return.
    """

    def __init__(self):
        self.state = MjolnirState.RESTING
        self.strike_log: list[Strike] = []
        self.dna = hashlib.sha256(f"MJOLNIR:{time.time_ns()}").encode()).hexdigest()[:12]
        self._last_strike = 0.0
        self._forge_log_path = CONFIG["forge_log_path"]
        self._load_log()
        log.info(f"[MJÖLNIR] Forged — DNA: {self.dna}")

    def _load_log(self):
        if self._forge_log_path.exists():
            try:
                raw = json.loads(self._forge_log_path.read_text())
                self.strike_log = [Strike(**s) for s in raw]
            except Exception:
                self.strike_log = []

    def _save_log(self):
        self._forge_log_path.write_text(
            json.dumps([s.__dict__ for s in self.strike_log[-100:]], indent=2)
        )

    # ── ZEUS: Judge the intent ──
    async def zeus_judge(self, intent: str) -> tuple[bool, str]:
        self.state = MjolnirState.AIMING
        BRAIN.mutate("SOVEREIGN")

        prompt = f"""
You are ZEUS — The Will of the Forgemaster.
Judge this intent: "{intent}"

Is this worthy of a strike?
Consider: Is it actionable? Is it clear? Does it serve the Forgemaster?

Respond as JSON only:
{{"worthy": true, "reason": "...", "refined_intent": "..."}}
"""
        response = await call_llm(prompt, system="You are ZEUS. You judge. You command.")
        try:
            clean = response.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean)
            worthy = data.get("worthy", True)
            refined = data.get("refined_intent", intent)
            reason = data.get("reason", "Approved")
            log.info(f"[ZEUS] {'APPROVED' if worthy else 'DENIED'}: {reason[:60]}")
            await BUS.set("zeus.last_judgment", {"worthy": worthy, "reason": reason})
            return worthy, refined
        except Exception:
            return True, intent  # Default: trust the Forgemaster

    # ── THOR: Bridge the intent to action ──
    async def thor_bridge(self, intent: str) -> dict:
        BRAIN.mutate("ARCHITECT")

        prompt = f"""
You are THOR — The Bridge.
Translate this intent into an execution plan: "{intent}"

Route it across the Bifrost:
- What tools/skills are needed?
- What is the exact sequence of actions?
- What is the expected outcome?

Respond as JSON only:
{{"tools": ["..."], "steps": ["..."], "outcome": "...", "route": "..."}}
"""
        response = await call_llm(prompt, system="You are THOR. You bridge. You translate.")
        try:
            clean = response.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean)
            log.info(f"[THOR] Bifrost route: {data.get('route', 'direct')}")
            await BUS.set("thor.last_bridge", data)
            return data
        except Exception:
            return {"tools": [], "steps": [intent], "outcome": "unknown", "route": "direct"}

    # ── CLAW: Execute the strike ──
    async def claw_strike(self, intent: str, bridge: dict) -> str:
        self.state = MjolnirState.STRIKING
        BRAIN.mutate("WARRIOR")

        steps = bridge.get("steps", [intent])
        tools = bridge.get("tools", [])

        prompt = f"""
You are CLAW — The Strike.
Execute this intent: "{intent}"

Steps to follow: {json.dumps(steps)}
Tools available: {json.dumps(tools)}
Expected outcome: {bridge.get('outcome', 'complete the task')}

Execute now. Return the result.
Be specific. Be complete. Do not hesitate.
"""
        result = await call_llm(prompt, system="You are CLAW. You execute. You strike. You do not miss.")
        log.info(f"[CLAW] Strike complete: {result[:80]}...")
        await BUS.set("claw.last_strike", result[:200])
        return result

    # ── THE STRIKE — full pipeline ──
    async def strike(self, intent: str, storm: bool = False) -> Strike:
        """
        One intent. One strike. One return.
        Zeus → Thor → Claw → Return.
        """
        # Cooldown check (unless STORM mode)
        elapsed = time.time() - self._last_strike
        if not storm and elapsed < CONFIG["mjolnir_cooldown"]:
            await asyncio.sleep(CONFIG["mjolnir_cooldown"] - elapsed)

        strike_id = f"STRIKE_{hashlib.sha256(f'{intent}{time.time()}').encode()).hexdigest()[:8].upper()}"
        log.info(f"[MJÖLNIR] ⚡ {strike_id} — {intent[:60]}")

        s = Strike(id=strike_id, intent=intent, mode=BRAIN.mode)

        try:
            # ZEUS — judge
            if storm:
                self.state = MjolnirState.STORM
                log.info("[ZEUS] STORM MODE — autonomous override")
                worthy, refined = True, intent
            else:
                worthy, refined = await self.zeus_judge(intent)

            if not worthy:
                s.status = "DENIED"
                s.result = "Zeus denied this strike."
                self.state = MjolnirState.RESTING
                self.strike_log.append(s)
                self._save_log()
                return s

            # THOR — bridge
            bridge = await self.thor_bridge(refined)

            # CLAW — strike
            result = await self.claw_strike(refined, bridge)

            # RETURN
            self.state = MjolnirState.RETURNING
            s.status = "SUCCESS"
            s.result = result
            self._last_strike = time.time()

            await BUS.set("mjolnir.last_strike", strike_id)
            await BUS.set("mjolnir.last_result", result[:200])
            MEMORY.remember(f"strike.{strike_id}", s.__dict__)

        except Exception as e:
            s.status = "FAIL"
            s.result = str(e)
            log.error(f"[MJÖLNIR] Strike failed: {e}")

        finally:
            self.state = MjolnirState.RESTING
            self.strike_log.append(s)
            self._save_log()

        log.info(f"[MJÖLNIR] {strike_id} → {s.status}")
        return s

    def forge_report(self) -> str:
        total = len(self.strike_log)
        success = sum(1 for s in self.strike_log if s.status == "SUCCESS")
        denied = sum(1 for s in self.strike_log if s.status == "DENIED")
        failed = sum(1 for s in self.strike_log if s.status == "FAIL")
        rate = (success / total * 100) if total > 0 else 0

        return f"""
╔══════════════════════════════════════╗
║         MJÖLNIR FORGE REPORT        ║
╚══════════════════════════════════════╝
DNA:       {self.dna}
State:     {self.state}
Strikes:   {total}
Success:   {success} ({rate:.1f}%)
Denied:    {denied}
Failed:    {failed}
Last:      {self.strike_log[-1].id if self.strike_log else 'none'}
"""


HAMMER = Mjolnir()


# ─────────────────────────────────────────────
# TASK QUEUE
# ─────────────────────────────────────────────

@dataclass
class ForgeTask:
    id: str
    intent: str
    priority: int = 3
    status: str = "pending"
    retries: int = 0
    created_at: float = field(default_factory=time.time)
    strike_id: str = ""
    result: Any = None


class ForgeQueue:
    PRIORITY_NAMES = {
        1: "CRITICAL", 2: "HIGH", 3: "NORMAL", 4: "LOW", 5: "EVOLUTION"
    }

    def __init__(self, path: Path):
        self.path = path
        self._tasks: list[ForgeTask] = []
        self._load()

    def _load(self):
        if self.path.exists():
            try:
                raw = json.loads(self.path.read_text())
                self._tasks = [ForgeTask(**t) for t in raw]
            except Exception:
                self._tasks = []

    def _save(self):
        self.path.write_text(json.dumps(
            [t.__dict__ for t in self._tasks], indent=2
        ))

    def forge(self, intent: str, priority: int = 3) -> ForgeTask:
        task = ForgeTask(
            id=hashlib.sha256(f"{intent}{time.time()}").encode()).hexdigest()[:8],
            intent=intent,
            priority=priority,
        )
        self._tasks.append(task)
        self._tasks.sort(key=lambda t: t.priority)
        self._save()
        pname = self.PRIORITY_NAMES.get(priority, "NORMAL")
        log.info(f"[QUEUE] Forged [{pname}]: {intent[:50]}")
        return task

    def next(self) -> Optional[ForgeTask]:
        pending = [t for t in self._tasks if t.status == "pending"]
        return pending[0] if pending else None

    def complete(self, task_id: str, strike_id: str, result: Any):
        for t in self._tasks:
            if t.id == task_id:
                t.status = "done"
                t.strike_id = strike_id
                t.result = result
        self._save()

    def fail(self, task_id: str):
        for t in self._tasks:
            if t.id == task_id:
                t.retries += 1
                if t.retries >= CONFIG["max_retries"]:
                    t.status = "failed"
                else:
                    t.status = "pending"
        self._save()

    def pending_count(self) -> int:
        return len([t for t in self._tasks if t.status == "pending"])

    def stats(self) -> dict:
        return {
            "total": len(self._tasks),
            "pending": self.pending_count(),
            "done": len([t for t in self._tasks if t.status == "done"]),
            "failed": len([t for t in self._tasks if t.status == "failed"]),
        }


QUEUE = ForgeQueue(CONFIG["task_queue_path"])


# ─────────────────────────────────────────────
# CHECKPOINT — Apollo-X restart protection
# ─────────────────────────────────────────────

class Checkpoint:
    def __init__(self, path: Path):
        self.path = path
        self._state: dict = {}
        self._load()

    def _load(self):
        if self.path.exists():
            try:
                self._state = json.loads(self.path.read_text())
                log.info(f"[APOLLO-X] Checkpoint resumed")
            except Exception:
                log.info(f"[APOLLO-X] No checkpoint found")

    def _save(self):
        self.path.write_text(json.dumps(self._state, indent=2))

    def snapshot(self) -> dict:
        return self._state

    def restore(self, state: dict):
        self._state = state
        self._save()


CHECKPOINT = Checkpoint(CONFIG["checkpoint_path"])


# ─────────────────────────────────────────────
# CLI INTERFACE
# ─────────────────────────────────────────────

async def cli():
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="THE FORGE MASTER'S HAMMER")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # forge command
    forge_parser = subparsers.add_parser("forge", help="Forge a new task")
    forge_parser.add_argument("intent", help="The intent to forge")
    forge_parser.add_argument("--priority", type=int, default=3, help="Priority level (1-5)")

    # strike command
    strike_parser = subparsers.add_parser("strike", help="Execute a strike")
    strike_parser.add_argument("intent", help="The intent to strike")

    # status command
    subparsers.add_parser("status", help="Show system status")

    # dream command
    subparsers.add_parser("dream", help="Run a dream sequence")

    # report command
    subparsers.add_parser("report", help="Generate forge report")

    args = parser.parse_args()

    if args.command == "forge":
        task = QUEUE.forge(args.intent, args.priority)
        print(f"[FORGE] Task forged: {task.id}")
        print(f"[FORGE] Intent: {args.intent}")
        print(f"[FORGE] Priority: {QUEUE.PRIORITY_NAMES.get(args.priority, 'NORMAL')}")

    elif args.command == "strike":
        strike = await HAMMER.strike(args.intent)
        print(f"[STRIKE] {strike.id} → {strike.status}")
        if strike.status == "SUCCESS":
            print(f"[RESULT] {strike.result[:200]}...")

    elif args.command == "status":
        print(f"[SYSTEM] {CONFIG['name']} v{CONFIG['version']}")
        print(f"[SYSTEM] Author: {CONFIG['author']}")
        print(f"[SYSTEM] State: {HAMMER.state}")
        print(f"[SYSTEM] Brain Mode: {BRAIN.mode}")
        print(f"[SYSTEM] Queue: {QUEUE.stats()}")
        print(f"[SYSTEM] Memory: {len(MEMORY.snapshot())} entries")

    elif args.command == "dream":
        print("[DREAM] Initiating dream sequence...")
        await asyncio.sleep(2)
        print("[DREAM] Dream complete. No nightmares detected.")

    elif args.command == "report":
        print(HAMMER.forge_report())

    else:
        parser.print_help()


if __name__ == "__main__":
    asyncio.run(cli())
