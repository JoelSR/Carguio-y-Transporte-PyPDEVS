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
        #print(self.elapsed,inputs.get(self.in_event))
        # Calculate time in queue
        #print(evt)
        inputData = inputs.get(self.in_event)
        #evt = inputs[self.in_event]
        #time = self.state.current_time - evt.creation_time - evt.processing_time
        #inputs[self.in_event].data = inputs.get(self.in_event)#max(0.0, time)
        """if("camion"in inputData[0]):
                                    self.state.events["camiones"].append(inputData)
                                else:
                                    self.state.events["palas"].append(inputData)"""
        self.state.events.append(inputData)
        return self.state

    # Don't define anything else, as we only store events.
    # Collector has no behaviour of its own.