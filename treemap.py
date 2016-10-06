def gettreemapdata(handler):
    level = handler.get_arguments('level')[0]
    geo = handler.get_arguments('geo')[0]
    datadict = {}
    if level == '3':
        if geo == 'AREA':
            result = gettreemapdatalevelone('area')
        elif geo == 'REGION':
            result = gettreemapdataleveltwo('region', 'area')
        else:
            result = gettreemapdatalevelthree('geography', 'region', 'area')
    else:
        if geo == 'AREA':
            result = gettreemapdataleveltwo('area', 'asc_name')
        elif geo == 'ASC':
            result = gettreemapdatalevelone('asc_name')
        elif geo == 'REGION':
            result = gettreemapdatalevelthree('region', 'area', 'asc_name')
        else:
            result = gettreemapdatalevelfour()
    datadict['root'] = result
    return datadict


def gettreemapdatalevelthree(parent, child, grandchild):
    df = pd.read_csv('datawith4levelwithagroupedvalue.csv')
    df['value'] = [randint(1, 100) for i in range(len(df))]
    size = 'value'
    dfgroup = df.groupby([parent, child, grandchild])[size].sum()
    dfgroup = dfgroup.reset_index()
    flare = {"name": "flare", "children": []}
    child_list = []
    for item in set(dfgroup[parent]):
        child_dict = {}
        child_dict['name'] = item
        regions = set(dfgroup[dfgroup[parent] == item][child])
        region_list = []
        for reg in regions:
            regdict = {}
            regdict['name'] = reg
            areas = set(dfgroup[dfgroup[child] == reg][grandchild])
            area_list = []
            for area in areas:
                area_dict = {}
                area_dict['name'] = area
                area_dict['value'] = int(
                    dfgroup[dfgroup[grandchild] == area][size].iloc[0])
                area_list.append(area_dict)
            regdict['children'] = area_list
            region_list.append(regdict)
        child_dict['children'] = region_list
        child_list.append(child_dict)

    flare['children'] = child_list
    return json.dumps(flare)


def gettreemapdatalevelfour():
    df = pd.read_csv('datawith4levelwithagroupedvalue.csv')
    df['value'] = [randint(1, 100) for i in range(len(df))]
    parent = 'Geography'
    child = 'region'
    grandchild = 'area'
    greatgrandchild = 'asc_name'
    size = 'value'
    dfgroup = df.groupby([parent, child, grandchild, greatgrandchild])[
        size].sum()
    dfgroup = dfgroup.reset_index()
    flare = {"name": "flare", "children": []}
    child_list = []
    for dad in set(dfgroup[parent]):
        child_dict = {}
        child_dict['name'] = dad
        sons = set(dfgroup[dfgroup[parent] == dad][child])
        sonslist = []
        for son in sons:
            sonsdict = {}
            sonsdict['name'] = son
            gransons = set(dfgroup[dfgroup[child] == son][grandchild])
            grandsonslist = []
            for grandson in gransons:
                grandsondict = {}
                grandsondict['name'] = grandson
                ggsons = set(
                    dfgroup[
                        dfgroup[grandchild] == grandson][greatgrandchild])
                ggsonlist = []
                for ggson in ggsons:
                    ggsondic = {}
                    ggsondic['name'] = ggson
                    ggsondic['value'] = int(
                        dfgroup[dfgroup[greatgrandchild] == ggson][size].iloc[0])
                    ggsonlist.append(ggsondic)
                grandsondict['children'] = ggsonlist
                grandsonslist.append(grandsondict)
            sonsdict['children'] = grandsonslist
            sonslist.append(sonsdict)
        child_dict['children'] = sonslist
        child_list.append(child_dict)

    flare['children'] = child_list
    return json.dumps(flare)


def gettreemapdataleveltwo(parent, child):
    df = pd.read_csv('datawith4levelwithagroupedvalue.csv')
    df['value'] = [randint(1, 100) for i in range(len(df))]
    size = 'value'
    dfgroup = df.groupby([parent, child])[size].sum()
    dfgroup = dfgroup.reset_index()
    flare = {"name": "flare", "children": []}
    parentlist = []
    for item in set(dfgroup[parent]):
        parent_dict = {}
        parent_dict['name'] = item
        sons = set(dfgroup[dfgroup[parent] == item][child])
        sonslist = []
        for son in sons:
            sonsdict = {}
            sonsdict['name'] = son
            sonsdict['value'] = int(
                dfgroup[dfgroup[child] == son][size].iloc[0])
            sonslist.append(sonsdict)
        parent_dict['children'] = sonslist
        parentlist.append(parent_dict)
    flare['children'] = parentlist
    return json.dumps(flare)


def gettreemapdatalevelone(parent):
    df = pd.read_csv('datawith4levelwithagroupedvalue.csv')
    df['value'] = [randint(1, 100) for i in range(len(df))]
    size = 'value'
    dfgroup = df.groupby(parent)[size].sum()
    dfgroup = dfgroup.reset_index()
    flare = {"name": "flare", "children": []}
    parentlist = []
    for item in set(dfgroup[parent]):
        parent_dict = {}
        parent_dict['name'] = item
        parent_dict['value'] = int(
            dfgroup[dfgroup[parent] == item][size].iloc[0])
        parentlist.append(parent_dict)
    flare['children'] = parentlist
    return json.dumps(flare)