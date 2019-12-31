import bpy
import math
import os
import sys


#cancel anything we were doing
bpy.ops.object.mode_set( mode = "OBJECT" )
bpy.ops.object.select_all(action='DESELECT')

#apply any rotation
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
bpy.ops.object.select_all(action='DESELECT')

BoneNameMap = {
    "Hips": "Pelvis",
    "Spine": "spine_01",
    "Spine1":"spine_02",
    "Spine2":"spine_03",
    "LeftShoulder":"clavicle_l",
    "LeftArm":"UpperArm_L",
    "LeftForeArm":"lowerarm_l",
    "LeftHand":"Hand_L",
    "LeftHandIndex1":"index_01_l",
    "LeftHandIndex2":"index_02_l",
    "LeftHandIndex3":"index_03_l",
    "LeftHandMiddle1":"middle_01_l",
    "LeftHandMiddle2":"middle_02_l",
    "LeftHandMiddle3":"middle_03_l",
    "LeftHandPinky1":"pinky_01_l",
    "LeftHandPinky2":"pinky_02_l",
    "LeftHandPinky3":"pinky_03_l",
    "LeftHandRing1":"ring_01_l",
    "LeftHandRing2":"ring_02_l",
    "LeftHandRing3":"ring_03_l",
    "LeftHandThumb1":"thumb_01_l",
    "LeftHandThumb2":"thumb_02_l",
    "LeftHandThumb3":"thumb_03_l",
    "RightShoulder":"clavicle_r",
    "RightArm":"UpperArm_R",
    "RightForeArm":"lowerarm_r",
    "RightHand":"Hand_R",
    "RightHandIndex1":"index_01_r",
    "RightHandIndex2":"index_02_r",
    "RightHandIndex3":"index_03_r",
    "RightHandMiddle1":"middle_01_r",
    "RightHandMiddle2":"middle_02_r",
    "RightHandMiddle3":"middle_03_r",
    "RightHandPinky1":"pinky_01_r",
    "RightHandPinky2":"pinky_02_r",
    "RightHandPinky3":"pinky_03_r",
    "RightHandRing1":"ring_01_r",
    "RightHandRing2":"ring_02_r",
    "RightHandRing3":"ring_03_r",
    "RightHandThumb1":"thumb_01_r",
    "RightHandThumb2":"thumb_02_r",
    "RightHandThumb3":"thumb_03_r",
    "Neck":"neck_01",
    "Head":"head",
    "LeftUpLeg":"Thigh_L",
    "LeftLeg":"calf_l",
    "LeftFoot":"Foot_L",
    "LeftToeBase":"ball_l",
    "RightUpLeg":"Thigh_R",
    "RightLeg":"calf_r",
    "RightFoot":"Foot_R",
    "RightToeBase":"ball_r"
}

def FixArmature(armature):
    bpy.data.objects[armature.name].select_set(True)
    theRootNodeName = armature.data.bones[0].name
    index = theRootNodeName.find(":")
    if index != -1:
        index = index + 1
        for bone in armature.data.bones:
            bone.name = bone.name[index:]
            if bone.name in BoneNameMap.keys():
                bone.name = BoneNameMap[bone.name]
    bpy.ops.object.mode_set(mode = "EDIT")
    for bone in armature.data.edit_bones:
        if bone.parent == None:
            oldRoot = bone
            break
    root_bone = armature.data.edit_bones.new('Root')
    root_bone.tail = oldRoot.head
    oldRoot.parent = root_bone
        
    keyframes = []
    anim = armature.animation_data
    if anim is not None and anim.action is not None:
        for fcu in anim.action.fcurves:
            if fcu.data_path == "pose.bones[\"Pelvis\"].location":
                #print(fcu.data_path)
                for keyframe in fcu.keyframe_points:
                    x, y = keyframe.co
                    if x not in keyframes:
                        keyframes.append((math.ceil(x)))

    if len(keyframes) > 0:
        #print(len(keyframes))
        bpy.ops.object.posemode_toggle()
        for i in range(keyframes[-1] - keyframes[0]):
            bpy.context.scene.frame_set(i + keyframes[0] + 1)
            armature.pose.bones["Pelvis"].location[0] = 0
            armature.pose.bones["Pelvis"].location[2] = 0
            bpy.ops.anim.keyframe_insert_menu(type='Location')                  
            

    bpy.ops.object.mode_set ( mode = "OBJECT" )
    bpy.ops.object.select_all(action='DESELECT')       
    bpy.data.objects[armature.name].select_set(False)


#pass through each armature in the scene and remove the mixamo: text from the bone names
for armature in [ob for ob in bpy.data.objects if ob.type == 'ARMATURE']:
    FixArmature(armature)

 

print("DONE") 