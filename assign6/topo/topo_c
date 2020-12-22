import zlib
import sys
import os


def topo_order_commits():
    child_commits = dict()
    parent_commit = dict()
    branch_commit = get_localBranch()
    full_commits = create_relations(child_commits, parent_commit)
   
    topo_order = create_topo()

    # all the commit hashses will be printed out in topological order 
    output = topo_order[0]
    for x in branch_commit:
        #go through the correct amount of time
        if topo_order[0] == branch_commit[x]:
            #make sure to seperate each branch with a space
            output = output + " " + x
    print (output)

    # initialize a variable to compare with the topo list 
    x = 1
    #go through topo list until the length becomes greater than the addition
    while (len(topo_order) > x):
        output= ""
        commit_curr = topo_order[x]
        parent_prev = parent_commit[topo_order[x-1]]

        # first check the commit_curr in the the parent of the previous commit 
        if commit_curr not in parent_prev:
            for place in range(len(parent_prev)):
                new_parent = len(parent_prev) - 1
                if place != new_parent:
                    # add the previous parent comment into the next line
                    output = output + parent_prev[place] + " "
                else:
                    # then add the children of the current parent commit just added 
                    output = output + parent_prev[place]
            
            print (output + "=")
            print ()
            output = "="
            
            for place in range(len(child_commits[commit_curr])):
                if place == len(child_commits[commit_curr]) - 1:
                    output = output + child_commits[commit_curr][place]
                else:
                    output = output + child_commits[commit_curr][place] + " "
            print (output)
        
        output = commit_curr
        for y in branch_commit:
            if topo_order[x] == branch_commit[y]:
                output = output + " " + y
        # prints the branch and hash of commit if verivied that the commit is a branch 
        print(output)
        
        #make sure to increment the count of x 
        x = x + 1

# get all the branches in the specific git reposititory 
def get_localBranch():
    #use the os.path to find all the branches inside git/refs/heads
    directory_branch = os.path.join (get_git_top(), 'refs', 'heads')
    branch_names = []
    for a, b, c in os.walk(directory_branch):
        for x in c: 
            path_fullBranch = os.path.join(a, x)
            branch = path_fullBranch[len(directory_branch)+1:]
            branch_names.append(branch)  

    commit_branch = dict()
    #read hashes stored inside each branch file
    for x in branch_names:
        ID = open((os.path.join (directory_branch, x)), 'r').read().replace('\n', '')
        commit_branch[x] = ID

    return commit_branch

def create_relations (child_commits = dict(), parent_commit = dict()):
    # we will build a commit graph using the contents inside .../.git/objects
    # we will start our relation with our branches
    branch_contents = get_localBranch()
    commit_root = []
    stack = [] # for DFS
    for b in branch_contents:
        stack.append(branch_contents[b])
    
    # find the parent and child of each commit 
    while True:
        commit_curr = stack.pop()
        commit_curr_path = os.path.join((os.path.join (get_git_top(), 'objects')), commit_curr[:2], commit_curr[2:])
        compressed = open(commit_curr_path, 'rb').read()
        contents_de = zlib.decompress(compressed).decode()

        if commit_curr not in parent_commit:
            parent_commit[commit_curr] = []
        if commit_curr not in child_commits:
            child_commits[commit_curr] = []
     
        
        while (-1 < contents_de.find('\nparent')):
            parent = contents_de[contents_de.find('\nparent') + 8: contents_de.find('\nparent') + 48]
            parent_commit[commit_curr].append(contents_de[contents_de.find('\nparent') + 8: contents_de.find('\nparent') + 48])
            
            if parent not in stack and parent not in parent_commit:
                stack.append(parent)
            
            if parent not in child_commits:
                child_commits[parent] = []
            
            child_commits[parent].append(commit_curr)
            contents_de = contents_de[contents_de.find('\nparent') + 48:]

        if (len(stack) == 0):
            break                                                

    #find root_nodes (commits with no parents)
    for x in parent_commit:
        if (len(parent_commit[x]) == 0):
            commit_root.append (x)
            
    return commit_root

#function gets the top level git directory path 
def get_git_top():
    while (os.path.dirname(os.getcwd()) != os.getcwd()):
        # if a path is found, return the path with the ./git
        if (os.path.isdir(os.getcwd() + '/.git')):
       	    return os.path.join (os.getcwd(), '.git') 

def create_topo ():
    # get parent and chilren relation by calling create_relations
    child_commits = dict()
    parent_commit = dict()
    root_commits = create_relations(child_commits, parent_commit)

    # buld tological ordering relation using DFS
    topo_order = []
    next = []

    # first add all commits with no parents into next
    for x in root_commits:
        next.append (x)


    while True:
        commit_curr = next.pop(0)
        topo_order.append(commit_curr)

        for x in child_commits[commit_curr]:
            parent_commit[x].remove(commit_curr)
            
            if (len(parent_commit[x]) == 0):
                next.append(x)

        if (len(next) == 0):
            break

    # before you return make sure to reverse the list 
    topo_order.reverse()
    
    #finally return the topological order
    return topo_order


if __name__ == '__main__':
     topo_order_commits()
