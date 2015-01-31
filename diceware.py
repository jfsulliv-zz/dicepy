#!/usr/bin/python
import os,sys,getopt,math,string,random

minEntropy = 56 # Set higher as needed

def diceware(num, wlist, sep):
    phrase = ""
    gen = random.SystemRandom()
    for i in range(0,num):
        phrase += diceround(wlist, gen)
        if i < num-1:
            phrase += sep
    return phrase

def diceround(wlist, gen):
    total = len(wlist)
    val = gen.randint(0,total)
    return wlist[val].rstrip()

def isAscii(s):
    return all(ord(c) < 128 for c in s)

def computeEntropy(n, wordlist):
    total = len(wordlist)
    space = math.pow(total,n)
    ent = math.log2(space)
    return ent

def numWords(entropy, wordlist):
    total = len(wordlist)
    space = math.pow(2,entropy)
    wc = math.log(space, total)
    return math.ceil(wc)

def usage(pname):
    print (
    """
    Usage: %s [OPTIONS]
    Generate a strong Diceware password, writing to standard output.

      -h,  --help                   Display this message and exit. 
      -w num, --words=num           Specify the number of words 
                                    (default=5)
      -e num, --entropy=num         Specify the minimum key entropy
                                    (overrides -w, default=0)
      -s sep, --seperator=sep       Specify the words separator
                                    (default=".")
      -d file, --dictionary=file    Specify the dictionary file
                                    (default=/usr/share/words)
      -o file, --output=file        Specify an output file.
                                    (default=None)

    PROPER USAGE
    ============
    For best results, the following settings should be used.
    1) At least 48 bits of entropy. More entropy is better.
    2) A dictinary file with at least 65536 words. Less words in a 
        dictionary file will mean less password entropy.
    3) The word seperator should not be an alphabetic character, as
        this can create collisions!

        Example:
            let.ing
            letting

    """ %pname )
def main(name, argv):
    try:
        opts, args = getopt.getopt(argv, "hw:e:d:s:o:",
        ['help','words=','entropy=','dictionary=','seperator=','output='])
    except getopt.GetoptError:
        usage(name)
        sys.exit(1)

    words = 6
    entropy = 0
    dictfile = "/usr/share/dict/words"
    sep = '.'
    out = None
    for opt, arg in opts:
        if opt in ('-h','--help'):
            usage(name)
            sys.exit(0)
        elif opt in ('-w', '--words'):
            words = int(arg)
        elif opt in ('-e', '--entropy'):
            entropy = int(arg)
        elif opt in ('-d', '--dictionary'):
            dictfile = arg
        elif opt in ('-s', '--seperator'):
            sep = arg
            if sep.isalpha():
                print("WARNING - Don't use an alphabetic word "
                "separator. This may result in password collisions, "
                "weakening the password's strength.")
        elif opt in ('-o', '--output'):
            out = arg

    # Check the options for legality
    if out != None:
        of = open(outfile, 'rw')

    if entropy <= 0 and words <= 0:
        print("Error - Must specify positive word count or entropy.")
        exit(1)
    if entropy > 0:
        useEntropy = 1
    else:
        useEntropy = 0

    df = open(dictfile, 'r')
    if df == None:
        print("Error - File " + dictfile + " not found.")
        exit(1)

    wordlist = []
    for line in df:
        if not isAscii(line) or "'s" in line:
            continue
        wordlist.append(line)

    if useEntropy:
        words = numWords(entropy,wordlist)
        entropy = computeEntropy(words, wordlist)
        print("Words = " + str(words))
        print("Entropy = " + str(entropy))
    else:
        entropy = computeEntropy(words, wordlist)
        print("Words = " + str(words))
        print("Entropy = " + str(entropy))

    if entropy < minEntropy:
        print("WARNING - Password will have less than " +
        str(minEntropy)
        + " bits of entropy. This may be an insecure password.")

    print("Generating Password. This may take some time. Performing "
    "some other tasks on the computer may help to populate the entropy "
    "pool.")
    print("...")
    passphrase = diceware(words, wordlist, sep) 
    if out:
        of.write(passphhrase)
        print("Password written to " + out)
        of.close()
    else:
        print("")
        print(passphrase)
        print("")
    sys.exit()

if __name__=="__main__":
    main(sys.argv[0], sys.argv[1:])

