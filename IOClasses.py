#------------------------------------------#
# Title: IO Classes
# Desc: A Module for IO Classes
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# DBiesinger, 2030-Jan-02, Extended functionality to add tracks
# AAllen, 2020-Sept-05, added code for show_tracks()
# AAllen, 2020-Sept-07, updated save_inventory() and load_inventory() to save
#                       and load track
# AAllen, 2020-Sept-07, added get_CD_ID_choice()
# AAllen, 2020-Sept-07, added get_Track_ID_choice()
# AAllen, 2020-Sept-08, updated get_CD_ID_choice() to call find_CD_ID in
#                       ProcessingClasses
# AAllen, 2020-Sept-08, updated get_Track_ID_choice() to call find_Track_ID in
#                       ProcessingClasses
# AAllen, 2020-Sept-08, added get_user_input method to get type validated input
# AAllen, 2020-Sept-08, updated get_cd_info to use get_user_input and validate
#                       ID is an int
# AAllen, 2020-Sept-08, updated get_track_info to use get_user_input and validate
#                       ID/Position is an int
#------------------------------------------#

if __name__ == '__main__':
    raise Exception('This file is not meant to run by itself')

import DataClasses as DC
import ProcessingClasses as PC

class FileIO:
    """Processes data to and from file:

    properties:

    methods:
        save_inventory(file_name, lst_Inventory): -> None
        load_inventory(file_name): -> (a list of CD objects)

    """
    @staticmethod
    def save_inventory(file_name: list, lst_Inventory: list) -> None:
        """


        Args:
            file_name (list): list of file names [CD Inventory, Track Inventory]
                            that hold the data.
            lst_Inventory (list): list of CD objects.

        Returns:
            None.

        """
        # confirm that we have file name for CDs and Tracks
        try:
            file_name_CD = file_name[0]
            file_name_Tracks = file_name[1]
        except Exception as e:
            print('There was a general error!', e, e.__doc__, type(e), sep='\n')
        
        try:
            # write a record to CD Inventory file for each CD
            with open(file_name_CD, 'w') as file:
                for disc in lst_Inventory:
                    file.write(disc.get_record())
            # write a record to Track Inventory file for each Track, add CD ID
            with open(file_name_Tracks, 'w') as file:
                for disc in lst_Inventory:
                    lst_Tracks = disc.cd_tracks
                    for row in lst_Tracks:
                        if row != None:
                            file.write('{},{}'.format(disc.cd_id, row.get_record()))                      
        except Exception as e:
            print('There was a general error!', e, e.__doc__, type(e), sep='\n')

    @staticmethod
    def load_inventory(file_name: list) -> list:
        """


        Args:
            file_name (list): list of file names [CD Inventory, Track Inventory] that hold the data.

        Returns:
            list: list of CD objects.

        """

        lst_Inventory = []
        # verify that file name was received for both files - CDs and Tracks
        try:
            file_name_CD = file_name[0]
            file_name_Tracks = file_name[1]
        except Exception as e:
            print('There was a general error!', e, e.__doc__, type(e), sep='\n')
            
        # Load CD data from CDs file
        try:
            with open(file_name_CD, 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    row = DC.CD(int(data[0]), data[1], data[2])
                    lst_Inventory.append(row)
        except Exception as e:
            print('There was a general error!', e, e.__doc__, type(e), sep='\n')   
        
        # Load Track data from Tracks file
        try:
            with open(file_name_Tracks, 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    for row in lst_Inventory:
                        if row.cd_id == int(data[0]):
                            track_cd = row
                    new_track = DC.Track(int(data[1]), data[2], data[3]) 
                    track_cd.add_track(new_track)
        except Exception as e:
            print('There was a general error!', e, e.__doc__, type(e), sep='\n')
        return lst_Inventory

class ScreenIO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Main Menu\n\n[l] load Inventory from file\n[a] Add CD / Album\n[d] Display Current Inventory')
        print('[c] Choose CD / Album\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, d, c, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'd', 'c', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, d, c, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def print_CD_menu():
        """Displays a sub menu of choices for CD / Album to the user

        Args:
            None.

        Returns:
            None.
        """

        print('CD Sub Menu\n\n[a] Add track\n[d] Display cd / Album details\n[r] Remove track\n[x] exit to Main Menu')

    @staticmethod
    def menu_CD_choice():
        """Gets user input for CD sub menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices a, d, r or x

        """
        choice = ' '
        while choice not in ['a', 'd', 'r', 'x']:
            choice = input('Which operation would you like to perform? [a, d, r or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def get_CD_ID_choice(table):
        """Gets user input for CD choice

        Args:
            table (list): 2D data structure (list of CD objects)
                        that holds the data during runtime.

        Returns:
            choice (int): integer of the CD ID that user has chosen, returns
                            None if users exits out

        """
        
        choice = None
        while choice != 'x':
            choice = input('Select the CD / Album index: ')
            # if the user choices x, return None for choice to let user exit
            if choice == 'x':
                choice = None
                return choice
            # check if user choice is a valid int and the cd exists in the
            # inventory list
            try:
                choice = int(choice)
                found = PC.DataProcessor.find_cd_id(table, choice)
                if found == True:
                    return choice
                else:
                    print('Please choose an existing ID from the inventory. ',
                          'Enter \'x\' to exit to menu.\n')
            except:
                print('\n!CD ID must be a valid integer. Enter \'x\' to cancel.\n')
                
    @staticmethod
    def get_Track_ID_choice(cd):
        """Gets user input for Track choice

        Args:
            cd (DC.CD object): cd object from which to get track ID

        Returns:
            choice (int): integer of the CD ID that user has chosen

        """
        
        choice = None
        while choice != 'x':
            choice = input('Select the Track position/index: ')
            # if choice is x, return None for choice so user can exit
            if choice == 'x':
                choice = None
                return choice
            # check if user choice is a valid int and the track position exists
            # in the cd track list
            try:
                choice = int(choice)
                found = PC.DataProcessor.find_track_id(cd, choice)
                if found == True:        
                    return choice
                else:
                    print('Please choose an existing ID from the inventory. ',
                          'Enter \'x\' to exit to menu.\n')
            except:
                print('\n!Track Position ID must be a valid integer. ',
                      'Enter \'x\' to cancel.\n')
        
    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list): 2D data structure (list of CD objects)
                        that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        try:
            for row in table:
                print(row)
        except:
            print('-- No CDs to show --')
        print('======================================')

    @staticmethod
    def show_tracks(cd):
        """Displays the Tracks on a CD / Album

        Args:
            cd (CD): CD object.

        Returns:
            None.

        """
        print('====== Current CD / Album: ======')
        try:
            print(cd)
        except:
            print('-- No CD to show --')
        print('=================================')
        try:
            print(cd.get_tracks())
        except:
            print('-- No Tracks --')
        print('=================================')

    @staticmethod
    def get_CD_info():
        """function to request CD information from User to add CD to inventory


        Returns:
            cdId (int): Holds the ID of the CD dataset.
            cdTitle (string): Holds the title of the CD.
            cdArtist (string): Holds the artist of the CD.

        """
        # confirm that ID entered is positive integer
        while True:
            cdId = ScreenIO.get_typed_input(int,'Enter ID: ','ID must be a valid integer.')
            if cdId > 0:
                break
            else:
                print('CD ID must be positive integer.\n')
        cdTitle = input('What is the CD\'s title? ').strip()
        cdArtist = input('What is the Artist\'s name? ').strip()
        return cdId, cdTitle, cdArtist

    @staticmethod
    def get_track_info():
        """function to request Track information from User to add Track to CD / Album


        Returns:
            trkId (int): Holds the ID of the Track dataset.
            trkTitle (string): Holds the title of the Track.
            trkLength (string): Holds the length (time) of the Track.

        """
        # confirm that ID entered is positive integer
        while True:
            trkId = ScreenIO.get_typed_input(int,'Enter Position on CD / Album: ',
                                        'Track Position must be a valid integer.')
            if trkId > 0:
                break
            else:
                print('CD ID must be a positive integer.\n')
        trkTitle = input('What is the Track\'s title? ').strip()
        trkLength = input('What is the Track\'s length? ').strip()
        return trkId, trkTitle, trkLength
    
    
    @staticmethod
    def get_typed_input(_type, prompt, error):
        """function to request user input, verify input and ask again if
            incorrect
            Author: Douglas Klos
            
        Args:
            _type(string): type of input expected
            prompt(string): text to show when requesting input
            error(string): text to show when input is not correct type

        Returns:
            value (_type): user input converted to _type requested

        """
        while True:
            try:
                value = _type(input(prompt))
                break
            except ValueError:
                print (error)
    
        return value
    
        
