from graph import Graph
import time as casio

from tqdm import tqdm

def readGraph() -> Graph:
    """
    Reads the web-Google.txt file and returns a Graph object
    """
    page_graph = Graph()
    print("Reading web-Google.txt...")
    total_lines = 5105044  # Accurate total number of lines in the file
    with open('tp4/web-Google.txt', 'r') as file:
        # Skip initial comment lines
        for l in file:
            if l.startswith("#"):
                total_lines -= 1  # Adjust total_lines for each comment line skipped
            else:
                break

        for l in tqdm(file, initial=1, total=total_lines):
            if l.startswith("#"):
                continue  # Skip any additional comment lines
            parts = l.strip().split("\t")
            if len(parts) == 2:
                source, target = parts
                if not page_graph.vertex_exists(source):
                    page_graph.add_vertex(source)
                if not page_graph.vertex_exists(target):
                    page_graph.add_vertex(target)
                page_graph.add_edge(source, target)
    print("Finished reading web-Google.txt")
    return page_graph

def processTime(start, end, message="Time elapsed: "):
    # Create a function that prints the hours or minutes only if they are greater than 0, and the seconds always with 2 decimal places
    hours, remainder = divmod(end - start, 3600)
    minutes, seconds = divmod(remainder, 60)
    seconds = round(seconds, 2)
    if hours > 0: # Espero que esto nunca se cumpla
        print(message + f"{hours:.0f}h {minutes:.0f}m {seconds}s")
    elif minutes > 0:
        print(message + f"{minutes:.0f}m {seconds}s")
    else:
        print(message + f"{seconds}s")

def act1(page_graph: Graph):
    print("--------------------")
    print("         P1         ")
    print("--------------------")
    start = casio.time()
    
    print("Calculating number of weakly connected components and size of the biggest weakly connected component...")
    number_of_wcc, wcc_dict = page_graph.getNumberOfWCC()
    biggest_wcc_size = page_graph.getBiggestWCC(wcc=wcc_dict)

    print(f"Number of weakly connected components: {number_of_wcc}")
    print(f"Size of the biggest weakly connected component: {biggest_wcc_size}")
    
    end = casio.time()
    
    processTime(start, end)
    print()
    # Los resultados son: 
    # Number of weakly connected components: 2746 
    # Size of the biggest weakly connected component: 855802

def act2(page_graph: Graph):
    # Como mi grafo tiene 875713 vertices, no puedo calcular el tiempo que me llevaría recorrer todos los caminos mínimos; pero puedo tomar una muestra de tamaño N y calcular el promedio de los caminos mínimos de esa muestra, después multiplicar ese promedio por el total de caminos mínimos posibles para obtener una estimación del tiempo que me llevaría recorrer todos los caminos.
    
    print("--------------------")
    print("         P2         ")
    print("--------------------")
    
    start = casio.time()
    
    n = 100
    
    print(f"Estimating time for all shortest paths with {n} samples...")
    time = page_graph.estimateTimeForShortestPaths(n, seed=None)
    processTime(0, time, "Estimated time: ")
    
    end = casio.time()
    
    processTime(start, end)
    print()    
    # El resultado es: 
    # Estimated time: 328.0h 43.0m 20.89s
    
def act3(page_graph: Graph, undirected = False):
    print("--------------------")
    print("         P3         ")
    print("--------------------")
    
    start = casio.time()
    
    print("Calculating the number of triangles using a directed Graph...")
    n_triangles_directed = page_graph.getNumberOfTrianglesDirected()
    print(f"Number of triangles using a Directed Graph: {n_triangles_directed:,}")
    
    if undirected:
        print("Calculating the number of triangles using an undirected Graph...")
        n_trinagles_undirected = page_graph.getNumberOfTrianglesUndirected()
        print(f"Number of triangles using an Undirected Graph: {n_trinagles_undirected:,}")
        
    end = casio.time()
    
    processTime(start, end)
    print()    
    # Results:
    # Number of triangles using a Directed Graph: 3,889,771
    # Number of triangles using an Undirected Graph: 13,391,903
    
def act4(page_graph: Graph):
    print("--------------------")
    print("         P4         ")
    print("--------------------")
    
    # Acá nuevamente no puedo calcular el diámetro del grafo, pero puedo tomar N puntos de inicio e iterar buscando los caminos más largos comparándolos entre sí.
    
    start = casio.time()
    
    n = 10
    print(f"Estimating the diameter of the graph with {n} starting vertices...")
    diameter = page_graph.estimateGraphDiameter(n, seed=None, directed=False)
    print(f"Estimated diameter of the graph: {diameter}")
    
    end = casio.time()
    
    processTime(start, end)
    print()    
    # Estimated diameter of the graph: 24
    # Time elapsed: 6m 0.09s
    
def act5(page_graph: Graph):
    print("--------------------")
    print("         P5         ")
    print("--------------------")
    
    # Calculo el pageRank de los 10 primeros vértices
    start = casio.time()
    
    n = 10
    
    print(f"Finding the top {n} vertices with the highest PageRank...")
    
    print(page_graph.getTopPageRankVertices(n))
    end = casio.time()
    
    processTime(start, end)
    print() 
    
    # Results
    # Converged after 61 iterations, aborting...
    # Top vertices with the highest PageRank:
    # Vertex: 597621, PageRank: 0.000644356692909492
    # Vertex: 41909, PageRank: 0.0006425477256693725
    # Vertex: 163075, PageRank: 0.0006305999262383353
    # Vertex: 537039, PageRank: 0.0006269920571772538
    # Vertex: 384666, PageRank: 0.0005489073817720516
    # Vertex: 504140, PageRank: 0.0005337169626427533
    # Vertex: 486980, PageRank: 0.000505691228595806
    # Vertex: 605856, PageRank: 0.0005008187129537594
    # Vertex: 32163, PageRank: 0.0004970646588593843
    # Vertex: 558791, PageRank: 0.0004947016865199656

    # Time elapsed: 2m 8.08s
    
def act6(page_graph: Graph):
    print("--------------------")
    print("         P6         ")
    print("--------------------")
    
    start = casio.time()
    print(f"Estimating the graph's circunference...")
    circunference = page_graph.find_circumference(timeout=10) # Change the timeout if needed. 5s works fine but 10s is more reliable.
    print(f"Estimated circunference of the graph: {circunference}")
    end = casio.time()
    
    processTime(start, end)
    print()
    
    # Estimating the graph's circunference...
    #         Cycle of length 214 found!                                                                                                                                                                           
    #         Cycle of length 321 found!                                                                                                                                                                           
    #         Cycle of length 327 found!                                                                                                                                                                           
    #         Cycle of length 330 found!                                                                                                                                                                           
    #         Cycle of length 331 found!                                                                                                                                                                           
    # Estimated circunference of the graph: 331
    # Time elapsed: 1m 37.0s
        
    
# Puntos extra

# def extra1(page_graph: Graph):
#     print("--------------------")
#     print("        Extra1      ")
#     print("--------------------")
    
#     # Programe una función genérica que extendiendo la definición del triángulo calcule la
#     # cantidad de polígonos de K lados. Haga un gráfico para mostrar la cantidad de
#     # polígonos por cantidad de lados, estimando aquellos que no pueda calcular. (+2
#     # puntos)
    
#     start = casio.time()
    

    
#     end = casio.time()
    
#     processTime(start, end)
#     print()
    
#     # Results
#     # Graph density: 1.0e-05
#     # Time elapsed: 0.0s

def extra2(page_graph: Graph, directed = False):
    print("--------------------")
    print("        Extra2      ")
    print("--------------------")
    
    start = casio.time()
    print("Calculating the graph's average clustering coefficient for an undirected graph...")
    clustering_coefficient = page_graph.average_clustering_coefficient_undirected()
    print(f"Average clustering coefficient for an undirected graph: {clustering_coefficient}")
    
    if directed:
        print("Calculating the graph's average clustering coefficient for a directed graph...")
        clustering_coefficient_directed = page_graph.average_clustering_coefficient_directed()
        print(f"Average clustering coefficient for a directed graph: {clustering_coefficient_directed}")
    
    end = casio.time()
    
    processTime(start, end)
    print()
    
    # Results
    # Average clustering coefficient for an undirected graph: 0.5142961475354295
    # Average clustering coefficient for a directed graph: 0.3651263215748557
    # Time elapsed: 16.24s
    
def extra3(page_graph: Graph):
    print("--------------------")
    print("        Extra3      ")
    print("--------------------")
    
    start = casio.time()
    n = 100
    print(f"Estimating the graph's betweenness centrality with {n} samples...")
    node, value = page_graph.betweenness_centrality(n, seed=None)
    print(f"Node with the highest betweenness centrality: {node}, Value: {value}")
    end = casio.time()
    
    processTime(start, end)
    print()
    
    # Results
    # Node with the highest betweenness centrality: 560622, Value: 48932.75
    # Time elapsed: 3m 42.17s
    
if __name__ == "__main__":
    page_graph = readGraph()
    
    # Actividades
    # act1(page_graph)
    # act2(page_graph)
    # act3(page_graph, undirected=False)
    # act4(page_graph)
    # act5(page_graph)
    act6(page_graph)
    
    # Extras
    # extra1(page_graph)
    # extra2(page_graph, directed=True)
    # extra3(page_graph)
    
    
    ciclo_1000= ['0', '891835', '867923', '857527', '852419', '659942', '874936', '908063', '893345', '877572', '855717', '838648', '816332', '786977', '756187', '667543', '601675', '502158', '639260', '483633', '849302', '810869', '52218', '835704', '912971', '885738', '684320', '868027', '886955', '293403', '798461', '852097', '889722', '787970', '364070', '33707', '577693', '774023', '226594', '880088', '419746', '885067', '530338', '859996', '361593', '816319', '792130', '893897', '870280', '871233', '853288', '754402', '675215', '286972', '350179', '896450', '721790', '862643', '823007', '677155', '840820', '438493', '877491', '814002', '891442', '865737', '790973', '858952', '804464', '786566', '914829', '912254', '750791', '834077', '771728', '770747', '764480', '732514', '554817', '70053', '146550', '622917', '610899', '552166', '547989', '891739', '870408', '807669', '713651', '701322', '664016', '623033', '907084', '896112', '894409', '585141', '547356', '517246', '385622', '810829', '829376', '816834', '789611', '706975', '888540', '648876', '788616', '618541', '573392', '457523', '884610', '879047', '852601', '861749', '763442', '873613', '619444', '848019', '581858', '733657', '522442', '809846', '514312', '452247', '525011', '81200', '871711', '884101', '423499', '398624', '903769', '903524', '849299', '844403', '822928', '901259', '799267', '580791', '331883', '824360', '276241', '864444', '722374', '570121', '383256', '444301', '728143', '803708', '378705', '902554', '427517', '839840', '667537', '531099', '859194', '877798', '853656', '425439', '778827', '760145', '538339', '472646', '748714', '265293', '405509', '765744', '144217', '834049', '616082', '3612', '785038', '776738', '760713', '811857', '776223', '877677', '849176', '904386', '853987', '819444', '570603', '518352', '480124', '313629', '810223', '804446', '151515', '785947', '19248', '453337', '789315', '899802', '874960', '587629', '490447', '393849', '896320', '794696', '728404', '316298', '898623', '892995', '855366', '797813', '789207', '765530', '750924', '754736', '749410', '113479', '749302', '633880', '624198', '250667', '825811', '815684', '857176', '605856', '881531', '823051', '853992', '901342', '874181', '799974', '713944', '329250', '173880', '858252', '810590', '663931', '821355', '647603', '872458', '909832', '875061', '768770', '768205', '696834', '794567', '722801', '495534', '856766', '696230', '897585', '602138', '597424', '666030', '509674', '280932', '647391', '888532', '779387', '671805', '772187', '680377', '858682', '915904', '908412', '787681', '531512', '679611', '543262', '96943', '812272', '864133', '775169', '823686', '426009', '283369', '752266', '740525', '893268', '775109', '719798', '378289', '795050', '591818', '712803', '690013', '537334', '549560', '489644', '433276', '900279', '499063', '419955', '739238', '215549', '838792', '649234', '529342', '418946', '173623', '816613', '124350', '908114', '700383', '652260', '566502', '462157', '61782', '827069', '758768', '607273', '794206', '901817', '753521', '872551', '651721', '846943', '910721', '894474', '827428', '450284', '362980', '188459', '817824', '821196', '133280', '643620', '536292', '630544', '245101', '833901', '584018', '446520', '871173', '602482', '785764', '397206', '815811', '242659', '571699', '223270', '722886', '773785', '382688', '603331', '821189', '821565', '754217', '548744', '137121', '847742', '218263', '35133', '698532', '789237', '865871', '161775', '718894', '866323', '257509', '819692', '433622', '619626', '185197', '835005', '803606', '905553', '863188', '808199', '371811', '706514', '818811', '388465', '775478', '884333', '672519', '847353', '864196', '772466', '670277', '371739', '908799', '1536', '793156', '651263', '351041', '891630', '881222', '829336', '908428', '889853', '805189', '871213', '873458', '897866', '762358', '908800', '753403', '641176', '751730', '878373', '737717', '589098', '877587', '552389', '503306', '659539', '797842', '694934', '497475', '453915', '442925', '442847', '423946', '789347', '771686', '753770', '726420', '604441', '415818', '313291', '183648', '177550', '581799', '855241', '709424', '795660', '869245', '839336', '798236', '820907', '574818', '561025', '493845', '451475', '674717', '913809', '750703', '722549', '479672', '467530', '223242', '865005', '912253', '640076', '731971', '60543', '869944', '713724', '910413', '830204', '474704', '801989', '199821', '642014', '889171', '712981', '750263', '835925', '808187', '791018', '769621', '689600', '714270', '625782', '691766', '427421', '813742', '814507', '204941', '862361', '614173', '90692', '847369', '832384', '739535', '703671', '684769', '570086', '557014', '546925', '757595', '907359', '882944', '901913', '800326', '731766', '486892', '131671', '353858', '881972', '696746', '629798', '645237', '548664', '846610', '848428', '812310', '789671', '754869', '718006', '573325', '568229', '701301', '821408', '543885', '89271', '851273', '845449', '744043', '878371', '912668', '457134', '884123', '815698', '910172', '908358', '896056', '819762', '878804', '806344', '535759', '854117', '767489', '739248', '611806', '593672', '494498', '471717', '380913', '413824', '501298', '665535', '824724', '714386', '856554', '912882', '765751', '675820', '803476', '153213', '115566', '859009', '873554', '848959', '546588', '696023', '601924', '530392', '487550', '302204', '26728', '775942', '231686', '479770', '666661', '674934', '864212', '691636', '812721', '647491', '641706', '732329', '724317', '845691', '192359', '839729', '872795', '520491', '325451', '425669', '523129', '377780', '779398', '571004', '798590', '751384', '886156', '908993', '813872', '532391', '776449', '766517', '663802', '712808', '762591', '812853', '593768', '914393', '588523', '498903', '879533', '870269', '859506', '840037', '911571', '910665', '890061', '866254', '778110', '756866', '625548', '499893', '665062', '307853', '824913', '425981', '423460', '363581', '528051', '912558', '859000', '742892', '710097', '699182', '559340', '738193', '441822', '445146', '434255', '359877', '310641', '264849', '709209', '690674', '260557', '776907', '365935', '130306', '474018', '220342', '212631', '94862', '708450', '752035', '712564', '890953', '518633', '736576', '872995', '564876', '896158', '787411', '846823', '592537', '903737', '627546', '560302', '812406', '729710', '779475', '104787', '915483', '710337', '700544', '912229', '857183', '870628', '863514', '727600', '858465', '156959', '703978', '509534', '808821', '505017', '536724', '822301', '811456', '291034', '885330', '840785', '785991', '339134', '154947', '878394', '794246', '735490', '631867', '628476', '517544', '505142', '842599', '485865', '864194', '849736', '576098', '862104', '642115', '906877', '717791', '688824', '466336', '452785', '393863', '292746', '237802', '153084', '267122', '151519', '912974', '905109', '829833', '591670', '838570', '890606', '800354', '829993', '857417', '718679', '898650', '662605', '820247', '845064', '901377', '868734', '719389', '630447', '899194', '857619', '597621', '895278', '889423', '698251', '821330', '729403', '904086', '913856', '814844', '858426', '838939', '710269', '655199', '469304', '584921', '389176', '377185', '262130', '675328', '229102', '679524', '735165', '227485', '537678', '245681', '224169', '387708', '116225', '513308', '733315', '97985', '350606', '730789', '850870', '791389', '863708', '876516', '73521', '768450', '732344', '836073', '754171', '654885', '590122', '852949', '648990', '890343', '886753', '734279', '706304', '747118', '911371', '809280', '613178', '858421', '873361', '827090', '421117', '107219', '909218', '122407', '893356', '864792', '798261', '775303', '853946', '808959', '747782', '915785', '783447', '684849', '802305', '814415', '913313', '738106', '654863', '730742', '860173', '228203', '779176', '783319', '893006', '511876', '878167', '826878', '529334', '457493', '676179', '295859', '546284', '884792', '835599', '564993', '435423', '841269', '823052', '537438', '280172', '190733', '894612', '893447', '860169', '813980', '802946', '737817', '846237', '727632', '633099', '309471', '706690', '484721', '674497', '385595', '547262', '872157', '46531', '914488', '861241', '589410', '827629', '868816', '900739', '837698', '915857', '835247', '787964', '899813', '906898', '410669', '885166', '904319', '894029', '854809', '834266', '654976', '906407', '870141', '270873', '841133', '821671', '885533', '758173', '894756', '451317', '817585', '886951', '486023', '890866', '802204', '711909', '85998', '693585', '858901', '529138', '732498', '571622', '851101', '525463', '230254', '905725', '836582', '812154', '915997', '766543', '574388', '711564', '419404', '801666', '761411', '789213', '800853', '45288', '902680', '553985', '844643', '914556', '457122', '410652', '886537', '319824', '117244', '795250', '905634', '632695', '913201', '914073', '906024', '901039', '881208', '867243', '852995', '829662', '871425', '753110', '792510', '635117', '779641', '420562', '627835', '913237', '887936', '861331', '872656', '909001', '827300', '883335', '857533', '551694', '453572', '448267', '424792', '342982', '294654', '833042', '254689', '200854', '858231', '913397', '881111', '596356', '810433', '910845', '361078', '845607', '817502', '857613', '584486', '613280', '548331', '519308', '878812', '866108', '749324', '835727', '438837', '325128', '906743', '683760', '767983', '685475', '426971', '26797', '84065', '684520', '150850', '102685', '907438', '860619', '400217', '625526', '51097', '174311', '334121', '841825', '510853', '904415', '787012', '781439', '754072', '208859', '715217', '604419', '840280', '583352', '901494', '884235', '438822', '860950', '148170', '376953', '407947', '664133', '775696', '470365', '596972', '846924', '875701', '405192', '786053', '496122', '140896', '845614', '540852', '445349', '745315', '871379', '600594', '0']
    
    # print(page_graph.checkIfPathExists(ciclo_1000))