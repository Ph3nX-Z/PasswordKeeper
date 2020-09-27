##By Ph3nX-Z on github : https://github.com/Ph3nX-Z/  ##
import hashlib
import binascii
class Hash:
    def __init__(self,passwd):
        self.hash=None
        self.real=passwd
    def hasher(self):
        final_hash=""
        word=self.real

        salt="db"
        salted=hashlib.sha3_512(salt.encode())
        salted=salted.hexdigest()

        md5=hashlib.md5(word.encode())
        md52=md5.hexdigest()

        sha1=hashlib.sha1(word.encode())
        sha12=sha1.hexdigest()

        ntlm=hashlib.new('md4', word.encode('utf-16le')).digest()
        ntlm2=binascii.hexlify(ntlm).decode("utf8")

        for letter in salted[8:16]:
            md52+=letter
        for letters in salted[16:20]:
            ntlm2+=letters
        for letter2 in salted[0:4]:
            ntlm2+=letter2


        index=0
        for index in range(0,40,1):
            to_add=ntlm2[index]+sha12[index]+md52[index]
            final_hash+=to_add

        final_hash=final_hash[::-1]
        final_hash_marked="<--$Ph3nX-Z$"+final_hash+"-->"
        self.hash=final_hash_marked
    def verify(self):
        self.hasher()
        with open('accounthash.hash','r') as hashfile:
            hash_from_file=hashfile.read()
        if hash_from_file==self.hash:
            return True
        else:
            return False
    def __str__(self):
        self.hasher()
        return self.hash

if __name__=='__main__':
    hash1=Hash("password")
    print(hash1)
    status=hash1.verify()
    print(status)