'''
Copyright (C) 2017 Jeremy Legigan AKA Pistiwique


Created by Jeremy Legigan AKA Pistiwique

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Linked Scale",
    "description": "",
    "author": "Jeremy Legigan AKA Pistiwique",
    "version": (0, 0, 1),
    "blender": (2, 78, 0),
    "location": "View3D",
    "category": "Object"}

import bpy
from bpy.types import PropertyGroup, Panel
from bpy.props import FloatProperty, BoolProperty, EnumProperty, \
    PointerProperty


def get_constraint_axis(axis):
    sfp = bpy.context.window_manager.sfp_props
    multi_constraint = {'ALL': (True, True, True),
                        'X_Y': (True, True, False),
                        'X_Z': (True, False, True),
                        'Y_Z': (False, True, True),
                        }

    single_constraint = {0: (True, False, False),
                         1: (False, True, False),
                         2: (False, False, True),
                         }

    if sfp.linked_axis != 'FREE':
        if (axis == 0 and sfp.linked_axis not in {'ALL', 'X_Y', 'X_Z'}) or \
                (axis == 1 and sfp.linked_axis not in {'ALL', 'X_Y', 'Y_Z'}) or \
                (axis == 2 and sfp.linked_axis not in {'ALL', 'X_Z', 'Y_Z'}):
            return single_constraint[axis]

        return multi_constraint[sfp.linked_axis]

    return single_constraint[axis]


def update_axis(axis_idx, ratio):
    constraint_axis = get_constraint_axis(axis_idx)

    bpy.ops.transform.resize(value=(ratio, ratio, ratio), constraint_axis
                             =constraint_axis, constraint_orientation=
                             bpy.context.space_data.transform_orientation
                             )


def get_dimension(self, axis):
    return bpy.context.object.dimensions[axis]


def set_dimension(self, value, axis):
    if value <= 0:
        value = 0.001

    axis_dict = {0: self.dim_x,
                 1: self.dim_y,
                 2: self.dim_z
                 }

    update_axis(axis, value / axis_dict[axis])


#  -------------  COLLECTION PROPERTY -------------  #

class ScaleFromLengthProperties(PropertyGroup):
    dim_x = FloatProperty(
            name="Dimension X",
            description="Absolute bounding box of the object",
            soft_min=0.001,
            precision=3,
            get=lambda s: get_dimension(s, 0),
            set=lambda s, v: set_dimension(s, v, 0),
            unit='LENGTH',
            )

    dim_y = FloatProperty(
            name="Dimension Y",
            description="Absolute bounding box of the object",
            soft_min=0.001,
            precision=3,
            get=lambda s: get_dimension(s, 1),
            set=lambda s, v: set_dimension(s, v, 1),
            unit='LENGTH',
            )

    dim_z = FloatProperty(
            name="Dimension Z",
            description="Absolute bounding box of the object",
            soft_min=0.001,
            precision=3,
            get=lambda s: get_dimension(s, 2),
            set=lambda s, v: set_dimension(s, v, 2),
            unit='LENGTH',
            )

    ratio = FloatProperty()

    linked_axis = EnumProperty(
            name="Linked axis",
            items=(('ALL', "All", ""),
                   ('X_Y', "X-Y", ""),
                   ('X_Z', "X-Z", ""),
                   ('Y_Z', "Y-Z", ""),
                   ('FREE', "Free", "")),
            default='ALL',
            )


#  ----------------  PANEL  ----------------  #

class TestPanel(Panel):
    bl_idname = "linked_scale"
    bl_label = "Linked Scale"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        sfp = context.window_manager.sfp_props
        layout.prop(sfp, "linked_axis", expand=True)
        col = layout.column(align=True)
        col.prop(sfp, "dim_x", text="X")
        col.prop(sfp, "dim_y", text="Y")
        col.prop(sfp, "dim_z", text="Z")


#  --------------  REGISTER  --------------  #

def register():
    bpy.utils.register_module(__name__)

    bpy.types.WindowManager.sfp_props = PointerProperty(
        type=ScaleFromLengthProperties)


def unregister():
    del bpy.types.WindowManager.sfp_props

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()