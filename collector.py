from pypdevs.DEVS import AtomicDEVS

# Define the state of the collector as a structured object
class CollectorState(object):
    def __init__(self):
        # Contains received events and simulation time
        #self.events = {"camiones":[],"palas":[]}
        self.events = []
        self.current_time = 0.0

class Collector(AtomicDEVS):
    def __init__(self,cQ,pQ):

        self.camiones = []
        self.palas = []

        AtomicDEVS.__init__(self, "Collector")
        self.state = CollectorState()
        # Has only one input port
        self.in_event = self.addInPort("in_event")

    def extTransition(self, inputs):
        # Update simulation time
        self.state.current_time += self.elapsed
        inputData = inputs.get(self.in_event)
        inputData[1] = self.state.current_time
        self.state.events.append(inputData)
        return self.state

    # Don't define anything else, as we only store events.
    # Collector has no behaviour of its own.
