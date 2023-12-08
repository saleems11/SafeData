# SafeData
Using the registraion password, the MFA token is encrepted

#### Some Information regarding how the SafeData application Stores the password
Using the user password a hash key is generated in the size of 256 bits, the hashed 
password is used to encrypt the MFA key via AES-256-CBC,
then this encrypted key is stored in a file.

##### Authentication Process
The authentication is required for (Encryption/Decryption)!
The User Enter his password and Mfa pin, the password is Hashified
then the Mfa key is decrypted, using the MFA key the MFA pin is validated. 

## Encryption Used:
**AES**, based on:  
https://www.arcserve.com/blog/5-common-encryption-algorithms-and-unbreakables-future  
**CBC**, based on:
https://security.stackexchange.com/questions/184305/why-would-i-ever-use-aes-256-cbc-if-aes-256-gcm-is-more-secure

###### Encryption Process
Using the hashed mfa key the passwords are encrypted, also Gebbrish data is added.

###### Decryption Process
Using the hashed user password key the passwords are decrypted. 


#### Possible attacks

##### Password is Known:
The password could be hashified and the MFA key could be decrypted.
So, for now it is very vonurable for this attack. 

##### MFA key is Known:
As the password is hashified, it is very dificult to get back his value, the only attack
that could be used is guessing the password and try encrypting the MFA key to have the same
encrypted value.

##### Feature that I have Plan to add:
**1. API Support**  
**2. More Secure Password Saving Method**


## To Do:
1. Allow multi Users
2. Save More Data

Saleem Saiegh