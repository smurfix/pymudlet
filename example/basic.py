#!/usr/bin/python3

from mudlet import Server
import trio
from mudlet.util import ValueEvent
from functools import partial
import logging

class S(Server):
    async def hello2(self, prompt,e):
        await trio.sleep(2)
        # from here you could again call mudlet
        e.set("Hello, "+prompt)

    def hello(self, prompt):
        e = ValueEvent()
        # do not call into Mudlet from here, you will deadlock
        self.main.start_soon(self.hello2,prompt,e)
        return e

    async def run(self):
        print("connected")
        bb = await self.mud.py.backoff
        print("current back-off is",bb)

        self.register_call("hello", self.hello)

        async with self.events("gmcp.MG.room.info") as h:
            async for msg in h:
                info = await self.mud.gmcp.MG.room.info
                print("ROOM",info)

async def main():
    async with S(cfg=dict(name="sample_basic")) as s:
        await s.run()
logging.basicConfig(level=logging.INFO)
trio.run(main)
