"""Use pyOCD 0.45.1's native connection retries for all CoreSight targets.

Activate through pyocd.yaml's user_script option or an explicit --script option.
This overrides DebugPortSetup only, including any pack-specific definition.
The target still supplies its memory map, flash algorithm, and other sequences.
"""


def will_init_target(target, init_sequence):
    dp = getattr(target, "dp", None)
    if dp is not None:
        # Returning False selects DPConnector.connect(), which retries the SWJ
        # handshake and can switch to the dormant activation sequence.
        dp.connect_debug_port_hook = lambda: False
