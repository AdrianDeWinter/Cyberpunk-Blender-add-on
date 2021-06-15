import bpy
import os
from ..main.common import imageFromPath

class Humanskin:
    def __init__(self, BasePath, valueToIgnore,image_format):
        self.BasePath = BasePath
        self.valueToIgnore = valueToIgnore
        self.image_format = image_format
    def create(self,Skin,Mat):
        CurMat = Mat.node_tree
        CurMat.nodes['Principled BSDF'].inputs['Subsurface'].default_value = 0.012
        if Skin.get("normal"):
            nImg = imageFromPath(self.BasePath + Skin["normal"],self.image_format,True)
            
            nImgNode = CurMat.nodes.new("ShaderNodeTexImage")
            nImgNode.location = (-800,-250)
            nImgNode.image = nImg
            nImgNode.label = "normal"

            Sep = CurMat.nodes.new("ShaderNodeSeparateRGB")
            Sep.location = (-500,-250)
            Sep.hide = True
            
            Comb = CurMat.nodes.new("ShaderNodeCombineRGB")
            Comb.location = (-350,-250)
            Comb.hide = True
            
            CurMat.links.new(nImgNode.outputs[0],Sep.inputs[0])
            CurMat.links.new(Sep.outputs[0],Comb.inputs[0])
            CurMat.links.new(Sep.outputs[1],Comb.inputs[1])
            Comb.inputs[2].default_value = 1
            
            nMap = CurMat.nodes.new("ShaderNodeNormalMap")
            nMap.location = (-150,-250)
            nMap.hide = True

            CurMat.links.new(Comb.outputs[0],nMap.inputs[1])
            
            CurMat.links.new(nMap.outputs[0],CurMat.nodes['Principled BSDF'].inputs['Normal'])
        
        if Skin.get("albedo"):
            aImg = imageFromPath(self.BasePath + Skin["albedo"],self.image_format)
            
            aImgNode = CurMat.nodes.new("ShaderNodeTexImage")
            aImgNode.location = (-300,200)
            aImgNode.image = aImg
            aImgNode.label = "albedo"

            CurMat.links.new(aImgNode.outputs[0],CurMat.nodes['Principled BSDF'].inputs['Base Color'])
            
        if Skin.get("tintColor"):
            tColor = CurMat.nodes.new("ShaderNodeRGB")
            tColor.location = (-300,200)
            tColor.hide = True
            tColor.label = "tintColor"
            tColor.outputs[0].default_value = (float(Skin["tintColor"]["x"]),float(Skin["tintColor"]["y"]),float(Skin["tintColor"]["z"]),float(Skin["tintColor"]["w"]))
        
        if Skin.get("tintColorMask"):
            tmaskImg = imageFromPath(self.BasePath + Skin["tintColorMask"],self.image_format)
            
            tmaskNode = CurMat.nodes.new("ShaderNodeTexImage")
            tmaskNode.location = (-500,200)
            tmaskNode.image = tmaskImg
            tmaskNode.hide = True
            tmaskNode.label = "tintColorMask"

        if Skin.get("roughness"):
            rImg = imageFromPath(self.BasePath + Skin["roughness"],self.image_format)
            
            rImgNode = CurMat.nodes.new("ShaderNodeTexImage")
            rImgNode.location = (-600,100)
            rImgNode.image = rImg
            rImgNode.hide = True
            rImgNode.label = "roughness"

        if Skin.get("detailNormal"):
            ndImg = imageFromPath(self.BasePath + Skin["detailNormal"],self.image_format)
            
            ndImgNode = CurMat.nodes.new("ShaderNodeTexImage")
            ndImgNode.location = (-600,0)
            ndImgNode.image = ndImg
            ndImgNode.hide = True
            ndImgNode.label = "detailNormal"

        if Skin.get("detailNormalInfluence"):
            ndInfluence = CurMat.nodes.new("ShaderNodeValue")
            ndInfluence.location = (-600,0)
            ndInfluence.outputs[0].default_value = float(Skin["detailNormalInfluence"])
            ndInfluence.hide = True
            ndInfluence.label = "detailNormalInfluence"

        if Skin.get("detailmap_Squash"):
            ndSqImg = imageFromPath(self.BasePath + Skin["detailmap_Squash"],self.image_format)
            
            ndSqImgNode = CurMat.nodes.new("ShaderNodeTexImage")
            ndSqImgNode.location = (-800,-100)
            ndSqImgNode.image = ndSqImg
            ndSqImgNode.hide = True
            ndSqImgNode.label = "detailmap_Squash"

        if Skin.get("detailmap_Stretch"):
            ndStImg = imageFromPath(self.BasePath + Skin["detailmap_Stretch"],self.image_format)
            
            ndStImgNode = CurMat.nodes.new("ShaderNodeTexImage")
            ndStImgNode.location = (-1100,-100)
            ndStImgNode.image = ndStImg
            ndStImgNode.hide = True
            ndStImgNode.label = "detailmap_Stretch"