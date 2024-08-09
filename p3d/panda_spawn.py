from direct.showbase.ShowBase import ShowBase
from random import random, randint

window = ShowBase()

load_model = window.loader.load_model


def spawn_panda():
    panda = load_model("panda")
    panda.reparent_to(window.render)

    scale = randint(0, 10) + random()
    panda.set_scale((scale, scale, scale))

    panda.set_pos((randint(-1000, 1000) + random(), randint(-1000, 1000) + random(), randint(-1000, 1000) + random()))

    panda.set_hpr((randint(-180, 180), randint(-180, 180), randint(-180, 180)))

    #panda.set_shear((12, 0, 1))

    panda.set_color((random(), random(), random(), random()))


window.accept("a", spawn_panda)


async def spawn_panda_task(task):
    panda = load_model("panda")
    panda.reparent_to(window.render)

    scale = randint(0, 10) + random()
    panda.set_scale((scale, scale, scale))

    panda.set_pos((randint(-100, 100) + random(), randint(-100, 100) + random(), randint(-100, 100) + random()))

    await task.pause(0.5)

    panda.set_hpr((randint(-180, 180), randint(-180, 180), randint(-180, 180)))

    #panda.set_shear((12, 0, 1))

    panda.set_color((random(), random(), random(), random()))

    return task.cont


window.add_task(spawn_panda_task)

window.run()
