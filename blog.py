#!/usr/bin/python3
import sys
import os
import sqlite3
running = True
def create():
    try:   
        con = sqlite3.connect('ABC.db')
        r= con.execute('PRAGMA foreign_keys=ON')
        c = con.cursor()
        c.execute("create table if not exists category_tab(cat_id integer primary key autoincrement,\
                   categ text not null Unique)")
        c.execute("insert or ignore into category_tab(cat_id, categ) values(0, 'default')")
        c.execute("create table if not exists post_tab(pid integer primary key autoincrement,\
                   post_nam text not null, post_cont text, cati integer references\
                   category_tab(cat_id))") 
    except Exception as error:
        print(str(error))    
#INSERT POST IN blog
def insertPost(post_Nam, post_Cont, categ=0):
    try:
        con = sqlite3.connect('ABC.db')
        c = con.cursor()
        c.execute("select pid from post_tab where post_nam=?",(post_Nam,))
        listname = c.fetchall();
        if len(listname) == 0:
            c.execute("insert into post_tab(post_nam, post_cont,cati)\
                       values(?,?,?)",(post_Nam, post_Cont, categ))
        else:
            print("Post Name is already exists")
    except Exception as err:
        print(str(err))
    finally:
        con.commit()
        con.close()
# to generate list of post... 
def listdb():
    try:
        con = sqlite3.connect('ABC.db')
        c = con.cursor()
        c.execute("select * from post_tab")
        data = c.fetchall()
        for eachr in data:
            query = "select categ from category_tab where cat_id \
                     =" + str(eachr[3])
            cat = list(c.execute(query))
            print("Category:(%s)" %(cat[0]))
            print("ID:%s Post Name: %s   \n\tContent: %s\n"\
                  %(eachr[0], eachr[1], eachr[2]))
    except Exception as err:
        print("No post available",str(err))
# to search KEYWORD in the post 
def searchdb(key):
    try:   
        con = sqlite3.connect('ABC.db')
        c = con.cursor()
        query = "select * from post_tab where post_nam like\
                '%" + key + "%' OR post_Cont like '%" + key + "%'"
        #print(query)
        c.execute(query)
        for row in c.fetchall():
            print("Post Name: %s" %row[1])
            print("Post Content: %s" %row[2])
    except Exception as err:
        print("Command is not valid",str(err))   
    finally:
        con.close()
# to add category to the category list
def createCat(cname):
    try:
        num = cname
        con = sqlite3.connect('ABC.db')
        c = con.cursor()
        c.execute("insert into category_tab(categ) values(?)",(cname,))         
    except Exception as error:
        print("Category Name already exists or default value used ")        
    finally:
        con.commit()
        con.close()
#to print category list
def listCat():
    try:
        con = sqlite3.connect('ABC.db')
        c = con.cursor()
        c.execute("select * from category_tab")
        data = c.fetchall()
        print("Category List")
        for row in data:
            print("ID:%s   Name:%s" %(row[0], row[1]))
        #print("Category Name: %s" %row[1])
    except:
        print("List is empty")      
    finally:
        con.close()

""" here we assign category id to post  pid: post id,
    Cid : category id"""
def assignCat(pid, cid):
    try:
        con = sqlite3.connect('ABC.db')
        c = con.cursor()
        qry1= "select count(*) from category_tab where cat_id =" + str(cid)
        c.execute(qry1)
        data = c.fetchone()
        if data == 0:
            print("Category doesn\'t exists")
        else:
            query = "update post_tab set cati= " + str(cid) + " where pid= " + str(pid)
            c.execute(query)
    except Exception as error:
        print(str(error))
    finally: 
        con.commit()
        con.close()

"""format: blog.py post add "title" "content" --category "cat-name"""
def bothCmd(lst):
    try:  
        createCat(lst[5])
        con = sqlite3.connect('ABC.db')
        c = con.cursor()
        qry ="select cat_id from category_tab where categ='" + str(lst[5]) + "'"
        c.execute(qry)
        cid = c.fetchone()
        if cid != None:
            p = cid[0]
            insertPost(lst[2], lst[3], p)
        print("Post submited with category ", lst[5])
    except Exception as error:
        print(err)      
# command determiner function to decide the command
def cmdDet(arg):
    try:
        if arg[0] == '--help':
            print('----Commands for using blog----')
            print('post')
            print('post list  -> Lists the post present')
            print('post add ["title"] ["content"] -> adds a new post and content ')
            print('post search ["Keyword"] -> searches for posts and content with ["keyword"] present')                                        
            print('post add ["title"] ["content"] --category ["cat-name"] ->adds new post and Category')
            print('\ncategory')
            print('category add [category name] -> adds new category')
            print('category list -> lists the category available')
            print('category [assign post ID] [Cat ID] -> assigns category to the post')
        # Post commands start here
        elif (arg[0] == 'post' and len(arg) >= 2):     
             try:
                if (arg[1] == 'add' and len(arg) == 4):    # add
                    insertPost(arg[2] , arg[3])
                elif arg[1] == 'search':   # Search
                    searchdb(arg[2])
                elif (arg[1] == 'list' and len(arg) == 2):   #list
                    listdb()
                elif (len(arg) == 6):
                    if (arg[4] == '--category'):	# 9th Command
                        bothCmd(arg)
                else:
                    print('Command doesn\'t exist or argument not present')
                    print('for help type blog.py --help')
             except Exception as err:
                 print("Command argument not present or invalid",str(err)) 
                 print('for help type blog.py --help')
        # category commands start from here
        elif (arg[0] == 'category' and len(arg) >= 2):  # category
            try:
                if (arg[1] == 'add' and len(arg) == 3): 
                    if (arg[2].isdigit()) == False:
                        createCat(arg[2]) # adding category name                               
                    else:
                        print("Category name should be words")
                elif (arg[1] == 'list' and len(arg) == 2):      
                    listCat()    #category list command
                elif (arg[1] == 'assign' and len(arg) == 4):    #Category assign 
                    assignCat(arg[2], arg[3])
                else:
                    print("Command incorrect or argument not provided")
            except Exception as error:
                print("Command is invalid", str(error))
        else:
             print('Command or arguments incorrect...')
             print('For help type blog.py --help')
    except Exception as err:
        print('No Argument ')
        print('For help type blog.py --help', str(err))
def main(argv):
    if __name__ == "__main__":
        arg = argv[1:]
        create()
        if len(arg) >= 1:
            cmdDet(arg)
        
main(sys.argv)
