# Blog

Blog is command line blogger application, User can add post with category specified.
It has 8 commands to perform add, assign, list, search operations on the blog. It has --help command to view the format of the commands with corresponding explanation about the commands.

Application is built using python 3 and Sqlite3 database. Two tables cover up the backened of the application. First table is for post and second stores the category that are assigned to posts. 

###Commands
 * ./blog.py --help
 * ./blog.py post list  
 * ./blog.py post add "Post Name" "Content"
 * ./blog.py post search "keyword"
 * ./blog.py category add "Category-Name"
 * ./blog.py category list
 * ./blog.py category assign post-id cat-id
 * ./blog.py post add "title" "content" --category "Cat-Name"
  

Blog application responds to the above command format with properly specified arguments. Application creates database tables for the user when run for the first time. In case of invalid format error messages are provided. Framework is not used to built the code.

Blog supports 8 commands those are mentioned above.

###Assumptions
 These are some assumptions which are also the requirement to run the Blog code. 



  * ###Sqlite3 is installed on the machine.
       * Type in following command if sqlite is not present:                            
          * sudo apt-get intall sqlite3 libsqlite3-dev
  * ###Python3 is installed on the machine.
       * Python is installed on stable release version of ubuntu 14.04. 
          Type in following command python3 is not present:
          * sudo apt-get install python3-minimal
          
  * #####Manually change the permission of the file using following command
      * chmod +X blog.py

###Instructions

* Copy and Save the file as blog.py
* run with following command:

```    
 ./blog.py [commands] [arguments1] [argument2]
 
Example:-

./blog.py post list

(This command will list the post already present)
```

###Code Snippets
This section of code is to search for a keyword in the table of post's. The keyword is accepted as argument of the function and searched in the table.

```pythonscript
  def searchdb(key):
    try:   
        con = sqlite3.connect('ABC.db')
        c = con.cursor()
        query = "select * from post_tab where post_nam like\
                '%" + key + "%' OR post_Cont like '%" + key + "%'"
        c.execute(query)
        for row in c.fetchall():
            print("Post Name: %s" %row[1])
            print("Post Content: %s" %row[2])
    except Exception as err:
        print("Command is not valid",str(err))   
    finally:
        con.close()

```


###Unit Test Cases
Unit test cases are provided in separate repository. The test cases are created using the builtin Unittest framework. Unittest is a pythons standard library since version 2.1.

You can download and store test cases file in any folder and run:
```
:~/YourFolder/TestCases$ python3 test_Case_file.py

```
To run all the tests in the directory, run following command from the directory which contains all the test cases:
```
/TestCase_directory$ python3 -m unittest discover 
```


### Libraries

* sqlite3 : This is the sqlite library to connect to the database and carry the             transactions.

* unittest : This modules used to write the test cases
            
