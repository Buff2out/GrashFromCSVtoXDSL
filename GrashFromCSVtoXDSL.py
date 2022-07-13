import csv

# Реализовать метод рассчёта вероятности нечётного и четного
def alg_1(nd):
    cntNd = 2 ** (len(nd))
    b = bin(0)
    sz = len(bin(cntNd - 1)) - 2
    probVec = []
    
    sum1 = 0
    for i in range(len(nd)):
        sum1 += 1
    
    
    for p in range(cntNd - 1, -1, -1):
        b = bin(p)
        sum2 = 0
        k = from_binstr_to_list(b[2:], sz)
        for i in range(len(k)):
            sum2 += k[i]
        
        probVec.append( str(round((sum2)/(sum1), 6) ) )
        probVec.append( str(round(1 - float(probVec[len(probVec) - 1]), 6 )) )
        
    
    return probVec



def alg_2(Node, nd):
    cntNd = 2 ** (len(nd))
    b = bin(0)
    sz = len(bin(cntNd - 1)) - 2
    probVec = []
    
    sum1 = 0
    for i in range(len(nd)):
        sum1 += Node[nd[i]]
    
    
    for p in range(cntNd - 1, -1, -1):
        b = bin(p)
        sum2 = 0
        k = from_binstr_to_list(b[2:], sz)
        for i in range(len(k)):
            sum2 += k[i] * Node[nd[i]]
        
        probVec.append( str(round(0.99 * (sum2)/(sum1), 6) ) )
        probVec.append( str(round(1 - float(probVec[len(probVec) - 1]), 6 )) )
        
    
    return probVec
            
            
        
        
def from_binstr_to_list(st, sz):
    lst = []
    for i in range(sz - (len(st)) ):
        lst.append(0)
    for i in range(len(st)):
        lst.append( int(st[i]) )

    return lst
        
    
    
def find_i(Nodes, id_nd):
    for i in range(len(Nodes)):
        if Nodes[i]["Name"] == id_nd:
            return i
    
    
def find_nodes_n_output(line, Nodes):
    new_fl = []
    q, i, nd, id_nd = 0, 0, '', ''
    while i < len(line):
        q, nd = get_id(line[i])
        if q == 1:
            new_fl.append(line[i])
            id_nd = nd
            for j in range(2):
                i += 1
                new_fl.append(line[i])
            i += 1
            
            num_id_nd = "".join(c for c in id_nd if  c.isdecimal())
            
            q, nd = get_nodes(line[i])
            if q == 1 and len(num_id_nd) >= 2:
                nd = swap_mng_fr(nd)
                new_fl.append("			<parents>" + nd + "</parents>" + '\n')
            else: 
                new_fl.append(line[i]) 
                
            if q == 1 and len(num_id_nd) >= 2:
                nd = nd.split()
                ind = find_i(Nodes, id_nd)
                probVec = alg_2(Nodes[ind], nd)
                probVec1 = " ".join(probVec)
                new_fl.append("			<probabilities>" + probVec1 + "</probabilities>" + '\n')
                i += 1
            elif q == 1 and len(num_id_nd) == 1:
                nd = nd.split()
                probVec = alg_1(nd)
                probVec1 = " ".join(probVec)
                new_fl.append("			<probabilities>" + probVec1 + "</probabilities>" + '\n')
                i += 1
            i += 1
                
        elif q == 0:
            new_fl.append(line[i])
            i += 1
            
    return new_fl
    
    
    
def swap_mng_fr(nd):
    nd = nd.split()  # to list
    for i in range(len(nd)):
        temp = ""
        if nd[i][len(nd[i]) - 1] == "C":
            temp = nd[i]
            del nd[i]
            nd.insert(0, temp)
            nd = " ".join(nd) # to str
            return nd   # return str
    
    
    
        
def get_id(line):
    if line[2:11] == '<cpt id="':
        return 1, line[11:-3]
    else:
        return 0, line
    
    
def get_nodes(line):
    if line[3:12] == '<parents>':
        return 1, line[12:-11]
    else:
        return 0, line
        

    
        
def filt(reader):
    list1 = []
    Nodes = []
    for i in reader: # инициализируем данные таблицы в матрицу для простоты
        list1.append(i)
    i, j = 0, 0
    p, length = 0, 0
    while i < len(list1): # для всех узлов реализуем список словарей Nodes
        j = 0
        p = 1
        Nd = {}
        while j + 1 < len(list1[i]) and list1[i][j + 1] == "Name of":
            d1 = {"Name": list1[i][j]}
            Nd.update(d1)
            #print("filt1", list1[i + p][j], list1[i + p][j + 2], "NodeName", list1[i][j])
            while i + p < 152 and list1[i + p][j] != "Manager op":
                #print("filt2", list1[i + p][j], list1[i + p][j + 2], "NodeName", list1[i][j])
                if list1[i + p][j] != '':
                    #print("filt3", list1[i + p][j], list1[i + p][j + 2], "NodeName", list1[i][j])
                    if list1[i + p][j + 2] == "Weak":
                        d1 = {list1[i + p][j]: 3} # добавляем силу связи в словарь
                    elif list1[i + p][j + 2] == "Medium":
                        d1 = {list1[i + p][j]: 8}
                    elif list1[i + p][j + 2] == "Strong":
                        d1 = {list1[i + p][j]: 20}
                    else:
                        d1 = {list1[i + p][j]: 8}
                        print(d1)
                    Nd.update(d1)
                p += 1
            if list1[i + p][j + 2] == "Weak":
                d1 = {Nd["Name"] + 'C': 3, Nd["Name"] + 'S': 3} # Manager op
            elif list1[i + p][j + 2] == "Medium":
                d1 = {Nd["Name"] + 'C': 8, Nd["Name"] + 'S': 3}
            elif list1[i + p][j + 2] == "Strong":
                d1 = {Nd["Name"] + 'C': 20, Nd["Name"] + 'S': 3}
            Nd.update(d1)
            Nodes.append(Nd)
            Nd = {}
            j += 3
            p = 1
        i += p
    lst = Nodes
                
    return lst



with open("EssenceGraph_22.03_true.xdsl", 'r') as file:
    res = []
    for line in file:
        res.append(line)
        
    
    with open("Alphs.csv", "r") as ta:
        reader = csv.reader(ta)
        
        Nodes = filt(reader)
      
    new_fl = find_nodes_n_output(res, Nodes)

    # Фильтровать с 2 и более цифрами, найти в Nodes индекс по Name
    # Реализовать 2^(n + 1) перестановок отрицания между этих узлов
    # Реализовать формулу и в OUTPUT
        
            
with open(".\EssenceGraph_R_09.02_3_COPY.xdsl", 'w') as outp:
    for i in new_fl:
        outp.write(i)