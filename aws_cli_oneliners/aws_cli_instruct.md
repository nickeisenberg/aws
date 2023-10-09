1. Go to 
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
and follow the instruction for installation.

2. Create an access key in the aws consol by...
* logining into the aws consol
* clicking the name on the top right
* click security credentials
* click on create an access key

3. Make sure you save the secret key.

4. Now we can configure the aws terminal client by...
* Open the terminal and run `aws configure`. 
* Enter the access 
* Enter the secret key.
* You can leave the default region blank. It defualts to the US-East. 
* You can leave the default output blank as well too as it defaults to JSON.

5. After successful completion of this, `~/.aws` will be created and will contain the 
files `config` and `credentials`
