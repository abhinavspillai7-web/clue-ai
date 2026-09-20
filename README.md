# 🕵️ Clue AI

An AI-powered implementation of the classic deduction board game **Clue** (also known as *Cluedo*). Play against computer opponents that reason about hidden information, track what every player knows, and make strategic suggestions and accusations, or watch AI agents play each other.

> **Status:** 🚧 Work in progress. See the [Roadmap](#roadmap) for what's done and what's next.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How the Game Works](#how-the-game-works)
- [How the AI Works](#how-the-ai-works)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Testing and Benchmarking](#testing-and-benchmarking)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

---

## Overview

Clue is a game of **imperfect information**: a murder has been committed, and one *suspect*, one *weapon*, and one *room* are sealed in a confidential envelope. The remaining cards are dealt to the players. By making suggestions and observing which players can (or can't) refute them, each player narrows down the solution.

That makes it an excellent playground for AI techniques such as:

- Logical deduction and constraint satisfaction
- Probabilistic reasoning under uncertainty
- Information-theoretic move selection
- Opponent modeling
- (Optionally) LLM-based agents

This project provides a game engine plus a set of pluggable AI players you can play against, compare, and extend.

## Features

- ✅ Full Clue rules engine (turns, movement, suggestions, refutations, accusations)
- ✅ Multiple AI difficulty levels, from random to expert deduction
- ✅ Per-player **knowledge base** that tracks who has, doesn't have, or might have each card
- ✅ Pluggable agent interface, so you can write your own AI in a single file
- ✅ Headless simulation mode for running thousands of games
- ✅ Reproducible games via random seeds
- ✅ Game logs and replay support
- 🔲 Graphical or web interface *(planned)*

## How the Game Works

**Cards**

| Category | Options |
|----------|---------|
| Suspects (6) | Miss Scarlett, Colonel Mustard, Mrs. White, Mr. Green, Mrs. Peacock, Professor Plum |
| Weapons (6) | Candlestick, Knife, Lead Pipe, Revolver, Rope, Wrench |
| Rooms (9) | Kitchen, Ballroom, Conservatory, Dining Room, Billiard Room, Library, Lounge, Hall, Study |

**Turn flow**

1. **Roll and move** to a room (or hallway).
2. **Suggest**: when in a room, name a suspect and weapon. The suggestion is always for the room you're in.
3. **Refute**: starting with the player to the left, each player checks their hand. The first player holding a matching card secretly shows *one* to the suggester.
4. **Accuse** (optional, once): name the suspect, weapon, and room. If correct, you win; if wrong, you're eliminated but still must show cards to refute others.

## How the AI Works

Each AI agent maintains a model of the hidden world and chooses actions based on it.

### 1. Knowledge Base

Every agent tracks a card-ownership matrix (players × cards) with three states: **has**, **doesn't have**, and **unknown**. It also records the *constraints* revealed during play:

- **Refutation with a shown card:** the player definitely holds that card.
- **Refutation with an unseen card:** the player holds *at least one* of the three suggested cards.
- **Player passes:** that player holds *none* of the three suggested cards.
- **Solution constraint:** exactly one suspect, one weapon, and one room are in the envelope.

### 2. Inference

Agents can use one or more of these strategies (configurable per level):

| Level | Strategy |
|-------|----------|
| `random` | Picks legal moves at random. Baseline. |
| `basic` | Tracks its own hand and confirmed cards; suggests unknown cards. |
| `logic` | Propositional deduction / constraint propagation over "at least one of" clauses. |
| `probabilistic` | Estimates the probability of each card being in the envelope (e.g., via SAT-based model counting or Monte Carlo sampling of consistent deals). |
| `expert` | Probabilistic inference plus **information-gain** move selection and opponent modeling. |

### 3. Action Selection

- **Movement:** prefer rooms where a suggestion is expected to reduce uncertainty the most.
- **Suggestions:** choose the suspect/weapon that maximizes expected information gain, and occasionally bluff by suggesting cards from its own hand to mislead opponents.
- **Accusations:** accuse only when the probability of the solution exceeds a configurable confidence threshold (default `0.95`).

### 4. (Optional) LLM Agent

An experimental agent can use a large language model to reason over the game state in natural language. It receives a structured game-state summary and returns a legal action. This is mainly useful for comparison against the classical agents.

## Getting Started

### Prerequisites

> Adjust this section to match your stack. The examples below assume Python.

- Python 3.10+
- `pip` (or `uv` / `poetry`)

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/clue-ai.git
cd clue-ai

# (Recommended) create a virtual environment
python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Play against the AI

```bash
python -m clue.play --players 4 --human 1 --ai-level logic
```

### Watch AI vs. AI

```bash
python -m clue.play --players 4 --human 0 --ai-level expert --verbose
```

### Run a batch simulation

```bash
python -m clue.simulate --games 1000 --agents random,logic,probabilistic,expert --seed 42
```

### Common options

| Flag | Description | Default |
|------|-------------|---------|
| `--players` | Number of players (3–6) | `4` |
| `--human` | Number of human players | `1` |
| `--ai-level` | `random`, `basic`, `logic`, `probabilistic`, `expert` | `logic` |
| `--seed` | Random seed for reproducibility | random |
| `--verbose` | Print each agent's reasoning | off |
| `--log` | Save the game log to a file | off |

### Writing your own agent

Create a class that implements the `Agent` interface:

```python
from clue.agents.base import Agent

class MyAgent(Agent):
    def choose_move(self, state, legal_moves):
        """Return one of the legal movement options."""
        ...

    def choose_suggestion(self, state, room):
        """Return (suspect, weapon) to suggest."""
        ...

    def choose_refutation(self, state, suggestion, matching_cards):
        """Return which matching card to reveal."""
        ...

    def observe(self, event):
        """Update your knowledge from public game events."""
        ...

    def decide_accusation(self, state):
        """Return (suspect, weapon, room) or None."""
        ...
```

Then register it in `clue/agents/__init__.py` and run it with `--ai-level my_agent`.

## Project Structure

```
clue-ai/
├── clue/
│   ├── engine/          # Rules, board, turn logic, card deck
│   ├── agents/          # AI players (random, logic, probabilistic, expert, llm)
│   ├── knowledge/       # Knowledge base and inference (constraints, SAT, sampling)
│   ├── ui/              # CLI (and future GUI/web) interfaces
│   ├── play.py          # Entry point: play a game
│   └── simulate.py      # Entry point: batch simulations
├── tests/               # Unit and integration tests
├── docs/                # Design notes and diagrams
├── requirements.txt
├── LICENSE
└── README.md
```

## Configuration

Settings can be provided via CLI flags or a `config.yaml` file:

```yaml
game:
  players: 4
  seed: null

ai:
  level: expert
  accusation_threshold: 0.95
  bluff_probability: 0.10
  monte_carlo_samples: 5000

llm:            # only needed for the LLM agent
  enabled: false
  model: your-model-name
  api_key_env: LLM_API_KEY
```

## Testing and Benchmarking

```bash
# Run the test suite
pytest

# Compare agent strength (win rate and average turns to win)
python -m clue.simulate --games 5000 --agents random,basic,logic,probabilistic,expert
```

Suggested metrics to track:

- **Win rate** per agent type
- **Average turns to solve**
- **Incorrect accusation rate**
- **Deduction accuracy** (how often the agent's top guess is correct at each turn)

## Roadmap

- [x] Core rules engine
- [x] Random and basic agents
- [ ] Logical deduction agent
- [ ] Probabilistic inference agent
- [ ] Information-gain move selection
- [ ] Opponent modeling and bluffing
- [ ] LLM-based agent
- [ ] Game replay viewer
- [ ] Web or GUI front end
- [ ] Online multiplayer

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a pull request

Please include tests for new functionality and follow the existing code style.

## License

Distributed under the [MIT License](LICENSE). *(Change this to whichever license you choose.)*

## Disclaimer

This is an independent, non-commercial fan and educational project. **Clue®** / **Cluedo®** is a trademark of Hasbro, Inc. This project is not affiliated with, endorsed by, or sponsored by Hasbro.
