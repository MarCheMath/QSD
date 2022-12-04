import Language
from configuration import LANGUAGE

def names_to_list(names):
    name_list = str.split(names,sep='\n')
    while '' in name_list: name_list.remove('')
    if Language.dummy[LANGUAGE] in name_list:
        raise ValueError(Language.errorMessageDUMMYinNamelist[LANGUAGE].format(Language.dummy[LANGUAGE],name_list))
    if len(name_list)%2==0: #if even number of persons added
        return name_list
    else:
        return name_list+[Language.dummy[LANGUAGE]]