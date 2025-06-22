#1 features pending

import os
import datetime
class HospitalManagement:
    def __init__(self):
        self.curUid = ''
        self.curName = ''
        self.curEmail = ''
        self.curPass = ''
        self.curContact = ''
        self.curAbout = ''
        
        self.patientUid = ''
        self.patientName = ''
        self.patientEmail = ''
        self.patientContact = ''
        
    def nospace(self, text):#working
        return '_'.join(text.split())
    def withspace(self, text):#working
        return ' '.join(text.split('_'))
    def getNewPrescriptionId(self):#working
        pList = sorted(os.listdir('Data\\Prescriptions\\'))
        filePath = 'Data\\Prescriptions\\' + pList[-1]
        with open(filePath, 'r') as file:
            read = file.readline()
        return str(int(read.split()[-1]) + 1)
    def getNewId(self, fileName):#working
        with open('Data\\'+fileName+'.txt', 'r') as file:
            read = file.readlines()
        return str(int(read[-1].split()[0]) + 1)
    def getUserById(self, Uid, userType):#working
        filePath = 'Data\\'+userType + 's.txt'
        with open(filePath, 'r') as file:
            read = file.readlines()
        for u in read:
            words = u.split()
            if words[0] == Uid:
                return words
    def showUserProfile(self):#working
        print('\n_____ My Profile _____')
        print('Name:', self.curName,'\nEmail:', self.curEmail, '\nContact:', self.curContact, '\nAbout:', self.curAbout)
    def createMedicines(self):#working
        while True:
            mName = input('Enter the name of Medicine (enter "BACK" to go back): ')
            if mName.lower()=='back':
                return
            elif mName=='':
                print('! Medicine name can not be blank!')
            else:
                while True:
                    mrp = input('Enter the MRP of Medicine: ')
                    try:
                        mrp = float(mrp)
                    except ValueError:
                        print('! Invalid MRP entered. Please enter again!')
                    else:
                        break
                with open('Data\\Medicines.txt','a') as file:
                    file.write(self.getNewId('Medicines')+' ' + self.nospace(mName.upper()) + ' ' + str(mrp) + ' \n')
                print('Medicine Added.')
    def searchDoctor(self):#working
        print('_____ Search Doctor _____')
        isAny = False
        while True:
            search = input('Enter about doctor to search (enter "BACK" to go back): ')
            if search=='':
                print('! No input provided. Try again!')
            elif search.lower()=='back':
                return
            else:
                search = search.lower().split()
                with open('Data\\Doctors.txt', 'r') as file:
                    read = file.readlines()
                for line in read:
                    searchText = line.lower()
                    searchCount = 0
                    for word in search:
                        if word in searchText:
                            searchCount += 1
                    if searchCount>= len(search):
                        isAny = True
                        words = line.split()
                        print('UID:', words[0],' First Name:', words[1], ' Last Name:', words[2], ' Email:', words[3], ' Contact:', words[5])
                if not isAny:
                    print('! No Results found. Search again!')
    
    def foundPatientInMyList(self, Uid):#working
        with open('Data\\Patient of Doctor.txt', 'r') as file:
            read = file.readlines()
        for line in read:
            words = line.split()
            if words[3]==self.curUid and words[6]==Uid:
                return True
        return False
            
    def createPrescription(self):#working
        pNo = self.getNewPrescriptionId()
        string = 'Prescription No: ' + pNo + ' \nDate and Time: ' + str(datetime.datetime.now()) + " \n\nDoctor's Details:- \nUID: "
        string += self.curUid + ' \nName: ' + self.curName + ' \nEmail: ' + self.curEmail + ' \nPh. No.: ' + self.curContact + " \n\nPatient's Details:- \nUID: "
        while True:
            email = input('Enter an email of Patient (enter "BACK" to go back): ')
            if email=='':
                print('! Email can not be empty. Enter again!')
            elif email.lower() == 'back':
                return
            elif self.foundUser(email, 'Patient') and self.foundPatientInMyList(self.patientUid):
                string += self.patientUid + ' \nName: ' + self.patientName + ' \nEmail: ' + self.patientEmail + ' \nPh. No.: ' + self.patientContact + ' \n\nDescription:- \n'
                break
            else:
                print('! Email not found. Enter again!')
        while True:
            description = input('Enter description of Prescription: ')
            if description=='':
                print('! Description can not be blank!')
            else:
                string += description + ' \n\nMedicines:- \n'
                break
        with open('Data\\Medicines.txt', 'r') as file:
            medicines = [x.split()[1] for x in file.readlines()]
        medNo = 1
        total = 0.0
        buyMeds = []
        while True:
            search = input('Search Product (enter "BACK" to stop adding new product): ').upper()
            results = []
            if search=='BACK':
                if len(buyMeds)>0:
                    for i in buyMeds:
                        string += i
                else:
                    string+= 'No medicines required.\n'
                string += '\nTotal Amount: ' + str(total) + ' \n'
                self.generatePrescription(pNo, string)
                break
            search = search.split()
            #generating Results of searched words
            rcount = 0
            for i in medicines:
                c = len(search)
                count = 0
                for j in search:
                    if j in i:
                        count+= 1
                if count>=c:
                    results.append(i)
            
            if len(results) ==0:
                print('! No Medicine found. Search again!')
            elif len(results) == 1:
                details = self.getMedicineDetails(results[0])
                print('Medicine Selected:', self.withspace(results[0]))
                while True:
                    inpquant = input('Enter the quantity of Medicine: ')
                    if inpquant.isnumeric():
                        if int(inpquant)>0:
                            medString = str(medNo) + '. ' + self.withspace(details[1]) + ' (Rate: ' + details[2] + ') Quantity: ' + inpquant
                            price = float(details[2]) * int(inpquant)
                            medString += ' Subtotal: ' + str(price) + ' \n'
                            total += price
                            buyMeds.append(medString)
                            medNo += 1
                            print('Medicine Added.')
                            break
                        else:
                            print('! Quantity should be greater than 0!')
                    else:
                        print('! Invalid Quantity. Enter again!')
            else:
                print('Results:')
                print('Enter Unique Medicine from below list.')
                for i in results:
                    print(self.withspace(i))
    def generatePrescription(self, pNo, content):#working
        filePath = 'Data\\Prescriptions\\' + str(pNo) + '.txt'
        with open(filePath, 'w') as file:
            file.write(content)
            print('Prescription Generated.')
    def showAllPrescriptions(self):#working
        folderPath = 'Data\\Prescriptions\\'
        print('_____ List of All Prescriptions _____')
        for fileName in sorted(os.listdir(folderPath)):
            if '.txt' in fileName:
                with open(folderPath + fileName, 'r') as file:
                    read = file.readlines()
                string = read[0].strip() + ' ' + read[1].strip() + ' Doctor ' + read[4].strip() + ' ' + read[5].strip() + ' Patient ' + read[10].strip() + ' ' + read[11].strip()
                print(string)
    def listUserPrescriptions(self):
        isAny = False
        folderPath = 'Data\\Prescriptions\\'
        print('_____ List of my Prescriptions _____')
        for fileName in sorted(os.listdir(folderPath)):
            if '.txt' in fileName:
                with open(folderPath + fileName, 'r') as file:
                    read = file.readlines()
                if read[10].split()[-1]==self.curUid:
                    string = read[0].strip() + ' ' + read[1].strip() + ' Doctor ' + read[4].strip() + ' ' + read[5].strip() + ' Patient ' + read[10].strip() + ' ' + read[11].strip()
                    print(string)
                    isAny = True
        if not isAny:
            print('! No Prescription is created for you!')
    def showLatestPrescription(self):#working
        folderPath = 'Data\\Prescriptions\\'
        print('_____ Latest Prescription _____')
        for fileName in sorted(os.listdir(folderPath), reverse=True):
            if '.txt' in fileName:
                with open(folderPath + fileName, 'r') as file:
                    read = file.readlines()
                if read[10].split()[-1]==self.curUid:
                    with open(folderPath + fileName, 'r') as file:
                        print(file.read())
                    return
        print('! No Prescription is created for you!')
    def getMedicineDetails(self, name): #working
        with open('Data\\Medicines.txt', 'r') as file:
            read = file.readlines()
        for line in read:
            words = line.split()
            if words[1] == name:
                return words
    def addPatientToList(self):#working
        while True:
            email = input('Enter an email of Patient (enter "BACK" to go back): ')
            if email=='':
                print('! Email can not be empty. Enter again!')
            elif email.lower() == 'back':
                return
            elif self.foundUser(email, 'Patient'):
                break
            else:
                print('! Email not found. Enter again!')
        string = self.getNewId('Patient of Doctor') + ' ' + self.curName + ' ' + self.curUid + ' ' + self.patientName + ' ' + self.patientUid + ' \n'
        with open('Data\\Patient of Doctor.txt', 'a') as file:
            file.write(string)
    
    def showMyPatients(self):#working
        with open('Data\\Patient of Doctor.txt', 'r') as file:
            read = file.readlines()
        print('_____ List of my Patients _____')
        foundAny = False
        for patient in read:
            words = patient.split()
            if words[3]==self.curUid:
                foundAny = True
                patientDetails = self.getUserById(words[6], 'Patient')
                print('UID:', patientDetails[0], ' Name:', patientDetails[1], patientDetails[2], ' Email:', patientDetails[3], ' Contact:', patientDetails[5])
        if not foundAny:
            print('! No Patient found in your list. Add patient to your list first!')
    def removeUser(self, userType):#working
        filePath = 'Data\\' + userType + 's.txt'
        while True:
            email = input('Enter an email of '+ userType +' to be removed (enter "BACK" to go back): ')
            if email=='':
                print('! Email can not be empty. Enter again!')
            elif email.lower() == 'back':
                return
            elif self.foundUser(email, userType):
                break
            else:
                print('! Email not found. Enter again!')

        with open(filePath, 'r') as file:
            read = file.readlines()
        newRead = []
        for user in read:
            words = user.split()
            if words[3]!=email:
                newRead.append(user)
            else:
                print(userType, 'Removed:', words[1], words[2])
        with open(filePath, 'w') as file:
            file.writelines(newRead)
    
    def createUser(self, userType):#working
        filePath = 'Data\\'+ userType + 's.txt'
        
        while True:
            firstName = input('Enter First Name (enter "BACK" to go back): ')
            if firstName=='':
                print('! First Name can not be blank!')
            elif firstName.lower() == 'back':
                return
            else:
                break
        while True:
            lastName = input('Enter Last Name: ')
            if lastName=='':
                print('! Last Name can not be blank. Try again!')
            else:
                break
        while True:
            userEmail = input("Enter " + userType + "'s Email: ")
            if userEmail=='':
                print('! Email can not be blank. Try again!')
            else:
                break
        while True:
            userContact = input("Enter " + userType + "'s Contact Number: ")
            if len(userContact)==10 and userContact.isnumeric():
                break
            else:
                print('! Invalid contact. Enter again!')
        while True:
            userPass = input("Enter " + userType + "'s Password: ")
            if userPass=='':
                print('! Password can not be blank. Try again!')
            else:
                break
        while True:
            userAbout = input("Enter " + userType + "'s About details: ")
            if userAbout=='':
                print('! About can not be blank. Try again!')
            else:
                break
        userString = ' '.join([self.getNewId((userType + 's')), firstName, lastName, userEmail, userPass, userContact, self.nospace(userAbout),'\n'])
        with open(filePath, 'a') as file:
            file.write(userString)
        print('New', userType,'Added.')
        
    def patientSession(self):#working
        while True:
            print('\n______ UID:', self.curUid,' Name:', self.curName, '_____')
            print('1. View my latest Prescription\n2. List all of my Prescriptions\n3. Search Doctor\n4. Show my Profile\n5. Exit')
            optin = input('Enter Option: ')
            if optin.isnumeric():
                if optin=='1':
                    self.showLatestPrescription()#working
                elif optin=='2':
                    self.listUserPrescriptions()#working
                elif optin=='3':
                    self.searchDoctor()#working
                elif optin=='4':
                    self.showUserProfile()#working
                elif optin=='5':
                    print('Exitting...')
                    break
                else:
                    print('! Invalid input. Please enter option between 1 & 5!')
            else:
                print('! Invalid input. Please enter only numbers!')
    def doctorSession(self):#working
        while True:
            print('\n______ UID:', self.curUid,' Name:', self.curName, '_____')
            print('1. Create Prescription\n2. Create an account for new Patient\n3. Add Patient to my list\n4. Show my Patient List\n5. Show my Profile\n6. Exit')
            optin = input('Enter Option: ')
            if optin.isnumeric():
                if optin=='1':
                    self.createPrescription()#working
                elif optin=='2':
                    self.createUser('Patient')#working
                elif optin=='3':
                    self.addPatientToList()#working
                elif optin=='4':
                    self.showMyPatients()#working
                elif optin=='5':
                    self.showUserProfile()#working
                elif optin=='6':
                    print('Exitting...')
                    break
                else:
                    print('! Invalid input. Please enter option between 1 & 6!')
            else:
                print('! Invalid input. Please enter only numbers!')
    def adminSession(self):#working
        while True:
            print('\n______ UID:', self.curUid,' Name:', self.curName, '_____')
            print('1. Add new Doctor to Hospital\n2. Remove Doctor from Hospital\n3. Show all Prescriptions of Hospital\n4. Show all Patients\n5. Add new Medicine\n6. Show my Profile\n7. Exit')
            optin = input('Enter Option: ')
            if optin.isnumeric():
                if optin=='1':
                    self.createUser('Doctor')#working
                elif optin=='2':
                    self.removeUser('Doctor')#working
                elif optin=='3':
                    self.showAllPrescriptions()#working
                elif optin=='4':
                    self.showAllUsers('Patient')#working
                elif optin=='5':
                    self.createMedicines()#working
                elif optin=='6':
                    self.showUserProfile()#working
                elif optin=='7':
                    print('Exitting...')
                    break
                else:
                    print('! Invalid input. Please enter option between 1 & 7!')
            else:
                print('! Invalid input. Please enter only numbers!')
    
    def verifyUser(self, email, password, userType): #working
        filePath = 'Data\\' + userType + 's.txt'
        with open(filePath,'r') as file:
            line = file.readline()
            while line!='':
                words = line.split()
                if words[3]==email and words[4]==password:
                    self.curUid, self.curName, self.curEmail, self.curContact, self.curAbout = words[0],(words[1]+' '+words[2]), words[3], words[5], self.withspace(words[6])
                    return True
                line = file.readline()
            return False
    def userLogin(self, userType): #working
        print('\n_____ Login as',userType,'_____')
        while True:
            inp = input('Enter your email (enter "BACK" to go back): ')
            if inp.upper()=='BACK':
                break
            elif inp!='':
                if self.foundUser(inp, userType):
                    while True:
                        passInput = input('Enter your Password (enter "BACK" to go back): ')
                        if passInput.upper()=='BACK':
                            break
                        elif self.verifyUser(inp, passInput, userType):
                            print('Login Successfull.')
                            if userType=='Patient':
                                self.patientSession()
                            elif userType=='Doctor':
                                self.doctorSession()
                            elif userType=='Administrator':
                                self.adminSession()
                            return
                        else:
                            print('! Incorrect Password. Enter Again!')
                else:
                    print('! Email not found. Enter again!')
            else:
                print('! Input can not be blank. Try again!')
    def foundUser(self, email, userType): #working
        filePath = 'Data\\' + userType + 's.txt'
        with open(filePath,'r') as file:
            line = file.readline()
            while line:
                words = line.split()
                if words[3]==email:
                    self.patientEmail = email
                    self.patientUid = words[0]
                    self.patientName = words[1] + ' ' + words[2]
                    self.patientContact = words[5]
                    return True
                line = file.readline()
            return False
    def showAllUsers(self, userType):#working
        print('\n_____ ' + userType + 's List: _____')
        filePath = 'Data\\' + userType + 's.txt'
        with open(filePath, 'r') as file:
            ls = file.readlines()
        for person in ls:
            words = person.split()
            print('UID:', words[0],' First Name:', words[1], ' Last Name:', words[2], ' Email:', words[3], ' Contact:', words[5])

    def showAllMedicines(self):#working
        with open('Data\\Medicines.txt', 'r') as file:
            read = file.readlines()
        print('\n_____ List of all Medicines _____')
        for i in read:
            words = i.split()
            print('Medicine ID:', words[0], ' Name:', self.withspace(words[1]), ' MRP:', words[2])
    def start(self):#working
        while True:
            print('\n_____ Main Menu ____\n1. Login as Patient\n2. Create new Patient account\n3. Login as Doctor\n4. Show all Doctors\n5. Show all Medicines\n6. Login as Administrator\n7. Exit')
            optin = input('Enter Option: ')
            if optin.isnumeric():
                if optin=='1':
                    self.userLogin('Patient')
                elif optin=='2':
                    self.createUser('Patient')
                elif optin=='3':
                    self.userLogin('Doctor')
                elif optin=='4':
                    self.showAllUsers('Doctor')
                elif optin=='5':
                    self.showAllMedicines()
                elif optin=='6':
                    self.userLogin('Administrator')
                elif optin=='7':
                    print('Exitting...')
                    break
                else:
                    print('! Invalid input. Please enter option between 1 & 7!')
            else:
                print('! Invalid input. Please enter only numbers!')

                
                
Hospital = HospitalManagement()
Hospital.start()