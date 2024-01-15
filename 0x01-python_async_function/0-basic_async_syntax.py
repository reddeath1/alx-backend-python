#!/usr/bin/env python3
"""
Write asynchronous coroutine
Takes integer as an argument max_delay
"""

import random
import asyncio


async def wait_random(max_delay: int = 10) -> float:
    """
    Asynchronous coroutine
    max_delay
    """
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)

    return delay
