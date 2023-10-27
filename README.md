# SafeData
Using the registraion password, the MFA token is encrepted

#### Some Information regarding how the SafeData application Stores the password
Using the user password a hash key is generated, the hashed password is used to encrypt the MFA key,
then this encrypted key is stored in a file.

##### Authentication Process
The authentication is required for (Encryption/Decryption)!
The User Enter his password and Mfa pin, the password is Hashified
then the Mfa key is decrypted, using the MFA key the MFA pin is validated. 

###### Encryption Process
Using the hashed user password key the passwords are encrypted.

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


Saleem Saiegh