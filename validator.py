from lxml import etree
from io import StringIO
import sys

xml_file = sys.argv[1]

#open and read xml file
#with open(xml_file, 'r') as xml_file_r:
#    xml_to_check = xml_file_r.read()

# parse xml
try:
    parser = etree.XMLParser(dtd_validation=True)
    doc = etree.parse(xml_file, parser)
    print('XML well formed, syntax ok.')

# check for file IO error
except IOError:
    print('Invalid File')

# check for XML syntax errors
except etree.XMLSyntaxError as err:
    print('XML Syntax Error, see error_syntax.log')
    with open('error_syntax.log', 'w') as error_log_file:
        error_log_file.write(str(err.error_log))
    quit()

except:
    print('Unknown error, exiting.')
    quit()
