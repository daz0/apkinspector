import sys

if sys.path[0] == "":
	sys.path.append(sys.path[1]+"/androguard/")
	PATH_INSTALL = sys.path[1]+"/androguard"
else:
	sys.path.append(sys.path[0]+"/androguard/")
	PATH_INSTALL = sys.path[0]+"/androguard"

print sys.path

sys.path.append(PATH_INSTALL + "./androguard/")
sys.path.append(PATH_INSTALL + "/androguard/core")
sys.path.append(PATH_INSTALL + "/androguard/core/bytecodes")
sys.path.append(PATH_INSTALL + "/androguard/core/predicates")	### not present in new AG
sys.path.append(PATH_INSTALL + "/androguard/core/analysis")
sys.path.append(PATH_INSTALL + "/androguard/core/vm")
sys.path.append(PATH_INSTALL + "/androguard/core/wm")	### not present in new AG
sys.path.append(PATH_INSTALL + "/core/protection")	### not present in new AG
sys.path.append(PATH_INSTALL + "/classification")	### not present in new AG
 
### ZW - import androguard, analysis, androlyze
import androguard, androlyze, analysis
import bytecode

from dvm import *
## ZW - from analysis import VMAnalysis

print "print the sys.path again......"
print sys.path

print dir(DalvikVMFormat)
print dir(analysis)
print analysis.__package__
print analysis.__path__
print analysis.__file__
print analysis.__doc__
print analysis.__builtins__

class CLASS:
    apk = None
    vm = None
    vmx = None
    
    def __init__(self, apk, vm, vmx):
        self.apk = apk
        self.vm = vm
        self.vmx = vmx
    
    def get_class(self):
        return self.vm.get_classes()
        
    def get_classname(self, classes):
        return classes.get_name()
    
    def get_methods(self, classes):
        return classes.get_methods()
    
    def get_methodname(self, method):
        return method.get_name()
        
    def get_code(self, method):
        return method._code.show()
        
    def get_classlist(self):
        return self.vm.get_classes_names()
    
    def get_methods_class(self, classes):
        return self.vm.get_methods_class(classes)
    
    def get_maxdepth(self):
        classesnames = self.vm.get_classes_names()
        maxdepth = 0
        for i in classesnames:
            l = len(i.split("/"))
            if l > maxdepth:
                maxdepth = l
                
        return maxdepth


    #get where a permission is used
    def get_permission(self):
        pathDict = {}
        perms_access = self.vmx.tainted_packages.get_permissions([])
        for perm in perms_access:
            pathDict[perm] = self.show_path(perms_access[perm])
        
        return pathDict
  
    
    def show_path(self, paths):
        accessPathList = []
        for path in paths:
            if isinstance(path,analysis.analysis.PathP):
                if path.get_access_flag() == analysis.analysis.TAINTED_PACKAGE_CALL:
                    ## accessPath = ("%s %s %s (@%s-0x%x)  --->  %s %s %s") % (path.get_method().get_class_name(), path.get_method().get_name(), \
                    ##                                                 path.get_method().get_descriptor(), path.get_bb().get_name(), path.get_bb().start + path.get_idx(), \
                    ##                                                 path.get_class_name(), path.get_name(), path.get_descriptor())
                    a1, a2, a3 = path.get_src(self.vm.get_class_manager())
                    b1, b2, b3 = path.get_dst(self.vm.get_class_manager())
                    accessPath = ("%s %s %s --->  %s %s %s") % (a1, a2, a3, b1, b2, b3)
																			
                    accessPathList.append(accessPath)
            
        return accessPathList
        
        

    
    # All Invoke Methods
    def get_methodInvoke(self):
        methodInvokeList = []
        allMethods = self.vm.get_methods()
        import Global
        for m in allMethods:
#Yuan :build callinout tree
           
            invokingMethod = m.get_class_name() + " " + m.get_descriptor() +"," + m.get_name()
            if (Global.NAV_NO == 1):
                print "name first method"
                Global.FM = invokingMethod
                
            code =  m.get_code()
            if code == None:
                continue
            else:
                bc = code.get_bc()
                idx = 0
                lineNum = 1
                for i in bc.get_instructions():
                    ## line = i.show_buff(idx)
                    line = i.get_name() + " " + i.show_buff(idx)
                    print "ZW " + line
                    if line.find("invoke-") >= 0:
						invokedMethod = i.show_buff(idx)
						methodInvokeList.append(invokingMethod +" ---> " + invokedMethod + "^Line:"+str(lineNum)+"  Offset:"+"0x%x" % idx)
                    	
##                        index = line.index("[meth@")
##                        method = str(line[index:])
##                        method2 = method.split(" ")                        

##                        # set the class
##                        ClassStartIndex = index + len(method2[0]) + len(method2[1]) + 2
##                        className = line[ClassStartIndex : ClassStartIndex + len(method2[2])]
##                        
##                        # set the return type
##                        ReturnStartIndex = index + method.rindex(")") + 2
##                        returnType = line[ReturnStartIndex : ReturnStartIndex+len(method2[-2])]
##                        
##                        # set the method name 
##                        NameStartIndex = index + method.rindex(" ") + 1
##                        methodName = line[NameStartIndex : NameStartIndex + len(method2[-1]) - 1]
                        
##                        # set the parameter name
##                        ParameterStartIndex = index + method.index("(")
##                        ParameterEndIndex = index + method.rindex(")") + 1
##                        parameterName = line[ParameterStartIndex : ParameterEndIndex]
                        
##                        # set the descriptor name
##                        descriptorName = parameterName +returnType
                        
##                        invokedMethod = className + " " +descriptorName+ "," + methodName
##                        methodInvokeList.append(invokingMethod +" ---> " + invokedMethod + "^Line:"+str(lineNum)+"  Offset:"+"0x%x" % idx)
                        
                    lineNum += 1
                    idx += i.get_length() 
#        print "methodinvoke list\n" 
#        print  methodInvokeList
        file = open('method.txt','a')
#             file.write("%s\n" % method)
        file.write("%s\n" % methodInvokeList )
        file.close
        Global.endmethod = invokedMethod
        return methodInvokeList

