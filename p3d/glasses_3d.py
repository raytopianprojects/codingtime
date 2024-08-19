from direct.showbase.ShowBase import ShowBase
from panda3d.core import load_prc_file_data

# Enable Effecct
load_prc_file_data("", """red-blue-stereo 1
red-blue-stereo-colors yellow|magenta red|blue
""")
# Add this to change which colors are used
# red-blue-stereo-colors green cyan
# use the pipe operator for better effect
# red-blue-stereo-colors green|cyan red|blue

window = ShowBase()
forest = window.loader.load_model("environment")
forest.reparent_to(window.render)
forest.setScale(0.25, 0.25, 0.25)
forest.setPos(-8, 42, 0)

from math import sin, cos, pi


def move_camera(task):
    angle_degrees = task.time * 6.0

    angle_radians = angle_degrees * (pi / 180.0)

    window.camera.set_pos(20 * sin(angle_radians), -20 * cos(angle_radians), 3)

    window.camera.set_hpr(angle_degrees, 0, 0)

    return task.cont


window.taskMgr.add(move_camera)

from direct.actor.Actor import Actor

panda = Actor("models/panda",
              {"walk": "models/panda-walk"})

panda.setScale(0.3, 0.3, 0.3)
panda.reparentTo(window.render)
panda.loop("walk")

from direct.interval.IntervalGlobal import Sequence

pos_interval1 = panda.posInterval(13,
                                  (0, -10, 0),
                                  startPos=(0, 10, 0))

pos_interval2 = panda.posInterval(13,
                                  (0, 10, 0),
                                  startPos=(0, -10, 0))

hpr_interval1 = panda.hprInterval(3,
                                  (180, 0, 0),
                                  startHpr=(0, 0, 0))

hpr_interval2 = panda.hprInterval(3,
                                  (0, 0, 0),
                                  startHpr=(180, 0, 0))

# Create and play the sequence that coordinates the intervals.

panda_pace = Sequence(pos_interval1, hpr_interval1,
                      pos_interval2, hpr_interval2,
                      name="panda")

panda_pace.loop()

from panda3d.core import DirectionalLight, AmbientLight

sun = DirectionalLight("Sun")

sun.setShadowCaster(True, 2048, 2048)

sun_nodepath = window.render.attach_new_node(sun)
sun_nodepath.set_p(-30)

bmin, bmax = window.render.get_tight_bounds(sun_nodepath)
lens = sun.get_lens()
lens.set_film_offset((bmin.xz + bmax.xz) * 0.5)
lens.set_film_size(bmax.xz - bmin.xz)
lens.set_near_far(bmin.y, bmax.y)

window.render.set_light(sun_nodepath)

ambient = AmbientLight("Ambient")
ambient.set_color((0.5, 0.5, 0.5, 1))
ambient_nodepath = window.render.attach_new_node(ambient)
window.render.set_light(ambient_nodepath)

window.render.set_shader_auto()

window.run()
