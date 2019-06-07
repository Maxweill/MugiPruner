import os, ConfigParser,io

def get_list():
    with open("config.INI") as f:
        sample_config = f.read()
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.readfp(io.BytesIO(sample_config))

    Images=[]
    Extension = ['JPG', 'BMP', 'PNG']
    for dirpath, dirnames, filenames in os.walk(unicode(config.get('config','ParentDir'))):
        for filename in filenames:

            Image = os.path.join(dirpath, filename)
            #print(Image)
            ext = Image.split('.')[::-1][0].upper()
            if ext in Extension:
                Images.append(Image)
        if config.get('config','Recursive')!="true":
            break
    return Images