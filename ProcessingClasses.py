#------------------------------------------#
# Title: Processing Classes
# Desc: A Module for processing Classes
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# DBiesinger, 2030-Jan-02, Extended functionality to add tracks
# AAllen, 2020-Sept-05, Added select_cd method
# AAllen, 2020-Sept-07, Added code for add_track
# AAllen, 2020-Sept-07, Added remove_track method
# AAllen, 2020-Sept-08, Added find_cd_id and find_track_id
#------------------------------------------#

if __name__ == '__main__':
    raise Exception('This file is not meant to ran by itself')

import DataClasses as DC

class DataProcessor:
    """Processing the data in the application"""
    @staticmethod
    def add_CD(CDInfo, table):
        """function to add CD info in CDinfo to the inventory table.


        Args:
            CDInfo (tuple): Holds information (ID, CD Title, CD Artist) to be added to inventory.
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """

        cdId, title, artist = CDInfo
        try:
            cdId = int(cdId)
            for row in table:
                if row.cd_id == cdId:
                    print('!A CD with ID:', cdId ,' already exists. Unable to add CD.\n')
                    return
            row = DC.CD(cdId, title, artist)
            table.append(row)
        except Exception as e:
            print('There was a general error!', e, e.__doc__, type(e), sep='\n') 
        

    @staticmethod
    def select_cd(table: list, cd_idx: int) -> DC.CD:
        """selects a CD object out of table that has the ID cd_idx

        Args:
            table (list): Inventory list of CD objects.
            cd_idx (int): id of CD object to return

        Raises:
            Exception: If id is not in list.

        Returns:
            row (DC.CD): CD object that matches cd_idx

        """
        
        try:
            for row in table:
                if row.cd_id == cd_idx:
                    return row
        except TypeError:
            print('CD ID must be an integer.\n')
        except Exception as e:
            print('There was a general error!', e, e.__doc__, type(e), sep='\n') 



    @staticmethod
    def add_track(track_info: tuple, cd: DC.CD) -> None:
        """adds a Track object with attributes in track_info to cd


        Args:
            track_info (tuple): Tuple containing track info (position, title, Length).
            cd (DC.CD): cd object the track gets added to.

        Raises:
            Exception: Exception raised in case position is not an integer.

        Returns:
            None: track is added to cd object passed in

        """

        try:
            new_track = DC.Track(track_info[0], track_info[1], track_info[2])
            cd.add_track(new_track)
        except:
            raise Exception ("Unable to add track to CD.")
            
    @staticmethod
    def remove_track(track_position: int, cd: DC.CD) -> None:
        """removes a Track object with the given track position


        Args:
            track_position (int): integer of the track position to remove
            cd (DC.CD): cd object the track gets added to.

        Raises:
            Exception: Exception raised in case position is not an integer.

        Returns:
            None: track is removed from cd object passed in

        """
        try:
            cd.rmv_track(track_position)
        except:
            raise Exception ("Unable to  add track to CD.")
            
    @staticmethod
    def find_cd_id(table: list, cd_idx: int) -> True:
        """verifies an ID exists in CD inventory

        Args:
            table (list): Inventory list of CD objects.
            cd_idx (int): id of CD object to return

        Raises:
            Exception: If id is not in list.

        Returns:
            True if ID is in the CD inventory list

        """
        # check each cd in the list to see if there is a matching ID
        try:
            for row in table:
                if row.cd_id == cd_idx:
                    return True
            return False
        except TypeError:
            print('CD ID must be an integer.\n')
        except Exception as e:
            print('There was a general error!', e, e.__doc__, type(e), sep='\n') 
    
    
    @staticmethod
    def find_track_id(cd: DC.CD, track_idx: int) -> True:
        """verifies an ID exists as a Track position in Track list

        Args:
            cd: CD object
            cd_idx (int): id of CD object to return

        Raises:
            Exception: If id is not in list.

        Returns:
            True if ID imatches a Track position

        """
        # check each Track in the Track list for a matching ID, but skip the
        # None filler Tracks
        try:
            for row in cd.cd_tracks:
                if (row != None) and (row.position == track_idx):
                    return True
            return False
        except TypeError:
            print('Track Position ID must be an integer.\n')
        except Exception as e:
            print('There was a general error!', e, e.__doc__, type(e), sep='\n') 


