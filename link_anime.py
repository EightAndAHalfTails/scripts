#!/usr/bin/env python
def unbracket(string, left='[', right=']'):
    result = ""
    bracket_depth = 0
    for char in string:
        if char == left:
            bracket_depth += 1
        if bracket_depth == 0:
            result += char
        if char == right:
            bracket_depth -= 1
    return result

def niceify(string):
    result = unbracket(string)
    result = unbracket(result, left='(', right=')')
    result = result.replace('.mkv','')
    result = result.replace('.avi','')
    result = result.replace('_',' ')
    result = result.replace('.',' ')
    result = result.replace('v2', '')
    result = result.replace('v3', '')
    result = result.replace('`', '\'')
    result = result.lstrip()
    result = result.rstrip()
    return result

if __name__=="__main__":
    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    args = parser.parse_args()
    #print(args.target)

    for filename in os.listdir(args.target):
        link = niceify(filename)
        target=args.target + '/' + filename
        #print(args.target + filename)
        #print(link)
        try:
            os.link(target, link)
        except FileExistsError:
            pass#print("File Exists: {}".format(target))
        except PermissionError as e:
            print("Linking file {} failed: {}".format(target, e.strerror))
