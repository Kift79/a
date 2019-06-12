#!/usr/bin/env python
from math import pi as PI
from I3Tray import I3Tray
from icecube import icetray, dataio, dataclasses, phys_services

@icetray.traysegment
def GeneratorSegment(tray, name):
    def generator(frame):
        frame["tree"] = dataclasses.I3MCTree()

    tray.Add("I3InfiniteSource")
    tray.Add(generator, streams=[icetray.I3Frame.DAQ])
    tray.Add(lambda frame: frame.Has("tree"), streams=[icetray.I3Frame.DAQ])

class ExampleModule(icetray.I3Module):
    def __init__(self, context):
        icetray.I3Module.__init__(self, context)
        self.AddParameter("RNG", 'I3RandomService', None)

    def Configure(self):
        self.rng = self.GetParameter("RNG")
        if not self.rng:
            self.rng = self.context["I3RandomService"]
            if not self.rng:
                icetray.logging.log_fatal("No RNG found!!!")

    def DAQ(self, frame):
        random_number = self.rng.uniform(PI)
        frame['RandomNumber'] = dataclasses.I3Double(random_number)
        self.PushFrame(frame)
        
tray = I3Tray()
tray.context['I3RandomService'] = phys_services.I3GSLRandomService(42)
tray.Add(GeneratorSegment)
tray.Add(ExampleModule)
tray.Add("Dump")
tray.Execute(10)

             
