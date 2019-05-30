import asyncio
import logging

import _signal
from _signal import signal
from discordia import Discordia

log = logging.getLogger(__name__)


class Kharabot():
    def __init__(self, token):
        self.loop = asyncio.get_event_loop()
        self.discordtoken = token
        self.discord = Discordia(loop=self.loop)

    def run(self):
        loop = self.loop

        try:
            loop.add_signal_handler(_signal.SIGINT, lambda: loop.stop())
            loop.add_signal_handler(_signal.SIGTERM, lambda: loop.stop())
        except NotImplementedError:
            pass

        async def runner():
            await self.discord.go(self.discordtoken)

        def stop_loop_on_completion(f):
            loop.stop()

        future = asyncio.ensure_future(runner(), loop=loop)
        future.add_done_callback(stop_loop_on_completion)
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            log.info('Received signal to terminate bot and event loop.')
        finally:
            future.remove_done_callback(stop_loop_on_completion)
            log.info('Cleaning up tasks.')
            self._cleanup_loop()

    def _cleanup_loop(self):
        loop = self.loop

        try:
            self._cancel_tasks()
        finally:
            log.info('Closing the event loop.')
            loop.close()

    def _cancel_tasks(self):
        loop = self.loop

        try:
            task_retriever = asyncio.Task.all_tasks
        except AttributeError:
            task_retriever = asyncio.all_tasks

        tasks = {t for t in task_retriever(loop=loop) if not t.done()}

        if not tasks:
            return

        log.info('Cleaning up after %d tasks.', len(tasks))
        for task in tasks:
            task.cancel()

        loop.run_until_complete(asyncio.gather(
            *tasks, loop=loop, return_exceptions=True))
        log.info('All tasks finished cancelling.')

        for task in tasks:
            if task.cancelled():
                continue
            if task.exception() is not None:
                msg = 'Unhandled exception during Kharabot.run shutdown.'
                loop.call_exception_handler({
                    'message': msg,
                    'exception': task.exception(),
                    'task': task
                })