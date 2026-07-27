"""Allow `python -m linter` to run the ClarityGate CLI."""

from .claritygate import main

raise SystemExit(main())

