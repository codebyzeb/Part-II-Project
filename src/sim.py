from environment import Environment
from entity import Entity, ACTION
import time


class Simulation:

    numEpochs = 0
    numCycles = 0
    entity = None

    def __init__(self, epochs, cycles, ent):
        self.numEpochs = epochs
        self.numCycles = cycles
        self.entity = ent

    def run(self, debug=True):
        self.entity = Entity()
        env = Environment()
        env.placeEntity()

        # Do whole simulation
        for epoch in range(self.numEpochs):

            # Do an epoch
            for step in range(self.numCycles):
                entityPos = env.getEntityPosition()
                mushDist, mushPos = env.closestMushroom(entityPos)

                angle = env.getAngle(entityPos, mushPos)
                mush = env.getCell(mushPos) if env.adjacent(
                    entityPos, mushPos) else 0
                action, _ = self.entity.behaviourManual(
                    angle, mush, (0.5, 0.5, 0.5))

                if (debug):
                    print("Epoch:", epoch, "   Cycle:", step)
                    print(env)
                    print("Entity energy:", self.entity.energy)
                    print("Entity position: (",
                          entityPos[0],
                          ",",
                          entityPos[1],
                          ")",
                          sep="")
                    print("Closest mushroom position: (",
                          mushPos[0],
                          ",",
                          mushPos[1],
                          ")",
                          sep="")
                    print("Direction: ", env.entityDirection)
                    print("Angle: ", angle)
                    print("Mushroom input: ", mush)
                    print("Action chosen: ", action)
                    ##time.sleep(0.1)
                    input()

                env.moveEntity(action)
                if (env.entityPosition == mushPos):
                    self.entity.eat(env.getCell(mushPos))
                    env.clearCell(mushPos)

            env.reset()
            env.placeEntity()


sim = Simulation(5, 50, Entity())
sim.run(debug=True)
