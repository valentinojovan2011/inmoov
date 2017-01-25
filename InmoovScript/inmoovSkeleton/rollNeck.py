# ##############################################################################
#						*** MOD ROLLNECK ***
# ##############################################################################


 
  
# ##############################################################################
# 							PERSONNAL PARAMETERS
# ##############################################################################  
isRollNeckActivated=0  
#read current skeleton part config
ThisSkeletonPart=inspect.getfile(inspect.currentframe()).replace('.py','')

try:
	CheckFileExist(ThisSkeletonPart)
	ThisSkeletonPartConfig = ConfigParser.ConfigParser()
	ThisSkeletonPartConfig.read(ThisSkeletonPart+'.config')

	isRollNeckActivated=ThisSkeletonPartConfig.getboolean('MAIN', 'isRollNeckActivated') 
	autoDetach=ThisSkeletonPartConfig.getboolean('MAIN', 'autoDetach')
	autoAttach=ThisSkeletonPartConfig.getboolean('MAIN', 'autoAttach')
	RollNeckArduino=ThisSkeletonPartConfig.get('ARDUINO', 'RollNeckArduino')
	RollNeckPin=ThisSkeletonPartConfig.getint('ARDUINO', 'RollNeckPin')
	
except:
	errorSpokenFunc('ConfigParserProblem','rollneck.config')
	pass
    
  
  
  


# ##############################################################################
# 								SERVO FUNCTIONS
# ##############################################################################

if isRollNeckActivated==1 and (ScriptType!="NoArduino"):

# ##############################################################################
# 								ARDUINO CHECK
# ##############################################################################
	masterArduinoRollNeckIsconnected=0
	try:
		
		
		if RollNeckArduino=="left":
			masterArduinoRollNeckIsconnected=LeftPortIsConnected
		if RollNeckArduino=="right":
			masterArduinoRollNeckIsconnected=RightPortIsConnected
		RollNeckArduino=eval(RollNeckArduino)
		
	except:
		errorSpokenFunc('BAdrduinoChoosen',', Roll Neck')
		isRollNeckActivated=0
		pass	
	
	if masterArduinoRollNeckIsconnected:
		talkEvent(lang_startingRollNeck)
		rollneck = Runtime.create("rollneck","Servo")
				
		rollneck.map(ThisSkeletonPartConfig.getint('MINIMUM_MAP', 'rollneck'),ThisSkeletonPartConfig.getint('MAXIMUM_MAP', 'rollneck'),ThisSkeletonPartConfig.getint('SERVO_MINIMUM', 'rollneck'),ThisSkeletonPartConfig.getint('SERVO_MAXIMUM', 'rollneck')) 
		rollneck.setVelocity(ThisSkeletonPartConfig.getint('DEF_SPEED', 'rollneck'))
		rollneck.setRest(ThisSkeletonPartConfig.getint('SERVO_MAP_REST', 'rollneck'))
		
	
		if ThisSkeletonPartConfig.getboolean('SERVO_INVERTED', 'rollneck'):
			rollneck.setInverted(True)
			
		rollneck = Runtime.start("rollneck","Servo")
		rollneck.attach(RollNeckArduino, RollNeckPin, ThisSkeletonPartConfig.getint('SERVO_MAP_REST', 'rollneck'), ThisSkeletonPartConfig.getint('DEF_SPEED', 'rollneck'))
		
		if autoDetach:
			rollneck.enableAutoAttach(1)
		
		if autoDetach:
			rollneck.autoDetach()		
		rollneck.rest()
		sleep(2)
		rollneck.detach()
		
		
	else:
		#we force parameter if arduino is off
		isRollNeckActivated=0
		
#todo set inverted
