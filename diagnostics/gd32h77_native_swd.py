"""Use pyOCD 0.45.1's native SWD connection retries for GD32H77DIW.

Activate through pyocd.yaml's user_script option or an explicit --script option.
This changes DebugPortSetup only; the pack still supplies memory and flash data.
"""


def will_init_target(target, init_sequence):
    if (target.session.options.get("target_override") or "").lower() == "gd32h77diw":
        # Returning False selects DPConnector.connect(), which retries the SWJ
        # handshake and can switch to the dormant activation sequence.
        target.dp.connect_debug_port_hook = lambda: False
