##############################################################
# Attribute Editor Tool (PyMel Version)
# Created By: Garvin Beltz
# Version: 1.0
# Last Update: 11/16/2022

# Tool allows for a user to mass edit attributes of selected
# objects with a user provided prefix or suffix. The current 
# version of this program allows the user to locked, hidden,
# or keyable settings of attributes.

# NOTE: The "Extra" and "Custom Attibutes" options do not 
# currently work.
##############################################################
import pymel.core as pm

class AE_Window(object):
    # Window Constructor
    def __init__(self):
        
        # Creates initial name and dimensions of window
        self.window = ("AE Window") 
        self.title = "Attribute Editor 1.0"
        self.size = (400,400)
        
        # Closes old version of window before creating new one
        if pm.window(self.window, exists=True):
            pm.deleteUI(self.window, window=True)
            
        # Creates new version of window
        self.window = pm.window(self.window, title=self.title, widthHeight=self.size)
        pm.columnLayout(adjustableColumn=True)
        
        # Creates all the text and buttons of the window
        pm.text(label='Naming Convention Prefix/Suffix')
        self.geoNaming = pm.textFieldGrp(label='Geometry: ', text='_Geo')
        self.geoNamingToggle= pm.checkBoxGrp(label='Apply Edits: ')
        self.jntNaming = pm.textFieldGrp(label='Joint: ', text='_Jnt')
        self.jntNamingToggle= pm.checkBoxGrp(label='Apply Edits: ')
        self.ctrlNaming = pm.textFieldGrp(label='Control: ', text='_Ctrl')
        self.ctrlNamingToggle= pm.checkBoxGrp(label='Apply Edits: ')
        self.grpNaming = pm.textFieldGrp(label='Group: ', text='_Grp')
        self.grpNamingToggle= pm.checkBoxGrp(label='Apply Edits: ')
        self.xtraNaming = pm.textFieldGrp(label='Extra: ')
        self.xtraNamingToggle= pm.checkBoxGrp(label='Apply Edits: ')
        
        pm.separator(height=20)
        pm.text(label='Translation')
        self.xTranslate = pm.checkBoxGrp(numberOfCheckBoxes=3, label='Translate X: ', label1='Locked', label2='Hidden', label3='Nonkeyable')
        self.yTranslate = pm.checkBoxGrp(numberOfCheckBoxes=3, label='Translate Y: ', label1='Locked', label2='Hidden', label3='Nonkeyable')
        self.zTranslate = pm.checkBoxGrp(numberOfCheckBoxes=3, label='Translate Z: ', label1='Locked', label2='Hidden', label3='Nonkeyable')
        
        pm.separator(height=20)
        pm.text(label='Rotation')
        self.xRotate = pm.checkBoxGrp(numberOfCheckBoxes=3, label='Rotate X: ', label1='Locked', label2='Hidden', label3='Nonkeyable')
        self.yRotate = pm.checkBoxGrp(numberOfCheckBoxes=3, label='Rotate Y: ', label1='Locked', label2='Hidden', label3='Nonkeyable')
        self.zRotate = pm.checkBoxGrp(numberOfCheckBoxes=3, label='Rotate Z: ', label1='Locked', label2='Hidden', label3='Nonkeyable')
        
        pm.separator(height=20)
        pm.text(label='Scale')
        self.xScale = pm.checkBoxGrp(numberOfCheckBoxes=3, label='Scale X: ', label1='Locked', label2='Hidden', label3='Nonkeyable')
        self.yScale = pm.checkBoxGrp(numberOfCheckBoxes=3, label='Scale Y: ', label1='Locked', label2='Hidden', label3='Nonkeyable')
        self.zScale = pm.checkBoxGrp(numberOfCheckBoxes=3, label='Scale Z: ', label1='Locked', label2='Hidden', label3='Nonkeyable')
        
        pm.separator(height=20)
        pm.text(label='Visability')
        self.viz = pm.checkBoxGrp(numberOfCheckBoxes=3, label='Visability: ', label1='Locked', label2='Hidden', label3='Nonkeyable')
        
        pm.separator(height=20)
        pm.text(label='Custom Attributes')
        self.customName = pm.textFieldGrp(label='Attribute Name: ')
        self.customEdit = pm.checkBoxGrp(numberOfCheckBoxes=3, label='Custom Attribute: ', label1='Locked', label2='Hidden', label3='Nonkeyable')
        
        self.editAttributesBtn = pm.button(label='Edit Attributes', command=self.editAttribute)
        
        # Display the window
        pm.showWindow()
        
    # Function to determine what of the users selection wil be edited
    def getTargets(self):
        # Gets the user supplied name and if it is editable or not
        geoName = pm.textFieldGrp(self.geoNaming, query=True, text=True)
        geoEdit = pm.checkBoxGrp(self.geoNamingToggle, query=True, value1=True)
        jntName = pm.textFieldGrp(self.jntNaming, query=True, text=True)
        jntEdit = pm.checkBoxGrp(self.jntNamingToggle, query=True, value1=True)
        ctrlName = pm.textFieldGrp(self.ctrlNaming, query=True, text=True)
        ctrlEdit = pm.checkBoxGrp(self.ctrlNamingToggle, query=True, value1=True)
        grpName = pm.textFieldGrp(self.grpNaming, query=True, text=True)
        grpEdit = pm.checkBoxGrp(self.grpNamingToggle, query=True, value1=True)
        xtraName = pm.textFieldGrp(self.xtraNaming, query=True, text=True)
        xtraEdit = pm.checkBoxGrp(self.xtraNamingToggle, query=True, value1=True)
        
        # Gets the users selection and creates empty lists
        selection = pm.ls(sl=True)    
        editable = []
        targets = []
        
        # If editable, adds the prefix/suffix to the editable list
        if geoEdit:
            editable.append(geoName)
        if jntEdit:
            editable.append(jntName)
        if ctrlEdit:
            editable.append(ctrlName)
        if grpEdit:
            editable.append(grpName)
        if xtraEdit:
            editable.append(xtraName)
        
        # Loops through user selection and adds objects that are editable to target list
        for edit in editable:
            for sel in selection:
                if sel.startswith(edit) or sel.endswith(edit):
                    targets.append(sel)
        return targets
    
    # Function to lock or unlock attributes  
    def lockAttribute(self, *args):
        targets = self.getTargets()
        txLock = pm.checkBoxGrp(self.xTranslate, query=True, value1=True)
        tyLock = pm.checkBoxGrp(self.yTranslate, query=True, value1=True)
        tzLock = pm.checkBoxGrp(self.zTranslate, query=True, value1=True)
        rxLock = pm.checkBoxGrp(self.xRotate, query=True, value1=True)
        ryLock = pm.checkBoxGrp(self.yRotate, query=True, value1=True)
        rzLock = pm.checkBoxGrp(self.zRotate, query=True, value1=True)
        sxLock = pm.checkBoxGrp(self.xScale, query=True, value1=True)
        syLock = pm.checkBoxGrp(self.yScale, query=True, value1=True)
        szLock = pm.checkBoxGrp(self.zScale, query=True, value1=True)
        vizLock = pm.checkBoxGrp(self.viz, query=True, value1=True)
        #customName = pm.textFieldGrp(self.customName, query=True, text=True)
        #customLock = pm.checkBoxGrp(self.customEdit, query=True, value1=True)
        
        # Translations
        if txLock:
            for target in targets:
                pm.setAttr(target.tx, lock=True)      
        else:
            for target in targets:
                pm.setAttr(target.tx, lock=False)          
        if tyLock:
            for target in targets:
                pm.setAttr(target.ty, lock=True)       
        else:
            for target in targets:
                pm.setAttr(target.ty, lock=False)        
        if tzLock:
            for target in targets:
                pm.setAttr(target.tz, lock=True)       
        else:
            for target in targets:
                pm.setAttr(target.tz, lock=False)
                
        # Rotations        
        if rxLock:
            for target in targets:
                pm.setAttr(target.rx, lock=True)        
        else:
            for target in targets:
                pm.setAttr(target.rx, lock=False)         
        if ryLock:
            for target in targets:
                pm.setAttr(target.ry, lock=True)        
        else:
            for target in targets:
                pm.setAttr(target.ry, lock=False)          
        if rzLock:
            for target in targets:
                pm.setAttr(target.rz, lock=True)        
        else:
            for target in targets:
                pm.setAttr(target.rz, lock=False)
                
        # Scales
        if sxLock:
            for target in targets:
                pm.setAttr(target.sx, lock=True)        
        else:
            for target in targets:
                pm.setAttr(target.sx, lock=False)         
        if syLock:
            for target in targets:
                pm.setAttr(target.sy, lock=True)        
        else:
            for target in targets:
                pm.setAttr(target.sy, lock=False)          
        if szLock:
            for target in targets:
                pm.setAttr(target.sz, lock=True)        
        else:
            for target in targets:
                pm.setAttr(target.sz, lock=False)
        
        # Visability        
        if vizLock:
            for target in targets:
                pm.setAttr(target.v, lock=True)
        else:
            for target in targets:
                pm.setAttr(target.v, lock=False)
        '''
        if customLock:
            for target in targets:
                pm.setAttr(target.customName, lock=True)
        else:
            for target in targets:
                pm.setAttr(target.customName, lock=False)
        '''
    
    # Function to hide or unhide attributes
    # NOTE: Hiding attributes also makes them nonkeyable
    def hideAttribute(self, *args):
        global txHide, tyHide, tzHide, rxHide, ryHide, rzHide, sxHide, syHide, szHide, vizHide
        targets = self.getTargets()
        txHide = pm.checkBoxGrp(self.xTranslate, query=True, value2=True)
        tyHide = pm.checkBoxGrp(self.yTranslate, query=True, value2=True)
        tzHide = pm.checkBoxGrp(self.zTranslate, query=True, value2=True)
        rxHide = pm.checkBoxGrp(self.xRotate, query=True, value2=True)
        ryHide = pm.checkBoxGrp(self.yRotate, query=True, value2=True)
        rzHide = pm.checkBoxGrp(self.zRotate, query=True, value2=True)
        sxHide = pm.checkBoxGrp(self.xScale, query=True, value2=True)
        syHide = pm.checkBoxGrp(self.yScale, query=True, value2=True)
        szHide = pm.checkBoxGrp(self.zScale, query=True, value2=True)
        vizHide = pm.checkBoxGrp(self.viz, query=True, value2=True)
        #customName = pm.textFieldGrp(self.customName, query=True, text=True)
        #customHide = pm.checkBoxGrp(self.customEdit, query=True, value1=True)
        
        # Translations
        if txHide:
            for target in targets:
                pm.setAttr(target.tx, keyable=False, channelBox=False)      
        else:
            for target in targets:
                pm.setAttr(target.tx, keyable=True, channelBox=True)          
        if tyHide:
            for target in targets:
                pm.setAttr(target.ty, keyable=False, channelBox=False)       
        else:
            for target in targets:
                pm.setAttr(target.ty, keyable=True, channelBox=True)        
        if tzHide:
            for target in targets:
                pm.setAttr(target.tz, keyable=False, channelBox=False)       
        else:
            for target in targets:
                pm.setAttr(target.tz, keyable=True, channelBox=True)
        
        # Rotations        
        if rxHide:
            for target in targets:
                pm.setAttr(target.rx, keyable=False, channelBox=False)        
        else:
            for target in targets:
                pm.setAttr(target.rx, keyable=True, channelBox=True)         
        if ryHide:
            for target in targets:
                pm.setAttr(target.ry, keyable=False, channelBox=False)        
        else:
            for target in targets:
                pm.setAttr(target.ry, keyable=True, channelBox=True)          
        if rzHide:
            for target in targets:
                pm.setAttr(target.rz, keyable=False, channelBox=False)        
        else:
            for target in targets:
                pm.setAttr(target.rz, keyable=True, channelBox=True)
        
        # Scales
        if sxHide:
            for target in targets:
                pm.setAttr(target.sx, keyable=False, channelBox=False)     
        else:
            for target in targets:
                pm.setAttr(target.sx, keyable=True, channelBox=True)         
        if syHide:
            for target in targets:
                pm.setAttr(target.sy, keyable=False, channelBox=False)        
        else:
            for target in targets:
                pm.setAttr(target.sy, keyable=True, channelBox=True)          
        if szHide:
            for target in targets:
                pm.setAttr(target.sz, keyable=False, channelBox=False)        
        else:
            for target in targets:
                pm.setAttr(target.sz, keyable=True, channelBox=True)
        
        # Visability        
        if vizHide:
            for target in targets:
                pm.setAttr(target.v, keyable=False, channelBox=False)
        else:
            for target in targets:
                pm.setAttr(target.v, keyable=True, channelBox=True)
        
        '''
        if customHide:
            for target in targets:
                pm.setAttr(target.customName, keyable=False)
        else:
            for target in targets:
                pm.setAttr(target.customName, keyable=True)
        '''
        
    # Function to adjust keyability of attributes
    def keyAttribute(self, *args):
        targets = self.getTargets()
        txKey = pm.checkBoxGrp(self.xTranslate, query=True, value3=True)
        tyKey = pm.checkBoxGrp(self.yTranslate, query=True, value3=True)
        tzKey = pm.checkBoxGrp(self.zTranslate, query=True, value3=True)
        rxKey = pm.checkBoxGrp(self.xRotate, query=True, value3=True)
        ryKey = pm.checkBoxGrp(self.yRotate, query=True, value3=True)
        rzKey = pm.checkBoxGrp(self.zRotate, query=True, value3=True)
        sxKey = pm.checkBoxGrp(self.xScale, query=True, value3=True)
        syKey = pm.checkBoxGrp(self.yScale, query=True, value3=True)
        szKey = pm.checkBoxGrp(self.zScale, query=True, value3=True)
        vizKey = pm.checkBoxGrp(self.viz, query=True, value3=True)
        #customName = pm.textFieldGrp(self.customName, query=True, text=True)
        #customKey = pm.checkBoxGrp(self.customEdit, query=True, value1=True)
        
        # Translations
        if txHide:
            pass
        else:
            if txKey:
                for target in targets:
                    pm.setAttr(target.tx, keyable=False, channelBox=True)      
            else:
                for target in targets:
                    pm.setAttr(target.tx, keyable=True)          
        if tyHide:
            pass
        else:
            if tyKey:
                for target in targets:
                    pm.setAttr(target.ty, keyable=False, channelBox=True)      
            else:
                for target in targets:
                    pm.setAttr(target.ty, keyable=True) 
        if tzHide:
            pass
        else:
            if tzKey:
                for target in targets:
                    pm.setAttr(target.tz, keyable=False, channelBox=True)      
            else:
                for target in targets:
                    pm.setAttr(target.tz, keyable=True) 
        
        # Rotations        
        if rxHide:
            pass
        else:
            if rxKey:
                for target in targets:
                    pm.setAttr(target.rx, keyable=False, channelBox=True)      
            else:
                for target in targets:
                    pm.setAttr(target.rx, keyable=True)         
        if ryHide:
            pass
        else:
            if ryKey:
                for target in targets:
                    pm.setAttr(target.ry, keyable=False, channelBox=True)      
            else:
                for target in targets:
                    pm.setAttr(target.ry, keyable=True) 
        if rzHide:
            pass
        else:
            if rzKey:
                for target in targets:
                    pm.setAttr(target.rz, keyable=False, channelBox=True)      
            else:
                for target in targets:
                    pm.setAttr(target.rz, keyable=True) 
        
        # Scales
        if sxHide:
            pass
        else:
            if sxKey:
                for target in targets:
                    pm.setAttr(target.sx, keyable=False, channelBox=True)      
            else:
                for target in targets:
                    pm.setAttr(target.sx, keyable=True)         
        if syHide:
            pass
        else:
            if syKey:
                for target in targets:
                    pm.setAttr(target.sy, keyable=False, channelBox=True)      
            else:
                for target in targets:
                    pm.setAttr(target.sy, keyable=True) 
        if szHide:
            pass
        else:
            if szKey:
                for target in targets:
                    pm.setAttr(target.sz, keyable=False, channelBox=True)      
            else:
                for target in targets:
                    pm.setAttr(target.sz, keyable=True)   
        
        # Visability 
        if vizHide:
            pass
        else:       
            if vizKey:
                for target in targets:
                    pm.setAttr(target.v, keyable=False, channelBox=True)
            else:
                for target in targets:
                    pm.setAttr(target.v, keyable=True)
        
        '''
        if customKey:
            for target in targets:
                pm.setAttr(target.customName, keyable=False)
        else:
            for target in targets:
                pm.setAttr(target.customName, keyable=True)
        ''' 
        
        
    def editAttribute(self, *args):
        self.lockAttribute() 
        self.hideAttribute()
        self.keyAttribute()
        
               
               
        
aeWindow = AE_Window()