"""
Dispatcher: Event loop and callback system for neurons.
"""
import asyncio

class Dispatcher:
    def __init__(self):
        self.neurons = []
        self.event_queue = asyncio.Queue()

    def register(self, neuron):
        self.neurons.append(neuron)

    async def dispatch(self):
        while True:
            event = await self.event_queue.get()
            for neuron in self.neurons:
                await neuron.on_event(event['value'], event.get('source'))

    async def emit(self, value, source=None):
        await self.event_queue.put({'value': value, 'source': source})
