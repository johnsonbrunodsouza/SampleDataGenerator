import json
from random import choice,randint
import string
import sys
from collections import namedtuple
import os
import pandas as pd

TAB = '\t'

data_types2methods = {'CHAR':string.ascii_letters,'VARCHAR':string.ascii_letters,'DECIMAL':string.digits}

### parse data type 
def parse_datatype(column_type):
    return column_type.strip().replace(' ','').replace('(',' ').replace(')','').replace(',',' ').split(' ')

def get_running_record(rec_prefix,num):
    if '$' in rec_prefix:
        literal = rec_prefix[0:rec_prefix.index('$')]
        padding_len = len(rec_prefix[rec_prefix.index('$'):])
        record = literal + str(num).zfill(padding_len)
        return record
    else:
        return rec_prefix

def generate_sample_data(config,field_type_df,lookup):
    package_name = config.package[0::2]
    package_row_prefix = config.package[1::2]

    with open(config.output_file,"w") as file_handler:
        for row in range(1,config.number_of_rows+1):
            for p_tuple in zip(package_name,package_row_prefix):
                prefix = get_running_record(p_tuple[1],row)
                output_line = [prefix]

                filtered = field_type_df[ field_type_df[config.fields_configuration.searchfield_column] == p_tuple[0] ]
                filtered = filtered.dropna()
                for index in filtered.index:
                    data_type = filtered[config.fields_configuration.datatype][index]
                    tokens = parse_datatype(data_type)
                    datatype_length = int(tokens[1])
                    random_length = datatype_length
                    column_for_lookup =  filtered[config.fields_configuration.de_refernce][index]

                    if column_for_lookup in lookup:
                        random_index = randint(0,len(lookup[column_for_lookup])-1)
                        look_up_value = lookup[column_for_lookup][ random_index ]
                        output_line.append(str(look_up_value))
                    else:
                        if datatype_length>1:
                            random_length = randint(0,int(tokens[1]))
                        randam_value = ''.join(choice(data_types2methods[tokens[0].upper()]) for i in range(random_length)).capitalize()
                        generated_field_value = randam_value + " " * (int(tokens[1]) - random_length)
                        output_line.append(generated_field_value)
                file_handler.write(''.join(output_line) + '\n')

def load_configurations(config_file):
    """Loads application configuration 
    
    Parameters:
    config_file(str): Path of application configuration file

    Returns:
    config: configurations
    """

    def json2class(c_dict):
        return namedtuple('config',c_dict.keys())(*c_dict.values())

    with open(config_file) as c_file:
        json_file_str = ''.join(c_file.readlines())

    config = json.loads(json_file_str,object_hook=json2class)
    return config


def help():
    print("Usage: python test_data_generator.py configuration.json")

def validate_config_file(config):
    _,file_extention = os.path.splitext(config.column_types_config_file)

    if file_extention.upper() in [".XLS",".XLSX"]:
        df = pd.read_excel(config.column_types_config_file)
        fields_of_interest = [config.fields_configuration.searchfield_column, \
                              config.fields_configuration.populate_data_flag, \
                              config.fields_configuration.datatype,\
                              config.fields_configuration.de_refernce]
        return df[fields_of_interest]

def get_lookup_data(config):
    lookup_table = {}
    df = pd.read_excel(config.lookup_data)

    for column in df.head():
        column_values = [item for item in df[column].to_list() if str(item) != 'nan']
        lookup_table[column] = column_values

    return lookup_table

if __name__ == "__main__":
    if len(sys.argv) != 2:
        help()
        exit(1)
    
    config = load_configurations(sys.argv[1])
    field_type_df = validate_config_file(config)
    lookup = get_lookup_data(config)
    generate_sample_data(config,field_type_df,lookup)


def adding_a_function_git():
    return -1