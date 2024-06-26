# -*- coding: utf-8 -*-
# @Author: Jean Besnier
# @Date:   2024-06-20 13:48:52
# @Last Modified by:   Jean Besnier
# @Last Modified time: 2024-06-22 14:50:30

import pandas as pd
import sys
import argparse

def clean_csv_file():
    '''
    Function to clean all missing values of a csv file
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_path", required= True, help=" Path to csv file")
    parser.add_argument("-s", "--separator", help="Separator of the csv file")
    args = parser.parse_args()
    try:
        data = pd.read_csv(args.file_path, sep=',' if (args.separator == None) else args.separator)
    except BaseException as e:
        print(f"The file couldn't be parsed\n{e}")
        exit(1)
    null_dict = dict()
    for column in data.columns:
        null_dict[column] = data[column].isnull().sum()
    if sum(null_dict.values()) == 0:
        print("The dataset doesn't contain any missing values ")
        exit(0)
    print(f"The dataset contains {sum(null_dict.values())} null values")
    res = ' '
    while res != 'n' and res != '' and res != 'Y':
        res = input("Would you like to handle the missing values? [Y/n] : ")
    if res == "n":
        exit(0)
    else:
        print("Here are the categories where there are missing values")
        for key, values in null_dict.items():
            if values != 0:
                print(f"{key} : {values}")
        res = ' '
        while (res != 'N' and res != '' and res != 'y' ):
          res = input("Do you want to remove rows containing those missing values? [y/N] : ")
        if res == "N" or res == '':
            exit(0)
        else:
            res = ' '
            while (res != 'N' and res != '' and res != 'y'):
                res = input("Do you want to remove all these rows? [y/N] : ")
            if res == 'y':
                data.dropna(axis = 'columns', inplace=True)
            else:
                status = 0
                while status == 0:
                    print("Type skip or choose a category to remove among :")
                    for key, values in null_dict.items():
                        if values != 0:
                            print(f"{key}")
                    res = input(">")
                    if res == "skip":
                        status = 1
                        break
                    if res in null_dict.keys() and null_dict[res] != 0:
                        data.dropna(subset = [res], inplace= True)
                        null_dict[res] = 0
                    else:
                        print("Wrong category name")
                        continue
                    if sum(null_dict.values()) == 0:
                        status = 1
                        print("There are no more missing values in the dataset")
                        break
                    choice = input("Do you want to continue? [Y/n] : ")
                    if choice == 'n':
                        status = 1
            res = ' '
            while (res != 'N' and res != '' and res != 'y'):
                res = input("Do you want to replace the existing file? [y/N] : ")
            if (res == 'y'):
                try:
                    data.to_csv(args.file_path, sep=',' if (args.separator == None) else args.separator)
                except Exception as e:
                    print(e)
                    exit(1)
            else:
                status = 0
                while (status == 0):
                    res = input("Enter the new file name: ")
                    if not res.endswith('.csv'):
                        res += ".csv"
                    try:
                        data.to_csv(res, mode='x')
                        status = 1
                    except FileExistsError:
                        print("This file already exists")
								
		# TODO: - proposer une suppression categorie par catégorie ✓
				#       - remplacer la suppression des valeurs manquantes par un remplissage (par la moyenne ou le voisin le plus proche)
				#       - rajouter la suppression des doublons      
				#       - vérifier les types de données, mettre en lumière les valeurs potentiellement problématiques
				#       - identifier les outliers et proposer de les supprimer     
				#       - Standardisation ?
    
def main():
    clean_csv_file()
    
if __name__ == "__main__":
    main()