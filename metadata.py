import os, sys, glob, json, random, time, copy, string, re, ast
import json5 as json
import base64
sys.path.append(os.getcwd())
import subprocess
import pkg_resources

required  = {'json5'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing   = required - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
    
#print("os.getcwd() : "+os.getcwd())
#print("__file__ : "+__file__)
#print("os.path.dirname(__file__) : "+os.path.dirname(__file__))
#os.chdir(os.path.dirname(__file__))
#print(__name__)

from ConsoleColor import print, console
    
try:
    fullpaths=[]
    for v in range(1, len(sys.argv)):
        #print("[cyan]args[/cyan] : ",sys.argv[v])
        if os.path.isdir(sys.argv[v]):
            fullpaths+=glob.glob(sys.argv[v]+"\\*.safetensors", recursive=True)
        else:
            fullpaths+=glob.glob(sys.argv[v], recursive=True)
    #print(fullpaths)
    for fn in fullpaths:
        if os.path.isfile(fn+".txt"):
            print(f"{fn} [cyan]txt exist[/cyan]")
            continue
        print(f"{fn} [green]run[/green]")
        try:
            with open(fn, 'rb') as f:
                bytes = f.read(8)
                #print(bytes)
                i=int.from_bytes(bytes, byteorder='little')
                #print(i)
                bytes=f.read(i)
                text=bytes.decode('utf-8')
                #text=str(bytes, 'utf-8')
                #print(text)
                d=json.loads(text)
                #d=ast.literal_eval(text)
                #print(d)
                #print(type(d))
                #print(type(d["__metadata__"]))
                if "__metadata__" not in d :#or "ss_tag_frequency" not in d["__metadata__"]
                    with open(fn+".txt", 'x', encoding='utf-8') as fp:
                        print(f"{fn} [yellow]txt no[/yellow]")
                        continue
                    
                d2=d["__metadata__"]
                if "ssmd_cover_images" in d2 :
                    print("ssmd_cover_images")
                    imgstring=d2.pop("ssmd_cover_images",None)
                    imgdata = base64.b64decode(imgstring)
                    with open(fn+".png", 'wb') as fi:
                        fi.write(imgdata)
                if "ss_tag_frequency" in d2 :
                    print("ss_tag_frequency")
                    d2["ss_tag_frequency"]=json.loads(d2["ss_tag_frequency"])
                if "ss_datasets" in d2 :
                    print("ss_datasets")
                    d2["ss_datasets"]=json.loads(d2["ss_datasets"])
                #text2=d["__metadata__"]["ss_tag_frequency"]
                #print(type(text2))
                #for v in text2:
                #    #print(text2[v])
                #    #print(v)
                #    #text2[v]=json.loads(text2[v])
                #    try:
                #        text2[v]=ast.literal_eval(text2[v])
                #    except Exception:
                #        pass
                #text2=ast.literal_eval(text2)
                #text2=json.dumps(text2)
                #text2=json.loads(text2)
                #print(type(text2))
                #print(text2)
                #nm=os.path.splitext(fn)[0]
                #print(nm)
                with open(fn+".txt", 'w', encoding='utf-8') as fp:
                    json.dump(d2, fp, sort_keys=False, indent=4)
                print(f"{fn} [green]txt make[/green]")
        except Exception:
        
            #print(f"[{ccolor}]vmin,vmax,i : [/{ccolor}]",vmin,vmax,i)
            console.print_exception()
            with open(fn+".txt", 'w', encoding='utf-8') as fp:
                fp.write("Exception")
                #pass
            print(f"{fn} [red]txt Exception[/red]")


except Exception:
    #print(f"[{ccolor}]vmin,vmax,i : [/{ccolor}]",vmin,vmax,i)
    console.print_exception()
    quit()
