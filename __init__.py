import bpy
from bpy.props import (
    StringProperty,
    BoolProperty,
    FloatProperty,
    EnumProperty,
)
from bpy_extras.io_utils import (
    ImportHelper,
    ExportHelper,
    path_reference_mode,
    axis_conversion,
)

# 多语言支持
def get_translation_dict():
    """根据Blender版本返回对应的翻译字典"""
    translations_dict = {
        "en_US": {
            ("*", "Export Datasmith"): "Export Datasmith",
            ("*", "Selected objects only"): "Selected objects only",
            ("*", "Export animations"): "Export animations",
            ("*", "Apply modifiers"): "Apply modifiers",
            ("*", "Skip meshes and textures"): "Skip meshes and textures",
            ("*", "Use sRGB gamma hack (UE 4.24 and below)"): "Use sRGB gamma hack (UE 4.24 and below)",
            ("*", "Compatibility mode"): "Compatibility mode",
            ("*", "Write metadata"): "Write metadata",
            ("*", "Enable logging"): "Enable logging",
            ("*", "Enable profiling"): "Enable profiling",
            ("*", "Description"): "Export scene as Datasmith asset",
            ("*", "Exports only the selected objects"): "Exports only the selected objects",
            ("*", "Export object animations (transforms only)"): "Export object animations (transforms only)",
            ("*", "Applies geometry modifiers when exporting. (This may break mesh instancing)"): "Applies geometry modifiers when exporting. (This may break mesh instancing)",
            ("*", "Allows for faster exporting, useful if you only changed transforms or shaders"): "Allows for faster exporting, useful if you only changed transforms or shaders",
            ("*", "Flags sRGB texture to use gamma as sRGB is not supported in old versions"): "Flags sRGB texture to use gamma as sRGB is not supported in old versions",
            ("*", "Enable this if you don't have the UE4 plugin, Improves material nodes support, but at a reduced quality"): "Enable this if you don't have the UE4 plugin, Improves material nodes support, but at a reduced quality",
            ("*", "Writes custom properties of objects and meshes as metadata.\nIt may be useful to disable this when using certain addons"): "Writes custom properties of objects and meshes as metadata.\nIt may be useful to disable this when using certain addons",
            ("*", "Enable logging to Window > System console"): "Enable logging to Window > System console",
            ("*", "For development only, writes a python profile 'datasmith.prof'"): "For development only, writes a python profile 'datasmith.prof'",
        },
    }

    # 根据Blender版本选择合适的中文locale ID
    if bpy.app.version >= (4, 0, 0):
        locale_id = "zh_HANS"
    else:
        locale_id = "zh_CN"

    translations_dict[locale_id] = {
        ("*", "Export Datasmith"): "导出 Datasmith",
        ("*", "Selected objects only"): "仅导出选中对象",
        ("*", "Export animations"): "导出动画",
        ("*", "Apply modifiers"): "应用修改器",
        ("*", "Skip meshes and textures"): "跳过网格和纹理",
        ("*", "Use sRGB gamma hack (UE 4.24 and below)"): "使用 sRGB gamma 修复（UE 4.24 及以下）",
        ("*", "Compatibility mode"): "兼容模式",
        ("*", "Write metadata"): "写入元数据",
        ("*", "Enable logging"): "启用日志记录",
        ("*", "Enable profiling"): "启用性能分析",
        ("*", "Description"): "将场景导出为Datasmith资产",
        ("*", "Exports only the selected objects"): "只导出选中的对象",
        ("*", "Export object animations (transforms only)"): "导出对象动画（仅变换）",
        ("*", "Applies geometry modifiers when exporting. (This may break mesh instancing)"): "导出时应用几何体修改器。（这可能会破坏网格实例化）",
        ("*", "Allows for faster exporting, useful if you only changed transforms or shaders"): "允许更快地导出，如果您仅更改了变换或着色器则很有用",
        ("*", "Flags sRGB texture to use gamma as sRGB is not supported in old versions"): "标记sRGB纹理以使用gamma，因为在旧版本中不支持sRGB",
        ("*", "Enable this if you don't have the UE4 plugin, Improves material nodes support, but at a reduced quality"): "如果您没有UE4插件，则启用此选项，改进材质节点支持，但质量会有所降低",
        ("*", "Writes custom properties of objects and meshes as metadata.\nIt may be useful to disable this when using certain addons"): "将对象和网格的自定义属性作为元数据写入。当使用某些插件时，禁用此功能可能有用",
        ("*", "Enable logging to Window > System console"): "启用日志记录到窗口 > 系统控制台",
        ("*", "For development only, writes a python profile 'datasmith.prof'"): "仅用于开发，写入一个Python分析文件 'datasmith.prof'",
    }

    return translations_dict

def register_translations():
    translations_dict = get_translation_dict()
    bpy.app.translations.register(__name__, translations_dict)

def unregister_translations():
    bpy.app.translations.unregister(__name__)

# 插件信息
bl_info = {
    "name": "Unreal Datasmith format",
    "author": "Andrés Botero",
    "version": (1, 0, 3),
    "blender": (4, 0, 0),
    "location": "File > Export > Datasmith (.udatasmith)",
    "description": "Export scene as Datasmith asset",  # 空字符串，将在UI中动态生成
    "warning": "",
    "category": "Import-Export",
    "support": 'COMMUNITY',
    "wiki_url": "https://github.com/0xafbf/blender-datasmith-export",
}

if "bpy" in locals():
    import importlib
    if "export_datasmith" in locals():
        importlib.reload(export_datasmith)

class ExportDatasmith(bpy.types.Operator, ExportHelper):
    """Write a Datasmith file"""
    bl_idname = "export_scene.datasmith"
    bl_label = "Export Datasmith"
    bl_options = {'PRESET'}

    filename_ext = ".udatasmith"
    filter_glob: StringProperty(default="*.udatasmith", options={'HIDDEN'})

    export_selected: BoolProperty(
        name="Selected objects only",
        description="Exports only the selected objects",
        default=False,
    )
    export_animations: BoolProperty(
        name="Export animations",
        description="Export object animations (transforms only)",
        default=True,
    )
    apply_modifiers: BoolProperty(
        name="Apply modifiers",
        description="Applies geometry modifiers when exporting. "
                   "(This may break mesh instancing)",
        default=True,
    )
    minimal_export: BoolProperty(
        name="Skip meshes and textures",
        description="Allows for faster exporting, useful if you only changed "
                   "transforms or shaders",
        default=False,
    )
    use_gamma_hack: BoolProperty(
        name="Use sRGB gamma hack (UE 4.24 and below)",
        description="Flags sRGB texture to use gamma as sRGB is not supported in old versions",
        default=False,
    )
    compatibility_mode: BoolProperty(
        name="Compatibility mode",
        description="Enable this if you don't have the UE4 plugin, "
                   "Improves material nodes support, but at a reduced quality",
        default=False,
    )
    write_metadata: BoolProperty(
        name="Write metadata",
        description="Writes custom properties of objects and meshes as metadata.\nIt may be useful to disable this when using certain addons",
        default=True,
    )
    use_logging: BoolProperty(
        name="Enable logging",
        description="Enable logging to Window > System console",
        default=False,
    )
    use_profiling: BoolProperty(
        name="Enable profiling",
        description="For development only, writes a python profile 'datasmith.prof'",
        default=False,
    )

    def execute(self, context):
        keywords = self.as_keywords(ignore=("filter_glob",))
        from . import export_datasmith
        profile = keywords["use_profiling"]
        if not profile:
            return export_datasmith.save(context, **keywords)
        else:
            import cProfile
            pr = cProfile.Profile()
            pr.enable()
            result = export_datasmith.save(context, **keywords)
            pr.disable()
            path = "datasmith.prof"
            pr.dump_stats(path)
            return result

def menu_func_export(self, context):
    self.layout.operator(ExportDatasmith.bl_idname, text="Datasmith (.udatasmith)")

def register():
    bpy.utils.register_class(ExportDatasmith)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    register_translations()  # 注册多语言支持

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.utils.unregister_class(ExportDatasmith)
    unregister_translations()  # 注销多语言支持

if __name__ == "__main__":
    register()