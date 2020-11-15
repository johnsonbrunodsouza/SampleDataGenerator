import configuration
import json
from random import choice,randint
import string
import sys

TAB = '\t'

data_types2methods = {'CHAR':string.ascii_letters,'VARCHAR':string.ascii_letters,'DECIMAL':string.digits}

### get configuration
def read_configuration(conf_file):
    try:
        with open(conf_file) as c_file:
            json_conf = json.load(c_file)
            config  = configuration.configuration(**json_conf)
    
        return config
    except:
        print("Exception:" + str(sys.exc_info()[1]))
    return None

### parse data type 
def parse_datatype(column_type):
    return column_type.strip().replace(' ','').replace('(',' ').replace(')','').replace(',',' ').split(' ')

### gets fie
def read_field_type_config(config):
    field_list = []
    field_value_dict={}
    processed_header = False
    with open(config.column_types_config_file, mode="r") as conf_handler:
        for line in conf_handler.readlines():
            fields = line.strip().split(config.delimiter)

            if not processed_header:
                processed_header = True
                for index,item in enumerate(fields):
                    if item in config.__dict__.values():
                        field_value_dict[item] = index
            else:
                datafield_index = field_value_dict[config.datatype_fieldname]
                populate_field_flag_index = field_value_dict[config.populate_data_flag_fieldname]
                if len(fields) > max( datafield_index,populate_field_flag_index):
                    datatype_field = fields[datafield_index]
                    populate_field_flag = False
                    if fields[populate_field_flag_index].upper() == "TRUE":
                        populate_field_flag = True
                    
                    field_list.append( (datatype_field,populate_field_flag) )
    return field_list

def get_field_mappings(config,header):
    fields = header.strip().split(config.delimiter)
    field_value_dict = {}
    for index,item in enumerate(fields):
        if item in config.__dict__.values():
            field_value_dict[item] = index
    return field_value_dict

### geneate random value based on data type and length
def generate_radom_value(config,field_list):
    with open(config.output_file,"w") as file_handler:
        for row in range(0,config.number_of_rows):
            output_line = []
            for tuple_item in field_list:
                tokens = parse_datatype(tuple_item[0])
                datatype_length = int(tokens[1])
                random_length = datatype_length
                if datatype_length>1:
                    random_length = randint(0,int(tokens[1]))
                randam_value = ''.join(choice(data_types2methods[tokens[0].upper()]) for i in range(random_length)).capitalize()
                generated_field_value = randam_value + " " * (int(tokens[1]) - random_length)
                output_line.append(generated_field_value)
            
            file_handler.write(''.join(output_line) + '\n')
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_data_generator.py configuration.json")
        exit(1)
    
    config = read_configuration(sys.argv[1])

    field_list = read_field_type_config(config)
    #print(field_list)
    generate_radom_value(config,field_list)


    



    
    

#