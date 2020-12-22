# I used the command `strace python3 topo_order_commits.py 2>test` to make sure that my code didn't invoke any command line commands. 
import sys
import os
import zlib


def topo_order():
    first = topo[0]
    output = first
    for branch_hash in branch_hashes:
        if first == branch_hashes[branch_hash]:
            output += ' ' + branch_hash
    print(output)
    
    j = 1
    while(len(topo) > j): # Stop when then number of iterations exceeds the length of topo in order to make sure we don't get an index out of ob
        output = ''
        current = topo[j]
        prev_parent = parents[topo[j-1]]

        if current not in prev_parent:
            for x in range(len(prev_parent)):      
                output +=  prev_parent[x]
                if x!= len(prev_parent) - 1:
                    output += ' '
                
            print(output +  '=')
            print ()
            output = '='

            for x in range(len(children[current])):
                output += children[current][x]
                if x != len(children[current]) - 1:
                    output +=  ' '
            print(output)

        output = current
        for branch_hash in branch_hashes:
            if topo[j] == branch_hashes[branch_hash]:
                output += ' ' + branch_hash

        print(output)
        j += 1
                    

        
   
def generate_topo():
    global topo
    topo = list()
    next = [root for root in root_commits]

    # Temporary copies in order to preserve the values of parents and children
    parents_temp = parents
    children_temp = children
    
    while len(next) != 0:
        current = next[0]
        topo.append(current)
        del next[0]
        
        for i in children_temp[current]:
            parents_temp[i].remove(current)
            if(len(parents_temp[i]) == 0):
               next.append(i)
    # Reverse to get correct topo order
    topo.reverse()

def get_commit_nodes():
    global children
    global parents
    children = dict()
    parents = dict()

    temp = [branch_hashes[branch_hash] for branch_hash in branch_hashes]

    # Find parents and children
    while len(temp) != 0:
        current = temp[-1]
        del temp[-1]
        current_dir = f'{git_dir}/objects/{current[:2]}/{current[2:]}'
        commit_contents = zlib.decompress(open(current_dir, 'rb').read()).decode()

        if current not in parents:
            parents[current] = []
        if current not in children:
            children[current] = []

        while(commit_contents.find('\nparent') != -1): # Run while index of '\nparent' exists in commit_contents
            ha = commit_contents[commit_contents.find('\nparent') + 8 : commit_contents.find('\nparent') + 48]
            parents[current].append(ha)
            parent = ha
            if parent not in temp and parent not in parents:
                temp.append(parent)
            if parent not in children:
                children[parent] = []

            children[parent].append(current)
            commit_contents = commit_contents[commit_contents.find('\nparent') + 48:]

          
    # Root commits
    global root_commits
    root_commits = [parent for parent in parents if (len(parents[parent]) == 0)]


def get_git_dir():
    dir = os.getcwd()
    global git_dir
    
    # Check first if .git file is in current directory
    if os.path.isdir(dir + '/.git'):
        git_dir = dir + '/.git'
        return
    # Then check if .git file in parent directories
    else:
        dir = dir.split('/')
        for i in range(len(dir) - 1, 1, -1):            
            if os.path.isdir('/'.join(dir[0:i]) + '/.git'):
                git_dir = '/'.join(dir[0:i]) + '/.git'
                return
    sys.stderr
    sys.exit()
            
            
def get_git_branches():    
    # Append every child file in the /refs/heads directory to a list of branches

    branches = list()
    branch_dir = f'{git_dir}/refs/heads'
    # Check all directories and files within the heads directory
    for root, dirs, files in os.walk(branch_dir):
       for f in files:
           branches.append((f'{root}/{f}')[len(branch_dir)+1:])
            
    global branch_hashes
    branch_hashes = dict()

    for branch in branches:
        branch_hashes[branch] = open(f'{branch_dir}/{branch}', 'r').read().replace('\n', '')
        
def topo_order_commits():
    get_git_dir() # global git_dir
    get_git_branches() # global branches_hashes
    get_commit_nodes() # global children, parents, root_commits
    generate_topo() # global topo
    topo_order() 

    
if __name__ == '__main__':
    topo_order_commits()
