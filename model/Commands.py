import subprocess
import User

class Command:
    validCommands = [
            'id',
            'systeminfo',
            'users',
            'kill',
            'gift',
            'purpose'
            ]
    userDB = User()
    def __init__(self, userDB) -> None:

        pass

    def id_command(self):
        return subprocess.run(['id'], capture_output=True) # returns the binary format
    
    def systeminfo_command(self):
        return subprocess.run(['lscpu'], capture_output=True) # returns the binary format
    
    def users_command(self):
        return 

    def runCommand(self, command):
        '''
        sanitization of input
        run the command using subprocess
        '''
        if(command in self.validCommands):
            for userCommand in self.validCommands:
                if(userCommand == self.validCommands):
                    detectedCommand = self.validCommands
                    
            pass
        else:
            raise Exception('The damn command is not present! You moron')
    pass
